================================================================================
HLP08 – HOW2 ID-MERGE-RUN (DEV)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : HLP08_How2_ID-Merge-Run
Tag             : #dev #how2 #hlp #hlp08 #idmerge #s5
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-15
================================================================================

## Structure-Bootstrapping: Von structure.txt zum stabilen Archi-Modell

## Zweck

Dieses How2 beschreibt den vollständigen Prozess um die Blueprint-Ordnerstruktur
(`structure.txt`) als ArchiMate-Elemente in ein bestehendes Archi 5.8 Modell
zu importieren und stabile IDs zu erhalten.

Der Prozess besteht aus **zwei Runs** mit einem manuellen Eingriff dazwischen.

---

## Voraussetzungen

- Blueprint-Root ist konfiguriert (`root.cfg`)
- `structure.txt` ist aktuell (frisch generiert)
- `HLP08_structure2xml.py` liegt in `01-artifacts\01-scripts\`
- Ziel-Modell in Archi 5.8 ist offen (leeres oder bestehendes Modell)
- run-scope.txt ist bekannt und zugänglich

---

## Schritt 0 — Vorbereitung: Master-Stack bereinigen

**KRITISCH — immer vor einem neuen ID-Merge-Run ausführen!**

Der CSV-Flow ist Append-only. Ohne diesen Schritt entstehen Mehrfacheinträge
im Archi-Modell (Duplikate).

```powershell
# Master CSVs leeren — nur Header behalten
$m = "C:\Prototyping\R+MUNI\01-artifacts\02-csv\00-master"
"ID,Type,Name,Documentation,Specialization" | Set-Content "$m\elements.csv" -Encoding UTF8
"ID,Type,Name,Documentation,Source,Target,Specialization" | Set-Content "$m\relations.csv" -Encoding UTF8
"ID,Key,Value" | Set-Content "$m\properties.csv" -Encoding UTF8

# master.xml löschen
Remove-Item "C:\Prototyping\R+MUNI\01-artifacts\00-xml\00-master\master.xml" -ErrorAction SilentlyContinue
```

---

## Run 1 — Strukturimport (nur Elemente)

### Schritt 1 — Frische structure.txt erzeugen

```powershell
cd "C:\Prototyping\R+MUNI"
tree /f /a > structure.txt
```

### Schritt 2 — HLP08 ausführen

```powershell
cd "C:\Prototyping\R+MUNI\01-artifacts\01-scripts"
py .\HLP08_structure2xml.py
```

Erwartete Ausgabe:
```
✅ 277 Elemente (67 Ordner, 210 Dateien), 264 Relationen
   → ...\01-artifacts\00-xml\03-child\00-archimatechild\muni2import.xml
```

### Schritt 3 — run-scope.txt prüfen

Folgende Einträge müssen aktiv (uncommentiert) sein:
```
SOURCE=OEF
MODEL=muni2import.xml

SOURCE=MASTER
MODEL=muni2import.xml
```

Alle anderen Einträge können aktiv bleiben oder auskommentiert werden
je nach gewünschtem Modell-Scope.

### Schritt 4 — XML-Flow ausführen

```powershell
py .\XML00-resolve_root.py
py .\XML01-collect_sources.py
py .\XML02-parse_child_xml.py
py .\XML03-build_index.py
py .\XML04-merge_master.py
py .\XML05-clear_merge.py
py .\XML06-finalize-master.py
py .\XML07-cleanup-artifacts.py
```

Alle Schritte müssen mit OK abschließen.

### Schritt 5 — CSV-Flow ausführen

```powershell
py .\CSV00-validate_environment.py
py .\CSV09-masterxml2csv.py
py .\CSV98-clean_master.py
py .\CSV99-export_snapshot.py
```

### Schritt 6 — Import-Folder vorbereiten

**Nur elements.csv importieren in Run 1** — properties und relations
haben noch keine stabilen IDs und würden Fehler erzeugen:

```powershell
# properties.csv und relations.csv aus Import-Folder entfernen
$i = "C:\Prototyping\R+MUNI\01-artifacts\02-csv\04-import"
Remove-Item "$i\properties.csv" -ErrorAction SilentlyContinue
Remove-Item "$i\relations.csv" -ErrorAction SilentlyContinue
```

### Schritt 7 — Archi CSV Import (Run 1)

In Archi 5.8:
1. **File → Import → CSV → in bestehendes Modell**
2. `01-artifacts\02-csv\04-import\elements.csv` auswählen
3. Import bestätigen

Archi vergibt jetzt **stabile IDs** für alle importierten Elemente.

### Schritt 8 — OEF Export aus Archi

Nach dem Import das Modell als OEF exportieren:
1. **File → Export → Model to Open Exchange XML Format**
2. Speichern als neuer Modellname (z.B. `MUNI TESTI.xml`) in
   `01-artifacts\00-xml\03-child\00-archimatechild\`

---

## Manueller Eingriff zwischen Run 1 und Run 2

### run-scope.txt anpassen

`muni2import.xml` auskommentieren — ab jetzt läuft nur noch
das stabile OEF-Modell aus Archi:

```
# muni2import.xml deaktivieren nach Run 1:
#SOURCE=OEF
#MODEL=muni2import.xml

