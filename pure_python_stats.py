#!/usr/bin/env python3
"""
pure_python_stats.py
Descriptive-statistics engine using ONLY the Python standard library.

Examples
--------
python pure_python_stats.py data/tw_posts.csv  --g1 month_year      --g2 month_year source
python pure_python_stats.py data/fb_ads.csv    --g1 page_id         --g2 page_id ad_id
python pure_python_stats.py data/fb_posts.csv  --g1 Facebook_Id     --g2 Facebook_Id post_id
"""
import argparse, csv, statistics, time, itertools
from pathlib import Path
from collections import defaultdict, Counter

# ── CLI ───────────────────────────────────────────────────────────────
P = argparse.ArgumentParser(description="Descriptive stats (stdlib only)")
P.add_argument("csv",  help="Path to CSV file")
P.add_argument("--g1", nargs="+", required=True, help="Level-1 grouping column(s)")
P.add_argument("--g2", nargs="+", required=True, help="Level-2 grouping column(s)")
args      = P.parse_args()
csv_path  = Path(args.csv)
level1    = args.g1
level2    = args.g2
# ---------------------------------------------------------------------


# ── Helpers ───────────────────────────────────────────────────────────
def numeric_stats(values):
    """Return dict of count/mean/std/min/median/max."""
    nums = [v for v in values if v is not None]
    if not nums:
        return {}
    out = {
        "count": len(nums),
        "mean":  statistics.fmean(nums),
        "std":   statistics.pstdev(nums) if len(nums) > 1 else 0.0,
        "min":   min(nums),
        "median": statistics.median(nums),
        "max":   max(nums),
    }
    return out


def write_dicts_to_csv(rows, header, path: Path):
    """rows = iterable of dicts with identical keys; header is list(str)."""
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)


# ── Load CSV into memory (list of dicts) ─────────────────────────────
with csv_path.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    data   = [row for row in reader]

# Infer numeric columns: those convertible to float for ≥ 95 % of non-blank rows
numeric_cols, cat_cols = [], []
total_rows = len(data)
for col in reader.fieldnames:
    convertable = 0
    for row in data:
        v = row[col].strip()
        if v == "":
            continue
        try:
            float(v)
            convertable += 1
        except ValueError:
            break
    if convertable >= 0.95 * total_rows:
        numeric_cols.append(col)
    else:
        cat_cols.append(col)

# ── Prepare output folder ────────────────────────────────────────────
out_dir = Path("outputs") / csv_path.stem / "stdlib"
out_dir.mkdir(parents=True, exist_ok=True)

t0 = time.perf_counter()

# ── Overall numeric stats ────────────────────────────────────────────
overall_rows = []
for col in numeric_cols:
    vals = [float(r[col]) if r[col].strip() else None for r in data]
    stats = numeric_stats(vals)
    stats["missing_count"] = vals.count(None)
    stats["feature"] = col
    overall_rows.append(stats)

header = ["feature", "count", "mean", "std", "min", "median", "max", "missing_count"]
write_dicts_to_csv(overall_rows, header, out_dir / "overall_numeric.csv")

# ── Overall categorical top-5 (skip high-cardinality) ────────────────
with (out_dir / "overall_top5_categorical.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["column", "value", "count"])
    for col in cat_cols:
        col_vals = [r[col].strip() for r in data]
        if len(set(col_vals)) > 0.95 * total_rows:
            continue
        for val, cnt in Counter(col_vals).most_common(5):
            w.writerow([col, val, cnt])

# ── Grouped numeric stats (level1 & level2) ──────────────────────────
def grouped_numeric(rows, group_cols, tag):
    buckets = defaultdict(lambda: defaultdict(list))
    for r in rows:
        key = tuple(r[c] for c in group_cols)
        for col in numeric_cols:
            v = r[col].strip()
            if v != "":
                buckets[key][col].append(float(v))

    output_rows = []
    for key, col_dict in buckets.items():
        row = {group_cols[i]: key[i] for i in range(len(group_cols))}
        for col, nums in col_dict.items():
            s = numeric_stats(nums)
            for stat_name, val in s.items():
                row[f"{col}_{stat_name}"] = val
        output_rows.append(row)

    # header: group cols + flattened numeric_stat columns
    numeric_headers = [f"{c}_{s}" for c in numeric_cols
                       for s in ("count", "mean", "std", "min", "median", "max")]
    header = group_cols + numeric_headers
    write_dicts_to_csv(output_rows, header, out_dir / f"by_{'_'.join(group_cols)}_numeric.csv")


grouped_numeric(data, level1, "level1")
grouped_numeric(data, level2, "level2")

# ── Done ─────────────────────────────────────────────────────────────
print(f"[stdlib ] {csv_path.name:>15} → {out_dir}   "
      f"{time.perf_counter() - t0:.2f}s")
