#!/usr/bin/env python3
# XML03-build_index.py
#
# Purpose:
# - Build a deterministic, minimal index of objects per model file.
# - No content duplication, only references + core attributes.
#
# Inputs:
#   <root>/02-stages/99-logs/XML00-root.resolved.txt
#   <root>/02-stages/00-archimatearchive/XML01-sources.resolved.txt
#   <root>/02-stages/01-bpmnarchive/XML01-sources.resolved.txt
#
# Outputs:
#   <root>/02-stages/00-archimatearchive/XML03-index.xml
#   <root>/02-stages/01-bpmnarchive/XML03-index.xml
#
# Logs:
#   <root>/02-stages/99-logs/XML03-index.log

import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime


DEBUG = False

XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
XSI_TYPE_ATTR = f"{{{XSI_NS}}}type"


def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def die(message, log_path=None):
    line = f"[XML03] {ts()} | ERROR | {message}"
    print(line, file=sys.stderr)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    sys.exit(1)


def log(message, log_path=None):
    line = f"[XML03] {ts()} | {message}"
    if DEBUG:
        print(line)
    if log_path:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def strip_ns(tag):
    if tag.startswith("{") and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


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
            for raw in f:
                line = raw.strip()
                if line.startswith("FILE="):
                    files.append(line.split("=", 1)[1])
    except Exception as e:
        die(f"cannot read sources file: {e}", log_path)

    return files


def first_text(elem):
    if elem is None:
        return None
    txt = (elem.text or "").strip()
    return txt if txt else None


def build_archi_entries(tree):
    root = tree.getroot()
    entries = []

    # We index common OEF object containers by tag name.
    # This is intentionally simple: "look for tag, take identifier, take xsi:type if present".
    wanted = {"element", "relationship", "item", "view", "node", "connection", "folder", "propertyDefinition", "property"}

    for e in root.iter():
        tag = strip_ns(e.tag)
        if tag not in wanted:
            continue

        obj_id = e.attrib.get("identifier")
        if not obj_id:
            continue

        xsi_type = e.attrib.get(XSI_TYPE_ATTR)

        # Optional convenience name: first <name> descendant text (any lang)
        name = None
        name_elem = e.find(".//{*}name")
        name = first_text(name_elem)

        entries.append({
            "kind": tag,
            "id": obj_id,
            "tag": tag,
            "xsi_type": xsi_type,
            "name": name
        })

    entries.sort(key=lambda x: (x["kind"], x["id"]))
    return entries


def build_bpmn_entries(tree):
    root = tree.getroot()
    entries = []

    # BPMN: index any element that has an "id" attribute.
    # Keep tag localname (e.g. serviceTask) but preserve kind as "bpmn:<tag>" for readability.
    for e in root.iter():
        obj_id = e.attrib.get("id")
        if not obj_id:
            continue

        tag_local = strip_ns(e.tag)
        kind = f"bpmn:{tag_local}"

        # Optional convenience name: @name if present
        name = e.attrib.get("name")

        entries.append({
            "kind": kind,
            "id": obj_id,
            "tag": tag_local,
            "xsi_type": None,
            "name": name.strip() if isinstance(name, str) and name.strip() else None
        })

    entries.sort(key=lambda x: (x["kind"], x["id"]))
    return entries


def write_index_xml(out_path, source, models, log_path):
    idx = ET.Element("index", {
        "version": "1",
        "source": source,
        "created": ts()
    })

    for m in models:
        model_el = ET.SubElement(idx, "model", {
            "file": m["file"],
            "name": m["name"]
        })

        for ent in m["entries"]:
            attrs = {
                "kind": ent["kind"],
                "id": ent["id"],
                "tag": ent["tag"],
            }
            if ent.get("xsi_type"):
                attrs["xsi_type"] = ent["xsi_type"]
            if ent.get("name"):
                attrs["name"] = ent["name"]

            ET.SubElement(model_el, "entry", attrs)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    ET.ElementTree(idx).write(out_path, encoding="utf-8", xml_declaration=True)
    log(f"wrote index: {out_path}", log_path)


def process_source(root_path, source, archive_subdir, builder_fn, log_path):
    sources_file = os.path.join(root_path, "02-stages", archive_subdir, "XML01-sources.resolved.txt")
    if not os.path.isfile(sources_file):
        log(f"no sources file for {source}, skipping: {sources_file}", log_path)
        return

    rel_files = read_sources_txt(sources_file, log_path)
    models = []

    for rel_path in rel_files:
        abs_path = os.path.join(root_path, rel_path)
        if not os.path.isfile(abs_path):
            log(f"{source}: missing file: {rel_path}", log_path)
            continue

        try:
            tree = ET.parse(abs_path)
        except Exception as e:
            log(f"{source}: parse error: {rel_path} | {e}", log_path)
            continue

        try:
            entries = builder_fn(tree)
        except Exception as e:
            log(f"{source}: index build error: {rel_path} | {e}", log_path)
            continue

        models.append({
            "file": rel_path,
            "name": os.path.basename(rel_path),
            "entries": entries
        })

        log(f"{source}: indexed model {os.path.basename(rel_path)} | entries={len(entries)}", log_path)

    out_path = os.path.join(root_path, "02-stages", archive_subdir, "XML03-index.xml")
    write_index_xml(out_path, source, models, log_path)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    root_resolved = os.path.abspath(
        os.path.join(script_dir, "..", "..", "02-stages", "99-logs", "XML00-root.resolved.txt")
    )
    root = read_root_resolved(root_resolved)

    logs_dir = os.path.join(root, "02-stages", "99-logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, "XML03-index.log")

    log(f"Using root: {root}", log_path)

    process_source(root, "archi", "00-archimatearchive", build_archi_entries, log_path)
    process_source(root, "bpmn", "01-bpmnarchive", build_bpmn_entries, log_path)

    print("[XML03] OK | index build completed")


if __name__ == "__main__":
    main()
