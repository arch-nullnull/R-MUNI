#!/usr/bin/env python3
# XML00-resolve_root.py
#
# Purpose (Flow-Stage):
# - Read and validate root.txt (BLUEPRINT_ROOT=...)
# - Resolve an absolute root path
# - Persist the resolved root path as a text artifact under:
#     <rootfolder>/03-stages/99-logs/XML00-root.resolved.txt
# - Write an optional log file under:
#     <rootfolder>/03-stages/99-logs/XML00-root.log
#
# Notes:
# - No STDOUT contract. Console output is informational only.
# - No writes to 02-artifacts/00-xml/00-master and no writes to installation root.
# - Root resolution is anchored exclusively by root.txt.

import os
import sys
from datetime import datetime


DEBUG = False


def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def die(message: str, log_path: str | None = None) -> None:
    line = f"[XML00] {now_ts()} | ERROR | {message}"
    print(line, file=sys.stderr)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    sys.exit(1)


def log(message: str, log_path: str | None = None) -> None:
    line = f"[XML00] {now_ts()} | {message}"
    if DEBUG:
        print(line)
    if log_path:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def find_root_txt(script_dir: str) -> str:
    # Expected location based on your fixed structure:
    # <rootfolder>/02-artifacts/01-scripts/XML00-resolve_root.py
    # root.txt is at: <rootfolder>/root.txt
    return os.path.abspath(os.path.join(script_dir, "..", "..", "root.txt"))


def read_blueprint_root(root_txt_path: str, log_path: str | None) -> str:
    try:
        with open(root_txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        die(f"cannot read root.txt: {e}", log_path)

    root_value = None

    for line in lines:
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#"):
            continue

        if stripped.startswith("BLUEPRINT_ROOT="):
            if root_value is not None:
                die("multiple BLUEPRINT_ROOT entries found in root.txt", log_path)
            root_value = stripped.split("=", 1)[1].strip()

    if root_value is None:
        die("no BLUEPRINT_ROOT entry found in root.txt", log_path)

    if root_value == "":
        die("BLUEPRINT_ROOT value is empty", log_path)

    return root_value


def resolve_root_path(root_txt_path: str, root_value: str, log_path: str | None) -> str:
    if os.path.isabs(root_value):
        root_path = root_value
        log("BLUEPRINT_ROOT is absolute", log_path)
    else:
        root_path = os.path.abspath(os.path.join(os.path.dirname(root_txt_path), root_value))
        log("BLUEPRINT_ROOT is relative; resolved against root.txt location", log_path)

    if not os.path.isdir(root_path):
        die(f"resolved root path does not exist or is not a directory: {root_path}", log_path)

    return root_path


def ensure_stage_dirs(root_path: str, log_path: str | None) -> str:
    stages_dir = os.path.join(root_path, "03-stages")
    logs_dir = os.path.join(stages_dir, "99-logs")

    if not os.path.isdir(stages_dir):
        die(f"expected stages directory not found: {stages_dir}", log_path)

    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


def write_resolved_root_txt(logs_dir: str, root_path: str, log_path: str | None) -> str:
    out_path = os.path.join(logs_dir, "XML00-root.resolved.txt")
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(root_path.rstrip() + "\n")
    except Exception as e:
        die(f"cannot write resolved root artifact: {e}", log_path)

    return out_path


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # We only know where to write logs after resolving root.
    # So we buffer minimal console errors until then.
    root_txt_path = find_root_txt(script_dir)

    if not os.path.isfile(root_txt_path):
        die(f"root.txt not found at expected location: {root_txt_path}", None)

    # Resolve root first (no file logging yet).
    root_value = read_blueprint_root(root_txt_path, None)
    root_path = resolve_root_path(root_txt_path, root_value, None)

    # Now we can log to <rootfolder>/03-stages/99-logs/
    logs_dir = ensure_stage_dirs(root_path, None)
    log_path = os.path.join(logs_dir, "XML00-root.log")

    log(f"root.txt: {root_txt_path}", log_path)
    log(f"BLUEPRINT_ROOT raw: {root_value}", log_path)
    log(f"Resolved root path: {root_path}", log_path)

    out_path = write_resolved_root_txt(logs_dir, root_path, log_path)
    log(f"Wrote: {out_path}", log_path)

    # Informational console output (not a contract)
    print(f"[XML00] OK | root resolved -> {out_path}")


if __name__ == "__main__":
    main()
