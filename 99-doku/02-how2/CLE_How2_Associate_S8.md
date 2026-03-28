================================================================================
CLE CLEANING SCRIPTS — HOW2 (Associate)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : CLE_How2_Associate_S8
Tag             : #associate #how2 #cle #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : ENTWURF
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Hinweis         : Inhalt initial ident mit DEV-Gegenstück — inhaltliche Trennung in Stage 1
================================================================================

Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-15
Ablageort       : 00-concept/02-how2/CLE_How2_S5.md
================================================================================


VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- Python 3.10+ (keine externen Pakete erforderlich)
- root.cfg vorhanden und <rootfolder> korrekt eingetragen
- Scripts liegen in <rootfolder>\01-artifacts\01-scripts\
- Log-Ordner 02-stages\99-logs\ wird automatisch erstellt wenn nicht vorhanden


ZWEI MODI — KURZ ERKLÄRT
--------------------------------------------------------------------------------
Ordner-Clean  (CLE10–CLE53)  →  gesamter Ordnerinhalt wird gelöscht
Datei-Delete  (CLE26)        →  nur benannte Einzeldateien werden gelöscht


================================================================================
KURZREFERENZ — ALLE SCRIPTS
================================================================================


── BASIS ───────────────────────────────────────────────────────────────────────

CLE00 – Root-Diagnose und Referenz-Log für die CLE-Reihe
  py .\CLE00-resolve_root.py
  → Liest root.cfg, zeigt alle aufgelösten Pfade mit Status [OK / WARNUNG]
  → Schreibt Referenz-Log: 02-stages\99-logs\CLE00-resolve_root.log
  → Nützlich als erster Check wenn Pfade nicht stimmen


── XML-GRUPPE (01-artifacts\00-xml) ────────────────────────────────────────────

CLE10 – XML Master leeren
  py .\CLE10-xml_master.py
  → Ziel: 00-xml\00-master

CLE11 – Alle XML Child-Ordner leeren (ArchiMate + BPMN)
  py .\CLE11-xml_all_childs.py
  → Ziele: 00-xml\03-child\00-archimatechild
           00-xml\03-child\01-bpmnchild

CLE12 – XML ArchiMate Child leeren
  py .\CLE12-xml_archimate_child.py
  → Ziel: 00-xml\03-child\00-archimatechild

CLE13 – XML BPMN Child leeren
  py .\CLE13-xml_bpmn_child.py
  → Ziel: 00-xml\03-child\01-bpmnchild

CLE14 – XML Import leeren
  py .\CLE14-xml_import.py
  → Ziel: 00-xml\04-import

CLE15 – XML Export leeren
  py .\CLE15-xml_export.py
  → Ziel: 00-xml\99-exports


── CSV-GRUPPE (01-artifacts\02-csv) ────────────────────────────────────────────

CLE20 – CSV Master leeren
  py .\CLE20-csv_master.py
  → Ziel: 02-csv\00-master

CLE21 – Alle CSV Child-Ordner leeren (ArchiMate + BPMN)
  py .\CLE21-csv_all_childs.py
  → Ziele: 02-csv\03-child\00-archimatechild
           02-csv\03-child\01-bpmnchild

CLE22 – CSV ArchiMate Child leeren
  py .\CLE22-csv_archimate_child.py
  → Ziel: 02-csv\03-child\00-archimatechild

CLE23 – CSV BPMN Child leeren
  py .\CLE23-csv_bpmn_child.py
  → Ziel: 02-csv\03-child\01-bpmnchild

CLE24 – CSV Import leeren (gesamter Ordner)
  py .\CLE24-csv_import.py
  → Ziel: 02-csv\04-import (alle Dateien)

CLE25 – CSV Export leeren
  py .\CLE25-csv_export.py
  → Ziel: 02-csv\99-exports

CLE26 – CSV Import: nur properties.csv + relations.csv löschen  ★ SPEZIALFALL
  py .\CLE26-csv_no_id.py
  → Löscht gezielt: 02-csv\04-import\properties.csv
                    02-csv\04-import\relations.csv
  → elements.csv bleibt erhalten
  → Anwendungsfall: ID-lose Objekte in den Archi-OEF-XML-CSV-Archi Flow
    integrieren — nur elements.csv mit den neuen Objekten wird benötigt
  → Abgrenzung zu CLE24: CLE24 löscht ALLES in 04-import,
    CLE26 löscht nur die zwei genannten Dateien


── XLSX-GRUPPE (01-artifacts\03-XLSX) ──────────────────────────────────────────

CLE30 – XLSX Master leeren
  py .\CLE30-xlsx_master.py
  → Ziel: 03-XLSX\00-master

