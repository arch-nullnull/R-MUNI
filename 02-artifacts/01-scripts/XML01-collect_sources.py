#!/usr/bin/env python3
# XML01-collect_sources.py
#
# Flow-Stage:
# - Reads resolved root from:
#     <rootfolder>/03-stages/99-logs/XML00-root.resolved.txt
# - Reads source folder declarations from:
#     <rootfolder>/02-artifacts/00-xml/child_mapping.txt
# - Collects all files from declared source folders
# - Persists a complete, self-describing reference TXT per source type
# - Writes a separate LOG for runtime information
#
# Reference artifacts:
#   <rootfolder>/03-stages/00-archimatearchive/XML01-sources.resolved.txt
#   <rootfolder>/03-stages/01-bpmnarchive/XML01-sources.resolved.txt
#
# Logs:
#   <rootfolder>/03-stages/99-logs/XML01-sources.log

import os
import sys
from datetime import datetime


DEBUG = False


def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def die(message, log_path=None):
    line = f"[XML01] {ts()} | ERROR | {message}"
    print(line, file=sys.stderr)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    sys.exit(1)


def log(message, log_path=None):
    line = f"[XML01] {ts()} | {message}"
    if DEBUG:
        print(line)
    if log_path:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def read_root_resolved(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            root = f.readline().strip()
    except Exception as e:
        die(f"cannot read resolved root file: {e}")

    if not root:
        die("resolved root path is empty")

    if not os.path.isdir(root):
        die(f"resolved root path is not a directory: {root}")

    return root


def read_child_mapping(path, log_path):
    entries = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        die(f"cannot read child_mapping.txt: {e}", log_path)

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if "-" not in stripped:
            die(f"invalid mapping line {idx}: missing '-' separator", log_path)

        source_type, rel_folder = stripped.split("-", 1)
        source_type = source_type.strip()
        rel_folder = rel_folder.strip()

        if not source_type or not rel_folder:
            die(f"invalid mapping line {idx}: empty source_type or folder", log_path)

        entries.append((source_type, rel_folder))

    if not entries:
        die("child_mapping.txt contains no valid entries", log_path)

    return entries


def collect_files(folder, source_type):
    if source_type == "archi":
        extensions = (".xml",)
    elif source_type == "bpmn":
        extensions = (".bpmn",)
    else:
        extensions = ()

    files = []
    for name in sorted(os.listdir(folder)):
        full = os.path.join(folder, name)
        if not os.path.isfile(full):
            continue
        if extensions and not name.lower().endswith(extensions):
            continue
        files.append(full)

    return files


def archive_dir_for(root, source_type):
    if source_type == "archi":
        sub = "00-archimatearchive"
    elif source_type == "bpmn":
        sub = "01-bpmnarchive"
    else:
        sub = "99-logs"

    path = os.path.join(root, "03-stages", sub)
    os.makedirs(path, exist_ok=True)
    return path


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    root_resolved = os.path.abspath(
        os.path.join(script_dir, "..", "..", "03-stages", "99-logs", "XML00-root.resolved.txt")
    )

    root = read_root_resolved(root_resolved)

    logs_dir = os.path.join(root, "03-stages", "99-logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, "XML01-sources.log")

    log(f"Using root: {root}", log_path)

    mapping_file = os.path.join(root, "02-artifacts", "00-xml", "child_mapping.txt")
    mappings = read_child_mapping(mapping_file, log_path)

    for source_type, rel_folder in mappings:
        abs_folder = os.path.join(root, rel_folder)

        if not os.path.isdir(abs_folder):
            die(f"source folder not found: {abs_folder}", log_path)

        log(f"Collecting source_type={source_type} from {rel_folder}", log_path)

        files = collect_files(abs_folder, source_type)
        archive_dir = archive_dir_for(root, source_type)
        out_file = os.path.join(archive_dir, "XML01-sources.resolved.txt")

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"SOURCE_TYPE={source_type}\n")
            f.write(f"SOURCE_FOLDER={rel_folder}\n\n")
            for file_path in files:
                rel_path = os.path.relpath(file_path, root)
                f.write(f"FILE={rel_path}\n")

        log(f"Wrote {len(files)} files to {out_file}", log_path)

    print("[XML01] OK | source collection completed")


if __name__ == "__main__":
    main()
