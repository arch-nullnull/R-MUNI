"""
CSV10-masterCsv2Assets.py
=========================
Converts master.xml into Jira Assets-compatible CSV import files,
grouped by semantic category.

Input:
  master.xml    02-artifacts/00-xml/00-master/master.xml

Output (02-artifacts/02-csv/05-assets/):
  assets_processes.csv     BusinessProcess, BusinessFunction, BusinessService,
                           BusinessInteraction, ApplicationProcess,
                           ApplicationFunction, TechnologyProcess + BPMN matches
  assets_applications.csv  ApplicationComponent, ApplicationService,
                           ApplicationInterface, ApplicationCollaboration,
                           ApplicationEvent, SystemSoftware
  assets_actors.csv        BusinessActor, BusinessRole, BusinessInterface,
                           Stakeholder
  assets_technology.csv    Node, Device, TechnologyService, TechnologyFunction,
                           TechnologyInterface, TechnologyCollaboration,
                           TechnologyEvent, CommunicationNetwork, Path
  assets_motivation.csv    Goal, Requirement, Principle, Constraint, Driver,
                           Assessment, Outcome, Value, Meaning, Capability,
                           ValueStream
  assets_physical.csv      Equipment, Facility, Material, DistributionNetwork,
                           Location
  assets_other.csv         DataObject, BusinessObject, Artifact, Representation,
                           Deliverable, Contract, Product, Resource, WorkPackage,
                           Plateau, Gap, CourseOfAction, Grouping,
                           ImplementationEvent, BusinessEvent,
                           ApplicationInteraction, TechnologyInteraction
  assets_relations.csv     All relations (ONLY if INCLUDE_RELATIONS=true in
                           assetsexport.txt)

Column mapping (master.xml -> Jira Assets CSV):
  identifier    -> objectKey        Unique key; collision strategy applies
  xsi:type      -> ArchiType        ArchiMate type label
  name          -> Name             Display name
  documentation -> Description      Free-text
  specialization -> Specialization  Passthrough
  sourceModel   -> SourceModel      Origin model file
  [properties]  -> one column each  Flattened, one col per property key

ID collision strategy (DEFAULT: merge):
  Same identifier appears in multiple sourceModels.
  merge      First wins; SourceModel = comma-joined list of all models
  last_wins  Last occurrence overwrites
  prefix     objectKey = "<sourceModel>::<id>" (always unique)

assetsexport.txt (02-artifacts/02-csv/02-sync/assetsexport.txt):
  Controls export behaviour. Format: KEY=VALUE lines.
  Lines starting with # are inactive comments.

  Supported keys:
    INCLUDE_RELATIONS=true        Export relations (default: false)
    INCLUDE_SOURCE_MODEL=true     Add SourceModel column (default: true)
    ID_STRATEGY=merge             merge | last_wins | prefix (default: merge)
    EXCLUDE_TYPE=Artifact         Exclude ArchiMate type (repeatable)
    INCLUDE_SOURCEMODEL=Architecture.xml  Restrict to sourceModel (repeatable)

  Example assetsexport.txt:
    # Export config for Jira Assets
    INCLUDE_RELATIONS=true
    ID_STRATEGY=merge
    EXCLUDE_TYPE=Artifact
    INCLUDE_SOURCEMODEL=Architecture.xml

File locations (relative to BLUEPRINT_ROOT):
  master.xml    02-artifacts/00-xml/00-master/master.xml
  filter        02-artifacts/02-csv/02-sync/assetsexport.txt
  assets output 02-artifacts/02-csv/05-assets/
  log           03-stages/99-logs/CSV10-masterCsv2Assets.log
  run-scope     03-stages/run-scope.txt

Naming convention: CSV[NN]-[PascalCaseDescription].py
"""

import sys
import csv
import io
import logging
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from xml.etree import ElementTree as ET


# ===========================================================
# CONFIG
# ===========================================================

SCRIPT_NAME = "CSV10-masterCsv2Assets"
ROOT_FILE   = "root.txt"

MASTER_XML_REL = r"02-artifacts/00-xml/00-master/master.xml"
ASSETS_OUT_REL = r"02-artifacts/02-csv/05-assets"
FILTER_REL     = r"02-artifacts/02-csv/02-sync/assetsexport.txt"
LOG_REL        = r"03-stages/99-logs/CSV10-masterCsv2Assets.log"
RUN_SCOPE_REL  = r"03-stages/run-scope.txt"

