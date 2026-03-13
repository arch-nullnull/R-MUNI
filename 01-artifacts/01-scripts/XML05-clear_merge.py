#!/usr/bin/env python3
# ==========================================================
# XML05-clear_merge.py
#
# PURPOSE
# ----------------------------------------------------------
# Apply declarative consolidation rules to the current
# master XML in order to resolve logical duplicates and
# produce a fixed, consistent output state.
#
# The script executes exactly what is declared in sync.txt.
# No implicit decisions are made.
# ==========================================================

import os
from datetime import datetime
from lxml import etree


# ==========================================================
# STAGE 0 – PATH RESOLUTION
# ==========================================================

def resolve_root() -> str:
    script_dir = os.path.abspath(os.path.dirname(__file__))
    resolved_path = os.path.abspath(
        os.path.join(script_dir, "..", "..", "02-stages", "99-logs", "XML00-root.resolved.txt")
    )
    if not os.path.isfile(resolved_path):
        raise RuntimeError(f"XML00-root.resolved.txt not found at: {resolved_path}")
    with open(resolved_path, "r", encoding="utf-8") as f:
        root = f.readline().strip()
    if not root or not os.path.isdir(root):
        raise RuntimeError(f"Invalid root path in XML00-root.resolved.txt: {root}")
    return root


# ==========================================================
# STAGE 1 – LOAD INPUTS
# ==========================================================

def load_master(path):
    return etree.parse(path)

def load_sync_rules(path):
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
# STAGE 2 – BUILD OBJECT INDEX
# ==========================================================

def build_index(tree):
    index = {
        "all": [],
        "by_identifier": {},
        "by_external_id": {}
    }

    for elem in tree.xpath("//*"):
        index["all"].append(elem)

        identifier = elem.get("identifier")
        external_id = elem.get("id")

        if identifier:
            index["by_identifier"].setdefault(identifier, []).append(elem)

        if external_id:
            index["by_external_id"].setdefault(external_id, []).append(elem)

    return index


# ==========================================================
# STAGE 3 – SELECTOR MATCHING
# ==========================================================

def strip_ns(tag):
    """
    Entfernt den XML-Namespace aus einem lxml-Tag.
    Aus '{http://...}serviceTask' wird 'serviceTask'.
    """
    if tag and tag.startswith("{") and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def match_selector(selector, element):
    """
    Selector-Format: <source>-<entry-point>+filter+filter

    WICHTIG: lxml-Tags haben das Format {namespace-uri}localname.
    Wir arbeiten hier immer mit dem lokalen Namen (strip_ns) und dem
    sourceSystem-Attribut fuer source-Checks, damit Namespace-URIs
    den Matching-Prozess nicht stoeren.
    """
    if "-" not in selector:
        return False

    source, rest = selector.split("-", 1)

    local_tag = strip_ns(element.tag)
    source_system = element.get("sourceSystem", "")

    # Source-Check: archi
    if source == "archi":
        # ArchiMate-Elemente: entweder ueber sourceSystem-Annotation (gesetzt von XML04)
        # oder ueber typische lokale Tagnamen aus dem OEF-Export
        is_archi = (
            source_system == "archi"
            or local_tag in ("element", "relationship", "item", "view",
                             "node", "connection", "folder", "propertyDefinition")
        )
        if not is_archi:
            return False

    # Source-Check: bpmn
    if source == "bpmn":
        # BPMN-Elemente: entweder ueber sourceSystem-Annotation (gesetzt von XML04)
        # oder lokalen Tag-Namen der typisch BPMN-spezifisch ist
        # NICHT mehr via 'bpmn' in element.tag, da Namespace-URI diese Prueung bricht!
        is_bpmn = (
            source_system == "bpmn"
            or local_tag in ("serviceTask", "process", "startEvent", "endEvent",
                             "sequenceFlow", "userTask", "subProcess", "callActivity",
                             "exclusiveGateway", "parallelGateway", "inclusiveGateway",
                             "intermediateCatchEvent", "intermediateThrowEvent",
                             "boundaryEvent", "documentation", "definitions",
                             "extensionElements")
        )
        if not is_bpmn:
            return False

    # entry-point + Filter trennen
    if "+" in rest:
        entry_point, filters_str = rest.split("+", 1)
        filters = filters_str.split("+")
    else:
        entry_point = rest
        filters = []

    entry_point = entry_point.strip()

    # entry-point matching: bpmn:serviceTask -> lokaler Name ist 'serviceTask'
    # entry_point kann 'bpmn:serviceTask' oder 'element' oder '*' sein
    if entry_point != "*":
        # Normalisieren: 'bpmn:serviceTask' -> 'serviceTask' fuer lokalen Vergleich
        ep_local = entry_point.split(":")[-1] if ":" in entry_point else entry_point
        if local_tag != ep_local:
            return False

    # Filter-Tokens auswerten
    for flt in filters:
        flt = flt.strip()

        if flt == "has:id" and not element.get("id"):
            return False
        if flt == "has:identifier" and not element.get("identifier"):
            return False
        if flt == "no:identifier" and element.get("identifier"):
            return False
        if flt.startswith("same:"):
            continue  # wird waehrend des Merge-Vorgangs geprueft

    return True


