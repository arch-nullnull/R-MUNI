# NBX02-scan_network.py
# NBX-Flow – Netzwerk-Scan
# Einzige Wirkung: IP-Bereich aus nbx_config.txt scannen via python-nmap,
#                  Rohdaten als nbx_raw.json in 02-stages\ schreiben
# Erfasst: erreichbare Hosts, Hostnamen, OS-Hints, offene Ports + Services
# Voraussetzung: NBX01 erfolgreich, nmap installiert, python-nmap installiert
# Output: 02-stages\nbx_raw.json
# Folge:  NBX03
# Stage:  S1.02
#
# Voraussetzungen (in Install.txt eintragen):
#   nmap binary  : https://nmap.org/download.html
#   python-nmap  : pip install python-nmap

import os
import sys
import json
import time
import threading
from datetime import datetime

# HLP00 direkt importieren (Blueprint-Standard)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HLP00_resolve_root import get_root_cfg

# ─── Konstanten ───────────────────────────────────────────────────────────────

SCRIPT_NAME  = "NBX02-scan_network"
LOG_FILENAME = "NBX02-scan_network.log"
NBX00_OUT    = "NBX00-root.resolved.txt"
RAW_FILENAME = "nbx_raw.json"

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


def lese_nbx_config(pfad):
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


