#!/usr/bin/env python3
# ATL02-atlCsv2JiraCsv.py
#
# Zweck (Flow-Stage):
# - atl_*.csv aus 03-stages/00-archimatearchive/ lesen
# - Eine Jira-Import-CSV generieren (alle Layer zusammengeführt)
# - Output (temporär, Import-Fragment):
#     <rootfolder>/03-stages/00-archimatearchive/jira_ea_import.csv
# - Log:
#     <rootfolder>/03-stages/99-logs/ATL02-atlCsv2JiraCsv.log
#
# Jira-Felder:
#   Summary           = Name des EA-Objekts (Pflicht)
#   Issue Type        = "Task" (Pflicht)
#   Description       = Beschreibung + EA-Kontext
#   Component/s       = ArchiMate Layer-Name (= Jira Komponente, vordefiniert)
#   Labels            = ArchiType (feingranularer Filter, z.B. ApplicationComponent)
#   External issue ID = objectKey (Merge-Schlüssel — verhindert Duplikate)
#   EA-ObjectKey      = objectKey (Referenz-ID für Verlinkung in Tickets)
#   EA-ArchiType      = ArchiMate Typ (lesbar)
#   EA-Layer          = Layer-Name (redundant zu Component/s, für Lesbarkeit)
#   EA-SourceModel    = Herkunftsmodell aus master.xml
#
# Merge-Logik (External issue ID):
#   Erster Import  → Issue wird neu angelegt, External issue ID gespeichert
#   Zweiter Import → Jira findet External issue ID → Update statt Duplikat
#
# Jira Komponenten (müssen im Projekt R+MUNI EA vorhanden sein):
#   Strategy
#   Business
#   Application
#   Technology & Physical
#   Motivation
#   Implementation & Migration
#   Relations
#   Other
#   Views  (reserviert für manuelle Einträge)
#
# Jira CSV-Import Regeln:
# - Erste Zeile = Spaltenheader (exakt wie Jira sie erwartet)
# - "Summary" ist Pflicht
# - "Issue Type" ist Pflicht
# - Encoding: UTF-8 mit BOM (für Jira CSV-Import mit Sonderzeichen)
#
# Workflow nach dem Script:
# 1. jira_ea_import.csv in Jira importieren:
#    Jira → Projekt R+MUNI EA → ... → Importieren → CSV
# 2. Feld-Mapping in Jira UI:
#    Summary           → Zusammenfassung   (Pflicht)
#    Issue Type        → Vorgangstyp       (Pflicht, Wert: Task / Aufgabe)
#    Description       → Beschreibung
#    Component/s       → Komponente/n
#    Labels            → Stichwörter
#    External issue ID → Externe Vorgangs-ID  (Merge-Schlüssel!)
# 3. Import starten
# 4. Confluence: Jira-Issues-Makro einbetten
#    Grob:  component = "Application"
#    Fein:  labels = "ApplicationComponent"
#
# Regeln:
# - Liest ATL00-root.resolved.txt als Root-Referenz
# - ATL01 muss vor ATL02 ausgeführt worden sein
# - Kein mkdir — Ordner müssen existieren (ATL00 hat das geprüft)
# - Hard fail bei jedem Fehler

import sys
import csv
import io
import os
from datetime import datetime


# ===========================================================
# KONSTANTEN
# ===========================================================

SCRIPT_KUERZEL = "ATL02"
LOG_FILENAME   = "ATL02-atlCsv2JiraCsv.log"
ROOT_RESOLVED  = "ATL00-root.resolved.txt"

IN_DIR_REL   = os.path.join("03-stages", "00-archimatearchive")
OUT_DIR_REL  = os.path.join("03-stages", "00-archimatearchive")
LOGS_DIR_REL = os.path.join("03-stages", "99-logs")

OUTPUT_FILENAME = "jira_ea_import.csv"

# Layer-Dateien: CSV-Dateiname-Stamm -> Layer-Name (= Jira Komponente)
# Reihenfolge bestimmt die Verarbeitungsreihenfolge
LAYER_DATEIEN: list[tuple[str, str]] = [
    ("atl_strategy",       "Strategy"),
    ("atl_business",       "Business"),
    ("atl_application",    "Application"),
    ("atl_technology",     "Technology & Physical"),
    ("atl_motivation",     "Motivation"),
    ("atl_implementation", "Implementation & Migration"),
    ("atl_relations",      "Relations"),
    ("atl_other",          "Other"),
]

