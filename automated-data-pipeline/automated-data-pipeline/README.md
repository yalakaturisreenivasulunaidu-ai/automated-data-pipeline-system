# Automated Data Pipeline System

A simple, extensible ETL (Extract → Transform → Load) pipeline written in
Python. It's meant as a clean starting point you can build on: swap in real
data sources, add new transformation steps, or point the loader at a real
database.

## Features

- **Config-driven** — all paths and settings live in `config/config.yaml`,
  nothing is hardcoded.
- **Extract** — reads one or more CSV files (easy to extend to APIs, DBs, S3…).
- **Transform** — cleans column names, drops duplicates/nulls, adds derived
  columns, and validates the result against simple rules.
- **Load** — writes the cleaned data to a local SQLite database and a
  processed CSV file.
- **Logging** — every run logs to both the console and a rotating log file
  under `logs/`.
- **Scheduling (optional)** — run once, or keep the pipeline running on an
  interval using the `schedule` library.
- **Tests** — a small pytest suite covering the transform step.

## Project structure

```
automated-data-pipeline/
├── config/
│   └── config.yaml          # pipeline settings
├── data/
│   ├── raw/                 # input CSVs go here
│   │   └── sample_sales.csv # example input data
│   └── processed/           # output lands here
├── logs/                    # run logs (created automatically)
├── pipeline/
│   ├── __init__.py
│   ├── extract.py           # Extractor: reads raw data
│   ├── transform.py         # Transformer: cleans & enriches data
│   ├── load.py              # Loader: writes to SQLite + CSV
│   ├── pipeline.py          # Pipeline: wires the stages together
│   └── logger.py            # shared logging setup
├── tests/
│   └── test_transform.py
├── main.py                  # entry point (run once or on a schedule)
├── requirements.txt
└── README.md
```

## Quick start

```bash
# 1. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the pipeline once
python main.py

# 4. Or run it continuously on the schedule defined in config.yaml
python main.py --schedule
```

Output appears in `data/processed/` (CSV) and `data/pipeline.db` (SQLite),
and every run is logged to `logs/pipeline.log`.

## Configuration

Edit `config/config.yaml`:

```yaml
pipeline:
  name: "sales_pipeline"

extract:
  input_dir: "data/raw"
  file_pattern: "*.csv"

transform:
  drop_duplicates: true
  dropna_columns: ["order_id", "amount"]
  derived_columns:
    total_with_tax: "amount * 1.08"

load:
  sqlite_path: "data/pipeline.db"
  table_name: "sales"
  output_csv: "data/processed/sales_clean.csv"

schedule:
  interval_minutes: 60
```

## Extending it

- **New data source**: add a method to `pipeline/extract.py` (e.g.
  `extract_from_api`, `extract_from_database`) and call it from
  `Pipeline.run()`.
- **New transform step**: add a method to `pipeline/transform.py`'s
  `Transformer` class and call it inside `transform()`.
- **New destination**: add a method to `pipeline/load.py` (e.g. Postgres,
  S3, a REST API).

## Running tests

```bash
pytest
```
