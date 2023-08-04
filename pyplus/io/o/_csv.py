import csv
import typing
import collections.abc


CsvValue = int | float | str | None
CsvRow = typing.Iterable[CsvValue]
class CsvWriter(typing.Protocol):
    def writerow(self, row: CsvRow) -> CsvRow: ...
    def writerows(self, rows: typing.Iterable[CsvRow]) -> None: ...
    def __enter__(self, *args, **kwargs) -> 'CsvWriter': ...
    def __exit__(self, *args, **kwargs) -> None: ... 


class _Writer:
    path: str
    delimiter: str
    header: collections.abc.Sequence[str] | None
    _c_file: typing.TextIO | None
    _c_writer: CsvWriter | None
    _has_header: bool


    def __init__(
        self,
        path: str,
        *,
        delimiter: str = ';',
        header: collections.abc.Sequence[str] | None = None,
    ):
        self.path = path
        self.delimiter = delimiter
        self.header = header

        self._has_header = False
        self._c_writer = None
        self._c_file = None


    @property
    def _writer(self) -> CsvWriter:
        _c_writer = self._c_writer

        writer: CsvWriter
        if _c_writer is None:
            file = open(self.path, 'w+', encoding='utf-8', newline='')
            writer = csv.writer(file, delimiter=self.delimiter) # type: ignore[assignment]
            self._c_file = file
            self._c_writer = writer
        else:
            writer = _c_writer

        return writer


    def _write_header(self) -> bool:
        header = self.header
        if self._has_header or header is None:
            return False

        self._writer.writerow(header)
        self._has_header = True
        return True


    def writeheader(self) -> bool:
        return self._write_header()

    def writerow(self, row: CsvRow) -> CsvRow:
        self._write_header()
        return self._writer.writerow(row)


    def writerows(self, row: typing.Iterable[CsvRow]) -> None:
        self._write_header()
        return self._writer.writerows(row)


    def close(self) -> None:
        file = self._c_file
        if file is None:
            return

        file.close()


    def __enter__(self, *args, **kwargs) -> CsvWriter:
        writer = self._writer
        return self


    def __exit__(self, *args, **kwargs) -> None:
        self.close()
