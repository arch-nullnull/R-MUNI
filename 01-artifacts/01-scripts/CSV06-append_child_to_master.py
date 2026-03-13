#!/usr/bin/env python3
# CSV06-append_child_to_master.py
#
# Purpose:
# - Append Archi CSV exports (child) into master CSV files
# - Append-only, never overwrite
# - Safe newline handling
# - Missing child CSVs are logged but do not abort
#
# Source:
# - <root>/01-artifacts/02-csv/03-child/00-archimatechild
#
# Target:
# - <root>/01-artifacts/02-csv/00-master
#
# Logs:
# - <root>/02-stages/99-logs/CSV06-append.log
#
# BUGFIX (Stage 4 / 2026-03-11):
# Dateinamen werden aus run-scope.txt SOURCE=CSV Eintraegen gelesen.
# Fallback auf hardcoded Namen wenn kein aktiver SOURCE=CSV Eintrag
# vorhanden ist. Ermoeglicht Archi File Prefix im CSV Export.

import os
import sys
from datetime import datetime


# ----------------------------------------------------------
# Konstanten
# ----------------------------------------------------------

FALLBACK_FILES = ["elements.csv", "relations.csv", "properties.csv"]
SOURCE_TYPE    = "CSV"


# ----------------------------------------------------------
# Hilfsfunktionen
# ----------------------------------------------------------

def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg, log_path):
    line = f"[CSV06] {now_ts()} | {msg}"
    print(line)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def ensure_trailing_newline(path):
    with open(path, "rb+") as f:
        f.seek(0, os.SEEK_END)
        if f.tell() == 0:
            return
        f.seek(-1, os.SEEK_END)
        if f.read(1) != b"\n":
            f.write(b"\n")


# ----------------------------------------------------------
# run-scope.txt lesen
# ----------------------------------------------------------

def read_csv_scope(run_scope_path, log_path):
    """
    Liest alle aktiven SOURCE=CSV / MODEL= Pairs aus run-scope.txt.

    Format (aktives Pair):
      SOURCE=CSV
      MODEL=MUNI FLOW elements.csv

    Kommentierte Zeilen (#) werden ignoriert.
    Rueckgabe: Liste der MODEL= Werte fuer SOURCE=CSV.
    Leere Liste wenn kein aktiver Eintrag vorhanden oder Datei fehlt.
    """
    if not os.path.isfile(run_scope_path):
        log(f"run-scope.txt nicht gefunden: {run_scope_path} — Fallback aktiv", log_path)
        return []

    aktive_zeilen = []
    with open(run_scope_path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.upper().startswith("SNAPSHOT_"):
                continue
            aktive_zeilen.append(s)

    modelle = []
    i = 0
    while i < len(aktive_zeilen):
        if aktive_zeilen[i].upper().startswith("SOURCE="):
            source = aktive_zeilen[i].split("=", 1)[1].strip().upper()
            if (
                i + 1 < len(aktive_zeilen)
                and aktive_zeilen[i + 1].upper().startswith("MODEL=")
            ):
                model = aktive_zeilen[i + 1].split("=", 1)[1].strip()
                if source == SOURCE_TYPE:
                    modelle.append(model)
                i += 2
                continue
        i += 1

    if modelle:
        log(f"run-scope.txt SOURCE=CSV aktiv: {modelle}", log_path)
    else:
        log("run-scope.txt: kein aktives SOURCE=CSV — Fallback auf Standardnamen", log_path)

    return modelle


# ----------------------------------------------------------
# Hauptlogik
# ----------------------------------------------------------

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_file = os.path.abspath(
        os.path.join(script_dir, "..", "..", "02-stages", "99-logs", "CSV00-root.resolved.txt")
    )

    if not os.path.isfile(root_file):
        print("[CSV06] ERROR | CSV00-root.resolved.txt nicht gefunden", file=sys.stderr)
        sys.exit(1)

    with open(root_file, "r", encoding="utf-8") as f:
        root = f.readline().strip()

    child_dir      = os.path.join(root, "01-artifacts", "02-csv", "03-child", "00-archimatechild")
    master_dir     = os.path.join(root, "01-artifacts", "02-csv", "00-master")
    log_dir        = os.path.join(root, "02-stages", "99-logs")
    run_scope_path = os.path.join(root, "02-stages", "run-scope.txt")

    log_path = os.path.join(log_dir, "CSV06-append.log")

    # Dateinamen aus run-scope.txt lesen — Fallback auf hardcoded Namen
    csv_scope = read_csv_scope(run_scope_path, log_path)
    files = csv_scope if csv_scope else FALLBACK_FILES

    for fname in files:
        child_path  = os.path.join(child_dir, fname)
        # Master-Dateiname: Prefix abschneiden via endswith
        # Funktioniert unabhaengig von Leerzeichen im Prefix
        # Beispiel: "MUNI FLOWelements.csv" → "elements.csv"
        master_fname = next((f for f in FALLBACK_FILES if fname.endswith(f)), fname)
        master_path  = os.path.join(master_dir, master_fname)

        if not os.path.isfile(child_path):
            msg = f"Child CSV fehlt, übersprungen: {fname}"
            log(msg, log_path)
            continue

        if not os.path.isfile(master_path):
            msg = f"Master CSV fehlt, übersprungen: {master_fname}"
            log(msg, log_path)
            continue

        with open(child_path, "r", encoding="utf-8") as src:
            lines = src.readlines()

        if len(lines) <= 1:
            msg = f"Keine Datenzeilen in child CSV: {fname}"
            log(msg, log_path)
            continue

        data_lines = lines[1:]  # Header überspringen

        ensure_trailing_newline(master_path)

        with open(master_path, "a", encoding="utf-8", newline="") as tgt:
            for line in data_lines:
                tgt.write(line)

        msg = f"{len(data_lines)} Zeilen aus {fname} → {master_fname} eingefügt"
        log(msg, log_path)

    log("Append-Zyklus abgeschlossen", log_path)


if __name__ == "__main__":
    main()