def extrahiere_host_daten(host, nm):
    """
    Extrahiert alle relevanten Felder aus einem nmap Host-Ergebnis.
    host       : IP-String (z.B. '192.168.1.1')
    nm         : nmap.PortScanner Objekt nach scan()
    Zugriff via nm[host] — nicht nm['scan'][host].
    Gibt dict zurück — fehlende Werte als leerer String.
    """
    daten = {}
    host_data = nm[host]

    # IP-Adresse
    daten["ip"] = host

    # Hostname
    hostnames = host_data.get("hostnames", [])
    if hostnames and hostnames[0].get("name"):
        daten["hostname"] = hostnames[0]["name"]
    else:
        daten["hostname"] = ""

    # Status
    daten["status"] = host_data.get("status", {}).get("state", "")

    # OS-Hints (beste Schätzung wenn vorhanden)
    os_matches = host_data.get("osmatch", [])
    if os_matches:
        bester_match = os_matches[0]
        daten["os_name"]     = bester_match.get("name", "")
        daten["os_accuracy"] = bester_match.get("accuracy", "")
    else:
        daten["os_name"]     = ""
        daten["os_accuracy"] = ""

    # Offene Ports und Services
    ports = []
    tcp_daten = host_data.get("tcp", {})
    for port_nr, port_info in tcp_daten.items():
        if port_info.get("state") == "open":
            ports.append({
                "port":     port_nr,
                "protocol": "tcp",
                "service":  port_info.get("name", ""),
                "product":  port_info.get("product", ""),
                "version":  port_info.get("version", ""),
            })
    udp_daten = host_data.get("udp", {})
    for port_nr, port_info in udp_daten.items():
        if port_info.get("state") == "open":
            ports.append({
                "port":     port_nr,
                "protocol": "udp",
                "service":  port_info.get("name", ""),
                "product":  port_info.get("product", ""),
                "version":  port_info.get("version", ""),
            })

    daten["open_ports"] = ports

    # MAC-Adresse und Hersteller (wenn vorhanden — meist nur im lokalen Netz)
    addresses = host_data.get("addresses", {})
    daten["mac"]        = addresses.get("mac", "")
    vendor_dict         = host_data.get("vendor", {})
    daten["mac_vendor"] = vendor_dict.get(addresses.get("mac", ""), "")

    return daten

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

    resolved        = parse_resolved_txt(nbx00_path)
    nbx_config_pfad = resolved.get("<nbxconfig>", "")

    # 3) nbx_config.txt lesen
    if not os.path.isfile(nbx_config_pfad):
        log(f"[FEHLER] nbx_config.txt nicht gefunden: {nbx_config_pfad}", log_path)
        sys.exit(1)

    config       = lese_nbx_config(nbx_config_pfad)
    ip_range     = config.get("ip_range", "").strip()
    scan_ports   = config.get("scan_ports", "").strip()
    output_label = config.get("output_label", "nbx").strip()
    scan_args    = config.get("scan_args", "-sV --open").strip()

    log(f"ip_range     : {ip_range}", log_path)
    log(f"scan_ports   : {scan_ports}", log_path)
    log(f"output_label : {output_label}", log_path)
    log(f"scan_args    : {scan_args}", log_path)

    # 4) python-nmap importieren
    try:
        import nmap
    except ImportError:
        log("[FEHLER] python-nmap nicht installiert.", log_path)
        log("         Bitte ausfuehren: pip install python-nmap", log_path)
        log("         Voraussetzung:    nmap binary unter https://nmap.org", log_path)
        sys.exit(1)

    # 5) nmap initialisieren
    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        log("[FEHLER] nmap binary nicht gefunden.", log_path)
        log("         Bitte nmap installieren: https://nmap.org/download.html", log_path)
        log("         Windows: Installer ausfuehren, dann PowerShell neu starten.", log_path)
        sys.exit(1)

    # 6) Phase 1 — Ping-Sweep: alle aktiven Hosts finden
    log("Phase 1: Ping-Sweep (alle aktiven Hosts) ...", log_path)
    nm_ping = nmap.PortScanner()
    try:
        nm_ping.scan(
            hosts=ip_range,
            arguments="-sn -PE -PP -PS80,443 -PA80 --host-timeout 10s"
        )
    except Exception as e:
        log(f"[FEHLER] Ping-Sweep fehlgeschlagen: {e}", log_path)
        sys.exit(1)

    alle_hosts = nm_ping.all_hosts()
    log(f"Phase 1 abgeschlossen: {len(alle_hosts)} Host(s) gefunden", log_path)
    for h in alle_hosts:
        log(f"  gefunden: {h}", log_path)

    if not alle_hosts:
        log("[WARNUNG] Keine Hosts gefunden — ip_range und Netzwerk pruefen.", log_path)

    # 7) Phase 2 — Port-Scan mit Countdown (5 Minuten Kaffeepause)
    log(f"Phase 2: Port-Scan {len(alle_hosts)} Host(s) | Ports: {scan_ports}", log_path)
    log("  Timeout: 5 Minuten — bitte warten (Kaffeepause) ...", log_path)

    scan_fertig = threading.Event()

    def countdown():
        gesamt = 300  # 5 Minuten
        schritte = [300, 240, 180, 120, 60, 30, 10, 5, 4, 3, 2, 1]
        start = time.time()
        for sek in schritte:
            if scan_fertig.is_set():
                break
            verbleibend = gesamt - (time.time() - start)
            if verbleibend <= sek:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{ts}]   ... noch ca. {int(verbleibend)}s")
            ziel = start + (gesamt - sek)
            while time.time() < ziel:
                if scan_fertig.is_set():
                    return
                time.sleep(0.5)

    timer_thread = threading.Thread(target=countdown, daemon=True)
    timer_thread.start()

    hosts_str = " ".join(alle_hosts) if alle_hosts else ip_range
    try:
        nm.scan(
            hosts=hosts_str,
            ports=scan_ports,
            arguments=scan_args + " -T3 --host-timeout 60s"
        )
    except nmap.PortScannerError as e:
        log(f"[FEHLER] Port-Scan fehlgeschlagen: {e}", log_path)
        scan_fertig.set()
        sys.exit(1)
    except Exception as e:
        log(f"[FEHLER] Unerwarteter Fehler beim Port-Scan: {e}", log_path)
        scan_fertig.set()
        sys.exit(1)
    finally:
        scan_fertig.set()

    # Hosts aus Phase 1 zusammenführen — auch Hosts ohne offene Ports übernehmen
    gefundene_hosts = list(set(alle_hosts + nm.all_hosts()))
    log(f"Phase 2 abgeschlossen.", log_path)
    log(f"Hosts gesamt (Phase 1 + 2): {len(gefundene_hosts)}", log_path)

    # 6) Rohdaten aufbereiten
    hosts_daten = []
    for host in gefundene_hosts:
        try:
            if host in nm.all_hosts():
                # Host hat Daten aus Phase 2 (Port-Scan)
                host_dict = extrahiere_host_daten(host, nm)
            else:
                # Host nur in Phase 1 gefunden (kein offener Port) — Basisdaten aus Ping-Sweep
                hostnames = nm_ping[host].get("hostnames", [])
                hostname  = hostnames[0].get("name", "") if hostnames else ""
                addresses = nm_ping[host].get("addresses", {})
                mac       = addresses.get("mac", "")
                vendor    = nm_ping[host].get("vendor", {}).get(mac, "")
                host_dict = {
                    "ip":         host,
                    "hostname":   hostname,
                    "status":     nm_ping[host].get("status", {}).get("state", "up"),
                    "os_name":    "",
                    "os_accuracy": "",
                    "open_ports": [],
                    "mac":        mac,
                    "mac_vendor": vendor,
                }
            hosts_daten.append(host_dict)
            ports_anzahl = len(host_dict.get("open_ports", []))
            log(f"  {host:20s}  hostname: {host_dict['hostname']:30s}  "
                f"status: {host_dict['status']:8s}  offene Ports: {ports_anzahl}", log_path)
        except Exception as e:
            log(f"  [WARNUNG] Fehler bei Host {host}: {e}", log_path)

    # 7) nbx_raw.json schreiben
    raw = {
        "_meta": {
            "scanned_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip_range":     ip_range,
            "scan_ports":   scan_ports,
            "scan_args":    scan_args,
            "output_label": output_label,
            "host_count":   len(hosts_daten),
        },
        "hosts": hosts_daten,
    }

    archive_dir = os.path.join(stages_dir, "00-archimatearchive")
    raw_pfad = os.path.join(archive_dir, RAW_FILENAME)
    try:
        with open(raw_pfad, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=2, default=str)
        log(f"nbx_raw.json geschrieben: {raw_pfad}", log_path)
    except Exception as e:
        log(f"[FEHLER] nbx_raw.json konnte nicht geschrieben werden: {e}", log_path)
        sys.exit(1)

    # 8) Abschluss
    log("=" * 60, log_path)
    log(f"ABSCHLUSS: {len(hosts_daten)} Host(s) erfasst — NBX03 startbereit", log_path)
    log("=" * 60, log_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
