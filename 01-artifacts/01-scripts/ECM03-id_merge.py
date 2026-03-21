# ECM03-id_merge.py
# EasyCSVMapper – ID-Merge fuer Properties und Relations
#
# Voraussetzung:
#   ECM02 gelaufen → properties.csv + relations.csv in 00-archimatearchive\ (ID-los)
#   Archi Import (elements.csv) → IDs vergeben
#   Archi CSV Export → 04-import\elements.csv (MIT IDs)
#
# Was ECM03 tut:
#   1) Liest 04-import\elements.csv — frischer Archi-Export MIT IDs
#   2) Liest 00-archimatearchive\properties.csv — ID-los, geparkt
#   3) Liest OEF XML — welche Property gehoert zu welchem Ziel-Element-Typ
#   4) Merged IDs via Reihenfolge-Join (Zeile N properties → Zeile N Ziel-Element)
#   5) Schreibt 04-import\properties.csv MIT IDs
#   6) Kopiert 04-import\relations.csv (unveraendert, nur Header)
#
# JOIN-REGEL (KRITISCH):
#   Element-Namen duerfen zwischen ECM02-Import und ECM03 NICHT veraendert
#   worden sein — der Reihenfolge-Join setzt stabile Exportreihenfolge voraus!
#
# Voraussetzung: ECM00 + ECM02 erfolgreich + Archi Export nach 04-import\

import os
import sys
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HLP00_resolve_root import get_root_cfg

# ─── Konstanten ───────────────────────────────────────────────────────────────

SCRIPT_NAME  = "ECM03-id_merge"
LOG_FILENAME = "ECM03-id_merge.log"
ECM00_OUT    = "ECM00-root.resolved.txt"

ARCHI_PROPERTIES_HEADER = ["ID", "Key", "Value"]
ARCHI_RELATIONS_HEADER  = ["ID", "Type", "Name", "Documentation",
                            "Source", "Target", "Specialization"]

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


