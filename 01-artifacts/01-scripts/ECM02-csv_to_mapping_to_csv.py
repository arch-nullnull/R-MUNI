# ECM02-csv_to_mapping_to_csv.py
# EasyCSVMapper – Müll-CSV mit OEF Mapping zu Archi-Import-CSVs
# Liest trash_*.csv aus 00-archimatechild\
# Liest OEF Mapping-Modell aus 99-mappingmodel\ (MAPPING= aus run-scope.txt)
# Schreibt:
#   04-import\elements.csv                        ← direkt Archi-importfertig
#   02-stages\00-archimatearchive\properties.csv  ← geparkt, noch ID-los
#   02-stages\00-archimatearchive\relations.csv   ← geparkt, noch ID-los
#
# Mapping-Logik (aus OEF):
#   Element OHNE eingehende Association → eigenständiges Element (Typ aus OEF)
#   Element MIT eingehender Association → Property des Ziel-Elements
#     Key   = Name des Quell-Elements (= CSV-Spaltenname)
#     Value = Wert aus CSV-Datenzeile
#
# Voraussetzung: ECM00 + ECM01 erfolgreich, run-scope.txt mit MAPPING= befüllt

import os
import sys
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HLP00_resolve_root import get_root_cfg

# ─── Konstanten ───────────────────────────────────────────────────────────────

SCRIPT_NAME  = "ECM02-csv_to_mapping_to_csv"
LOG_FILENAME = "ECM02-csv_to_mapping_to_csv.log"
ECM00_OUT    = "ECM00-root.resolved.txt"

ARCHI_ELEMENTS_HEADER   = ["ID", "Type", "Name", "Documentation", "Specialization"]
ARCHI_RELATIONS_HEADER  = ["ID", "Type", "Name", "Documentation", "Source", "Target", "Specialization"]
ARCHI_PROPERTIES_HEADER = ["ID", "Key", "Value"]

ENCODINGS    = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]
TRENNZEICHEN = [";", ",", "\t", "|"]

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


def erkenne_encoding(pfad):
    for enc in ENCODINGS:
        try:
            with open(pfad, "r", encoding=enc) as f:
                zeilen = f.readlines()
            return enc, zeilen
        except (UnicodeDecodeError, LookupError):
            continue
    raise ValueError(f"Kein passendes Encoding gefunden: {os.path.basename(pfad)}")


def erkenne_trennzeichen(zeilen):
    probe = zeilen[:min(5, len(zeilen))]
    bestes = None
    beste_anzahl = 0
    for trenner in TRENNZEICHEN:
        anzahlen = [zeile.count(trenner) for zeile in probe]
        if min(anzahlen) > 0 and min(anzahlen) == max(anzahlen):
            if anzahlen[0] > beste_anzahl:
                beste_anzahl = anzahlen[0]
                bestes = trenner
    if bestes is None:
        for trenner in TRENNZEICHEN:
            anzahl = sum(zeile.count(trenner) for zeile in probe)
            if anzahl > beste_anzahl:
                beste_anzahl = anzahl
                bestes = trenner
    return bestes


def lese_trash_csv(pfad, log_path):
    """Liest trash_*.csv mit auto-Encoding und auto-Trennzeichen."""
    enc, zeilen = erkenne_encoding(pfad)
    log(f"  Encoding   : {enc}", log_path)
    trenner = erkenne_trennzeichen(zeilen)
    log(f"  Trennzeichen: {repr(trenner)}", log_path)
    with open(pfad, "r", encoding=enc, newline="") as f:
        reader = csv.DictReader(f, delimiter=trenner)
        rows = list(reader)
    # Spaltenköpfe bereinigen (strip)
    if rows:
        erste = rows[0]
        saubere_keys = {k: k.strip() for k in erste.keys()}
        rows = [{saubere_keys[k]: v.strip() for k, v in row.items()} for row in rows]
    log(f"  Zeilen      : {len(rows)}", log_path)
    return rows


