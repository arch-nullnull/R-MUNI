#!/usr/bin/env python3
# CSV99-export_snapshot.py
#
# Purpose:
#   Create an Archi-compatible CSV import snapshot from master CSVs.
#   The master is NEVER modified.
#
# Scope:
#   elements.csv
#   properties.csv
#   relations.csv
#
# Behavior:
#   - Deterministic
#   - Config-driven TYPE exclusion (csvexport.txt)
#   - Last-wins deduplication
#   - ID-less objects supported
#   - Import folder files are overwritten
#
# Output:
#   <root>/02-artifacts/02-csv/04-import
#
# Logging:
#   <root>/03-stages/99-logs/CSV99-export_snapshot.log

import csv
import os
from datetime import datetime


FILES = ["elements.csv", "properties.csv", "relations.csv"]


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg, log_path):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[CSV99] {now()} | {msg}\n")


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def load_export_filter(path):
    if not os.path.isfile(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return {
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        }


def main():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_file = os.path.join(
        script_dir, "..", "..", "03-stages", "99-logs", "CSV00-root.resolved.txt"
    )

    with open(root_file, encoding="utf-8") as f:
        root = f.readline().strip()

    log_dir = os.path.join(root, "03-stages", "99-logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "CSV99-export_snapshot.log")

    log("=== CSV99 RUN START ===", log_path)

    master_dir = os.path.join(root, "02-artifacts", "02-csv", "00-master")
    import_dir = os.path.join(root, "02-artifacts", "02-csv", "04-import")
    os.makedirs(import_dir, exist_ok=True)

    export_filter_path = os.path.join(
        root, "02-artifacts", "02-csv", "02-sync", "csvexport.txt"
    )
    export_filter = load_export_filter(export_filter_path)

    log(f"csvexport loaded: {export_filter}", log_path)

    for fname in FILES:
        header, rows = read_csv(os.path.join(master_dir, fname))
        result = []
        seen = {}

        for row in reversed(rows):
            row_id = row.get("ID", "").strip()

            if "Type" in row and row["Type"] in export_filter:
                log(f"{fname} | EXCLUDED TYPE | {row}", log_path)
                continue

            if fname == "elements.csv":
                key = row_id if row_id else (
                    row.get("Type"),
                    row.get("Name"),
                    row.get("Documentation"),
                    row.get("Specialization"),
                )

            elif fname == "properties.csv":
                key = (row_id, row.get("Key")) if row_id else (
                    row.get("Key"),
                    row.get("Value"),
                )

            else:
                key = (
                    row.get("Type"),
                    row.get("Source"),
                    row.get("Target"),
                    row.get("Specialization"),
                )

            if key in seen:
                log(f"{fname} | DUPLICATE | {row}", log_path)
                continue

            seen[key] = True
            result.append(row)

        result.reverse()
        write_csv(os.path.join(import_dir, fname), header, result)
        log(f"{fname} | WRITTEN | {len(result)} rows", log_path)

    log("CSV99 completed successfully", log_path)
    print("[CSV99] OK | CSV99-export_snapshot completed")


if __name__ == "__main__":
    main()
