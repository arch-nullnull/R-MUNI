"""
HLP03 – Cleaner: Ordnerinhalt löschen (Ordner selbst bleibt erhalten)
MUNI App Helper Scripts

Verwendung:
    python HLP03_clean.py <ordner> [<ordner2> ...]
    python HLP03_clean.py cache temp output   ← mehrere Ordner gleichzeitig
"""

import os
import sys
import shutil
import datetime

# ── Root-Auflösung ─────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "logs", "HLP03_clean.log")

# ── Hilfsfunktionen ────────────────────────────────────────────────────────────
def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg: str):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp()}] {msg}\n")
    print(f"[{timestamp()}] {msg}")

def abs_path(p: str) -> str:
    return p if os.path.isabs(p) else os.path.join(ROOT, p)

# ── Hauptlogik ─────────────────────────────────────────────────────────────────
def clean_folder(folder: str):
    folder = abs_path(folder)

    if not os.path.isdir(folder):
        log(f"[SKIP]  Ordner nicht gefunden: {folder}")
        return

    removed_files = 0
    removed_dirs  = 0
    errors        = 0

    for entry in os.listdir(folder):
        entry_path = os.path.join(folder, entry)
        try:
            if os.path.isfile(entry_path) or os.path.islink(entry_path):
                os.remove(entry_path)
                removed_files += 1
                log(f"  [DEL-F]  {entry_path}")
            elif os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
                removed_dirs += 1
                log(f"  [DEL-D]  {entry_path}")
        except Exception as e:
            log(f"  [FEHLER] {entry_path} – {e}")
            errors += 1

    log(f"[OK]  {folder} bereinigt — "
        f"{removed_files} Datei(en), {removed_dirs} Unterordner gelöscht, {errors} Fehler.")

def main():
    if len(sys.argv) < 2:
        print("Verwendung: python HLP03_clean.py <ordner> [<ordner2> ...]")
        sys.exit(1)

    log(f"{'='*50}  Start HLP03 Clean")
    for folder in sys.argv[1:]:
        clean_folder(folder)
    log(f"{'='*50}  Ende HLP03 Clean")

if __name__ == "__main__":
    main()
