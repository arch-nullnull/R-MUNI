================================================================================
SCRIPT-BAUKASTEN
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : SCRIPT-BAUKASTEN
Tag             : #dev #scriptbaukasten #flows #rmuni
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
================================================================================

## Ziel

Der Script-Baukasten beschreibt das Ausführungsmodell für technische Flows.
Ein Flow ist ein deklarativ beschriebenes Ablaufmodell, das durch einen Interpreter deterministisch ausgeführt wird.

Der Fokus liegt auf:
- expliziten Aufgaben
- kleinen, isolierten Scripts
- vollständiger Transparenz
- einfacher Debugbarkeit

Es gibt keine Workflow-Engine, keine Worker und keine implizite Runtime-Semantik.

---

## Grundprinzip

Ein Flow beschreibt *was* passiert.
Scripts implementieren *wie* es passiert.

Die Ausführung erfolgt als Atomic Run:
- ein Start
- ein vollständiger Ablauf
- ein Ergebnis oder ein Fehler

Nicht alle modellierten Elemente sind ausführbar.
Nur explizit adressierte Elemente werden interpretiert.

---

## Script-Philosophie

Jedes Script erfüllt genau eine Aufgabe.

Regeln:
- 1 Script = 1 Task
- keine versteckten Seiteneffekte
- keine impliziten Abhängigkeiten
- keine globale Zustandslogik

Ein Script:
- prüft seine erwarteten Inputs
- führt eine klar abgegrenzte Funktion aus
- validiert seine Outputs
- loggt sein Verhalten
- bricht bei Fehlern hart ab

---

## Vertrag zwischen Flow und Script

Der Vertrag ist explizit und minimal.

Ein Script:
- liest nur deklarierte Inputs
- schreibt nur deklarierte Outputs
- kennt keine anderen Flow-Elemente

Der Interpreter:
- übergibt nur erlaubte Inputs
- akzeptiert nur erlaubte Outputs
- beendet den Flow bei Vertragsverletzungen

---

## Ausführungsmodell

Die Ausführung erfolgt synchron und deterministisch.

Eigenschaften:
- keine Parallelität
- kein Resume
- kein Retry
- kein versteckter Zustand

Fehler führen zum sofortigen Abbruch des Flows.
Der vollständige Kontext ist zur Laufzeit sichtbar.

---

## Trigger-Prinzip

Ein Flow reagiert ausschließlich auf explizite Trigger.

Trigger sind opt-in:
- ein Element ist nur dann ausführbar, wenn es explizit als Trigger markiert ist
- fehlende oder negative Trigger-Informationen sind kein Fehler

Nicht-Trigger sind der Normalfall. Sie beeinflussen die Ausführung nicht.

---

## Modellnutzung

Das Flow-Modell dient als:
- Ablaufbeschreibung
- Dokumentation
- Konsistenzprüfung
- deklaratives Runbook

Modelle können visuelle, fachliche oder technische Elemente enthalten.
Nur explizit getriggerte Elemente werden interpretiert.

Nicht adressierte Elemente sind inert:
- sie beeinflussen die Ausführung nicht
- sie dienen ausschließlich der Verständlichkeit

---

## Interpreter (FLOW)

FLOW ist der Interpreter des Script-Baukastens.

FLOW:
- liest Modelle, interpretiert sie aber nicht
- erkennt ausschließlich explizite Trigger
- ordnet Trigger über eine Mapping-Datei Scripts zu
- führt Scripts deterministisch aus

FLOW kennt:
- keine Engine-Semantik
- keine Prozesslogik
- keine impliziten Abhängigkeiten

---

## Naming-Konvention

Schema: `<KÜRZEL><Nr>-<funktionsbeschreibung>.<extension>`

| Kürzel | Bedeutung | Beispiel |
|--------|-----------|---------|
| `CSV` | CSV Flow — Archi CSV Import/Export | `CSV06-append_child_to_master.py` |
| `XML` | XML Flow — Master XML Aufbau | `XML04-merge_master.py` |
| `M2B` | Master to Blueprint Flow | `M2B01-master_extract.py` |
| `ATL` | Atlassian Flow — Jira/Confluence | `ATL01-masterXml2AtlCsv.py` |
| `HLP` | Helper Scripts — wiederverwendbar | `HLP00_resolve_root.py` |
| `FLW` | Flow Scriptrunner | `FLW00-scriptrunner.py` |

Regeln:
- Leerzeichen immer durch Unterstrich `_` ersetzen
- Nummer ist fortlaufend pro Kürzel-Serie
- Historische Files nicht umbenennen — neue Files konsequent nach Schema
- Sondernummern haben fixe Bedeutung (siehe unten)

### Sondernummern pro Serie

| Nummer | Bedeutung |
|--------|-----------|
| `00` | Root-Auflösung / Umgebungsvalidierung |
| `98` | Cleaner / Quality Gate (vor Export) |
| `99` | Export / Snapshot |

---

## File-Extension Konvention

| Extension | Zweck | Beispiel |
|-----------|-------|---------|
| `.py` | Python Script | `CSV06-append_child_to_master.py` |
| `.log` | Technisches Debug-Log — maschinell, nur bei Problemen relevant | `CSV01-validate_model.log` |
| `.txt` | Workflow-Artefakt — wird von Scripts gelesen oder vom User manuell geprüft im Workflow | `run-scope.txt`, `model-scope.txt`, `CSV00-root.resolved.txt` |
| `.cfg` | Konfiguration — einmalig vom User gesetzt, selten geändert | `root.cfg` |
| `.md` | Dokumentation — für Menschen lesbar, strukturiert | Sprint-Dokus, GOV, Baukasten |
| `.csv` | Tabellarische Daten — Archi Import/Export Format | `elements.csv` |
| `.xml` | Strukturierte Daten — Master XML, OEF Export | `master.xml` |
| `.xlsx` | Excel — Archi XLSX Export | `MUNI EA.xlsx` |
| `.archimate` | Archi Modell-Datei | `MUNI EA.archimate` |
| `.bpmn` | BPMN Prozessmodell | `MUNI FLOW.bpmn` |

