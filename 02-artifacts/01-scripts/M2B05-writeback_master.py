#!/usr/bin/env python3
# M2B05-writeback_master.py
#
# Purpose:
# - Read all enriched *.bpmn files from active BPMN directory
# - Write complete BPMN content back into master.xml
# - *.bpmn always wins on conflict (newest source)
# - Annotate sourceSystem=bpmn, sourceModel=<filename>
# - Update master.xml last-updated timestamp
#
# Strategy:
# - Per *.bpmn file: extract <process> id (= Archi identifier)
# - Search master.xml for existing <definitions> block with same process id
#   - NOT found: append complete <definitions> subtree
#   - FOUND: replace existing block (*.bpmn wins)
# - Write master.xml
#
# GUARANTEES:
# - Archi elements (sourceSystem=archi) are NEVER touched
# - No IDs are modified
# - Empty/hull-only BPMN files are written back as-is
#   (hull = process with no children except BPMNDiagram)
#
# Inputs:
#   <root>/01-model/01-bpmn/00-bpmnactive/*.bpmn
#   <root>/02-artifacts/00-xml/00-master/master.xml
#
# Output:
#   <root>/02-artifacts/00-xml/00-master/master.xml  (in-place update)
#
# Logs:
#   <root>/03-stages/99-logs/M2B05-writeback.log

from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime
import sys
import shutil


# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

ACTIVE_BPMN_DIR = ROOT_DIR / "01-model" / "01-bpmn" / "00-bpmnactive"
MASTER_XML = ROOT_DIR / "02-artifacts" / "00-xml" / "00-master" / "master.xml"
MASTER_BACKUP = ROOT_DIR / "02-artifacts" / "00-xml" / "00-master" / "master.xml.bak"

LOG_DIR = ROOT_DIR / "03-stages" / "99-logs"
LOG_FILE = LOG_DIR / "M2B05-writeback.log"

NS_BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL"
NS_BPMNDI = "http://www.omg.org/spec/BPMN/20100524/DI"

# Alle bekannten BPMN Namespace-Prefixe registrieren
# damit sie beim Schreiben erhalten bleiben
ET.register_namespace("bpmn", NS_BPMN)
ET.register_namespace("bpmndi", NS_BPMNDI)
ET.register_namespace("dc", "http://www.omg.org/spec/DD/20100524/DC")
ET.register_namespace("di", "http://www.omg.org/spec/DD/20100524/DI")
ET.register_namespace("zeebe", "http://camunda.org/schema/zeebe/1.0")
ET.register_namespace("camunda", "http://camunda.org/schema/1.0/bpmn")
ET.register_namespace("modeler", "http://camunda.org/schema/modeler/1.0")


# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------

def log(msg: str):
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def abort(msg: str):
    log(f"[ABORT] {msg}")
    sys.exit(1)


# ----------------------------------------------------------
# BPMN Helpers
# ----------------------------------------------------------

def get_process_id(bpmn_root: ET.Element) -> str | None:
    """
    Extrahiert die process id aus einem <definitions> Root-Element.
    Sucht nach dem ersten <process> Element unabhaengig vom Namespace.
    """
    for el in bpmn_root.iter():
        local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if local == "process":
            return el.get("id")
    return None


def is_hull_only(bpmn_root: ET.Element) -> bool:
    """
    Prueft ob ein BPMN File nur eine leere Huelle ist
    (process hat keine Tasks, Events, Gateways etc.)
    Nuetzlich fuer Logging aber kein Ausschlussgrund.
    """
    content_tags = {
        "serviceTask", "userTask", "scriptTask", "businessRuleTask",
        "sendTask", "receiveTask", "manualTask", "callActivity",
        "subProcess", "startEvent", "endEvent", "intermediateCatchEvent",
        "intermediateThrowEvent", "boundaryEvent",
        "exclusiveGateway", "parallelGateway", "inclusiveGateway",
        "eventBasedGateway", "complexGateway"
    }
    for el in bpmn_root.iter():
        local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if local in content_tags:
            return False
    return True


