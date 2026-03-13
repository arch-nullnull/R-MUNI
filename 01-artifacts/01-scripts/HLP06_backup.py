"""
HLP06 – Backup Script
MUNI App Helper Scripts

Erstellt ein vollständiges, timestamped Backup der Umgebung als .zip Archiv.
Das Archiv enthält ein Manifest (manifest.json) das von HLP07 zum Restore
verwendet wird.

Verwendung:
    python HLP06_backup.py                              ← Root sichern → ./backups/
    python HLP06_backup.py --src  <ordner>              ← anderen Quellordner
    python HLP06_backup.py --dest <ordner>              ← anderen Zielordner
    python HLP06_backup.py --src data --dest D:/backups ← beides kombiniert
    python HLP06_backup.py --exclude cache temp .git    ← Ordner ausschließen

Ausgabe:
    <dest>/MUNI_backup_YYYYMMDD_HHMMSS.zip
    logs/HLP06_backup.log
"""

import os
import sys
import json
import hashlib
import zipfile
import platform
import datetime
import argparse

# ── Root-Auflösung ─────────────────────────────────────────────────────────────
ROOT     = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "logs", "HLP06_backup.log")

# Standard-Ausschlüsse
DEFAULT_EXCLUDE = {
    ".git", "__pycache__", ".venv", "venv", "node_modules",
    ".idea", ".vscode", ".DS_Store", "Thumbs.db",
}

# ── Hilfsfunktionen ────────────────────────────────────────────────────────────
def timestamp(fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(fmt)

def timestamp_file():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def log(msg: str):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    line = f"[{timestamp()}] {msg}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)

def abs_path(p: str) -> str:
    return p if os.path.isabs(p) else os.path.join(ROOT, p)

def format_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def file_checksum(filepath: str, algorithm: str = "sha256") -> str:
    """SHA-256 Checksum einer Datei (für Integritätsprüfung beim Restore)."""
    h = hashlib.new(algorithm)
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, IOError):
        return "ERROR"

def collect_files(src: str, exclude: set) -> list[dict]:
    """Alle Dateien rekursiv sammeln, Ausschlüsse beachten."""
    collected = []
    for dirpath, dirnames, filenames in os.walk(src):
        # Ausgeschlossene Ordner in-place herausfiltern (verhindert weiteren Abstieg)
        dirnames[:] = sorted(d for d in dirnames if d not in exclude)
        filenames   = sorted(filenames)

        for filename in filenames:
            if filename in exclude:
                continue
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, src)
            try:
                size = os.path.getsize(filepath)
            except OSError:
                size = 0
            collected.append({
                "rel_path"  : rel_path,
                "abs_path"  : filepath,
                "size_bytes": size,
                "size_human": format_size(size),
            })
    return collected

# ── Manifest ───────────────────────────────────────────────────────────────────
def build_manifest(src: str, files: list[dict], zip_name: str,
                   exclude: list, checksums: bool = True) -> dict:
    log("  Manifest wird erstellt ...")
    file_entries = []
    for entry in files:
        e = {
            "path"      : entry["rel_path"].replace("\\", "/"),  # immer forward slash
            "size_bytes": entry["size_bytes"],
            "size_human": entry["size_human"],
        }
        if checksums:
            e["sha256"] = file_checksum(entry["abs_path"])
        file_entries.append(e)

    total_bytes = sum(f["size_bytes"] for f in files)

    return {
        "manifest_version": "1.0",
        "tool"            : "HLP06_backup.py",
        "restore_tool"    : "HLP07_restore.py",
        "created_at"      : timestamp(),
        "zip_name"        : zip_name,
        "source_root"     : src,
        "platform": {
            "os"          : platform.system(),
            "release"     : platform.release(),
            "machine"     : platform.machine(),
            "python"      : sys.version.split()[0],
            "hostname"    : platform.node(),
        },
        "stats": {
            "file_count"  : len(files),
            "total_size"  : format_size(total_bytes),
            "total_bytes" : total_bytes,
        },
        "exclude_list"    : sorted(exclude),
        "files"           : file_entries,
    }

# ── Backup-Kern ────────────────────────────────────────────────────────────────
def create_backup(src: str, dest: str, exclude: set, checksums: bool = True):
    src  = abs_path(src)
    dest = abs_path(dest)

    if not os.path.isdir(src):
        log(f"[FEHLER] Quellordner nicht gefunden: {src}")
        sys.exit(1)

    os.makedirs(dest, exist_ok=True)

    ts       = timestamp_file()
    zip_name = f"MUNI_backup_{ts}.zip"
    zip_path = os.path.join(dest, zip_name)

    log(f"{'='*60}  HLP06 Backup Start")
    log(f"  Quelle  : {src}")
    log(f"  Ziel    : {zip_path}")
    log(f"  Exclude : {sorted(exclude)}")
    log("  Dateien werden gesammelt ...")

    files = collect_files(src, exclude)
    log(f"  {len(files)} Datei(en) gefunden.")

    # Manifest bauen (inkl. Checksums)
    manifest = build_manifest(src, files, zip_name, sorted(exclude), checksums)
    manifest_json = json.dumps(manifest, indent=2, ensure_ascii=False)

    # ZIP erstellen
    log(f"  ZIP wird erstellt ...")
    written = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=6) as zf:

        # Alle gesammelten Dateien schreiben
        for entry in files:
            arcname = os.path.join("backup", entry["rel_path"])
            try:
                zf.write(entry["abs_path"], arcname)
                written += 1
                log(f"    [+] {entry['rel_path']}  ({entry['size_human']})")
            except (OSError, PermissionError) as e:
                log(f"    [!] SKIP  {entry['rel_path']} – {e}")

        # Manifest als letzte Datei einpacken
        zf.writestr("manifest.json", manifest_json)
        log("    [+] manifest.json  (eingebettet)")

    zip_size = os.path.getsize(zip_path)
    log(f"  {'─'*56}")
    log(f"  Backup fertig!")
    log(f"  Archiv   : {zip_path}")
    log(f"  Dateien  : {written} / {len(files)}")
    log(f"  Größe    : {format_size(zip_size)}")
    log(f"{'='*60}  Ende HLP06")

    print(f"\n  ✓ Backup gespeichert → {zip_path}")
    return zip_path

# ── CLI ────────────────────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description="HLP06 – MUNI Backup Script",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--src",  default=ROOT,
                        help="Quellordner (Standard: Root des Scripts)")
    parser.add_argument("--dest", default=os.path.join(ROOT, "backups"),
                        help="Zielordner für das Backup (Standard: ./backups/)")
    parser.add_argument("--exclude", nargs="*", default=[],
                        help="Zusätzliche Ordner/Dateien zum Ausschließen")
    parser.add_argument("--no-checksums", action="store_true",
                        help="SHA-256 Checksums überspringen (schneller)")
    return parser.parse_args()

if __name__ == "__main__":
    args    = parse_args()
    exclude = DEFAULT_EXCLUDE | set(args.exclude)
    create_backup(
        src       = args.src,
        dest      = args.dest,
        exclude   = exclude,
        checksums = not args.no_checksums,
    )
