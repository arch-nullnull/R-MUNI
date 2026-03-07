#!/usr/bin/env python3
# M2B01-master_extract.py
#
# Purpose:
# - Extract Archi BusinessProcess elements from master.xml
# - Apply M2Bmapping.txt as HARD FILTER
#   (element type + sourceModel)
# - Apply run-scope.txt SOURCE=BPMN as SCOPE FILTER (Ebene 1)
# - Create tool-ready BPMN 2.0 hulls
# - Only if no BPMN for the identity exists
#
# Mapping applies ONLY here.
# No Camunda metadata
# No content
# No StartEvents
# No overwrite
# No abort on existing BPMN
#
# BUGFIX (Stage 3 / 2026-03-06):
# run-scope.txt SOURCE=BPMN wird als vorgelagerter Scope Filter
# ausgewertet. Nur Prozesse deren sourceModel einem aktiven
# SOURCE=BPMN MODEL= Eintrag entspricht werden materialisiert.
# Rueckwaertskompatibel: kein SOURCE=BPMN in run-scope.txt
# -> kein zusaetzlicher Filter (Verhalten wie vor dem Fix).

from pathlib import Path
import xml.etree.ElementTree as ET


# ----------------------------------------------------------
# CONFIG (EXPLICIT)
# ----------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

STAGE_DIR = ROOT_DIR / "03-stages"
HULL_DIR = STAGE_DIR / "01-bpmnarchive"

MASTER_XML = ROOT_DIR / "02-artifacts" / "00-xml" / "00-master" / "master.xml"
MAPPING_FILE = ROOT_DIR / "02-artifacts" / "00-xml" / "01-mapping" / "M2Bmapping.txt"
RUN_SCOPE_FILE = ROOT_DIR / "02-artifacts" / "00-xml" / "01-mapping" / "run-scope.txt"

NS_BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL"
NS_BPMNDI = "http://www.omg.org/spec/BPMN/20100524/DI"
XSI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"

ET.register_namespace("bpmn", NS_BPMN)
ET.register_namespace("bpmndi", NS_BPMNDI)


# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------

def bpmn(tag):
    return f"{{{NS_BPMN}}}{tag}"

def bpmndi(tag):
    return f"{{{NS_BPMNDI}}}{tag}"


def load_mapping_rules():
    rules = []
    with MAPPING_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            rules.append(line)
    return rules


def load_bpmn_scope() -> list:
    """
    Liest run-scope.txt und gibt alle aktiven SOURCE=BPMN MODEL= Werte
    als Liste zurueck.

    Format in run-scope.txt (aktives Pair):
      SOURCE=BPMN
      MODEL=MUNI FLOW.xml

    Kommentierte Zeilen (#) werden ignoriert.
    SNAPSHOT Zeilen (SNAPSHOT_SOURCE / SNAPSHOT_MODEL) werden ignoriert.

    Rueckgabe:
      Liste der aktiven MODEL= Werte fuer SOURCE=BPMN
      Leere Liste wenn kein SOURCE=BPMN vorhanden oder Datei fehlt.
    """
    if not RUN_SCOPE_FILE.exists():
        print(f"[M2B01] WARNING: run-scope.txt not found, no scope filter applied")
        return []

    scope_models = []
    lines = []

    with RUN_SCOPE_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Kommentare und leere Zeilen ignorieren
            if not line or line.startswith("#"):
                continue
            # SNAPSHOT Zeilen ignorieren (beginnen mit SNAPSHOT_)
            if line.startswith("SNAPSHOT_"):
                continue
            lines.append(line)

    # Pairs lesen: SOURCE= gefolgt von MODEL=
    i = 0
    while i < len(lines):
        if lines[i].startswith("SOURCE="):
            source = lines[i].split("=", 1)[1].strip()
            if i + 1 < len(lines) and lines[i + 1].startswith("MODEL="):
                model = lines[i + 1].split("=", 1)[1].strip()
                if source.upper() == "BPMN":
                    scope_models.append(model)
                i += 2
                continue
        i += 1

    if scope_models:
        print(f"[M2B01] run-scope.txt SCOPE FILTER active: {scope_models}")
    else:
        print(f"[M2B01] run-scope.txt: no SOURCE=BPMN found, no scope filter applied")

    return scope_models


