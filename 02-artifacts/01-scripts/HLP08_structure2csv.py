import csv
import re
import uuid
from collections import Counter
from pathlib import Path

# Root-Auflösung über root.txt — Script kann von überall aufgerufen werden
ROOT = Path(__file__).parent / "root.txt"
if not ROOT.exists():
    raise FileNotFoundError(f"root.txt nicht gefunden in: {ROOT.parent}")

BASE = ROOT.parent  # Projektverzeichnis = Ordner wo root.txt liegt

INPUT_FILE    = BASE / "structure.txt"
OUT_ELEMENTS  = BASE / "02-artifacts" / "02-csv" / "04-import" / "elements.csv"
OUT_RELATIONS = BASE / "02-artifacts" / "02-csv" / "04-import" / "relations.csv"


def parse_tree(lines):
    entries = []
    for raw in lines:
        line = raw.rstrip("\r\n")
        if not line.strip():
            continue
        m = re.match(r'^([|+\\ \-]*)([^\|+\\\-\s].*)$', line)
        if not m:
            continue
        prefix = m.group(1)
        name = m.group(2).strip()
        if not name:
            continue
        depth = len(prefix) // 4
        is_folder = not bool(re.search(r'\.\w{1,10}$', name))
        entries.append((depth, name, is_folder))
    return entries


def build_records(entries):
    stack = {}
    records = []
    for depth, name, is_folder in entries:
        stack = {d: n for d, n in stack.items() if d < depth}
        stack[depth] = name
        full_path = "/".join(stack[d] for d in sorted(stack))
        parent_keys = sorted(k for k in stack if k < depth)
        parent_path = "/".join(stack[k] for k in parent_keys) if parent_keys else None
        records.append({
            "name": name,
            "full_path": full_path,
            "parent_path": parent_path,
            "is_folder": is_folder,
            "depth": depth,
        })
    return records


def write_csvs(records):
    path_to_id = {}
    for r in records:
        r["id"] = "id-" + str(uuid.uuid4())
        path_to_id[r["full_path"]] = r["id"]

    OUT_ELEMENTS.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT_ELEMENTS, "w", newline="", encoding="utf-8") as f:
        fields = ["ID", "Type", "Name", "Documentation", "full_path", "item_type", "depth"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in records:
            w.writerow({
                "ID": r["id"],
                "Type": "TechnologyArtifact",
                "Name": r["name"],
                "Documentation": "",
                "full_path": r["full_path"],
                "item_type": "folder" if r["is_folder"] else "file",
                "depth": r["depth"],
            })

    rel_count = 0
    with open(OUT_RELATIONS, "w", newline="", encoding="utf-8") as f:
        fields = ["ID", "Type", "Name", "Documentation", "Source", "Target"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in records:
            if r["parent_path"] and r["parent_path"] in path_to_id:
                w.writerow({
                    "ID": "id-" + str(uuid.uuid4()),
                    "Type": "CompositionRelationship",
                    "Name": "",
                    "Documentation": "",
                    "Source": path_to_id[r["parent_path"]],
                    "Target": r["id"],
                })
                rel_count += 1

    return len(records), rel_count


def main():
    with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    start = next((i + 1 for i, l in enumerate(lines) if l.strip().startswith("C:.")), 3)
    entries = parse_tree(lines[start:])
    records = build_records(entries)
    n_elem, n_rel = write_csvs(records)

    print(f"✅ {n_elem} Elemente, {n_rel} Relationen")
    print(f"   → {OUT_ELEMENTS}")
    print(f"   → {OUT_RELATIONS}")

    depth_dist = Counter(r["depth"] for r in records)
    for d in sorted(depth_dist):
        ftype = Counter("folder" if r["is_folder"] else "file" for r in records if r["depth"] == d)
        print(f"   Tiefe {d}: {depth_dist[d]} ({ftype.get('folder',0)} Ordner, {ftype.get('file',0)} Dateien)")


if __name__ == "__main__":
    main()
