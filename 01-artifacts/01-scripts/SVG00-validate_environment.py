# ==============================================================================
# SVG00-validate_environment.py
# ==============================================================================
# Reihe   : SVG — Image to SVG Konvertierung
# Aufgabe : Umgebungsvalidierung — root.cfg und svg_config.txt prüfen
# Output  : 02-stages\99-logs\SVG00-validate_environment.log
# Abhängig: HLP00_resolve_root.py
# ==============================================================================
# R+MUNI Blueprint | Stage S1.04 | 2026-04-12
# ==============================================================================

import os
import sys
from datetime import datetime

# ------------------------------------------------------------------------------
# HLP00 einbinden — root.cfg auflösen
# ------------------------------------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from HLP00_resolve_root import get_root_cfg
except ImportError:
    print("[SVG00] FEHLER: HLP00_resolve_root.py nicht gefunden.")
    print("        Erwartet in: " + script_dir)
    sys.exit(1)

# ------------------------------------------------------------------------------
# Konstanten
# ------------------------------------------------------------------------------
SCRIPT_ID   = "SVG00"
CONFIG_NAME = "svg_config.txt"
LOG_NAME    = "SVG00-validate_environment.log"

PFLICHTFELDER = [
    "inkscape_exe",
    "svg_source_folder",
    "svg_target_folder",
    "svg_overwrite",
    "svg_formats",
]

# ------------------------------------------------------------------------------
# Hilfsfunktionen
# ------------------------------------------------------------------------------

