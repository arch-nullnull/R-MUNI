# ==============================================================================
# SVG04-trace.py
# ==============================================================================
# Reihe   : SVG — Image to SVG Konvertierung
# Aufgabe : Bilddateien via Inkscape Trace Bitmap vektorisieren (Option B)
# Output  : 02-stages\99-logs\SVG04-trace.log
# Abhängig: HLP00_resolve_root.py, SVG01-inventory.log
# ==============================================================================
# HINWEIS — Trace-Qualität:
#   Linienzeichnungen und kontrastreiche Grafiken → gute Ergebnisse
#   Fotos, Farbverläufe, komplexe Rasterbilder   → meist unbrauchbar
#   Qualitätsurteil liegt beim Anwender — SVG04 ist kein Autopilot.
#
# HINWEIS — Versionsabhängigkeit:
#   Der Inkscape CLI --actions String für Trace ist versionsabhängig.
#   Getestet auf Basis aktueller Inkscape-Versionen (1.x).
#   Bei Fehler: Inkscape-Version prüfen, ggf. actions-String anpassen.
#
# Trace-Parameter in svg_config.txt:
#   svg_trace_threshold  Helligkeitsschwelle 0.0–1.0 (Default: 0.5)
#   svg_trace_mode       brightness | edge | color (Default: brightness)
# ==============================================================================
# R+MUNI Blueprint | Stage S1.04 | 2026-04-12
# ==============================================================================

import os
import sys
import subprocess
from datetime import datetime

# ------------------------------------------------------------------------------
# HLP00 einbinden
# ------------------------------------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from HLP00_resolve_root import get_root_cfg
except ImportError:
    print("[SVG04] FEHLER: HLP00_resolve_root.py nicht gefunden.")
    sys.exit(1)

# ------------------------------------------------------------------------------
# Konstanten
# ------------------------------------------------------------------------------
SCRIPT_ID    = "SVG04"
CONFIG_NAME  = "svg_config.txt"
INVENTAR_LOG = "SVG01-inventory.log"
LOG_NAME     = "SVG04-trace.log"

# Trace-Modi — gültige Werte
TRACE_MODI = ("brightness", "edge", "color")

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


