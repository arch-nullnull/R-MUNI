# =============================================================
# HLP99-mkdir.py
# =============================================================
# Reihe   : HLP
# Zweck   : Vollständige R+MUNI Ordnerstruktur anlegen
#           (ausgehend vom <rootfolder> laut root.cfg)
# Outcome : Alle Ordner gemäß structure.txt existieren
# Stage   : S8
# =============================================================

import os
import sys

# --- Root auflösen via HLP00 ---------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from HLP00_resolve_root import get_root_cfg

cfg = get_root_cfg()
root = cfg["<rootfolder>"]

print(f"[HLP99] root resolved → {root}")

# =============================================================
# ORDNERSTRUKTUR — vollständig nach structure.txt
# Pfade relativ zu <rootfolder>
# =============================================================

FOLDERS = [
    # 00-model
    r"00-model\00-archimate\00-archimateactive",
    r"00-model\00-archimate\01-archimateactivesub",
    r"00-model\00-archimate\99-mappingmodel",
    r"00-model\01-bpmn\00-bpmnactive",
    r"00-model\01-bpmn\99-bpmnMUNI",
    r"00-model\02-xyvision",

    # 01-artifacts / 00-xml
    r"01-artifacts\00-xml\00-master",
    r"01-artifacts\00-xml\01-mapping",
    r"01-artifacts\00-xml\02-sync",
    r"01-artifacts\00-xml\03-child\00-archimatechild",
    r"01-artifacts\00-xml\03-child\01-bpmnchild",
    r"01-artifacts\00-xml\03-child\02-xychild",
    r"01-artifacts\00-xml\04-import",
    r"01-artifacts\00-xml\99-exports",

    # 01-artifacts / 01-scripts
    r"01-artifacts\01-scripts\jArchi\examples\Change type to\1. Strategy",
    r"01-artifacts\01-scripts\jArchi\examples\Change type to\2. Business",
    r"01-artifacts\01-scripts\jArchi\examples\Change type to\3. Application",
    r"01-artifacts\01-scripts\jArchi\examples\Change type to\4. Technology & Physical",
    r"01-artifacts\01-scripts\jArchi\examples\Change type to\5. Motivation",
    r"01-artifacts\01-scripts\jArchi\examples\Change type to\6. Implementation & Migration",
    r"01-artifacts\01-scripts\jArchi\examples\Change type to\7. Other",
    r"01-artifacts\01-scripts\jArchi\examples\Change type to\8. Relations",
    r"01-artifacts\01-scripts\jArchi\examples\lib",

    # 01-artifacts / 02-csv
    r"01-artifacts\02-csv\00-master",
    r"01-artifacts\02-csv\01-mapping",
    r"01-artifacts\02-csv\02-sync",
    r"01-artifacts\02-csv\03-child\00-archimatechild",
    r"01-artifacts\02-csv\03-child\01-bpmnchild",
    r"01-artifacts\02-csv\03-child\02-xychild",
    r"01-artifacts\02-csv\04-import",
    r"01-artifacts\02-csv\99-exports",

    # 01-artifacts / 03-XLSX
    r"01-artifacts\03-XLSX\00-master",
    r"01-artifacts\03-XLSX\01-mapping",
    r"01-artifacts\03-XLSX\02-sync",
    r"01-artifacts\03-XLSX\03-child\00-archimatechild",
    r"01-artifacts\03-XLSX\03-child\01-bpmnchild",
    r"01-artifacts\03-XLSX\03-child\02-xychild",
    r"01-artifacts\03-XLSX\04-import",
    r"01-artifacts\03-XLSX\99-exports",

    # 01-artifacts / 04-flow
    r"01-artifacts\04-flow\00-archimateFLW",
    r"01-artifacts\04-flow\01-bpmnFLW",

    # 01-artifacts / 05-reports
    r"01-artifacts\05-reports\00-archimate",
    r"01-artifacts\05-reports\01-bpmn",
    r"01-artifacts\05-reports\99-html",

    # 02-stages
    r"02-stages\00-archimatearchive",
    r"02-stages\01-bpmnarchive",
    r"02-stages\02-xyarchive",
    r"02-stages\99-logs",
]

# =============================================================
# AUSFÜHRUNG
# =============================================================

created = 0
existing = 0
errors = 0

for rel_path in FOLDERS:
    full_path = os.path.join(root, rel_path)
    try:
        if os.path.exists(full_path):
            print(f"  [OK]      bereits vorhanden → {rel_path}")
            existing += 1
        else:
            os.makedirs(full_path)
            print(f"  [ERSTELLT] {rel_path}")
            created += 1
    except Exception as e:
        print(f"  [FEHLER]  {rel_path} → {e}")
        errors += 1

# =============================================================
# ZUSAMMENFASSUNG
# =============================================================

print()
print("=" * 60)
print(f"[HLP99] Abgeschlossen")
print(f"        Erstellt : {created}")
print(f"        Vorhanden: {existing}")
print(f"        Fehler   : {errors}")
print("=" * 60)

if errors > 0:
    sys.exit(1)