def parse_svg_config(config_path):
    """Liest svg_config.txt und gibt ein dict zurück.
    Kommentare (#) und Leerzeilen werden übersprungen.
    """
    result = {}
    with open(config_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                result[key.strip()] = value.strip()
    return result


def write_log(log_path, lines):
    """Schreibt Zeilen in das Log-File (UTF-8)."""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def ts():
    """Aktueller Zeitstempel für Log-Zeilen."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ------------------------------------------------------------------------------
# Hauptlogik
# ------------------------------------------------------------------------------

def main():
    log_lines = []
    fehler    = 0
    warnungen = 0

    def log(status, message):
        line = f"[{ts()}] [{status:<7}] {message}"
        log_lines.append(line)
        print(line)

    log_lines.append("=" * 72)
    log_lines.append(f"  {SCRIPT_ID} — Umgebungsvalidierung")
    log_lines.append(f"  R+MUNI Blueprint | SVG-Reihe | {ts()}")
    log_lines.append("=" * 72)
    log_lines.append("")

    # --- 1. root.cfg auflösen ---
    # HLP00 liefert Keys mit spitzen Klammern: <rootfolder>, <stages> etc.
    log_lines.append("--- 1. root.cfg ---")
    try:
        cfg        = get_root_cfg()
        rootfolder = cfg.get("<rootfolder>", "")
        stages     = cfg.get("<stages>", "")

        if not rootfolder:
            log("FEHLER", "<rootfolder> ist leer — root.cfg prüfen.")
            _finalize(log_lines, stages, LOG_NAME)
            sys.exit(1)

        log("OK", f"root.cfg aufgelöst")
        log("OK", f"rootfolder = {rootfolder}")
        log("OK", f"stages     = {stages}")
    except Exception as e:
        log("FEHLER", f"root.cfg konnte nicht aufgelöst werden: {e}")
        print(f"\n[{SCRIPT_ID}] Kritischer Fehler — Abbruch.")
        sys.exit(1)

    log_lines.append("")

    # --- 2. svg_config.txt lokalisieren ---
    log_lines.append("--- 2. svg_config.txt ---")
    config_path = os.path.join(rootfolder, "99-doku", CONFIG_NAME)
    log("INFO", f"Erwarteter Pfad: {config_path}")

    if not os.path.isfile(config_path):
        log("FEHLER", f"svg_config.txt nicht gefunden: {config_path}")
        log("FEHLER", f"Datei ablegen unter: {config_path}")
        _finalize(log_lines, stages, LOG_NAME)
        print(f"\n[{SCRIPT_ID}] Kritischer Fehler — Abbruch.")
        sys.exit(1)
    log("OK", "svg_config.txt gefunden")

    log_lines.append("")

    # --- 3. svg_config.txt parsen und Pflichtfelder prüfen ---
    log_lines.append("--- 3. Pflichtfelder ---")
    try:
        svg_cfg = parse_svg_config(config_path)
    except Exception as e:
        log("FEHLER", f"svg_config.txt konnte nicht gelesen werden: {e}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    for feld in PFLICHTFELDER:
        if feld not in svg_cfg or not svg_cfg[feld].strip():
            log("FEHLER", f"Pflichtfeld fehlt oder leer: {feld}")
            fehler += 1
        else:
            log("OK", f"{feld} = {svg_cfg[feld]}")

    if fehler > 0:
        log_lines.append("")
        log("FEHLER", f"{fehler} Pflichtfeld(er) fehlen oder leer — Abbruch.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    log_lines.append("")

    # --- 4. inkscape_exe prüfen ---
    log_lines.append("--- 4. Inkscape ---")
    inkscape_exe = svg_cfg["inkscape_exe"]
    if not os.path.isfile(inkscape_exe):
        log("FEHLER", f"inkscape_exe nicht gefunden: {inkscape_exe}")
        log("FEHLER", "Pfad in svg_config.txt anpassen.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)
    log("OK", f"inkscape_exe gefunden: {inkscape_exe}")

    log_lines.append("")

    # --- 5. Quellordner prüfen ---
    log_lines.append("--- 5. Quellordner ---")
    source_folder = svg_cfg["svg_source_folder"]
    if not os.path.isdir(source_folder):
        log("FEHLER", f"svg_source_folder nicht gefunden: {source_folder}")
        log("FEHLER", "Pfad in svg_config.txt prüfen.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)
    log("OK", f"svg_source_folder gefunden: {source_folder}")

    log_lines.append("")

    # --- 6. Zielordner prüfen ---
    log_lines.append("--- 6. Zielordner ---")
    target_folder = svg_cfg["svg_target_folder"]
    if not os.path.isdir(target_folder):
        log("WARNUNG", f"svg_target_folder nicht gefunden: {target_folder}")
        log("WARNUNG", "Zielordner vor SVG03/SVG04 manuell anlegen.")
        warnungen += 1
    else:
        log("OK", f"svg_target_folder gefunden: {target_folder}")

    log_lines.append("")

    # --- 7. svg_formats prüfen ---
    log_lines.append("--- 7. Formate ---")
    formate = [f.strip().lower() for f in svg_cfg["svg_formats"].split(",") if f.strip()]
    if not formate:
        log("FEHLER", "svg_formats ist leer — mindestens ein Format erforderlich.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)
    log("OK", f"svg_formats: {', '.join(formate)}")

    log_lines.append("")

    # --- Zusammenfassung ---
    log_lines.append("=" * 72)
    if fehler == 0 and warnungen == 0:
        log_lines.append(f"  ERGEBNIS: OK — Umgebung vollständig validiert.")
    elif fehler == 0:
        log_lines.append(f"  ERGEBNIS: WARNUNG — {warnungen} Warnung(en), keine kritischen Fehler.")
    else:
        log_lines.append(f"  ERGEBNIS: FEHLER — {fehler} kritischer Fehler.")
    log_lines.append("=" * 72)

    _finalize(log_lines, stages, LOG_NAME)


def _finalize(log_lines, stages, log_name):
    """Log-File in 99-logs schreiben."""
    if not stages:
        print(f"\n[{SCRIPT_ID}] Log konnte nicht geschrieben werden — stages Pfad leer.")
        return
    try:
        log_path = os.path.join(stages, "99-logs", log_name)
        write_log(log_path, log_lines)
        print(f"\n[{SCRIPT_ID}] Log geschrieben: {log_path}")
    except Exception as e:
        print(f"\n[{SCRIPT_ID}] Log konnte nicht geschrieben werden: {e}")


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
