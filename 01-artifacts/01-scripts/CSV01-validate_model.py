#!/usr/bin/env python3
# CSV01-validate_model.py
#
# Purpose (Flow-Stage):
# - Inspect ArchiMate model structure inside the Blueprint
# - Collect informational context about available models
# - Persist model scope information as a structured text artifact
#
# Output:
# - <rootfolder>/03-stages/model-scope.txt
# - <rootfolder>/03-stages/99-logs/CSV01-validate_model.log
#
# Rules:
# - Informational only (no decisions, no filtering)
# - No mutation of model data
# - No directory creation
# - Abort only on technical failures

import os
import sys
from datetime import datetime


DEBUG = False


def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def die(message: str, log_path: str | None = None) -> None:
    line = f"[CSV01] {now_ts()} | ERROR | {message}"
    print(line, file=sys.stderr)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    sys.exit(1)


def log(message: str, log_path: str | None = None) -> None:
    line = f"[CSV01] {now_ts()} | {message}"
    if DEBUG:
        print(line)
    if log_path:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def read_root_resolved(script_dir: str) -> str:
    path = os.path.abspath(
        os.path.join(script_dir, "..", "..", "03-stages", "99-logs", "CSV00-root.resolved.txt")
    )
    if not os.path.isfile(path):
        die(f"missing CSV00 root artifact: {path}", None)

    try:
        with open(path, "r", encoding="utf-8") as f:
            root = f.readline().strip()
    except Exception as e:
        die(f"cannot read CSV00 root artifact: {e}", None)

    if root == "" or not os.path.isdir(root):
        die(f"invalid root path resolved by CSV00: {root}", None)

    return root


def classify_archimate_file(filename: str) -> str:
    name = filename.lower()
    if name.endswith(".archimate"):
        return "ARCHIMATE"
    if name.endswith(".bak"):
        return "BACKUP"
    return "OTHER"


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_path = read_root_resolved(script_dir)

    stages_dir = os.path.join(root_path, "03-stages")
    logs_dir = os.path.join(stages_dir, "99-logs")

    if not os.path.isdir(stages_dir):
        die(f"expected stages directory not found: {stages_dir}", None)

    if not os.path.isdir(logs_dir):
        die(f"expected logs directory not found: {logs_dir}", None)

    log_path = os.path.join(logs_dir, "CSV01-validate_model.log")
    log(f"Resolved root path: {root_path}", log_path)

    archimate_root = os.path.join(root_path, "01-model", "00-archimate")
    log(f"Inspecting ArchiMate root: {archimate_root}", log_path)

    active_models = []
    active_sub_models = []
    other_files = []

    if os.path.isdir(archimate_root):
        for folder in sorted(os.listdir(archimate_root)):
            folder_path = os.path.join(archimate_root, folder)
            if not os.path.isdir(folder_path):
                continue

            log(f"Scanning folder: {folder}", log_path)

            for fname in sorted(os.listdir(folder_path)):
                fpath = os.path.join(folder_path, fname)
                if not os.path.isfile(fpath):
                    continue

                classification = classify_archimate_file(fname)

                if folder == "00-archimateactive" and classification == "ARCHIMATE":
                    active_models.append(fname)
                elif folder == "01-archimateactivesub" and classification == "ARCHIMATE":
                    active_sub_models.append(fname)
                else:
                    other_files.append(f"{folder}/{fname}")

                log(f" - {fname} [{classification}]", log_path)
    else:
        log("INFO: ArchiMate root directory not found", log_path)

    out_path = os.path.join(stages_dir, "model-scope.txt")

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("ACTIVE_MODELS:\n")
            for m in active_models:
                f.write(f"- {m}\n")
            f.write("\n")

            f.write("ACTIVE_SUB_MODELS:\n")
            for m in active_sub_models:
                f.write(f"- {m}\n")
            f.write("\n")

            f.write("OTHER_ARCHIMATE_FILES:\n")
            for m in other_files:
                f.write(f"- {m}\n")
            f.write("\n")
    except Exception as e:
        die(f"cannot write model-scope artifact: {e}", log_path)

    log(f"Wrote model scope artifact: {out_path}", log_path)
    print(f"[CSV01] OK | model context collected -> {out_path}")


if __name__ == "__main__":
    main()
