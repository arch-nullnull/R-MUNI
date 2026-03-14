#!/usr/bin/env python3
# ==========================================================
# XML05-clear_merge.py
#
# ZWECK
# ----------------------------------------------------------
# Konsolidierungsregeln aus sync.txt auf das aktuelle
# master.generated.xml anwenden.
# Logische Duplikate aufloesen, bereinigten Output schreiben.
#
# Das Script fuehrt aus was in sync.txt deklariert ist.
# Keine impliziten Entscheidungen.
#
# Inputs:
#   <root>/01-artifacts/00-xml/00-master/master.generated.xml
#   <root>/01-artifacts/00-xml/02-sync/sync.txt
#
# Output:
#   <root>/01-artifacts/00-xml/00-master/master.cleared.xml
#
# Log:
#   <root>/02-stages/99-logs/XML05-clear_merge.log
#
# Basis: Cleaning Run 5.5 | Stage 5
# Bibliothek: xml.etree.ElementTree (Standard — kein lxml)
# ==========================================================

import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime


# ==========================================================
# STAGE 0 – PFAD-AUFLOESUNG
# ==========================================================

def resolve_root() -> str:
    """
    Liest den Root-Pfad aus XML00-root.resolved.txt.
    Die Datei liegt zwei Ebenen ueber dem Script-Ordner
    im 02-stages/99-logs Verzeichnis.
    """
    script_dir = os.path.abspath(os.path.dirname(__file__))
    resolved_path = os.path.abspath(
        os.path.join(script_dir, "..", "..", "02-stages", "99-logs", "XML00-root.resolved.txt")
    )
    if not os.path.isfile(resolved_path):
        raise RuntimeError(f"XML00-root.resolved.txt nicht gefunden: {resolved_path}")
    with open(resolved_path, "r", encoding="utf-8") as f:
        root = f.readline().strip()
    if not root or not os.path.isdir(root):
        raise RuntimeError(f"Ungueltiger Root-Pfad in XML00-root.resolved.txt: {root}")
    return root


# ==========================================================
# STAGE 1 – INPUTS LADEN
# ==========================================================

def load_master(path: str) -> ET.ElementTree:
    """Laedt master.generated.xml als ElementTree."""
    return ET.parse(path)


def load_sync_rules(path: str) -> list:
    """
    Liest sync.txt und gibt eine Liste von Regel-Dicts zurueck.
    Format pro Zeile: <selector> :: <action>
    Ohne :: wird action="keep" angenommen.
    """
    rules = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "::" in line:
                selector, action = line.split("::", 1)
                action = action.strip()
            else:
                selector = line
                action = "keep"
            rules.append({
                "selector": selector.strip(),
                "action": action
            })
    return rules


# ==========================================================
# STAGE 2 – OBJEKT-INDEX AUFBAUEN
# ==========================================================

def build_index(tree: ET.ElementTree) -> dict:
    """
    Erstellt einen Index aller Elemente im Baum.
    Indiziert nach 'identifier' (Archi-Anker) und 'id' (externe ID).
    """
    index = {
        "all": [],
        "by_identifier": {},
        "by_external_id": {}
    }

    for elem in tree.getroot().iter():
        index["all"].append(elem)

        identifier = elem.get("identifier")
        external_id = elem.get("id")

        if identifier:
            index["by_identifier"].setdefault(identifier, []).append(elem)

        if external_id:
            index["by_external_id"].setdefault(external_id, []).append(elem)

    return index


# ==========================================================
# STAGE 3 – NAMESPACE-HANDLING & SELECTOR-MATCHING
# ==========================================================

