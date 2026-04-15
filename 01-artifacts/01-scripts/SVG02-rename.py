# ==============================================================================
# SVG02-rename.py
# ==============================================================================
# Reihe   : SVG — Image to SVG Konvertierung
# Aufgabe : Dateien mit RENAME_REQUIRED aus SVG01-Inventar umbenennen
# Output  : 02-stages\99-logs\SVG02-rename.log
# Abhängig: HLP00_resolve_root.py, SVG01-inventory.log
# ==============================================================================
# Bereinigungsregeln:
#   Leerzeichen      → Unterstrich
#   Sonderzeichen    → entfernen (außer Bindestrich und Punkt)
# Kollision: existiert bereinigter Name bereits → SKIP, keine Überschreibung
# ==============================================================================
# R+MUNI Blueprint | Stage S1.04 | 2026-04-12
# ==============================================================================

import os
import sys
import re
from datetime import datetime

# ------------------------------------------------------------------------------
# HLP00 einbinden
# ------------------------------------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from HLP00_resolve_root import get_root_cfg
except ImportError:
    print("[SVG02] FEHLER: HLP00_resolve_root.py nicht gefunden.")
    sys.exit(1)

# ------------------------------------------------------------------------------
# Konstanten
# ------------------------------------------------------------------------------
SCRIPT_ID    = "SVG02"
CONFIG_NAME  = "svg_config.txt"
INVENTAR_LOG = "SVG01-inventory.log"
LOG_NAME     = "SVG02-rename.log"

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


def bereinige_name(dateiname):
    """Bereinigt einen Dateinamen:
    - Leerzeichen → Unterstrich
    - Sonderzeichen entfernen (außer Bindestrich, Unterstrich, Punkt)
    - Name und Endung werden getrennt behandelt — Endung bleibt unverändert
    """
    name, ext = os.path.splitext(dateiname)
    name = name.replace(" ", "_")
    name = re.sub(r"[^\w\-]", "", name)  # \w = [a-zA-Z0-9_]
    return name + ext


