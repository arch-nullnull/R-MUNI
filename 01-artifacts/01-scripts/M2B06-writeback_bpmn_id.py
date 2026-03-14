#!/usr/bin/env python3
# M2B06-writeback_bpmn_id.py
#
# Zweck:
#   Liest alle aktiven BPMN-Dateien und schreibt die BPMN Process ID
#   als Property "BPMN_ID" zurueck in das zugehoerige Archi-Element
#   in master.xml.
#
# Regeln:
#   - BPMN_ID wird NUR gesetzt wenn sie noch nicht vorhanden ist (immutable)
#   - BPMN_ID wird NIE ueberschrieben wenn bereits gesetzt
#   - Leere Werte werden NIE geschrieben
#   - Nur Archi-Elemente (sourceSystem=archi) werden angefasst
#   - PropertyDefinition wird automatisch angelegt wenn fehlend
#
# Match-Hierarchie (in dieser Reihenfolge):
#   1. BPMN process id == Archi identifier        (direkter ID-Match)
#   2. BPMN process name == Archi element name    (Name-Fallback)
#   3. Kein Match -> ueberspringen, nur loggen
#
# Backup:
#   master.xml.bak wird vor dem Schreiben erstellt
#
# Log:
#   <root>/02-stages/99-logs/M2B06-writeback_bpmn_id.log

from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime
import sys
import shutil


# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

ROOT_DIR       = Path(__file__).resolve().parents[2]
ACTIVE_BPMN    = ROOT_DIR / "00-model" / "01-bpmn" / "00-bpmnactive"
MASTER_XML     = ROOT_DIR / "01-artifacts" / "00-xml" / "00-master" / "master.xml"
MASTER_BACKUP  = ROOT_DIR / "01-artifacts" / "00-xml" / "00-master" / "master.xml.bak"
LOG_DIR        = ROOT_DIR / "02-stages" / "99-logs"
LOG_FILE       = LOG_DIR / "M2B06-writeback_bpmn_id.log"

NS_A           = "http://www.opengroup.org/xsd/archimate/3.0/"
NS_XSI         = "http://www.w3.org/2001/XMLSchema-instance"
NS_BPMN        = "http://www.omg.org/spec/BPMN/20100524/MODEL"

PROP_DEF_ID    = "propid-bpmn-id"
PROP_NAME      = "BPMN_ID"

ET.register_namespace("",        NS_A)
ET.register_namespace("xsi",     NS_XSI)
ET.register_namespace("bpmn",    NS_BPMN)
ET.register_namespace("bpmndi",  "http://www.omg.org/spec/BPMN/20100524/DI")
ET.register_namespace("dc",      "http://www.omg.org/spec/DD/20100524/DC")
ET.register_namespace("di",      "http://www.omg.org/spec/DD/20100524/DI")
ET.register_namespace("zeebe",   "http://camunda.org/schema/zeebe/1.0")
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

def get_bpmn_process(bpmn_file: Path) -> tuple[str, str] | None:
    """
    Liest process id und name aus einer BPMN-Datei.
    Gibt (process_id, process_name) zurueck oder None bei Fehler.
    """
    try:
        tree = ET.parse(bpmn_file)
        root = tree.getroot()
        for el in root.iter():
            local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
            if local == "process":
                pid   = (el.get("id")   or "").strip()
                pname = (el.get("name") or "").strip()
                if pid:
                    return pid, pname
    except ET.ParseError as e:
        log(f"[WARN] cannot parse {bpmn_file.name}: {e}")
    return None


# ----------------------------------------------------------
# Archi master.xml Helpers
# ----------------------------------------------------------

def get_element_name(el: ET.Element) -> str:
    """
    Extrahiert den Namen eines Archi-Elements.
    Bevorzugt xml:lang="de", Fallback erster <name> Text.
    """
    a = f"{{{NS_A}}}"
    name_de  = None
    name_any = None
    for child in el:
        clocal = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if clocal != "name":
            continue
        text = (child.text or "").strip()
        if not text:
            continue
        lang = child.get("{http://www.w3.org/XML/1998/namespace}lang", "")
        if lang == "de" and name_de is None:
            name_de = text
        if name_any is None:
            name_any = text
    return name_de or name_any or ""


def get_existing_bpmn_id(el: ET.Element) -> str:
    """
    Liest den aktuellen BPMN_ID Property-Wert eines Archi-Elements.
    Gibt "" zurueck wenn nicht vorhanden.
    """
    a = f"{{{NS_A}}}"
    for props in el:
        plocal = props.tag.split("}")[-1] if "}" in props.tag else props.tag
        if plocal != "properties":
            continue
        for prop in props:
            prop_local = prop.tag.split("}")[-1] if "}" in prop.tag else prop.tag
            if prop_local != "property":
                continue
            ref = prop.get("propertyDefinitionRef", "")
            if ref != PROP_DEF_ID:
                continue
            for val in prop:
                vlocal = val.tag.split("}")[-1] if "}" in val.tag else val.tag
                if vlocal == "value":
                    return (val.text or "").strip()
    return ""


