# NBX01-validate_config.py
# NBX-Flow – Konfigurationsvalidierung
# Einzige Wirkung: nbx_config.txt lesen und Pflichtfelder prüfen
# Prüft: ip_range vorhanden und parsebar, scan_ports gültig,
#        output_label gesetzt
# Voraussetzung: NBX00 erfolgreich
# Output: 02-stages\99-logs\NBX01-validate_config.log
# Folge:  NBX02
# Stage:  S1.02

import os
import sys
from datetime import datetime

# HLP00 direkt importieren (Blueprint-Standard)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HLP00_resolve_root import get_root_cfg

# ─── Konstanten ───────────────────────────────────────────────────────────────

SCRIPT_NAME  = "NBX01-validate_config"
LOG_FILENAME = "NBX01-validate_config.log"
NBX00_OUT    = "NBX00-root.resolved.txt"

# ─── Logging ──────────────────────────────────────────────────────────────────

def log(msg, log_path):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ─── Hilfsfunktionen ──────────────────────────────────────────────────────────

def parse_resolved_txt(pfad):
    """Liest NBX00-root.resolved.txt und gibt dict zurück."""
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
    """nbx_config.txt als dict lesen. Kommentare und Leerzeilen ignorieren."""
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


def pruefe_ip_range(wert, log_path):
    """
    Prüft ob ip_range parsebar ist.
    Erlaubt: einzelne IP (192.168.1.1),
             CIDR (192.168.1.0/24),
             Bereich (192.168.1.1-192.168.1.254),
             Komma-getrennte Liste der obigen Formate.
    Gibt (ok, hinweis) zurück.
    """
    import ipaddress
    eintraege = [e.strip() for e in wert.split(",") if e.strip()]
    if not eintraege:
        return False, "ip_range ist leer"

    for eintrag in eintraege:
        # CIDR
        try:
            ipaddress.ip_network(eintrag, strict=False)
            continue
        except ValueError:
            pass
        # Bereich mit Bindestrich
        if "-" in eintrag:
            teile = eintrag.split("-")
            if len(teile) == 2:
                try:
                    ipaddress.ip_address(teile[0].strip())
                    ipaddress.ip_address(teile[1].strip())
                    continue
                except ValueError:
                    pass
        # Einzelne IP
        try:
            ipaddress.ip_address(eintrag)
            continue
        except ValueError:
            pass
        return False, f"Ungültiger Eintrag in ip_range: '{eintrag}'"

    return True, f"{len(eintraege)} Eintrag/Einträge gültig"


def pruefe_ports(wert, log_path):
    """
    Prüft ob scan_ports parsebar ist.
    Erlaubt: Komma-getrennte Portnummern oder Bereiche (22,80,443,8000-8080)
    Gibt (ok, hinweis) zurück.
    """
    if not wert or wert.strip() == "":
        return False, "scan_ports ist leer"
    teile = [t.strip() for t in wert.split(",") if t.strip()]
    for teil in teile:
        if "-" in teil:
            grenzen = teil.split("-")
            if len(grenzen) == 2:
                try:
                    a, b = int(grenzen[0]), int(grenzen[1])
                    if 0 < a <= 65535 and 0 < b <= 65535 and a <= b:
                        continue
                except ValueError:
                    pass
            return False, f"Ungültiger Port-Bereich: '{teil}'"
        else:
            try:
                p = int(teil)
                if 0 < p <= 65535:
                    continue
            except ValueError:
                pass
            return False, f"Ungültige Portnummer: '{teil}'"
    return True, f"{len(teile)} Port-Eintrag/Einträge gültig"

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

    fehler = []

    # 2) NBX00-root.resolved.txt lesen
    nbx00_path = os.path.join(logs_dir, NBX00_OUT)
    if not os.path.isfile(nbx00_path):
        log("[FEHLER] NBX00-root.resolved.txt nicht gefunden.", log_path)
        log("         Bitte zuerst NBX00-validate_environment.py ausfuehren.", log_path)
        sys.exit(1)

    resolved       = parse_resolved_txt(nbx00_path)
    nbx_config_pfad = resolved.get("<nbxconfig>", "")
    log(f"nbx_config.txt: {nbx_config_pfad}", log_path)

    # 3) nbx_config.txt lesen
    if not os.path.isfile(nbx_config_pfad):
        log(f"[FEHLER] nbx_config.txt nicht gefunden: {nbx_config_pfad}", log_path)
        sys.exit(1)

    config = lese_nbx_config(nbx_config_pfad)
    log("nbx_config.txt gelesen:", log_path)
    for key, val in config.items():
        log(f"  {key} = {val}", log_path)

    # 4) Pflichtfeld: ip_range
    ip_range = config.get("ip_range", "").strip()
    log(f"Pruefe ip_range: '{ip_range}'", log_path)
    if not ip_range:
        msg = "[FEHLER] ip_range fehlt in nbx_config.txt"
        log(msg, log_path)
        fehler.append(msg)
    else:
        ok, hinweis = pruefe_ip_range(ip_range, log_path)
        if ok:
            log(f"  OK — {hinweis}", log_path)
        else:
            msg = f"[FEHLER] ip_range ungültig: {hinweis}"
            log(msg, log_path)
            fehler.append(msg)

    # 5) Pflichtfeld: scan_ports
    scan_ports = config.get("scan_ports", "").strip()
    log(f"Pruefe scan_ports: '{scan_ports}'", log_path)
    if not scan_ports:
        msg = "[FEHLER] scan_ports fehlt in nbx_config.txt"
        log(msg, log_path)
        fehler.append(msg)
    else:
        ok, hinweis = pruefe_ports(scan_ports, log_path)
        if ok:
            log(f"  OK — {hinweis}", log_path)
        else:
            msg = f"[FEHLER] scan_ports ungültig: {hinweis}"
            log(msg, log_path)
            fehler.append(msg)

    # 6) Pflichtfeld: output_label
    output_label = config.get("output_label", "").strip()
    log(f"Pruefe output_label: '{output_label}'", log_path)
    if not output_label:
        msg = "[FEHLER] output_label fehlt in nbx_config.txt"
        log(msg, log_path)
        fehler.append(msg)
    else:
        log(f"  OK", log_path)

    # 7) Abschluss
    log("=" * 60, log_path)
    if fehler:
        log(f"ABSCHLUSS: {len(fehler)} Fehler — NBX02 nicht startbereit", log_path)
        for f in fehler:
            log(f"  {f}", log_path)
        log("=" * 60, log_path)
        sys.exit(1)
    else:
        log("ABSCHLUSS: nbx_config.txt gueltig — NBX02 startbereit", log_path)
        log("=" * 60, log_path)
        sys.exit(0)


if __name__ == "__main__":
    main()