def matches_scope(proc: dict, bpmn_scope: list) -> bool:
    """
    Prueft ob ein Prozess im aktiven BPMN Scope liegt.
    Vergleich: proc["sourceModel"] gegen bpmn_scope Eintraege.

    Ist bpmn_scope leer -> kein Filter, alles passiert (rueckwaertskompatibel).
    """
    if not bpmn_scope:
        return True
    return proc.get("sourceModel", "") in bpmn_scope


def parse_mapping_rule(rule: str) -> dict:
    """
    Example rule:
    archi[model=*Process*]-element-xsi:type="BusinessProcess"
    """
    parsed = {
        "model": None,
        "xsi_type": None
    }

    if "archi[" in rule:
        ctx = rule.split("archi[", 1)[1].split("]", 1)[0]
        if ctx.startswith("model="):
            parsed["model"] = ctx.replace("model=", "").strip().strip('"')

    if 'element-xsi:type="' in rule:
        parsed["xsi_type"] = rule.split('element-xsi:type="', 1)[1].split('"', 1)[0]

    return parsed


def matches_mapping(proc: dict, rules: list) -> bool:
    """
    proc must contain:
    - id
    - name
    - xsi_type
    - sourceModel
    """
    for rule in rules:
        parsed = parse_mapping_rule(rule)

        if parsed["xsi_type"] and proc.get("xsi_type") != parsed["xsi_type"]:
            continue

        if parsed["model"]:
            pattern = parsed["model"].replace("*", "")
            if pattern and pattern not in proc.get("sourceModel", ""):
                continue

        return True

    return False


def bpmn_exists(process_id: str, target_filename: str | None = None) -> bool:
    """
    Prueft ob eine BPMN Datei fuer diesen Prozess bereits existiert.
    Zwei Kriterien (OR):
      1. Eine Datei enthaelt <process id=process_id>  (ID-Match)
      2. Eine Datei hat denselben Zieldateinamen       (Name-Match)
    Verhindert Duplikate wenn safe_filename() dasselbe BPMN
    unter leicht abweichendem Dateinamen ablegen wuerde.
    """
    for file in HULL_DIR.glob("*.bpmn"):
        # Kriterium 2: Dateiname-Match (schnell, kein XML-Parsen noetig)
        if target_filename and file.stem == target_filename:
            return True
        # Kriterium 1: ID-Match im XML
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            proc = root.find(f".//{bpmn('process')}")
            if proc is not None and proc.get("id") == process_id:
                return True
        except ET.ParseError:
            continue
    return False


def safe_filename(name: str) -> str:
    """Bereinigt einen Prozessnamen fuer den Einsatz als Dateiname.
    Erlaubte Sonderzeichen: Leerzeichen, - _ . +
    """
    keepchars = (" ", "-", "_", ".", "+")
    return "".join(c for c in name if c.isalnum() or c in keepchars).strip()


# ----------------------------------------------------------
# master.xml Extraktion
# ----------------------------------------------------------

