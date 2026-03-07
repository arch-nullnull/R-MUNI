#!/usr/bin/env python3
# M2B03-clear.py
#
# Purpose:
# - Clear M2B* artifacts from 03-stages/01-bpmnarchive
# - Clear M2B01* and M2B02* logs from 03-stages/99-logs
# - Keep M2B00-root.resolved
# - Keep M2B03* logs
# - Do NOT touch active model
# - Do NOT create directories

from pathlib import Path
import sys
from datetime import datetime


# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

ARCHIVE_DIR = ROOT_DIR / "03-stages" / "01-bpmnarchive"
LOG_DIR = ROOT_DIR / "03-stages" / "99-logs"
LOG_FILE = LOG_DIR / "M2B03-clear.log"


# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------

def log(msg: str):
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def abort(msg: str):
    log(f"[ABORT] {msg}")
    sys.exit(1)


# ----------------------------------------------------------
# Core Logic
# ----------------------------------------------------------

def main():
    if not ARCHIVE_DIR.exists():
        abort(f"archive directory missing: {ARCHIVE_DIR}")

    if not LOG_DIR.exists():
        abort(f"log directory missing: {LOG_DIR}")

    log("start M2B03 clearing")

    # --- clear archive ---
    for item in ARCHIVE_DIR.iterdir():
        if item.name.startswith("M2B"):
            if item.is_file():
                item.unlink()
                log(f"archive removed file: {item.name}")
            elif item.is_dir():
                for sub in item.rglob("*"):
                    if sub.is_file():
                        sub.unlink()
                item.rmdir()
                log(f"archive removed directory: {item.name}")

    # --- clear logs ---
    for log_file in LOG_DIR.iterdir():
        name = log_file.name

        if name == "M2B00-root.resolved":
            continue

        if name.startswith("M2B03"):
            continue

        if name.startswith("M2B01") or name.startswith("M2B02"):
            log_file.unlink()
            log(f"log removed: {name}")

    log("clearing completed")


if __name__ == "__main__":
    main()
