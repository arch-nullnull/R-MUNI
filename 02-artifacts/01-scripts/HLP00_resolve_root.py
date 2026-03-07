"""
HLP00 – Installationsverzeichnis auflösen und im Log bereitstellen
MUNI App Helper Scripts
"""

import os
import sys
import platform
import datetime

# ── Root-Auflösung ─────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "HLP00_root.log")

# ── Hilfsfunktionen ────────────────────────────────────────────────────────────
def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(lines: list[str], filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

# ── Hauptlogik ─────────────────────────────────────────────────────────────────
def resolve_root():
    info = [
        f"{'='*60}",
        f"  HLP00 – Root Resolution Log",
        f"  Timestamp : {timestamp()}",
        f"{'='*60}",
        f"  Script    : {os.path.abspath(__file__)}",
        f"  Root      : {ROOT}",
        f"  OS        : {platform.system()} {platform.release()}",
        f"  Python    : {sys.version.split()[0]}",
        f"  CWD       : {os.getcwd()}",
        f"{'='*60}",
    ]

    for line in info:
        print(line)

    log(info, LOG_FILE)
    print(f"\n  [OK] Log geschrieben → {LOG_FILE}")

if __name__ == "__main__":
    resolve_root()
