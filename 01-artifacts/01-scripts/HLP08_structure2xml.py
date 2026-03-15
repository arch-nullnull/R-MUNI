#!/usr/bin/env python3
# HLP08_structure2xml.py
#
# Zweck:
# - structure.txt parsen und ein Archi OEF-konformes XML erzeugen
# - Output direkt in den XML-Flow einspielbar (SOURCE=OEF)
# - Alle Ordner und Dateien werden als Artifact modelliert (Archi CSV-Import-Format)
# - Eltern-Kind Beziehungen werden als Composition modelliert
# - Organizations-Block spiegelt die Baumstruktur wider
#
# Ablageort    : <rootfolder>\01-artifacts\01-scripts\HLP08_structure2xml.py
# Input        : <rootfolder>\structure.txt
# Output       : <rootfolder>\01-artifacts\00-xml\03-child\00-archimatechild\muni2import.xml
#
# Basis: Stage 5.5 | HLP00-Import-Muster | ArchiMate OEF 3.1

import re
import uuid
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.dom import minidom

# Root-Auflösung über HLP00 — Standard-Muster Stage 5
from HLP00_resolve_root import get_root_cfg

cfg       = get_root_cfg()
ROOT      = Path(cfg["<rootfolder>"])
ARTIFACTS = Path(cfg["<artifacts>"])

INPUT_FILE = ROOT / "structure.txt"
OUTPUT_XML = ARTIFACTS / "00-xml" / "03-child" / "00-archimatechild" / "muni2import.xml"

# OEF Namespace
NS = "http://www.opengroup.org/xsd/archimate/3.0/"
DC = "http://purl.org/dc/elements/1.1/"
XSI = "http://www.w3.org/2001/XMLSchema-instance"


# ----------------------------------------------------------
# Hilfsfunktionen
# ----------------------------------------------------------

def new_id() -> str:
    """Erzeugt eine Archi-konforme ID (id-<uuid ohne Bindestriche>)."""
    return "id-" + uuid.uuid4().hex


def parse_tree(lines: list[str]) -> list[tuple[int, str, bool]]:
    """
    Parst die tree-Ausgabe von structure.txt.
    Gibt Liste von (tiefe, name, ist_ordner) zurück.
    """
    entries = []
    for raw in lines:
        line = raw.rstrip("\r\n")
        if not line.strip():
            continue
        m = re.match(r'^([|+\\ \-]*)([^\|+\\\-\s].*)$', line)
        if not m:
            continue
        prefix = m.group(1)
        name = m.group(2).strip()
        if not name:
            continue
        depth = len(prefix) // 4
        # Ordner haben keine Dateiendung (max 10 Zeichen)
        is_folder = not bool(re.search(r'\.\w{1,10}$', name))
        entries.append((depth, name, is_folder))
    return entries


def build_records(entries: list[tuple]) -> list[dict]:
    """
    Baut aus der flachen Entry-Liste strukturierte Records mit
    full_path und parent_path auf.
    """
    stack = {}
    records = []
    for depth, name, is_folder in entries:
        stack = {d: n for d, n in stack.items() if d < depth}
        stack[depth] = name
        full_path = "/".join(stack[d] for d in sorted(stack))
        parent_keys = sorted(k for k in stack if k < depth)
        parent_path = "/".join(stack[k] for k in parent_keys) if parent_keys else None
        records.append({
            "id":          new_id(),
            "name":        name,
            "full_path":   full_path,
            "parent_path": parent_path,
            "is_folder":   is_folder,
            "depth":       depth,
        })
    return records


# ----------------------------------------------------------
# XML Aufbau
# ----------------------------------------------------------

def build_organization_items(records: list[dict], path_to_id: dict, parent_path=None) -> list[ET.Element]:
    """
    Erzeugt rekursiv <item identifierRef="..."> Elemente
    für den organizations-Block.
    """
    items = []
    children = [r for r in records if r["parent_path"] == parent_path]
    for r in children:
        item = ET.Element("item")
        item.set("identifierRef", r["id"])
        # Rekursiv Kinder anhängen
        sub_items = build_organization_items(records, path_to_id, r["full_path"])
        for si in sub_items:
            item.append(si)
        items.append(item)
    return items


