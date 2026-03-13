#!/usr/bin/env python3
"""
FLW02-map_elements – Element-ID-Scanner für flowmapping.txt

Scannt BPMN- und Archi-XML-Dateien und gibt alle relevanten Elemente aus:
  - ID (z.B. Activity_0abc123)
  - Typ (z.B. serviceTask, userTask, WorkPackage)
  - Name (aus dem name-Attribut)

Sonderregel für BPMN serviceTask mit Trigger:Ja:
  Wenn ein serviceTask in seiner <documentation> "Trigger:Ja" enthält,
  wird der name-Wert direkt als Scriptname übernommen.
  → Ergebnis ist eine fertige flowmapping.txt Zeile ohne manuellen Eingriff.
  → Fehlt der Name trotz Trigger:Ja → Platzhalter <SCRIPT_HIER_EINTRAGEN>

Alle anderen Elemente (kein Trigger:Ja) erscheinen als auskommentierte
Referenz-Zeilen — zur Übersicht, aber nicht zum direkten Einfügen.

Ausgabe:
  - 03-stages/99-logs/flw02-map_elements.log  (detailliert)
  - 03-stages/flw02-map_elements.txt          (Referenz für flowmapping.txt)
"""

import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def localname(tag: str) -> str:
    """Entfernt den Namespace-Prefix aus einem XML-Tag."""
    return tag.split("}", 1)[-1] if "}" in tag else tag


def get_xsi_type(elem: ET.Element) -> str:
    """Liest den xsi:type Wert eines Elements (fuer Archi)."""
    for k, v in elem.attrib.items():
        if localname(k) == "type":
            return v
    return ""


def is_archi(root: ET.Element) -> bool:
    """Prueft ob eine XML-Datei eine Archi-Datei ist."""
    for node in root.iter():
        if localname(node.tag) in ("propertyDefinition", "model"):
            return True
    return False


def is_bpmn(root: ET.Element) -> bool:
    """Prueft ob eine XML-Datei eine BPMN-Datei ist."""
    for node in root.iter():
        if localname(node.tag) in ("definitions", "process", "serviceTask",
                                   "userTask", "sendTask"):
            return True
    return False


def has_trigger_ja(elem: ET.Element) -> bool:
    """
    Prueft ob ein BPMN Element eine <documentation> mit "Trigger:Ja" hat.
    Namespace-agnostisch.
    """
    for child in elem:
        if localname(child.tag) == "documentation":
            text = (child.text or "").strip()
            if "Trigger:Ja" in text:
                return True
    return False


# ---------------------------------------------------------------------------
# Blueprint Root ermitteln
# ---------------------------------------------------------------------------

def resolve_blueprint_root() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_file  = os.path.abspath(os.path.join(script_dir, "..", "..", "root.txt"))

    if not os.path.isfile(root_file):
        print(f"[FLW02] ABORT: root.txt nicht gefunden: {root_file}")
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
        print("[FLW02] ABORT: BLUEPRINT_ROOT fehlt oder ist leer in root.txt")
        sys.exit(1)

    if not os.path.isabs(root_value):
        root_value = os.path.abspath(
            os.path.join(os.path.dirname(root_file), root_value)
        )

    return root_value


# ---------------------------------------------------------------------------
# BPMN Scanner
# ---------------------------------------------------------------------------

BPMN_RELEVANT_KEYWORDS = (
    "Task", "Event", "Gateway", "SubProcess",
    "CallActivity", "AdHocSubProcess"
)

BPMN_SKIP_TAGS = {
    "definitions", "process", "collaboration", "participant",
    "messageFlow", "sequenceFlow", "laneSet", "lane",
    "incoming", "outgoing", "extensionElements", "documentation",
    "conditionExpression", "multiInstanceLoopCharacteristics",
    "dataInputAssociation", "dataOutputAssociation",
    "resourceRole", "potentialOwner", "formalExpression",
    "Bounds", "BPMNShape", "BPMNEdge", "BPMNLabel",
    "BPMNDiagram", "BPMNPlane", "waypoint",
}