# Jira CSV-Spalten (exakt in dieser Reihenfolge)
# Spaltennamen müssen dem exakten Jira-Feldnamen entsprechen
JIRA_SPALTEN = [
    "Summary",            # Pflicht — Name des EA-Objekts
    "Issue Type",         # Pflicht — immer "Task"
    "Description",        # Freitext — aus master.xml documentation + EA-Kontext
    "Component/s",        # ArchiMate Layer (= Jira Komponente, vordefiniert)
    "Labels",             # ArchiType (feingranular, z.B. ApplicationComponent)
    "External issue ID",  # objectKey — Merge-Schlüssel (verhindert Duplikate)
    "EA-ObjectKey",       # Archi identifier — für Referenz & Verlinkung
    "EA-ArchiType",       # ArchiMate Typ (lesbar, redundant zu Labels)
    "EA-Layer",           # Layer-Name (redundant zu Component/s, für Lesbarkeit)
    "EA-SourceModel",     # Herkunftsmodell aus master.xml
]

JIRA_ISSUE_TYPE = "Task"


# ===========================================================
# HILFSFUNKTIONEN
# ===========================================================

def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str, log_path: str) -> None:
    line = f"[{SCRIPT_KUERZEL}] {now_ts()} | {message}"
    print(line)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def die(message: str, log_path: str | None = None) -> None:
    line = f"[{SCRIPT_KUERZEL}] {now_ts()} | ERROR | {message}"
    print(line, file=sys.stderr)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    sys.exit(1)


# ===========================================================
# ROOT AUFLÖSEN
# ===========================================================

def resolve_root(script_dir: str) -> str:
    logs_candidate = os.path.abspath(
        os.path.join(script_dir, "..", "..", "03-stages", "99-logs")
    )
    resolved_file = os.path.join(logs_candidate, ROOT_RESOLVED)

    if not os.path.isfile(resolved_file):
        die(
            f"ATL00-root.resolved.txt nicht gefunden: {resolved_file}\n"
            f"  → Bitte zuerst ATL00 ausführen.",
            None,
        )

    with open(resolved_file, "r", encoding="utf-8") as f:
        root_path = f.readline().strip()

    if not root_path or not os.path.isdir(root_path):
        die(
            f"Ungültiger Root-Pfad in ATL00-root.resolved.txt: '{root_path}'",
            None,
        )

    return root_path


# ===========================================================
# CSV LESEN
# ===========================================================

