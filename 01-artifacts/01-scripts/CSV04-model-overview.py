#!/usr/bin/env python3
# CSV04-model_overview.py
#
# Purpose:
# - Provide a flat, factual inventory of all existing model realities
# - Each artifact is written as its own SOURCE / MODEL entry
# - No mapping, no interpretation, no assumptions
#
# Output:
# - <rootfolder>/02-stages/run-scope.txt (extended, not interpreted)
# - <rootfolder>/02-stages/99-logs/CSV04-model_overview.log
#
# Rules:
# - Read-only
# - No directory creation
# - No resolution logic
# - Context only

import os
import sys
from datetime import datetime


def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str, log_path: str):
    line = f"[CSV04] {now_ts()} | {message}"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def die(message: str, log_path: str):
    log(f"ERROR | {message}", log_path)
    sys.exit(1)


def read_root(script_dir: str) -> str:
    path = os.path.join(
        script_dir, "..", "..", "02-stages", "99-logs", "CSV00-root.resolved.txt"
    )
    path = os.path.abspath(path)

    if not os.path.isfile(path):
        die(f"Missing root resolution file: {path}", path)

    with open(path, "r", encoding="utf-8") as f:
        root = f.readline().strip()

    if not root or not os.path.isdir(root):
        die(f"Invalid root path: {root}", path)

    return root


def read_scope_models(scope_path: str) -> list[str]:
    """
    Liest SOURCE=archi / MODEL= Paare aus run-scope.txt.
    Nur Einträge mit Endung .archimate werden übernommen —
    .bak, log-0.txt und andere Archi-interne Dateien werden ignoriert.
    """
    models = []
    current_source = None
    with open(scope_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("SOURCE="):
                current_source = line.split("=", 1)[1].strip().lower()
            elif line.startswith("MODEL="):
                model = line.split("=", 1)[1].strip()
                if current_source == "archi":
                    # Nur .archimate Dateien — keine .bak, log-0.txt etc.
                    if model.lower().endswith(".archimate"):
                        models.append(model)
    return models


def list_files(directory: str, extensions: tuple = ()) -> list[str]:
    """
    Listet Dateien in einem Ordner.
    extensions: Tuple von erlaubten Endungen z.B. (".xml",)
    Leeres Tuple = alle Dateien (kein Filter).
    """
    if not os.path.isdir(directory):
        return []
    result = []
    for f in sorted(os.listdir(directory)):
        if not os.path.isfile(os.path.join(directory, f)):
            continue
        if extensions and not f.lower().endswith(extensions):
            continue
        result.append(f)
    return result


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root = read_root(script_dir)

    stages_dir = os.path.join(root, "02-stages")
    logs_dir = os.path.join(stages_dir, "99-logs")
    scope_path = os.path.join(stages_dir, "run-scope.txt")

    log_path = os.path.join(logs_dir, "CSV04-model_overview.log")
    log(f"Resolved root path: {root}", log_path)

    if not os.path.isfile(scope_path):
        die(f"Missing run-scope.txt: {scope_path}", log_path)

    entries = []

    # --- Archi models from scope ---
    archi_models = read_scope_models(scope_path)
    for model in archi_models:
        entries.append(("archi", model))
        log(f"Found Archi model: {model}", log_path)

    # --- OEF artifacts (nur .xml — .xsd Schemadateien werden ignoriert) ---
    oef_dir = os.path.join(root, "01-artifacts", "00-xml", "03-child", "00-archimatechild")
    for f in list_files(oef_dir, extensions=(".xml",)):
        entries.append(("OEF", f))
        log(f"Found OEF artifact: {f}", log_path)

    # --- XLSX artifacts (nur .xlsx) ---
    xlsx_dir = os.path.join(root, "01-artifacts", "03-XLSX", "03-child", "00-archimatechild")
    for f in list_files(xlsx_dir, extensions=(".xlsx",)):
        entries.append(("XLSX", f))
        log(f"Found XLSX artifact: {f}", log_path)

    # --- CSV artifacts (nur .csv) ---
    csv_dir = os.path.join(root, "01-artifacts", "02-csv", "03-child", "00-archimatechild")
    for f in list_files(csv_dir, extensions=(".csv",)):
        entries.append(("CSV", f))
        log(f"Found CSV artifact: {f}", log_path)

    # --- Write flat inventory ---
    try:
        with open(scope_path, "w", encoding="utf-8") as f:
            for source, model in entries:
                f.write(f"SOURCE={source}\n")
                f.write(f"MODEL={model}\n\n")
    except Exception as e:
        die(f"Failed to write run-scope.txt: {e}", log_path)

    log("Flat source inventory written to run-scope.txt", log_path)
    print("[CSV04] OK | flat model overview completed")


if __name__ == "__main__":
    main()
