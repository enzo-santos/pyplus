import csv
import typing

import itertools

M = typing.TypeVar("M")


def _read_lines(
    fpath: str,
    *,
    delimiter=";",
    skiprows: int = 0,
) -> typing.Iterator[list[str]]:
    with open(fpath, encoding="utf-8") as f:
        reader: typing.Iterator[list[str]]
        reader = csv.reader(f, delimiter=delimiter)
        if skiprows:
            reader = itertools.islice(reader, skiprows, None)

        yield from reader


def _read_models(
    fpath: str,
    *,
    delimiter=";",
    header: int = 0,
    converter: typing.Callable[[dict[str, str]], M],
) -> typing.Iterator[M]:
    with open(fpath, encoding="utf-8") as f:
        file: typing.Iterator[str] = f
        if header:
            file = itertools.islice(file, header, None)

        reader = csv.DictReader(file, delimiter=";")
        for record in reader:
            yield converter(record)