def lese_csv(pfad):
    """Liest CSV mit utf-8, gibt list of dicts zurück."""
    with open(pfad, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def lese_run_scope_mapping(run_scope_path):
    """Liest MAPPING= Wert aus run-scope.txt."""
    with open(run_scope_path, "r", encoding="utf-8") as f:
        for zeile in f:
            zeile = zeile.strip()
            if zeile.upper().startswith("MAPPING="):
                _, _, val = zeile.partition("=")
                return val.strip()
    return None


def lese_oef_target_typ(xml_pfad, log_path):
    """
    Liest OEF XML und gibt dict zurück:
      { "property_spaltenname": "ziel_element_typ" }
    Also: welcher Property-Spaltenname gehoert zu welchem Ziel-Element-Typ.
    """
    tree = ET.parse(xml_pfad)
    root = tree.getroot()

    def tag(el):
        return el.tag.split("}")[-1]

    # Elemente einlesen
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

    # Associations einlesen
    associations = []
    for rel in root.iter():
        if tag(rel) == "relationship":
            rel_typ = rel.get("{http://www.w3.org/2001/XMLSchema-instance}type", "")
            if rel_typ == "Association":
                source = rel.get("source", "")
                target = rel.get("target", "")
                if source and target:
                    associations.append({"source": source, "target": target})

    # Property-Spaltenname → Ziel-Element-Typ
    property_sources = {a["source"] for a in associations}
    result = {}
    for ident, info in elemente.items():
        if ident in property_sources:
            target_id  = next(
                (a["target"] for a in associations if a["source"] == ident), None
            )
            target_typ = elemente[target_id]["typ"] if target_id in elemente else ""
            result[info["name"]] = target_typ
            log(f"  Property '{info['name']}' → Ziel-Typ '{target_typ}'", log_path)

    return result

# ─── Hauptlogik ───────────────────────────────────────────────────────────────

def main():

    try:
        cfg = get_root_cfg()
    except Exception as e:
        print(f"[FEHLER] root.cfg konnte nicht aufgeloest werden: {e}")
        sys.exit(1)

    stages_dir    = cfg["<stages>"]
    artifacts_dir = cfg["<artifacts>"]
    logs_dir      = os.path.join(stages_dir, "99-logs")
    log_path      = os.path.join(logs_dir, LOG_FILENAME)

    log("=" * 60, log_path)
    log(f"START {SCRIPT_NAME}", log_path)
    log("=" * 60, log_path)

    # 1) Pfade
    ecm00_path    = os.path.join(logs_dir,      ECM00_OUT)
    import_dir    = os.path.join(artifacts_dir, "02-csv", "04-import")
    archive_dir   = os.path.join(stages_dir,    "00-archimatearchive")

    el_pfad       = os.path.join(import_dir,  "elements.csv")
    prop_src_pfad = os.path.join(archive_dir, "properties.csv")
    rel_src_pfad  = os.path.join(archive_dir, "relations.csv")
    prop_dst_pfad = os.path.join(import_dir,  "properties.csv")
    rel_dst_pfad  = os.path.join(import_dir,  "relations.csv")

    # 2) ECM00 prüfen
    if not os.path.isfile(ecm00_path):
        log("[FEHLER] ECM00-root.resolved.txt nicht gefunden.", log_path)
        sys.exit(1)

    resolved          = parse_resolved_txt(ecm00_path)
    mapping_model_dir = resolved.get("<mappingmodel>", "")

    # 3) Alle benötigten Dateien prüfen
    for pfad, bezeichnung in [
        (el_pfad,       "elements.csv (04-import — Archi Export)"),
        (prop_src_pfad, "properties.csv (00-archimatearchive)"),
        (rel_src_pfad,  "relations.csv  (00-archimatearchive)"),
    ]:
        if not os.path.isfile(pfad):
            log(f"[FEHLER] Nicht gefunden: {bezeichnung}", log_path)
            log(f"         Erwartet unter: {pfad}", log_path)
            sys.exit(1)

    log(f"elements.csv  : {el_pfad}", log_path)
    log(f"properties.csv: {prop_src_pfad}", log_path)
    log(f"relations.csv : {rel_src_pfad}", log_path)

    # 4) run-scope.txt → MAPPING= lesen
    run_scope_path = os.path.join(stages_dir, "run-scope.txt")
    mapping_name   = lese_run_scope_mapping(run_scope_path)
    if not mapping_name:
        log("[FEHLER] Kein MAPPING= in run-scope.txt gefunden.", log_path)
        sys.exit(1)

    xml_pfad = os.path.join(mapping_model_dir, mapping_name)
    if not os.path.isfile(xml_pfad):
        log(f"[FEHLER] OEF XML nicht gefunden: {xml_pfad}", log_path)
        sys.exit(1)

    log(f"OEF XML       : {xml_pfad}", log_path)

    # 5) OEF lesen — welcher Property-Key gehoert zu welchem Ziel-Typ
    log("Lese OEF Mapping ...", log_path)
    property_ziel_typ = lese_oef_target_typ(xml_pfad, log_path)

    # 6) elements.csv lesen (MIT IDs)
    log("Lese elements.csv (mit IDs) ...", log_path)
    elements = lese_csv(el_pfad)
    log(f"  Elemente: {len(elements)}", log_path)

    # IDs ohne Wert prüfen
    ohne_id = [e for e in elements if not e.get("ID", "").strip()]
    if ohne_id:
        log(f"  [WARNUNG] {len(ohne_id)} Elemente ohne ID — bitte Archi Export pruefen", log_path)

    # Index aufbauen: Typ → liste von IDs (in Reihenfolge)
    typ_ids = {}
    for el in elements:
        typ = el.get("Type", "").strip()
        eid = el.get("ID", "").strip()
        if typ not in typ_ids:
            typ_ids[typ] = []
        typ_ids[typ].append(eid)

    log("  Element-IDs pro Typ:", log_path)
    for typ, ids in typ_ids.items():
        log(f"    {typ}: {len(ids)} IDs", log_path)

    # 7) properties.csv lesen (ID-los)
    log("Lese properties.csv (geparkt) ...", log_path)
    props = lese_csv(prop_src_pfad)
    log(f"  Properties: {len(props)}", log_path)

    # 8) ID-Merge — Reihenfolge-Join pro Ziel-Typ
    log("Fuehre ID-Merge durch ...", log_path)

    # Zaehler pro Ziel-Typ (fuer Reihenfolge-Join)
    typ_zaehler = {typ: 0 for typ in typ_ids}

    gemergete_props = []
    nicht_zugewiesen = 0

    for prop in props:
        key = prop.get("Key", "").strip()
        val = prop.get("Value", "").strip()

        # Welcher Ziel-Typ fuer diesen Key?
        ziel_typ = property_ziel_typ.get(key, "")

        if not ziel_typ or ziel_typ not in typ_ids:
            log(f"  [WARNUNG] Key '{key}' — kein Ziel-Typ gefunden, ID bleibt leer", log_path)
            gemergete_props.append({"ID": "", "Key": key, "Value": val})
            nicht_zugewiesen += 1
            continue

        # Naechste ID dieses Typs holen
        idx = typ_zaehler.get(ziel_typ, 0)
        ids_fuer_typ = typ_ids[ziel_typ]

        if idx < len(ids_fuer_typ):
            owner_id = ids_fuer_typ[idx]
        else:
            # Reihenfolge wiederholt sich (mehrere Properties pro Element)
            owner_id = ids_fuer_typ[idx % len(ids_fuer_typ)]

        gemergete_props.append({"ID": owner_id, "Key": key, "Value": val})

        # Zaehler nur erhoehen wenn alle Property-Keys dieses Elements durch sind
        # Strategie: nach jedem vollstaendigen Key-Satz weiterruecken
        # Wir zaehlen Keys pro Typ-Gruppe
        typ_zaehler[ziel_typ] = idx + 1

    log(f"  Gemergete Properties: {len(gemergete_props)}", log_path)
    if nicht_zugewiesen:
        log(f"  [WARNUNG] {nicht_zugewiesen} Properties ohne ID-Zuweisung", log_path)

    # 9) properties.csv schreiben nach 04-import\
    log(f"Schreibe properties.csv nach 04-import ...", log_path)
    with open(prop_dst_pfad, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(ARCHI_PROPERTIES_HEADER)
        for p in gemergete_props:
            writer.writerow([p["ID"], p["Key"], p["Value"]])
    log(f"  {len(gemergete_props)} Zeilen geschrieben", log_path)

    # 10) relations.csv aus archive nach 04-import\ kopieren
    log(f"Kopiere relations.csv nach 04-import ...", log_path)
    rels = lese_csv(rel_src_pfad)
    with open(rel_dst_pfad, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(ARCHI_RELATIONS_HEADER)
        for r in rels:
            writer.writerow([
                r.get("ID", ""),            r.get("Type", ""),
                r.get("Name", ""),          r.get("Documentation", ""),
                r.get("Source", ""),        r.get("Target", ""),
                r.get("Specialization", "")
            ])
    log(f"  relations.csv: {len(rels)} Zeilen kopiert", log_path)

    # 11) Abschluss
    log("=" * 60, log_path)
    log("ABSCHLUSS: ID-Merge erfolgreich", log_path)
    log(f"  04-import\\properties.csv bereit fuer Archi-Import", log_path)
    log(f"  04-import\\relations.csv  bereit fuer Archi-Import", log_path)
    log("  WICHTIG: Element-Namen duerfen zwischen ECM02 und ECM03", log_path)
    log("           NICHT veraendert worden sein!", log_path)
    log("=" * 60, log_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
