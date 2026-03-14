#!/usr/bin/env python3
# HLP10-cleanup_property_definitions.py
#
# Zweck:
#   Bereinigt veraltete und doppelte PropertyDefinitions in master.xml.
#   Behält ausschließlich die aktuelle PropertyDefinition für "3PartyId"
#   (identifier=propid-3partyid).
#   Alle anderen PropertyDefinitions werden entfernt.
#
#   Hintergrund:
#   Durch frühere Entwicklungsversuche sind veraltete PropertyDefinitions
#   (ID3Party, 3rdPartyID) und doppelte identifier (propid-1) in master.xml
#   entstanden. Diese verhindern dass Archi die 3PartyId korrekt importiert.
#
# GARANTIEN:
#   - Nur PropertyDefinitions werden angefasst
#   - Alle anderen Elemente (ArchiMate, BPMN) bleiben unverändert
#   - master.xml.bak wird vor dem Schreiben erstellt
#   - Alle entfernten Definitionen werden geloggt
#
# Einmalig ausführen — danach kann das Script gelöscht werden.
#
# Log:
#   <root>/02-stages/99-logs/HLP10-cleanup_property_definitions.log

from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime
import sys
import shutil

ROOT_DIR    = Path(__file__).resolve().parents[2]
MASTER_XML  = ROOT_DIR / "01-artifacts" / "00-xml" / "00-master" / "master.xml"
MASTER_BAK  = ROOT_DIR / "01-artifacts" / "00-xml" / "00-master" / "master.xml.bak"
LOG_DIR     = ROOT_DIR / "02-stages" / "99-logs"
LOG_FILE    = LOG_DIR / "HLP10-cleanup_property_definitions.log"

NS_A   = "http://www.opengroup.org/xsd/archimate/3.0/"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"

# Die einzige PropertyDefinition die BEHALTEN wird
KEEP_IDENTIFIER = "propid-3partyid"
KEEP_NAME       = "3PartyId"

ET.register_namespace("", NS_A)
ET.register_namespace("xsi", NS_XSI)
ET.register_namespace("bpmn",    "http://www.omg.org/spec/BPMN/20100524/MODEL")
ET.register_namespace("bpmndi",  "http://www.omg.org/spec/BPMN/20100524/DI")
ET.register_namespace("dc",      "http://www.omg.org/spec/DD/20100524/DC")
ET.register_namespace("di",      "http://www.omg.org/spec/DD/20100524/DI")
ET.register_namespace("zeebe",   "http://camunda.org/schema/zeebe/1.0")
ET.register_namespace("camunda", "http://camunda.org/schema/1.0/bpmn")
ET.register_namespace("modeler", "http://camunda.org/schema/modeler/1.0")


def log(msg: str):
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def abort(msg: str):
    log(f"[ABORT] {msg}")
    sys.exit(1)


def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log("start HLP10 cleanup property definitions")

    if not MASTER_XML.exists():
        abort(f"master.xml fehlt: {MASTER_XML}")

    # Backup
    shutil.copy2(MASTER_XML, MASTER_BAK)
    log(f"Backup erstellt: {MASTER_BAK.name}")

    try:
        tree = ET.parse(MASTER_XML)
        root = tree.getroot()
    except ET.ParseError as e:
        abort(f"master.xml kann nicht geparst werden: {e}")

    a = f"{{{NS_A}}}"

    # Alle PropertyDefinitions finden
    to_remove = []
    keep_found = False

    for child in list(root):
        local = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if local != "propertyDefinition":
            continue

        ident   = child.get("identifier", "")
        name_el = child.find(f"{a}name")
        name    = name_el.text.strip() if (name_el is not None and name_el.text) else ""

        if ident == KEEP_IDENTIFIER and name == KEEP_NAME:
            log(f"  BEHALTEN: identifier='{ident}'  name='{name}'")
            keep_found = True
        else:
            log(f"  ENTFERNEN: identifier='{ident}'  name='{name}'")
            to_remove.append(child)

    # Entfernen
    for el in to_remove:
        root.remove(el)
        log(f"  -> entfernt")

    if not keep_found:
        log("[WARN] Ziel-PropertyDefinition (propid-3partyid / 3PartyId) wurde nicht gefunden!")
        log("       Bitte M2B06 danach ausführen — sie wird dann neu angelegt.")

    log(f"Entfernt: {len(to_remove)} PropertyDefinitions")

    # Schreiben
    root.set("last-updated",    datetime.now().isoformat(timespec="seconds"))
    root.set("last-updated-by", "HLP10")

    try:
        tree.write(MASTER_XML, encoding="utf-8", xml_declaration=True)
    except Exception as e:
        abort(f"master.xml kann nicht geschrieben werden: {e}")

    log("HLP10 abgeschlossen — master.xml bereinigt")
    log("Nächster Schritt: M2B06 ausführen um 3PartyId neu zu schreiben")


if __name__ == "__main__":
    main()