def parse_oef_mapping(xml_pfad, log_path):
    """
    Liest OEF XML und gibt Mapping-Struktur zurück:

    elemente: dict { identifier → {"name": str, "typ": str} }
    associations: list [ {"source": id, "target": id} ]

    Daraus abgeleitete Logik:
      - Element dessen identifier als SOURCE in einer Association vorkommt
        → wird Property des TARGET-Elements
      - Element ohne SOURCE-Rolle → eigenständiges Element
    """
    tree = ET.parse(xml_pfad)
    root = tree.getroot()

    # Namespace-agnostisch
    def tag(el):
        return el.tag.split("}")[-1]

    elemente = {}
    for el in root.iter():
        if tag(el) == "element":
            ident = el.get("identifier", "")
            typ   = el.get("{http://www.w3.org/2001/XMLSchema-instance}type", "")
            name  = ""
            for child in el:
                if tag(child) == "name":
                    name = (child.text or "").strip()
                    break
            if ident:
                elemente[ident] = {"name": name, "typ": typ}

    associations = []
    for rel in root.iter():
        if tag(rel) == "relationship":
            rel_typ = rel.get("{http://www.w3.org/2001/XMLSchema-instance}type", "")
            if rel_typ == "Association":
                source = rel.get("source", "")
                target = rel.get("target", "")
                if source and target:
                    associations.append({"source": source, "target": target})

    log(f"  OEF Elemente    : {len(elemente)}", log_path)
    log(f"  OEF Associations: {len(associations)}", log_path)

    # Welche IDs sind SOURCE einer Association?
    property_sources = {a["source"] for a in associations}

    # Mapping aufbauen: name → {"typ", "ist_property", "target_name"}
    mapping = {}
    for ident, info in elemente.items():
        name = info["name"]
        if ident in property_sources:
            # Ziel-Element finden
            target_id = next(
                (a["target"] for a in associations if a["source"] == ident),
                None
            )
            target_name = elemente[target_id]["name"] if target_id and target_id in elemente else ""
            mapping[name] = {
                "typ":         info["typ"],
                "ist_property": True,
                "target_name": target_name
            }
            log(f"    Property : {name} → Attribut von '{target_name}'", log_path)
        else:
            mapping[name] = {
                "typ":         info["typ"],
                "ist_property": False,
                "target_name": ""
            }
            log(f"    Element  : {name} → Typ {info['typ']}", log_path)

    return mapping


