#!/usr/bin/env python3
# ATL01-masterXml2AtlCsv.py
#
# Zweck (Flow-Stage):
# - master.xml lesen und in 9 ArchiMate Layer-CSVs transformieren
# - Scope-Filter: nur Elemente deren sourceModel in SOURCE=ATL aus run-scope.txt steht
# - Output (temporär, wird nach Flow nicht mehr benötigt):
#     <rootfolder>/03-stages/00-archimatearchive/atl_*.csv
# - Log:
#     <rootfolder>/03-stages/99-logs/ATL01-masterXml2AtlCsv.log
#
# Layer-Mapping (1:1 ArchiMate 3.2 Layer):
#   atl_strategy.csv          StrategyCapability, StrategyResource,
#                             CourseOfAction, ValueStream
#   atl_business.csv          BusinessActor, BusinessRole, BusinessCollaboration,
#                             BusinessInterface, BusinessProcess, BusinessFunction,
#                             BusinessInteraction, BusinessEvent, BusinessService,
#                             BusinessObject, Contract, Representation,
#                             Product
#   atl_application.csv       ApplicationComponent, ApplicationCollaboration,
#                             ApplicationInterface, ApplicationFunction,
#                             ApplicationInteraction, ApplicationProcess,
#                             ApplicationEvent, ApplicationService,
#                             DataObject
#   atl_technology.csv        Node, Device, SystemSoftware, TechnologyCollaboration,
#                             TechnologyInterface, Path, CommunicationNetwork,
#                             TechnologyFunction, TechnologyInteraction,
#                             TechnologyProcess, TechnologyEvent, TechnologyService,
#                             Artifact
#   atl_physical.csv          Equipment, Facility, DistributionNetwork,
#                             Material
#   atl_motivation.csv        Stakeholder, Driver, Assessment, Goal,
#                             Outcome, Principle, Requirement, Constraint,
#                             Meaning, Value, Capability
#   atl_implementation.csv    WorkPackage, Deliverable, ImplementationEvent,
#                             Plateau, Gap
#   atl_other.csv             Grouping, Location, Junction
#                             (+ alle unbekannten Typen)
#   atl_relations.csv         AssociationRelationship, CompositionRelationship,
#                             AggregationRelationship, AssignmentRelationship,
#                             RealizationRelationship, ServingRelationship,
#                             AccessRelationship, InfluenceRelationship,
#                             TriggeringRelationship, FlowRelationship,
#                             SpecializationRelationship
#
# Hinweis Views:
#   Views (DiagramModel, SketchModel, ArchimateDiagramModel) werden
#   in master.xml nicht als <element> gespeichert — kein atl_views.csv.
#   Die Jira-Komponente "Views" ist für manuelle Einträge reserviert.
#
# Spalten pro CSV:
#   objectKey       Archi identifier (eindeutiger Schlüssel)
#   ArchiType       ArchiMate Typ (xsi:type)
#   Layer           ArchiMate Layer-Name (= Jira Komponente)
#   Name            Anzeigename
#   Description     Dokumentation / Beschreibung
#   Specialization  Spezialisierung (falls vorhanden)
#   SourceModel     Herkunfts-Modell aus master.xml
#   [Properties]    Dynamisch — eine Spalte pro Property-Key
#
# Regeln:
# - Liest ATL00-root.resolved.txt als Root-Referenz
# - Scope-Filter über SOURCE=ATL in run-scope.txt (Hard Filter)
# - ID-Kollision: merge (erste Instanz gewinnt, SourceModel wird zusammengeführt)
# - Kein mkdir — Ordner müssen existieren (ATL00 hat das geprüft)
# - Hard fail bei jedem Fehler

import sys
import csv
import io
import os
from collections import defaultdict
from datetime import datetime
from xml.etree import ElementTree as ET


# ===========================================================
# KONSTANTEN
# ===========================================================

SCRIPT_KUERZEL = "ATL01"
LOG_FILENAME   = "ATL01-masterXml2AtlCsv.log"
ROOT_RESOLVED  = "ATL00-root.resolved.txt"
SOURCE_TYPE    = "ATL"

