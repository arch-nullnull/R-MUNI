#!/usr/bin/env python3
# CLE26-csv_no_id.py
#
# Zweck:
# - Gezieltes Löschen von zwei definierten Dateien (kein Ordner-Clean)
# - Ziel-Dateien:
#   01-artifacts\02-csv\04-import\properties.csv
#   01-artifacts\02-csv\04-import\relations.csv
#
# Anwendungsfall:
# - Spezialfall: Integration von "Archi-ID-losen" Objekten in den
#   Archi-OEF-XML-CSV-Archi Flow
# - properties.csv und relations.csv werden gezielt entfernt damit
#   nur elements.csv im Import-Ordner verbleibt
# - elements.csv bleibt bewusst erhalten — sie enthält die neuen
#   ID-losen Objekte die über den Flow eine Archi-ID erhalten sollen
#
# Abgrenzung zu CLE24:
# - CLE24 löscht den gesamten Inhalt von 04-import
# - CLE26 löscht gezielt nur properties.csv + relations.csv
#   und lässt alle anderen Dateien (inkl. elements.csv) unangetastet
#
# Ablageort  : <rootfolder>\01-artifacts\01-scripts\CLE26-csv_no_id.py
# Referenz   : CLE24-csv_import.py | CLE00-resolve_root.py
# Stage 5 | Cleaning Run 5.5

import os
import sys
from datetime import datetime

# ----------------------------------------------------------
# Konstanten
# ----------------------------------------------------------

SCRIPT_KUERZEL = "CLE26"
LOG_FILENAME   = "CLE26-csv_no_id.log"

# Ziel-Dateien relativ zu <artifacts>
# Nur diese zwei Dateien werden gelöscht — keine anderen
ZIEL_DATEIEN = [
    os.path.join("02-csv", "04-import", "properties.csv"),
    os.path.join("02-csv", "04-import", "relations.csv"),
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
# Einzelne Datei löschen
# ----------------------------------------------------------

def delete_file(filepath: str, log_path: str | None = None) -> bool:
    """
    Löscht eine einzelne Datei gezielt.
    Gibt True zurück wenn gelöscht, False wenn übersprungen.
    Bricht nicht ab wenn Datei nicht vorhanden — [SKIP] statt Fehler.
    """
    if not os.path.isfile(filepath):
        _log(f"[SKIP]  Datei nicht gefunden: {filepath}", log_path)
        return False

    try:
        os.remove(filepath)
        _log(f"  [DEL-F]  {filepath}", log_path)
        return True
    except Exception as e:
        _log(f"  [FEHLER] {filepath} — {e}", log_path)
        return False


# ----------------------------------------------------------
# Hauptprogramm
# ----------------------------------------------------------

def main() -> None:
    cfg       = _resolve_root()
    artifacts = cfg.get("<artifacts>", "")

    if not artifacts:
        print(f"[{SCRIPT_KUERZEL}] ERROR | <artifacts> nicht in root.cfg", file=sys.stderr)
        sys.exit(1)

    # Log-Pfad
    stages_dir = cfg.get("<stages>", "")
    logs_dir   = os.path.join(stages_dir, "99-logs") if stages_dir else ""
    log_path   = os.path.join(logs_dir, LOG_FILENAME) if logs_dir else None
    if logs_dir:
        os.makedirs(logs_dir, exist_ok=True)

    _log(f"{'='*55}  Start {SCRIPT_KUERZEL}", log_path)
    _log(f"Modus: Gezieltes Datei-Löschen (kein Ordner-Clean)", log_path)

    deleted = 0
    skipped = 0

    for relativ in ZIEL_DATEIEN:
        ziel_datei = os.path.join(artifacts, relativ)
        _log(f"Ziel-Datei  : {ziel_datei}", log_path)
        if delete_file(ziel_datei, log_path):
            deleted += 1
        else:
            skipped += 1

    _log(
        f"[OK]  Abgeschlossen — "
        f"{deleted} Datei(en) gelöscht, {skipped} nicht vorhanden ([SKIP]).",
        log_path
    )
    _log(f"{'='*55}  Ende {SCRIPT_KUERZEL}", log_path)

    if log_path:
        print(f"[{SCRIPT_KUERZEL}] Log geschrieben -> {log_path}")


if __name__ == "__main__":
    main()
