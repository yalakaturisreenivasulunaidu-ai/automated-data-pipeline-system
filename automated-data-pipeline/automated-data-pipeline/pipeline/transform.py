"""Transform stage: cleans, validates, and enriches the extracted data."""

import pandas as pd

from pipeline.logger import get_logger

logger = get_logger(__name__)


class Transformer:
    def __init__(self, config: dict):
        cfg = config.get("transform", {})
        self.drop_duplicates = cfg.get("drop_duplicates", True)
        self.dropna_columns = cfg.get("dropna_columns", [])
        self.derived_columns = cfg.get("derived_columns", {})

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._clean_column_names(df)
        df = self._drop_invalid_rows(df)
        df = self._add_derived_columns(df)
        self._validate(df)
        logger.info("Transformed data: %d rows, %d columns", *df.shape)
        return df

    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        return df

    def _drop_invalid_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)

        cols_present = [c for c in self.dropna_columns if c in df.columns]
        if cols_present:
            df = df.dropna(subset=cols_present)

        if self.drop_duplicates:
            df = df.drop_duplicates()

        after = len(df)
        logger.info("Dropped %d invalid/duplicate row(s)", before - after)
        return df.reset_index(drop=True)

    def _add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for new_col, expression in self.derived_columns.items():
            try:
                df[new_col] = df.eval(expression)
                logger.info("Added derived column '%s' = %s", new_col, expression)
            except Exception as exc:
                logger.warning(
                    "Skipping derived column '%s' (%s): %s", new_col, expression, exc
                )
        return df

    def _validate(self, df: pd.DataFrame) -> None:
        if df.empty:
            raise ValueError("Transformed DataFrame is empty — check your inputs.")
        if df.isnull().values.any():
            null_counts = df.isnull().sum()
            logger.warning(
                "Remaining null values after cleaning:\n%s",
                null_counts[null_counts > 0].to_string(),
            )
