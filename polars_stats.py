import sys, time, polars as pl

def main(csv_path: str) -> None:
    start = time.perf_counter()
    df = pl.read_csv(csv_path)
    # TODO: compute overall + grouped stats and write to outputs/
    end = time.perf_counter()
    print(f"Polars finished in {end - start:.2f}s")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python polars_stats.py <csv_path>")
        sys.exit(1)
    main(sys.argv[1])