CLE31 – Alle XLSX Child-Ordner leeren (ArchiMate + BPMN)
  py .\CLE31-xlsx_all_childs.py
  → Ziele: 03-XLSX\03-child\00-archimatechild
           03-XLSX\03-child\01-bpmnchild

CLE32 – XLSX ArchiMate Child leeren
  py .\CLE32-xlsx_archimate_child.py
  → Ziel: 03-XLSX\03-child\00-archimatechild

CLE33 – XLSX BPMN Child leeren
  py .\CLE33-xlsx_bpmn_child.py
  → Ziel: 03-XLSX\03-child\01-bpmnchild

CLE34 – XLSX Import leeren
  py .\CLE34-xlsx_import.py
  → Ziel: 03-XLSX\04-import

CLE35 – XLSX Export leeren
  py .\CLE35-xlsx_export.py
  → Ziel: 03-XLSX\99-exports


── REPORTS-GRUPPE (01-artifacts\05-reports) ────────────────────────────────────

CLE40 – Alle Report-Ordner leeren (ArchiMate + BPMN + HTML)
  py .\CLE40-reports_all.py
  → Ziele: 05-reports\00-archimate
           05-reports\01-bpmn
           05-reports\99-html

CLE41 – Reports ArchiMate leeren
  py .\CLE41-reports_archimate.py
  → Ziel: 05-reports\00-archimate

CLE42 – Reports BPMN leeren
  py .\CLE42-reports_bpmn.py
  → Ziel: 05-reports\01-bpmn

CLE43 – Reports HTML leeren
  py .\CLE43-reports_html.py
  → Ziel: 05-reports\99-html


── STAGES-GRUPPE (02-stages) ───────────────────────────────────────────────────

CLE50 – Alle Stages-Ordner leeren (Archive + Logs)
  py .\CLE50-stages_all.py
  → Ziele: 00-archimatearchive
           01-bpmnarchive
           99-logs
  → ACHTUNG: löscht auch alle bestehenden Logs

CLE51 – ArchiMate-Archiv leeren
  py .\CLE51-stages_archimate.py
  → Ziel: 00-archimatearchive

CLE52 – BPMN-Archiv leeren
  py .\CLE52-stages_bpmn.py
  → Ziel: 01-bpmnarchive

CLE53 – Log-Ordner leeren  ★ ACHTUNG
  py .\CLE53-stages_logs.py
  → Ziel: 99-logs
  → Löscht ALLE bestehenden Logs aller Reihen (CLE, CSV, XML, ...)
  → CLE53 schreibt selbst KEIN Log (Ziel wurde gerade geleert)
  → Nur Konsolen-Ausgabe bleibt sichtbar


================================================================================
TYPISCHE ANWENDUNGSFÄLLE
================================================================================


Sauberer Start vor einem neuen ArchiMate-CSV-Run:
--------------------------------------------------------------------------------
  py .\CLE20-csv_master.py
  py .\CLE22-csv_archimate_child.py
  py .\CLE24-csv_import.py
  → Danach CSV-Flow ausführen (CSV01 ff.)


Sauberer Start vor einem neuen BPMN-Run:
--------------------------------------------------------------------------------
  py .\CLE13-xml_bpmn_child.py
  py .\CLE23-csv_bpmn_child.py
  py .\CLE33-xlsx_bpmn_child.py
  py .\CLE42-reports_bpmn.py
  py .\CLE52-stages_bpmn.py


Vollständiger Reset aller CSV-Ordner:
--------------------------------------------------------------------------------
  py .\CLE20-csv_master.py
  py .\CLE21-csv_all_childs.py
  py .\CLE24-csv_import.py
  py .\CLE25-csv_export.py


ID-lose Objekte in den Flow integrieren (Spezialfall CLE26):
--------------------------------------------------------------------------------
Szenario: elements.csv mit neuen Objekten (noch ohne Archi-ID) liegt
bereits in 02-csv\04-import. Nur properties.csv und relations.csv
sollen entfernt werden, elements.csv muss erhalten bleiben.

  py .\CLE26-csv_no_id.py
  → properties.csv + relations.csv gelöscht
  → elements.csv bleibt erhalten
  → Danach Flow für ID-losen Import ausführen

  Abgrenzung: py .\CLE24-csv_import.py würde ALLES löschen —
  auch elements.csv. In diesem Szenario daher CLE24 NICHT verwenden.


