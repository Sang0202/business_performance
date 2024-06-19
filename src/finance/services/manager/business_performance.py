from __future__ import annotations
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


class BusinessPerformance:
    def __init__(
        self, df: pd.DataFrame, ds: str, groups: dict, alias: dict | None = None
    ) -> None:
        self.df = df.copy()
        del df
        self.ds = ds
        self.groups = groups
        self.alias = {} if alias is None else alias
        assert isinstance(alias, dict)
        self.mask = None
        self.columns = []
        self.act_cols = []
        self._datetime()
        self._sum_by_group()

    def _sum_by_group(self) -> None:
        act_keys = ["actual_cost", "actual_revenue", "actual_profit"]
        for k, v in self.groups.items():
            columns = v.get("columns")
            name = v.get("name")
            if columns is None or name is None:
                raise ArithmeticError(f"columns and name cannot be null!")
            self.df[name] = self.df[columns].sum(axis=1)
            self.columns.extend(columns)
            self.columns.append(name)
            if k in act_keys:
                self.act_cols.extend(columns)
                self.act_cols.append(name)

        groups = self.groups
        profit_name = self.alias.get("actual_profit", "actual_profit")
        projected_profit_name = self.alias.get("projected_profit", "projected_profit")
        self.df[profit_name] = (
            self.df[groups["actual_revenue"]["name"]]
            - self.df[groups["actual_cost"]["name"]]
        )
        self.columns.append(profit_name)
        self.act_cols.append(profit_name)
        if "projected_cost" in groups and "projected_revenue" in groups:
            self.df[projected_profit_name] = (
                self.df[groups["projected_revenue"]["name"]]
                - self.df[groups["projected_cost"]["name"]]
            )
            self.columns.append(projected_profit_name)

    def _datetime(self) -> None:
        ds_dtype = self.df[self.ds].dtype
        if hasattr(ds_dtype, "pyarrow_dtype"):
            ds_dtype = getattr(ds_dtype, "pyarrow_dtype")
        if ds_dtype in ["string", "object", "double", "float"]:
            self.df[self.ds] = pd.to_datetime(self.df[self.ds])

    def _mask(self, ds_filter: dict) -> pd.Series:
        self.mask = pd.DataFrame([self.df[k] == v for k, v in ds_filter.items()]).all()
        self.ds_filter = ds_filter

    def _percent_change(
        self, same: str = "year", previous: str = "month"
    ) -> pd.DataFrame:
        mc_columns = self.act_cols

        result = self.df.copy()
        result = result.sort_values(by=[same, previous])
        result[mc_columns] = result.groupby(by=same)[mc_columns].pct_change() * 100

        def fix_na(row):
            bl = result[previous] == (row[previous] - 1)
            for key in self.ds_filter:
                if key != previous:
                    bl = bl & (result[key] == row[key])
            if not result[bl].any(axis=None):
                row[mc_columns] = np.nan
            return row

        result = result.apply(fix_na, axis=1)
        na_columns = [col for col in self.columns if col not in mc_columns]
        result[na_columns] = np.nan

        return result.loc[self.mask].reset_index(drop=True).round(2)

    def _group_by_time(self, ds_filter: dict, agg_fn: str = "sum") -> None:
        ds_funcs = {
            "year": lambda x: self.df[x].dt.year,
            "quarter": lambda x: self.df[x].dt.quarter,
            "month": lambda x: self.df[x].dt.month,
        }
        if agg_fn not in ["sum", "mean"]:
            raise AttributeError(f"not support function {agg_fn}")
        for ds_key in ds_filter:
            ds_func = ds_funcs.get(ds_key)
            if ds_func is None:
                raise AttributeError(f"{ds_key} filter is not supported")
            self.df[ds_key] = ds_func(self.ds)
        agg_ojb = {col: agg_fn for col in self.columns}
        self.df = self.df.groupby(list(ds_filter.keys())).agg(agg_ojb).reset_index()
        self._mask(ds_filter=ds_filter)

    def total_by_time(self) -> pd.DataFrame:
        return self.df[self.mask].reset_index(drop=True)

    def percent_by_total(self) -> pd.DataFrame:
        current_columns = []
        result = self.df.copy()
        for elem in self.groups.values():
            columns = elem.get("columns")
            current_columns.extend(columns)
            name = elem.get("name")
            for col in columns:
                result[col] = (self.df[col] / self.df[name]) * 100
        na_columns = [col for col in self.columns if col not in current_columns]
        result[na_columns] = np.nan
        return result[self.mask].reset_index(drop=True).round(2)

    def percent_by_kpi(self) -> pd.DataFrame:
        pairs = [
            ("actual_cost", "projected_cost"),
            ("actual_revenue", "projected_revenue"),
            ("actual_profit", "projected_profit"),
        ]
        current_columns = []
        result = self.df.copy()
        for act, proj in pairs:
            act_val = self.groups.get(act)
            proj_val = self.groups.get(proj)
            if act_val is None or proj_val is None:
                continue
            act_columns = act_val.get("columns")
            proj_columns = proj_val.get("columns")
            assert isinstance(act_columns, list) and isinstance(proj_columns, list)
            if len(act_columns) != len(proj_columns):
                raise AttributeError(f"{act} and {proj} columns not same length")
            for x, y in zip(act_columns, proj_columns):
                result[x] = (result[x] / result[y]) * 100
                current_columns.append(x)
            act_name = act_val.get("name")
            proj_name = proj_val.get("name")
            if act_name is None or proj_name is None:
                continue
            result[act_name] = (result[act_name] / result[proj_name]) * 100
            current_columns.append(act_name)

            act_profit = self.alias.get(act)
            proj_profit = self.alias.get(proj)
            if act_profit is None or proj_profit is None:
                continue
            result[act_profit] = (result[act_profit] / result[proj_profit]) * 100
            current_columns.append(act_profit)
        na_columns = [col for col in self.columns if col not in current_columns]
        result[na_columns] = np.nan
        return result[self.mask].reset_index(drop=True).round(2)

    def percent_change_month(self) -> pd.DataFrame:
        return self._percent_change(same="year", previous="month")

    def percent_change_year(self) -> pd.DataFrame:
        return self._percent_change(same="month", previous="year")


def business_performance(
    df: pd.DataFrame,
    ds: str,
    groups: dict,
    alias: dict,
    ds_filter: dict,
    agg_fn: str = "sum",
    report: list = [
        "total_by_time",
        "percent_by_time",
        "percent_kpi",
        "percent_change_month",
        "percent_change_year",
    ],
    **kwargs,
) -> pd.DataFrame:
    bz_perfm = BusinessPerformance(df=df, ds=ds, groups=groups, alias=alias)
    bz_perfm._group_by_time(ds_filter=ds_filter, agg_fn=agg_fn)
    lst = []
    for med in report:
        if not hasattr(bz_perfm, med):
            raise NotImplementedError(f"{med} is not imppelemented")
        lst.append(getattr(bz_perfm, med)())
    if len(lst) == 1:
        return lst[0]
    result = pd.concat(lst, ignore_index=True)
    result.drop(columns=list(ds_filter.keys()), inplace=True)
    result["report"] = report
    del bz_perfm.df
    return result
