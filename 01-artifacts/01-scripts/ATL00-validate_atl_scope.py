#!/usr/bin/env python3
# ATL00-validate_atl_scope.py
#
# Zweck (Flow-Stage):
# - root.cfg lesen und Root-Pfad auflösen (via HLP00_resolve_root)
# - run-scope.txt lesen und SOURCE=ATL Pairs extrahieren
# - master.xml auf Existenz und Lesbarkeit prüfen
# - Ausgabe-Ordner prüfen:
#     <stages>\00-archimatearchive\
#     <stages>\99-logs\
# - Aufgelösten Root persistieren als:
#     <stages>\99-logs\ATL00-root.resolved.txt
# - Log schreiben nach:
#     <stages>\99-logs\ATL00-validate_atl_scope.log
#
# Regeln:
# - Keine Abhängigkeit zu anderen Flow-Stages
# - Deterministisch, audit-freundlich
# - Abbruch bei Fehler (hard fail)
# - Kein Schreiben außerhalb von <stages>\99-logs\
# - Basis: HLP00_resolve_root | Cleaning Run 5.5 | Stage 5

import os
import sys
from datetime import datetime
from HLP00_resolve_root import get_root_cfg


# ----------------------------------------------------------
# Konstanten
# ----------------------------------------------------------

SCRIPT_KUERZEL = "ATL00"
LOG_FILENAME   = "ATL00-validate_atl_scope.log"
RESOLVED_FILE  = "ATL00-root.resolved.txt"
SOURCE_TYPE    = "ATL"

# Pflichtordner relativ zu <stages>
REQUIRED_STAGE_DIRS = [
    "00-archimatearchive",
    "99-logs",
]

# master.xml relativ zu <artifacts>
MASTER_XML_REL = os.path.join("00-xml", "00-master", "master.xml")

# run-scope.txt relativ zu <stages>
RUN_SCOPE_REL  = "run-scope.txt"


# ----------------------------------------------------------
# Hilfsfunktionen
# ----------------------------------------------------------

def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str, log_path: str | None = None) -> None:
    line = f"[{SCRIPT_KUERZEL}] {now_ts()} | {message}"
    print(line)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass


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


# ----------------------------------------------------------
# run-scope.txt lesen
# ----------------------------------------------------------

