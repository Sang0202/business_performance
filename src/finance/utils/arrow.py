from __future__ import annotations
from typing import List
import os

import pandas as pd
import pyarrow as pa
from pyarrow import feather


def read_arrow(filename: str, columns: List[str] | None = None) -> pa.Table:
    return feather.read_table(filename, columns=columns)


def read_pandas(filename: str, columns: List[str] | None = None) -> pd.DataFrame:
    tb = read_arrow(filename, columns=columns)
    # return tb.to_pandas(types_mapper=pd.ArrowDtype)
    return tb.to_pandas()


def write_arrow(
    tb: pa.Table | pd.DataFrame,
    filename: str,
    compression="lz4",
    chunk_size=None,
    version=2,
):
    feather.write_feather(
        tb, filename, compression=compression, chunksize=chunk_size, version=version
    )


def create_path(file_path: str):
    parent_path, filename = os.path.split(file_path)
    if parent_path and not os.path.exists(parent_path):
        os.makedirs(parent_path, exist_ok=True)
