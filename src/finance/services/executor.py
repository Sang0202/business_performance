from __future__ import annotations
from py4j.java_collections import JavaMap
from .reporter import reporter
from titan.finance.utils.java import map_to_dict


def executor(service: str, params: dict | JavaMap) -> str:
    # fix convert JavaMap to Python dict.
    if isinstance(params, JavaMap):
        params = map_to_dict(params)

    if service == "reporter":
        return reporter(params)

    raise RuntimeError(f"Service «{service}» does not exist")
