#!/usr/bin/env python3
# M2B00-root-check.py
#
# Purpose (Flow-Stage):
# - Resolve project root autonomously for M2B
# - Fast-path: reuse XML00-root.resolved.txt if present
# - Fallback: read root.txt and resolve BLUEPRINT_ROOT (XML00 logic)
# - Persist resolved root as:
#     <rootfolder>/03-stages/99-logs/M2B00-root.resolved.txt
# - Write log to:
#     <rootfolder>/03-stages/99-logs/M2B00-root-check.log
#
# Rules:
# - No calls to XML00
# - No writes to XML00 artifacts
# - No directory creation except logs dir
# - Deterministic, audit-friendly

import os
import sys
from datetime import datetime


DEBUG = False


def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def die(message: str, log_path: str | None = None) -> None:
    line = f"[M2B00] {now_ts()} | ERROR | {message}"
    print(line, file=sys.stderr)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    sys.exit(1)


def log(message: str, log_path: str | None = None) -> None:
    line = f"[M2B00] {now_ts()} | {message}"
    if DEBUG:
        print(line)
    if log_path:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def script_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def expected_xml00_root_resolved(script_dir: str) -> str:
    # <rootfolder>/02-artifacts/01-scripts/M2B00-root-check.py
    # XML00 artifact at: <rootfolder>/03-stages/99-logs/XML00-root.resolved.txt
    return os.path.abspath(
        os.path.join(script_dir, "..", "..", "03-stages", "99-logs", "XML00-root.resolved.txt")
    )


def expected_root_txt(script_dir: str) -> str:
    # root.txt at: <rootfolder>/root.txt
    return os.path.abspath(os.path.join(script_dir, "..", "..", "root.txt"))


def read_resolved_root(path: str, log_path: str | None) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            root = f.readline().strip()
    except Exception as e:
        die(f"cannot read resolved root file: {e}", log_path)

    if root == "":
        die("resolved root file is empty", log_path)

    if not os.path.isdir(root):
        die(f"resolved root path is not a directory: {root}", log_path)

    return root


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


def ensure_logs_dir(root_path: str, log_path: str | None) -> str:
    stages_dir = os.path.join(root_path, "03-stages")
    logs_dir = os.path.join(stages_dir, "99-logs")

    if not os.path.isdir(stages_dir):
        die(f"expected stages directory not found: {stages_dir}", log_path)

    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


def write_m2b_root_resolved(logs_dir: str, root_path: str, log_path: str | None) -> str:
    out_path = os.path.join(logs_dir, "M2B00-root.resolved.txt")
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(root_path.rstrip() + "\n")
    except Exception as e:
        die(f"cannot write M2B resolved root artifact: {e}", log_path)
    return out_path


def main() -> None:
    sdir = script_dir()

    # We only know where to log after resolving root
    xml00_resolved = expected_xml00_root_resolved(sdir)
    root_txt = expected_root_txt(sdir)

    root_path = None
    log_path = None

    # Fast-path: reuse XML00 artifact
    if os.path.isfile(xml00_resolved):
        root_path = read_resolved_root(xml00_resolved, None)
        logs_dir = ensure_logs_dir(root_path, None)
        log_path = os.path.join(logs_dir, "M2B00-root-check.log")
        log(f"Reused XML00 root artifact: {xml00_resolved}", log_path)
        log(f"Resolved root path: {root_path}", log_path)

    # Fallback: resolve via root.txt
    else:
        if not os.path.isfile(root_txt):
            die(f"neither XML00-root.resolved.txt nor root.txt found", None)

        root_value = read_blueprint_root(root_txt, None)
        root_path = resolve_root_path(root_txt, root_value, None)
        logs_dir = ensure_logs_dir(root_path, None)
        log_path = os.path.join(logs_dir, "M2B00-root-check.log")

        log(f"root.txt: {root_txt}", log_path)
        log(f"BLUEPRINT_ROOT raw: {root_value}", log_path)
        log(f"Resolved root path: {root_path}", log_path)

    out_path = write_m2b_root_resolved(logs_dir, root_path, log_path)
    log(f"Wrote: {out_path}", log_path)

    print(f"[M2B00] OK | root resolved -> {out_path}")


if __name__ == "__main__":
    main()
