#!/usr/bin/env python3
# XML02-parse_child_xml.py
#
# Flow-Stage:
# - Reads source reference TXTs from XML01
# - Opens each listed XML / BPMN file
# - Extracts basic structural metadata
# - Persists parsed metadata as reference TXT
# - Writes a separate LOG for runtime information
#
# Reference outputs:
#   <root>/02-stages/00-archimatearchive/XML02-parsed.txt
#   <root>/02-stages/01-bpmnarchive/XML02-parsed.txt
#
# Logs:
#   <root>/02-stages/99-logs/XML02-parse.log

import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime


DEBUG = False


def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def die(message, log_path=None):
    line = f"[XML02] {ts()} | ERROR | {message}"
    print(line, file=sys.stderr)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    sys.exit(1)


def log(message, log_path=None):
    line = f"[XML02] {ts()} | {message}"
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

    if not root or not os.path.isdir(root):
        die(f"invalid resolved root path: {root}")

    return root


def read_sources_txt(path, log_path):
    files = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        die(f"cannot read sources file: {e}", log_path)

    for line in lines:
        line = line.strip()
        if line.startswith("FILE="):
            files.append(line.split("=", 1)[1])

    return files


def parse_xml_file(abs_path):
    try:
        tree = ET.parse(abs_path)
        root = tree.getroot()
    except Exception as e:
        return None, f"parse error: {e}"

    tag = root.tag
    namespace = None

    if tag.startswith("{") and "}" in tag:
        namespace = tag.split("}")[0].strip("{")
        tag = tag.split("}", 1)[1]

    return {
        "root_tag": tag,
        "namespace": namespace
    }, None


def process_source(root_path, source_type, archive_subdir, log_path):
    sources_file = os.path.join(
        root_path,
        "02-stages",
        archive_subdir,
        "XML01-sources.resolved.txt"
    )

    if not os.path.isfile(sources_file):
        log(f"no sources file found for {source_type}, skipping", log_path)
        return

    files = read_sources_txt(sources_file, log_path)

    out_file = os.path.join(
        root_path,
        "02-stages",
        archive_subdir,
        "XML02-parsed.txt"
    )

    with open(out_file, "w", encoding="utf-8") as out:
        out.write(f"SOURCE_TYPE={source_type}\n\n")

        for rel_path in files:
            abs_path = os.path.join(root_path, rel_path)

            out.write(f"FILE={rel_path}\n")

            if not os.path.isfile(abs_path):
                out.write("STATUS=missing\n\n")
                log(f"missing file: {rel_path}", log_path)
                continue

            meta, error = parse_xml_file(abs_path)

            if error:
                out.write("STATUS=error\n")
                out.write(f"ERROR={error}\n\n")
                log(f"parse error in {rel_path}: {error}", log_path)
                continue

            out.write("STATUS=ok\n")
            out.write(f"ROOT_TAG={meta['root_tag']}\n")
            if meta["namespace"]:
                out.write(f"NAMESPACE={meta['namespace']}\n")
            out.write("\n")

    log(f"parsed {len(files)} files for {source_type}", log_path)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    root_resolved = os.path.abspath(
        os.path.join(script_dir, "..", "..", "02-stages", "99-logs", "XML00-root.resolved.txt")
    )

    root = read_root_resolved(root_resolved)

    logs_dir = os.path.join(root, "02-stages", "99-logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, "XML02-parse.log")

    log(f"Using root: {root}", log_path)

    process_source(root, "archi", "00-archimatearchive", log_path)
    process_source(root, "bpmn", "01-bpmnarchive", log_path)

    print("[XML02] OK | XML parsing completed")


if __name__ == "__main__":
    main()
