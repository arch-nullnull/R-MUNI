#!/usr/bin/env python3
# ATL00-validate_atl_scope.py
#
# Zweck (Flow-Stage):
# - Root-Pfad auflösen (identisch zu CSV00 / XML00 / M2B00)
# - run-scope.txt lesen und SOURCE=ATL Pairs extrahieren
# - master.xml auf Existenz und Lesbarkeit prüfen
# - Ausgabe-Ordner prüfen:
#     <rootfolder>/03-stages/00-archimatearchive/
#     <rootfolder>/02-artifacts/05-reports/00-archimate/99-ATL/
# - Aufgelösten Root persistieren als:
#     <rootfolder>/03-stages/99-logs/ATL00-root.resolved.txt
# - Log schreiben nach:
#     <rootfolder>/03-stages/99-logs/ATL00-validate_atl_scope.log
#
# Regeln:
# - Keine Abhängigkeit zu anderen Stages
# - Deterministisch, audit-freundlich
# - Abbruch bei Fehler (hard fail)
# - Kein Schreiben außerhalb von 03-stages/99-logs/

import os
import sys
from datetime import datetime


# ----------------------------------------------------------
# Konstanten
# ----------------------------------------------------------

SCRIPT_KUERZEL = "ATL00"
LOG_FILENAME   = "ATL00-validate_atl_scope.log"
ROOT_RESOLVED  = "ATL00-root.resolved.txt"
SOURCE_TYPE    = "ATL"

MASTER_XML_REL = os.path.join(
    "02-artifacts", "00-xml", "00-master", "master.xml"
)
RUN_SCOPE_REL  = os.path.join("03-stages", "run-scope.txt")

# Ausgabe-Ordner die geprüft werden müssen
REQUIRED_DIRS = [
    os.path.join("03-stages", "00-archimatearchive"),
    os.path.join("03-stages", "99-logs"),
]


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
# Root auflösen
# ----------------------------------------------------------

def find_root_txt(script_dir: str) -> str:
    """
    Erwartet root.txt zwei Ebenen über dem Script-Ordner.
    Pfad: <rootfolder>/root.txt
    Script liegt in: <rootfolder>/02-artifacts/01-scripts/
    """
    return os.path.abspath(
        os.path.join(script_dir, "..", "..", "root.txt")
    )


