from __future__ import annotations
import pandas as pd
from titan.finance.services import manager


def worker(df: pd.DataFrame, operations: list[dict]) -> pd.DataFrame:
    for operation in operations:
        operator = operation.get("operator")

        if operator is None:
            raise ValueError("operator cannot be null!")
        options = operation.get("options", {})

        if not hasattr(manager, operator):
            raise AttributeError(f"Unsupported operator {operator}")

        df = getattr(manager, operator)(df, **options)

    return df
