# NBX00-validate_environment.py
# NBX-Flow – Umgebungsvalidierung
# Einzige Wirkung: root.cfg auflösen via HLP00, resolved.txt schreiben
# Prüft: HLP00 erreichbar, root.cfg vorhanden, 99-logs vorhanden,
#         nbx_config.txt (01-artifacts\02-csv\01-mapping\) vorhanden,
#         00-archimatechild vorhanden
# Output: 02-stages\99-logs\NBX00-root.resolved.txt
# Folge:  NBX01
# Stage:  S1.02

import os
import sys
from datetime import datetime

# HLP00 direkt importieren (Blueprint-Standard)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HLP00_resolve_root import get_root_cfg

# ─── Konstanten ───────────────────────────────────────────────────────────────

SCRIPT_NAME  = "NBX00-validate_environment"
LOG_FILENAME = "NBX00-validate_environment.log"
OUT_FILENAME = "NBX00-root.resolved.txt"

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
        print(f"[FEHLER] root.cfg konnte nicht aufgeloest werden: {e}")
        sys.exit(1)

    stages_dir    = cfg["<stages>"]
    artifacts_dir = cfg["<artifacts>"]
    logs_dir      = os.path.join(stages_dir, "99-logs")

    # Log-Ordner muss vorhanden sein (wird nicht angelegt — GOV)
    if not os.path.isdir(logs_dir):
        print(f"[FEHLER] Log-Ordner nicht gefunden: {logs_dir}")
        print("         Bitte Ordnerstruktur pruefen (structure.txt).")
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

    # 3) nbx_config.txt prüfen (01-artifacts\02-csv\01-mapping\)
    nbx_config_path = os.path.join(artifacts_dir, "02-csv", "01-mapping", "nbx_config.txt")
    log(f"Pruefe nbx_config.txt: {nbx_config_path}", log_path)
    if not os.path.isfile(nbx_config_path):
        msg = f"[FEHLER] nbx_config.txt nicht gefunden: {nbx_config_path}"
        log(msg, log_path)
        log("         Bitte nbx_config.txt anlegen (Vorlage: NBX-Skill)", log_path)
        fehler.append(msg)
    else:
        log("  OK", log_path)

    # 4) 00-archimatechild prüfen (Zielordner für nbx_trash.csv)
    child_dir = os.path.join(artifacts_dir, "02-csv", "03-child", "00-archimatechild")
    log(f"Pruefe 00-archimatechild: {child_dir}", log_path)
    if not os.path.isdir(child_dir):
        msg = f"[FEHLER] 00-archimatechild nicht gefunden: {child_dir}"
        log(msg, log_path)
        fehler.append(msg)
    else:
        log("  OK", log_path)

    # 5) 02-stages prüfen (Zwischenartefakte)
    log(f"Pruefe 02-stages: {stages_dir}", log_path)
    if not os.path.isdir(stages_dir):
        msg = f"[FEHLER] 02-stages nicht gefunden: {stages_dir}"
        log(msg, log_path)
        fehler.append(msg)
    else:
        log("  OK", log_path)

    # 6) resolved.txt schreiben
    log(f"Schreibe Output: {out_path}", log_path)
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("# NBX00-root.resolved.txt\n")
            f.write(f"# Erstellt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Zweck: Aufgeloeste Pfade fuer NBX-Flow\n\n")
            for key, val in cfg.items():
                f.write(f"{key}={val}\n")
            f.write(f"\n<nbxconfig>={nbx_config_path}\n")
            f.write(f"<childdir>={child_dir}\n")
        log(f"Output geschrieben: {out_path}", log_path)
    except Exception as e:
        msg = f"[FEHLER] Output konnte nicht geschrieben werden: {e}"
        log(msg, log_path)
        fehler.append(msg)

    # 7) Abschluss
    log("=" * 60, log_path)
    if fehler:
        log(f"ABSCHLUSS: {len(fehler)} Fehler — NBX-Flow nicht startbereit", log_path)
        for f in fehler:
            log(f"  {f}", log_path)
        log("=" * 60, log_path)
        sys.exit(1)
    else:
        log("ABSCHLUSS: Alle Pruefungen bestanden — NBX01 startbereit", log_path)
        log("=" * 60, log_path)
        sys.exit(0)


if __name__ == "__main__":
    main()