def ensure_property_definition(master_root: ET.Element) -> bool:
    """
    Stellt sicher dass die PropertyDefinition fuer BPMN_ID existiert.
    Legt sie an wenn fehlend.
    Gibt True zurueck wenn neu angelegt, False wenn bereits vorhanden.
    """
    a = f"{{{NS_A}}}"
    for child in master_root:
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if local != "propertyDefinition":
            continue
        if child.get("identifier") == PROP_DEF_ID:
            return False

    # Neu anlegen
    prop_def = ET.Element(f"{{{NS_A}}}propertyDefinition")
    prop_def.set("identifier", PROP_DEF_ID)
    prop_def.set(f"{{{NS_XSI}}}type", "StringProperty")
    name_el = ET.SubElement(prop_def, f"{{{NS_A}}}name")
    name_el.text = PROP_NAME
    master_root.insert(0, prop_def)
    log(f"PropertyDefinition angelegt: {PROP_DEF_ID} / {PROP_NAME}")
    return True


def write_bpmn_id(el: ET.Element, bpmn_id: str):
    """
    Schreibt BPMN_ID als Property auf ein Archi-Element.
    Legt <properties> Block an wenn fehlend.
    """
    a = f"{{{NS_A}}}"

    # Bestehenden <properties> Block suchen
    props_el = None
    for child in el:
        clocal = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if clocal == "properties":
            props_el = child
            break

    if props_el is None:
        props_el = ET.SubElement(el, f"{{{NS_A}}}properties")

    # Neues <property> anlegen
    prop = ET.SubElement(props_el, f"{{{NS_A}}}property")
    prop.set("propertyDefinitionRef", PROP_DEF_ID)
    val = ET.SubElement(prop, f"{{{NS_A}}}value")
    val.text = bpmn_id


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log("start M2B06 writeback BPMN_ID")

    if not ACTIVE_BPMN.exists():
        abort(f"active BPMN directory missing: {ACTIVE_BPMN}")
    if not MASTER_XML.exists():
        abort(f"master.xml missing: {MASTER_XML}")

    # Backup
    shutil.copy2(MASTER_XML, MASTER_BACKUP)
    log(f"backup: {MASTER_BACKUP.name}")

    # master.xml laden
    try:
        tree = ET.parse(MASTER_XML)
        root = tree.getroot()
    except ET.ParseError as e:
        abort(f"cannot parse master.xml: {e}")

    # PropertyDefinition sicherstellen
    ensure_property_definition(root)

    # Archi-Elemente indexieren: id -> element, name -> element
    a = f"{{{NS_A}}}"
    xsi_type_attr = f"{{{NS_XSI}}}type"

    index_by_id   = {}  # identifier -> element
    index_by_name = {}  # name -> element (nur BusinessProcess)

    for el in root.iter():
        local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if local != "element":
            continue
        if el.get("sourceSystem") != "archi":
            continue
        xsi_type = el.get(xsi_type_attr, "")
        if "BusinessProcess" not in xsi_type:
            continue

        archi_id = el.get("identifier", "").strip()
        if archi_id:
            index_by_id[archi_id] = el

        name = get_element_name(el)
        if name:
            index_by_name[name] = el

    log(f"Archi BusinessProcess Elemente: {len(index_by_id)}")

    # BPMN Dateien verarbeiten
    bpmn_files = sorted(ACTIVE_BPMN.glob("*.bpmn"))
    log(f"BPMN Dateien in active: {len(bpmn_files)}")

    stats = {"set": 0, "skip_exists": 0, "skip_no_match": 0, "skip_empty": 0}

    for bpmn_file in bpmn_files:
        result = get_bpmn_process(bpmn_file)
        if not result:
            log(f"[SKIP] kein process Element: {bpmn_file.name}")
            continue

        pid, pname = result

        if not pid:
            log(f"[SKIP] leere process id: {bpmn_file.name}")
            stats["skip_empty"] += 1
            continue

        # Match-Hierarchie
        matched_el   = None
        match_reason = ""

        # Weg 1: direkte ID
        if pid in index_by_id:
            matched_el   = index_by_id[pid]
            match_reason = "ID-Match"

        # Weg 2: Name-Fallback
        if matched_el is None and pname and pname in index_by_name:
            matched_el   = index_by_name[pname]
            match_reason = "Name-Match"

        if matched_el is None:
            log(f"[NO MATCH] {bpmn_file.name} | pid={pid} name='{pname}'")
            stats["skip_no_match"] += 1
            continue

        archi_id = matched_el.get("identifier", "")

        # BPMN_ID immutable — nur setzen wenn noch nicht vorhanden
        existing = get_existing_bpmn_id(matched_el)
        if existing:
            log(f"[SKIP] BPMN_ID bereits gesetzt ({existing}): {archi_id} via {match_reason}")
            stats["skip_exists"] += 1
            continue

        # Schreiben
        write_bpmn_id(matched_el, pid)
        log(f"[SET] BPMN_ID={pid} -> {archi_id} ({get_element_name(matched_el)}) via {match_reason}")
        stats["set"] += 1

    if stats["set"] == 0:
        log("keine Aenderungen — master.xml wird nicht geschrieben")
    else:
        root.set("last-updated",    datetime.now().isoformat(timespec="seconds"))
        root.set("last-updated-by", "M2B06")
        try:
            tree.write(MASTER_XML, encoding="utf-8", xml_declaration=True)
            log(f"master.xml geschrieben")
        except Exception as e:
            abort(f"cannot write master.xml: {e}")

    log(
        f"M2B06 abgeschlossen | "
        f"set={stats['set']} "
        f"skip_exists={stats['skip_exists']} "
        f"skip_no_match={stats['skip_no_match']} "
        f"skip_empty={stats['skip_empty']}"
    )


if __name__ == "__main__":
    main()
