#!/usr/bin/env python3
# CSV01-validate_model.py
#
# Zweck (Flow-Stage):
# - ArchiMate Modellstruktur im Blueprint prüfen
# - Verfügbare Modelle als Kontext-Artefakt persistieren
# - Ausgabe:
#     <stages>\model-scope.txt
#     <stages>\99-logs\CSV01-validate_model.log
#
# Regeln:
# - Nur lesend — keine Modell-Daten verändern
# - Kein mkdir
# - Abbruch nur bei technischen Fehlern
# - Cleaning Run 5.5 | Stage 5

import os
import sys
from datetime import datetime


# ----------------------------------------------------------
# Konstanten
# ----------------------------------------------------------

SCRIPT_KUERZEL = "CSV01"
LOG_FILENAME   = "CSV01-validate_model.log"


# ----------------------------------------------------------
# Hilfsfunktionen
# ----------------------------------------------------------

def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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


def log(message: str, log_path: str | None = None) -> None:
    line = f"[{SCRIPT_KUERZEL}] {now_ts()} | {message}"
    if log_path:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


# ----------------------------------------------------------
# Root aus CSV00-Artefakt lesen
# ----------------------------------------------------------

def read_root_resolved(script_dir: str) -> str:
    path = os.path.abspath(
        os.path.join(script_dir, "..", "..", "02-stages", "99-logs", "CSV00-root.resolved.txt")
    )
    if not os.path.isfile(path):
        die(f"CSV00-root.resolved.txt fehlt: {path}", None)
    try:
        with open(path, "r", encoding="utf-8") as f:
            root = f.readline().strip()
    except Exception as e:
        die(f"CSV00-root.resolved.txt nicht lesbar: {e}", None)
    if not root or not os.path.isdir(root):
        die(f"Ungültiger Root-Pfad in CSV00-root.resolved.txt: {root}", None)
    return root


# ----------------------------------------------------------
# Hauptlogik
# ----------------------------------------------------------

def classify_archimate_file(filename: str) -> str:
    name = filename.lower()
    if name.endswith(".archimate"):
        return "ARCHIMATE"
    if name.endswith(".bak"):
        return "BACKUP"
    return "OTHER"


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_path  = read_root_resolved(script_dir)

    stages_dir = os.path.join(root_path, "02-stages")
    logs_dir   = os.path.join(stages_dir, "99-logs")

    if not os.path.isdir(stages_dir):
        die(f"Stages-Ordner fehlt: {stages_dir}", None)
    if not os.path.isdir(logs_dir):
        die(f"Logs-Ordner fehlt: {logs_dir}", None)

    log_path = os.path.join(logs_dir, LOG_FILENAME)
    log(f"Root: {root_path}", log_path)

    archimate_root = os.path.join(root_path, "00-model", "00-archimate")
    log(f"Scanne ArchiMate Root: {archimate_root}", log_path)

    active_models     = []
    active_sub_models = []
    other_files       = []

    if os.path.isdir(archimate_root):
        for folder in sorted(os.listdir(archimate_root)):
            folder_path = os.path.join(archimate_root, folder)
            if not os.path.isdir(folder_path):
                continue
            log(f"Ordner: {folder}", log_path)
            for fname in sorted(os.listdir(folder_path)):
                fpath = os.path.join(folder_path, fname)
                if not os.path.isfile(fpath):
                    continue
                classification = classify_archimate_file(fname)
                if folder == "00-archimateactive" and classification == "ARCHIMATE":
                    active_models.append(fname)
                elif folder == "01-archimateactivesub" and classification == "ARCHIMATE":
                    active_sub_models.append(fname)
                else:
                    other_files.append(f"{folder}/{fname}")
                log(f"  - {fname} [{classification}]", log_path)
    else:
        log("INFO: ArchiMate Root-Ordner nicht gefunden", log_path)

    out_path = os.path.join(stages_dir, "model-scope.txt")
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("ACTIVE_MODELS:\n")
            for m in active_models:
                f.write(f"- {m}\n")
            f.write("\n")
            f.write("ACTIVE_SUB_MODELS:\n")
            for m in active_sub_models:
                f.write(f"- {m}\n")
            f.write("\n")
            f.write("OTHER_ARCHIMATE_FILES:\n")
            for m in other_files:
                f.write(f"- {m}\n")
            f.write("\n")
    except Exception as e:
        die(f"Kann model-scope.txt nicht schreiben: {e}", log_path)

    log(f"model-scope.txt geschrieben: {out_path}", log_path)
    print(f"[{SCRIPT_KUERZEL}] OK | Modell-Kontext gesammelt -> {out_path}")


if __name__ == "__main__":
    main()
