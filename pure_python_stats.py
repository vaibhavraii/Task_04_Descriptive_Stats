import sys, time

def main(csv_path: str) -> None:
    start = time.perf_counter()
    # TODO: implement pure-stdlib descriptive stats
    end = time.perf_counter()
    print(f"Pure-Python finished in {end - start:.2f}s")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pure_python_stats.py <csv_path>")
        sys.exit(1)
    main(sys.argv[1])
