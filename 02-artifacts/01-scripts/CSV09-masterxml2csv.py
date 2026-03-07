"""
CSV09-masterXml2Csv.py
======================
Converts master.xml into Archi-compatible CSV import files:
  - elements.csv
  - relations.csv
  - properties.csv

master.xml structure:
  <master> root contains direct children of mixed types:
    - ArchiMate elements:  sourceSystem="archi"  (ArchiMate 3.0 namespace)
    - BPMN definitions:    sourceSystem="bpmn"   (BPMN 2.0 namespace)
  Both sit as flat siblings under <master>.

Dispatcher logic:
  Iterates direct children of <master> and dispatches by sourceSystem:
    "archi"  -> parse_archi_element()
    "bpmn"   -> parse_bpmn_definitions()  (via bpmnmastercsvsync.txt rules)
    unknown  -> logged and skipped

run-scope.txt:
  SOURCE=MASTER + MODEL=<sourceModel value> filters which children are processed.
  Empty run-scope = process ALL children regardless of sourceModel.
  Lines starting with # are inactive.

BPMN match logic (per process element):
  Name match found in elements.csv (exact, case-sensitive):
    -> append property row: archi_id, BPMN_ID, <bpmn_process_id>
  No match:
    -> append new element row WITHOUT ID (Archi assigns ID on import)
    -> append property row: (empty ID), BPMN_ID, <bpmn_process_id>

Output:
  elements.csv, relations.csv, properties.csv  (overwrite, atomic write)

File locations (relative to BLUEPRINT_ROOT):
  master.xml        02-artifacts\\00-xml\\00-master\\master.xml
  bpmn mapping      02-artifacts\\00-xml\\01-mapping\\bpmnmastercsvsync.txt
  csv output        02-artifacts\\02-csv\\00-master
  log               03-stages\\99-logs\\CSV09-masterXml2Csv.log
  run-scope         03-stages\\run-scope.txt

Naming convention: CSV[NN]-[PascalCaseDescription].py
"""

import sys
import csv
import io
import logging
from pathlib import Path
from xml.etree import ElementTree as ET
from datetime import datetime


# ===========================================================
# CONFIG
# ===========================================================

SCRIPT_NAME          = "CSV09-masterXml2Csv"
ROOT_FILE            = "root.txt"
SOURCE_FILTER_MASTER = "MASTER"

NS_A    = "http://www.opengroup.org/xsd/archimate/3.0/"
NS_XSI  = "http://www.w3.org/2001/XMLSchema-instance"
NS_BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL"

MASTER_XML_REL   = r"02-artifacts\00-xml\00-master\master.xml"
RUN_SCOPE_REL    = r"03-stages\run-scope.txt"
CSV_OUT_REL      = r"02-artifacts\02-csv\00-master"
LOG_REL          = r"03-stages\99-logs\CSV09-masterXml2Csv.log"
BPMN_MAPPING_REL = r"02-artifacts\00-xml\01-mapping\bpmnmastercsvsync.txt"

ELEMENTS_CSV   = "elements.csv"
RELATIONS_CSV  = "relations.csv"
PROPERTIES_CSV = "properties.csv"

ELEMENTS_HEADER   = ["ID", "Type", "Name", "Documentation", "Specialization"]
RELATIONS_HEADER  = ["ID", "Type", "Name", "Documentation", "Source", "Target", "Specialization"]
PROPERTIES_HEADER = ["ID", "Key", "Value"]


# ===========================================================
# ROOT RESOLUTION
# ===========================================================

def resolve_root() -> Path:
    search = Path(__file__).resolve().parent
    for _ in range(8):
        candidate = search / ROOT_FILE
        if candidate.exists():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("BLUEPRINT_ROOT=") or line.startswith("<rootfolde>="):
                    value = line.split("=", 1)[1].strip()
                    return Path(value)
            break
        search = search.parent
    raise FileNotFoundError(
        "root.txt not found or BLUEPRINT_ROOT not set. "
        "Place script inside the Blueprint folder structure."
    )


# ===========================================================
# LOGGING
# ===========================================================