# ==========================================================
# STAGE 4 – CONSOLIDATION ACTIONS
# ==========================================================

def merge_objects(canonical, duplicate, log):
    parent = duplicate.getparent()
    if parent is not None:
        parent.remove(duplicate)
        log.append(
            f"MERGE: removed duplicate id={duplicate.get('id')} "
            f"into identifier={canonical.get('identifier')}"
        )

def keep_object(obj, log):
    log.append(f"KEEP: id={obj.get('id')}")

def ignore_object(obj, log):
    log.append(f"IGNORE: id={obj.get('id')}")


# ==========================================================
# STAGE 5 – APPLY RULES
# ==========================================================

def apply_rules(tree, rules, index, log):
    for rule in rules:
        selector = rule["selector"]
        action = rule["action"]

        for elem in list(index["all"]):
            if not match_selector(selector, elem):
                continue

            identifier = elem.get("identifier")
            external_id = elem.get("id")

            if action == "merge" and external_id and not identifier:
                candidates = index["by_external_id"].get(external_id, [])
                canonicals = [e for e in candidates if e.get("identifier")]

                if len(canonicals) == 1:
                    canonical = canonicals[0]

                    if "same:type" in selector:
                        if canonical.get(
                            "{http://www.w3.org/2001/XMLSchema-instance}type"
                        ) != elem.get(
                            "{http://www.w3.org/2001/XMLSchema-instance}type"
                        ):
                            log.append(
                                f"SKIP: type mismatch id={external_id}"
                            )
                            continue

                    if "same:sourceSystem" in selector:
                        if canonical.get("sourceSystem") != elem.get("sourceSystem"):
                            log.append(
                                f"SKIP: sourceSystem mismatch id={external_id}"
                            )
                            continue

                    merge_objects(canonical, elem, log)

                else:
                    log.append(
                        f"AMBIGUOUS: id={external_id} candidates={len(canonicals)}"
                    )

            elif action == "keep":
                keep_object(elem, log)

            elif action == "ignore":
                ignore_object(elem, log)


# ==========================================================
# STAGE 6 – WRITE OUTPUT
# ==========================================================

def write_output(tree, path):
    tree.write(
        path,
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8"
    )

def write_log(entries, path):
    with open(path, "w", encoding="utf-8") as f:
        for line in entries:
            f.write(line + "\n")


# ==========================================================
# STAGE 7 – MAIN FLOW
# ==========================================================

def main():
    ROOT = resolve_root()

    XML_DIR = os.path.join(ROOT, "01-artifacts", "00-xml")
    MASTER_IN = os.path.join(XML_DIR, "00-master", "master.generated.xml")
    MASTER_OUT = os.path.join(XML_DIR, "00-master", "master.cleared.xml")
    SYNC_FILE = os.path.join(XML_DIR, "02-sync", "sync.txt")
    LOG_DIR = os.path.join(ROOT, "02-stages", "99-logs")
    LOG_FILE = os.path.join(LOG_DIR, "XML05-clear_merge.log")

    log = []
    log.append("==================================================")
    log.append(f"XML05 STARTED: {datetime.utcnow().isoformat()}")

    tree = load_master(MASTER_IN)
    rules = load_sync_rules(SYNC_FILE)
    index = build_index(tree)

    apply_rules(tree, rules, index, log)

    write_output(tree, MASTER_OUT)

    log.append(f"OUTPUT WRITTEN: {MASTER_OUT}")
    log.append(f"XML05 COMPLETED: {datetime.utcnow().isoformat()}")
    log.append("==================================================")

    write_log(log, LOG_FILE)


if __name__ == "__main__":
    main()
