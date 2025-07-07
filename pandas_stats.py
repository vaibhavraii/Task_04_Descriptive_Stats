#!/usr/bin/env python3
"""
pandas_stats.py
Flexible descriptive-statistics engine using pandas.

Run examples
------------
# Facebook ADS  ➜ group by page, then page×ad
python pandas_stats.py data/fb_ads.csv   --g1 page_id         --g2 page_id ad_id

# Facebook POSTS ➜ group by page, then page×post
python pandas_stats.py data/fb_posts.csv --g1 page_id         --g2 page_id post_id

# Twitter POSTS  ➜ group by month, then month×source
python pandas_stats.py data/tw_posts.csv --g1 month_year      --g2 month_year source
"""
import argparse, time, csv
from pathlib import Path
import pandas as pd

# ---------- command-line arguments -----------------------------------
parser = argparse.ArgumentParser(description="Descriptive stats with pandas")
parser.add_argument("csv",  help="Path to a CSV file")
parser.add_argument("--g1", nargs="+", required=True, help="Level-1 grouping column(s)")
parser.add_argument("--g2", nargs="+", required=True, help="Level-2 grouping column(s)")
args = parser.parse_args()

csv_path = Path(args.csv)
level1   = args.g1              # list of column names
level2   = args.g2
# ---------------------------------------------------------------------


def main() -> None:
    t0 = time.perf_counter()

    # one sub-folder per dataset, e.g. outputs/fb_posts
    out_dir = Path("outputs") / csv_path.stem / "pandas"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1 ─ load
    df = pd.read_csv(csv_path, low_memory=False)

    # 2 ─ numeric columns only
    num_cols = df.select_dtypes(include="number").columns

    # overall numeric stats
    df[num_cols].describe().T.to_csv(out_dir / "overall_numeric.csv")

    # level-1 numeric stats
    (df.groupby(level1)[num_cols]
       .agg(["count", "mean", "std", "min", "max"])
       .to_csv(out_dir / f"by_{'_'.join(level1)}_numeric.csv"))

    # level-2 numeric stats
    (df.groupby(level2)[num_cols]
       .agg(["count", "mean", "std", "min", "max"])
       .to_csv(out_dir / f"by_{'_'.join(level2)}_numeric.csv"))

    # 3 ─ top-5 for each categorical column
    with (out_dir / "overall_top5_categorical.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["column", "value", "count"])
        for col in df.select_dtypes(exclude="number").columns:
            vc = df[col].value_counts(dropna=False).head(5)
            for val, cnt in vc.items():
                w.writerow([col, val, cnt])

    runtime = time.perf_counter() - t0
    print(f"[pandas] {csv_path.name:>15} → {out_dir}   {runtime:6.2f}s")


if __name__ == "__main__":
    main()
