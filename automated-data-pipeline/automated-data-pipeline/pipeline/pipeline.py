"""Wires the Extract, Transform, and Load stages into a single run."""

import time

import yaml

from pipeline.extract import Extractor
from pipeline.transform import Transformer
from pipeline.load import Loader
from pipeline.logger import get_logger

logger = get_logger(__name__)


def load_config(path: str = "config/config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


class Pipeline:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = load_config(config_path)
        self.extractor = Extractor(self.config)
        self.transformer = Transformer(self.config)
        self.loader = Loader(self.config)

    def run(self) -> None:
        name = self.config["pipeline"]["name"]
        start = time.time()
        logger.info("=== Starting pipeline run: %s ===", name)

        try:
            raw_df = self.extractor.extract()
            clean_df = self.transformer.transform(raw_df)
            self.loader.load(clean_df)
        except Exception:
            logger.exception("Pipeline run failed")
            raise
        else:
            elapsed = time.time() - start
            logger.info(
                "=== Pipeline run '%s' completed successfully in %.2fs ===",
                name, elapsed,
            )
