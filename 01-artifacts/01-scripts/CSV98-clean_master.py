#!/usr/bin/env python3
# CSV98-clean_master.py
#
# Zweck (Flow-Stage):
# - Master CSVs auf bekannte Qualitätsprobleme prüfen und bereinigen
# - Direkte Bereinigung in elements.csv, relations.csv, properties.csv
# - Lesbarer Report als Zusammenfassung der Fundstellen und Fixes
#
# Bekannte Probleme die bereinigt werden:
#   [FIX-01] Formula-Prefix: ="..." → ...
#            Ursache: Archi CSV-Export escaped Namen die mit 00- beginnen
#            als Excel-Formel. Beispiel: ="00-archimatechild" → 00-archimatechild
#   [FIX-02] Backtick/Accent ´ in Texten → '
#            Ursache: Copy-Paste aus verschiedenen Quellen (Word, OneNote etc.)
#            Beispiel: "Library´s" → "Library's"
#
# Quelle & Ziel:
#   <artifacts>\02-csv\00-master\elements.csv    (direkt überschrieben)
#   <artifacts>\02-csv\00-master\relations.csv   (direkt überschrieben)
#   <artifacts>\02-csv\00-master\properties.csv  (direkt überschrieben)
#
# Output:
#   <stages>\99-logs\CSV98-clean_master.log
#   <stages>\99-logs\CSV98-clean_master_report.txt
#
# Regeln:
# - Liest CSV00-root.resolved.txt als Root-Referenz
# - Idempotent — mehrfaches Ausführen ist sicher
# - Kein mkdir
# - Hard fail bei technischen Fehlern
# - Cleaning Run 5.5 | Stage 5

import os
import sys
import csv
import re
from datetime import datetime


# ----------------------------------------------------------
# Konstanten
# ----------------------------------------------------------

SCRIPT_KUERZEL = "CSV98"
LOG_FILENAME   = "CSV98-clean_master.log"
REPORT_FILENAME = "CSV98-clean_master_report.txt"

MASTER_FILES = ["elements.csv", "relations.csv", "properties.csv"]

# Bekannte Fix-Regeln: (ID, Beschreibung, Prüffunktion, Fix-Funktion)
# Werden auf jeden Feldwert angewendet
FIX_RULES = [
    (
        "FIX-01",
        "Formula-Prefix: =\\\"...\\\" → ...",
        lambda v: bool(re.match(r'^=".*"$', v)),
        lambda v: re.sub(r'^="(.*)"$', r'\1', v),
    ),
    (
        "FIX-02",
        "Backtick/Accent ´ → '",
        lambda v: "´" in v,
        lambda v: v.replace("´", "'"),
    ),
]


# ----------------------------------------------------------
# Hilfsfunktionen
# ----------------------------------------------------------

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


# ----------------------------------------------------------
# Root aus CSV00-Artefakt lesen
# ----------------------------------------------------------

def read_root_resolved(script_dir: str) -> str:
    path = os.path.abspath(
        os.path.join(script_dir, "..", "..", "02-stages", "99-logs", "CSV00-root.resolved.txt")
    )
    if not os.path.isfile(path):
        die(f"CSV00-root.resolved.txt fehlt: {path}", None)
    with open(path, "r", encoding="utf-8") as f:
        root = f.readline().strip()
    if not root or not os.path.isdir(root):
        die(f"Ungültiger Root-Pfad: {root}", None)
    return root


# ----------------------------------------------------------
# CSV bereinigen
# ----------------------------------------------------------

