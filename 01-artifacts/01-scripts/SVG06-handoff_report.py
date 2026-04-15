# ==============================================================================
# SVG06-handoff_report.py
# ==============================================================================
# Reihe   : SVG — Image to SVG Konvertierung
# Aufgabe : Abschlussprüfung — alle Logs der SVG-Reihe auswerten und
#           Gesamtstatus ausgeben
# Output  : 02-stages\99-logs\SVG06-handoff_report.log
# Abhängig: HLP00_resolve_root.py
# ==============================================================================
# Liest alle vorhandenen SVG-Reihe Logs aus 99-logs und gibt einen
# konsolidierten Überblick über den Gesamtstatus des Laufs.
# Prüft zusätzlich ob erwartete SVG-Zieldateien vorhanden sind.
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
    print("[SVG06] FEHLER: HLP00_resolve_root.py nicht gefunden.")
    sys.exit(1)

# ------------------------------------------------------------------------------
# Konstanten
# ------------------------------------------------------------------------------
SCRIPT_ID   = "SVG06"
CONFIG_NAME = "svg_config.txt"
LOG_NAME    = "SVG06-handoff_report.log"

# Alle SVG-Reihe Logs in Reihenfolge
SVG_LOGS = [
    ("SVG00", "SVG00-validate_environment.log"),
    ("SVG01", "SVG01-inventory.log"),
    ("SVG02", "SVG02-rename.log"),
    ("SVG03", "SVG03-embed.log"),
    ("SVG04", "SVG04-trace.log"),
    ("SVG05", "SVG05-resize.log"),
]

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


def format_groesse(path):
    try:
        b = os.path.getsize(path)
        if b < 1024:
            return f"{b} B"
        elif b < 1024 * 1024:
            return f"{b/1024:.1f} KB"
        else:
            return f"{b/(1024*1024):.1f} MB"
    except Exception:
        return "?"


def lese_log_zusammenfassung(log_path):
    """Liest die ZUSAMMENFASSUNG aus einem SVG-Log.
    Sucht den Block zwischen '=== ZUSAMMENFASSUNG' und '==='
    und gibt die Zeilen als Liste zurück."""
    zeilen = []
    in_zusammenfassung = False

    try:
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip()
                if "ZUSAMMENFASSUNG" in line:
                    in_zusammenfassung = True
                    continue
                if in_zusammenfassung:
                    if line.startswith("="):
                        break
                    if line.strip():
                        zeilen.append(line.strip())
    except Exception as e:
        zeilen.append(f"Log nicht lesbar: {e}")

    return zeilen


def lese_ergebnis(log_path):
    """Liest das ERGEBNIS aus SVG00 Log."""
    try:
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                if "ERGEBNIS:" in line:
                    return line.strip()
    except Exception:
        pass
    return "ERGEBNIS: nicht ermittelbar"


def hat_fehler(log_path):
    """Prüft ob ein Log FEHLER-Einträge enthält."""
    try:
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                if "[FEHLER]" in line or "Fehler            :" in line:
                    # Zusammenfassungszeile mit Fehler > 0 prüfen
                    if "Fehler            :" in line:
                        teile = line.split(":")
                        if len(teile) >= 2:
                            try:
                                if int(teile[-1].strip()) > 0:
                                    return True
                            except ValueError:
                                pass
                    elif "[FEHLER]" in line:
                        return True
    except Exception:
        pass
    return False


