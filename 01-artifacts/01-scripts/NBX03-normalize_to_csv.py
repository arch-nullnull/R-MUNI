# NBX03-normalize_to_csv.py
# NBX-Flow – Normierung und CSV-Export
# Einzige Wirkung: nbx_raw.json lesen, normieren, trash_nbx.csv schreiben
# Hosts  → nbx_objecttype: host
# Services (offene Ports) → nbx_objecttype: service
# 3PartyID: nbx_<ip>_<protocol>_<port> für Services, nbx_<ip> für Hosts
# Voraussetzung: NBX02 erfolgreich
# Output: 01-artifacts\02-csv\03-child\00-archimatechild\trash_nbx.csv
# Folge:  NBX04
# Stage:  S1.02

import os
import sys
import json
import csv
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HLP00_resolve_root import get_root_cfg

# ─── Konstanten ───────────────────────────────────────────────────────────────

SCRIPT_NAME   = "NBX03-normalize_to_csv"
LOG_FILENAME  = "NBX03-normalize_to_csv.log"
NBX00_OUT     = "NBX00-root.resolved.txt"
RAW_FILENAME  = "nbx_raw.json"
TRASH_FILENAME = "trash_nbx.csv"

# trash_nbx.csv Header — ECM-kompatibel (GOV 6.6)
CSV_HEADER = [
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
]

# Lokale Domain-Suffixe die abgeschnitten werden
LOKALE_SUFFIXE = [".fritz.box", ".local", ".lan", ".home", ".internal", ".localdomain"]

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


def safe(wert):
    """None und fehlende Werte als leerer String."""
    if wert is None:
        return ""
    return str(wert).strip()


def bereinige_name(hostname, manufacturer=""):
    """
    Lokale Domain-Suffixe abschneiden.
    AVM/FRITZ!Box Sonderfall: wpad.fritz.box → FRITZ!Box
    """
    if not hostname:
        return ""
    name = hostname.strip()
    if name.lower().startswith("wpad") or "avm" in manufacturer.lower():
        if any(name.lower().endswith(s) for s in LOKALE_SUFFIXE):
            return "FRITZ!Box"
    for suffix in LOKALE_SUFFIXE:
        if name.lower().endswith(suffix):
            name = name[: -len(suffix)]
            break
    return name


def normiere_host(host, output_label):
    ip           = safe(host.get("ip"))
    manufacturer = safe(host.get("mac_vendor"))
    name         = bereinige_name(safe(host.get("hostname")), manufacturer) or ip
    mac          = safe(host.get("mac"))

    desc_teile = []
    if manufacturer:
        desc_teile.append(manufacturer)
    if mac:
        desc_teile.append(f"MAC:{mac}")
    description = " | ".join(desc_teile)

    return {
        "3PartyID":       "nbx_" + ip.replace(".", "_"),
        "nbx_objecttype": "host",
        "Name":           name,
        "Role":           "",
        "Platform":       "",
        "Site":           "",
        "Status":         safe(host.get("status")),
        "Manufacturer":   manufacturer,
        "Model":          "",
        "Description":    description,
        "nbx_source":     output_label,
        "nbx_raw_id":     ip,
    }


def normiere_service(host, port_info, output_label):
    ip       = safe(host.get("ip"))
    name     = bereinige_name(safe(host.get("hostname")), safe(host.get("mac_vendor"))) or ip

    port     = safe(port_info.get("port"))
    protocol = safe(port_info.get("protocol"))
    service  = safe(port_info.get("service"))
    product  = safe(port_info.get("product"))
    version  = safe(port_info.get("version"))

    service_name = service or f"{port}/{protocol}"

    desc_teile = []
    if product:
        desc_teile.append(product)
    if version:
        desc_teile.append(version)
    desc_teile.append(f"Port {port}/{protocol}")
    description = " | ".join(desc_teile)

    return {
        "3PartyID":       f"nbx_{ip.replace('.', '_')}_{protocol}_{port}",
        "nbx_objecttype": "service",
        "Name":           service_name,
        "Role":           "",
        "Platform":       "",
        "Site":           name,
        "Status":         "active",
        "Manufacturer":   "",
        "Model":          "",
        "Description":    description,
        "nbx_source":     output_label,
        "nbx_raw_id":     f"{ip}:{port}",
    }

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

    nbx00_path = os.path.join(logs_dir, NBX00_OUT)
    if not os.path.isfile(nbx00_path):
        log("[FEHLER] NBX00-root.resolved.txt nicht gefunden.", log_path)
        log("         Bitte zuerst NBX00-validate_environment.py ausfuehren.", log_path)
        sys.exit(1)

    resolved  = parse_resolved_txt(nbx00_path)
    child_dir = resolved.get("<childdir>", "")

    raw_pfad = os.path.join(stages_dir, "00-archimatearchive", RAW_FILENAME)
    if not os.path.isfile(raw_pfad):
        log(f"[FEHLER] nbx_raw.json nicht gefunden: {raw_pfad}", log_path)
        log("         Bitte zuerst NBX02-scan_network.py ausfuehren.", log_path)
        sys.exit(1)

    with open(raw_pfad, "r", encoding="utf-8") as f:
        raw = json.load(f)

    meta         = raw.get("_meta", {})
    hosts        = raw.get("hosts", [])
    output_label = meta.get("output_label", "scan")

    log(f"nbx_raw.json gelesen : {len(hosts)} Host(s)", log_path)
    log(f"Gescannt am          : {meta.get('scanned_at', '?')}", log_path)
    log(f"IP-Bereich           : {meta.get('ip_range', '?')}", log_path)

    zeilen         = []
    count_hosts    = 0
    count_services = 0

    for host in hosts:
        zeilen.append(normiere_host(host, output_label))
        count_hosts += 1
        for port_info in host.get("open_ports", []):
            zeilen.append(normiere_service(host, port_info, output_label))
            count_services += 1

    log(f"Hosts normiert       : {count_hosts}", log_path)
    log(f"Services normiert    : {count_services}", log_path)
    log(f"Zeilen gesamt        : {len(zeilen)}", log_path)

    if not os.path.isdir(child_dir):
        log(f"[FEHLER] Zielordner nicht gefunden: {child_dir}", log_path)
        sys.exit(1)

    trash_pfad = os.path.join(child_dir, TRASH_FILENAME)
    with open(trash_pfad, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(zeilen)

    log(f"trash_nbx.csv        : {trash_pfad}", log_path)
    log(f"                       {len(zeilen)} Zeilen geschrieben", log_path)
    log("=" * 60, log_path)
    log(f"ABSCHLUSS: trash_nbx.csv bereit — NBX04 startbereit", log_path)
    log(f"  Naechster Schritt: ECM00 -> ECM01 (Phase 1) oder ECM02 (Phase 2)", log_path)
    log("=" * 60, log_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
