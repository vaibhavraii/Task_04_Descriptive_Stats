# Task 04 – Descriptive Statistics Engine

This repository contains three independent implementations that produce identical descriptive-statistics outputs for the 2024 US-presidential-election social-media dataset:

## 1 · Project Overview
The goal was to build a reproducible “stats engine” that generates identical descriptive-statistics outputs three different ways:

| Script | Tech stack |
|--------|------------|
| `pure_python_stats.py` | Python 3 standard library only |
| `pandas_stats.py` | pandas |
| `polars_stats.py` | polars |

All three scripts accept the same CLI flags and produce the same four CSV reports for each dataset.

Dataset URL= https://drive.google.com/file/d/1Jq0fPb-tq76Ee_RtM58fT0_M3o-JDBwe/view?usp=sharing

## 2. Quick start
```bash
# 1 · clone repo & enter folder
git clone https://github.com/<your-handle>/Task_04_Descriptive_Stats.git
cd Task_04_Descriptive_Stats

# 2 · create & activate virtual-env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 

# activate virtual environment first
python pandas_stats.py   data/your_dataset.csv
python polars_stats.py   data/your_dataset.csv
python pure_python_stats.py data/your_dataset.csv

# 3 · drop raw CSVs into data/
#    (they’re excluded from version control)

# 4 · run any engine …

## Twitter posts
python pandas_stats.py      data/tw_posts.csv  --g1 month_year      --g2 month_year source
python polars_stats.py      data/tw_posts.csv  --g1 month_year      --g2 month_year source
python pure_python_stats.py data/tw_posts.csv  --g1 month_year      --g2 month_year source

## Facebook ads
python pandas_stats.py      data/fb_ads.csv    --g1 page_id         --g2 page_id ad_id
…

3 · Performance comparison (runs on M2 MacBook Air)

| Dataset   | Engine | Runtime (s) |
| --------- | ------ | ----------- |
| tw\_posts | Pandas | 0.18        |
| tw\_posts | Polars | 0.05        |
| tw\_posts | Stdlib | 0.97        |
| fb\_ads   | Pandas | 11.64       |
| fb\_ads   | Polars | 0.6         |
| fb\_ads   | Stdlib | 25.47       |
| fb\_posts | Pandas | 0.68        |
| fb\_posts | Polars | 0.07        |
| fb\_posts | Stdlib | 1.86        |


