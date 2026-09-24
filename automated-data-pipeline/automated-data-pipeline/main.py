"""Entry point for the Automated Data Pipeline System.

Usage:
    python main.py                # run the pipeline once
    python main.py --schedule     # run it repeatedly on the configured interval
"""

import argparse
import time

from pipeline.pipeline import Pipeline
from pipeline.logger import get_logger

logger = get_logger("main")


def run_once() -> None:
    pipeline = Pipeline()
    pipeline.run()


def run_on_schedule() -> None:
    import schedule

    pipeline = Pipeline()
    interval = pipeline.config.get("schedule", {}).get("interval_minutes", 60)

    logger.info("Scheduling pipeline to run every %d minute(s)", interval)
    schedule.every(interval).minutes.do(pipeline.run)

    # Run once immediately, then wait for the schedule.
    pipeline.run()
    while True:
        schedule.run_pending()
        time.sleep(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Automated Data Pipeline System")
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run continuously on the interval defined in config.yaml",
    )
    args = parser.parse_args()

    if args.schedule:
        run_on_schedule()
    else:
        run_once()


if __name__ == "__main__":
    main()
