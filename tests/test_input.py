import io
import os
import typing
import tempfile
import unittest
import functools

import pyplus.io.i


class _TempWriting:
    delimiter: str
    _file: typing.IO
    _closed: bool

    def __init__(self, file: typing.IO, delimiter: str) -> None:
        self.delimiter = delimiter
        self._file = file
        self._closed = False

    def write(self, *args: object) -> None:
        if self._closed:
            raise RuntimeError("the file is closed")
        print(*args, sep=self.delimiter, file=self._file)

    def close(self):
        if not self._closed:
            self._file.close()
        os.remove(self._file.name)

    @property
    def path(self) -> str:
        if not self._closed:
            self._file.close()
            self._closed = True
        return self._file.name


class _TempWriter:
    delimiter: str
    _writing: _TempWriting | None

    def __init__(self, delimiter: str) -> None:
        self.delimiter = delimiter
        self._writing = None

    def __enter__(self) -> _TempWriting:
        file = tempfile.NamedTemporaryFile("w+", delete=False, dir=".")
        writing = _TempWriting(file, self.delimiter)
        self._writing = writing
        return writing

    def __exit__(self, *args, **kwargs) -> None:
        if (writing := self._writing) is not None:
            writing.close()


T = typing.TypeVar("T")


class _TestCase(unittest.TestCase):
    def assertNext(self, iterator: typing.Iterator[T], value: T):
        self.assertEqual(next(iterator), value)

    def assertEnds(self, iterator: typing.Iterator[T]):
        self.assertRaises(StopIteration, next, iterator)


class CsvLinesTestCase(_TestCase):
    def test_shouldConsiderSemicolonAsDelimiter(self):
        with _TempWriter(delimiter=";") as writing:
            writing.write("Name", "Plays", "Alive")
            writing.write("Paul McCartney", "Bass", "True")
            writing.write("John Lennon", "Guitar", "False")
            writing.write("George Harrison", "Guitar", "False")
            writing.write("Ringo Starr", "Drums", "True")

            iterator = pyplus.io.i.csv_lines(writing.path, delimiter=";")
            self.assertNext(iterator, ["Name", "Plays", "Alive"])
            self.assertNext(iterator, ["Paul McCartney", "Bass", "True"])
            self.assertNext(iterator, ["John Lennon", "Guitar", "False"])
            self.assertNext(iterator, ["George Harrison", "Guitar", "False"])
            self.assertNext(iterator, ["Ringo Starr", "Drums", "True"])
            self.assertEnds(iterator)

    def test_shouldConsiderCommaAsDelimiter(self):
        with _TempWriter(delimiter=",") as writing:
            writing.write("Name", "Plays", "Alive")
            writing.write("Paul McCartney", "Bass", "True")
            writing.write("John Lennon", "Guitar", "False")
            writing.write("George Harrison", "Guitar", "False")
            writing.write("Ringo Starr", "Drums", "True")

            iterator = pyplus.io.i.csv_lines(writing.path, delimiter=",")
            self.assertNext(iterator, ["Name", "Plays", "Alive"])
            self.assertNext(iterator, ["Paul McCartney", "Bass", "True"])
            self.assertNext(iterator, ["John Lennon", "Guitar", "False"])
            self.assertNext(iterator, ["George Harrison", "Guitar", "False"])
            self.assertNext(iterator, ["Ringo Starr", "Drums", "True"])
            self.assertEnds(iterator)

    def test_shouldSkipRows(self):
        with _TempWriter(delimiter=";") as writing:
            writing.write("Name", "Plays", "Alive")
            writing.write("Paul McCartney", "Bass", "True")
            writing.write("John Lennon", "Guitar", "False")
            writing.write("George Harrison", "Guitar", "False")
            writing.write("Ringo Starr", "Drums", "True")

            iterator = pyplus.io.i.csv_lines(writing.path, skiprows=1)
            self.assertNext(iterator, ["Paul McCartney", "Bass", "True"])
            self.assertNext(iterator, ["John Lennon", "Guitar", "False"])
            self.assertNext(iterator, ["George Harrison", "Guitar", "False"])
            self.assertNext(iterator, ["Ringo Starr", "Drums", "True"])
            self.assertEnds(iterator)


class CsvModelsTestCase(_TestCase):
    def test_shouldConsiderSemicolonAsDelimiter(self):
        with _TempWriter(delimiter=";") as writing:
            writing.write("Name", "Plays", "Alive")
            writing.write("Paul McCartney", "Bass", "True")
            writing.write("John Lennon", "Guitar", "False")
            writing.write("George Harrison", "Guitar", "False")
            writing.write("Ringo Starr", "Drums", "True")

            iterator = pyplus.io.i.csv_models(
                writing.path,
                delimiter=";",
                converter=lambda x: x,
            )
            self.assertNext(
                iterator,
                {"Name": "Paul McCartney", "Plays": "Bass", "Alive": "True"},
            )
            self.assertNext(
                iterator,
                {"Name": "John Lennon", "Plays": "Guitar", "Alive": "False"},
            )
            self.assertNext(
                iterator,
                {"Name": "George Harrison", "Plays": "Guitar", "Alive": "False"},
            )
            self.assertNext(
                iterator,
                {"Name": "Ringo Starr", "Plays": "Drums", "Alive": "True"},
            )
            self.assertEnds(iterator)

    def test_shouldConsiderCommaAsDelimiter(self):
        with _TempWriter(delimiter=",") as writing:
            writing.write("Name", "Plays", "Alive")
            writing.write("Paul McCartney", "Bass", "True")
            writing.write("John Lennon", "Guitar", "False")
            writing.write("George Harrison", "Guitar", "False")
            writing.write("Ringo Starr", "Drums", "True")

            iterator = pyplus.io.i.csv_models(
                writing.path,
                delimiter=",",
                converter=lambda x: x,
            )
            self.assertNext(
                iterator,
                {"Name": "Paul McCartney", "Plays": "Bass", "Alive": "True"},
            )
            self.assertNext(
                iterator,
                {"Name": "John Lennon", "Plays": "Guitar", "Alive": "False"},
            )
            self.assertNext(
                iterator,
                {"Name": "George Harrison", "Plays": "Guitar", "Alive": "False"},
            )
            self.assertNext(
                iterator,
                {"Name": "Ringo Starr", "Plays": "Drums", "Alive": "True"},
            )
            self.assertEnds(iterator)

    def test_shouldSkipRows(self):
        with _TempWriter(delimiter=",") as writing:
            writing.write("Some", "Random", "Data")
            writing.write("Name", "Plays", "Alive")
            writing.write("Paul McCartney", "Bass", "True")
            writing.write("John Lennon", "Guitar", "False")
            writing.write("George Harrison", "Guitar", "False")
            writing.write("Ringo Starr", "Drums", "True")

            iterator = pyplus.io.i.csv_models(
                writing.path,
                delimiter=",",
                converter=lambda x: x,
                header=1,
            )
            self.assertNext(
                iterator,
                {"Name": "Paul McCartney", "Plays": "Bass", "Alive": "True"},
            )
            self.assertNext(
                iterator,
                {"Name": "John Lennon", "Plays": "Guitar", "Alive": "False"},
            )
            self.assertNext(
                iterator,
                {"Name": "George Harrison", "Plays": "Guitar", "Alive": "False"},
            )
            self.assertNext(
                iterator,
                {"Name": "Ringo Starr", "Plays": "Drums", "Alive": "True"},
            )
            self.assertEnds(iterator)


if __name__ == "__main__":
    unittest.main()
