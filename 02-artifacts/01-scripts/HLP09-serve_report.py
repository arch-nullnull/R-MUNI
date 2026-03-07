#!/usr/bin/env python3
# HLP09-serve_report.py
#
# Zweck:
#   Startet lokale Webserver fuer alle in webconfig.txt konfigurierten Reports.
#   Jeder Report laeuft auf seinem eigenen Port — alle gleichzeitig.
#   Liest BLUEPRINT_ROOT aus root.txt.
#   Liest Report-Konfiguration aus:
#     02-artifacts/05-reports/webconfig.txt
#
# webconfig.txt Format:
#   # Kommentar
#   NAME=MUNI EA Modell
#   PATH=00-archimate/MUNI EA Modell
#   PORT=8080
#
#   NAME=Business Prozesse
#   PATH=01-bpmn/Business Prozesse
#   PORT=8081
#
# Verwendung:
#   python HLP09-serve_report.py
#   python HLP09-serve_report.py --no-browser   (kein automatischer Browser)
#
# Beenden:
#   STRG+C im Terminal
#
# Ablage:  02-artifacts/01-scripts/HLP09-serve_report.py
# Log:     03-stages/99-logs/HLP09-serve_report.log

import os
import sys
import socket
import threading
import webbrowser
import http.server
import datetime
from functools import partial


# ===========================================================
# KONFIGURATION
# ===========================================================

SCRIPT_NAME    = "HLP09"
REPORTS_REL    = os.path.join("02-artifacts", "05-reports")
WEBCONFIG_REL  = os.path.join("02-artifacts", "05-reports", "webconfig.txt")
LOG_REL        = os.path.join("03-stages", "99-logs", "HLP09-serve_report.log")


# ===========================================================
# HILFSFUNKTIONEN
# ===========================================================

def now_ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str, log_path: str | None = None):
    line = f"[{SCRIPT_NAME}] {now_ts()} | {message}"
    print(line)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass


def warn(message: str, log_path: str | None = None):
    line = f"[{SCRIPT_NAME}] {now_ts()} | WARNUNG | {message}"
    print(line)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass


def die(message: str, log_path: str | None = None):
    line = f"[{SCRIPT_NAME}] {now_ts()} | FEHLER | {message}"
    print(line, file=sys.stderr)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    sys.exit(1)


def get_local_ip() -> str:
    """Ermittelt die lokale Netzwerk-IP-Adresse des Rechners."""
    try:
        # Verbindung simulieren um lokale IP zu ermitteln — kein Paket wird gesendet
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_hostname() -> str:
    """Gibt den Windows-Hostnamen des Rechners zurueck."""
    try:
        return socket.gethostname()
    except Exception:
        return "localhost"


# ===========================================================
# ROOT.TXT AUFLOESUNG
# ===========================================================

def find_root_txt(script_dir: str) -> str:
    """
    Sucht root.txt relativ zum Script-Verzeichnis.
    Script liegt in: 02-artifacts/01-scripts/
    root.txt liegt in: <BLUEPRINT_ROOT>/root.txt
    Zwei Ebenen hoch: ../../root.txt
    """
    return os.path.abspath(os.path.join(script_dir, "..", "..", "root.txt"))


