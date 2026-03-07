#!/usr/bin/env python3
"""
FLW01-discover – XML-Typ-Scanner fuer FLOW

Scannt den XML-Ordner und ermittelt:
  - Archi: alle vorhandenen xsi:type-Werte (element_type)
  - BPMN:  alle vorhandenen Element-Tags  (element_tag)

Zeigt zusaetzlich fuer jeden gefundenen Typ/Tag:
  - ob er in flowtriggers.txt konfiguriert ist
  - welche Section matcht
  - was der dispatch_key ist
  - welchen order-Wert die Regel hat

Ausgabe:
  - 03-stages/99-logs/flw01-discover.log  (detailliert, mit Fundorten)
  - 03-stages/flw01-discover.txt          (kompakt, Referenz fuer flowtriggers.txt)
"""

import os
import sys
import configparser
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def localname(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def get_xsi_type(elem: ET.Element) -> str:
    for k, v in elem.attrib.items():
        if localname(k) == "type":
            return v
    return ""


def is_archi(root: ET.Element) -> bool:
    for node in root.iter():
        if localname(node.tag) in ("propertyDefinition", "model"):
            return True
    return False


def is_bpmn(root: ET.Element) -> bool:
    for node in root.iter():
        if localname(node.tag) in ("definitions", "process", "serviceTask",
                                    "userTask", "sendTask"):
            return True
    return False


# ---------------------------------------------------------------------------
# Blueprint Root
# ---------------------------------------------------------------------------

def resolve_blueprint_root() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_file  = os.path.abspath(os.path.join(script_dir, "..", "..", "root.txt"))

    if not os.path.isfile(root_file):
        print(f"[FLW01] ABORT: root.txt not found: {root_file}")
        sys.exit(1)

    root_value = None
    with open(root_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("BLUEPRINT_ROOT="):
                root_value = line.split("=", 1)[1].strip()
                break

    if not root_value:
        print("[FLW01] ABORT: BLUEPRINT_ROOT missing or empty")
        sys.exit(1)

    if not os.path.isabs(root_value):
        root_value = os.path.abspath(
            os.path.join(os.path.dirname(root_file), root_value)
        )

    return root_value


# ---------------------------------------------------------------------------
# flowtriggers.txt einlesen
# ---------------------------------------------------------------------------

def load_trigger_rules(path: str) -> list:
    if not os.path.isfile(path):
        print(f"[FLW01] WARN: flowtriggers.txt not found: {path}")
        return []

    cfg = configparser.ConfigParser(
        comment_prefixes=("#", ";"),
        inline_comment_prefixes=("#",),
    )
    cfg.read(path, encoding="utf-8")

    rules = []
    for section in cfg.sections():
        raw = dict(cfg[section])
        try:
            order = int(raw.get("order", "0").strip())
        except ValueError:
            order = 0
        rules.append({
            "section":      section,
            "order":        order,
            "source":       raw.get("source", "").strip().lower(),
            "element_tag":  raw.get("element_tag", "").strip(),
            "element_type": raw.get("element_type", "").strip() or None,
            "dispatch_key": raw.get("dispatch_key", "").strip(),
            "conditions":   {
                k: v for k, v in raw.items() if k.startswith("condition.")
            },
        })

    rules.sort(key=lambda r: r["order"])
    return rules


def match_archi_type(xtype: str, rules: list) -> list:
    matches = []
    for r in rules:
        if r["source"] != "archi":
            continue
        if r["element_type"] and r["element_type"] != xtype:
            continue
        matches.append(r)
    return matches


def match_bpmn_tag(tag: str, rules: list) -> list:
    matches = []
    for r in rules:
        if r["source"] != "bpmn":
            continue
        if r["element_tag"] == tag:
            matches.append(r)
    return matches


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def scan_archi(root: ET.Element, rel_path: str,
               types: dict, types_detail: dict) -> None:
    for elem in root.iter():
        if localname(elem.tag) != "element":
            continue
        xtype = get_xsi_type(elem)
        if not xtype:
            continue
        types[xtype].add(rel_path)
        identifier = (elem.attrib.get("identifier") or "").strip()
        if identifier:
            types_detail[xtype].add(identifier)


def scan_bpmn(root: ET.Element, rel_path: str, tags: dict) -> None:
    skip = {
        "definitions", "process", "collaboration", "participant",
        "messageFlow", "sequenceFlow", "laneSet", "lane",
        "incoming", "outgoing", "extensionElements", "documentation",
        "conditionExpression", "multiInstanceLoopCharacteristics",
        "dataInputAssociation", "dataOutputAssociation",
        "resourceRole", "potentialOwner", "formalExpression",
        "Bounds", "BPMNShape", "BPMNEdge", "BPMNLabel", "BPMNDiagram",
        "BPMNPlane", "waypoint",
    }
    for elem in root.iter():
        ln = localname(elem.tag)
        if ln in skip:
            continue
        if any(kw in ln for kw in (
            "Task", "Event", "Gateway", "SubProcess",
            "CallActivity", "AdHocSubProcess"
        )):
            tags[ln].add(rel_path)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def _match_label(matches: list) -> str:
    if not matches:
        return "NOT CONFIGURED"
    parts = []
    for m in matches:
        parts.append(
            f"section=[{m['section']}] order={m['order']} dispatch_key={m['dispatch_key']}"
        )
    return " | ".join(parts)


def write_log(path: str, ts: str,
              archi_types: dict, archi_detail: dict,
              bpmn_tags: dict, scanned: list,
              rules: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("FLW01-discover – Scan Log\n")
        f.write(f"Run: {ts}\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Scanned files ({len(scanned)}):\n")
        for s in scanned:
            f.write(f"  {s}\n")
        f.write("\n")

        f.write(f"Trigger rules loaded ({len(rules)}):\n")
        for r in rules:
            f.write(f"  order={r['order']:>4}  [{r['section']}]  "
                    f"source={r['source']}  dispatch_key={r['dispatch_key']}\n")
        f.write("\n")

        f.write("=" * 60 + "\n")
        f.write(f"ARCHI – element_type ({len(archi_types)} unique)\n")
        f.write("=" * 60 + "\n")
        if archi_types:
            for t in sorted(archi_types):
                matches = match_archi_type(t, rules)
                label   = _match_label(matches)
                files   = sorted(archi_types[t])
                ids     = sorted(archi_detail.get(t, set()))

                f.write(f"\n  {t}\n")
                f.write(f"    Trigger match : {label}\n")
                f.write(f"    Found in:\n")
                for fn in files:
                    f.write(f"      {fn}\n")
                if ids:
                    f.write(f"    Identifiers ({len(ids)}):\n")
                    for i in ids[:10]:
                        f.write(f"      {i}\n")
                    if len(ids) > 10:
                        f.write(f"      ... (+{len(ids) - 10} more)\n")
        else:
            f.write("  (none found)\n")

        f.write("\n")

        f.write("=" * 60 + "\n")
        f.write(f"BPMN – element_tag ({len(bpmn_tags)} unique)\n")
        f.write("=" * 60 + "\n")
        if bpmn_tags:
            for t in sorted(bpmn_tags):
                matches = match_bpmn_tag(t, rules)
                label   = _match_label(matches)
                files   = sorted(bpmn_tags[t])

                f.write(f"\n  {t}\n")
                f.write(f"    Trigger match : {label}\n")
                f.write(f"    Found in:\n")
                for fn in files:
                    f.write(f"      {fn}\n")
        else:
            f.write("  (none found)\n")

        f.write("\n")


def write_summary(path: str, ts: str,
                  archi_types: dict, bpmn_tags: dict,
                  rules: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("# flw01-discover.txt\n")
        f.write(f"# Generated: {ts}\n")
        f.write("# Use this as reference when writing flowtriggers.txt\n")
        f.write("# CONFIGURED     = matched in flowtriggers.txt\n")
        f.write("# NOT CONFIGURED = not yet mapped\n")
        f.write("#\n\n")

        f.write("# ------------------------------------------------------------\n")
        f.write("# ARCHI – available element_type values\n")
        f.write("# ------------------------------------------------------------\n")
        if archi_types:
            for t in sorted(archi_types):
                matches = match_archi_type(t, rules)
                count   = len(archi_types[t])
                if matches:
                    sections = ", ".join(f"[{m['section']}]" for m in matches)
                    orders   = ", ".join(str(m["order"]) for m in matches)
                    dk       = " / ".join(m["dispatch_key"] for m in matches)
                    status   = f"CONFIGURED -> {sections}  order={orders}  dispatch_key={dk}"
                else:
                    status = "NOT CONFIGURED"
                f.write(f"element_type = {t:<35} # {count} file(s) | {status}\n")
        else:
            f.write("# (none found)\n")

        f.write("\n")

        f.write("# ------------------------------------------------------------\n")
        f.write("# BPMN – available element_tag values\n")
        f.write("# ------------------------------------------------------------\n")
        if bpmn_tags:
            for t in sorted(bpmn_tags):
                matches = match_bpmn_tag(t, rules)
                count   = len(bpmn_tags[t])
                if matches:
                    sections = ", ".join(f"[{m['section']}]" for m in matches)
                    orders   = ", ".join(str(m["order"]) for m in matches)
                    dk       = " / ".join(m["dispatch_key"] for m in matches)
                    status   = f"CONFIGURED -> {sections}  order={orders}  dispatch_key={dk}"
                else:
                    status = "NOT CONFIGURED"
                f.write(f"element_tag  = {t:<35} # {count} file(s) | {status}\n")
        else:
            f.write("# (none found)\n")

        f.write("\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    blueprint_root = resolve_blueprint_root()

    xml_root      = os.path.join(blueprint_root, "02-artifacts", "00-xml", "03-child")
    triggers_file = os.path.join(blueprint_root, "02-artifacts", "04-flow", "flowtriggers.txt")
    log_path      = os.path.join(blueprint_root, "03-stages", "99-logs", "flw01-discover.log")
    txt_path      = os.path.join(blueprint_root, "03-stages", "flw01-discover.txt")

    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[FLW01] {ts} | Starting scan: {xml_root}")

    rules        = load_trigger_rules(triggers_file)
    archi_types  = defaultdict(set)
    archi_detail = defaultdict(set)
    bpmn_tags    = defaultdict(set)
    scanned      = []

    for dirpath, _, files in os.walk(xml_root):
        for fn in sorted(files):
            if not fn.lower().endswith((".xml", ".bpmn", ".archimate")):
                continue
            path = os.path.join(dirpath, fn)
            rel  = os.path.relpath(path, blueprint_root)
            scanned.append(rel)
            try:
                tree      = ET.parse(path)
                root_elem = tree.getroot()
            except Exception as e:
                print(f"[FLW01] WARN: could not parse {rel}: {e}")
                continue
            if is_archi(root_elem):
                scan_archi(root_elem, rel, archi_types, archi_detail)
            if is_bpmn(root_elem):
                scan_bpmn(root_elem, rel, bpmn_tags)

    write_log(log_path, ts, archi_types, archi_detail, bpmn_tags, scanned, rules)
    write_summary(txt_path, ts, archi_types, bpmn_tags, rules)

    print(f"[FLW01] {ts} | Scanned       : {len(scanned)} file(s)")
    print(f"[FLW01] {ts} | Archi types   : {len(archi_types)}")
    print(f"[FLW01] {ts} | BPMN tags     : {len(bpmn_tags)}")
    print(f"[FLW01] {ts} | Rules loaded  : {len(rules)}")

    unconfigured_archi = [t for t in archi_types if not match_archi_type(t, rules)]
    unconfigured_bpmn  = [t for t in bpmn_tags  if not match_bpmn_tag(t, rules)]
    if unconfigured_archi:
        print(f"[FLW01] {ts} | NOT CONFIGURED (archi): {', '.join(sorted(unconfigured_archi))}")
    if unconfigured_bpmn:
        print(f"[FLW01] {ts} | NOT CONFIGURED (bpmn) : {', '.join(sorted(unconfigured_bpmn))}")

    print(f"[FLW01] {ts} | Log     -> {log_path}")
    print(f"[FLW01] {ts} | Summary -> {txt_path}")


if __name__ == "__main__":
    main()