Kompletter System-Reset (Hard Clean):
--------------------------------------------------------------------------------
ACHTUNG: Löscht alle Artifacts, alle Archive, alle Logs.
Nur verwenden wenn ein vollständiger Neustart gewünscht ist.
Vorher Git-Status prüfen oder HLP06-Backup erstellen.

  py .\CLE10-xml_master.py
  py .\CLE11-xml_all_childs.py
  py .\CLE14-xml_import.py
  py .\CLE15-xml_export.py
  py .\CLE20-csv_master.py
  py .\CLE21-csv_all_childs.py
  py .\CLE24-csv_import.py
  py .\CLE25-csv_export.py
  py .\CLE30-xlsx_master.py
  py .\CLE31-xlsx_all_childs.py
  py .\CLE34-xlsx_import.py
  py .\CLE35-xlsx_export.py
  py .\CLE40-reports_all.py
  py .\CLE50-stages_all.py


Diagnose wenn Pfade nicht aufgelöst werden:
--------------------------------------------------------------------------------
  py .\CLE00-resolve_root.py
  → Zeigt welche Pfade OK sind und welche fehlen
  → Log: 02-stages\99-logs\CLE00-resolve_root.log


Log-Ordner nach längerem Betrieb aufräumen:
--------------------------------------------------------------------------------
  py .\CLE53-stages_logs.py
  → Löscht alle Logs — sauberer Zustand für neuen Run-Zyklus
  → Danach: py .\CLE00-resolve_root.py für neues Referenz-Log


================================================================================
LOG-AUSGABE VERSTEHEN
================================================================================

Standardfall Ordner-Clean — Beispiel CLE10:
  [CLE10] 2026-03-15 10:23:45 | =====  Start CLE10
  [CLE10] 2026-03-15 10:23:45 | Ziel-Ordner : C:\...\00-xml\00-master
  [CLE10] 2026-03-15 10:23:45 |   [DEL-F]  C:\...\00-master\elements.xml
  [CLE10] 2026-03-15 10:23:45 |   [DEL-D]  C:\...\00-master\temp
  [CLE10] 2026-03-15 10:23:45 | [OK]  ... bereinigt — 1 Datei(en), 1 Unterordner, 0 Fehler.
  [CLE10] 2026-03-15 10:23:45 | =====  Ende CLE10

Spezialfall Datei-Delete — Beispiel CLE26:
  [CLE26] 2026-03-15 10:30:00 | =====  Start CLE26
  [CLE26] 2026-03-15 10:30:00 | Modus: Gezieltes Datei-Löschen (kein Ordner-Clean)
  [CLE26] 2026-03-15 10:30:00 | Ziel-Datei  : C:\...\04-import\properties.csv
  [CLE26] 2026-03-15 10:30:00 |   [DEL-F]  C:\...\04-import\properties.csv
  [CLE26] 2026-03-15 10:30:00 | Ziel-Datei  : C:\...\04-import\relations.csv
  [CLE26] 2026-03-15 10:30:00 |   [DEL-F]  C:\...\04-import\relations.csv
  [CLE26] 2026-03-15 10:30:00 | [OK]  Abgeschlossen — 2 Datei(en) gelöscht, 0 nicht vorhanden.
  [CLE26] 2026-03-15 10:30:00 | =====  Ende CLE26

Ziel nicht vorhanden — [SKIP]:
  [CLE12] 2026-03-15 10:25:00 | [SKIP]  Ordner nicht gefunden: C:\...\00-archimatechild
  [CLE12] 2026-03-15 10:25:00 | [OK]  ... bereinigt — 0 Datei(en), 0 Unterordner, 0 Fehler.
  → Kein Abbruch — Script läuft durch, Ziel war einfach noch leer / nicht befüllt

Fehler beim Löschen — [FEHLER]:
  [CLE20] 2026-03-15 10:26:00 | [FEHLER]  C:\...\elements.csv — [Errno 13] Permission denied
  → Datei gesperrt (z.B. in Excel geöffnet)
  → Datei schließen, Script erneut ausführen


================================================================================
ENTSCHEIDUNGSHILFE: WELCHES CLE-SCRIPT?
================================================================================

Ich will...                                      Richtiges Script
------------------------------------------------ -------------------------------
...vor dem ArchiMate-CSV-Flow alles leeren       CLE20 + CLE22 + CLE24
...vor dem BPMN-Flow alles leeren                CLE13 + CLE23 + CLE33
...nur den XML Master leeren                     CLE10
...alle XML Child-Ordner auf einmal leeren        CLE11
...nur den BPMN XML Child leeren                 CLE13
...ID-lose Objekte importieren (elements.csv     CLE26  ← nicht CLE24!
   erhalten, nur prop+rel löschen)
...alle Reports zurücksetzen                     CLE40
...nur BPMN Reports leeren                       CLE42
...das ArchiMate-Archiv leeren                   CLE51
...alle Logs löschen                             CLE53
...prüfen ob root.cfg korrekt aufgelöst wird     CLE00


================================================================================
CLE_How2_S5 | Stage 5 | 2026-03-15 | R+MUNI Blueprint
================================================================================