NS_A   = "http://www.opengroup.org/xsd/archimate/3.0/"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"

# ----------------------------------------------------------
# Semantic groups: output filename stem -> [ArchiMate types]
# ----------------------------------------------------------
TYPE_GROUPS: dict[str, list[str]] = {
    "assets_processes": [
        "BusinessProcess", "BusinessFunction", "BusinessService",
        "BusinessInteraction", "ApplicationProcess", "ApplicationFunction",
        "TechnologyProcess",
    ],
    "assets_applications": [
        "ApplicationComponent", "ApplicationService", "ApplicationInterface",
        "ApplicationCollaboration", "ApplicationEvent", "SystemSoftware",
    ],
    "assets_actors": [
        "BusinessActor", "BusinessRole", "BusinessInterface", "Stakeholder",
    ],
    "assets_technology": [
        "Node", "Device", "TechnologyService", "TechnologyFunction",
        "TechnologyInterface", "TechnologyCollaboration", "TechnologyEvent",
        "CommunicationNetwork", "Path",
    ],
    "assets_motivation": [
        "Goal", "Requirement", "Principle", "Constraint", "Driver",
        "Assessment", "Outcome", "Value", "Meaning", "Capability",
        "ValueStream",
    ],
    "assets_physical": [
        "Equipment", "Facility", "Material", "DistributionNetwork", "Location",
    ],
    "assets_other": [
        "DataObject", "BusinessObject", "Artifact", "Representation",
        "Deliverable", "Contract", "Product", "Resource", "WorkPackage",
        "Plateau", "Gap", "CourseOfAction", "Grouping",
        "ImplementationEvent", "BusinessEvent",
        "ApplicationInteraction", "TechnologyInteraction",
    ],
}

# Reverse lookup: ArchiMate type -> group stem
TYPE_TO_GROUP: dict[str, str] = {
    t: g for g, types in TYPE_GROUPS.items() for t in types
}

BASE_COLUMNS = [
    "objectKey", "ArchiType", "Name", "Description",
    "Specialization", "SourceModel",
]

RELATIONS_COLUMNS = [
    "objectKey", "RelationType", "Name", "Description",
    "Source", "Target", "Specialization", "SourceModel",
]


# ===========================================================
# HELPERS
# ===========================================================

def _local(tag: str) -> str:
    """Strip XML namespace: '{http://...}localname' -> 'localname'."""
    return tag.split("}", 1)[1] if tag.startswith("{") else tag


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
                    return Path(line.split("=", 1)[1].strip())
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
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    if not logger.handlers:
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setFormatter(fmt)
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger


# ===========================================================
# ASSETSEXPORT.TXT CONFIG LOADER
# ===========================================================

def load_export_config(path: Path, logger: logging.Logger) -> dict:
    """
    Parses assetsexport.txt.

    Returns dict:
      include_relations    bool   (default False)
      include_source_model bool   (default True)
      id_strategy          str    merge | last_wins | prefix  (default merge)
      exclude_types        set    ArchiMate types to skip
      include_sourcemodels set    restrict to these sourceModels (empty = all)
    """
    cfg = {
        "include_relations":    False,
        "include_source_model": True,
        "id_strategy":          "merge",
        "exclude_types":        set(),
        "include_sourcemodels": set(),
    }

    if not path.exists():
        logger.info(f"assetsexport.txt not found: {path} — using defaults")
        return cfg

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, val = line.partition("=")
            key = key.strip().upper()
            val = val.strip()
            if key == "INCLUDE_RELATIONS":
                cfg["include_relations"] = val.lower() in ("true", "1", "yes")
            elif key == "INCLUDE_SOURCE_MODEL":
                cfg["include_source_model"] = val.lower() in ("true", "1", "yes")
            elif key == "ID_STRATEGY":
                if val.lower() in ("merge", "last_wins", "prefix"):
                    cfg["id_strategy"] = val.lower()
                else:
                    logger.warning(f"Unknown ID_STRATEGY={val!r} — using merge")
            elif key == "EXCLUDE_TYPE":
                cfg["exclude_types"].add(val)
            elif key == "INCLUDE_SOURCEMODEL":
                cfg["include_sourcemodels"].add(val)
        else:
            # Bare line = legacy EXCLUDE_TYPE for backwards compat
            cfg["exclude_types"].add(line)

    logger.info(
        f"Export config loaded: relations={cfg['include_relations']} "
        f"id_strategy={cfg['id_strategy']!r} "
        f"exclude_types={cfg['exclude_types']} "
        f"include_sourcemodels={cfg['include_sourcemodels']}"
    )
    return cfg