def scan_bpmn_elements(root: ET.Element, rel_path: str) -> list:
    """
    Scannt eine BPMN-Datei.

    Fuer serviceTask mit Trigger:Ja:
      - trigger_ja = True
      - script     = Name des Tasks (oder Platzhalter wenn leer)

    Fuer alle anderen Elemente:
      - trigger_ja = False
      - script     = None (nur zur Uebersicht)
    """
    results = []

    for elem in root.iter():
        ln = localname(elem.tag)
        if ln in BPMN_SKIP_TAGS:
            continue
        if not any(kw in ln for kw in BPMN_RELEVANT_KEYWORDS):
            continue

        elem_id   = elem.attrib.get("id",   "").strip()
        elem_name = elem.attrib.get("name", "").strip()

        if not elem_id:
            continue

        # Sonderregel: serviceTask + Trigger:Ja -> Script direkt aus Name
        if ln == "serviceTask" and has_trigger_ja(elem):
            if elem_name:
                script     = elem_name
                trigger_ja = True
                warnung    = None
            else:
                script     = "<SCRIPT_HIER_EINTRAGEN>"
                trigger_ja = True
                warnung    = "WARNUNG: Trigger:Ja aber kein Scriptname als Name eingetragen!"
        else:
            script     = None
            trigger_ja = False
            warnung    = None

        results.append({
            "id":         elem_id,
            "name":       elem_name if elem_name else "(kein Name)",
            "typ":        ln,
            "datei":      rel_path,
            "trigger_ja": trigger_ja,
            "script":     script,
            "warnung":    warnung,
        })

    return results


# ---------------------------------------------------------------------------
# Archi Scanner
# ---------------------------------------------------------------------------

def scan_archi_elements(root: ET.Element, rel_path: str) -> list:
    """Scannt eine Archi-XML-Datei. Archi hat keine Trigger:Ja Logik."""
    results = []
    for elem in root.iter():
        if localname(elem.tag) != "element":
            continue
        xtype      = get_xsi_type(elem)
        identifier = elem.attrib.get("identifier", "").strip()

        name_elem = None
        for child in elem:
            if localname(child.tag) == "name":
                name_elem = (child.text or "").strip()
                break
        if not name_elem:
            name_elem = elem.attrib.get("name", "").strip()

        if not identifier or not xtype:
            continue

        results.append({
            "id":         identifier,
            "name":       name_elem if name_elem else "(kein Name)",
            "typ":        xtype,
            "datei":      rel_path,
            "trigger_ja": False,
            "script":     None,
            "warnung":    None,
        })

    return results


# ---------------------------------------------------------------------------
# Output schreiben
# ---------------------------------------------------------------------------

def write_log(path: str, ts: str,
              all_elements: list, scanned: list) -> None:
    """Detailliertes Logfile."""
    trigger_elems = [e for e in all_elements if e["trigger_ja"]]
    warnungen     = [e for e in all_elements if e["warnung"]]

    with open(path, "w", encoding="utf-8") as f:
        f.write("FLW02-map_elements - Detail Log\n")
        f.write(f"Run: {ts}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Gescannte Dateien  : {len(scanned)}\n")
        f.write(f"Elemente gesamt    : {len(all_elements)}\n")
        f.write(f"Davon Trigger:Ja   : {len(trigger_elems)}\n")
        f.write(f"Warnungen          : {len(warnungen)}\n\n")

        f.write("Gescannte Dateien:\n")
        for s in scanned:
            f.write(f"  {s}\n")
        f.write("\n")

        if warnungen:
            f.write("=" * 60 + "\n")
            f.write("WARNUNGEN\n")
            f.write("=" * 60 + "\n")
            for e in warnungen:
                f.write(f"  ID   : {e['id']}\n")
                f.write(f"  Datei: {e['datei']}\n")
                f.write(f"  Info : {e['warnung']}\n\n")

        f.write("=" * 60 + "\n")
        f.write("ALLE ELEMENTE - nach Datei\n")
        f.write("=" * 60 + "\n\n")

        dateien = sorted(set(e["datei"] for e in all_elements))
        for datei in dateien:
            elems = [e for e in all_elements if e["datei"] == datei]
            f.write(f"Datei: {datei}\n")
            for e in elems:
                trigger_label = "Trigger:Ja" if e["trigger_ja"] else "kein Trigger"
                f.write(f"  [{trigger_label}] {e['id']}\n")
                f.write(f"    Name  : {e['name']}\n")
                f.write(f"    Typ   : {e['typ']}\n")
                if e["script"]:
                    f.write(f"    Script: {e['script']}\n")
                if e["warnung"]:
                    f.write(f"    !! {e['warnung']}\n")
                f.write("\n")
            f.write("-" * 40 + "\n\n")


