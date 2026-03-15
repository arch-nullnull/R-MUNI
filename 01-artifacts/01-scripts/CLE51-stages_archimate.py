#!/usr/bin/env python3
# CLE51-stages_archimate.py
#
# Zweck:
# - Ordnerinhalt löschen (Ordner selbst bleibt erhalten)
# - Ziele:
#   02-stages\00-archimatearchive
#
# Ablageort  : <rootfolder>\01-artifacts\01-scripts\CLE51-stages_archimate.py
# Referenz   : HLP03_clean.py | CLE00-resolve_root.py
# Stage 5 | Cleaning Run 5.5

import os
import sys
import shutil
from datetime import datetime

# ----------------------------------------------------------
# Konstanten
# ----------------------------------------------------------

SCRIPT_KUERZEL = "CLE51"
LOG_FILENAME   = "CLE51-stages_archimate.log"

# Ziel-Ordner relativ zu <stages>
ZIEL_LISTE = [
    os.path.join('00-archimatearchive'),
]


# ----------------------------------------------------------
# Hilfsfunktionen
# ----------------------------------------------------------

def _now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _log(message: str, log_path: str | None = None) -> None:
    line = f"[{SCRIPT_KUERZEL}] {_now_ts()} | {message}"
    print(line)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass


def _die(message: str, log_path: str | None = None) -> None:
    line = f"[{SCRIPT_KUERZEL}] {_now_ts()} | ERROR | {message}"
    print(line, file=sys.stderr)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    sys.exit(1)


# ----------------------------------------------------------
# root.cfg auflösen (inline — keine Abhängigkeit zu CLE00)
# ----------------------------------------------------------

def _resolve_root() -> dict:
    """Liest root.cfg und gibt aufgelöstes Pfad-Dict zurück."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path   = os.path.abspath(os.path.join(script_dir, "..", "..", "root.cfg"))

    if not os.path.isfile(cfg_path):
        print(f"[{SCRIPT_KUERZEL}] ERROR | root.cfg nicht gefunden: {cfg_path}", file=sys.stderr)
        sys.exit(1)

    raw = {}
    with open(cfg_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if not stripped.startswith("<") or "=" not in stripped:
                continue
            key, _, value = stripped.partition("=")
            raw[key.strip()] = value.strip()

    if "<rootfolder>" not in raw:
        print(f"[{SCRIPT_KUERZEL}] ERROR | <rootfolder> fehlt in root.cfg", file=sys.stderr)
        sys.exit(1)

    rootfolder = raw["<rootfolder>"]
    return {k: v.replace("<rootfolder>", rootfolder) for k, v in raw.items()}


# ----------------------------------------------------------
# Ordner bereinigen
# ----------------------------------------------------------

def clean_folder(folder: str, log_path: str | None = None) -> None:
    """Löscht den Inhalt eines Ordners — Ordner selbst bleibt erhalten."""

    if not os.path.isdir(folder):
        _log(f"[SKIP]  Ordner nicht gefunden: {folder}", log_path)
        return

    removed_files = 0
    removed_dirs  = 0
    errors        = 0

    for entry in os.listdir(folder):
        entry_path = os.path.join(folder, entry)
        try:
            if os.path.isfile(entry_path) or os.path.islink(entry_path):
                os.remove(entry_path)
                removed_files += 1
                _log(f"  [DEL-F]  {entry_path}", log_path)
            elif os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
                removed_dirs += 1
                _log(f"  [DEL-D]  {entry_path}", log_path)
        except Exception as e:
            _log(f"  [FEHLER] {entry_path} — {e}", log_path)
            errors += 1

    _log(
        f"[OK]  {folder} bereinigt — "
        f"{removed_files} Datei(en), {removed_dirs} Unterordner gelöscht, "
        f"{errors} Fehler.",
        log_path
    )


# ----------------------------------------------------------
# Hauptprogramm
# ----------------------------------------------------------

def main() -> None:
    cfg      = _resolve_root()
    basepath = cfg.get("<stages>", "")

    if not basepath:
        print(f"[{SCRIPT_KUERZEL}] ERROR | <stages> nicht in root.cfg", file=sys.stderr)
        sys.exit(1)

    # Log-Pfad
    stages_dir = cfg.get("<stages>", "")
    logs_dir   = os.path.join(stages_dir, "99-logs") if stages_dir else ""
    log_path   = os.path.join(logs_dir, LOG_FILENAME) if logs_dir else None
    if logs_dir:
        os.makedirs(logs_dir, exist_ok=True)

    _log(f"{'='*55}  Start {SCRIPT_KUERZEL}", log_path)

    for relativ in ZIEL_LISTE:
        ziel = os.path.join(basepath, relativ)
        _log(f"Ziel-Ordner : {ziel}", log_path)
        clean_folder(ziel, log_path)

    _log(f"{'='*55}  Ende {SCRIPT_KUERZEL}", log_path)
    if log_path:
        print(f"[{SCRIPT_KUERZEL}] Log geschrieben -> {log_path}")


if __name__ == "__main__":
    main()