# ===========================================================
# RUN-SCOPE LOADER
# ===========================================================

def load_run_scope(path: Path, logger: logging.Logger) -> set:
    """Returns set of MODEL values for SOURCE=MASTER. Empty = process ALL."""
    allowed = set()
    if not path.exists():
        logger.warning(f"run-scope.txt not found — processing ALL")
        return allowed
    lines = [
        ln.strip()
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    i = 0
    while i < len(lines):
        if lines[i].upper().startswith("SOURCE="):
            src = lines[i].split("=", 1)[1].strip().upper()
            if i + 1 < len(lines) and lines[i + 1].upper().startswith("MODEL="):
                mdl = lines[i + 1].split("=", 1)[1].strip()
                if src == "MASTER":
                    allowed.add(mdl)
                i += 2
                continue
        i += 1
    if allowed:
        logger.info(f"Run scope (SOURCE=MASTER): {allowed}")
    else:
        logger.info("Run scope: no active MASTER entries — processing ALL")
    return allowed


# ===========================================================
# XML PARSING
# ===========================================================

def parse_master_xml(
    xml_path: Path,
    cfg: dict,
    run_scope: set,
    logger: logging.Logger,
) -> tuple[list[dict], list[dict], dict[str, set]]:
    """
    Single-pass parse of master.xml.

    Returns:
      elements   list[dict]          Assets-ready, flattened rows
      relations  list[dict]          Relation rows (empty if not enabled)
      prop_keys  dict[group -> set]  Property keys seen per group
    """
    a   = f"{{{NS_A}}}"
    xsi = f"{{{NS_XSI}}}"

    try:
        tree = ET.parse(str(xml_path))
    except ET.ParseError as e:
        logger.error(f"XML parse error: {e}")
        sys.exit(1)

    root = tree.getroot()

    # Collect PropertyDefinitions
    prop_defs: dict[str, str] = {}
    for pd in root.iter(f"{a}propertyDefinition"):
        pid     = pd.get("identifier")
        name_el = pd.find(f"{a}name")
        pname   = (name_el.text.strip()
                   if (name_el is not None and name_el.text) else pid)
        if pid:
            prop_defs[pid] = pname
    logger.info(f"PropertyDefinitions ({len(prop_defs)}): "
                f"{list(prop_defs.values())}")

    elements:  list[dict]     = []
    relations: list[dict]     = []
    prop_keys: dict[str, set] = defaultdict(set)

    # id -> list index for collision handling
    id_index: dict[str, int] = {}

    # name -> objectKey for BPMN matching (seeded from archi pass)
    bpmn_name_map: dict[str, str] = {}

    stats = {
        "archi_elements":  0,
        "archi_relations": 0,
        "bpmn_matched":    0,
        "bpmn_new":        0,
        "id_collisions":   0,
        "skipped_scope":   0,
        "skipped_type":    0,
    }

    def _obj_key(eid: str, src_model: str) -> str:
        if cfg["id_strategy"] == "prefix":
            return f"{src_model}::{eid}" if src_model else eid
        return eid

    # ----------------------------------------------------------
    # Iterate direct children of <master>
    # ----------------------------------------------------------
    for child in root:
        lt         = _local(child.tag)
        source_sys = child.get("sourceSystem", "").lower()
        src_model  = child.get("sourceModel", "")

        # Run-scope filter
        if run_scope and src_model not in run_scope:
            stats["skipped_scope"] += 1
            continue

        # assetsexport.txt INCLUDE_SOURCEMODEL filter
        if cfg["include_sourcemodels"] and src_model not in cfg["include_sourcemodels"]:
            continue

        # ----------------------------------------------------------------
        # ArchiMate element
        # ----------------------------------------------------------------
        if source_sys == "archi" and lt == "element":
            eid   = child.get("identifier", "").strip()
            etype = child.get(f"{xsi}type", "")

            if etype in cfg["exclude_types"]:
                stats["skipped_type"] += 1
                logger.debug(f"  EXCLUDED TYPE | {etype}")
                continue

            name_el = child.find(f"{a}name")
            name    = (name_el.text.strip()
                       if (name_el is not None and name_el.text) else "")
            doc_el  = child.find(f"{a}documentation")
            doc     = (doc_el.text.strip()
                       if (doc_el is not None and doc_el.text) else "")
            spec    = child.get("specialization", "")

            elem_props: dict[str, str] = {}
            for prop in child.findall(f".//{a}property"):
                ref    = prop.get("propertyDefinitionRef", "")
                pkey   = prop_defs.get(ref, ref)
                val_el = prop.find(f"{a}value")
                val    = (val_el.text.strip()
                          if (val_el is not None and val_el.text) else "")
                elem_props[pkey] = val

            obj_key = _obj_key(eid, src_model)
            group   = TYPE_TO_GROUP.get(etype, "assets_other")

            row = {
                "objectKey":      obj_key,
                "ArchiType":      etype,
                "Name":           name,
                "Description":    doc,
                "Specialization": spec,
                "SourceModel":    src_model,
                **elem_props,
            }

            # --- Collision handling ---
            if cfg["id_strategy"] == "prefix":
                elements.append(row)
                id_index[obj_key] = len(elements) - 1

            elif cfg["id_strategy"] == "last_wins":
                if eid in id_index:
                    elements[id_index[eid]] = row
                    stats["id_collisions"] += 1
                    logger.debug(f"  COLLISION last_wins | {eid!r}")
                else:
                    elements.append(row)
                    id_index[eid] = len(elements) - 1

            else:  # merge (default)
                if eid in id_index:
                    existing = elements[id_index[eid]]
                    prev_sm  = existing["SourceModel"]
                    if src_model and src_model not in prev_sm.split(", "):
                        existing["SourceModel"] = f"{prev_sm}, {src_model}"
                    stats["id_collisions"] += 1
                    logger.debug(
                        f"  COLLISION merge | {eid!r} "
                        f"models={existing['SourceModel']!r}"
                    )
                else:
                    elements.append(row)
                    id_index[eid] = len(elements) - 1

            # Seed BPMN name map
            if name:
                bpmn_name_map[name] = obj_key

            # Track property keys per group
            for k in elem_props:
                prop_keys[group].add(k)

            stats["archi_elements"] += 1

        # ----------------------------------------------------------------
        # ArchiMate relationship (optional)
        # ----------------------------------------------------------------
        elif source_sys == "archi" and lt == "relationship":
            if not cfg["include_relations"]:
                continue

            eid     = child.get("identifier", "").strip()
            etype   = child.get(f"{xsi}type", "")
            name_el = child.find(f"{a}name")
            name    = (name_el.text.strip()
                       if (name_el is not None and name_el.text) else "")
            doc_el  = child.find(f"{a}documentation")
            doc     = (doc_el.text.strip()
                       if (doc_el is not None and doc_el.text) else "")
            obj_key = _obj_key(eid, src_model)

            relations.append({
                "objectKey":      obj_key,
                "RelationType":   etype,
                "Name":           name,
                "Description":    doc,
                "Source":         child.get("source", ""),
                "Target":         child.get("target", ""),
                "Specialization": child.get("specialization", ""),
                "SourceModel":    src_model,
            })
            stats["archi_relations"] += 1

        # ----------------------------------------------------------------
        # BPMN definitions
        # ----------------------------------------------------------------
        elif lt == "definitions":
            bpmn_src = child.get("sourceModel", "")
            for el in child.iter():
                if _local(el.tag).lower() != "process":
                    continue
                bpmn_id   = (el.get("id")   or "").strip()
                bpmn_name = (el.get("name") or "").strip()

                if not bpmn_id:
                    logger.warning("  BPMN <process> missing 'id' — skipped")
                    continue

                matched_key = bpmn_name_map.get(bpmn_name)

                if matched_key is not None:
                    # Enrich existing element with BPMN_ID
                    idx = id_index.get(matched_key)
                    if idx is not None:
                        elements[idx]["BPMN_ID"] = bpmn_id
                        grp = TYPE_TO_GROUP.get(
                            elements[idx].get("ArchiType", ""), "assets_other"
                        )
                        prop_keys[grp].add("BPMN_ID")
                    stats["bpmn_matched"] += 1
                    logger.info(
                        f"  BPMN MATCH  | {bpmn_name!r} "
                        f"-> key={matched_key!r} BPMN_ID={bpmn_id}"
                    )
                else:
                    # New stub for unmatched BPMN process
                    obj_key = bpmn_id
                    row = {
                        "objectKey":      obj_key,
                        "ArchiType":      "BusinessProcess",
                        "Name":           bpmn_name,
                        "Description":    "",
                        "Specialization": "",
                        "SourceModel":    bpmn_src or "bpmn",
                        "BPMN_ID":        bpmn_id,
                    }
                    elements.append(row)
                    bpmn_name_map[bpmn_name] = obj_key
                    prop_keys["assets_processes"].add("BPMN_ID")
                    stats["bpmn_new"] += 1
                    logger.info(
                        f"  BPMN NEW    | {bpmn_name!r} "
                        f"BPMN_ID={bpmn_id}"
                    )

    logger.info(
        f"Parse complete | "
        f"elements={stats['archi_elements']} "
        f"relations={stats['archi_relations']} "
        f"bpmn_matched={stats['bpmn_matched']} "
        f"bpmn_new={stats['bpmn_new']} "
        f"id_collisions={stats['id_collisions']} "
        f"skipped_scope={stats['skipped_scope']} "
        f"skipped_type={stats['skipped_type']}"
    )
    return elements, relations, prop_keys


# ===========================================================
# CSV WRITING
# ===========================================================

def write_csv(path: Path, headers: list, rows: list,
              logger: logging.Logger) -> None:
    """Atomic write via in-memory buffer. Overwrites existing file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf,
        fieldnames=headers,
        quoting=csv.QUOTE_ALL,
        extrasaction="ignore",
        restval="",
        lineterminator="\r\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8")
    logger.info(f"  Written {len(rows):>5} rows -> {path.name}")


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
    logger.info(f"BLUEPRINT_ROOT : {root_path}")

    xml_path    = root_path / MASTER_XML_REL
    filter_path = root_path / FILTER_REL
    out_dir     = root_path / ASSETS_OUT_REL
    scope_path  = root_path / RUN_SCOPE_REL

    logger.info(f"master.xml     : {xml_path}")
    logger.info(f"assetsexport   : {filter_path}")
    logger.info(f"assets out dir : {out_dir}")

    if not xml_path.exists():
        logger.error(f"master.xml not found: {xml_path}")
        sys.exit(1)

    cfg       = load_export_config(filter_path, logger)
    run_scope = load_run_scope(scope_path, logger)

    logger.info("-" * 60)
    elements, relations, prop_keys = parse_master_xml(
        xml_path, cfg, run_scope, logger
    )

    # ----------------------------------------------------------
    # Group elements by semantic category
    # ----------------------------------------------------------
    grouped: dict[str, list[dict]] = defaultdict(list)
    unclassified_types: set[str]   = set()

    for row in elements:
        atype = row.get("ArchiType", "")
        group = TYPE_TO_GROUP.get(atype)
        if group:
            grouped[group].append(row)
        else:
            unclassified_types.add(atype)
            grouped["assets_other"].append(row)

    if unclassified_types:
        logger.warning(
            f"Unclassified ArchiTypes -> assets_other.csv: "
            f"{sorted(unclassified_types)}"
        )

    # ----------------------------------------------------------
    # Build column headers per group (base + dynamic properties)
    # ----------------------------------------------------------
    logger.info("-" * 60)
    logger.info("Writing output files...")

    base_cols = (BASE_COLUMNS if cfg["include_source_model"]
                 else [c for c in BASE_COLUMNS if c != "SourceModel"])

    written: list[str] = []

    for group_name, group_rows in grouped.items():
        if not group_rows:
            continue
        extra  = sorted(prop_keys.get(group_name, set()))
        hdrs   = base_cols + extra
        target = out_dir / f"{group_name}.csv"
        write_csv(target, hdrs, group_rows, logger)
        written.append(target.name)

    # Relations (opt-in)
    if cfg["include_relations"]:
        if relations:
            target = out_dir / "assets_relations.csv"
            write_csv(target, RELATIONS_COLUMNS, relations, logger)
            written.append(target.name)
        else:
            logger.info(
                "  Relations: INCLUDE_RELATIONS=true but no relations found"
            )

    # ----------------------------------------------------------
    # Summary
    # ----------------------------------------------------------
    logger.info("-" * 60)
    logger.info(f"Output files written ({len(written)}):")
    for f in written:
        logger.info(f"  {out_dir / f}")
    logger.info("=" * 60)
    logger.info(f"{SCRIPT_NAME} DONE")
    print(
        f"[{SCRIPT_NAME}] OK | {len(written)} file(s) written to {out_dir}"
    )


if __name__ == "__main__":
    main()
