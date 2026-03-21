# ECM01-csv_fields_to_artifacts.py
# EasyCSVMapper – Müll-CSV Felder als Artifact-CSV ausgeben
# Liest alle trash_*.csv aus 00-archimatechild\
# Erkennt Encoding und Trennzeichen automatisch
# Schreibt pro trash_*.csv eine Archi-importfertige elements.csv
# nach 01-artifacts\02-csv\04-import\
# Format Output: ID,Type,Name,Documentation,Specialization
#   - ID          : leer (Archi vergibt beim Import)
#   - Type        : Artifact
#   - Name        : Spaltenname aus Müll-CSV
#   - Documentation: erster Beispielwert aus Müll-CSV (Zeile 1)
#   - Specialization: leer
# Voraussetzung: ECM00 erfolgreich

import os
import sys
import csv
from datetime import datetime

# HLP00 direkt importieren (Blueprint-Standard)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HLP00_resolve_root import get_root_cfg

# ─── Konstanten ───────────────────────────────────────────────────────────────

SCRIPT_NAME  = "ECM01-csv_fields_to_artifacts"
LOG_FILENAME = "ECM01-csv_fields_to_artifacts.log"
ECM00_OUT    = "ECM00-root.resolved.txt"

# Archi elements.csv Header
ARCHI_HEADER = ["ID", "Type", "Name", "Documentation", "Specialization"]

# Encoding Reihenfolge für auto-Erkennung
ENCODINGS = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]

# Trennzeichen Kandidaten
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
    """Liest ECM00-root.resolved.txt und gibt dict zurück."""
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
    """
    Versucht die Datei mit verschiedenen Encodings zu öffnen.
    Gibt (encoding, inhalt_zeilen) zurück oder wirft Exception.
    """
    for enc in ENCODINGS:
        try:
            with open(pfad, "r", encoding=enc) as f:
                zeilen = f.readlines()
            return enc, zeilen
        except (UnicodeDecodeError, LookupError):
            continue
    raise ValueError(f"Kein passendes Encoding gefunden fuer: {os.path.basename(pfad)}")


def erkenne_trennzeichen(zeilen):
    """
    Zählt Vorkommen jedes Trennzeichen-Kandidaten in den ersten 5 Zeilen.
    Gibt das konsistenteste Trennzeichen zurück.
    """
    probe = zeilen[:min(5, len(zeilen))]
    bestes = None
    beste_anzahl = 0

    for trenner in TRENNZEICHEN:
        anzahlen = [zeile.count(trenner) for zeile in probe]
        # Konsistenz: alle Zeilen haben gleiche Anzahl und > 0
        if min(anzahlen) > 0 and min(anzahlen) == max(anzahlen):
            if anzahlen[0] > beste_anzahl:
                beste_anzahl = anzahlen[0]
                bestes = trenner

    # Fallback: höchste Gesamtzahl wenn kein konsistentes gefunden
    if bestes is None:
        for trenner in TRENNZEICHEN:
            anzahl = sum(zeile.count(trenner) for zeile in probe)
            if anzahl > beste_anzahl:
                beste_anzahl = anzahl
                bestes = trenner

    return bestes


def lese_csv(pfad, log_path):
    """
    Liest eine CSV-Datei mit auto-Encoding und auto-Trennzeichen.
    Gibt (encoding, trenner, header, erste_datenzeile) zurück.
    """
    enc, zeilen = erkenne_encoding(pfad)
    log(f"  Encoding erkannt : {enc}", log_path)

    trenner = erkenne_trennzeichen(zeilen)
    log(f"  Trennzeichen     : {repr(trenner)}", log_path)

    # Sauber parsen mit erkanntem Encoding und Trennzeichen
    with open(pfad, "r", encoding=enc, newline="") as f:
        reader = csv.reader(f, delimiter=trenner)
        zeilen_liste = list(reader)

    if not zeilen_liste:
        raise ValueError("CSV ist leer")

    header = [h.strip() for h in zeilen_liste[0]]
    erste_datenzeile = zeilen_liste[1] if len(zeilen_liste) > 1 else []

    return enc, trenner, header, erste_datenzeile


