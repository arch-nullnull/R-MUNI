# NBX04-ip_merge.py
# NBX-Flow – IP-Merge
# Einzige Wirkung: trash_nbx.csv lesen, service-Zeilen auf zugehörige
#                  host-Zeile aggregieren, Ergebnis als trash_nbx.csv
#                  zurückschreiben (eine Zeile pro Host, open_ports Spalte)
# Voraussetzung: NBX03 erfolgreich
# Output: 01-artifacts\02-csv\03-child\00-archimatechild\trash_nbx.csv (gemergt)
#         02-stages\99-logs\NBX04-ip_merge.log
# Folge:  NBX05
# Stage:  S1.05

import os
import sys
import csv
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HLP00_resolve_root import get_root_cfg

# ─── Konstanten ───────────────────────────────────────────────────────────────

SCRIPT_NAME    = "NBX04-ip_merge"
LOG_FILENAME   = "NBX04-ip_merge.log"
NBX00_OUT      = "NBX00-root.resolved.txt"
TRASH_FILENAME = "trash_nbx.csv"

# Header nach Merge — open_ports als neue letzte Spalte
CSV_HEADER_MERGED = [
    "3PartyID",
    "nbx_objecttype",
    "Name",
    "Role",
    "Platform",
    "Site",
    "Status",
    "Manufacturer",
    "Model",
    "Description",
    "nbx_source",
    "nbx_raw_id",
    "open_ports",
]

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


def port_str_aus_description(zeile):
    """
    Port-String direkt aus Description lesen.
    NBX03 schreibt Description als: 'Product | Version | Port 22/tcp'
    Letztes Segment nach ' | ' enthält 'Port 22/tcp'.
    Fallback: Name-Spalte (enthält Service-Namen wie 'ssh', 'http').
    """
    description  = zeile.get("Description", "").strip()
    service_name = zeile.get("Name", "").strip()

    # Description parsen — letztes Segment suchen das mit 'Port ' beginnt
    if description:
        teile = [t.strip() for t in description.split("|")]
        for teil in reversed(teile):
            if teil.lower().startswith("port "):
                port_info = teil[5:].strip()   # 'Port ' abschneiden → '22/tcp'
                if service_name and service_name not in port_info:
                    return f"{port_info}:{service_name}"
                return port_info

    # Fallback: nur Service-Name
    return service_name


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

    # 3) trash_nbx.csv lesen
    trash_pfad = os.path.join(child_dir, TRASH_FILENAME)
    if not os.path.isfile(trash_pfad):
        log(f"[FEHLER] trash_nbx.csv nicht gefunden: {trash_pfad}", log_path)
        log("         Bitte zuerst NBX03-normalize_to_csv.py ausfuehren.", log_path)
        sys.exit(1)

    zeilen_roh = []
    with open(trash_pfad, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for zeile in reader:
            zeilen_roh.append(zeile)

    log(f"trash_nbx.csv gelesen : {len(zeilen_roh)} Zeile(n) (roh)", log_path)

    # 4) Durchlauf 1 — alle Hosts einsammeln
    hosts      = {}   # ip → host-dict
    host_order = []   # Reihenfolge erhalten
    services   = {}   # ip → [port_str, ...]

    count_hosts    = 0
    count_services = 0
    count_skip     = 0

    for zeile in zeilen_roh:
        typ = zeile.get("nbx_objecttype", "").strip()
        if typ == "host":
            ip = zeile.get("nbx_raw_id", "").strip()
            if ip and ip not in hosts:
                hosts[ip] = dict(zeile)
                host_order.append(ip)
                services[ip] = []
            count_hosts += 1

    log(f"Durchlauf 1 — Hosts   : {count_hosts}", log_path)

    # 5) Durchlauf 2 — alle Services zuordnen (Reihenfolge in CSV irrelevant)
    for zeile in zeilen_roh:
        typ = zeile.get("nbx_objecttype", "").strip()
        if typ == "service":
            # nbx_raw_id bei service = 'IP:Port' (NBX03 Konvention)
            raw_id = zeile.get("nbx_raw_id", "").strip()
            ip     = raw_id.split(":")[0] if ":" in raw_id else raw_id
            pstr   = port_str_aus_description(zeile)

            if ip in hosts:
                services[ip].append(pstr)
            else:
                log(f"  [WARNUNG] Service ohne Host: {raw_id} — uebersprungen", log_path)
                count_skip += 1
            count_services += 1

    log(f"Durchlauf 2 — Services: {count_services}", log_path)
    if count_skip:
        log(f"Uebersprungen          : {count_skip}", log_path)

    # 6) Ergebnis zusammenbauen — eine Zeile pro Host
    zeilen_merged = []
    for ip in host_order:
        eintrag = hosts[ip]
        eintrag["open_ports"] = " | ".join(services[ip]) if services[ip] else ""
        zeilen_merged.append(eintrag)

    log(f"Merged                 : {len(zeilen_merged)} Zeile(n) (eine pro Host)", log_path)

    # 7) trash_nbx.csv zurückschreiben
    try:
        with open(trash_pfad, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=CSV_HEADER_MERGED,
                extrasaction="ignore"
            )
            writer.writeheader()
            writer.writerows(zeilen_merged)
        log(f"trash_nbx.csv geschrieben: {trash_pfad}", log_path)
        log(f"                           {len(zeilen_merged)} Zeilen, "
            f"{count_services} Services aggregiert", log_path)
    except Exception as e:
        log(f"[FEHLER] trash_nbx.csv konnte nicht geschrieben werden: {e}", log_path)
        sys.exit(1)

    # 8) Abschluss
    log("=" * 60, log_path)
    log("ABSCHLUSS: IP-Merge abgeschlossen — NBX05 startbereit", log_path)
    log("=" * 60, log_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