def lese_csv(pfad: str, log_path: str) -> tuple[list[str], list[dict]]:
    if not os.path.isfile(pfad):
        log(f"  Nicht gefunden (übersprungen): {os.path.basename(pfad)}", log_path)
        return [], []

    try:
        with open(pfad, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            spalten = list(reader.fieldnames or [])
            zeilen  = list(reader)
        log(f"  Gelesen: {os.path.basename(pfad)} | {len(zeilen)} Zeilen", log_path)
        return spalten, zeilen
    except Exception as e:
        die(f"CSV nicht lesbar: {pfad} | {e}", log_path)


# ===========================================================
# JIRA-ZEILE BAUEN
# ===========================================================

def baue_jira_zeile(
    atl_zeile: dict,
    layer_name: str,
) -> dict:
    """
    Konvertiert eine atl_*.csv Zeile in eine Jira-Import-Zeile.

    Summary          : Name des EA-Objekts (Fallback: [ArchiType] objectKey)
    Component/s      : Layer-Name (= Jira Komponente, exakter Name erforderlich)
    Labels           : ArchiType ohne Leerzeichen (feingranularer Filter)
    External issue ID: objectKey (Merge-Schlüssel für Update statt Duplikat)
    """
    obj_key      = atl_zeile.get("objectKey", "").strip()
    archi_type   = atl_zeile.get("ArchiType", "").strip()
    name         = atl_zeile.get("Name", "").strip()
    description  = atl_zeile.get("Description", "").strip()
    source_model = atl_zeile.get("SourceModel", "").strip()
    bpmn_id      = atl_zeile.get("BPMN_ID", "").strip()

    # Summary — Pflichtfeld, darf nicht leer sein
    summary = name if name else (
        f"[{archi_type}] {obj_key}" if archi_type else obj_key
    )

    # Description — Kontext anreichern
    desc_teile = []
    if description:
        desc_teile.append(description)
        desc_teile.append("")  # Leerzeile als Trenner
    desc_teile.append(f"EA-ObjectKey: {obj_key}")
    desc_teile.append(f"ArchiType: {archi_type}")
    desc_teile.append(f"Layer: {layer_name}")
    if source_model:
        desc_teile.append(f"SourceModel: {source_model}")
    if bpmn_id:
        desc_teile.append(f"BPMN-ID: {bpmn_id}")

    # Labels — Leerzeichen nicht erlaubt in Jira Labels → Underscore
    label = archi_type.replace(" ", "_") if archi_type else "EA_Object"

    return {
        "Summary":           summary,
        "Issue Type":        JIRA_ISSUE_TYPE,
        "Description":       "\n".join(desc_teile),
        "Component/s":       layer_name,
        "Labels":            label,
        "External issue ID": obj_key,
        "EA-ObjectKey":      obj_key,
        "EA-ArchiType":      archi_type,
        "EA-Layer":          layer_name,
        "EA-SourceModel":    source_model,
    }


# ===========================================================
# JIRA CSV SCHREIBEN
# ===========================================================

def schreibe_jira_csv(
    pfad: str,
    zeilen: list[dict],
    log_path: str,
) -> None:
    """
    Schreibt die Jira-Import-CSV.
    UTF-8 mit BOM — Jira CSV-Import erwartet das für Sonderzeichen.
    Überschreibt bestehende Datei.
    """
    if not os.path.isdir(os.path.dirname(pfad)):
        die(f"Ausgabe-Ordner fehlt: {os.path.dirname(pfad)}", log_path)

    buf = io.StringIO()
    writer = csv.DictWriter(
        buf,
        fieldnames=JIRA_SPALTEN,
        quoting=csv.QUOTE_ALL,
        extrasaction="ignore",
        restval="",
        lineterminator="\r\n",
    )
    writer.writeheader()
    writer.writerows(zeilen)

    # UTF-8 mit BOM (Jira-kompatibel für Sonderzeichen)
    with open(pfad, "w", encoding="utf-8-sig", newline="") as f:
        f.write(buf.getvalue())

    log(f"  Geschrieben: {os.path.basename(pfad)} | {len(zeilen)} Zeilen", log_path)


# ===========================================================
# MAIN
# ===========================================================

def main() -> None:
    sdir      = os.path.dirname(os.path.abspath(__file__))
    root_path = resolve_root(sdir)

    logs_dir = os.path.join(root_path, LOGS_DIR_REL)
    log_path = os.path.join(logs_dir, LOG_FILENAME)

    log("=" * 60, log_path)
    log(f"ATL02 START | {now_ts()}", log_path)
    log(f"BLUEPRINT_ROOT: {root_path}", log_path)

    in_dir  = os.path.join(root_path, IN_DIR_REL)
    out_dir = os.path.join(root_path, OUT_DIR_REL)

    if not os.path.isdir(in_dir):
        die(f"Input-Ordner fehlt: {in_dir}", log_path)

    # Alle Layer-CSVs lesen und zu Jira-Zeilen umwandeln
    log("-" * 60, log_path)
    log("Lese Layer-CSVs...", log_path)

    alle_jira_zeilen: list[dict] = []
    stats_pro_layer:  list[tuple[str, int]] = []

    for datei_stamm, layer_name in LAYER_DATEIEN:
        pfad = os.path.join(in_dir, f"{datei_stamm}.csv")
        _, zeilen = lese_csv(pfad, log_path)

        jira_zeilen = [baue_jira_zeile(z, layer_name) for z in zeilen]
        alle_jira_zeilen.extend(jira_zeilen)
        stats_pro_layer.append((layer_name, len(jira_zeilen)))

    if not alle_jira_zeilen:
        die(
            "Keine Zeilen aus atl_*.csv gelesen.\n"
            "  → Bitte zuerst ATL01 ausführen.",
            log_path,
        )

    # Jira-Import-CSV schreiben
    log("-" * 60, log_path)
    log("Schreibe Jira-Import-CSV...", log_path)

    out_pfad = os.path.join(out_dir, OUTPUT_FILENAME)
    schreibe_jira_csv(out_pfad, alle_jira_zeilen, log_path)

    # Zusammenfassung
    log("-" * 60, log_path)
    log("Zeilen pro Layer:", log_path)
    for layer_name, anzahl in stats_pro_layer:
        log(f"  {layer_name:<30} {anzahl:>5} Zeilen", log_path)
    log(f"  {'GESAMT':<30} {len(alle_jira_zeilen):>5} Zeilen", log_path)
    log("-" * 60, log_path)
    log(f"Output: {out_pfad}", log_path)
    log("=" * 60, log_path)
    log("ATL02 ERFOLGREICH", log_path)

    print(
        f"[ATL02] OK | {len(alle_jira_zeilen)} Zeilen -> "
        f"03-stages/00-archimatearchive/{OUTPUT_FILENAME}"
    )


if __name__ == "__main__":
    main()