def strip_ns(tag: str) -> str:
    """
    Entfernt den XML-Namespace-Prefix aus einem ET-Tag.
    Aus '{http://...}serviceTask' wird 'serviceTask'.
    Aus 'bpmn:serviceTask' (ohne geschwungene Klammer) bleibt es unveraendert.
    """
    if tag and tag.startswith("{") and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def match_selector(selector: str, element: ET.Element) -> bool:
    """
    Prueft ob ein Element auf einen Selector passt.

    Selector-Format: <source>-<entry-point>+filter+filter

    source:      archi | bpmn
    entry-point: lokaler Tag-Name oder * fuer Wildcard
    filter:      has:id | has:identifier | no:identifier | same:* (wird spaeter geprueft)
    """
    if "-" not in selector:
        return False

    source, rest = selector.split("-", 1)
    local_tag = strip_ns(element.tag)
    source_system = element.get("sourceSystem", "")

    # --- Source-Check: archi ---
    if source == "archi":
        is_archi = (
            source_system == "archi"
            or local_tag in (
                "element", "relationship", "item", "view",
                "node", "connection", "folder", "propertyDefinition"
            )
        )
        if not is_archi:
            return False

    # --- Source-Check: bpmn ---
    if source == "bpmn":
        is_bpmn = (
            source_system == "bpmn"
            or local_tag in (
                "serviceTask", "process", "startEvent", "endEvent",
                "sequenceFlow", "userTask", "subProcess", "callActivity",
                "exclusiveGateway", "parallelGateway", "inclusiveGateway",
                "intermediateCatchEvent", "intermediateThrowEvent",
                "boundaryEvent", "documentation", "definitions",
                "extensionElements"
            )
        )
        if not is_bpmn:
            return False

    # --- Entry-Point und Filter trennen ---
    if "+" in rest:
        entry_point, filters_str = rest.split("+", 1)
        filters = filters_str.split("+")
    else:
        entry_point = rest
        filters = []

    entry_point = entry_point.strip()

    # --- Entry-Point matching ---
    # 'bpmn:serviceTask' -> lokaler Vergleich mit 'serviceTask'
    if entry_point != "*":
        ep_local = entry_point.split(":")[-1] if ":" in entry_point else entry_point
        if local_tag != ep_local:
            return False

    # --- Filter-Tokens auswerten ---
    for flt in filters:
        flt = flt.strip()
        if flt == "has:id" and not element.get("id"):
            return False
        if flt == "has:identifier" and not element.get("identifier"):
            return False
        if flt == "no:identifier" and element.get("identifier"):
            return False
        if flt.startswith("same:"):
            continue  # wird beim Merge-Vorgang geprueft

    return True


# ==========================================================
# STAGE 4 – KONSOLIDIERUNGS-AKTIONEN
# ==========================================================

def find_parent(tree: ET.ElementTree, child: ET.Element):
    """
    Sucht das Eltern-Element eines gegebenen Elements im Baum.
    ET hat kein .getparent() — daher manuell suchen.
    """
    for parent in tree.getroot().iter():
        if child in list(parent):
            return parent
    return None


def merge_objects(tree: ET.ElementTree, canonical: ET.Element,
                  duplicate: ET.Element, log: list) -> None:
    """Entfernt das Duplikat aus dem Baum."""
    parent = find_parent(tree, duplicate)
    if parent is not None:
        parent.remove(duplicate)
        log.append(
            f"MERGE: duplicate entfernt id={duplicate.get('id')} "
            f"-> canonical identifier={canonical.get('identifier')}"
        )
    else:
        log.append(
            f"MERGE: kein Parent gefunden fuer id={duplicate.get('id')} — uebersprungen"
        )


def keep_object(obj: ET.Element, log: list) -> None:
    log.append(f"KEEP: id={obj.get('id')}")


def ignore_object(obj: ET.Element, log: list) -> None:
    log.append(f"IGNORE: id={obj.get('id')}")


# ==========================================================
# STAGE 5 – REGELN ANWENDEN
# ==========================================================