def clean_csv(csv_path: str, log_path: str) -> dict:
    """
    Liest eine CSV, wendet alle Fix-Regeln an, schreibt sie zurück.
    Gibt einen Dict mit Statistiken pro Fix-Regel zurück.
    """
    if not os.path.isfile(csv_path):
        log(f"ÜBERSPRUNGEN (fehlt): {csv_path}", log_path)
        return {}

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    if not fieldnames:
        log(f"ÜBERSPRUNGEN (leer): {csv_path}", log_path)
        return {}

    # Statistiken pro Fix-Regel
    stats = {rule_id: [] for rule_id, _, _, _ in FIX_RULES}

    cleaned_rows = []
    for row_idx, row in enumerate(rows, start=2):  # Zeile 1 = Header
        cleaned_row = {}
        for field, value in row.items():
            if value is None:
                cleaned_row[field] = value
                continue
            current_value = value
            for rule_id, desc, check_fn, fix_fn in FIX_RULES:
                if check_fn(current_value):
                    fixed = fix_fn(current_value)
                    stats[rule_id].append({
                        "zeile": row_idx,
                        "feld": field,
                        "vorher": current_value,
                        "nachher": fixed,
                    })
                    current_value = fixed
            cleaned_row[field] = current_value
        cleaned_rows.append(cleaned_row)

    # Zurückschreiben
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()
        writer.writerows(cleaned_rows)

    total_fixes = sum(len(v) for v in stats.values())
    log(f"{os.path.basename(csv_path)} | {len(rows)} Zeilen geprüft | {total_fixes} Fixes", log_path)

    return stats


# ----------------------------------------------------------
# Report schreiben
# ----------------------------------------------------------

def write_report(
    report_path: str,
    results: dict,  # {filename: {rule_id: [hits]}}
    log_path: str,
) -> None:
    lines = []
    lines.append("=" * 60)
    lines.append(f"CSV98 Clean Master — Report")
    lines.append(f"Erstellt: {now_ts()}")
    lines.append("=" * 60)

    total_all = 0

    for fname, stats in results.items():
        file_total = sum(len(v) for v in stats.values())
        total_all += file_total
        lines.append(f"\n── {fname} ── ({file_total} Fixes)")

        for rule_id, desc, _, _ in FIX_RULES:
            hits = stats.get(rule_id, [])
            if not hits:
                continue
            lines.append(f"\n  [{rule_id}] {desc} — {len(hits)} Treffer")
            for hit in hits:
                lines.append(f"    Zeile {hit['zeile']:>4} | Feld: {hit['feld']}")
                lines.append(f"      Vorher : {hit['vorher'][:80]}")
                lines.append(f"      Nachher: {hit['nachher'][:80]}")

        if file_total == 0:
            lines.append("  Keine Probleme gefunden.")

    lines.append(f"\n{'=' * 60}")
    lines.append(f"GESAMT: {total_all} Fixes in {len(results)} Dateien")
    lines.append("=" * 60)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    log(f"Report geschrieben: {report_path}", log_path)


# ----------------------------------------------------------
# Hauptlogik
# ----------------------------------------------------------

def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_path  = read_root_resolved(script_dir)

    stages_dir    = os.path.join(root_path, "02-stages")
    logs_dir      = os.path.join(stages_dir, "99-logs")
    artifacts_dir = os.path.join(root_path, "01-artifacts")
    master_dir    = os.path.join(artifacts_dir, "02-csv", "00-master")

    log_path    = os.path.join(logs_dir, LOG_FILENAME)
    report_path = os.path.join(logs_dir, REPORT_FILENAME)

    log(f"Root: {root_path}", log_path)
    log(f"Master-Ordner: {master_dir}", log_path)

    if not os.path.isdir(master_dir):
        die(f"Master-Ordner fehlt: {master_dir}", log_path)

    # Alle Master CSVs bereinigen
    results = {}
    for fname in MASTER_FILES:
        csv_path = os.path.join(master_dir, fname)
        log(f"Prüfe: {fname}", log_path)
        stats = clean_csv(csv_path, log_path)
        results[fname] = stats

    # Report schreiben
    write_report(report_path, results, log_path)

    total = sum(
        sum(len(v) for v in stats.values())
        for stats in results.values()
    )

    print(f"[{SCRIPT_KUERZEL}] OK | {total} Fixes | Report -> {report_path}")


if __name__ == "__main__":
    main()