def annotate_bpmn_elements(bpmn_root: ET.Element, source_model: str):
    """
    Setzt sourceSystem=bpmn und sourceModel=<filename> auf alle
    direkten Top-Level Elemente (process, BPMNDiagram etc.)
    """
    for el in bpmn_root:
        local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        # Nur relevante BPMN Top-Level Elemente annotieren
        if local in ("process", "BPMNDiagram", "collaboration", "message",
                     "signal", "error", "escalation", "dataStore"):
            el.set("sourceSystem", "bpmn")
            el.set("sourceModel", source_model)


# ----------------------------------------------------------
# master.xml: BPMN Block Suche und Ersetzung
# ----------------------------------------------------------

def find_existing_bpmn_block(master_root: ET.Element, process_id: str) -> ET.Element | None:
    """
    Sucht im master.xml nach einem <definitions> Block der einen
    <process id=process_id> enthaelt.
    Gibt das <definitions> Element zurueck oder None.
    """
    for el in master_root:
        local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if local != "definitions":
            continue
        pid = get_process_id(el)
        if pid == process_id:
            return el
    return None


def replace_or_append_bpmn_block(
    master_root: ET.Element,
    new_definitions: ET.Element,
    process_id: str,
    source_model: str
) -> str:
    """
    Ersetzt einen bestehenden <definitions> Block in master.xml
    oder haengt ihn neu an.
    Gibt 'replaced' oder 'appended' zurueck.
    """
    annotate_bpmn_elements(new_definitions, source_model)

    existing = find_existing_bpmn_block(master_root, process_id)

    if existing is not None:
        # Position des bestehenden Blocks merken und ersetzen
        children = list(master_root)
        idx = children.index(existing)
        master_root.remove(existing)
        master_root.insert(idx, new_definitions)
        return "replaced"
    else:
        master_root.append(new_definitions)
        return "appended"


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log("start M2B05 writeback")

    if not ACTIVE_BPMN_DIR.exists():
        abort(f"active BPMN directory missing: {ACTIVE_BPMN_DIR}")

    if not MASTER_XML.exists():
        abort(f"master.xml missing: {MASTER_XML}")

    # Safety backup vor dem Schreiben
    shutil.copy2(MASTER_XML, MASTER_BACKUP)
    log(f"backup created: {MASTER_BACKUP.name}")

    # master.xml laden
    try:
        master_tree = ET.parse(MASTER_XML)
        master_root = master_tree.getroot()
    except ET.ParseError as e:
        abort(f"cannot parse master.xml: {e}")

    bpmn_files = sorted(ACTIVE_BPMN_DIR.glob("*.bpmn"))
    log(f"BPMN files found: {len(bpmn_files)}")

    stats = {"appended": 0, "replaced": 0, "skipped": 0, "hull": 0, "error": 0}

    for bpmn_file in bpmn_files:
        try:
            bpmn_tree = ET.parse(bpmn_file)
            bpmn_root = bpmn_tree.getroot()
        except ET.ParseError as e:
            log(f"[ERROR] cannot parse {bpmn_file.name}: {e}")
            stats["error"] += 1
            continue

        process_id = get_process_id(bpmn_root)

        if not process_id:
            log(f"[SKIP] no process id found in {bpmn_file.name}")
            stats["skipped"] += 1
            continue

        hull = is_hull_only(bpmn_root)
        if hull:
            stats["hull"] += 1
            log(f"[HULL] {bpmn_file.name} | process={process_id} (hull-only, writing back as-is)")
        else:
            log(f"[WRITE] {bpmn_file.name} | process={process_id}")

        action = replace_or_append_bpmn_block(
            master_root,
            bpmn_root,
            process_id,
            bpmn_file.name
        )

        stats[action] += 1
        log(f"  -> {action} in master.xml")

    # Timestamp auf master root setzen
    master_root.set("last-updated", datetime.now().isoformat(timespec="seconds"))
    master_root.set("last-updated-by", "M2B05")

    # master.xml schreiben
    try:
        master_tree.write(
            MASTER_XML,
            encoding="utf-8",
            xml_declaration=True
        )
    except Exception as e:
        abort(f"cannot write master.xml: {e}")

    log(
        f"master.xml updated | "
        f"appended={stats['appended']} replaced={stats['replaced']} "
        f"hull={stats['hull']} skipped={stats['skipped']} error={stats['error']}"
    )
    log("M2B05 writeback completed successfully")


if __name__ == "__main__":
    main()
