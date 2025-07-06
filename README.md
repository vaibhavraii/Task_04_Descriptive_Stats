# Task 04 – Descriptive Statistics Engine

This repository contains three independent implementations that produce identical descriptive-statistics outputs for the 2024 US-presidential-election social-media dataset:

| Script | Tech stack |
|--------|------------|
| `pure_python_stats.py` | Python 3 standard library only |
| `pandas_stats.py` | pandas |
| `polars_stats.py` | polars |

## Quick start
```bash
# activate virtual environment first
python pandas_stats.py   data/your_dataset.csv
python polars_stats.py   data/your_dataset.csv
python pure_python_stats.py data/your_dataset.csv
