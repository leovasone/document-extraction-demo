"""CLI entrypoint: process every document in a folder and report
structured results + throughput stats.

Usage:
    python main.py samples/input output/results.json
"""
import json
import sys
import time
from pathlib import Path

from src.pipeline import ExtractionPipeline


def main():
    input_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("samples/input")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output/results.json")

    pipeline = ExtractionPipeline()

    start = time.perf_counter()
    results = pipeline.process_folder(input_dir)
    total_elapsed = time.perf_counter() - start

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    n = len(results)
    avg = total_elapsed / n if n else 0
    docs_per_hour_single_worker = (3600 / avg) if avg else 0

    summary = {
        "documents_processed": n,
        "total_seconds": round(total_elapsed, 3),
        "avg_seconds_per_document": round(avg, 3),
        "throughput_docs_per_hour_single_worker": round(docs_per_hour_single_worker),
        "throughput_docs_per_hour_8_workers": round(docs_per_hour_single_worker * 8),
    }

    print(json.dumps(summary, indent=2))
    print(f"\nStructured results written to {output_path}")

    summary_path = output_path.parent / "benchmark.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Benchmark written to {summary_path}")


if __name__ == "__main__":
    main()
