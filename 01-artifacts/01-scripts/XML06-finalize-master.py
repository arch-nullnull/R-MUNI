#!/usr/bin/env python3
# ==========================================================
# XML06-finalize-master.py
#
# PURPOSE
# ----------------------------------------------------------
# Finalize the consolidated master state by materializing
# master.xml from the cleared master input.
#
# This stage performs no transformation and no validation.
# It exists solely to fix the master state as a stable
# reference for downstream processes.
# ==========================================================

import os
import shutil
from datetime import datetime


# ==========================================================
# STAGE 0 – PATH RESOLUTION
# ==========================================================

def resolve_root() -> str:
    script_dir = os.path.abspath(os.path.dirname(__file__))
    resolved_path = os.path.abspath(
        os.path.join(script_dir, "..", "..", "02-stages", "99-logs", "XML00-root.resolved.txt")
    )
    if not os.path.isfile(resolved_path):
        raise RuntimeError(f"XML00-root.resolved.txt not found at: {resolved_path}")
    with open(resolved_path, "r", encoding="utf-8") as f:
        root = f.readline().strip()
    if not root or not os.path.isdir(root):
        raise RuntimeError(f"Invalid root path in XML00-root.resolved.txt: {root}")
    return root


# ==========================================================
# STAGE 1 – FINALIZE MASTER
# ==========================================================

def finalize_master(src, dst):
    if not os.path.exists(src):
        raise FileNotFoundError(f"Input master not found: {src}")

    shutil.copyfile(src, dst)


# ==========================================================
# STAGE 2 – LOGGING
# ==========================================================

def write_log(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


# ==========================================================
# STAGE 3 – MAIN FLOW
# ==========================================================

def main():
    ROOT = resolve_root()

    XML_DIR = os.path.join(ROOT, "01-artifacts", "00-xml")
    MASTER_DIR = os.path.join(XML_DIR, "00-master")
    MASTER_IN = os.path.join(MASTER_DIR, "master.cleared.xml")
    MASTER_OUT = os.path.join(MASTER_DIR, "master.xml")
    LOG_DIR = os.path.join(ROOT, "02-stages", "99-logs")
    LOG_FILE = os.path.join(LOG_DIR, "XML06-finalize-master.log")

    log = []
    log.append("==================================================")
    log.append(f"XML06 STARTED: {datetime.utcnow().isoformat()}")

    finalize_master(MASTER_IN, MASTER_OUT)

    log.append(f"MASTER FINALIZED: {MASTER_OUT}")
    log.append(f"XML06 COMPLETED: {datetime.utcnow().isoformat()}")
    log.append("==================================================")

    write_log(LOG_FILE, log)


if __name__ == "__main__":
    main()
