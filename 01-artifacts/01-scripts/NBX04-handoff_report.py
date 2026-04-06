# NBX04-handoff_report.py
# NBX-Flow – Übergabe-Report
# Einzige Wirkung: nbx_trash.csv auswerten und menschenlesbaren
#                  Übergabe-Report mit Statistik und nächsten Schritten schreiben
# Voraussetzung: NBX03 erfolgreich
# Output: 02-stages\99-logs\NBX04-handoff_report.txt
# Folge:  ECM00
# Stage:  S1.02

import os
import sys
import csv
from datetime import datetime

# HLP00 direkt importieren (Blueprint-Standard)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HLP00_resolve_root import get_root_cfg

# ─── Konstanten ───────────────────────────────────────────────────────────────

SCRIPT_NAME    = "NBX04-handoff_report"
LOG_FILENAME   = "NBX04-handoff_report.log"
REPORT_FILENAME    = "NBX04-handoff_report.txt"
NBX00_OUT          = "NBX00-root.resolved.txt"
TRASH_FILENAME     = "trash_nbx.csv"
PROPERTIES_FILENAME = "properties_nbx.csv"

# ─── Logging ──────────────────────────────────────────────────────────────────

def log(msg, log_path):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ─── Hilfsfunktionen ──────────────────────────────────────────────────────────

def parse_resolved_txt(pfad):
    result = {}
    with open(pfad, "r", encoding="utf-8") as f:
        for zeile in f:
            zeile = zeile.strip()
            if not zeile or zeile.startswith("#"):
                continue
            if "=" in zeile:
                key, _, val = zeile.partition("=")
                result[key.strip()] = val.strip()
    return result


def lese_trash_csv(pfad):
    """nbx_trash.csv lesen, Statistik je nbx_objecttype zurückgeben."""
    zeilen      = []
    typ_zaehler = {}
    with open(pfad, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for zeile in reader:
            zeilen.append(zeile)
            typ = zeile.get("nbx_objecttype", "?")
            typ_zaehler[typ] = typ_zaehler.get(typ, 0) + 1
    return zeilen, typ_zaehler

# ─── Hauptlogik ───────────────────────────────────────────────────────────────

def main():

    # 1) root.cfg auflösen
    try:
        cfg = get_root_cfg()
    except Exception as e:
        print(f"[FEHLER] root.cfg konnte nicht aufgeloest werden: {e}")
        sys.exit(1)

    stages_dir = cfg["<stages>"]
    logs_dir   = os.path.join(stages_dir, "99-logs")
    log_path   = os.path.join(logs_dir, LOG_FILENAME)

    log("=" * 60, log_path)
    log(f"START {SCRIPT_NAME}", log_path)
    log("=" * 60, log_path)

    # 2) NBX00-root.resolved.txt lesen
    nbx00_path = os.path.join(logs_dir, NBX00_OUT)
    if not os.path.isfile(nbx00_path):
        log("[FEHLER] NBX00-root.resolved.txt nicht gefunden.", log_path)
        log("         Bitte zuerst NBX00-validate_environment.py ausfuehren.", log_path)
        sys.exit(1)

    resolved  = parse_resolved_txt(nbx00_path)
    child_dir = resolved.get("<childdir>", "")

    # 3) nbx_trash.csv lesen
    trash_pfad = os.path.join(child_dir, TRASH_FILENAME)
    if not os.path.isfile(trash_pfad):
        log(f"[FEHLER] nbx_trash.csv nicht gefunden: {trash_pfad}", log_path)
        log("         Bitte zuerst NBX03-normalize_to_csv.py ausfuehren.", log_path)
        sys.exit(1)

    zeilen, typ_zaehler = lese_trash_csv(trash_pfad)
    log(f"trash_nbx.csv gelesen     : {len(zeilen)} Zeile(n)", log_path)

    # properties_nbx.csv prüfen
    prop_pfad = os.path.join(child_dir, PROPERTIES_FILENAME)
    prop_count = 0
    if os.path.isfile(prop_pfad):
        with open(prop_pfad, "r", encoding="utf-8", newline="") as f:
            prop_count = sum(1 for _ in f) - 1  # Header abziehen
        log(f"properties_nbx.csv gelesen: {prop_count} Zeile(n)", log_path)
    else:
        log(f"[WARNUNG] properties_nbx.csv nicht gefunden: {prop_pfad}", log_path)

    # 4) Report aufbauen
    sep   = "=" * 60
    bericht = []
    bericht.append(sep)
    bericht.append("NBX-FLOW — ÜBERGABE-REPORT")
    bericht.append(sep)
    bericht.append(f"Erstellt   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    bericht.append(f"Stage      : S1.02")
    bericht.append(f"rootfolder : {cfg.get('<rootfolder>', '?')}")
    bericht.append("")

    bericht.append("── ERGEBNIS NBX03 ──────────────────────────────────────")
    bericht.append(f"trash_nbx.csv      : {trash_pfad}")
    bericht.append(f"Hosts gesamt       : {len(zeilen)}")
    bericht.append(f"properties_nbx.csv : {prop_pfad}")
    bericht.append(f"Properties gesamt  : {prop_count}")
    bericht.append("")

    bericht.append("── OBJEKTE JE TYP ──────────────────────────────────────")
    for typ, anzahl in sorted(typ_zaehler.items()):
        bericht.append(f"  {typ:20s}: {anzahl}")
    bericht.append("")

    bericht.append("── NÄCHSTE SCHRITTE ────────────────────────────────────")
    bericht.append("")
    bericht.append("  PHASE 1 — Erstmalig (Mapping-Modell noch nicht vorhanden):")
    bericht.append("    1. py ECM00-validate_environment.py")
    bericht.append("    2. py ECM01-csv_fields_to_artifacts.py")
    bericht.append("       → elements.csv in 02-csv\\04-import\\ erzeugt")
    bericht.append("    3. Archi: elements.csv importieren")
    bericht.append("    4. Archi: Mapping-Modell bauen")
    bericht.append("    5. Archi: OEF Export → 99-mappingmodel\\")
    bericht.append("")
    bericht.append("  PHASE 2 — Regulärer Lauf (Mapping-Modell vorhanden):")
    bericht.append("    1. py ECM00-validate_environment.py")
    bericht.append("    2. py ECM02-csv_to_mapping_to_csv.py")
    bericht.append("    3. Archi: elements.csv importieren")
    bericht.append("    4. py ECM03-id_merge.py")
    bericht.append("")
    bericht.append("  HINWEIS: nbx_raw.json in 02-stages\\ ist Zwischenartefakt")
    bericht.append("           → in .gitignore eintragen")
    bericht.append("")
    bericht.append(sep)
    bericht.append(f"NBX04 | R+MUNI Blueprint | S1.02")
    bericht.append(sep)

    # 5) Report schreiben
    report_pfad = os.path.join(logs_dir, REPORT_FILENAME)
    try:
        with open(report_pfad, "w", encoding="utf-8") as f:
            f.write("\n".join(bericht) + "\n")
        log(f"Report geschrieben: {report_pfad}", log_path)
    except Exception as e:
        log(f"[FEHLER] Report konnte nicht geschrieben werden: {e}", log_path)
        sys.exit(1)

    # Report auch auf Konsole
    print()
    for zeile in bericht:
        print(zeile)
    print()

    # 6) Abschluss
    log("=" * 60, log_path)
    log("ABSCHLUSS: Report erstellt — NBX-Flow abgeschlossen", log_path)
    log("=" * 60, log_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
