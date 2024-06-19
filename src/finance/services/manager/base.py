#!/usr/bin/env python3
from __future__ import annotations
import pandas as pd


def select(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return df[columns]


def drop(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return df.drop(columns=columns)


def drop_nulls(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    return df.dropna(subset=columns)


def rename(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    mapper = {k: v for k, v in mapping.items() if k in df}
    return df.rename(mapper=mapper)