MASTER_XML_REL = os.path.join("02-artifacts", "00-xml", "00-master", "master.xml")
OUT_DIR_REL    = os.path.join("03-stages", "00-archimatearchive")
RUN_SCOPE_REL  = os.path.join("03-stages", "run-scope.txt")
LOGS_DIR_REL   = os.path.join("03-stages", "99-logs")

NS_A   = "http://www.opengroup.org/xsd/archimate/3.0/"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"

# ----------------------------------------------------------
# Layer-Mapping: Dateiname-Stamm -> (Layer-Name, [ArchiMate Typen])
# Layer-Name = exakter Jira-Komponentenname
# ----------------------------------------------------------
LAYER_GROUPS: dict[str, tuple[str, list[str]]] = {
    "atl_strategy": (
        "Strategy",
        [
            "Capability", "ValueStream", "CourseOfAction", "Resource",
        ],
    ),
    "atl_business": (
        "Business",
        [
            "BusinessActor", "BusinessRole", "BusinessCollaboration",
            "BusinessInterface", "BusinessProcess", "BusinessFunction",
            "BusinessInteraction", "BusinessEvent", "BusinessService",
            "BusinessObject", "Contract", "Representation", "Product",
        ],
    ),
    "atl_application": (
        "Application",
        [
            "ApplicationComponent", "ApplicationCollaboration",
            "ApplicationInterface", "ApplicationFunction",
            "ApplicationInteraction", "ApplicationProcess",
            "ApplicationEvent", "ApplicationService",
            "DataObject",
        ],
    ),
    "atl_technology": (
        "Technology & Physical",
        [
            "Node", "Device", "SystemSoftware", "TechnologyCollaboration",
            "TechnologyInterface", "Path", "CommunicationNetwork",
            "TechnologyFunction", "TechnologyInteraction",
            "TechnologyProcess", "TechnologyEvent", "TechnologyService",
            "Artifact", "Equipment", "Facility", "DistributionNetwork",
            "Material",
        ],
    ),
    "atl_motivation": (
        "Motivation",
        [
            "Stakeholder", "Driver", "Assessment", "Goal",
            "Outcome", "Principle", "Requirement", "Constraint",
            "Meaning", "Value",
        ],
    ),
    "atl_implementation": (
        "Implementation & Migration",
        [
            "WorkPackage", "Deliverable", "ImplementationEvent",
            "Plateau", "Gap",
        ],
    ),
    "atl_relations": (
        "Relations",
        [
            "AssociationRelationship", "CompositionRelationship",
            "AggregationRelationship", "AssignmentRelationship",
            "RealizationRelationship", "ServingRelationship",
            "AccessRelationship", "InfluenceRelationship",
            "TriggeringRelationship", "FlowRelationship",
            "SpecializationRelationship",
        ],
    ),
    "atl_other": (
        "Other",
        [
            "Grouping", "Location", "Junction",
        ],
    ),
}

# Reverse-Lookup: ArchiMate Typ -> (Gruppen-Stamm, Layer-Name)
TYPE_TO_LAYER: dict[str, tuple[str, str]] = {
    t: (g, info[0])
    for g, info in LAYER_GROUPS.items()
    for t in info[1]
}

BASIS_SPALTEN = [
    "objectKey", "ArchiType", "Layer", "Name", "Description",
    "Specialization", "SourceModel",
]


# ===========================================================
# HILFSFUNKTIONEN
# ===========================================================

def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str, log_path: str) -> None:
    line = f"[{SCRIPT_KUERZEL}] {now_ts()} | {message}"
    print(line)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def die(message: str, log_path: str | None = None) -> None:
    line = f"[{SCRIPT_KUERZEL}] {now_ts()} | ERROR | {message}"
    print(line, file=sys.stderr)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    sys.exit(1)


def local_tag(tag: str) -> str:
    """Namespace entfernen: '{http://...}localname' -> 'localname'."""
    return tag.split("}", 1)[1] if tag.startswith("{") else tag


# ===========================================================
# ROOT AUFLÖSEN
# ===========================================================

