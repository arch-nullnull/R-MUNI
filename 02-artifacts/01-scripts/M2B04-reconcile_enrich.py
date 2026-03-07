#!/usr/bin/env python3
# M2B04-reconcile_enrich.py
#
# Purpose:
# - Reconcile active BPMN processes with Archi master.xml
# - Enrich allowed metadata ONLY on existing processes
#
# GUARANTEES:
# - NO new BPMN processes are created
# - NO process IDs are modified
#   EXCEPT one explicit bootstrap case:
#     Process_Example_001 -> real Archi identifier
#     Bootstrap fires ONLY if Process_Example_001 is present in
#     an active BPMN AND exactly ONE matching Archi process exists
#     for that BPMN file's name context.
# - NO empty values are written
# - Mapping context is respected (model relevance)
#
# Stage artifacts are allowed but MUST be cleared on success

from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime
import sys


# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

ACTIVE_BPMN_DIR = ROOT_DIR / "01-model" / "01-bpmn" / "00-bpmnactive"
ARCHI_MASTER = ROOT_DIR / "02-artifacts" / "00-xml" / "00-master" / "master.xml"
MAPPING_FILE = ROOT_DIR / "02-artifacts" / "00-xml" / "01-mapping" / "M2Bmapping.txt"

ARCHIVE_DIR = ROOT_DIR / "03-stages" / "01-bpmnarchive"
LOG_DIR = ROOT_DIR / "03-stages" / "99-logs"
LOG_FILE = LOG_DIR / "M2B04-reconcile.log"

NS_BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL"
XSI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"

ET.register_namespace("bpmn", NS_BPMN)


# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------

def log(msg: str):
    ts = datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def abort(msg: str):
    log(f"[ABORT] {msg}")
    sys.exit(1)


# ----------------------------------------------------------
# Mapping Context
# ----------------------------------------------------------

def load_relevant_models():
    models = []
    with MAPPING_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "archi[model=" in line:
                ctx = line.split("archi[model=", 1)[1].split("]", 1)[0]
                models.append(ctx.replace("*", ""))
    return models


# ----------------------------------------------------------
# Guardrails
# ----------------------------------------------------------

def assert_no_new_processes(before: set, after: set, allowed_changes: list):
    """
    Prueft ob die Prozess-ID-Menge legal ist.
    allowed_changes ist eine Liste von (old_id, new_id) Tuples fuer Bootstrap-Upgrades.
    """
    before_check = set(before)
    after_check = set(after)

    for old_id, new_id in allowed_changes:
        before_check.discard(old_id)
        after_check.discard(new_id)

    if before_check != after_check:
        abort(
            f"process set changed illegally – "
            f"before={before_check} after={after_check}"
        )


def safe_write(target: ET.Element, attr: str, value: str):
    if value is None:
        return
    value = value.strip()
    if not value:
        return
    if target.get(attr) != value:
        target.set(attr, value)
        log(f"enriched {attr} -> '{value}'")


# ----------------------------------------------------------
# master.xml Archi Index
# ----------------------------------------------------------

def build_archi_index() -> dict:
    """
    Liest alle BusinessProcess-Elemente aus master.xml.
    Gibt ein dict {identifier -> {id, name, sourceModel}} zurueck.
    """
    archi_index = {}

    master_tree = ET.parse(ARCHI_MASTER)
    master_root = master_tree.getroot()

    for el in master_root.iter():
        local_tag = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if local_tag != "element":
            continue

        if el.get(XSI_TYPE) != "BusinessProcess":
            continue

        archi_id = el.get("identifier")
        if not archi_id:
            continue

        source_model = el.get("sourceModel", "")

        # Name: bevorzuge xml:lang="de", Fallback erster <n>
        name_de = None
        name_any = None
        for child in el:
            clocal = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if clocal != "name":
                continue
            text = (child.text or "").strip()
            if not text:
                continue
            lang = child.get("{http://www.w3.org/XML/1998/namespace}lang", "")
            if lang == "de" and name_de is None:
                name_de = text
            if name_any is None:
                name_any = text

        name = name_de or name_any

        archi_index[archi_id] = {
            "id": archi_id,
            "name": name,
            "sourceModel": source_model
        }

    return archi_index


# ----------------------------------------------------------
# Bootstrap: Process_Example_001 Aufloesung
# ----------------------------------------------------------

