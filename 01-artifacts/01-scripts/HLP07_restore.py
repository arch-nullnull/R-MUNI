"""
HLP07 – Restore Script
MUNI App Helper Scripts

Spielt ein von HLP06 erstelltes Backup (.zip) wieder ein.
Liest das eingebettete manifest.json, validiert Checksums und stellt
alle Dateien wieder her — OS-agnostisch.

Verwendung:
    python HLP07_restore.py <backup.zip>                       ← Restore → Original-Pfad
    python HLP07_restore.py <backup.zip> --dest <ordner>       ← Restore → anderen Ordner
    python HLP07_restore.py <backup.zip> --dry-run             ← nur prüfen, nichts schreiben
    python HLP07_restore.py <backup.zip> --verify-only         ← nur Checksums prüfen
    python HLP07_restore.py <backup.zip> --dest ./recovered --no-verify  ← ohne Checksums

Ausgabe:
    Wiederhergestellte Dateien im Zielordner
    logs/HLP07_restore.log
"""

import os
import sys
import json
import hashlib
import zipfile
import datetime
import argparse

# ── Root-Auflösung ─────────────────────────────────────────────────────────────
ROOT     = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "logs", "HLP07_restore.log")

# ── Hilfsfunktionen ────────────────────────────────────────────────────────────
def timestamp(fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(fmt)

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
    h = hashlib.new(algorithm)
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, IOError):
        return "ERROR"