def setup_logging(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(SCRIPT_NAME)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    if not logger.handlers:
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setFormatter(fmt)
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger


# ===========================================================
# RUN-SCOPE PARSING
# ===========================================================

def load_run_scope(scope_path: Path, source_filter: str, logger: logging.Logger) -> set:
    """
    Returns set of MODEL values where paired SOURCE matches source_filter.
    Empty set = no active entries = process ALL.
    Lines starting with # are inactive.
    """
    allowed = set()

    if not scope_path.exists():
        logger.warning(f"run-scope.txt not found: {scope_path} — processing ALL")
        return allowed

    lines = [
        ln.strip()
        for ln in scope_path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.upper().startswith("SOURCE="):
            source_val = line.split("=", 1)[1].strip().upper()
            if i + 1 < len(lines) and lines[i + 1].upper().startswith("MODEL="):
                model_val = lines[i + 1].split("=", 1)[1].strip()
                if source_val == source_filter.upper():
                    allowed.add(model_val)
                i += 2
                continue
        i += 1

    if allowed:
        logger.info(f"Run scope (SOURCE={source_filter}): {allowed}")
    else:
        logger.info(f"Run scope: no active SOURCE={source_filter} entries — processing ALL")

    return allowed


# ===========================================================
# BPMN MAPPING LOADER
# ===========================================================

def load_bpmn_mapping(mapping_path: Path, logger: logging.Logger) -> list[dict]:
    """
    Parses bpmnmastercsvsync.txt.

    Format — 5-column CSV; rows starting with # are comments:
      "bpmn_local_tag","bpmn_id_attribute","bpmn_name_attribute","archi_type","property_key"

    Column definitions:
      bpmn_local_tag      Local XML tag name to match (case-insensitive).
                          Examples: process, subProcess, callActivity
      bpmn_id_attribute   Attribute holding the BPMN process ID stored as
                          3rd-party reference in properties.csv.
                          Typically: id
      bpmn_name_attribute Attribute holding the display name used for
                          exact matching against elements.csv Name column.
                          Typically: name
      archi_type          ArchiMate type used when creating NEW elements.
                          Examples: BusinessProcess, ApplicationProcess
      property_key        Key written to properties.csv.
                          Examples: BPMN_ID, ERP_ID, SAP_ID

    Rules evaluated in order; first matching rule per element wins.
    """
    if not mapping_path.exists():
        raise FileNotFoundError(f"Missing BPMN mapping file: {mapping_path}")

    rules = []
    with open(mapping_path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for lineno, row in enumerate(reader, start=1):
            if not row or row[0].strip().startswith("#"):
                continue
            if len(row) < 5:
                logger.warning(
                    f"bpmnmastercsvsync.txt line {lineno}: "
                    f"expected 5 columns, got {len(row)} — skipped"
                )
                continue
            rules.append({
                "bpmn_local_tag":      row[0].strip().lower(),
                "bpmn_id_attribute":   row[1].strip(),
                "bpmn_name_attribute": row[2].strip(),
                "archi_type":          row[3].strip(),
                "property_key":        row[4].strip(),
            })

    logger.info(f"BPMN mapping: {len(rules)} rule(s) from {mapping_path.name}")
    if not rules:
        raise ValueError("bpmnmastercsvsync.txt contains no active rules")
    return rules


# ===========================================================
# ARCHI ELEMENT PARSER
# ===========================================================

def parse_archi_element(
    child: ET.Element,
    prop_defs: dict[str, str],
    logger: logging.Logger,
) -> tuple[dict | None, list[dict]]:
    """
    Parses a single ArchiMate <element> direct child of <master>.
    Returns (element_dict, properties_list).
    """
    a   = f"{{{NS_A}}}"
    xsi = f"{{{NS_XSI}}}"

    eid = child.get("identifier")
    if not eid:
        logger.warning(f"ArchiMate element without identifier — skipped")
        return None, []

    etype   = child.get(f"{xsi}type", "")
    name_el = child.find(f"{a}name")
    name    = name_el.text.strip() if (name_el is not None and name_el.text) else ""
    doc_el  = child.find(f"{a}documentation")
    doc     = doc_el.text.strip() if (doc_el is not None and doc_el.text) else ""

    element = {
        "ID":             eid,
        "Type":           etype,
        "Name":           name,
        "Documentation":  doc,
        "Specialization": "",
    }

    properties = []
    for prop in child.findall(f".//{a}property"):
        ref    = prop.get("propertyDefinitionRef", "")
        key    = prop_defs.get(ref, ref)
        val_el = prop.find(f"{a}value")
        val    = val_el.text.strip() if (val_el is not None and val_el.text) else ""
        properties.append({"ID": eid, "Key": key, "Value": val})

    return element, properties


# ===========================================================
# BPMN DEFINITIONS PARSER
# ===========================================================

def _local(tag: str) -> str:
    """Strip namespace URI: '{http://...}localname' -> 'localname'."""
    return tag.split("}", 1)[1] if tag.startswith("{") else tag


def parse_bpmn_definitions(
    child: ET.Element,
    bpmn_rules: list[dict],
    existing_names: dict[str, str],
    logger: logging.Logger,
) -> tuple[list[dict], list[dict]]:
    """
    Parses a single BPMN <definitions> direct child of <master>.
    Dispatches via bpmnmastercsvsync.txt rules.

    Match logic per BPMN element:
      Name found in existing_names -> property row with archi_id
      No match                     -> new element stub (empty ID) + property row

    Returns (new_elements, new_properties).
    existing_names is updated in-place for within-run deduplication.
    """
    rule_by_tag = {}
    for rule in bpmn_rules:
        tag = rule["bpmn_local_tag"]
        if tag not in rule_by_tag:
            rule_by_tag[tag] = rule

    new_elements:   list[dict] = []
    new_properties: list[dict] = []

    for el in child.iter():
        local = _local(el.tag).lower()
        rule  = rule_by_tag.get(local)
        if rule is None:
            continue

        bpmn_id   = (el.get(rule["bpmn_id_attribute"])   or "").strip()
        bpmn_name = (el.get(rule["bpmn_name_attribute"]) or "").strip()

        if not bpmn_id:
            logger.warning(
                f"  BPMN <{local}> missing '{rule['bpmn_id_attribute']}' — skipped"
            )
            continue

        matched_id = existing_names.get(bpmn_name)  # None = no match

        if matched_id is not None:
            owner_id = matched_id
            logger.info(
                f"  BPMN MATCH  | name={bpmn_name!r} "
                f"archi_id={owner_id!r} | {rule['property_key']}={bpmn_id}"
            )
        else:
            owner_id = ""
            new_elements.append({
                "ID":             "",
                "Type":           rule["archi_type"],
                "Name":           bpmn_name,
                "Documentation":  "",
                "Specialization": "",
            })
            # Register so subsequent BPMN blocks in same run don't duplicate
            existing_names[bpmn_name] = ""
            logger.info(
                f"  BPMN NEW    | name={bpmn_name!r} "
                f"type={rule['archi_type']} | {rule['property_key']}={bpmn_id}"
            )

        new_properties.append({
            "ID":    owner_id,
            "Key":   rule["property_key"],
            "Value": bpmn_id,
        })

    return new_elements, new_properties


# ===========================================================
# CSV WRITING
# ===========================================================

def write_csv(path: Path, headers: list, rows: list, logger: logging.Logger):
    """Write CSV atomically via in-memory buffer. Overwrites existing file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf,
        fieldnames=headers,
        quoting=csv.QUOTE_ALL,
        extrasaction="ignore",
        lineterminator="\r\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8")
    logger.info(f"Written {len(rows):>5} rows -> {path.name}")


# ===========================================================
# MAIN
# ===========================================================

def main():
    try:
        root_path = resolve_root()
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    log_path = root_path / LOG_REL
    logger   = setup_logging(log_path)

    logger.info("=" * 60)
    logger.info(f"{SCRIPT_NAME} START  {datetime.now().isoformat()}")
    logger.info(f"BLUEPRINT_ROOT  : {root_path}")

    xml_path     = root_path / MASTER_XML_REL
    scope_path   = root_path / RUN_SCOPE_REL
    out_dir      = root_path / CSV_OUT_REL
    mapping_path = root_path / BPMN_MAPPING_REL

    logger.info(f"master.xml      : {xml_path}")
    logger.info(f"BPMN mapping    : {mapping_path}")
    logger.info(f"run-scope.txt   : {scope_path}")
    logger.info(f"CSV output dir  : {out_dir}")

    if not xml_path.exists():
        logger.error(f"master.xml not found: {xml_path}")
        sys.exit(1)

    # Load BPMN mapping (required — abort if missing)
    try:
        bpmn_rules = load_bpmn_mapping(mapping_path, logger)
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"BPMN mapping error: {e}")
        sys.exit(1)

    # Load run-scope filter
    run_scope = load_run_scope(scope_path, SOURCE_FILTER_MASTER, logger)

    # Parse master.xml
    logger.info("-" * 60)
    logger.info(f"Parsing: {xml_path}")

    try:
        tree = ET.parse(str(xml_path))
    except ET.ParseError as e:
        logger.error(f"XML parse error: {e}")
        sys.exit(1)

    master_root = tree.getroot()

    # Collect PropertyDefinitions from ArchiMate elements (for property key resolution)
    a   = f"{{{NS_A}}}"
    xsi = f"{{{NS_XSI}}}"
    prop_defs: dict[str, str] = {}
    for pd in master_root.iter(f"{a}propertyDefinition"):
        pid     = pd.get("identifier")
        name_el = pd.find(f"{a}name")
        name    = name_el.text.strip() if (name_el is not None and name_el.text) else pid
        if pid:
            prop_defs[pid] = name
    logger.info(f"PropertyDefinitions: {len(prop_defs)}")

    # Accumulators
    all_elements:   list[dict] = []
    all_relations:  list[dict] = []
    all_properties: list[dict] = []

    # existing_names tracks Name->ID for BPMN match logic
    # Pre-seeded from archi elements parsed in this run
    existing_names: dict[str, str] = {}

    stats = {"archi": 0, "bpmn_defs": 0, "bpmn_new": 0, "bpmn_matched": 0, "skipped": 0}

    # ----------------------------------------------------------
    # Dispatch over direct children of <master>
    # ----------------------------------------------------------
    for child in master_root:
        local_tag    = _local(child.tag)
        source_sys   = child.get("sourceSystem", "").lower()
        source_model = child.get("sourceModel", "")

        # Scope filter: skip if run_scope is active and this model is not in it
        if run_scope and source_model not in run_scope:
            logger.debug(
                f"  SCOPE SKIP | sourceSystem={source_sys!r} "
                f"sourceModel={source_model!r}"
            )
            stats["skipped"] += 1
            continue

        # --- ArchiMate element ---
        if source_sys == "archi" and local_tag == "element":
            element, props = parse_archi_element(child, prop_defs, logger)
            if element:
                all_elements.append(element)
                all_properties.extend(props)
                existing_names[element["Name"]] = element["ID"]
                stats["archi"] += 1
                logger.debug(
                    f"  ARCHI | {element['Type']:25} | {element['Name']!r}"
                )

        # --- ArchiMate relationship ---
        elif source_sys == "archi" and local_tag == "relationship":
            eid   = child.get("identifier")
            etype = child.get(f"{xsi}type", "")
            name_el = child.find(f"{a}name")
            name    = name_el.text.strip() if (name_el is not None and name_el.text) else ""
            doc_el  = child.find(f"{a}documentation")
            doc     = doc_el.text.strip() if (doc_el is not None and doc_el.text) else ""
            if eid:
                all_relations.append({
                    "ID":             eid,
                    "Type":           etype,
                    "Name":           name,
                    "Documentation":  doc,
                    "Source":         child.get("source", ""),
                    "Target":         child.get("target", ""),
                    "Specialization": "",
                })
                # Collect properties for relationship
                for prop in child.findall(f".//{a}property"):
                    ref    = prop.get("propertyDefinitionRef", "")
                    key    = prop_defs.get(ref, ref)
                    val_el = prop.find(f"{a}value")
                    val    = val_el.text.strip() if (val_el is not None and val_el.text) else ""
                    all_properties.append({"ID": eid, "Key": key, "Value": val})

        # --- BPMN definitions block ---
        elif local_tag == "definitions":
            bpmn_src = child.get("sourceModel", "")
            logger.info(f"  BPMN | sourceModel={bpmn_src!r}")
            new_els, new_props = parse_bpmn_definitions(
                child, bpmn_rules, existing_names, logger
            )
            all_elements.extend(new_els)
            all_properties.extend(new_props)
            stats["bpmn_defs"]    += 1
            stats["bpmn_new"]     += len(new_els)
            stats["bpmn_matched"] += len(new_props) - len(new_els)

        else:
            logger.warning(
                f"  UNKNOWN child | tag={local_tag!r} "
                f"sourceSystem={source_sys!r} — skipped"
            )
            stats["skipped"] += 1

    # ----------------------------------------------------------
    # Write CSVs (atomic overwrite)
    # ----------------------------------------------------------
    logger.info("-" * 60)
    logger.info("Writing CSV output...")

    try:
        write_csv(out_dir / ELEMENTS_CSV,   ELEMENTS_HEADER,   all_elements,   logger)
        write_csv(out_dir / RELATIONS_CSV,  RELATIONS_HEADER,  all_relations,  logger)
        write_csv(out_dir / PROPERTIES_CSV, PROPERTIES_HEADER, all_properties, logger)
    except Exception as e:
        logger.error(f"CSV write failed: {e}", exc_info=True)
        sys.exit(1)

    logger.info("-" * 60)
    logger.info(
        f"Summary | archi={stats['archi']} "
        f"bpmn_defs={stats['bpmn_defs']} "
        f"bpmn_new_elements={stats['bpmn_new']} "
        f"bpmn_matched={stats['bpmn_matched']} "
        f"skipped={stats['skipped']}"
    )
    logger.info("=" * 60)
    logger.info(f"{SCRIPT_NAME} DONE")
    print(f"[{SCRIPT_NAME}] OK | completed successfully")


if __name__ == "__main__":
    main()