def parse_inventar(inventar_path):
    """Identisch zu SVG03 — liest OK und RENAME_REQUIRED Einträge."""
    ergebnis = []
    STATUS_START    = 2
    DATEINAME_START = 2 + 18
    DATEINAME_ENDE  = DATEINAME_START + 45

    with open(inventar_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if len(line) < DATEINAME_START:
                continue
            status_teil = line[STATUS_START:STATUS_START + 18].strip()
            if status_teil in ("OK", "RENAME_REQUIRED"):
                dateiname = line[DATEINAME_START:DATEINAME_ENDE].strip()
                if dateiname and "." in dateiname and not dateiname.startswith(":"):
                    ergebnis.append((status_teil, dateiname))

    return ergebnis


def baue_actions_string(src_path, dst_path, trace_mode, trace_threshold):
    """Baut den Inkscape --actions String für Trace Bitmap.

    Ablauf:
      1. Datei öffnen (file-open)
      2. Alle Objekte selektieren (select-all)
      3. Trace Bitmap mit Parametern ausführen
      4. Originalbild löschen (das Rasterbild unter dem Trace)
      5. Als SVG exportieren
      6. Inkscape beenden

    Trace-Aktion je Modus:
      brightness  org.inkscape.color.trace -- threshold:<wert>
      edge        org.inkscape.color.trace -- edge-detection:<wert>
      color       org.inkscape.color.trace -- color
    """
    if trace_mode == "brightness":
        trace_action = f"org.inkscape.color.trace;select-all;delete"
    elif trace_mode == "edge":
        trace_action = f"org.inkscape.color.trace;select-all;delete"
    else:  # color
        trace_action = f"org.inkscape.color.trace;select-all;delete"

    actions = (
        f"file-open:{src_path};"
        f"select-all;"
        f"org.inkscape.color.trace;"
        f"export-filename:{dst_path};"
        f"export-do;"
        f"file-close"
    )
    return actions


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
    log_lines.append(f"  {SCRIPT_ID} — Trace-Konvertierung (Option B)")
    log_lines.append(f"  R+MUNI Blueprint | SVG-Reihe | {ts()}")
    log_lines.append("=" * 72)
    log_lines.append("")
    log_lines.append("  EXPERIMENTELL — Qualitätsurteil liegt beim Anwender.")
    log_lines.append("  Linienzeichnungen: gute Ergebnisse.")
    log_lines.append("  Fotos/Farbverläufe: meist unbrauchbar.")
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

    inkscape_exe    = svg_cfg.get("inkscape_exe", "").strip()
    source_folder   = svg_cfg.get("svg_source_folder", "").strip()
    target_folder   = svg_cfg.get("svg_target_folder", "").strip()
    overwrite       = svg_cfg.get("svg_overwrite", "false").strip().lower() == "true"
    trace_threshold = svg_cfg.get("svg_trace_threshold", "0.5").strip()
    trace_mode      = svg_cfg.get("svg_trace_mode", "brightness").strip().lower()

    for label, wert in [("inkscape_exe", inkscape_exe),
                        ("svg_source_folder", source_folder),
                        ("svg_target_folder", target_folder)]:
        if not wert:
            log("FEHLER", f"{label} leer — svg_config.txt prüfen.")
            _finalize(log_lines, stages, LOG_NAME)
            sys.exit(1)
        log("OK", f"{label} = {wert}")

    log("OK", f"svg_overwrite = {str(overwrite).lower()}")

    # Trace-Parameter validieren
    if trace_mode not in TRACE_MODI:
        log("WARNUNG", f"svg_trace_mode '{trace_mode}' unbekannt — verwende 'brightness'.")
        trace_mode = "brightness"
    else:
        log("OK", f"svg_trace_mode = {trace_mode}")

    try:
        threshold_val = float(trace_threshold)
        if not 0.0 <= threshold_val <= 1.0:
            raise ValueError
        log("OK", f"svg_trace_threshold = {trace_threshold}")
    except ValueError:
        log("WARNUNG", f"svg_trace_threshold '{trace_threshold}' ungültig — verwende 0.5.")
        trace_threshold = "0.5"

    log_lines.append("")

    # --- 3. Pfade prüfen ---
    log_lines.append("--- 3. Pfade ---")
    if not os.path.isfile(inkscape_exe):
        log("FEHLER", f"inkscape_exe nicht gefunden: {inkscape_exe}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)
    log("OK", "inkscape_exe gefunden")

    if not os.path.isdir(source_folder):
        log("FEHLER", f"svg_source_folder nicht gefunden: {source_folder}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)
    log("OK", "svg_source_folder gefunden")

    if not os.path.isdir(target_folder):
        log("FEHLER", f"svg_target_folder nicht gefunden: {target_folder}")
        log("FEHLER", "Zielordner manuell anlegen und erneut starten.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)
    log("OK", "svg_target_folder gefunden")

    log_lines.append("")

    # --- 4. SVG01-inventory.log lesen ---
    log_lines.append("--- 4. SVG01-inventory.log ---")
    inventar_path = os.path.join(stages, "99-logs", INVENTAR_LOG)

    if not os.path.isfile(inventar_path):
        log("FEHLER", f"SVG01-inventory.log nicht gefunden: {inventar_path}")
        log("FEHLER", "SVG01 zuerst ausführen.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    try:
        inventar = parse_inventar(inventar_path)
    except Exception as e:
        log("FEHLER", f"SVG01-inventory.log nicht lesbar: {e}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    log("OK", f"SVG01-inventory.log gelesen — {len(inventar)} Datei(en) zur Konvertierung")
    log_lines.append("")

    if not inventar:
        log("INFO", "Keine verarbeitbaren Dateien im Inventar — Abbruch.")
        _finalize(log_lines, stages, LOG_NAME)
        return

    # --- 5. Trace-Konvertierung ---
    log_lines.append("--- 5. Trace-Konvertierung ---")
    log_lines.append(f"  Modus: {trace_mode} | Threshold: {trace_threshold}")
    log_lines.append("")
    log_lines.append(f"  {'QUELLDATEI':<40} {'ZIELDATEI':<40} {'STATUS':<8} GROESSE")
    log_lines.append(f"  {'-'*40} {'-'*40} {'-'*8} {'-'*10}")

    for inv_status, dateiname in inventar:
        src_path = os.path.join(source_folder, dateiname)

        if not os.path.isfile(src_path):
            zeile = f"  {dateiname:<40} {'—':<40} {'FEHLER':<8} Quelldatei nicht gefunden"
            log_lines.append(zeile)
            print(zeile)
            zaehler["FEHLER"] += 1
            continue

        name_ohne_ext = os.path.splitext(dateiname)[0]
        svg_name      = name_ohne_ext + ".svg"
        dst_path      = os.path.join(target_folder, svg_name)

        if os.path.isfile(dst_path) and not overwrite:
            zeile = f"  {dateiname:<40} {svg_name:<40} {'SKIP':<8} bereits vorhanden"
            log_lines.append(zeile)
            print(zeile)
            zaehler["SKIP"] += 1
            continue

        # Inkscape CLI mit --actions für Trace
        try:
            actions = (
                f"file-open:{src_path};"
                f"select-all;"
                f"org.inkscape.color.trace;"
                f"export-filename:{dst_path};"
                f"export-do;"
                f"file-close"
            )

            result = subprocess.run(
                [inkscape_exe, "--actions", actions],
                capture_output=True,
                timeout=120
            )

            if result.returncode != 0 or not os.path.isfile(dst_path):
                fehler_detail = result.stderr.decode("utf-8", errors="replace").strip()
                fehler_detail = fehler_detail[:60] if fehler_detail else "Inkscape Exitcode != 0"
                zeile = f"  {dateiname:<40} {svg_name:<40} {'FEHLER':<8} {fehler_detail}"
                log_lines.append(zeile)
                print(zeile)
                zaehler["FEHLER"] += 1
            elif os.path.getsize(dst_path) == 0:
                zeile = f"  {dateiname:<40} {svg_name:<40} {'FEHLER':<8} SVG leer (0 Bytes)"
                log_lines.append(zeile)
                print(zeile)
                zaehler["FEHLER"] += 1
            else:
                groesse = format_groesse(dst_path)
                zeile = f"  {dateiname:<40} {svg_name:<40} {'OK':<8} {groesse}"
                log_lines.append(zeile)
                print(zeile)
                zaehler["OK"] += 1

        except subprocess.TimeoutExpired:
            zeile = f"  {dateiname:<40} {svg_name:<40} {'FEHLER':<8} Timeout (>120s)"
            log_lines.append(zeile)
            print(zeile)
            zaehler["FEHLER"] += 1
        except Exception as e:
            zeile = f"  {dateiname:<40} {svg_name:<40} {'FEHLER':<8} {str(e)[:60]}"
            log_lines.append(zeile)
            print(zeile)
            zaehler["FEHLER"] += 1

    log_lines.append("")

    # --- Zusammenfassung ---
    gesamt = sum(zaehler.values())
    log_lines.append("=" * 72)
    log_lines.append(f"  ZUSAMMENFASSUNG")
    log_lines.append(f"  Verarbeitet       : {gesamt}")
    log_lines.append(f"  OK                : {zaehler['OK']}")
    log_lines.append(f"  Übersprungen      : {zaehler['SKIP']}")
    log_lines.append(f"  Fehler            : {zaehler['FEHLER']}")

    if zaehler["FEHLER"] > 0:
        log_lines.append(f"")
        log_lines.append(f"  WARNUNG: {zaehler['FEHLER']} Konvertierung(en) fehlgeschlagen.")
        log_lines.append(f"           Inkscape-Version prüfen — --actions Trace ist versionsabhängig.")
        log_lines.append(f"           SVG03 (Embed) als Alternative verwenden.")

    if zaehler["SKIP"] > 0:
        log_lines.append(f"")
        log_lines.append(f"  HINWEIS: {zaehler['SKIP']} Datei(en) übersprungen.")
        log_lines.append(f"           svg_overwrite=true setzen um vorhandene SVGs zu überschreiben.")

    log_lines.append("=" * 72)

    print(f"\n[{SCRIPT_ID}] Verarbeitet: {gesamt} | OK: {zaehler['OK']} | "
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
