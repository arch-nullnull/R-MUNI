#!/usr/bin/env python3
"""
FLW00-scriptrunner – Modellgetriebener Script-Orchestrator

- liest XML-Modelle aus dem Blueprint
- erkennt Trigger gemäß flowtriggers.txt (kein Hardcoding)
- führt gemappte Scripts in der durch "order" definierten Reihenfolge aus

FLW00 interpretiert keine Prozesse, keine Diagramme
und keine Engine-Semantik.
"""

import os
import sys
import subprocess
import configparser
import xml.etree.ElementTree as ET
from datetime import datetime


# ---------------------------------------------------------------------------
# Logging & Abbruch
# ---------------------------------------------------------------------------

_log_handle = None  # wird in init_log() gesetzt


def log(msg: str) -> None:
    ts   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[FLW00] {ts} | {msg}"
    print(line)
    if _log_handle:
        _log_handle.write(line + "\n")
        _log_handle.flush()


def abort(msg: str) -> None:
    log(f"ABORT: {msg}")
    if _log_handle:
        _log_handle.close()
    sys.exit(1)


def init_log(path: str) -> None:
    global _log_handle
    os.makedirs(os.path.dirname(path), exist_ok=True)
    _log_handle = open(path, "a", encoding="utf-8")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _log_handle.write("\n" + "=" * 60 + "\n")
    _log_handle.write(f"FLW00 Run: {ts}\n")
    _log_handle.write("=" * 60 + "\n")
    _log_handle.flush()


# ---------------------------------------------------------------------------
# Blueprint Root
# ---------------------------------------------------------------------------

