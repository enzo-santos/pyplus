import typing

import xlrd  # type: ignore[import-untyped]

M = typing.TypeVar("M")


def _read_lines(
    fpath: str,
    *,
    sheet_index: int = 0,
    skiprows: int = 0,
) -> typing.Iterator[list[typing.Any]]:
    with xlrd.open_workbook(fpath, on_demand=True) as wb:
        ws = wb.sheet_by_index(sheet_index)
        for i in range(ws.nrows):
            if i < skiprows:
                continue

            yield [cell.value for cell in ws.row(i)]


def _read_models(
    fpath: str,
    *,
    sheet_index: int = 0,
    header: int = 0,
    converter: typing.Callable[[dict[str, typing.Any]], M],
) -> typing.Iterator[M]:
    with xlrd.open_workbook(fpath, on_demand=True) as wb:
        ws = wb.sheet_by_index(sheet_index)

        keys: list[str]
        for i in range(ws.nrows):
            if i < header:
                continue

            values: list[typing.Any]
            values = [cell.value for cell in ws.row(i)]
            if i == header:
                keys = typing.cast(list[str], values)
                continue

            data: dict[str, typing.Any]
            data = {
                key: values[i] if i < len(values) else None
                for i, key in enumerate(keys)
            }
            yield converter(data)
