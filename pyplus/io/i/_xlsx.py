import typing
import contextlib

import openpyxl

def _Reader(fpath: str, *, header: bool = True) -> typing.Iterable[list[typing.Any]]:
    with contextlib.closing(openpyxl.load_workbook(filename=fpath, read_only=True)) as wb:
        ws = wb.active
        if ws is None:
            return

        for i, row in enumerate(ws.rows): # type: ignore 
            if i == 0 and header:
                continue

            yield [cell.value for cell in row]