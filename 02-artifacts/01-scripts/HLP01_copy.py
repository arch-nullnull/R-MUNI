"""
HLP01 – Copy & Paste Script (Quelldatei bleibt erhalten)
MUNI App Helper Scripts

Verwendung:
    python HLP01_copy.py <quelle> <ziel>
    python HLP01_copy.py ordner_a/datei.txt ordner_b/datei.txt
    python HLP01_copy.py ordner_a ordner_b           ← ganzer Ordner
"""

import os
import sys
import shutil
import datetime

# ── Root-Auflösung ─────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "logs", "HLP01_copy.log")

# ── Hilfsfunktionen ────────────────────────────────────────────────────────────
def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg: str):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp()}] {msg}\n")
    print(f"[{timestamp()}] {msg}")

def abs_path(p: str) -> str:
    """Pfad relativ zu ROOT auflösen."""
    return p if os.path.isabs(p) else os.path.join(ROOT, p)

# ── Hauptlogik ─────────────────────────────────────────────────────────────────
def copy(src: str, dst: str):
    src = abs_path(src)
    dst = abs_path(dst)

    if not os.path.exists(src):
        log(f"[FEHLER] Quelle nicht gefunden: {src}")
        sys.exit(1)

    # Datei → Datei / Datei → Ordner
    if os.path.isfile(src):
        os.makedirs(dst if dst.endswith(os.sep) or not os.path.splitext(dst)[1] else os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        log(f"[COPY]  {src}  →  {dst}")

    # Ordner → Ordner (rekursiv)
    elif os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        log(f"[COPY]  Ordner {src}  →  {dst}")

    log("[OK] Copy abgeschlossen.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Verwendung: python HLP01_copy.py <quelle> <ziel>")
        sys.exit(1)

    copy(sys.argv[1], sys.argv[2])
