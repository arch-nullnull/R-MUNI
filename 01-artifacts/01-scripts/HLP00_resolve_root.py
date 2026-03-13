#!/usr/bin/env python3
# HLP00_resolve_root.py
#
# Zweck (HLP-Bibliothek):
# - root.cfg lesen und alle Pfad-Variablen als Dict bereitstellen
# - <rootfolder> ist der Anker — wird zuerst aufgelöst
# - Alle anderen Werte die <rootfolder> enthalten werden ersetzt
# - Kann standalone ausgeführt werden (Selbsttest / Diagnose)
# - Wird von allen Script-Reihen importiert:
#     from HLP00_resolve_root import get_root_cfg
#
# Ablageort  : <rootfolder>\01-artifacts\01-scripts\HLP00_resolve_root.py
# Konfiguration: <rootfolder>\root.cfg
#
# Ausgabe (standalone):
# - Konsolen-Ausgabe aller aufgelösten Pfade
# - <rootfolder>\02-stages\99-logs\HLP00_resolve_root.log
#
# Regeln:
# - Keine Abhängigkeit zu anderen Scripts
# - Deterministisch, audit-freundlich
# - Abbruch bei Fehler (hard fail)
# - Basis: Cleaning Run 5.5 | Stage 5

import os
import sys
from datetime import datetime


# ----------------------------------------------------------
# Konstanten
# ----------------------------------------------------------

SCRIPT_KUERZEL = "HLP00"
CFG_FILENAME   = "root.cfg"
LOG_FILENAME   = "HLP00_resolve_root.log"


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
    3. Geschwister-Ordner (<apps>, <doku> etc.) haben fixe Pfade
       und werden unverändert übernommen.

    Rückgabe-Beispiel:
    {
        "<rootfolder>": "C:\\Prototyping\\R+MUNI",
        "<models>":     "C:\\Prototyping\\R+MUNI\\00-model",
        "<artifacts>":  "C:\\Prototyping\\R+MUNI\\01-artifacts",
        "<stages>":     "C:\\Prototyping\\R+MUNI\\02-stages",
        "<apps>":       "C:\\Prototyping\\R+MUNI Apps",
        "<doku>":       "C:\\Prototyping\\R+MUNI Doku\\R+MUNI Doku-internal",
        "<dokupublic>": "C:\\Prototyping\\R+MUNI Doku\\R+MUNI Doku-public",
        "<creative>":   "C:\\Prototyping\\R+MUNI Doku\\R+MUNI Doku-creative",
    }

    Fehlerbehandlung: wirft ValueError bei ungültigem Inhalt.
    """
    if not os.path.isfile(cfg_path):
        raise ValueError(f"root.cfg nicht gefunden: {cfg_path}")

    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        raise ValueError(f"root.cfg nicht lesbar: {e}")

    raw = {}  # Rohwerte aus der Datei

    for line in lines:
        stripped = line.strip()
        # Leerzeilen und Kommentare überspringen
        if not stripped or stripped.startswith("#"):
            continue
        # Nur Zeilen mit <key>=value verarbeiten
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
        resolved[key] = value.replace("<rootfolder>", rootfolder)

    return resolved


# ----------------------------------------------------------
# Öffentliche API — wird von allen Scripts importiert
# ----------------------------------------------------------

def get_root_cfg() -> dict:
    """
    Findet root.cfg automatisch (relativ zum eigenen Script-Pfad)
    und gibt das aufgelöste Pfad-Dict zurück.

    Verwendung in anderen Scripts:
        from HLP00_resolve_root import get_root_cfg
        cfg = get_root_cfg()
        root     = cfg["<rootfolder>"]
        stages   = cfg["<stages>"]
        doku     = cfg["<doku>"]

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
    """
    Gibt den erwarteten Pfad zur root.cfg zurück.
    Nützlich für Diagnose und Logging in aufrufenden Scripts.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return find_root_cfg(script_dir)


# ----------------------------------------------------------
# Standalone-Ausführung — Selbsttest und Diagnose
# ----------------------------------------------------------

def main() -> None:
    """
    Standalone-Ausführung: liest root.cfg, gibt alle
    aufgelösten Pfade aus und schreibt ein Log.
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

    # Ausgabe aller aufgelösten Pfade
    _log(f"root.cfg gefunden : {cfg_path}", log_path)
    _log(f"{'─' * 50}", log_path)

    for key, value in cfg.items():
        exists = ""
        if os.path.isdir(value):
            exists = "  [OK - Ordner vorhanden]"
        elif os.path.isfile(value):
            exists = "  [OK - Datei vorhanden]"
        else:
            exists = "  [WARNUNG - Pfad nicht gefunden]"
        _log(f"  {key:<15} = {value}{exists}", log_path)

    _log(f"{'─' * 50}", log_path)
    _log(f"root.cfg erfolgreich gelesen — {len(cfg)} Variablen aufgelöst.", log_path)

    if log_path:
        print(f"[{SCRIPT_KUERZEL}] Log geschrieben -> {log_path}")


if __name__ == "__main__":
    main()
