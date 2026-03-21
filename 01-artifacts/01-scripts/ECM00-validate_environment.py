# ECM00-validate_environment.py
# EasyCSVMapper – Umgebungsvalidierung
# Prüft alle Voraussetzungen für den ECM-Flow:
#   - root.cfg auflösbar via HLP00
#   - 99-mappingmodel\ vorhanden
#   - 00-archimatearchive\ vorhanden (Output-Ordner für ECM01)
#   - 00-archimatechild\ vorhanden + mind. eine trash_*.csv drin
# Output: ECM00-root.resolved.txt in 02-stages\99-logs\
# Hinweis: run-scope.txt und OEF Modelle werden erst ab ECM02 benötigt

import os
import sys
from datetime import datetime

# HLP00 direkt importieren (Blueprint-Standard)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HLP00_resolve_root import get_root_cfg

# ─── Konstanten ───────────────────────────────────────────────────────────────

SCRIPT_NAME  = "ECM00-validate_environment"
LOG_FILENAME = "ECM00-validate_environment.log"
OUT_FILENAME = "ECM00-root.resolved.txt"

# ─── Logging ──────────────────────────────────────────────────────────────────

def log(msg, log_path):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ─── Hauptlogik ───────────────────────────────────────────────────────────────

def main():

    # 1) root.cfg auflösen
    try:
        cfg = get_root_cfg()
    except Exception as e:
        print(f"[FEHLER] root.cfg konnte nicht aufgelöst werden: {e}")
        sys.exit(1)

    models_dir    = cfg["<models>"]
    artifacts_dir = cfg["<artifacts>"]
    stages_dir    = cfg["<stages>"]
    logs_dir      = os.path.join(stages_dir, "99-logs")

    # Log-Ordner muss vorhanden sein (wird nicht angelegt — fix per GOV)
    if not os.path.isdir(logs_dir):
        print(f"[FEHLER] Log-Ordner nicht gefunden: {logs_dir}")
        print("         Bitte Ordnerstruktur prüfen (structure.txt).")
        sys.exit(1)

    log_path = os.path.join(logs_dir, LOG_FILENAME)
    out_path = os.path.join(logs_dir, OUT_FILENAME)

    log("=" * 60, log_path)
    log(f"START {SCRIPT_NAME}", log_path)
    log("=" * 60, log_path)

    fehler = []

    # 2) root.cfg Pfade protokollieren
    log("root.cfg aufgeloest:", log_path)
    for key, val in cfg.items():
        log(f"  {key} = {val}", log_path)

    # 3) Pfade ableiten
    mapping_model_dir = os.path.join(models_dir,    "00-archimate", "99-mappingmodel")
    archive_dir       = os.path.join(stages_dir,    "00-archimatearchive")
    child_dir         = os.path.join(artifacts_dir, "02-csv", "03-child", "00-archimatechild")

    # 4) 99-mappingmodel\ prüfen
    log(f"Pruefe 99-mappingmodel: {mapping_model_dir}", log_path)
    if not os.path.isdir(mapping_model_dir):
        msg = f"[FEHLER] 99-mappingmodel nicht gefunden: {mapping_model_dir}"
        log(msg, log_path)
        fehler.append(msg)
    else:
        log("  OK", log_path)

    # 5) 00-archimatearchive\ prüfen (ECM01 Output-Ordner)
    log(f"Pruefe 00-archimatearchive: {archive_dir}", log_path)
    if not os.path.isdir(archive_dir):
        msg = f"[FEHLER] 00-archimatearchive nicht gefunden: {archive_dir}"
        log(msg, log_path)
        fehler.append(msg)
    else:
        log("  OK", log_path)

    # 6) 00-archimatechild\ prüfen + trash_*.csv suchen
    log(f"Pruefe 00-archimatechild: {child_dir}", log_path)
    if not os.path.isdir(child_dir):
        msg = f"[FEHLER] 00-archimatechild nicht gefunden: {child_dir}"
        log(msg, log_path)
        fehler.append(msg)
    else:
        trash_files = [
            f for f in os.listdir(child_dir)
            if f.lower().startswith("trash_") and f.lower().endswith(".csv")
        ]
        if not trash_files:
            log("  [WARNUNG] Keine trash_*.csv Dateien gefunden", log_path)
            log("            Bitte Muell-CSV als trash_<name>.csv ablegen", log_path)
        else:
            log(f"  trash_*.csv gefunden: {len(trash_files)}", log_path)
            for f in trash_files:
                log(f"    {f}", log_path)

    # 7) Output schreiben
    log(f"Schreibe Output: {out_path}", log_path)
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("# ECM00-root.resolved.txt\n")
            f.write(f"# Erstellt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Zweck: Aufgeloeste Pfade fuer ECM-Flow\n\n")
            for key, val in cfg.items():
                f.write(f"{key}={val}\n")
            f.write(f"\n<mappingmodel>={mapping_model_dir}\n")
            f.write(f"<archive>={archive_dir}\n")
            f.write(f"<childdir>={child_dir}\n")
        log(f"Output geschrieben: {out_path}", log_path)
    except Exception as e:
        msg = f"[FEHLER] Output konnte nicht geschrieben werden: {e}"
        log(msg, log_path)
        fehler.append(msg)

    # 8) Abschluss
    log("=" * 60, log_path)
    if fehler:
        log(f"ABSCHLUSS: {len(fehler)} Fehler — ECM-Flow nicht startbereit", log_path)
        for f in fehler:
            log(f"  {f}", log_path)
        log("=" * 60, log_path)
        sys.exit(1)
    else:
        log("ABSCHLUSS: Alle Pruefungen bestanden — ECM01 startbereit", log_path)
        log("=" * 60, log_path)
        sys.exit(0)


if __name__ == "__main__":
    main()
