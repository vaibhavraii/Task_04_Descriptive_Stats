import sys, time, pandas as pd

def main(csv_path: str) -> None:
    start = time.perf_counter()
    df = pd.read_csv(csv_path, low_memory=False)
    # TODO: compute overall + grouped stats and write to outputs/
    end = time.perf_counter()
    print(f"Pandas finished in {end - start:.2f}s")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pandas_stats.py <csv_path>")
        sys.exit(1)
    main(sys.argv[1])
