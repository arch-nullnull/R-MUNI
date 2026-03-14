#!/usr/bin/env python3
# XML04-merge_master.py
#
# Purpose:
# - Apply declarative mapping rules to XML03 index
# - Select matching objects
# - Load original XML models only when needed
# - Merge COMPLETE XML subtrees into master.xml
#
# IMPORTANT:
# - Mapping acts ONLY as filter
# - IDs are NEVER modified
# - Source system is annotated for later analysis
# - Append-only, no deduplication, no merge logic
#
# Inputs:
#   <root>/02-stages/00-archimatearchive/XML03-index.xml
#   <root>/02-stages/01-bpmnarchive/XML03-index.xml
#   <root>/01-artifacts/00-xml/01-mapping/mapping.txt
#
# Output:
#   <root>/01-artifacts/00-xml/00-master/master.generated.xml
#
# Logs:
#   <root>/02-stages/99-logs/XML04-merge.log

import os
import fnmatch
import xml.etree.ElementTree as ET
from datetime import datetime


def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg, path):
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[XML04] {ts()} | {msg}\n")


def read_root_resolved(path):
    with open(path, "r", encoding="utf-8") as f:
        root = f.readline().strip()
    if not root or not os.path.isdir(root):
        raise RuntimeError("Invalid root path")
    return root


def read_mapping(path):
    rules = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            rules.append(line)
    return rules


def parse_rule(rule):
    """
    Syntax: <source>[<model-filter>]-<entry-point>+<filter>+<filter>

    Trennzeichen:
      -  nach source/model-filter -> entry-point beginnt
      +  nach entry-point         -> Attributfilter (AND-kombiniert)

    WICHTIG: entry-point darf intern : enthalten (z.B. bpmn:serviceTask),
    aber kein weiteres - als Trenner. Attributfilter werden ausschliesslich
    mit + angehaengt.
    """
    # 1) Source + optionalen Model-Filter extrahieren
    source = rule
    rest = ""

    # Trenne source[model] vom Rest beim ersten - das NACH dem optionalen [...]  kommt
    # Schrittweise: zuerst [model-filter] raus, dann beim naechsten - splitten
    model_filter = "*"

    if "[" in rule and "]" in rule:
        bracket_start = rule.index("[")
        bracket_end = rule.index("]")
        model_filter = rule[bracket_start + 1:bracket_end]
        # Alles vor [ ist source, alles nach ] (ab dem naechsten -) ist der rest
        source = rule[:bracket_start]
        after_bracket = rule[bracket_end + 1:]  # beginnt mit -
        if after_bracket.startswith("-"):
            rest = after_bracket[1:]  # Fuehrendes - entfernen
        else:
            rest = after_bracket
    else:
        # Kein model-filter: erstes - trennt source von entry-point
        if "-" not in rule:
            return {"source": rule, "model_filter": "*", "entry": "", "filters": []}
        source, rest = rule.split("-", 1)

    source = source.strip()

    # 2) entry-point und Attributfilter trennen (Trenner: +)
    entry = rest
    filters = []

    if "+" in rest:
        entry, flt = rest.split("+", 1)
        filters = flt.split("+")

    # rstrip(*) nur wenn reiner Wildcard, nicht bei bpmn:serviceTask etc.
    entry = entry.strip()
    if entry == "*":
        entry = ""

    return {
        "source": source,
        "model_filter": model_filter,
        "entry": entry,
        "filters": filters
    }


def load_index(path):
    return ET.parse(path).getroot()


def match_entry(entry_elem, rule):
    """
    Prueft ob ein Index-Eintrag (aus XML03-index.xml) auf eine Mapping-Regel passt.

    entry_elem ist ein <entry>-Element mit Attributen: kind, id, tag, xsi_type, name
    rule["entry"] = "" bedeutet Wildcard (alles passt beim kind-Check)
    """
    kind = entry_elem.get("kind", "")

    # entry="" -> Wildcard, alles passt
    if rule["entry"] != "" and not kind.endswith(rule["entry"]):
        return False

    # Attributfilter auswerten
    for f in rule["filters"]:
        f = f.strip()

        # xsi:type="Value" Filter
        if f.startswith("xsi:type="):
            val = f.split("=", 1)[1].strip('"').strip("'")
            if entry_elem.get("xsi_type") != val:
                return False

        # Weitere bekannte Filter koennen hier ergaenzt werden
        # (content-Filter wie bpmn:documentation>..< werden in XML04 nicht
        #  auf Index-Ebene geprueft - das wuerde das Laden des Original-XML
        #  erfordern; diese Filter werden deshalb hier als "pass" behandelt
        #  und spaeter beim Subtree-Load verifiziert wenn noetig)

    return True


