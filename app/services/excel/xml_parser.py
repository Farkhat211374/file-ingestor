import zipfile
from xml.etree.ElementTree import iterparse

from app.services.excel.config import COLUMN_MAPPING, BATCH_SIZE


def extract_shared_strings(zip_file: zipfile.ZipFile):
    shared_strings = []
    with zip_file.open("xl/sharedStrings.xml") as f:
        for _, elem in iterparse(f):
            if elem.tag.endswith("t"):
                shared_strings.append(elem.text)
    return shared_strings

def parse_row(elem, shared_strings):
    row = []
    for c in elem:
        if c.tag.endswith("c"):
            v = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
            if v is not None:
                val = v.text
                if c.attrib.get('t') == 's':
                    val = shared_strings[int(val)] if val.isdigit() else ''
                row.append(val)
    return row

def chunked_rows(zip_file: zipfile.ZipFile, shared_strings, header: list[str], chunk_size: int = BATCH_SIZE):
    mapped_header = [COLUMN_MAPPING.get(col, col) for col in header]
    first_row_skipped = False

    with zip_file.open("xl/worksheets/sheet1.xml") as f:
        current_chunk = []
        for event, elem in iterparse(f, events=("start", "end")):
            if elem.tag.endswith("row") and event == "end":
                if not first_row_skipped:
                    first_row_skipped = True
                    elem.clear()
                    continue  # пропустить заголовок
                row = parse_row(elem, shared_strings)
                if len(row) != len(mapped_header):
                    elem.clear()
                    continue
                record = dict(zip(mapped_header, row))
                current_chunk.append(record)
                if len(current_chunk) >= chunk_size:
                    yield current_chunk
                    current_chunk = []
                elem.clear()
        if current_chunk:
            yield current_chunk