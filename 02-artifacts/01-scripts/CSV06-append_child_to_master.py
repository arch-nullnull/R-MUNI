#!/usr/bin/env python3
# CSV06-append_child_to_master.py
#
# Purpose:
# - Append Archi CSV exports (child) into master CSV files
# - Append-only, never overwrite
# - Safe newline handling
# - Missing child CSVs are logged but do not abort
#
# Source:
# - <root>/02-artifacts/02-csv/03-child/00-archimatechild
#
# Target:
# - <root>/02-artifacts/02-csv/00-master
#
# Logs:
# - <root>/03-stages/99-logs/CSV06-append.log

import os
import sys
from datetime import datetime


def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg, log_path):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[CSV06] {now_ts()} | {msg}\n")


def ensure_trailing_newline(path):
    with open(path, "rb+") as f:
        f.seek(0, os.SEEK_END)
        if f.tell() == 0:
            return
        f.seek(-1, os.SEEK_END)
        if f.read(1) != b"\n":
            f.write(b"\n")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_file = os.path.abspath(
        os.path.join(script_dir, "..", "..", "03-stages", "99-logs", "CSV00-root.resolved.txt")
    )

    if not os.path.isfile(root_file):
        print("[CSV06] ERROR | CSV00-root.resolved.txt not found", file=sys.stderr)
        sys.exit(1)

    with open(root_file, "r", encoding="utf-8") as f:
        root = f.readline().strip()

    child_dir = os.path.join(root, "02-artifacts", "02-csv", "03-child", "00-archimatechild")
    master_dir = os.path.join(root, "02-artifacts", "02-csv", "00-master")
    log_dir = os.path.join(root, "03-stages", "99-logs")

    log_path = os.path.join(log_dir, "CSV06-append.log")

    files = ["elements.csv", "relations.csv", "properties.csv"]

    for fname in files:
        child_path = os.path.join(child_dir, fname)
        master_path = os.path.join(master_dir, fname)

        if not os.path.isfile(child_path):
            msg = f"Child CSV missing, skipped: {fname}"
            print(f"[CSV06] WARN | {msg}")
            log(msg, log_path)
            continue

        if not os.path.isfile(master_path):
            msg = f"Master CSV missing, skipped: {fname}"
            print(f"[CSV06] ERROR | {msg}")
            log(msg, log_path)
            continue

        with open(child_path, "r", encoding="utf-8") as src:
            lines = src.readlines()

        if len(lines) <= 1:
            msg = f"No data rows in child CSV: {fname}"
            print(f"[CSV06] INFO | {msg}")
            log(msg, log_path)
            continue

        data_lines = lines[1:]  # skip header

        ensure_trailing_newline(master_path)

        with open(master_path, "a", encoding="utf-8", newline="") as tgt:
            for line in data_lines:
                tgt.write(line)

        msg = f"Appended {len(data_lines)} rows from {fname}"
        print(f"[CSV06] OK | {msg}")
        log(msg, log_path)

    print("[CSV06] DONE | append cycle completed")


if __name__ == "__main__":
    main()