def schreibe_artifact_csv(output_pfad, header, erste_datenzeile, log_path):
    """
    Schreibt eine Archi-importfertige elements.csv.
    Ein Artifact pro Spaltenname aus der Müll-CSV.
    Documentation = erster Beispielwert (Zeile 1) wenn vorhanden.
    """
    with open(output_pfad, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(ARCHI_HEADER)

        for i, feldname in enumerate(header):
            # Beispielwert aus erster Datenzeile wenn vorhanden
            beispiel = ""
            if i < len(erste_datenzeile):
                beispiel = erste_datenzeile[i].strip()

            writer.writerow([
                "",           # ID — leer, Archi vergibt beim Import
                "Artifact",   # Type
                feldname,     # Name = Spaltenname
                beispiel,     # Documentation = Beispielwert
                ""            # Specialization — leer
            ])

    log(f"  Artifact-CSV geschrieben: {os.path.basename(output_pfad)}", log_path)
    log(f"  Felder: {len(header)}", log_path)

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

    # 2) ECM00-root.resolved.txt lesen
    ecm00_path = os.path.join(logs_dir, ECM00_OUT)
    if not os.path.isfile(ecm00_path):
        log("[FEHLER] ECM00-root.resolved.txt nicht gefunden.", log_path)
        log("         Bitte zuerst ECM00-validate_environment.py ausfuehren.", log_path)
        sys.exit(1)

    resolved    = parse_resolved_txt(ecm00_path)
    child_dir   = resolved.get("<childdir>", "")
    artifacts_dir = cfg["<artifacts>"]
    import_dir  = os.path.join(artifacts_dir, "02-csv", "04-import")

    log(f"00-archimatechild : {child_dir}", log_path)
    log(f"04-import         : {import_dir}", log_path)

    # 3) trash_*.csv Dateien finden
    if not os.path.isdir(child_dir):
        log(f"[FEHLER] child_dir nicht gefunden: {child_dir}", log_path)
        sys.exit(1)

    trash_files = sorted([
        f for f in os.listdir(child_dir)
        if f.lower().startswith("trash_") and f.lower().endswith(".csv")
    ])

    if not trash_files:
        log("[FEHLER] Keine trash_*.csv Dateien gefunden.", log_path)
        log("         Bitte Muell-CSV als trash_<n>.csv in 00-archimatechild\\ ablegen.", log_path)
        sys.exit(1)

    if len(trash_files) > 1:
        log(f"[FEHLER] Mehrere trash_*.csv gefunden ({len(trash_files)}) — nur eine pro Lauf erlaubt.", log_path)
        for f in trash_files:
            log(f"  {f}", log_path)
        log("         Bitte alle ausser der gewuenschten Datei entfernen.", log_path)
        sys.exit(1)

    log(f"trash_*.csv gefunden: {trash_files[0]}", log_path)

    # 4) Jede trash_*.csv verarbeiten
    verarbeitet = 0
    for dateiname in trash_files:
        csv_pfad = os.path.join(child_dir, dateiname)
        log(f"Verarbeite: {dateiname}", log_path)

        try:
            enc, trenner, header, erste_datenzeile = lese_csv(csv_pfad, log_path)

            log(f"  Spalten gefunden : {len(header)}", log_path)
            for h in header:
                log(f"    {h}", log_path)

            # Output immer elements.csv — Archi hat das hardcoded
            output_pfad = os.path.join(import_dir, "elements.csv")

            schreibe_artifact_csv(output_pfad, header, erste_datenzeile, log_path)
            verarbeitet += 1

        except Exception as e:
            msg = f"[FEHLER] {dateiname}: {e}"
            log(msg, log_path)
            fehler.append(msg)

    # 5) Abschluss
    log("=" * 60, log_path)
    if fehler:
        log(f"ABSCHLUSS: {len(fehler)} Fehler — bitte Log pruefen", log_path)
        for f in fehler:
            log(f"  {f}", log_path)
        log("=" * 60, log_path)
        sys.exit(1)
    else:
        log(f"ABSCHLUSS: {verarbeitet} Datei(en) verarbeitet — ECM02 startbereit", log_path)
        log(f"  Artifact-CSVs liegen in: {import_dir}", log_path)
        log("=" * 60, log_path)
        sys.exit(0)


if __name__ == "__main__":
    main()
