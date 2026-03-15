#!/usr/bin/env python3
# CLE00-resolve_root.py
#
# Zweck (CLE-Reihe):
# - root.cfg lesen und alle Pfad-Variablen als Dict bereitstellen
# - Schreibt Referenz-Log für die CLE-Reihe
# - Basis für alle CLE1x, CLE2x, CLE3x Scripts
# - Kann standalone ausgeführt werden (Selbsttest / Diagnose)
#
# Ablageort  : <rootfolder>\01-artifacts\01-scripts\CLE00-resolve_root.py
# Konfiguration: <rootfolder>\root.cfg
#
# Ausgabe (standalone):
# - Konsolen-Ausgabe aller aufgelösten Pfade
# - <rootfolder>\02-stages\99-logs\CLE00-resolve_root.log
#
# Regeln:
# - Keine Abhängigkeit zu anderen Scripts
# - Deterministisch, audit-freundlich
# - Abbruch bei Fehler (hard fail)
# - Referenz: HLP00_resolve_root.py | Stage 5 | Cleaning Run 5.5

import os
import sys
from datetime import datetime


# ----------------------------------------------------------
# Konstanten
# ----------------------------------------------------------

SCRIPT_KUERZEL = "CLE00"
CFG_FILENAME   = "root.cfg"
LOG_FILENAME   = "CLE00-resolve_root.log"


# ----------------------------------------------------------
# Hilfsfunktionen (Logging)
# ----------------------------------------------------------

def _now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _log(message: str, log_path: str | None = None) -> None:
    """Gibt eine Zeile auf der Konsole aus und schreibt sie optional ins Log."""
    line = f"[{SCRIPT_KUERZEL}] {_now_ts()} | {message}"
    print(line)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass


def _die(message: str, log_path: str | None = None) -> None:
    """Gibt Fehlermeldung aus und beendet das Script hart."""
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
# root.cfg finden
# ----------------------------------------------------------

def find_root_cfg(script_dir: str) -> str:
    """
    Sucht root.cfg zwei Ebenen über dem Script-Ordner.
    Erwarteter Pfad: <rootfolder>\root.cfg
    Script liegt in: <rootfolder>\01-artifacts\01-scripts\
    """
    return os.path.abspath(
        os.path.join(script_dir, "..", "..", CFG_FILENAME)
    )


# ----------------------------------------------------------
# root.cfg parsen
# ----------------------------------------------------------

def parse_root_cfg(cfg_path: str) -> dict:
    """
    Liest root.cfg und gibt alle Pfad-Variablen als Dict zurück.

    Auflösungsregel:
    1. <rootfolder> wird als erster Durchlauf aufgelöst — das ist der Anker.
    2. Alle anderen Werte die <rootfolder> als Platzhalter enthalten
       werden im zweiten Durchlauf ersetzt.

    Fehlerbehandlung: wirft ValueError bei ungültigem Inhalt.
    """
    if not os.path.isfile(cfg_path):
        raise ValueError(f"root.cfg nicht gefunden: {cfg_path}")

    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        raise ValueError(f"root.cfg nicht lesbar: {e}")

    raw = {}

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not stripped.startswith("<") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        key   = key.strip()
        value = value.strip()
        if key and value:
            raw[key] = value

    # Schritt 1: <rootfolder> zuerst auflösen — das ist der Anker
    if "<rootfolder>" not in raw:
        raise ValueError(
            "Kein <rootfolder> Eintrag in root.cfg gefunden.\n"
            "Bitte root.cfg prüfen und <rootfolder>=<Pfad> eintragen."
        )

    rootfolder = raw["<rootfolder>"]

    if not rootfolder:
        raise ValueError("<rootfolder> Wert ist leer in root.cfg.")

    # Schritt 2: Alle Werte auflösen — <rootfolder> als Platzhalter ersetzen
    resolved = {}
    for key, value in raw.items():
        resolved[key] = value.replace("<rootfolderoapply>", rootfolder).replace("<rootfolder>", rootfolder)

    return resolved


# ----------------------------------------------------------
# Öffentliche API — wird von allen CLE Scripts importiert
# ----------------------------------------------------------

def get_root_cfg() -> dict:
    """
    Findet root.cfg automatisch (relativ zum eigenen Script-Pfad)
    und gibt das aufgelöste Pfad-Dict zurück.

    Verwendung in CLE Scripts:
        from CLE00-resolve_root import get_root_cfg
        cfg = get_root_cfg()
        root      = cfg["<rootfolder>"]
        artifacts = cfg["<artifacts>"]

    Bricht mit sys.exit(1) ab wenn root.cfg nicht gefunden
    oder ungültig ist.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path   = find_root_cfg(script_dir)

    try:
        return parse_root_cfg(cfg_path)
    except ValueError as e:
        print(f"[{SCRIPT_KUERZEL}] {_now_ts()} | ERROR | {e}", file=sys.stderr)
        sys.exit(1)


def get_cfg_path() -> str:
    """Gibt den erwarteten Pfad zur root.cfg zurück."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return find_root_cfg(script_dir)


# ----------------------------------------------------------
# Standalone-Ausführung — Selbsttest und Diagnose
# ----------------------------------------------------------

def main() -> None:
    """
    Standalone-Ausführung: liest root.cfg, gibt alle
    aufgelösten Pfade aus und schreibt ein Referenz-Log
    für die gesamte CLE-Reihe.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path   = find_root_cfg(script_dir)

    print(f"[{SCRIPT_KUERZEL}] {_now_ts()} | Suche root.cfg: {cfg_path}")

    if not os.path.isfile(cfg_path):
        _die(f"root.cfg nicht gefunden: {cfg_path}")

    try:
        cfg = parse_root_cfg(cfg_path)
    except ValueError as e:
        _die(str(e))

    # Log-Pfad aufbauen — erst nach erfolgreicher cfg-Auflösung möglich
    stages_dir = cfg.get("<stages>", "")
    logs_dir   = os.path.join(stages_dir, "99-logs") if stages_dir else ""
    log_path   = os.path.join(logs_dir, LOG_FILENAME) if logs_dir else None

    # Log-Ordner anlegen falls nicht vorhanden
    if logs_dir:
        os.makedirs(logs_dir, exist_ok=True)

    # Ausgabe aller aufgelösten Pfade
    _log(f"{'='*55}  CLE-Reihe | Root-Auflösung", log_path)
    _log(f"root.cfg gefunden : {cfg_path}", log_path)
    _log(f"{'─' * 55}", log_path)

    for key, value in cfg.items():
        if os.path.isdir(value):
            exists = "  [OK - Ordner vorhanden]"
        elif os.path.isfile(value):
            exists = "  [OK - Datei vorhanden]"
        else:
            exists = "  [WARNUNG - Pfad nicht gefunden]"
        _log(f"  {key:<15} = {value}{exists}", log_path)

    _log(f"{'─' * 55}", log_path)
    _log(f"root.cfg erfolgreich gelesen — {len(cfg)} Variablen aufgelöst.", log_path)
    _log(f"Referenz bereit für CLE10–CLE35.", log_path)
    _log(f"{'='*55}  Ende CLE00", log_path)

    if log_path:
        print(f"[{SCRIPT_KUERZEL}] Log geschrieben -> {log_path}")


if __name__ == "__main__":
    main()