def parse_inventar(inventar_path):
    """Liest SVG01-inventory.log und gibt Liste der RENAME_REQUIRED
    Dateinamen zurück.

    Tabellenformat SVG01 (feste Spaltenbreiten, 2 Leerzeichen Einrückung):
      "  {STATUS:<18} {DATEINAME:<45} {EXT:<8} {GROESSE}"
    Status beginnt bei Position 2, Dateiname bei Position 21.
    Nur Zeilen die mit "  RENAME_REQUIRED" beginnen werden ausgewertet.
    """
    rename_liste = []
    STATUS_START    = 2
    DATEINAME_START = 2 + 18  # STATUS (18) + Leerzeichen
    DATEINAME_ENDE  = DATEINAME_START + 45

    with open(inventar_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            # Nur Zeilen mit RENAME_REQUIRED in der Status-Spalte
            status_teil = line[STATUS_START:STATUS_START + 18].strip()
            if status_teil == "RENAME_REQUIRED":
                dateiname = line[DATEINAME_START:DATEINAME_ENDE].strip()
                # Nur gueltige Dateinamen: Punkt erforderlich, keine Zusammenfassungszeilen
                if dateiname and "." in dateiname and not dateiname.startswith(":"):
                    rename_liste.append(dateiname)

    return rename_liste


# ------------------------------------------------------------------------------
# Hauptlogik
# ------------------------------------------------------------------------------

def main():
    log_lines = []
    zaehler   = {"OK": 0, "SKIP": 0, "FEHLER": 0}

    def log(status, message):
        line = f"[{ts()}] [{status:<7}] {message}"
        log_lines.append(line)
        print(line)

    log_lines.append("=" * 72)
    log_lines.append(f"  {SCRIPT_ID} — Dateinamen-Bereinigung")
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
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    try:
        svg_cfg = parse_svg_config(config_path)
    except Exception as e:
        log("FEHLER", f"svg_config.txt nicht lesbar: {e}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    source_folder = svg_cfg.get("svg_source_folder", "").strip()
    if not source_folder:
        log("FEHLER", "svg_source_folder leer — svg_config.txt prüfen.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    log("OK", f"svg_source_folder = {source_folder}")
    log_lines.append("")

    # --- 3. SVG01-inventory.log lesen ---
    log_lines.append("--- 3. SVG01-inventory.log ---")
    inventar_path = os.path.join(stages, "99-logs", INVENTAR_LOG)

    if not os.path.isfile(inventar_path):
        log("FEHLER", f"SVG01-inventory.log nicht gefunden: {inventar_path}")
        log("FEHLER", "SVG01 zuerst ausführen.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    try:
        rename_liste = parse_inventar(inventar_path)
    except Exception as e:
        log("FEHLER", f"SVG01-inventory.log nicht lesbar: {e}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    log("OK", f"SVG01-inventory.log gelesen — {len(rename_liste)} RENAME_REQUIRED Datei(en)")
    log_lines.append("")

    # --- 4. Umbenennung ---
    log_lines.append("--- 4. Umbenennung ---")

    if not rename_liste:
        log("INFO", "Keine Dateien mit RENAME_REQUIRED — nichts zu tun.")
        log_lines.append("")
        log_lines.append("=" * 72)
        log_lines.append("  ERGEBNIS: OK — Keine Umbenennungen erforderlich.")
        log_lines.append("=" * 72)
        _finalize(log_lines, stages, LOG_NAME)
        return

    log_lines.append("")
    log_lines.append(f"  {'ORIGINAL':<40} {'NEU':<40} STATUS")
    log_lines.append(f"  {'-'*40} {'-'*40} {'-'*7}")

    for original in rename_liste:
        src_path = os.path.join(source_folder, original)

        # Quelldatei prüfen
        if not os.path.isfile(src_path):
            zeile = f"  {original:<40} {'—':<40} FEHLER (nicht gefunden)"
            log_lines.append(zeile)
            print(zeile)
            zaehler["FEHLER"] += 1
            continue

        neuer_name = bereinige_name(original)
        dst_path   = os.path.join(source_folder, neuer_name)

        # Kein Umbenennen nötig wenn Name nach Bereinigung identisch
        if neuer_name == original:
            zeile = f"  {original:<40} {neuer_name:<40} SKIP (bereits sauber)"
            log_lines.append(zeile)
            print(zeile)
            zaehler["SKIP"] += 1
            continue

        # Kollisionsprüfung
        if os.path.exists(dst_path):
            zeile = f"  {original:<40} {neuer_name:<40} SKIP (Kollision)"
            log_lines.append(zeile)
            print(zeile)
            zaehler["SKIP"] += 1
            continue

        # Umbenennen
        try:
            os.rename(src_path, dst_path)
            zeile = f"  {original:<40} {neuer_name:<40} OK"
            log_lines.append(zeile)
            print(zeile)
            zaehler["OK"] += 1
        except Exception as e:
            zeile = f"  {original:<40} {neuer_name:<40} FEHLER ({e})"
            log_lines.append(zeile)
            print(zeile)
            zaehler["FEHLER"] += 1

    log_lines.append("")

    # --- Zusammenfassung ---
    log_lines.append("=" * 72)
    log_lines.append(f"  ZUSAMMENFASSUNG")
    log_lines.append(f"  Umbenannt         : {zaehler['OK']}")
    log_lines.append(f"  Übersprungen      : {zaehler['SKIP']}")
    log_lines.append(f"  Fehler            : {zaehler['FEHLER']}")

    if zaehler["FEHLER"] > 0:
        log_lines.append(f"")
        log_lines.append(f"  WARNUNG: {zaehler['FEHLER']} Umbenennung(en) fehlgeschlagen.")
        log_lines.append(f"           Log prüfen und manuell korrigieren.")

    if zaehler["SKIP"] > 0:
        log_lines.append(f"")
        log_lines.append(f"  HINWEIS: {zaehler['SKIP']} Datei(en) übersprungen.")
        log_lines.append(f"           Kollision oder Name bereits sauber.")

    log_lines.append(f"")
    log_lines.append(f"  HINWEIS: SVG01 erneut ausführen um aktualisiertes")
    log_lines.append(f"           Inventar vor SVG03/SVG04 zu erzeugen.")
    log_lines.append("=" * 72)

    print(f"\n[{SCRIPT_ID}] Umbenannt: {zaehler['OK']} | "
          f"Übersprungen: {zaehler['SKIP']} | Fehler: {zaehler['FEHLER']}")

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