def write_mapping_reference(path: str, ts: str,
                             all_elements: list, scanned: list) -> None:
    """
    Ausgabe-File fuer flowmapping.txt.

    ABSCHNITT 1: Fertige Mapping-Zeilen (serviceTask + Trigger:Ja)
                 -> direkt kopierbar, ID=Scriptname bereits befuellt
    ABSCHNITT 2: Alle uebrigen Elemente zur Uebersicht (auskommentiert)
    """
    trigger_elems = [e for e in all_elements if e["trigger_ja"]]
    other_elems   = [e for e in all_elements if not e["trigger_ja"]]
    warnungen     = [e for e in all_elements if e["warnung"]]

    with open(path, "w", encoding="utf-8") as f:
        f.write("# flw02-map_elements.txt\n")
        f.write(f"# Generiert: {ts}\n")
        f.write("#\n")
        f.write("# ABSCHNITT 1 - Fertige Mapping-Zeilen\n")
        f.write("#   serviceTask mit Trigger:Ja -> direkt in flowmapping.txt kopieren\n")
        f.write("#   Scriptname wurde automatisch aus dem Task-Namen uebernommen\n")
        f.write("#\n")
        f.write("# ABSCHNITT 2 - Alle uebrigen Elemente (nur Referenz, auskommentiert)\n")
        f.write("#\n")
        f.write(f"# Gescannte Dateien : {len(scanned)}\n")
        f.write(f"# Elemente gesamt   : {len(all_elements)}\n")
        f.write(f"# Davon Trigger:Ja  : {len(trigger_elems)}\n")
        if warnungen:
            f.write(f"# WARNUNGEN         : {len(warnungen)} (Trigger:Ja ohne Scriptname!)\n")
        f.write("#\n\n")

        # ABSCHNITT 1
        f.write("# " + "=" * 56 + "\n")
        f.write("# ABSCHNITT 1 - Fertige Mapping-Zeilen\n")
        f.write("# serviceTask + Trigger:Ja -> direkt kopierbar in flowmapping.txt\n")
        f.write("# " + "=" * 56 + "\n\n")

        if trigger_elems:
            dateien = sorted(set(e["datei"] for e in trigger_elems))
            for datei in dateien:
                elems = [e for e in trigger_elems if e["datei"] == datei]
                f.write(f"# Datei: {datei}\n")
                f.write("# " + "-" * 54 + "\n")
                for e in elems:
                    if e["warnung"]:
                        f.write(f"# !! {e['warnung']}\n")
                        f.write(f"# {e['id']:<40} | {e['typ']:<20} | Name fehlt\n")
                        f.write(f"{e['id']}={e['script']}\n")
                    else:
                        f.write(f"# {e['id']:<40} | {e['typ']:<20} | \"{e['name']}\"\n")
                        f.write(f"{e['id']}={e['script']}\n")
                    f.write("#\n")
                f.write("\n")
        else:
            f.write("# (keine serviceTask Elemente mit Trigger:Ja gefunden)\n\n")

        # ABSCHNITT 2
        f.write("# " + "=" * 56 + "\n")
        f.write("# ABSCHNITT 2 - Uebrige Elemente (nur Referenz, auskommentiert)\n")
        f.write("# " + "=" * 56 + "\n\n")

        if other_elems:
            dateien = sorted(set(e["datei"] for e in other_elems))
            for datei in dateien:
                elems = [e for e in other_elems if e["datei"] == datei]
                f.write(f"# Datei: {datei}\n")
                f.write("# " + "-" * 54 + "\n")
                for e in elems:
                    f.write(f"# {e['id']:<40} | {e['typ']:<20} | \"{e['name']}\"\n")
                    f.write(f"# {e['id']}=<SCRIPT_HIER_EINTRAGEN>\n")
                    f.write("#\n")
                f.write("\n")
        else:
            f.write("# (keine weiteren Elemente)\n\n")