def resolve_bootstrap(process_id: str, archi_index: dict, relevant_models: list) -> str | None:
    """
    Versucht Process_Example_001 durch eine echte Archi-ID zu ersetzen.

    Strategie:
    - Suche alle Archi-Prozesse die zum Mapping-Kontext passen
    - Wenn genau 1 Kandidat: Upgrade ausfuehren
    - Wenn 0 oder > 1 Kandidaten: KEIN Upgrade, nur loggen

    NICHT mehr: globaler ABORT wenn > 1 BusinessProcess im master.xml.
    Der Bootstrap betrifft NUR den einen Placeholder-Prozess.
    """
    if process_id != "Process_Example_001":
        return None

    # Kandidaten: Archi-Prozesse die zum Mapping-Kontext passen
    if relevant_models:
        candidates = [
            a for a in archi_index.values()
            if any(m in (a.get("sourceModel") or "") for m in relevant_models)
        ]
    else:
        candidates = list(archi_index.values())

    if len(candidates) == 0:
        log("bootstrap: no matching Archi process found -> placeholder remains")
        return None

    if len(candidates) > 1:
        names = [c.get("name", c["id"]) for c in candidates]
        log(
            f"bootstrap: {len(candidates)} candidates found ({names}) -> "
            f"bootstrap ambiguous for placeholder, skipping upgrade. "
            f"Manually assign the correct Archi identifier or narrow the model filter in M2Bmapping.txt."
        )
        return None

    # Genau 1 Kandidat: sicherer Upgrade
    new_id = candidates[0]["id"]
    log(f"bootstrap: upgrading Process_Example_001 -> {new_id} ({candidates[0].get('name', '')})")
    return new_id


# ----------------------------------------------------------
# Core Logic
# ----------------------------------------------------------

def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    log("start M2B04 reconcile / enrich")

    if not ACTIVE_BPMN_DIR.exists():
        abort("active BPMN directory missing")

    if not ARCHI_MASTER.exists():
        abort("master.xml missing")

    relevant_models = load_relevant_models()
    log(f"relevant models (context): {relevant_models}")

    # --------------------------------------------------
    # Archi Index aufbauen
    # --------------------------------------------------

    archi_index = build_archi_index()
    log(f"archi business processes loaded: {len(archi_index)}")

    # --------------------------------------------------
    # Snapshot existierender BPMN Prozess-IDs (GUARD)
    # --------------------------------------------------

    process_ids_before = set()
    bpmn_files = list(ACTIVE_BPMN_DIR.glob("*.bpmn"))

    for file in bpmn_files:
        try:
            tree = ET.parse(file)
            proc = tree.getroot().find(f".//{{{NS_BPMN}}}process")
            if proc is not None:
                process_ids_before.add(proc.get("id"))
        except ET.ParseError as e:
            log(f"WARNING: cannot parse {file.name}: {e}")

    log(f"active BPMN processes before reconcile: {len(process_ids_before)}")

    # --------------------------------------------------
    # Reconcile / Enrich
    # --------------------------------------------------

    bootstrap_changes = []

    for file in bpmn_files:
        try:
            tree = ET.parse(file)
        except ET.ParseError as e:
            log(f"WARNING: cannot parse {file.name}: {e}")
            continue

        root = tree.getroot()
        proc = root.find(f".//{{{NS_BPMN}}}process")

        if proc is None:
            log(f"WARNING: no <process> element in {file.name}")
            continue

        pid = proc.get("id")
        log(f"reconcile process: {pid} ({file.name})")

        # Bootstrap: Placeholder ersetzen falls eindeutig moeglich
        if pid == "Process_Example_001":
            new_id = resolve_bootstrap(pid, archi_index, relevant_models)
            if new_id:
                proc.set("id", new_id)
                bootstrap_changes.append(("Process_Example_001", new_id))
                pid = new_id
            # Kein else-abort: Flow laeuft weiter auch ohne Bootstrap-Erfolg

        # Enrich: Metadaten aus Archi uebertragen
        if pid not in archi_index:
            log(f"no Archi match for process {pid} -> report only, no enrichment")
            tree.write(file, encoding="utf-8", xml_declaration=True)
            continue

        archi = archi_index[pid]

        # Mapping-Kontext pruefen
        if relevant_models:
            if not any(m in (archi.get("sourceModel") or "") for m in relevant_models):
                log(f"skip enrich (model not relevant): {archi.get('sourceModel')}")
                tree.write(file, encoding="utf-8", xml_declaration=True)
                continue

        safe_write(proc, "name", archi.get("name"))

        tree.write(file, encoding="utf-8", xml_declaration=True)

    # --------------------------------------------------
    # Guard: keine illegalen Prozess-Aenderungen
    # --------------------------------------------------

    process_ids_after = set()
    for file in bpmn_files:
        try:
            tree = ET.parse(file)
            proc = tree.getroot().find(f".//{{{NS_BPMN}}}process")
            if proc is not None:
                process_ids_after.add(proc.get("id"))
        except ET.ParseError:
            pass

    assert_no_new_processes(process_ids_before, process_ids_after, bootstrap_changes)

    log(f"reconcile / enrich completed successfully | bootstrap_changes={bootstrap_changes}")
    log("stage artifacts may now be cleared")


if __name__ == "__main__":
    main()
