# ==============================================================================
# SVG01-inventory.py
# ==============================================================================
# Reihe   : SVG — Image to SVG Konvertierung
# Aufgabe : Quellordner einlesen und Inventarliste erstellen
# Output  : 02-stages\99-logs\SVG01-inventory.log
# Abhängig: HLP00_resolve_root.py
# ==============================================================================
# R+MUNI Blueprint | Stage S1.04 | 2026-04-12
# ==============================================================================

import os
import sys
from datetime import datetime

# ------------------------------------------------------------------------------
# HLP00 einbinden
# ------------------------------------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from HLP00_resolve_root import get_root_cfg
except ImportError:
    print("[SVG01] FEHLER: HLP00_resolve_root.py nicht gefunden.")
    print("        Erwartet in: " + script_dir)
    sys.exit(1)

# ------------------------------------------------------------------------------
# Konstanten
# ------------------------------------------------------------------------------
SCRIPT_ID   = "SVG01"
CONFIG_NAME = "svg_config.txt"
LOG_NAME    = "SVG01-inventory.log"

# Sonderzeichen die RENAME_REQUIRED auslösen (Leerzeichen separat geprüft)
SONDERZEICHEN = set('!@#$%^&*()+=[]{}|;:\'",<>?/\\`~')

# ------------------------------------------------------------------------------
# Hilfsfunktionen
# ------------------------------------------------------------------------------

def parse_svg_config(config_path):
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


def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_log(log_path, lines):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def braucht_umbenennung(dateiname):
    """Prüft ob der Dateiname (ohne Endung) Leerzeichen oder
    problematische Sonderzeichen enthält."""
    name_ohne_ext = os.path.splitext(dateiname)[0]
    if " " in name_ohne_ext:
        return True
    if any(c in SONDERZEICHEN for c in name_ohne_ext):
        return True
    return False


def format_groesse(bytes):
    """Lesbare Dateigröße."""
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024 * 1024:
        return f"{bytes/1024:.1f} KB"
    else:
        return f"{bytes/(1024*1024):.1f} MB"


# ------------------------------------------------------------------------------
# Hauptlogik
# ------------------------------------------------------------------------------

