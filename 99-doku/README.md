# R+MUNI — Öffentliche Blueprint Dokumentation

> *Eine Vorgehensweise. Ein Werkzeugkasten. Ein Baukasten. Dokumentiert, offen, reproduzierbar.*

---

## Was ist diese Dokumentation hier?

Dieses Repository enthält die öffentliche Entwicklungsdokumentation von **R+MUNI**.  
Keine Produktseite. Kein Marketing. Eine ehrliche, nachvollziehbare Entwicklungshistorie.

Wer R+MUNI verstehen will — wie es denkt, wie es entscheidet, wie es strukturiert — ist hier richtig.

Das Haupt-Repository mit Scripts und Installationsanleitung findest du hier:  
→ [github.com/arch-nullnull/R-MUNI](https://github.com/arch-nullnull/R-MUNI)

---

## Dokumentationsstruktur — was liegt wo

R+MUNI unterscheidet drei Dokumenttypen:

| Typ | Zweck | Beispiel |
|-----|-------|---------|
| **Principles** | Wie eine Script-Reihe funktioniert — Architektur, Entscheidungen, Philosophie | `CSV_FLOW_principles_S3.md` |
| **How2** | Wie man eine Script-Reihe bedient — Schritt für Schritt | `CSV_FLOW_How2_S3.md` |
| **Sprint-Doku** | Was in einem Entwicklungs-Sprint erarbeitet wurde — Delta zum letzten Freeze | `Sprint-DEV-S7-Z3-Feedbackschleifen_S7.md` |

Dazu kommen:

| Typ | Zweck |
|-----|-------|
| **Freeze** | Eingefrorener, stabiler Stand am Ende eines Stage — autarke Wissensbasis |
| **Backlog** | Offene Punkte die noch nicht umgesetzt sind — kein direkter Eingriff in Kernlogik |
| **GOV** | Governance — Grundregeln, Freigaben, Verantwortlichkeiten |

### Was bedeutet das `_S<N>` am Dateinamen?

Alle Dokumente im Beta-Zustand tragen einen Stage-Suffix — z.B. `_S6` oder `_S7`.  
Das zeigt auf einen Blick in welchem Entwicklungsstand das Dokument entstanden ist.  
**Immer prüfen aus welchem Stage ein Dokument stammt** — gerade bei frühen Stages (S3/S4) hat sich die Ordnerstruktur noch verändert.

---

## Script-Baukasten — das Grundprinzip

R+MUNI folgt einem klaren Grundsatz:

> *1 Script = 1 Task. Kein Script macht zwei Dinge.*

Jedes Script:
- prüft seine Inputs
- führt genau eine Funktion aus
- validiert seine Outputs
- loggt sein Verhalten
- bricht bei Fehlern hart ab — kein stilles Scheitern

Scripts werden in **Reihen** organisiert. Jede Reihe hat ein Kürzel:

| Reihe | Zweck |
|-------|-------|
| **HLP** | Hilfsfunktionen — Basis für alles andere (Kopieren, Backup, Server) |
| **CSV** | Kern-Datenverarbeitung — vom Archi-Export bis zum fertigen Import-Artefakt |
| **XML** | XML-Verarbeitung und Master-XML-Pflege |
| **M2B** | Master ↔ BPMN — erstellt aus dem Modell heraus BPMN-Prozesshüllen (Trigger: Business Prozess) |
| **ATL** | Atlassian-Integration — Confluence und Jira aus dem Modell heraus |
| **CLE** | Cleaning und Quality Gate — sauber rein, sauber raus |
| **ECM** | EasyCSVMapper — externe CSV-Quellen in ArchiMate importieren |
| **FLW** | Flow-Orchestrierung — Scripts sequenziell über den Scriptrunner ausführen |

Flows verknüpfen Scripts zu deterministischen Abläufen.  
Der **FLW Scriptrunner** ist der Interpreter — er liest Flows, erkennt Trigger, führt Scripts aus.  
Keine Workflow-Engine, keine implizite Runtime — nur explizite, nachvollziehbare Abläufe.

---

## Werkzeugkasten — Tier-Struktur

R+MUNI zwingt niemanden in ein Tool-Ökosystem. Es bietet aber eines an — kostenlos als Basis:

**MINIMAL** — absolutes Kernpaket, reicht für Grundbetrieb
- Archi 5.8 (ArchiMate 3.2 Modellierung)
- Camunda Modeler (BPMN 2.0)
- Python 3 (Basis für alle Scripts)

**DEFAULT** — vollständiger Betrieb, 100% kostenlos
- Alles aus MINIMAL
- Notepad++ mit Plugins (XML, CSV, Script-Ausführung)
- Git + GitHub Desktop (Versionierung, GUI)
- Obsidian (Blueprint-Navigation)
- OpenJDK 21, PowerShell 7, draw.io, KeePass

**ADDON** — opt-in, nach Bedarf
- Atlassian Free (Jira + Confluence) — ab 10 Usern kostenpflichtig
- BOC Group (Enterprise EA/BPMN — kostenpflichtig)
- VS Code + MCP Integration (DEV only)
- O365 Ecosystem (geplant)

> Der Kern bleibt kostenlos. Das ist kein Zufall — das ist Grundsatz.

---

## Ordnerstruktur DEV

```
R+MUNI <KUERZEL>\
  root.cfg                    ← einzige Konfigurationsquelle (Pfad anpassen)
  Install.txt                 ← Installationsanleitung
  structure.txt               ← Ordnerstruktur-Referenz
  README.md

  00-model\                   ← Archi + BPMN Modelle (read-only für Scripts)
    00-archimate\
      00-archimateactive\     ← aktives Archi-Modell
      01-archimateactivesub\  ← Submodelle
      99-mappingmodel\        ← OEF Mapping-Modell (ECM-Reihe)
    01-bpmn\

  01-artifacts\               ← alle abgeleiteten Artefakte
    00-xml\                   ← XML-Verarbeitung
    01-scripts\               ← ALLE Python-Scripts (eine Ablage)
    02-csv\                   ← CSV-Artefakte (master, mapping, child, import)
    03-XLSX\                  ← XLSX-Artefakte
    04-flow\                  ← FLW-Reihe + flowmapping + flowtriggers
    05-reports\               ← Archi HTML Reports

  02-stages\                  ← Laufzeit-Artefakte und Logs
    model-scope.txt           ← Archi-Modell Scope
    run-scope.txt             ← aktiver Verarbeitungs-Scope
    99-logs\                  ← alle Logs
```

Konfiguration läuft ausschließlich über `root.cfg` — eine Datei, ein Ort, keine Ausnahmen.  
Alle Scripts lösen Pfade daraus auf. Nie hardcoded.

---

## Mitmachen

**Als Beta-Kunde** — R+MUNI in deiner Organisation einsetzen und Feedback geben:  
→ [Ticketsystem / Helpcenter](https://ims-blueprint-ticketsystem.atlassian.net/helpcenter/RMNP/)

**Als Developer** — auf der Blueprint-Basis aufbauen.  
Die Dokumentation ist offen, jede Entscheidung hat einen dokumentierten Grund.  
Backlog-Inhalte und interne Sprint-Dokus sind auf Anfrage zugänglich — meld dich über GitHub Issues.

**R+MUNI ist AI-driven entwickelt** — der gesamte Entwicklungsprozess mit Claude als Pair-Partner ist dokumentiert und reproduzierbar. Das ist kein Marketingbegriff, das ist Methodik.

---

## Aktueller Stand

R+MUNI befindet sich in **Stage 7 — Real Beta & Ecosystem Expansion**.  
Aktive Beta-Kunden laufen produktiv. Das System funktioniert — mit echten Ecken und Kanten.

> Wer jetzt einsteigt, begleitet die Entwicklung aktiv. Das ist kein Nachteil — das ist der Punkt.

---

*R+MUNI Blueprint — entwickelt von EUMAXL | Stage 7 aktiv | 2026*  
*Fragen, Feedback, Interesse → [GitHub Issues](https://github.com/arch-nullnull/R-MUNI/issues) oder [Ticketsystem](https://ims-blueprint-ticketsystem.atlassian.net/helpcenter/RMNP/)*