def collect_matches(index_root, rules):
    """
    Liefert alle matching Eintraege aus dem XML03-Index fuer die gegebenen Regeln.
    Dedupliziert nach (model_file, entry_id) um Mehrfach-Merges durch ueberlappende
    Regeln zu vermeiden (z.B. archi-* + archi-element-xsi:type=... wuerden sonst
    dieselben Elemente mehrfach einfuegen).
    """
    seen = set()
    matches = []

    for model in index_root.findall("model"):
        model_name = model.get("name", "")
        model_file = model.get("file", "")

        for rule in rules:
            if not fnmatch.fnmatch(model_name, rule["model_filter"]):
                continue

            for entry in model.findall("entry"):
                if not match_entry(entry, rule):
                    continue

                entry_id = entry.get("id")
                dedup_key = (model_file, entry_id)

                if dedup_key in seen:
                    continue

                seen.add(dedup_key)
                matches.append({
                    "model_file": model_file,
                    "model_name": model_name,
                    "entry_id": entry_id,
                    "entry_kind": entry.get("kind")
                })

    return matches


def load_xml(path):
    return ET.parse(path)


def find_subtree(root, entry_id):
    for e in root.iter():
        if e.attrib.get("identifier") == entry_id or e.attrib.get("id") == entry_id:
            return e
    return None


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root = read_root_resolved(
        os.path.join(script_dir, "..", "..", "02-stages", "99-logs", "XML00-root.resolved.txt")
    )

    log_path = os.path.join(root, "02-stages", "99-logs", "XML04-merge.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    mapping_path = os.path.join(
        root, "01-artifacts", "00-xml", "01-mapping", "mapping.txt"
    )

    raw_rules = read_mapping(mapping_path)
    rules = []
    for r in raw_rules:
        parsed = parse_rule(r)
        rules.append(parsed)
        log(f"rule loaded: source={parsed['source']} model={parsed['model_filter']} "
            f"entry=[{parsed['entry']}] filters={parsed['filters']}", log_path)

    master_root = ET.Element("master")

    for src, sub in [("archi", "00-archimatearchive"), ("bpmn", "01-bpmnarchive")]:
        index_path = os.path.join(root, "02-stages", sub, "XML03-index.xml")
        if not os.path.isfile(index_path):
            log(f"index not found, skipping: {index_path}", log_path)
            continue

        index = load_index(index_path)
        src_rules = [r for r in rules if r["source"] == src]
        matches = collect_matches(index, src_rules)

        log(f"{src}: {len(matches)} entries matched", log_path)

        for m in matches:
            xml_path = os.path.join(root, m["model_file"])
            tree = load_xml(xml_path)
            subtree = find_subtree(tree.getroot(), m["entry_id"])

            if subtree is None:
                log(f"subtree not found: {m['entry_id']} in {m['model_file']}", log_path)
                continue

            # Annotate source system + source model WITHOUT touching IDs
            subtree.set("sourceSystem", src)
            subtree.set("sourceModel", m["model_name"] or os.path.basename(m["model_file"]))

            master_root.append(subtree)
            log(
                f"merged {src} {m['entry_kind']} {m['entry_id']} | "
                f"sourceModel={m['model_name'] or os.path.basename(m['model_file'])}",
                log_path
            )

    out_path = os.path.join(
        root, "01-artifacts", "00-xml", "00-master", "master.generated.xml"
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Namespace-Präfixe registrieren damit ET sie beim Schreiben
    # korrekt erhält und nicht zu ns0:, ns1: etc. umbenennt.
    # Ohne diese Registrierung gehen xsi:type Werte wie
    # "Relationship:CompositionRelationship" verloren.
    ET.register_namespace("xsi",          "http://www.w3.org/2001/XMLSchema-instance")
    ET.register_namespace("",             "http://www.opengroup.org/xsd/archimate/3.0/")
    ET.register_namespace("bpmn",         "http://www.omg.org/spec/BPMN/20100524/MODEL")
    ET.register_namespace("dc",           "http://www.omg.org/spec/DD/20100524/DC")
    ET.register_namespace("di",           "http://www.omg.org/spec/DD/20100524/DI")
    ET.register_namespace("bpmndi",       "http://www.omg.org/spec/BPMN/20100524/DI")

    ET.ElementTree(master_root).write(out_path, encoding="utf-8", xml_declaration=True)

    print("[XML04] OK | master merge completed")


if __name__ == "__main__":
    main()