def resolve_root(script_dir: str) -> str:
    logs_candidate = os.path.abspath(
        os.path.join(script_dir, "..", "..", "03-stages", "99-logs")
    )
    resolved_file = os.path.join(logs_candidate, ROOT_RESOLVED)

    if not os.path.isfile(resolved_file):
        die(
            f"ATL00-root.resolved.txt nicht gefunden: {resolved_file}\n"
            f"  → Bitte zuerst ATL00 ausführen.",
            None,
        )

    with open(resolved_file, "r", encoding="utf-8") as f:
        root_path = f.readline().strip()

    if not root_path or not os.path.isdir(root_path):
        die(
            f"Ungültiger Root-Pfad in ATL00-root.resolved.txt: '{root_path}'",
            None,
        )

    return root_path


# ===========================================================
# RUN-SCOPE LESEN
# ===========================================================

def read_atl_scope(run_scope_path: str, log_path: str) -> list[str]:
    if not os.path.isfile(run_scope_path):
        die(f"run-scope.txt nicht gefunden: {run_scope_path}", log_path)

    aktive_zeilen = []
    with open(run_scope_path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.upper().startswith("SNAPSHOT_"):
                continue
            aktive_zeilen.append(s)

    modelle = []
    i = 0
    while i < len(aktive_zeilen):
        if aktive_zeilen[i].upper().startswith("SOURCE="):
            source = aktive_zeilen[i].split("=", 1)[1].strip().upper()
            if (
                i + 1 < len(aktive_zeilen)
                and aktive_zeilen[i + 1].upper().startswith("MODEL=")
            ):
                model = aktive_zeilen[i + 1].split("=", 1)[1].strip()
                if source == SOURCE_TYPE:
                    modelle.append(model)
                    log(f"ATL Scope aktiv: MODEL={model}", log_path)
                i += 2
                continue
        i += 1

    if not modelle:
        die(
            "Kein aktives SOURCE=ATL / MODEL= Pair in run-scope.txt.\n"
            "  → Bitte ATL00 prüfen und run-scope.txt kontrollieren.",
            log_path,
        )

    return modelle


# ===========================================================
# MASTER.XML PARSEN
# ===========================================================

def parse_master_xml(
    master_xml_path: str,
    atl_scope: list[str],
    log_path: str,
) -> tuple[list[dict], dict[str, set]]:
    log(f"Parse master.xml: {master_xml_path}", log_path)

    try:
        tree = ET.parse(master_xml_path)
    except ET.ParseError as e:
        die(f"master.xml nicht parsebar: {e}", log_path)

    root = tree.getroot()
    a    = f"{{{NS_A}}}"
    xsi  = f"{{{NS_XSI}}}"

    # Property-Definitionen aus master.xml lesen
    prop_defs: dict[str, str] = {}
    for child in root:
        lt = local_tag(child.tag)
        if lt == "propertyDefinitions":
            for pd in child:
                pid      = pd.get("identifier", "")
                pname_el = pd.find(f"{a}name")
                pname    = (
                    pname_el.text.strip()
                    if (pname_el is not None and pname_el.text)
                    else pid
                )
                prop_defs[pid] = pname

    log(f"Property-Definitionen gefunden: {len(prop_defs)}", log_path)

    elements:      list[dict]        = []
    prop_keys:     dict[str, set]    = defaultdict(set)
    id_index:      dict[str, int]    = {}   # objectKey -> Index in elements
    bpmn_name_map: dict[str, str]    = {}   # BPMN-Prozessname -> objectKey

    stats = {
        "elemente":       0,
        "uebersprungen":  0,
        "id_kollisionen": 0,
        "bpmn_match":     0,
        "bpmn_neu":       0,
    }

    for child in root:
        lt        = local_tag(child.tag)
        src_model = child.get("sourceModel", "")

        # Scope-Filter: nur ATL-Modelle verarbeiten
        if src_model not in atl_scope:
            stats["uebersprungen"] += 1
            continue

        # --------------------------------------------------
        # ArchiMate Element
        # --------------------------------------------------
        if lt == "element":
            eid   = child.get("identifier", "").strip()
            etype = child.get(f"{xsi}type", "").strip()

            if not eid or not etype:
                continue

            # Anzeigename
            name_el = child.find(f"{a}name")
            name    = (
                name_el.text.strip()
                if (name_el is not None and name_el.text)
                else ""
            )

            # Beschreibung
            doc_el = child.find(f"{a}documentation")
            doc    = (
                doc_el.text.strip()
                if (doc_el is not None and doc_el.text)
                else ""
            )

            # Spezialisierung
            spec = child.get("specialization", "")

            # Properties
            elem_props: dict[str, str] = {}
            for prop in child.findall(f".//{a}property"):
                ref    = prop.get("propertyDefinitionRef", "")
                pkey   = prop_defs.get(ref, ref)
                val_el = prop.find(f"{a}value")
                val    = (
                    val_el.text.strip()
                    if (val_el is not None and val_el.text)
                    else ""
                )
                elem_props[pkey] = val

            # Layer und Gruppen-Stamm bestimmen
            layer_info = TYPE_TO_LAYER.get(etype)
            if layer_info:
                gruppe, layer_name = layer_info
            else:
                gruppe     = "atl_other"
                layer_name = "Other"

            obj_key = eid

            # ID-Kollision prüfen (merge: erste Instanz gewinnt)
            if obj_key in id_index:
                idx        = id_index[obj_key]
                vorh_model = elements[idx].get("SourceModel", "")
                if src_model not in vorh_model:
                    elements[idx]["SourceModel"] = f"{vorh_model},{src_model}"
                stats["id_kollisionen"] += 1
                log(f"  ID-Kollision (merge): {obj_key} | {src_model}", log_path)
                continue

            zeile = {
                "objectKey":      obj_key,
                "ArchiType":      etype,
                "Layer":          layer_name,
                "Name":           name,
                "Description":    doc,
                "Specialization": spec,
                "SourceModel":    src_model,
            }
            zeile.update(elem_props)

            # Property-Spalten für Gruppe registrieren
            for pk in elem_props:
                prop_keys[gruppe].add(pk)

            # BPMN-Name-Map für späteren Match aufbauen
            if name:
                bpmn_name_map[name] = obj_key

            id_index[obj_key] = len(elements)
            elements.append(zeile)
            stats["elemente"] += 1

        # --------------------------------------------------
        # BPMN definitions
        # --------------------------------------------------
        elif lt == "definitions":
            for el in child.iter():
                if local_tag(el.tag).lower() != "process":
                    continue
                bpmn_id   = (el.get("id")   or "").strip()
                bpmn_name = (el.get("name") or "").strip()

                if not bpmn_id:
                    continue

                matched_key = bpmn_name_map.get(bpmn_name)

                if matched_key is not None:
                    # Bestehendes Element mit BPMN_ID anreichern
                    idx = id_index.get(matched_key)
                    if idx is not None:
                        elements[idx]["BPMN_ID"] = bpmn_id
                        grp = TYPE_TO_LAYER.get(
                            elements[idx].get("ArchiType", ""),
                            ("atl_other", "Other"),
                        )[0]
                        prop_keys[grp].add("BPMN_ID")
                    stats["bpmn_match"] += 1
                    log(f"  BPMN Match: {bpmn_name!r} -> BPMN_ID={bpmn_id}", log_path)
                else:
                    # Neues Stub-Element für ungematchten BPMN-Prozess
                    zeile = {
                        "objectKey":      bpmn_id,
                        "ArchiType":      "BusinessProcess",
                        "Layer":          "Business",
                        "Name":           bpmn_name,
                        "Description":    "",
                        "Specialization": "",
                        "SourceModel":    src_model or "bpmn",
                        "BPMN_ID":        bpmn_id,
                    }
                    elements.append(zeile)
                    bpmn_name_map[bpmn_name] = bpmn_id
                    prop_keys["atl_business"].add("BPMN_ID")
                    stats["bpmn_neu"] += 1
                    log(f"  BPMN Neu (Stub): {bpmn_name!r} -> {bpmn_id}", log_path)

    log(
        f"Parse abgeschlossen | "
        f"Elemente={stats['elemente']} "
        f"Uebersprungen={stats['uebersprungen']} "
        f"ID-Kollisionen={stats['id_kollisionen']} "
        f"BPMN-Match={stats['bpmn_match']} "
        f"BPMN-Neu={stats['bpmn_neu']}",
        log_path,
    )

    return elements, prop_keys


# ===========================================================
# CSV SCHREIBEN
# ===========================================================

def schreibe_csv(
    pfad: str,
    spalten: list[str],
    zeilen: list[dict],
    log_path: str,
) -> None:
    if not os.path.isdir(os.path.dirname(pfad)):
        die(f"Ausgabe-Ordner fehlt: {os.path.dirname(pfad)}", log_path)

    buf = io.StringIO()
    writer = csv.DictWriter(
        buf,
        fieldnames=spalten,
        quoting=csv.QUOTE_ALL,
        extrasaction="ignore",
        restval="",
        lineterminator="\r\n",
    )
    writer.writeheader()
    writer.writerows(zeilen)

    with open(pfad, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())

    log(f"  Geschrieben: {len(zeilen):>5} Zeilen -> {os.path.basename(pfad)}", log_path)


# ===========================================================
# MAIN
# ===========================================================

def main() -> None:
    sdir      = os.path.dirname(os.path.abspath(__file__))
    root_path = resolve_root(sdir)

    logs_dir = os.path.join(root_path, LOGS_DIR_REL)
    log_path = os.path.join(logs_dir, LOG_FILENAME)

    log("=" * 60, log_path)
    log(f"ATL01 START | {now_ts()}", log_path)
    log(f"BLUEPRINT_ROOT: {root_path}", log_path)

    # run-scope.txt lesen
    run_scope_path = os.path.join(root_path, RUN_SCOPE_REL)
    atl_scope      = read_atl_scope(run_scope_path, log_path)
    log(f"ATL Scope: {atl_scope}", log_path)

    # master.xml prüfen
    master_xml_path = os.path.join(root_path, MASTER_XML_REL)
    if not os.path.isfile(master_xml_path):
        die(f"master.xml nicht gefunden: {master_xml_path}", log_path)

    # Output-Ordner prüfen
    out_dir = os.path.join(root_path, OUT_DIR_REL)
    if not os.path.isdir(out_dir):
        die(
            f"Ausgabe-Ordner fehlt: {out_dir}\n"
            f"  → Bitte ATL00 ausführen (prüft Ordner-Existenz).",
            log_path,
        )

    # master.xml parsen
    log("-" * 60, log_path)
    elemente, prop_keys = parse_master_xml(master_xml_path, atl_scope, log_path)

    # Elemente nach Layer aufteilen
    gruppiert:      dict[str, list[dict]] = defaultdict(list)
    unklassifiziert: set[str]             = set()

    for zeile in elemente:
        atype      = zeile.get("ArchiType", "")
        layer_info = TYPE_TO_LAYER.get(atype)
        if layer_info:
            gruppe = layer_info[0]
        else:
            unklassifiziert.add(atype)
            gruppe = "atl_other"
        gruppiert[gruppe].append(zeile)

    if unklassifiziert:
        log(
            f"WARNUNG: Unbekannte ArchiTypes -> atl_other.csv: "
            f"{sorted(unklassifiziert)}",
            log_path,
        )

    # CSVs schreiben
    log("-" * 60, log_path)
    log("Schreibe Output-Dateien...", log_path)

    geschrieben: list[str] = []

    for gruppen_stamm, gruppen_zeilen in gruppiert.items():
        if not gruppen_zeilen:
            continue
        extra   = sorted(prop_keys.get(gruppen_stamm, set()))
        spalten = BASIS_SPALTEN + extra
        ziel    = os.path.join(out_dir, f"{gruppen_stamm}.csv")
        schreibe_csv(ziel, spalten, gruppen_zeilen, log_path)
        geschrieben.append(os.path.basename(ziel))

    # Zusammenfassung
    log("-" * 60, log_path)
    log(f"Ausgabe-Ordner: {out_dir}", log_path)
    log(f"Dateien geschrieben ({len(geschrieben)}):", log_path)
    for fn in sorted(geschrieben):
        log(f"  {fn}", log_path)
    log("=" * 60, log_path)
    log("ATL01 ERFOLGREICH", log_path)

    print(
        f"[ATL01] OK | {len(geschrieben)} Datei(en) -> "
        f"03-stages/00-archimatearchive/"
    )


if __name__ == "__main__":
    main()
