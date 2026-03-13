#!/usr/bin/env python3
# CSV05-create_master_csvs.py
#
# Purpose:
# - Ensure the existence of master CSV files in the exact structure
#   expected by Archi 5.8 CSV import
# - Create files ONLY if they do not already exist
# - Never overwrite or modify existing files
#
# Output (if missing):
# - elements.csv
# - relations.csv
# - properties.csv
#
# Location:
# - <root>/01-artifacts/02-csv/00-master/
#
# Rules:
# - Idempotent
# - Structure only
# - No content generation
# - No destructive behavior

import os
import sys


def die(msg):
    print(f"[CSV05] ERROR | {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_file = os.path.abspath(
        os.path.join(script_dir, "..", "..", "02-stages", "99-logs", "CSV00-root.resolved.txt")
    )

    if not os.path.isfile(root_file):
        die("CSV00-root.resolved.txt not found")

    with open(root_file, "r", encoding="utf-8") as f:
        root = f.readline().strip()

    if not root or not os.path.isdir(root):
        die("Resolved root path is invalid")

    target_dir = os.path.join(root, "01-artifacts", "02-csv", "00-master")

    if not os.path.isdir(target_dir):
        die(f"Target directory does not exist: {target_dir}")

    master_files = {
        "elements.csv": '"ID","Type","Name","Documentation","Specialization"\n',
        "relations.csv": '"ID","Type","Name","Documentation","Source","Target","Specialization"\n',
        "properties.csv": '"ID","Key","Value"\n',
    }

    for filename, header in master_files.items():
        path = os.path.join(target_dir, filename)

        if os.path.isfile(path):
            print(f"[CSV05] exists, untouched: {filename}")
            continue

        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(header)

        print(f"[CSV05] created: {filename}")

    print("[CSV05] OK | master CSV structure ensured")


if __name__ == "__main__":
    main()
