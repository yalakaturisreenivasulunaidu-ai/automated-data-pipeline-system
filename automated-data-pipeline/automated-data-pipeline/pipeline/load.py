"""Load stage: writes the clean data to its destination(s).

Currently supports SQLite and CSV output. Add methods for other
destinations (Postgres, S3, a REST API, ...) as needed.
"""

import os
import sqlite3

import pandas as pd

from pipeline.logger import get_logger

logger = get_logger(__name__)


class Loader:
    def __init__(self, config: dict):
        cfg = config["load"]
        self.sqlite_path = cfg["sqlite_path"]
        self.table_name = cfg["table_name"]
        self.output_csv = cfg["output_csv"]

    def load(self, df: pd.DataFrame) -> None:
        self._load_to_sqlite(df)
        self._load_to_csv(df)

    def _load_to_sqlite(self, df: pd.DataFrame) -> None:
        os.makedirs(os.path.dirname(self.sqlite_path) or ".", exist_ok=True)
        with sqlite3.connect(self.sqlite_path) as conn:
            df.to_sql(self.table_name, conn, if_exists="replace", index=False)
        logger.info(
            "Loaded %d rows into SQLite table '%s' (%s)",
            len(df), self.table_name, self.sqlite_path,
        )

    def _load_to_csv(self, df: pd.DataFrame) -> None:
        os.makedirs(os.path.dirname(self.output_csv) or ".", exist_ok=True)
        df.to_csv(self.output_csv, index=False)
        logger.info("Wrote processed CSV to %s", self.output_csv)