### Wichtige Abgrenzungen

- `.log` ist NICHT für den Workflow gedacht — nur Debug bei Problemen
- `.txt` ist für Artefakte die im Workflow gelesen werden — bewusst menschenlesbar
- `.cfg` ist keine `.txt` — signalisiert einmalige Konfiguration durch den User
- Archi-interne Dateien (`.bak`, `.lck`, `log-0.txt`) werden von Scripts aktiv ignoriert

---

## Logging & Debugging

Debugging findet dort statt, wo die Logik liegt: im Script.

Jedes Script:
- loggt Start, relevante Schritte und Ergebnis in eine `.log` Datei
- gibt Fehler klar und nachvollziehbar aus
- verlässt sich auf die Konsole als primäre Diagnosequelle
- schreibt Logs ausschließlich nach `<stages>\99-logs\`

Log-Dateiname: `<KÜRZEL><Nr>-<beschreibung>.log`
Beispiel: `CSV06-append.log`, `XML04-merge.log`

Es gibt keine Engine-Logs, keine verteilten Zustände
und keine nachträgliche Rekonstruktion.

---

## Konfiguration & Root-Auflösung

### root.cfg

Die einzige vom User zu pflegende Konfigurationsdatei.
Liegt im Blueprint-Root-Ordner (`<rootfolder>\root.cfg`).

```
<rootfolder>=C:\Prototyping\R+MUNI
<models>=<rootfolder>\00-model
<artifacts>=<rootfolder>\01-artifacts
<stages>=<rootfolder>\02-stages
<apps>=C:\Prototyping\R+MUNI Apps
<doku>=C:\Prototyping\R+MUNI Doku\R+MUNI Doku-internal
<dokupublic>=C:\Prototyping\R+MUNI Doku\R+MUNI Doku-public
<creative>=C:\Prototyping\R+MUNI Doku\R+MUNI Doku-creative
```

Einziger User-Eingriff: `<rootfolder>` anpassen. Alle anderen Pfade leiten sich ab.

### HLP00 als zentraler cfg-Parser

`HLP00_resolve_root.py` ist die zentrale Bibliothek für Root-Auflösung.

```python
from HLP00_resolve_root import get_root_cfg
cfg = get_root_cfg()

root_path     = cfg["<rootfolder>"]
stages_dir    = cfg["<stages>"]
artifacts_dir = cfg["<artifacts>"]
models_dir    = cfg["<models>"]
```

Alle `*00` Scripts (CSV00, XML00, M2B00, ATL00) verwenden HLP00 direkt.
Nachfolgende Scripts lesen die `CSV00-root.resolved.txt` als Artefakt-Kette.
Vollständiger Umbau aller Scripts auf direkten HLP00-Import: nächster Cleaning Run.

---

## Ordnerstruktur (Stage 5)

```
<rootfolder>\
  root.cfg                        ← einzige User-Konfiguration
  00-model\                       ← Archi Modelle
  01-artifacts\                   ← alle Artefakte
    00-xml\                       ← XML Flow
    01-scripts\                   ← alle Scripts
    02-csv\                       ← CSV Flow
    03-XLSX\                      ← XLSX Flow
    05-reports\                   ← HLP09 Reports
  02-stages\                      ← Laufzeit-Artefakte
    run-scope.txt                 ← aktiver Run-Scope (Workflow-Artefakt)
    model-scope.txt               ← Modell-Inventar (Workflow-Artefakt)
    99-logs\                      ← alle Debug-Logs
```

Ordner werden NICHT von Scripts angelegt — Struktur ist fix.
Referenz: `structure.txt` (vom User gepflegt, einzige Quelle der Wahrheit).

---

## Extension-Filter Konvention

Scripts die Ordner scannen filtern aktiv nach erlaubten Extensions.
Archi-interne Dateien werden nie in Workflow-Artefakte übernommen.

| Source-Typ | Erlaubte Extension | Ignoriert |
|---|---|---|
| `SOURCE=archi` | `.archimate` | `.bak`, `log-0.txt`, `.lck` |
| `SOURCE=OEF` | `.xml` | `.xsd` Schema-Dateien |
| `SOURCE=XLSX` | `.xlsx` | alle anderen |
| `SOURCE=CSV` | `.csv` | alle anderen |
| `SOURCE=BPMN` | `.bpmn` | alle anderen |

---

## Abgrenzung

Dieses Konzept ist bewusst kein Workflow-System.

Es ersetzt:
- keine Event-Engine
- kein Scheduling
- keine verteilte Orchestrierung

Es ist ein:
- deklaratives Runbook
- technischer Baukasten
- kontrollierter Ausführungsrahmen

---

## Leitgedanke

Ein Flow soll verständlich sein, bevor er ausgeführt wird.
Ein Script soll verständlich sein, während es läuft.

Komplexität wird nicht abstrahiert, sondern bewusst vermieden.

---

*SCRIPT-BAUKASTEN | Stage 5 | Stand: 2026-03-13*