def read_atl_scope(run_scope_path: str, log_path: str | None) -> list[str]:
    """
    Liest alle aktiven SOURCE=ATL / MODEL= Pairs aus run-scope.txt.

    Pair-Regel:
      SOURCE=ATL     <- Zeile N
      MODEL=<name>   <- Zeile N+1, direkt darunter

    Kommentierte Zeilen (#) und SNAPSHOT-Zeilen werden ignoriert.
    Rückgabe: Liste der MODEL-Werte für SOURCE=ATL.
    """
    if not os.path.isfile(run_scope_path):
        die(f"run-scope.txt nicht gefunden: {run_scope_path}", log_path)

    active_lines = []
    with open(run_scope_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.upper().startswith("SNAPSHOT_"):
                continue
            active_lines.append(stripped)

    models = []
    i = 0
    while i < len(active_lines):
        if active_lines[i].upper().startswith("SOURCE="):
            source = active_lines[i].split("=", 1)[1].strip().upper()
            if (
                i + 1 < len(active_lines)
                and active_lines[i + 1].upper().startswith("MODEL=")
            ):
                model = active_lines[i + 1].split("=", 1)[1].strip()
                if source == SOURCE_TYPE:
                    models.append(model)
                    log(f"ATL Scope gefunden: MODEL={model}", log_path)
                i += 2
                continue
        i += 1

    return models


# ----------------------------------------------------------
# Prüfungen
# ----------------------------------------------------------

def check_master_xml(artifacts_dir: str, log_path: str | None) -> str:
    """Prüft ob master.xml existiert und lesbar ist."""
    master_xml = os.path.join(artifacts_dir, MASTER_XML_REL)
    if not os.path.isfile(master_xml):
        die(f"master.xml nicht gefunden: {master_xml}", log_path)
    try:
        with open(master_xml, "r", encoding="utf-8") as f:
            f.read(1)
    except Exception as e:
        die(f"master.xml nicht lesbar: {e}", log_path)
    log(f"master.xml OK: {master_xml}", log_path)
    return master_xml


def check_required_dirs(stages_dir: str, log_path: str | None) -> None:
    """
    Prüft ob alle erforderlichen Unterordner in <stages> vorhanden sind.
    Legt nichts an — bei fehlendem Ordner Abbruch mit Hinweis.
    """
    for sub in REQUIRED_STAGE_DIRS:
        full = os.path.join(stages_dir, sub)
        if not os.path.isdir(full):
            die(
                f"Erforderlicher Ordner fehlt: {full}\n"
                f"  → Bitte Ordner manuell anlegen: <stages>\\{sub}",
                log_path,
            )
        log(f"Ordner OK: {full}", log_path)


# ----------------------------------------------------------
# Root resolved schreiben
# ----------------------------------------------------------

def write_root_resolved(logs_dir: str, root_path: str, log_path: str | None) -> str:
    """Schreibt ATL00-root.resolved.txt — analog zu CSV00/XML00/M2B00."""
    out_path = os.path.join(logs_dir, RESOLVED_FILE)
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(root_path.rstrip() + "\n")
    except Exception as e:
        die(f"Kann {RESOLVED_FILE} nicht schreiben: {e}", log_path)
    return out_path


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main() -> None:
    # root.cfg lesen — HLP00 übernimmt Auflösung und Fehlerbehandlung
    cfg = get_root_cfg()

    root_path     = cfg["<rootfolder>"]
    stages_dir    = cfg["<stages>"]
    artifacts_dir = cfg["<artifacts>"]
    logs_dir      = os.path.join(stages_dir, "99-logs")

    # Logs-Ordner muss vorhanden sein (wird nicht angelegt)
    if not os.path.isdir(logs_dir):
        print(
            f"[{SCRIPT_KUERZEL}] ERROR | Logs-Ordner fehlt: {logs_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    log_path = os.path.join(logs_dir, LOG_FILENAME)

    log(f"root.cfg gelesen — Root: {root_path}", log_path)
    log(f"<stages>    : {stages_dir}", log_path)
    log(f"<artifacts> : {artifacts_dir}", log_path)

    # run-scope.txt lesen
    run_scope_path = os.path.join(stages_dir, RUN_SCOPE_REL)
    log(f"Lese run-scope.txt: {run_scope_path}", log_path)
    atl_models = read_atl_scope(run_scope_path, log_path)

    if not atl_models:
        die(
            "Kein aktives SOURCE=ATL / MODEL= Pair in run-scope.txt gefunden.\n"
            "  → Bitte run-scope.txt prüfen und SOURCE=ATL + MODEL=<name> eintragen.",
            log_path,
        )

    log(f"ATL Scope: {len(atl_models)} Modell(e) aktiv: {atl_models}", log_path)

    # master.xml prüfen
    check_master_xml(artifacts_dir, log_path)

    # Pflichtordner prüfen
    check_required_dirs(stages_dir, log_path)

    # Root resolved schreiben
    out_path = write_root_resolved(logs_dir, root_path, log_path)
    log(f"Geschrieben: {out_path}", log_path)

    # Zusammenfassung
    log("─" * 60, log_path)
    log("ATL00 ERFOLGREICH", log_path)
    log(f"  Root       : {root_path}", log_path)
    log(f"  ATL Modelle: {atl_models}", log_path)
    log(f"  master.xml : OK", log_path)
    log(f"  Ordner     : OK", log_path)
    log("─" * 60, log_path)

    print(f"[{SCRIPT_KUERZEL}] OK | ATL Scope validiert -> {len(atl_models)} Modell(e) aktiv")


if __name__ == "__main__":
    main()
