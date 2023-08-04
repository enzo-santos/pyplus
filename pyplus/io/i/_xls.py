import typing

import xlrd

def _Reader(fpath: str, *, header: bool = False) -> typing.Iterable[list[typing.Any]]:
    with xlrd.open_workbook(fpath, on_demand=True) as wb:
        ws = wb.sheet_by_index(0)
        for i in range(ws.nrows):
            if i == 0 and header:
                continue

            yield [cell.value for cell in ws.row(i)]
