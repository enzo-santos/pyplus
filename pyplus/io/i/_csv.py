import csv
import typing


def _Reader(fpath: str, *, delimiter: str = ';', header: bool = False) -> typing.Iterable[list[typing.Any]]:
    with open(fpath, encoding='utf-8') as f:
        for i, row in enumerate(csv.reader(f, delimiter=delimiter)):
            if header and i == 0:
                continue

            yield row
