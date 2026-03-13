#!/usr/bin/env python3
# ==========================================================
# XML07-cleanup-artifacts.py
#
# PURPOSE
# ----------------------------------------------------------
# Remove routine intermediate artifacts from XML00..XML05
# across master + archives, and prune logs for XML00..XML05.
#
# Keeps:
# - master.xml
# - XML06 logs
# - safety snapshots / archives not matching XML00..XML05 prefix
# ==========================================================

import os
from datetime import datetime, timezone


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
# STAGE 1 – CLEANUP RULES
# ==========================================================

ROUTINE_PREFIXES = tuple(f"XML0{i}-" for i in range(0, 6))  # XML00- .. XML05-

MASTER_FILES_TO_REMOVE = [
    "master.generated.xml",
    "master.cleared.xml",
]

def is_routine_fragment(filename: str) -> bool:
    return filename.startswith(ROUTINE_PREFIXES)

def remove_if_exists(path: str, log: list[str]):
    if os.path.exists(path):
        os.remove(path)
        log.append(f"REMOVED: {path}")
    else:
        log.append(f"SKIP: not found {path}")

def cleanup_master_intermediates(master_dir: str, log: list[str]):
    for name in MASTER_FILES_TO_REMOVE:
        remove_if_exists(os.path.join(master_dir, name), log)

def cleanup_routine_fragments_in_dir(folder: str, log: list[str]):
    if not os.path.isdir(folder):
        log.append(f"SKIP: folder missing {folder}")
        return

    for fname in os.listdir(folder):
        if is_routine_fragment(fname):
            remove_if_exists(os.path.join(folder, fname), log)

def cleanup_logs_xml00_to_xml05(log_dir: str, log: list[str]):
    if not os.path.isdir(log_dir):
        log.append(f"SKIP: folder missing {log_dir}")
        return

    for fname in os.listdir(log_dir):
        if fname.endswith(".log") and is_routine_fragment(fname):
            remove_if_exists(os.path.join(log_dir, fname), log)


# ==========================================================
# STAGE 2 – MAIN FLOW
# ==========================================================

def write_log(path: str, lines: list[str]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

def main():
    ROOT = resolve_root()

    MASTER_DIR = os.path.join(ROOT, "01-artifacts", "00-xml", "00-master")
    ARCHI_ARCHIVE_DIR = os.path.join(ROOT, "02-stages", "00-archimatearchive")
    BPMN_ARCHIVE_DIR = os.path.join(ROOT, "02-stages", "01-bpmnarchive")
    LOG_DIR = os.path.join(ROOT, "02-stages", "99-logs")
    LOG_FILE = os.path.join(LOG_DIR, "XML07-cleanup-artifacts.log")

    log = []
    log.append("==================================================")
    log.append(f"XML07 STARTED: {datetime.now(timezone.utc).isoformat()}")

    cleanup_master_intermediates(MASTER_DIR, log)
    cleanup_routine_fragments_in_dir(ARCHI_ARCHIVE_DIR, log)
    cleanup_routine_fragments_in_dir(BPMN_ARCHIVE_DIR, log)
    cleanup_logs_xml00_to_xml05(LOG_DIR, log)

    log.append(f"XML07 COMPLETED: {datetime.now(timezone.utc).isoformat()}")
    log.append("==================================================")

    write_log(LOG_FILE, log)

if __name__ == "__main__":
    main()
