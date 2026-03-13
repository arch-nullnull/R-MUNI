#!/usr/bin/env python3
# CSV00-validate_environment.py
#
# Zweck (Flow-Stage):
# - root.cfg lesen und Umgebung validieren (via HLP00_resolve_root)
# - Grundvoraussetzungen des CSV Flow prüfen
# - Aufgelösten Root persistieren als:
#     <stages>\99-logs\CSV00-root.resolved.txt
# - Log schreiben nach:
#     <stages>\99-logs\CSV00-validate_environment.log
#
# Regeln:
# - Keine Abhängigkeit zu anderen Flow-Stages
# - Deterministisch, audit-freundlich
# - Abbruch bei Fehler (hard fail)
# - Basis: HLP00_resolve_root | Cleaning Run 5.5 | Stage 5

import os
import sys
from datetime import datetime
from HLP00_resolve_root import get_root_cfg


# ----------------------------------------------------------
# Konstanten
# ----------------------------------------------------------

SCRIPT_KUERZEL = "CSV00"
LOG_FILENAME   = "CSV00-validate_environment.log"
RESOLVED_FILE  = "CSV00-root.resolved.txt"


# ----------------------------------------------------------
# Hilfsfunktionen
# ----------------------------------------------------------

def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str, log_path: str | None = None) -> None:
    line = f"[{SCRIPT_KUERZEL}] {now_ts()} | {message}"
    print(line)
    if log_path:
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


# ----------------------------------------------------------
# Prüfungen
# ----------------------------------------------------------

def check_required_dirs(cfg: dict, log_path: str | None) -> None:
    """
    Prüft ob alle Blueprint-Pflichtordner vorhanden sind.
    Legt nichts an — bei fehlendem Ordner Abbruch mit Hinweis.
    """
    pflicht = ["<models>", "<artifacts>", "<stages>"]
    for key in pflicht:
        path = cfg.get(key, "")
        if not path:
            die(f"Variable {key} fehlt in root.cfg", log_path)
        if not os.path.isdir(path):
            die(
                f"Pflichtordner fehlt: {path}\n"
                f"  → Bitte Ordner prüfen oder umbenennen: {key}",
                log_path,
            )
        log(f"Ordner OK: {key} = {path}", log_path)


# ----------------------------------------------------------
# Root resolved schreiben
# ----------------------------------------------------------

def write_root_resolved(logs_dir: str, root_path: str, log_path: str | None) -> str:
    """
    Schreibt CSV00-root.resolved.txt — wird von nachfolgenden
    CSV-Scripts als schneller Root-Anker gelesen.
    """
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

    root_path  = cfg["<rootfolder>"]
    stages_dir = cfg["<stages>"]
    logs_dir   = os.path.join(stages_dir, "99-logs")

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
    log(f"<models>    : {cfg.get('<models>', '?')}", log_path)
    log(f"<artifacts> : {cfg.get('<artifacts>', '?')}", log_path)

    # Pflichtordner prüfen
    check_required_dirs(cfg, log_path)

    # Root resolved schreiben
    out_path = write_root_resolved(logs_dir, root_path, log_path)
    log(f"Geschrieben: {out_path}", log_path)

    print(f"[{SCRIPT_KUERZEL}] OK | Umgebung validiert -> {out_path}")


if __name__ == "__main__":
    main()
