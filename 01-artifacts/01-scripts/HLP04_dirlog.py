"""
HLP04 – Ordnerinhalte in ein .log File schreiben
MUNI App Helper Scripts

Verwendung:
    python HLP04_dirlog.py <ordner> [<ordner2> ...]
    python HLP04_dirlog.py .                    ← aktuelles Verzeichnis
    python HLP04_dirlog.py data output assets   ← mehrere Ordner
"""

import os
import sys
import datetime

# ── Root-Auflösung ─────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "logs", "HLP04_dirlog.log")

# ── Hilfsfunktionen ────────────────────────────────────────────────────────────
def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write(f, msg: str):
    f.write(msg + "\n")
    print(msg)

def abs_path(p: str) -> str:
    return p if os.path.isabs(p) else os.path.join(ROOT, p)

def format_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

# ── Hauptlogik ─────────────────────────────────────────────────────────────────
def scan_folder(folder: str, f):
    folder = abs_path(folder)

    if not os.path.isdir(folder):
        write(f, f"  [SKIP]  Ordner nicht gefunden: {folder}")
        return

    write(f, f"\n{'─'*60}")
    write(f, f"  Ordner : {folder}")
    write(f, f"  Scan   : {timestamp()}")
    write(f, f"{'─'*60}")

    total_files = 0
    total_size  = 0

    for dirpath, dirnames, filenames in os.walk(folder):
        dirnames.sort()
        filenames.sort()

        # Relativer Einzug
        depth  = dirpath.replace(folder, "").count(os.sep)
        indent = "  " + "│  " * depth

        rel_dir = os.path.relpath(dirpath, folder)
        label   = "." if rel_dir == "." else rel_dir
        write(f, f"{indent}📁 {label}/")

        sub_indent = indent + "   "
        for filename in filenames:
            filepath  = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(filepath)
            except OSError:
                size = 0
            total_files += 1
            total_size  += size
            write(f, f"{sub_indent}📄 {filename}  ({format_size(size)})")

    write(f, f"\n  Gesamt : {total_files} Datei(en), {format_size(total_size)}")

def main():
    if len(sys.argv) < 2:
        print("Verwendung: python HLP04_dirlog.py <ordner> [<ordner2> ...]")
        sys.exit(1)

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        write(f, f"\n{'='*60}")
        write(f, f"  HLP04 – Directory Log  |  {timestamp()}")
        write(f, f"{'='*60}")

        for folder in sys.argv[1:]:
            scan_folder(folder, f)

        write(f, f"\n{'='*60}  Ende\n")

    print(f"\n  [OK] Log geschrieben → {LOG_FILE}")

if __name__ == "__main__":
    main()