def extract_processes_from_master() -> list:
    """
    Liest alle BusinessProcess-Elemente aus master.xml.
    Gibt eine Liste von dicts zurueck:
      - id         : Archi identifier
      - name       : erster gefundener <n> Text (bevorzugt xml:lang="de")
      - xsi_type   : z.B. "BusinessProcess"
      - sourceModel: Quelldatei laut XML04-Annotation
    """
    if not MASTER_XML.exists():
        print(f"[M2B01] ERROR: master.xml not found: {MASTER_XML}")
        return []

    processes = []

    try:
        tree = ET.parse(MASTER_XML)
        master_root = tree.getroot()
    except ET.ParseError as e:
        print(f"[M2B01] ERROR: cannot parse master.xml: {e}")
        return []

    for el in master_root.iter():
        # Nur direkte <element>-Tags beachten (lokaler Name ohne Namespace)
        local_tag = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if local_tag != "element":
            continue

        xsi_type = el.get(XSI_TYPE)
        if xsi_type != "BusinessProcess":
            continue

        archi_id = el.get("identifier")
        if not archi_id:
            continue  # Kein identifier -> nicht materialisierbar

        source_model = el.get("sourceModel", "")

        # Name extrahieren: bevorzuge xml:lang="de", Fallback: erster <n>
        name = None
        name_de = None
        name_any = None

        for name_el in el:
            nlocal = name_el.tag.split("}")[-1] if "}" in name_el.tag else name_el.tag
            if nlocal != "name":
                continue
            text = (name_el.text or "").strip()
            if not text:
                continue
            lang = name_el.get("{http://www.w3.org/XML/1998/namespace}lang", "")
            if lang == "de" and name_de is None:
                name_de = text
            if name_any is None:
                name_any = text

        name = name_de or name_any

        if not name:
            print(f"[M2B01] WARNING: BusinessProcess {archi_id} has no name, using ID as fallback")
            name = archi_id

        processes.append({
            "id": archi_id,
            "name": name,
            "xsi_type": xsi_type,
            "sourceModel": source_model
        })

    return processes


# ----------------------------------------------------------
# Core Logic
# ----------------------------------------------------------

def create_bpmn_hull(process_id: str, process_name: str):
    definitions = ET.Element(
        bpmn("definitions"),
        attrib={
            "targetNamespace": "http://example.com/bpmn"
        }
    )

    ET.SubElement(
        definitions,
        bpmn("process"),
        attrib={
            "id": process_id,
            "name": process_name,
            "isExecutable": "true"
        }
    )

    diagram = ET.SubElement(definitions, bpmndi("BPMNDiagram"), attrib={
        "id": "BPMNDiagram_1"
    })

    ET.SubElement(diagram, bpmndi("BPMNPlane"), attrib={
        "id": "BPMNPlane_1",
        "bpmnElement": process_id
    })

    tree = ET.ElementTree(definitions)

    filename = safe_filename(process_name) or process_id
    out_file = HULL_DIR / f"{filename}.bpmn"
    tree.write(out_file, encoding="utf-8", xml_declaration=True)

    print(f"[M2B01] created BPMN hull: {out_file.name}")


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main():
    HULL_DIR.mkdir(parents=True, exist_ok=True)

    # Ebene 1: Scope Filter aus run-scope.txt laden
    bpmn_scope = load_bpmn_scope()

    # Ebene 2: Hard Filter aus M2Bmapping.txt laden
    mapping_rules = load_mapping_rules()
    print(f"[M2B01] mapping rules loaded: {len(mapping_rules)}")

    # BusinessProcesses aus master.xml lesen
    archi_processes = extract_processes_from_master()
    print(f"[M2B01] BusinessProcess elements found in master.xml: {len(archi_processes)}")

    created = 0
    skipped_scope = 0
    skipped_mapping = 0
    skipped_exists = 0

    for proc in archi_processes:

        # Ebene 1: Scope Filter (run-scope.txt SOURCE=BPMN)
        if not matches_scope(proc, bpmn_scope):
            print(f"[M2B01] filtered by scope: {proc['id']} ({proc.get('sourceModel', '-')})")
            skipped_scope += 1
            continue

        # Ebene 2: Hard Filter (M2Bmapping.txt)
        if not matches_mapping(proc, mapping_rules):
            print(f"[M2B01] filtered by mapping: {proc['id']} ({proc.get('sourceModel', '-')})")
            skipped_mapping += 1
            continue

        process_id = proc["id"]
        process_name = proc["name"]

        target_filename = safe_filename(process_name) or process_id

        if bpmn_exists(process_id, target_filename):
            print(f"[M2B01] BPMN exists for {process_id} ({process_name}) -> skip")
            skipped_exists += 1
            continue

        create_bpmn_hull(process_id, process_name)
        created += 1

    print(f"[M2B01] OK | created={created} skipped_scope={skipped_scope} skipped_mapping={skipped_mapping} skipped_exists={skipped_exists}")


if __name__ == "__main__":
    main()