def read_blueprint_root(root_txt_path: str, log_path: str | None) -> str:
    """Liest BLUEPRINT_ROOT aus root.txt und loest den Pfad auf."""
    if not os.path.isfile(root_txt_path):
        die(f"root.txt nicht gefunden: {root_txt_path}", log_path)

    root_value = None
    with open(root_txt_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#") or not stripped:
                continue
            if stripped.startswith("BLUEPRINT_ROOT="):
                if root_value is not None:
                    die("Mehrere BLUEPRINT_ROOT Eintraege in root.txt gefunden", log_path)
                root_value = stripped.split("=", 1)[1].strip()

    if root_value is None:
        die("Kein BLUEPRINT_ROOT Eintrag in root.txt gefunden", log_path)
    if root_value == "":
        die("BLUEPRINT_ROOT ist leer in root.txt", log_path)

    # Relativen Pfad gegen Position von root.txt aufloesen
    if not os.path.isabs(root_value):
        root_value = os.path.abspath(
            os.path.join(os.path.dirname(root_txt_path), root_value)
        )

    if not os.path.isdir(root_value):
        die(f"BLUEPRINT_ROOT Verzeichnis existiert nicht: {root_value}", log_path)

    return root_value


# ===========================================================
# WEBCONFIG.TXT LESEN
# ===========================================================

def read_webconfig(webconfig_path: str, reports_base: str, log_path: str | None) -> list[dict]:
    """
    Liest webconfig.txt und gibt eine Liste von Report-Eintraegen zurueck.

    Jeder Eintrag besteht aus drei Zeilen (Reihenfolge egal, Leerzeile trennt):
      NAME=Anzeigename
      PATH=relativer/pfad/zum/report/ordner
      PORT=8080

    Rueckgabe: Liste von dicts:
      name      - Anzeigename
      path      - Relativer Pfad (wie in webconfig.txt)
      port      - Port-Nummer (int)
      abs_path  - Absoluter Pfad zum Report-Ordner
      status    - "ok" | "leer" | "kein_ordner"
    """
    if not os.path.isfile(webconfig_path):
        die(
            f"webconfig.txt nicht gefunden: {webconfig_path}\n"
            f"  Bitte Datei anlegen in: {os.path.dirname(webconfig_path)}\n"
            f"  Format:\n"
            f"    NAME=Mein Report\n"
            f"    PATH=00-archimate/Mein Report\n"
            f"    PORT=8080",
            log_path
        )

    entries    = []
    current    = {}
    seen_ports = {}
    last_line  = ""

    def finalize_entry(entry: dict):
        """Validiert und schliesst einen Eintrag ab."""
        if not entry:
            return

        # Pflichtfelder pruefen
        for field in ("name", "path", "port"):
            if field not in entry:
                die(
                    f"Unvollstaendiger Eintrag in webconfig.txt — "
                    f"Feld '{field.upper()}' fehlt (nahe: '{last_line}')",
                    log_path
                )

        # Port-Duplikat pruefen
        port = entry["port"]
        if port in seen_ports:
            die(
                f"Port {port} wird mehrfach verwendet in webconfig.txt.\n"
                f"  Erster Eintrag : '{seen_ports[port]}'\n"
                f"  Zweiter Eintrag: '{entry['name']}'",
                log_path
            )
        seen_ports[port] = entry["name"]

        # Absoluten Pfad aufbauen und Status pruefen
        abs_path   = os.path.join(reports_base, entry["path"])
        index_html = os.path.join(abs_path, "index.html")

        if not os.path.isdir(abs_path):
            entry["status"] = "kein_ordner"
        elif not os.path.isfile(index_html):
            entry["status"] = "leer"
        else:
            entry["status"] = "ok"

        entry["abs_path"] = abs_path
        entries.append(entry.copy())

    with open(webconfig_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()

            # Leerzeile oder Kommentar — Eintrag abschliessen
            if not line or line.startswith("#"):
                if current:
                    finalize_entry(current)
                    current = {}
                continue

            if "=" not in line:
                warn(f"Ungueltige Zeile in webconfig.txt ignoriert: '{line}'", log_path)
                continue

            key, _, value = line.partition("=")
            key   = key.strip().upper()
            value = value.strip()
            last_line = line

            if key == "NAME":
                current["name"] = value
            elif key == "PATH":
                # Backslash normalisieren fuer Windows-Pfade
                current["path"] = value.replace("\\", os.sep).replace("/", os.sep)
            elif key == "PORT":
                try:
                    current["port"] = int(value)
                except ValueError:
                    die(f"Ungueltige PORT-Angabe in webconfig.txt: '{value}'", log_path)
            else:
                warn(f"Unbekannter Schluessel in webconfig.txt ignoriert: '{key}'", log_path)

    # Letzten Eintrag abschliessen (Datei endet ohne Leerzeile)
    if current:
        finalize_entry(current)

    if not entries:
        die(
            "Keine gueltigen Eintraege in webconfig.txt gefunden.\n"
            "  Mindestens ein NAME/PATH/PORT Block wird benoetigt.",
            log_path
        )

    return entries


# ===========================================================
# WEBSERVER
# ===========================================================

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Handler — zeigt nur Fehler, keine normalen Requests."""

    def log_message(self, format, *args):
        # Nur HTTP-Fehler (4xx, 5xx) ausgeben
        if args and len(args) >= 2:
            status = str(args[1])
            if status.startswith("4") or status.startswith("5"):
                print(f"  [HTTP-FEHLER] {self.path} -> {status}")


def start_server_thread(name: str, abs_path: str, port: int, log_path: str | None):
    """Startet einen HTTP Server in einem eigenen Daemon-Thread."""
    handler = partial(QuietHandler, directory=abs_path)
    try:
        server = http.server.HTTPServer(("", port), handler)
    except OSError as e:
        die(
            f"Port {port} fuer '{name}' nicht verfuegbar.\n"
            f"  Moegliche Ursache: Port bereits belegt.\n"
            f"  Fehler: {e}",
            log_path
        )

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


# ===========================================================
# ARGUMENT-PARSING
# ===========================================================

def parse_args() -> bool:
    """Parst Kommandozeilenargumente. Gibt open_browser zurueck."""
    open_browser = True
    for arg in sys.argv[1:]:
        if arg == "--no-browser":
            open_browser = False
        else:
            print(f"Unbekanntes Argument: {arg}", file=sys.stderr)
            print("Verwendung: python HLP09-serve_report.py [--no-browser]")
            sys.exit(1)
    return open_browser


# ===========================================================
# HAUPTPROGRAMM
# ===========================================================

def main():
    open_browser = parse_args()

    # Script-Verzeichnis bestimmen
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # root.txt finden und Blueprint-Root aufloesen
    root_txt       = find_root_txt(script_dir)
    blueprint_root = read_blueprint_root(root_txt, None)

    # Log-Pfad setzen
    log_path = os.path.join(blueprint_root, LOG_REL)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    log(f"Blueprint Root : {blueprint_root}", log_path)

    # webconfig.txt lesen
    webconfig_path = os.path.join(blueprint_root, WEBCONFIG_REL)
    reports_base   = os.path.join(blueprint_root, REPORTS_REL)

    log(f"Lese webconfig : {webconfig_path}", log_path)
    entries = read_webconfig(webconfig_path, reports_base, log_path)

    # Netzwerk-Infos ermitteln
    local_ip = get_local_ip()
    hostname = get_hostname()

    # Spaltenbreite fuer saubere Tabellenausgabe
    max_name = max(len(e["name"]) for e in entries)
    col      = max(max_name, 22)

    # Server starten
    servers      = []
    started      = []
    skipped      = []
    browser_urls = []

    for entry in entries:
        name     = entry["name"]
        port     = entry["port"]
        status   = entry["status"]
        abs_path = entry["abs_path"]

        if status != "ok":
            grund = (
                "Ordner nicht gefunden"
                if status == "kein_ordner"
                else "kein index.html — bitte HTML Report exportieren"
            )
            warn(f"Uebersprungen: '{name}' (Port {port}) — {grund}", log_path)
            skipped.append((name, port, grund))
            continue

        server = start_server_thread(name, abs_path, port, log_path)
        servers.append(server)
        browser_urls.append(f"http://localhost:{port}")
        started.append((name, port))
        log(f"Gestartet: '{name}' | Port={port} | Pfad={abs_path}", log_path)

    # Mindestens ein Server muss laufen
    if not servers:
        die(
            "Kein einziger Report konnte gestartet werden.\n"
            "  Bitte webconfig.txt pruefen und HTML Reports exportieren.",
            log_path
        )

    # -----------------------------------------------------------
    # Terminal-Ausgabe — uebersichtliche Tabelle
    # -----------------------------------------------------------
    breite = col + 52
    sep    = "=" * breite
    dash   = "-" * breite

    print()
    print(sep)
    print(f"  R+MUNI Report Server  |  {now_ts()}")
    print(sep)
    print(f"  {'Report':<{col}}  {'Lokal':<24}  {'IP':<22}  Hostname")
    print(dash)

    for name, port in started:
        url_lokal = f"http://localhost:{port}"
        url_ip    = f"http://{local_ip}:{port}"
        url_host  = f"http://{hostname}:{port}"
        print(f"  {name:<{col}}  {url_lokal:<24}  {url_ip:<22}  {url_host}")

    if skipped:
        print(dash)
        print(f"  Uebersprungen ({len(skipped)} Eintrag/Eintraege):")
        for name, port, grund in skipped:
            print(f"    Port {port:<6}  {name:<{col}}  ->  {grund}")

    print(dash)
    print(f"  Beenden:  STRG+C")
    print(sep)
    print()

    log(f"Aktive Server: {len(servers)} | Uebersprungen: {len(skipped)}", log_path)

    # Browser fuer alle gestarteten Reports oeffnen
    if open_browser and browser_urls:
        def open_all_browsers():
            import time
            time.sleep(0.8)
            for url in browser_urls:
                webbrowser.open(url)
                time.sleep(0.4)  # Kurze Pause damit Tabs ordentlich oeffnen
        threading.Thread(target=open_all_browsers, daemon=True).start()

    # Hauptthread blockieren bis STRG+C
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print()
        print("  [OK] Alle Server gestoppt.")
        log("Alle Server gestoppt (STRG+C)", log_path)
        for server in servers:
            try:
                server.shutdown()
                server.server_close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
