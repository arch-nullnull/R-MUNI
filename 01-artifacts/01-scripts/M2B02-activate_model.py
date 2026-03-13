#!/usr/bin/env python3
# M2B02-activate_model.py
#
# Purpose:
# - Copy BPMN hulls into the active BPMN model directory
# - Do NOT overwrite existing active BPMN files
# - Do NOT create directories
# - Abort if expected directories are missing
# - Log to stage log directory
# - No XML parsing
# - No identity logic
# - No content changes

from pathlib import Path
import shutil
import sys
from datetime import datetime


# ----------------------------------------------------------
# CONFIG (EXPLICIT – NO ASSUMPTIONS)
# ----------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

HULL_DIR = ROOT_DIR / "02-stages" / "01-bpmnarchive"
ACTIVE_DIR = ROOT_DIR / "00-model" / "01-bpmn" / "00-bpmnactive"
LOG_DIR = ROOT_DIR / "02-stages" / "99-logs"
LOG_FILE = LOG_DIR / "M2B02-activate_model.log"


# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------

def log(msg: str):
    timestamp = datetime.now().isoformat(timespec="seconds")
    line = f"[{timestamp}] {msg}"
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
    if not LOG_DIR.exists():
        print("[M2B02][ABORT] log directory missing:", LOG_DIR)
        sys.exit(1)

    log("start activation")

    if not HULL_DIR.exists():
        abort(f"hull directory missing: {HULL_DIR}")

    if not ACTIVE_DIR.exists():
        abort(f"active model directory missing: {ACTIVE_DIR}")

    for hull in HULL_DIR.glob("*.bpmn"):
        target = ACTIVE_DIR / hull.name

        if target.exists():
            log(f"skip (already active): {hull.name}")
            continue

        shutil.copy2(hull, target)
        log(f"activated: {hull.name}")

    log("OK | activation completed")


if __name__ == "__main__":
    main()