# ── Manifest laden ─────────────────────────────────────────────────────────────
def load_manifest(zip_path: str) -> dict:
    """manifest.json aus dem ZIP lesen und als dict zurückgeben."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        if "manifest.json" not in zf.namelist():
            log("[FEHLER] Kein manifest.json im Archiv gefunden.")
            log("         Ist dies ein gültiges HLP06-Backup?")
            sys.exit(1)
        with zf.open("manifest.json") as mf:
            return json.load(mf)

def print_manifest_info(manifest: dict):
    log(f"  {'─'*56}")
    log(f"  Backup-Info aus manifest.json:")
    log(f"    Erstellt am : {manifest.get('created_at', '?')}")
    log(f"    Quelle      : {manifest.get('source_root', '?')}")
    log(f"    Dateien     : {manifest['stats'].get('file_count', '?')}")
    log(f"    Größe       : {manifest['stats'].get('total_size', '?')}")
    plat = manifest.get("platform", {})
    log(f"    Erstellt auf: {plat.get('os', '?')} {plat.get('release', '')} / "
        f"Python {plat.get('python', '?')}")
    log(f"  {'─'*56}")

# ── Checksum-Verifikation ──────────────────────────────────────────────────────
def verify_checksums(manifest: dict, dest: str) -> tuple[int, int]:
    """
    Vergleicht die im Manifest gespeicherten SHA-256 Hashes mit den
    tatsächlich wiederhergestellten Dateien.
    Gibt (ok_count, fail_count) zurück.
    """
    ok = fail = 0
    has_checksums = any("sha256" in f for f in manifest.get("files", []))

    if not has_checksums:
        log("  [INFO] Manifest enthält keine Checksums – Verifikation übersprungen.")
        return 0, 0

    log("  Checksum-Verifikation läuft ...")
    for entry in manifest.get("files", []):
        if "sha256" not in entry:
            continue
        rel   = entry["path"].replace("/", os.sep)
        fpath = os.path.join(dest, rel)

        if not os.path.exists(fpath):
            log(f"    [MISSING]  {entry['path']}")
            fail += 1
            continue

        actual   = file_checksum(fpath)
        expected = entry["sha256"]

        if actual == expected:
            ok += 1
        else:
            log(f"    [MISMATCH] {entry['path']}")
            log(f"               erwartet : {expected}")
            log(f"               erhalten : {actual}")
            fail += 1

    return ok, fail

# ── Restore-Kern ───────────────────────────────────────────────────────────────
def restore(zip_path: str, dest: str | None, dry_run: bool,
            verify_only: bool, no_verify: bool):

    zip_path = abs_path(zip_path)

    if not os.path.isfile(zip_path):
        log(f"[FEHLER] Backup-Archiv nicht gefunden: {zip_path}")
        sys.exit(1)

    log(f"{'='*60}  HLP07 Restore Start")
    log(f"  Archiv  : {zip_path}")

    # Manifest laden
    manifest = load_manifest(zip_path)
    print_manifest_info(manifest)

    # Zielordner bestimmen
    if dest:
        restore_root = abs_path(dest)
    else:
        restore_root = manifest.get("source_root", ROOT)
        log(f"  [INFO] Kein --dest angegeben → Restore nach Original-Pfad:")
        log(f"         {restore_root}")

    log(f"  Ziel    : {restore_root}")
    if dry_run:
        log("  [DRY-RUN] Keine Dateien werden geschrieben.")

    # Nur Checksums prüfen (kein Extract)
    if verify_only:
        log("  [VERIFY-ONLY] Nur Checksums werden geprüft ...")
        if not os.path.isdir(restore_root):
            log(f"[FEHLER] --verify-only benötigt bereits extrahierte Dateien in: {restore_root}")
            sys.exit(1)
        ok, fail = verify_checksums(manifest, restore_root)
        log(f"  Verifikation: {ok} OK, {fail} FEHLER")
        log(f"{'='*60}  Ende HLP07")
        return

    # Dateien extrahieren
    restored = skipped = errors = 0

    with zipfile.ZipFile(zip_path, "r") as zf:
        members = [m for m in zf.namelist()
                   if m.startswith("backup/") and not m.endswith("/")]

        for member in members:
            # Relativen Pfad aus dem Archiv extrahieren
            # member Format: "backup/relative/path/to/file.ext"
            rel_path = member[len("backup/"):]           # Prefix "backup/" entfernen
            rel_path = rel_path.replace("/", os.sep)     # OS-Pfadtrenner
            out_path = os.path.join(restore_root, rel_path)

            if dry_run:
                log(f"    [DRY] würde schreiben: {out_path}")
                restored += 1
                continue

            try:
                out_dir = os.path.dirname(out_path)
                os.makedirs(out_dir, exist_ok=True)

                with zf.open(member) as src, open(out_path, "wb") as dst:
                    dst.write(src.read())

                log(f"    [OK]  {rel_path}")
                restored += 1

            except Exception as e:
                log(f"    [!]   {rel_path} – FEHLER: {e}")
                errors += 1

    log(f"  {'─'*56}")
    log(f"  Restore: {restored} OK, {skipped} Skip, {errors} Fehler")

    # Checksum-Verifikation nach dem Restore
    if not dry_run and not no_verify:
        ok, fail = verify_checksums(manifest, restore_root)
        if fail == 0 and ok > 0:
            log(f"  Checksums: {ok} / {ok} ✓  Alle Dateien integer.")
        elif ok + fail == 0:
            log("  Checksums: –  (keine Checksums im Manifest)")
        else:
            log(f"  Checksums: {ok} OK, {fail} FEHLER – bitte Backup prüfen!")

    log(f"{'='*60}  Ende HLP07")

    if not dry_run:
        print(f"\n  ✓ Restore abgeschlossen → {restore_root}")
    else:
        print(f"\n  [DRY-RUN] Keine Dateien wurden geschrieben.")

# ── CLI ────────────────────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description="HLP07 – MUNI Restore Script",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("backup",
                        help="Pfad zum Backup-Archiv (.zip)")
    parser.add_argument("--dest", default=None,
                        help="Zielordner (Standard: Original-Pfad aus Manifest)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Nur simulieren, nichts schreiben")
    parser.add_argument("--verify-only", action="store_true",
                        help="Nur Checksums bereits vorhandener Dateien prüfen")
    parser.add_argument("--no-verify", action="store_true",
                        help="Checksum-Verifikation nach Restore überspringen")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    restore(
        zip_path    = args.backup,
        dest        = args.dest,
        dry_run     = args.dry_run,
        verify_only = args.verify_only,
        no_verify   = args.no_verify,
    )
