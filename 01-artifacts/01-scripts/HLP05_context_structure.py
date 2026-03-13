"""
HLP05 – Context File & Structure File erstellen und ablegen
MUNI App Helper Scripts

  context.json  →  Metadaten, Laufzeitinfos, Konfiguration
  structure.json →  Komplette Ordner-/Dateistruktur als JSON-Baum

Verwendung:
    python HLP05_context_structure.py                  ← Root scannen
    python HLP05_context_structure.py <ordner>         ← bestimmten Ordner scannen
    python HLP05_context_structure.py --context-only   ← nur context.json
    python HLP05_context_structure.py --structure-only ← nur structure.json
"""

import os
import sys
import json
import platform
import datetime

# ── Root-Auflösung ─────────────────────────────────────────────────────────────
ROOT     = os.path.dirname(os.path.abspath(__file__))
OUT_DIR  = os.path.join(ROOT, "context")
CTX_FILE = os.path.join(OUT_DIR, "context.json")
STR_FILE = os.path.join(OUT_DIR, "structure.json")
LOG_FILE = os.path.join(ROOT, "logs", "HLP05_context.log")

# ── Hilfsfunktionen ────────────────────────────────────────────────────────────
def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg: str):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp()}] {msg}\n")
    print(f"[{timestamp()}] {msg}")

def format_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

# ── Context File ───────────────────────────────────────────────────────────────
def build_context() -> dict:
    return {
        "meta": {
            "generated_by" : "HLP05_context_structure.py",
            "generated_at" : timestamp(),
            "version"      : "1.0.0",
        },
        "environment": {
            "os"           : f"{platform.system()} {platform.release()}",
            "architecture" : platform.machine(),
            "python"       : sys.version.split()[0],
            "hostname"     : platform.node(),
        },
        "paths": {
            "root"         : ROOT,
            "context_dir"  : OUT_DIR,
            "context_file" : CTX_FILE,
            "structure_file": STR_FILE,
            "log_file"     : LOG_FILE,
            "cwd"          : os.getcwd(),
        },
        "app": {
            "name"         : "MUNI",
            "description"  : "MUNI App – Helper Script Context",
            "note"         : "Dieses File wird automatisch von HLP05 generiert.",
        }
    }

def write_context():
    os.makedirs(OUT_DIR, exist_ok=True)
    ctx = build_context()
    with open(CTX_FILE, "w", encoding="utf-8") as f:
        json.dump(ctx, f, indent=2, ensure_ascii=False)
    log(f"[OK] context.json erstellt → {CTX_FILE}")

# ── Structure File ─────────────────────────────────────────────────────────────
def build_tree(path: str, skip_dirs: set = None) -> dict:
    """Rekursiver Aufbau eines JSON-Baums für einen Ordner."""
    if skip_dirs is None:
        skip_dirs = {".git", "__pycache__", ".venv", "node_modules", ".idea"}

    name = os.path.basename(path) or path
    node = {"name": name, "type": "directory", "children": []}

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        node["error"] = "Permission denied"
        return node

    for entry in entries:
        if entry in skip_dirs:
            continue
        entry_path = os.path.join(path, entry)

        if os.path.isdir(entry_path):
            node["children"].append(build_tree(entry_path, skip_dirs))
        elif os.path.isfile(entry_path):
            try:
                size = os.path.getsize(entry_path)
            except OSError:
                size = 0
            node["children"].append({
                "name"  : entry,
                "type"  : "file",
                "size"  : format_size(size),
                "bytes" : size,
            })

    node["file_count"] = sum(
        1 for c in node["children"] if c.get("type") == "file"
    )
    node["dir_count"] = sum(
        1 for c in node["children"] if c.get("type") == "directory"
    )
    return node

def write_structure(scan_path: str):
    os.makedirs(OUT_DIR, exist_ok=True)
    tree = build_tree(scan_path)
    structure = {
        "meta": {
            "generated_by": "HLP05_context_structure.py",
            "generated_at": timestamp(),
            "scan_root"   : scan_path,
        },
        "tree": tree
    }
    with open(STR_FILE, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    log(f"[OK] structure.json erstellt → {STR_FILE}")

# ── Entry Point ────────────────────────────────────────────────────────────────
def main():
    args         = sys.argv[1:]
    context_only = "--context-only"  in args
    struct_only  = "--structure-only" in args

    # Zielordner bestimmen (erstes Argument, das kein Flag ist)
    scan_path = ROOT
    for a in args:
        if not a.startswith("--"):
            candidate = a if os.path.isabs(a) else os.path.join(ROOT, a)
            if os.path.isdir(candidate):
                scan_path = candidate
            else:
                log(f"[WARN] Ordner nicht gefunden, benutze ROOT: {candidate}")
            break

    log(f"{'='*50}  Start HLP05")

    if not struct_only:
        write_context()

    if not context_only:
        write_structure(scan_path)

    log(f"{'='*50}  Ende HLP05")
    print(f"\n  Output-Ordner: {OUT_DIR}")

if __name__ == "__main__":
    main()