def apply_rules(tree: ET.ElementTree, rules: list, index: dict, log: list) -> None:
    """
    Wendet alle Regeln aus sync.txt auf den Baum an.
    Arbeitet auf einer Kopie der Element-Liste um Mutations-Probleme zu vermeiden.
    """
    for rule in rules:
        selector = rule["selector"]
        action = rule["action"]

        for elem in list(index["all"]):
            if not match_selector(selector, elem):
                continue

            external_id = elem.get("id")

            if action == "merge" and external_id and not elem.get("identifier"):
                candidates = index["by_external_id"].get(external_id, [])
                canonicals = [e for e in candidates if e.get("identifier")]

                if len(canonicals) == 1:
                    canonical = canonicals[0]

                    # same:type Pruefung
                    if "same:type" in selector:
                        xsi_ns = "{http://www.w3.org/2001/XMLSchema-instance}type"
                        if canonical.get(xsi_ns) != elem.get(xsi_ns):
                            log.append(f"SKIP: type mismatch id={external_id}")
                            continue

                    # same:sourceSystem Pruefung
                    if "same:sourceSystem" in selector:
                        if canonical.get("sourceSystem") != elem.get("sourceSystem"):
                            log.append(f"SKIP: sourceSystem mismatch id={external_id}")
                            continue

                    merge_objects(tree, canonical, elem, log)

                elif len(canonicals) == 0:
                    log.append(f"SKIP: kein canonical fuer id={external_id}")
                else:
                    log.append(f"AMBIGUOUS: id={external_id} | candidates={len(canonicals)}")

            elif action == "keep":
                keep_object(elem, log)

            elif action == "ignore":
                ignore_object(elem, log)


# ==========================================================
# STAGE 6 – OUTPUT SCHREIBEN
# ==========================================================

def write_output(tree: ET.ElementTree, path: str) -> None:
    """Schreibt den bereinigten Baum als XML-Datei."""
    ET.indent(tree.getroot(), space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def write_log(entries: list, path: str) -> None:
    """Schreibt das Log in eine Textdatei."""
    with open(path, "w", encoding="utf-8") as f:
        for line in entries:
            f.write(line + "\n")


# ==========================================================
# STAGE 7 – MAIN
# ==========================================================

def main() -> None:
    ROOT = resolve_root()

    XML_DIR    = os.path.join(ROOT, "01-artifacts", "00-xml")
    MASTER_IN  = os.path.join(XML_DIR, "00-master", "master.generated.xml")
    MASTER_OUT = os.path.join(XML_DIR, "00-master", "master.cleared.xml")
    SYNC_FILE  = os.path.join(XML_DIR, "02-sync", "sync.txt")
    LOG_DIR    = os.path.join(ROOT, "02-stages", "99-logs")
    LOG_FILE   = os.path.join(LOG_DIR, "XML05-clear_merge.log")

    # Pflicht-Dateien pruefen
    for p in [MASTER_IN, SYNC_FILE]:
        if not os.path.isfile(p):
            print(f"[XML05] ERROR | Datei fehlt: {p}", file=sys.stderr)
            sys.exit(1)

    log = []
    log.append("=" * 50)
    log.append(f"XML05 STARTED: {datetime.utcnow().isoformat()}")

    tree  = load_master(MASTER_IN)
    rules = load_sync_rules(SYNC_FILE)
    index = build_index(tree)

    log.append(f"master geladen: {MASTER_IN}")
    log.append(f"sync-regeln geladen: {len(rules)} Regeln")
    log.append(f"index aufgebaut: {len(index['all'])} Elemente")

    apply_rules(tree, rules, index, log)

    write_output(tree, MASTER_OUT)

    log.append(f"OUTPUT GESCHRIEBEN: {MASTER_OUT}")
    log.append(f"XML05 COMPLETED: {datetime.utcnow().isoformat()}")
    log.append("=" * 50)

    write_log(log, LOG_FILE)
    print(f"[XML05] OK | master cleared -> {MASTER_OUT}")


if __name__ == "__main__":
    main()