def read_blueprint_root(root_txt_path: str, log_path: str | None) -> str:
    """Liest BLUEPRINT_ROOT aus root.txt."""
    try:
        with open(root_txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        die(f"root.txt nicht lesbar: {e}", log_path)

    root_value = None
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("BLUEPRINT_ROOT="):
            if root_value is not None:
                die("Mehrfacher BLUEPRINT_ROOT Eintrag in root.txt", log_path)
            root_value = stripped.split("=", 1)[1].strip()

    if not root_value:
        die("Kein BLUEPRINT_ROOT Eintrag in root.txt gefunden", log_path)

    return root_value


def resolve_root_path(
    root_txt_path: str, root_value: str, log_path: str | None
) -> str:
    """Löst relativen oder absoluten Root-Pfad auf."""
    if os.path.isabs(root_value):
        root_path = root_value
        log("BLUEPRINT_ROOT ist absolut", log_path)
    else:
        root_path = os.path.abspath(
            os.path.join(os.path.dirname(root_txt_path), root_value)
        )
        log("BLUEPRINT_ROOT ist relativ — aufgelöst gegen root.txt", log_path)

    if not os.path.isdir(root_path):
        die(
            f"Aufgelöster Root-Pfad existiert nicht oder ist kein Ordner: {root_path}",
            log_path,
        )
    return root_path


# ----------------------------------------------------------
# run-scope.txt lesen
# ----------------------------------------------------------

def read_atl_scope(run_scope_path: str, log_path: str | None) -> list[str]:
    """
    Liest alle aktiven SOURCE=ATL / MODEL= Pairs aus run-scope.txt.

    Pair-Regel (identisch zu allen anderen Flows):
      SOURCE=ATL     <- Zeile N
      MODEL=<name>   <- Zeile N+1, direkt darunter, kein Abstand

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

def check_master_xml(root_path: str, log_path: str | None) -> str:
    """Prüft ob master.xml existiert und lesbar ist."""
    master_xml = os.path.join(root_path, MASTER_XML_REL)
    if not os.path.isfile(master_xml):
        die(f"master.xml nicht gefunden: {master_xml}", log_path)
    try:
        with open(master_xml, "r", encoding="utf-8") as f:
            f.read(1)
    except Exception as e:
        die(f"master.xml nicht lesbar: {e}", log_path)
    log(f"master.xml OK: {master_xml}", log_path)
    return master_xml


def check_required_dirs(root_path: str, log_path: str | None) -> None:
    """
    Prüft ob alle erforderlichen Ausgabe-Ordner existieren.
    Legt NICHTS an — bei fehlendem Ordner Abbruch mit Hinweis.
    """
    for rel in REQUIRED_DIRS:
        full = os.path.join(root_path, rel)
        if not os.path.isdir(full):
            die(
                f"Erforderlicher Ordner fehlt: {full}\n"
                f"  → Bitte Ordner manuell anlegen: {rel}",
                log_path,
            )
        log(f"Ordner OK: {full}", log_path)


# ----------------------------------------------------------
# Root resolved schreiben
# ----------------------------------------------------------

def write_root_resolved(logs_dir: str, root_path: str, log_path: str | None) -> str:
    """Schreibt ATL00-root.resolved.txt — analog zu CSV00/XML00/M2B00."""
    out_path = os.path.join(logs_dir, ROOT_RESOLVED)
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(root_path.rstrip() + "\n")
    except Exception as e:
        die(f"Kann ATL00-root.resolved.txt nicht schreiben: {e}", log_path)
    return out_path


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main() -> None:
    sdir        = os.path.dirname(os.path.abspath(__file__))
    root_txt    = find_root_txt(sdir)

    # Frühe Prüfung ohne Log-Pfad
    if not os.path.isfile(root_txt):
        die(f"root.txt nicht gefunden: {root_txt}", None)

    root_value  = read_blueprint_root(root_txt, None)
    root_path   = resolve_root_path(root_txt, root_value, None)

    # Logs-Ordner und Log-Pfad aufbauen
    logs_dir    = os.path.join(root_path, "03-stages", "99-logs")
    if not os.path.isdir(logs_dir):
        die(f"Logs-Ordner fehlt: {logs_dir}", None)
    log_path    = os.path.join(logs_dir, LOG_FILENAME)

    # Ab hier mit Log
    log(f"root.txt: {root_txt}", log_path)
    log(f"BLUEPRINT_ROOT (raw): {root_value}", log_path)
    log(f"Root-Pfad aufgelöst: {root_path}", log_path)

    # run-scope.txt lesen
    run_scope_path = os.path.join(root_path, RUN_SCOPE_REL)
    log(f"Lese run-scope.txt: {run_scope_path}", log_path)
    atl_models = read_atl_scope(run_scope_path, log_path)

    if not atl_models:
        die(
            "Kein aktives SOURCE=ATL / MODEL= Pair in run-scope.txt gefunden.\n"
            "  → Bitte run-scope.txt prüfen und SOURCE=ATL + MODEL=<name>.xml eintragen.",
            log_path,
        )

    log(f"ATL Scope: {len(atl_models)} Modell(e) aktiv: {atl_models}", log_path)

    # master.xml prüfen
    check_master_xml(root_path, log_path)

    # Ausgabe-Ordner prüfen
    check_required_dirs(root_path, log_path)

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

    print(f"[ATL00] OK | ATL Scope validiert -> {len(atl_models)} Modell(e) aktiv")


if __name__ == "__main__":
    main()
