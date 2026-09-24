"""Extract stage: pulls raw data into pandas DataFrames.

Currently supports reading CSV files from a local directory. Add new
methods (extract_from_api, extract_from_database, extract_from_s3, ...)
to plug in additional sources.
"""

import glob
import os

import pandas as pd

from pipeline.logger import get_logger

logger = get_logger(__name__)


class Extractor:
    def __init__(self, config: dict):
        self.input_dir = config["extract"]["input_dir"]
        self.file_pattern = config["extract"].get("file_pattern", "*.csv")

    def extract(self) -> pd.DataFrame:
        """Read every file matching the pattern and concatenate them."""
        search_path = os.path.join(self.input_dir, self.file_pattern)
        files = sorted(glob.glob(search_path))

        if not files:
            raise FileNotFoundError(
                f"No input files found matching '{search_path}'."
            )

        logger.info("Found %d input file(s): %s", len(files), files)

        frames = []
        for file_path in files:
            logger.info("Reading %s", file_path)
            frames.append(pd.read_csv(file_path))

        df = pd.concat(frames, ignore_index=True)
        logger.info("Extracted %d rows, %d columns", *df.shape)
        return df