def leere_master_csvs(import_dir, log_path):
    """Leert nur elements.csv auf Header-Stand — properties/relations gehen in archive."""
    pfad = os.path.join(import_dir, "elements.csv")
    with open(pfad, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(ARCHI_ELEMENTS_HEADER)
    log(f"  Geleert: elements.csv", log_path)


def schreibe_csvs(import_dir, archive_dir, trash_rows, mapping, log_path):
    """
    Verarbeitet jede Datenzeile der trash_*.csv:
    - Felder ohne Property-Rolle → elements.csv  → 04-import\
    - Felder mit Property-Rolle  → properties.csv → 00-archimatearchive\ (ID-los, geparkt)
    - relations.csv              → 00-archimatearchive\ (nur Header)
    """

    element_spalten  = {k: v for k, v in mapping.items() if not v["ist_property"]}
    property_spalten = {k: v for k, v in mapping.items() if v["ist_property"]}

    if trash_rows:
        alle_spalten  = set(trash_rows[0].keys())
        nicht_gemappt = alle_spalten - set(mapping.keys())
        if nicht_gemappt:
            log(f"  [WARNUNG] Spalten nicht im Mapping — werden ignoriert: {nicht_gemappt}", log_path)

    el_pfad   = os.path.join(import_dir,  "elements.csv")
    prop_pfad = os.path.join(archive_dir, "properties.csv")
    rel_pfad  = os.path.join(archive_dir, "relations.csv")

    # relations.csv — nur Header, geparkt
    with open(rel_pfad, "w", encoding="utf-8", newline="") as rel_f:
        csv.writer(rel_f, quoting=csv.QUOTE_ALL).writerow(ARCHI_RELATIONS_HEADER)

    el_count   = 0
    prop_count = 0

    with open(el_pfad,   "a", encoding="utf-8", newline="") as el_f, \
         open(prop_pfad, "w", encoding="utf-8", newline="") as prop_f:

        el_writer   = csv.writer(el_f,   quoting=csv.QUOTE_ALL)
        prop_writer = csv.writer(prop_f, quoting=csv.QUOTE_ALL)
        prop_writer.writerow(ARCHI_PROPERTIES_HEADER)

        for row in trash_rows:
            for spalte, info in element_spalten.items():
                wert = row.get(spalte, "")
                el_writer.writerow(["", info["typ"], wert, "", ""])
                el_count += 1

            for spalte, info in property_spalten.items():
                wert = row.get(spalte, "")
                prop_writer.writerow(["", spalte, wert])
                prop_count += 1

    log(f"  elements.csv   → 04-import         : {el_count} Zeilen", log_path)
    log(f"  properties.csv → 00-archimatearchive: {prop_count} Zeilen (ID-los, geparkt)", log_path)
    log(f"  relations.csv  → 00-archimatearchive: nur Header (geparkt)", log_path)

# ─── Hauptlogik ───────────────────────────────────────────────────────────────

def main():

    try:
        cfg = get_root_cfg()
    except Exception as e:
        print(f"[FEHLER] root.cfg konnte nicht aufgeloest werden: {e}")
        sys.exit(1)

    stages_dir    = cfg["<stages>"]
    artifacts_dir = cfg["<artifacts>"]
    models_dir    = cfg["<models>"]
    logs_dir      = os.path.join(stages_dir, "99-logs")
    log_path      = os.path.join(logs_dir, LOG_FILENAME)

    log("=" * 60, log_path)
    log(f"START {SCRIPT_NAME}", log_path)
    log("=" * 60, log_path)

    fehler = []

    # 1) ECM00-root.resolved.txt lesen
    ecm00_path = os.path.join(logs_dir, ECM00_OUT)
    if not os.path.isfile(ecm00_path):
        log("[FEHLER] ECM00-root.resolved.txt nicht gefunden.", log_path)
        log("         Bitte zuerst ECM00 ausfuehren.", log_path)
        sys.exit(1)

    resolved          = parse_resolved_txt(ecm00_path)
    mapping_model_dir = resolved.get("<mappingmodel>", "")
    child_dir         = resolved.get("<childdir>", "")
    import_dir        = os.path.join(artifacts_dir, "02-csv", "04-import")
    archive_dir       = os.path.join(stages_dir, "00-archimatearchive")

    log(f"child_dir   : {child_dir}", log_path)
    log(f"mappingmodel: {mapping_model_dir}", log_path)
    log(f"import_dir  : {import_dir}", log_path)
    log(f"archive_dir : {archive_dir}", log_path)

    # 2) run-scope.txt lesen → MAPPING= auflösen
    run_scope_path = os.path.join(stages_dir, "run-scope.txt")
    if not os.path.isfile(run_scope_path):
        log(f"[FEHLER] run-scope.txt nicht gefunden: {run_scope_path}", log_path)
        sys.exit(1)

    mapping_name = None
    aktuell = {}
    with open(run_scope_path, "r", encoding="utf-8") as f:
        for zeile in f:
            zeile = zeile.strip()
            if not zeile or zeile.startswith("#"):
                continue
            if "=" in zeile:
                key, _, val = zeile.partition("=")
                key = key.strip().upper()
                val = val.strip()
                if key == "SOURCE" and aktuell:
                    aktuell = {}
                aktuell[key] = val
                if key == "MAPPING":
                    mapping_name = val
                    break

    if not mapping_name:
        log("[FEHLER] Kein MAPPING= Eintrag in run-scope.txt gefunden.", log_path)
        log("         Beispiel:", log_path)
        log("           SOURCE=CSV", log_path)
        log("           MODEL=trash_test.csv", log_path)
        log("           MAPPING=trash_test", log_path)
        sys.exit(1)

    log(f"MAPPING     : {mapping_name}", log_path)

    # 3) OEF XML finden — MAPPING= Wert ist direkt der Dateiname inkl. Extension
    xml_pfad = os.path.join(mapping_model_dir, mapping_name)
    if not os.path.isfile(xml_pfad):
        log(f"[FEHLER] OEF XML nicht gefunden: {xml_pfad}", log_path)
        sys.exit(1)

    log(f"OEF XML     : {xml_pfad}", log_path)

    # 4) trash_*.csv finden
    trash_files = sorted([
        f for f in os.listdir(child_dir)
        if f.lower().startswith("trash_") and f.lower().endswith(".csv")
    ])

    if not trash_files:
        log("[FEHLER] Keine trash_*.csv gefunden.", log_path)
        sys.exit(1)

    if len(trash_files) > 1:
        log(f"[FEHLER] Mehrere trash_*.csv gefunden — nur eine pro Lauf erlaubt.", log_path)
        for f in trash_files:
            log(f"  {f}", log_path)
        sys.exit(1)

    trash_pfad = os.path.join(child_dir, trash_files[0])
    log(f"trash_*.csv : {trash_files[0]}", log_path)

    # 5) OEF Mapping parsen
    log("Lese OEF Mapping ...", log_path)
    try:
        mapping = parse_oef_mapping(xml_pfad, log_path)
    except Exception as e:
        log(f"[FEHLER] OEF XML konnte nicht gelesen werden: {e}", log_path)
        sys.exit(1)

    # 6) trash_*.csv lesen
    log(f"Lese trash_*.csv ...", log_path)
    try:
        trash_rows = lese_trash_csv(trash_pfad, log_path)
    except Exception as e:
        log(f"[FEHLER] trash_*.csv konnte nicht gelesen werden: {e}", log_path)
        sys.exit(1)

    # 7) Master-CSVs leeren
    log("Leere Master-CSVs in 04-import ...", log_path)
    try:
        leere_master_csvs(import_dir, log_path)
    except Exception as e:
        log(f"[FEHLER] Master-CSVs konnten nicht geleert werden: {e}", log_path)
        sys.exit(1)

    # 8) CSVs schreiben
    log("Schreibe elements/relations/properties.csv ...", log_path)
    try:
        schreibe_csvs(import_dir, archive_dir, trash_rows, mapping, log_path)
    except Exception as e:
        log(f"[FEHLER] CSV-Ausgabe fehlgeschlagen: {e}", log_path)
        sys.exit(1)

    # 9) Abschluss
    log("=" * 60, log_path)
    if fehler:
        log(f"ABSCHLUSS: {len(fehler)} Fehler", log_path)
        for f in fehler:
            log(f"  {f}", log_path)
        log("=" * 60, log_path)
        sys.exit(1)
    else:
        log("ABSCHLUSS: Mapping erfolgreich — 04-import bereit fuer Archi-Import", log_path)
        log("=" * 60, log_path)
        sys.exit(0)


if __name__ == "__main__":
    main()
