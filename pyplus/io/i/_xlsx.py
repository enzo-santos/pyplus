import typing
import contextlib

import openpyxl

def _Reader(fpath: str, *, header: bool = True, index: int | None = None) -> typing.Iterable[list[typing.Any]]:
    with contextlib.closing(openpyxl.load_workbook(filename=fpath, read_only=True)) as wb:
        if index is None:
            ws = wb.active
        else:
            ws = wb.worksheets[index]

        if ws is None:
            return

        for i, row in enumerate(ws.rows): # type: ignore 
            if i == 0 and header:
                continue

            yield [cell.value for cell in row]