#SOURCE=MASTER
#MODEL=muni2import.xml

# Stabiles Modell aktivieren:
SOURCE=OEF
MODEL=MUNI TESTI.xml

SOURCE=MASTER
MODEL=MUNI TESTI.xml
```

### Master-Stack nochmals bereinigen

```powershell
$m = "C:\Prototyping\R+MUNI\01-artifacts\02-csv\00-master"
"ID,Type,Name,Documentation,Specialization" | Set-Content "$m\elements.csv" -Encoding UTF8
"ID,Type,Name,Documentation,Source,Target,Specialization" | Set-Content "$m\relations.csv" -Encoding UTF8
"ID,Key,Value" | Set-Content "$m\properties.csv" -Encoding UTF8
Remove-Item "C:\Prototyping\R+MUNI\01-artifacts\00-xml\00-master\master.xml" -ErrorAction SilentlyContinue
```

---

## Run 2 — Vollständiger Import mit stabilen IDs

### Schritt 1 — XML-Flow ausführen

```powershell
py .\XML00-resolve_root.py
py .\XML01-collect_sources.py
py .\XML02-parse_child_xml.py
py .\XML03-build_index.py
py .\XML04-merge_master.py
py .\XML05-clear_merge.py
py .\XML06-finalize-master.py
py .\XML07-cleanup-artifacts.py
```

### Schritt 2 — CSV-Flow ausführen

```powershell
py .\CSV00-validate_environment.py
py .\CSV09-masterxml2csv.py
py .\CSV98-clean_master.py
py .\CSV99-export_snapshot.py
```

### Schritt 3 — Archi CSV Import (Run 2)

In Archi 5.8:
1. **File → Import → CSV → in bestehendes Modell**
2. `01-artifacts\02-csv\04-import\` — alle drei Files:
   - `elements.csv`
   - `relations.csv`
   - `properties.csv`
3. Import bestätigen

Jetzt sind stabile IDs vorhanden — Properties und Relations
werden korrekt den Elementen zugeordnet.

---

## Bekannte Einschränkungen

| # | Einschränkung | Workaround |
|---|---|---|
| 1 | OEF Type `TechnologyArtifact` ≠ Archi CSV Type | Archi importiert `TechnologyArtifact` korrekt wenn über XML-Flow→CSV09 verarbeitet |
| 2 | HLP08 erzeugt bei jedem Lauf neue UUIDs | Master-Stack vor jedem Run leeren (Schritt 0) |
| 3 | run-scope.txt manuell anpassen | Bewusst manuell — Automatisierung via S2C-Reihe im Backlog |
| 4 | Duplikate wenn Master-Stack nicht geleert | Schritt 0 konsequent ausführen |

---

## Langfristige Lösung

Die S2C-Reihe (Structure to CSV/Archi) im Backlog adressiert alle
Einschränkungen dieses manuellen Prozesses:
- Automatische Type-Normalisierung
- Guard-Funktion ersetzt manuellen run-scope.txt Eingriff
- ID-Stabilisierung ohne manuellen OEF-Export

→ Referenz: `Sprint-DEF-S2C-StructureImport.md`

---

*HOW2-HLP08-ID-Merge-Run | Stage 5 | 2026-03-15*