def main():
    log_lines = []

    def log(status, message):
        line = f"[{ts()}] [{status:<16}] {message}"
        log_lines.append(line)
        print(line)

    log_lines.append("=" * 72)
    log_lines.append(f"  {SCRIPT_ID} — Inventarisierung Quellordner")
    log_lines.append(f"  R+MUNI Blueprint | SVG-Reihe | {ts()}")
    log_lines.append("=" * 72)
    log_lines.append("")

    # --- 1. root.cfg ---
    log_lines.append("--- 1. root.cfg ---")
    try:
        cfg        = get_root_cfg()
        rootfolder = cfg.get("<rootfolder>", "")
        stages     = cfg.get("<stages>", "")
        if not rootfolder:
            log("FEHLER", "<rootfolder> leer — root.cfg prüfen.")
            sys.exit(1)
        log("OK", f"rootfolder = {rootfolder}")
    except Exception as e:
        log("FEHLER", f"root.cfg Fehler: {e}")
        sys.exit(1)

    log_lines.append("")

    # --- 2. svg_config.txt ---
    log_lines.append("--- 2. svg_config.txt ---")
    config_path = os.path.join(rootfolder, "99-doku", CONFIG_NAME)
    if not os.path.isfile(config_path):
        log("FEHLER", f"svg_config.txt nicht gefunden: {config_path}")
        log("FEHLER", "SVG00 zuerst ausführen und Fehler beheben.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    try:
        svg_cfg = parse_svg_config(config_path)
    except Exception as e:
        log("FEHLER", f"svg_config.txt nicht lesbar: {e}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    source_folder = svg_cfg.get("svg_source_folder", "").strip()
    formate_raw   = svg_cfg.get("svg_formats", "").strip()

    if not source_folder:
        log("FEHLER", "svg_source_folder ist leer — svg_config.txt prüfen.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    if not formate_raw:
        log("FEHLER", "svg_formats ist leer — svg_config.txt prüfen.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    formate = [f.strip().lower() for f in formate_raw.split(",") if f.strip()]
    log("OK", f"svg_source_folder = {source_folder}")
    log("OK", f"svg_formats       = {', '.join(formate)}")

    log_lines.append("")

    # --- 3. Quellordner prüfen ---
    log_lines.append("--- 3. Quellordner ---")
    if not os.path.isdir(source_folder):
        log("FEHLER", f"Quellordner nicht gefunden: {source_folder}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)
    log("OK", f"Quellordner gefunden: {source_folder}")

    log_lines.append("")

    # --- 4. Dateien scannen ---
    log_lines.append("--- 4. Scan ---")

    alle_eintraege = os.listdir(source_folder)
    alle_dateien   = [e for e in alle_eintraege
                      if os.path.isfile(os.path.join(source_folder, e))]

    zaehler = {"OK": 0, "RENAME_REQUIRED": 0, "SKIP": 0}
    inventar = []  # Liste der Ergebnisse für Tabelle

    for dateiname in sorted(alle_dateien):
        ext = os.path.splitext(dateiname)[1].lstrip(".").lower()
        pfad = os.path.join(source_folder, dateiname)
        try:
            groesse = os.path.getsize(pfad)
            groesse_str = format_groesse(groesse)
        except Exception:
            groesse_str = "?"

        if ext not in formate:
            status = "SKIP"
        elif braucht_umbenennung(dateiname):
            status = "RENAME_REQUIRED"
        else:
            status = "OK"

        zaehler[status] += 1
        inventar.append((status, dateiname, ext.upper(), groesse_str))

    # Tabelle ausgeben
    log_lines.append("")
    log_lines.append(f"  {'STATUS':<18} {'DATEINAME':<45} {'EXT':<8} {'GROESSE'}")
    log_lines.append(f"  {'-'*18} {'-'*45} {'-'*8} {'-'*10}")

    for status, dateiname, ext, groesse_str in inventar:
        zeile = f"  {status:<18} {dateiname:<45} {ext:<8} {groesse_str}"
        log_lines.append(zeile)
        print(zeile)

    log_lines.append("")

    # --- Zusammenfassung ---
    gesamt = sum(zaehler.values())
    log_lines.append("=" * 72)
    log_lines.append(f"  ZUSAMMENFASSUNG")
    log_lines.append(f"  Gesamt gefunden   : {gesamt}")
    log_lines.append(f"  OK                : {zaehler['OK']}")
    log_lines.append(f"  RENAME_REQUIRED   : {zaehler['RENAME_REQUIRED']}")
    log_lines.append(f"  SKIP              : {zaehler['SKIP']}")

    if zaehler["RENAME_REQUIRED"] > 0:
        log_lines.append(f"")
        log_lines.append(f"  HINWEIS: {zaehler['RENAME_REQUIRED']} Datei(en) mit RENAME_REQUIRED.")
        log_lines.append(f"           SVG02 ausführen um Dateinamen zu bereinigen.")

    if zaehler["OK"] + zaehler["RENAME_REQUIRED"] == 0:
        log_lines.append(f"")
        log_lines.append(f"  WARNUNG: Keine verarbeitbaren Dateien gefunden.")
        log_lines.append(f"           svg_formats in svg_config.txt prüfen.")

    log_lines.append("=" * 72)

    print(f"\n[{SCRIPT_ID}] Gesamt: {gesamt} | OK: {zaehler['OK']} | "
          f"RENAME_REQUIRED: {zaehler['RENAME_REQUIRED']} | SKIP: {zaehler['SKIP']}")

    _finalize(log_lines, stages, LOG_NAME)


def _finalize(log_lines, stages, log_name):
    if not stages:
        print(f"\n[{SCRIPT_ID}] Log konnte nicht geschrieben werden — stages Pfad leer.")
        return
    try:
        log_path = os.path.join(stages, "99-logs", log_name)
        write_log(log_path, log_lines)
        print(f"[{SCRIPT_ID}] Log geschrieben: {log_path}")
    except Exception as e:
        print(f"[{SCRIPT_ID}] Log konnte nicht geschrieben werden: {e}")


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
