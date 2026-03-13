"""
HLP02 – Ausschneiden Script (Quelldatei wird nach dem Verschieben gelöscht)
MUNI App Helper Scripts

Verwendung:
    python HLP02_move.py <quelle> <ziel>
    python HLP02_move.py ordner_a/datei.txt ordner_b/datei.txt
    python HLP02_move.py ordner_a ordner_b           ← ganzer Ordner
"""

import os
import sys
import shutil
import datetime

# ── Root-Auflösung ─────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "logs", "HLP02_move.log")

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
def move(src: str, dst: str):
    src = abs_path(src)
    dst = abs_path(dst)

    if not os.path.exists(src):
        log(f"[FEHLER] Quelle nicht gefunden: {src}")
        sys.exit(1)

    dst_dir = dst if os.path.isdir(dst) else os.path.dirname(dst)
    if dst_dir:
        os.makedirs(dst_dir, exist_ok=True)

    shutil.move(src, dst)
    log(f"[MOVE]  {src}  →  {dst}")
    log("[OK] Verschieben abgeschlossen. Quelldatei/-ordner gelöscht.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Verwendung: python HLP02_move.py <quelle> <ziel>")
        sys.exit(1)

    move(sys.argv[1], sys.argv[2])