def _read_root_value(root_file: str) -> str:
    """Liest <rootfolder> aus root.cfg – ohne log() Abhängigkeit."""
    with open(root_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("<rootfolder>="):
                return line.split("=", 1)[1].strip()
    return None


def resolve_blueprint_root() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_file  = os.path.abspath(os.path.join(script_dir, "..", "..", "root.cfg"))

    if not os.path.isfile(root_file):
        abort(f"root.cfg not found: {root_file}")

    root_value = None
    with open(root_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("<rootfolder>="):
                if root_value is not None:
                    abort("multiple <rootfolder> entries found")
                root_value = line.split("=", 1)[1].strip()

    if not root_value:
        abort("<rootfolder> missing or empty")

    if not os.path.isabs(root_value):
        root_value = os.path.abspath(
            os.path.join(os.path.dirname(root_file), root_value)
        )

    if not os.path.isdir(root_value):
        abort(f"resolved <rootfolder> does not exist: {root_value}")

    log(f"Blueprint root resolved: {root_value}")
    return root_value


# ---------------------------------------------------------------------------
# Mapping
# ---------------------------------------------------------------------------

def load_mapping(path: str) -> dict:
    if not os.path.isfile(path):
        abort(f"flowmapping.txt not found: {path}")

    mapping = {}
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                abort(f"invalid mapping line {idx}: {line}")
            key, script = line.split("=", 1)
            key    = key.strip()
            script = script.strip()
            if not key or not script:
                abort(f"invalid mapping line {idx}: {line}")
            if key in mapping:
                abort(f"duplicate mapping key: {key}")
            mapping[key] = script

    log(f"Loaded {len(mapping)} mapping entries")
    return mapping


# ---------------------------------------------------------------------------
# Trigger-Konfiguration
# ---------------------------------------------------------------------------

def load_trigger_rules(path: str) -> list:
    if not os.path.isfile(path):
        abort(f"flowtriggers.txt not found: {path}")

    cfg = configparser.ConfigParser(
        comment_prefixes=("#", ";"),
        inline_comment_prefixes=("#",),
    )
    cfg.read(path, encoding="utf-8")

    rules = []
    for section in cfg.sections():
        raw = dict(cfg[section])

        order_raw = raw.get("order", "").strip()
        if not order_raw:
            abort(f"[{section}] order is required")
        try:
            order = int(order_raw)
        except ValueError:
            abort(f"[{section}] order must be an integer, got: '{order_raw}'")

        source = raw.get("source", "").strip().lower()
        if source not in ("archi", "bpmn"):
            abort(f"[{section}] source must be 'archi' or 'bpmn', got: '{source}'")

        element_tag = raw.get("element_tag", "").strip()
        if not element_tag:
            abort(f"[{section}] element_tag is required")

        element_type = raw.get("element_type", "").strip() or None

        conditions = []
        for ck in sorted(k for k in raw if k.startswith("condition.")):
            conditions.append(_parse_condition(section, ck, raw[ck].strip()))

        # Wildcard-Modus: scriptTask darf ohne Condition laufen
        # (kein condition.<n> = alle scriptTask-Elemente werden ausgeführt)
        # Alle anderen Sektionen benötigen weiterhin mindestens eine Condition.
        element_tag_raw = raw.get("element_tag", "").strip()
        if not conditions and element_tag_raw != "scriptTask":
            abort(f"[{section}] at least one condition.<n> is required")

        dk_raw = raw.get("dispatch_key", "").strip()

        # scriptTask: kein dispatch_key nötig — documentation wird intern
        # als Scriptname verwendet. Alle anderen Sektionen benötigen dispatch_key.
        if not dk_raw and element_tag_raw != "scriptTask":
            abort(f"[{section}] dispatch_key is required")

        dispatch_key = _parse_dispatch_key(section, dk_raw) if dk_raw else None

        rules.append({
            "section":      section,
            "order":        order,
            "source":       source,
            "element_tag":  element_tag,
            "element_type": element_type,
            "conditions":   conditions,
            "dispatch_key": dispatch_key,
        })

    rules.sort(key=lambda r: r["order"])

    log(f"Loaded {len(rules)} trigger rule(s) from flowtriggers.txt "
        f"(order: {', '.join(str(r['order']) for r in rules)})")
    return rules


def _parse_condition(section: str, key: str, val: str) -> dict:
    if val.startswith("property:"):
        rest = val[len("property:"):]
        if "=" not in rest:
            abort(f"[{section}] {key}: property condition needs 'Name=Wert', got: '{val}'")
        name, value = rest.split("=", 1)
        return {"kind": "property", "name": name.strip(), "value": value.strip()}
    if val.startswith("tag:"):
        rest = val[len("tag:"):]
        if ":" not in rest:
            abort(f"[{section}] {key}: tag condition needs 'TagName:Text', got: '{val}'")
        tag_name, contains = rest.split(":", 1)
        return {"kind": "tag", "tag": tag_name.strip(), "contains": contains.strip()}
    abort(f"[{section}] {key}: unknown condition format: '{val}'")


def _parse_dispatch_key(section: str, val: str) -> dict:
    if val.startswith("property:"):
        name = val[len("property:"):].strip()
        if not name:
            abort(f"[{section}] dispatch_key property name is empty")
        return {"kind": "property", "name": name}
    if val.startswith("attr:"):
        name = val[len("attr:"):].strip()
        if not name:
            abort(f"[{section}] dispatch_key attr name is empty")
        return {"kind": "attr", "name": name}
    abort(f"[{section}] dispatch_key: unknown format: '{val}'")


# ---------------------------------------------------------------------------
# XML Helpers
# ---------------------------------------------------------------------------

def localname(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def get_xsi_type(elem: ET.Element) -> str:
    for k, v in elem.attrib.items():
        if localname(k) == "type":
            return v
    return ""


# ---------------------------------------------------------------------------
# Archi Property-Aufloesung
# ---------------------------------------------------------------------------

def _build_propdefs(root: ET.Element) -> dict:
    propdefs = {}
    for node in root.iter():
        if localname(node.tag) != "propertyDefinition":
            continue
        pid = (node.attrib.get("identifier") or "").strip()
        if not pid:
            continue
        for ch in list(node):
            if localname(ch.tag) == "name":
                name_text = (ch.text or "").strip()
                if name_text:
                    propdefs[pid] = name_text
                break
    return propdefs


def _read_props(elem: ET.Element, propdefs: dict) -> dict:
    props = {}
    for ch in list(elem):
        if localname(ch.tag) != "properties":
            continue
        for p in list(ch):
            if localname(p.tag) != "property":
                continue
            ref       = (p.attrib.get("propertyDefinitionRef") or "").strip()
            prop_name = propdefs.get(ref)
            if not prop_name:
                continue
            for vch in list(p):
                if localname(vch.tag) == "value":
                    value_text = (vch.text or "").strip()
                    if value_text:
                        props[prop_name] = value_text
                    break
    return props


# ---------------------------------------------------------------------------
# Trigger Detection
# ---------------------------------------------------------------------------

def detect_triggers(root: ET.Element, rules: list) -> list:
    triggers = []
    propdefs = None
    if any(r["source"] == "archi" for r in rules):
        propdefs = _build_propdefs(root)

    for rule in rules:
        if rule["source"] == "archi":
            triggers.extend(_detect_archi(root, rule, propdefs))
        elif rule["source"] == "bpmn":
            triggers.extend(_detect_bpmn(root, rule))

    return triggers


def _detect_archi(root: ET.Element, rule: dict, propdefs: dict) -> list:
    triggers = []
    for elem in root.iter():
        if localname(elem.tag) != rule["element_tag"]:
            continue
        if rule["element_type"] and get_xsi_type(elem) != rule["element_type"]:
            continue
        props = _read_props(elem, propdefs)
        if not _check_conditions(rule["conditions"], props=props):
            continue
        key = _resolve_dispatch_key(rule["dispatch_key"], elem, props)
        if not key:
            continue
        triggers.append({
            "source":  "archi",
            "section": rule["section"],
            "order":   rule["order"],
            "key":     key,
            "info":    (elem.attrib.get("identifier") or "").strip(),
        })
    return triggers


def _detect_bpmn(root: ET.Element, rule: dict) -> list:
    triggers = []
    for task in root.iter():
        if localname(task.tag) != rule["element_tag"]:
            continue
        tag_contents = {
            localname(ch.tag): (ch.text or "").strip()
            for ch in list(task)
        }
        if not _check_conditions(rule["conditions"], tag_contents=tag_contents):
            continue

        # scriptTask: kein dispatch_key konfiguriert →
        # documentation-Inhalt direkt als Scriptname verwenden.
        # Leer = SKIP (kein Fehler, kein Abbruch).
        if rule["dispatch_key"] is None:
            key = tag_contents.get("documentation", "").strip()
        else:
            key = _resolve_dispatch_key(rule["dispatch_key"], task, {})

        if not key:
            task_name = task.attrib.get("name", "(kein Name)")
            log(f"  SKIP (keine documentation): scriptTask '{task_name}'")
            continue
        triggers.append({
            "source":  "bpmn",
            "section": rule["section"],
            "order":   rule["order"],
            "key":     key,
            "info":    task.attrib.get("name", ""),
        })
    return triggers


def _check_conditions(conditions: list, props: dict = None,
                      tag_contents: dict = None) -> bool:
    for cond in conditions:
        if cond["kind"] == "property":
            if not props or props.get(cond["name"]) != cond["value"]:
                return False
        elif cond["kind"] == "tag":
            if not tag_contents:
                return False
            if cond["contains"] not in tag_contents.get(cond["tag"], ""):
                return False
    return True


def _resolve_dispatch_key(dispatch_key: dict, elem: ET.Element,
                          props: dict) -> str:
    kind = dispatch_key["kind"]
    name = dispatch_key["name"]
    if kind == "property":
        return props.get(name, "")
    if kind == "attr":
        return (elem.attrib.get(name) or "").strip()
    return ""


# ---------------------------------------------------------------------------
# Script Execution
# ---------------------------------------------------------------------------

def run_script(script_path: str, cwd: str) -> None:
    log(f"EXEC: {script_path}")
    result = subprocess.run([sys.executable, script_path], cwd=cwd)
    if result.returncode != 0:
        abort(f"script failed: {script_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_file  = os.path.abspath(os.path.join(script_dir, "..", "..", "root.cfg"))

    pre_root = None
    if os.path.isfile(root_file):
        pre_root = _read_root_value(root_file)
        if pre_root and not os.path.isabs(pre_root):
            pre_root = os.path.abspath(
                os.path.join(os.path.dirname(root_file), pre_root)
            )

    log_path = os.path.join(
        pre_root or ".", "02-stages", "99-logs", "flw00-scriptrunner.log"
    )
    init_log(log_path)

    blueprint_root = resolve_blueprint_root()

    # Flow-Ordner: BPMN und ArchiMate Flows getrennt gespeichert
    flow_bpmn_root  = os.path.join(blueprint_root, "01-artifacts", "04-flow", "01-bpmnFLW")
    flow_archi_root = os.path.join(blueprint_root, "01-artifacts", "04-flow", "00-archimateFLW")
    scripts_dir     = os.path.join(blueprint_root, "01-artifacts", "01-scripts")
    mapping_file    = os.path.join(blueprint_root, "01-artifacts", "04-flow", "flowmapping.txt")
    triggers_file   = os.path.join(blueprint_root, "01-artifacts", "04-flow", "flowtriggers.txt")

    mapping = load_mapping(mapping_file)
    rules   = load_trigger_rules(triggers_file)

    # Phase 1: alle Trigger aus BPMN- und ArchiMate-Flow-Ordnern sammeln
    all_triggers = []

    scan_roots = [
        ("bpmn",   flow_bpmn_root),
        ("archi",  flow_archi_root),
    ]

    for scan_type, scan_root in scan_roots:
        if not os.path.isdir(scan_root):
            log(f"SKIP (Ordner nicht vorhanden): {scan_root}")
            continue
        for dirpath, _, files in os.walk(scan_root):
            for fn in sorted(files):
                if not fn.lower().endswith((".xml", ".bpmn", ".archimate")):
                    continue
                path = os.path.join(dirpath, fn)
                rel  = os.path.relpath(path, blueprint_root)
                log(f"SCAN [{scan_type}]: {rel}")
                try:
                    tree = ET.parse(path)
                except Exception as e:
                    abort(f"invalid XML: {rel} ({e})")
                root_elem = tree.getroot()
                found = detect_triggers(root_elem, rules)
                for t in found:
                    log(f"  TRIGGER [order={t['order']}] [{t['section']}] "
                        f"key={t['key']} info={t['info']}")
                all_triggers.extend(found)

    log(f"Detected {len(all_triggers)} trigger(s)")

    # Phase 2: nach order sortieren
    all_triggers.sort(key=lambda t: t["order"])
    order_summary = ", ".join(t["key"] + "(order=" + str(t["order"]) + ")" for t in all_triggers)
    log(f"Execution order: {order_summary}")

    # Phase 3: Scripts ausfuehren
    executed = 0
    for t in all_triggers:
        # scriptTask: key = documentation-Inhalt = direkt der Scriptname.
        # Kein flowmapping.txt Lookup noetig.
        # Leer = bereits in _detect_bpmn gefiltert, kommt hier nicht an.
        if t["section"] == "bpmn_scripttask":
            script_name = t["key"]
        else:
            # ArchiMate WorkPackage und serviceTask: Lookup via flowmapping.txt
            script_name = mapping.get(t["key"])
            if not script_name:
                log(f"SKIP (unmapped): key={t['key']} [{t['section']}]")
                continue
        script_path = os.path.join(scripts_dir, script_name)
        if not os.path.isfile(script_path):
            abort(f"mapped script not found: {script_path}")
        run_script(script_path, blueprint_root)
        executed += 1

    log(f"FLW00 finished: executed={executed}, total_triggers={len(all_triggers)}")
    log(f"Log written to: {log_path}")

    if _log_handle:
        _log_handle.close()


if __name__ == "__main__":
    main()
