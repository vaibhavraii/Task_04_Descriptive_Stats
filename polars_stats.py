#!/usr/bin/env python3
"""
polars_stats.py
Flexible descriptive-statistics engine using Polars ≥ 0.20.

Run examples
------------
# Facebook ADS
python polars_stats.py data/fb_ads.csv   --g1 page_id     --g2 page_id ad_id
# Facebook POSTS
python polars_stats.py data/fb_posts.csv --g1 Facebook_Id --g2 Facebook_Id post_id
# Twitter POSTS
python polars_stats.py data/tw_posts.csv --g1 month_year  --g2 month_year source
"""
import argparse, time, csv
from pathlib import Path
import polars as pl

# ── CLI ───────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Descriptive stats with Polars")
parser.add_argument("csv",  help="Path to CSV file")
parser.add_argument("--g1", nargs="+", required=True, help="Level-1 grouping column(s)")
parser.add_argument("--g2", nargs="+", required=True, help="Level-2 grouping column(s)")
args     = parser.parse_args()
csv_path = Path(args.csv)
level1   = args.g1                 # list
level2   = args.g2
# ---------------------------------------------------------------------


def main() -> None:
    t0 = time.perf_counter()

    # engine-specific output folder
    out_dir = Path("outputs") / csv_path.stem / "polars"
    out_dir.mkdir(parents=True, exist_ok=True)

    # read CSV (infer dtypes from first 5000 rows for speed)
    df = pl.read_csv(csv_path, infer_schema_length=5000)

    # ── numeric features ──────────────────────────────────────────────
    num_cols = df.select(pl.selectors.numeric()).columns

    # overall numeric (Polars describe = count/mean/std/min/max)
    df.select(num_cols).describe().write_csv(out_dir / "overall_numeric.csv")

    # helper: grouped numeric stats → CSV
    def grouped_stats(cols, tag: str) -> None:
        agg_exprs = (
            [pl.col(c).count().alias(f"{c}_count") for c in num_cols] +
            [pl.col(c).mean().alias(f"{c}_mean")   for c in num_cols] +
            [pl.col(c).std().alias(f"{c}_std")     for c in num_cols] +
            [pl.col(c).min().alias(f"{c}_min")     for c in num_cols] +
            [pl.col(c).max().alias(f"{c}_max")     for c in num_cols]
        )
        (df.group_by(cols)
           .agg(agg_exprs)
           .write_csv(out_dir / f"by_{'_'.join(cols)}_{tag}.csv"))

    grouped_stats(level1, "numeric")
    grouped_stats(level2, "numeric")

    # ── categorical top-5 values (row-wise) ───────────────────────────
    cat_cols = [c for c in df.columns if c not in num_cols]
    with (out_dir / "overall_top5_categorical.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["column", "value", "count"])
        for col in cat_cols:
            # skip high-cardinality columns (>95 % unique)
            if df[col].n_unique() > 0.95 * df.height:
                continue
            vc = (df.group_by(col).len()
                    .sort("len", descending=True)
                    .limit(5))
            for row in vc.iter_rows(named=True):
                w.writerow([col, row[col], row["len"]])

    runtime = time.perf_counter() - t0
    print(f"[polars] {csv_path.name:>15} → {out_dir}   {runtime:6.2f}s")


if __name__ == "__main__":
    main()