def parse_inventar_dateien(inventar_path):
    """Liest SVG01-inventory.log — gibt Liste von Dateinamen zurück
    die konvertiert werden sollen (OK + RENAME_REQUIRED)."""
    ergebnis = []
    STATUS_START    = 2
    DATEINAME_START = 2 + 18
    DATEINAME_ENDE  = DATEINAME_START + 45

    try:
        with open(inventar_path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip()
                if len(line) < DATEINAME_START:
                    continue
                status_teil = line[STATUS_START:STATUS_START + 18].strip()
                if status_teil in ("OK", "RENAME_REQUIRED"):
                    dateiname = line[DATEINAME_START:DATEINAME_ENDE].strip()
                    if dateiname and "." in dateiname and not dateiname.startswith(":"):
                        ergebnis.append(dateiname)
    except Exception:
        pass

    return ergebnis


def parse_rename_mapping(rename_log_path):
    """Liest SVG02-rename.log — gibt dict {original: neu} zurück."""
    mapping = {}
    try:
        with open(rename_log_path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip()
                # Format: "  ORIGINAL   NEU   OK"
                if "OK" in line and "→" not in line and len(line) > 80:
                    # Feste Spalten: Original ab 2, Neu ab 43, Status ab 84
                    original = line[2:42].strip()
                    neu      = line[42:82].strip()
                    status   = line[82:].strip()
                    if original and neu and status == "OK":
                        mapping[original] = neu
    except Exception:
        pass
    return mapping


# ------------------------------------------------------------------------------
# Hauptlogik
# ------------------------------------------------------------------------------

def main():
    log_lines  = []
    gesamt_ok  = True

    def out(line=""):
        """Ausgabe auf Konsole und in Log."""
        log_lines.append(line)
        print(line)

    out("=" * 72)
    out(f"  {SCRIPT_ID} — Handoff-Report SVG-Reihe")
    out(f"  R+MUNI Blueprint | SVG-Reihe | {ts()}")
    out("=" * 72)
    out()

    # --- 1. root.cfg ---
    out("--- 1. root.cfg ---")
    try:
        cfg        = get_root_cfg()
        rootfolder = cfg.get("<rootfolder>", "")
        stages     = cfg.get("<stages>", "")
        if not rootfolder:
            out("[FEHLER] <rootfolder> leer — root.cfg prüfen.")
            sys.exit(1)
        out(f"[OK     ] rootfolder = {rootfolder}")
    except Exception as e:
        out(f"[FEHLER ] root.cfg Fehler: {e}")
        sys.exit(1)

    out()

    # --- 2. svg_config.txt ---
    out("--- 2. svg_config.txt ---")
    config_path = os.path.join(rootfolder, "99-doku", CONFIG_NAME)
    if not os.path.isfile(config_path):
        out(f"[FEHLER ] svg_config.txt nicht gefunden: {config_path}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    try:
        svg_cfg       = parse_svg_config(config_path)
        source_folder = svg_cfg.get("svg_source_folder", "").strip()
        target_folder = svg_cfg.get("svg_target_folder", "").strip()
        out(f"[OK     ] svg_source_folder = {source_folder}")
        out(f"[OK     ] svg_target_folder = {target_folder}")
    except Exception as e:
        out(f"[FEHLER ] svg_config.txt nicht lesbar: {e}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    out()
    logs_dir = os.path.join(stages, "99-logs")

    # --- 3. Log-Status je Script ---
    out("--- 3. Script-Status ---")
    out()
    out(f"  {'SCRIPT':<8} {'LOG-DATEI':<40} {'VORHANDEN':<12} FEHLER")
    out(f"  {'-'*8} {'-'*40} {'-'*12} {'-'*8}")

    log_status = {}  # script_id → (vorhanden, hat_fehler)

    for script_id, log_datei in SVG_LOGS:
        log_path  = os.path.join(logs_dir, log_datei)
        vorhanden = os.path.isfile(log_path)
        fehler    = hat_fehler(log_path) if vorhanden else False

        log_status[script_id] = (vorhanden, fehler)

        if fehler:
            gesamt_ok = False

        status_str  = "JA" if vorhanden else "NEIN"
        fehler_str  = "JA ⚠" if fehler else ("NEIN" if vorhanden else "—")
        zeile = f"  {script_id:<8} {log_datei:<40} {status_str:<12} {fehler_str}"
        out(zeile)

    out()

    # --- 4. Zusammenfassungen je Script ---
    out("--- 4. Zusammenfassungen ---")

    for script_id, log_datei in SVG_LOGS:
        log_path = os.path.join(logs_dir, log_datei)
        vorhanden, fehler = log_status[script_id]

        if not vorhanden:
            out()
            out(f"  [{script_id}] Log nicht vorhanden — Script nicht ausgeführt.")
            continue

        out()
        out(f"  [{script_id}]")

        # SVG00 hat ERGEBNIS statt ZUSAMMENFASSUNG
        if script_id == "SVG00":
            ergebnis = lese_ergebnis(log_path)
            out(f"    {ergebnis}")
        else:
            zusammenfassung = lese_log_zusammenfassung(log_path)
            if zusammenfassung:
                for z in zusammenfassung:
                    out(f"    {z}")
            else:
                out(f"    Keine Zusammenfassung gefunden.")

    out()

    # --- 5. SVG-Zieldateien prüfen ---
    out("--- 5. SVG-Zieldateien ---")

    inventar_path = os.path.join(logs_dir, "SVG01-inventory.log")
    rename_path   = os.path.join(logs_dir, "SVG02-rename.log")

    if not os.path.isfile(inventar_path):
        out("[INFO   ] SVG01-inventory.log nicht vorhanden — Zielprüfung übersprungen.")
    elif not target_folder or not os.path.isdir(target_folder):
        out(f"[WARNUNG] svg_target_folder nicht gefunden: {target_folder}")
        out("[INFO   ] Zielprüfung übersprungen.")
    else:
        quelldateien  = parse_inventar_dateien(inventar_path)
        rename_map    = parse_rename_mapping(rename_path) if os.path.isfile(rename_path) else {}

        out()
        out(f"  {'QUELLDATEI':<40} {'SVG-ZIELDATEI':<40} {'STATUS':<10} GROESSE")
        out(f"  {'-'*40} {'-'*40} {'-'*10} {'-'*10}")

        zaehler = {"VORHANDEN": 0, "LEER": 0, "FEHLEND": 0}

        for quelldatei in quelldateien:
            # Umbenannten Namen verwenden wenn vorhanden
            aktueller_name = rename_map.get(quelldatei, quelldatei)
            name_ohne_ext  = os.path.splitext(aktueller_name)[0]
            svg_name       = name_ohne_ext + ".svg"
            svg_path       = os.path.join(target_folder, svg_name)

            if not os.path.isfile(svg_path):
                zeile = f"  {quelldatei:<40} {svg_name:<40} {'FEHLEND':<10} —"
                out(zeile)
                zaehler["FEHLEND"] += 1
                gesamt_ok = False
            elif os.path.getsize(svg_path) == 0:
                zeile = f"  {quelldatei:<40} {svg_name:<40} {'LEER':<10} 0 B"
                out(zeile)
                zaehler["LEER"] += 1
                gesamt_ok = False
            else:
                groesse = format_groesse(svg_path)
                zeile = f"  {quelldatei:<40} {svg_name:<40} {'VORHANDEN':<10} {groesse}"
                out(zeile)
                zaehler["VORHANDEN"] += 1

        out()
        out(f"  Erwartet  : {len(quelldateien)}")
        out(f"  Vorhanden : {zaehler['VORHANDEN']}")
        out(f"  Leer      : {zaehler['LEER']}")
        out(f"  Fehlend   : {zaehler['FEHLEND']}")

        # Umbenennungen ausgeben wenn vorhanden
        if rename_map:
            out()
            out(f"  Umbenennungen (SVG02):")
            for original, neu in rename_map.items():
                out(f"    {original}  →  {neu}")

    out()

    # --- Abschluss-Banner ---
    out("=" * 72)
    if gesamt_ok:
        out("  ERGEBNIS: OK — SVG-Reihe vollständig und fehlerfrei.")
    else:
        out("  ERGEBNIS: WARNUNG — Fehler oder fehlende Dateien gefunden.")
        out("            Logs der betroffenen Scripts prüfen.")
    out("=" * 72)

    _finalize(log_lines, stages, LOG_NAME)


def _finalize(log_lines, stages, log_name):
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