def build_xml(records: list[dict]) -> str:
    """
    Baut das vollständige OEF XML und gibt es als
    formattierten String zurück.
    """
    path_to_id = {r["full_path"]: r["id"] for r in records}

    # Namespaces registrieren (kein Präfix für Haupt-NS)
    ET.register_namespace("",    NS)
    ET.register_namespace("dc",  DC)
    ET.register_namespace("xsi", XSI)

    # Root: <model>
    model = ET.Element(f"{{{NS}}}model")
    model.set(f"{{{XSI}}}schemaLocation",
              f"{NS} http://www.opengroup.org/xsd/archimate/3.1/archimate3_Diagram.xsd "
              f"{DC} http://www.opengroup.org/xsd/archimate/3.1/dc.xsd")
    model.set("identifier", new_id())

    # <name>
    name_el = ET.SubElement(model, f"{{{NS}}}name")
    name_el.set("{http://www.w3.org/XML/1998/namespace}lang", "de")
    name_el.text = "MUNI IMPO"

    # <metadata>
    metadata = ET.SubElement(model, f"{{{NS}}}metadata")
    schema = ET.SubElement(metadata, "schema")
    schema.text = "Dublin Core"
    schemaversion = ET.SubElement(metadata, "schemaversion")
    schemaversion.text = "1.1"
    dc_title = ET.SubElement(metadata, f"{{{DC}}}title")
    dc_title.text = "R+MUNI OEF Export — structure2xml"
    dc_creator = ET.SubElement(metadata, f"{{{DC}}}creator")
    dc_creator.text = "HLP08"

    # <elements> — alle Einträge als Artifact (Archi CSV-Import-kompatibler Type)
    elements_el = ET.SubElement(model, f"{{{NS}}}elements")
    for r in records:
        elem = ET.SubElement(elements_el, f"{{{NS}}}element")
        elem.set("identifier", r["id"])
        elem.set(f"{{{XSI}}}type", "Artifact")
        elem_name = ET.SubElement(elem, f"{{{NS}}}name")
        elem_name.set("{http://www.w3.org/XML/1998/namespace}lang", "de")
        elem_name.text = r["name"]
        # Documentation: full_path + typ als Kontext
        doc = ET.SubElement(elem, f"{{{NS}}}documentation")
        doc.set("{http://www.w3.org/XML/1998/namespace}lang", "de")
        doc.text = f"{'Ordner' if r['is_folder'] else 'Datei'} | Pfad: {r['full_path']} | Tiefe: {r['depth']}"
        # Properties: item_type und full_path
        props = ET.SubElement(elem, f"{{{NS}}}properties")
        prop1 = ET.SubElement(props, f"{{{NS}}}property")
        prop1.set("propertyDefinitionRef", "propdef-item_type")
        val1 = ET.SubElement(prop1, f"{{{NS}}}value")
        val1.set("{http://www.w3.org/XML/1998/namespace}lang", "de")
        val1.text = "folder" if r["is_folder"] else "file"
        prop2 = ET.SubElement(props, f"{{{NS}}}property")
        prop2.set("propertyDefinitionRef", "propdef-full_path")
        val2 = ET.SubElement(prop2, f"{{{NS}}}value")
        val2.set("{http://www.w3.org/XML/1998/namespace}lang", "de")
        val2.text = r["full_path"]

    # <relationships> — Eltern-Kind als Composition
    relationships_el = ET.SubElement(model, f"{{{NS}}}relationships")
    rel_count = 0
    for r in records:
        if r["parent_path"] and r["parent_path"] in path_to_id:
            rel = ET.SubElement(relationships_el, f"{{{NS}}}relationship")
            rel.set("identifier", new_id())
            rel.set(f"{{{XSI}}}type", "Composition")
            rel.set("source", path_to_id[r["parent_path"]])
            rel.set("target", r["id"])
            rel_count += 1

    # <organizations> — Baumstruktur für Archi-Ansicht
    org = ET.SubElement(model, f"{{{NS}}}organizations")
    org_label_item = ET.SubElement(org, f"{{{NS}}}item")
    label_el = ET.SubElement(org_label_item, f"{{{NS}}}label")
    label_el.set("{http://www.w3.org/XML/1998/namespace}lang", "de")
    label_el.text = "R+MUNI Struktur"
    top_items = build_organization_items(records, path_to_id, parent_path=None)
    for ti in top_items:
        org_label_item.append(ti)

    # <propertyDefinitions> — Definitionen für Properties
    prop_defs = ET.SubElement(model, f"{{{NS}}}propertyDefinitions")
    for prop_id, prop_name in [
        ("propdef-item_type", "item_type"),
        ("propdef-full_path", "full_path"),
    ]:
        pd = ET.SubElement(prop_defs, f"{{{NS}}}propertyDefinition")
        pd.set("identifier", prop_id)
        pd.set("type", "string")
        pd_name = ET.SubElement(pd, f"{{{NS}}}name")
        pd_name.set("{http://www.w3.org/XML/1998/namespace}lang", "de")
        pd_name.text = prop_name

    # Schöne Formatierung via minidom
    raw_xml = ET.tostring(model, encoding="unicode", xml_declaration=False)
    dom = minidom.parseString(raw_xml)
    pretty = dom.toprettyxml(indent="  ", encoding="UTF-8")
    # minidom fügt eigene XML-Deklaration ein — sauber ersetzen
    lines = pretty.decode("utf-8").splitlines()
    lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
    return "\n".join(lines)


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main():
    # Input prüfen
    if not INPUT_FILE.exists():
        print(f"❌ structure.txt nicht gefunden: {INPUT_FILE}")
        raise SystemExit(1)

    with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    # Startzeile nach "C:." suchen (tree-Header überspringen)
    start = next((i + 1 for i, l in enumerate(lines) if l.strip().startswith("C:.")), 3)

    entries = parse_tree(lines[start:])
    records = build_records(entries)
    xml_content = build_xml(records)

    # Output schreiben
    OUTPUT_XML.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_XML, "w", encoding="utf-8") as f:
        f.write(xml_content)

    # Statistik
    n_elem = len(records)
    n_rel  = sum(1 for r in records if r["parent_path"])
    n_fold = sum(1 for r in records if r["is_folder"])
    n_file = sum(1 for r in records if not r["is_folder"])

    print(f"✅ {n_elem} Elemente ({n_fold} Ordner, {n_file} Dateien), {n_rel} Relationen")
    print(f"   → {OUTPUT_XML}")

    from collections import Counter
    depth_dist = Counter(r["depth"] for r in records)
    for d in sorted(depth_dist):
        fc = sum(1 for r in records if r["depth"] == d and r["is_folder"])
        fi = sum(1 for r in records if r["depth"] == d and not r["is_folder"])
        print(f"   Tiefe {d}: {depth_dist[d]} ({fc} Ordner, {fi} Dateien)")


if __name__ == "__main__":
    main()
