import os
import json
import typing

import requests

P = typing.TypeVar("P", str, bytes, os.PathLike)

ResponseType = typing.Literal["text", "binary", "json"]


def _write(url: str, fpath: P, *, force: bool = False, ftype: ResponseType) -> P:
    if not force and os.path.isfile(fpath):
        return fpath

    response = requests.get(url)
    if not response.ok:
        raise ValueError(response.status_code)

    try:
        os.makedirs(os.path.dirname(fpath))
    except FileExistsError:
        pass

    match ftype:
        case "text":
            with open(fpath, "w+", encoding="utf-8") as f:
                f.write(response.text)

        case "binary":
            with open(fpath, "wb+") as f:
                f.write(response.content)

        case "json":
            with open(fpath, "w+", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=2)

    return fpath