# ---------------------------------------------------------------------------
# Hauptprogramm
# ---------------------------------------------------------------------------

def main() -> None:
    blueprint_root = resolve_blueprint_root()

    xml_root  = os.path.join(blueprint_root, "02-artifacts", "00-xml", "03-child")
    log_path  = os.path.join(blueprint_root, "03-stages", "99-logs", "flw02-map_elements.log")
    txt_path  = os.path.join(blueprint_root, "03-stages", "flw02-map_elements.txt")

    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[FLW02] {ts} | Starte Scan: {xml_root}")

    if not os.path.isdir(xml_root):
        print(f"[FLW02] ABORT: XML-Ordner nicht gefunden: {xml_root}")
        sys.exit(1)

    all_elements = []
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
                print(f"[FLW02] WARN: Datei konnte nicht gelesen werden: {rel}: {e}")
                continue

            if is_bpmn(root_elem):
                elems = scan_bpmn_elements(root_elem, rel)
                ready = sum(1 for e in elems if e["trigger_ja"])
                print(f"[FLW02] BPMN  | {len(elems):>3} Elemente | {ready:>2} Trigger:Ja | {rel}")
                all_elements.extend(elems)

            elif is_archi(root_elem):
                elems = scan_archi_elements(root_elem, rel)
                print(f"[FLW02] Archi | {len(elems):>3} Elemente |  - Trigger:Ja | {rel}")
                all_elements.extend(elems)

            else:
                print(f"[FLW02] SKIP  | Unbekanntes Format | {rel}")

    write_log(log_path, ts, all_elements, scanned)
    write_mapping_reference(txt_path, ts, all_elements, scanned)

    trigger_elems = [e for e in all_elements if e["trigger_ja"]]
    warnungen     = [e for e in all_elements if e["warnung"]]

    print("")
    print(f"[FLW02] {ts} | Gescannte Dateien   : {len(scanned)}")
    print(f"[FLW02] {ts} | Elemente gesamt     : {len(all_elements)}")
    print(f"[FLW02] {ts} | Fertige Mappings    : {len(trigger_elems)}")
    if warnungen:
        print(f"[FLW02] {ts} | !! WARNUNGEN        : {len(warnungen)} (Trigger:Ja ohne Scriptname)")
    print(f"[FLW02] {ts} | Log     -> {log_path}")
    print(f"[FLW02] {ts} | Mapping -> {txt_path}")
    print("")
    if trigger_elems and not warnungen:
        print("[FLW02] Abschnitt 1 aus flw02-map_elements.txt direkt in flowmapping.txt kopieren - fertig.")
    elif warnungen:
        print("[FLW02] ACHTUNG: Warnungs-Zeilen haben noch keinen Scriptnamen.")
        print("         -> Camunda Modeler oeffnen -> serviceTask Name eintragen -> Script neu ausfuehren.")


if __name__ == "__main__":
    main()
