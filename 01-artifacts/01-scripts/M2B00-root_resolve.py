#!/usr/bin/env python3
# M2B00-root_resolve.py
#
# Zweck (Flow-Stage):
# - root.cfg lesen und Root-Pfad auflösen (via HLP00_resolve_root)
# - Aufgelösten Root persistieren als:
#     <stages>\99-logs\M2B00-root.resolved.txt
# - Log schreiben nach:
#     <stages>\99-logs\M2B00-root-check.log
#
# Hinweis Fast-Path (alt):
# - Der bisherige Fast-Path via XML00-root.resolved.txt entfällt.
# - Alle Flows lesen direkt aus root.cfg via HLP00 — einheitlich.
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

SCRIPT_KUERZEL = "M2B00"
LOG_FILENAME   = "M2B00-root-check.log"
RESOLVED_FILE  = "M2B00-root.resolved.txt"


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
# Root resolved schreiben
# ----------------------------------------------------------

def write_root_resolved(logs_dir: str, root_path: str, log_path: str | None) -> str:
    """
    Schreibt M2B00-root.resolved.txt — wird von nachfolgenden
    M2B-Scripts als schneller Root-Anker gelesen.
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
    log(f"<artifacts> : {cfg.get('<artifacts>', '?')}", log_path)

    # Root resolved schreiben
    out_path = write_root_resolved(logs_dir, root_path, log_path)
    log(f"Geschrieben: {out_path}", log_path)

    print(f"[{SCRIPT_KUERZEL}] OK | Root aufgelöst -> {out_path}")


if __name__ == "__main__":
    main()
