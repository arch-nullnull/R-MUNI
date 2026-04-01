================================================================================
FREEZE 1.01 — R+MUNI BLUEPRINT
Stage 1.01 – DEV Template Resync & GOV Konsolidierung — Abschluss / Startpunkt Stage 1.02
================================================================================
Projekt             : R+MUNI Blueprint
Dokument            : FREEZE-1.01
Erstellt            : 2026-04-01
Stage               : 1.01 — ABGESCHLOSSEN
Status              : FREEZE BESTÄTIGT — Stage 1.01 vollständig
Vorgänger           : FREEZE-8 (2026-03-28)
Nachfolger          : FREEZE-1.02 (Startpunkt Stage 1.02 — neues Claude-Projekt)
Erstellt durch      : EUMAXL + Claude (Pair-Session)
================================================================================


================================================================================
FREEZE-NUMMERIERUNGS-KONVENTION
================================================================================

Freeze-Nummer = Startpunkt des gleichnamigen Stage (verbindlich ab Freeze 7)
  FREEZE-1.01  = autarke Wissensbasis für Stage 1.01 (abgeschlossen)
  FREEZE-1.02  = autarke Wissensbasis für Stage 1.02 (folgt)

Dieses Dokument ist die vollständige, autarke Wissensbasis für ein neues
Claude-Projekt ab Stage 1.02. Es enthält alles was Claude benötigt um
inkrementelle Sprints in Stage 1.02 eigenständig durchzuführen — ohne
Nachladen von Scripts, Dev-Dokumentationen oder Vorgänger-Freeze-Dokumenten.

Dieses Dokument ersetzt für neue Claude-Sessions vollständig:
  - FREEZE-8.md
  - STAGE100_ZIELE_S100.md (als Rahmenwissen eingearbeitet)
  - Alle Stage-1.01-Sprint-Dokumentationen (als Erkenntnisse eingearbeitet)

Ergänzend bereitgestellt im neuen Projekt (nicht in diesem Dokument):
  - Global_GOV_DEV_S101.md       (normative Governance — vollständig, S101-Stand)
  - AI_DRIVEN_DEV_METHODE_DEV_S101.md  (Methodik — vollständig)
  - naming_and_structure_S101.md (Ablagestruktur und Namenskonventionen)
  - structure.txt                (aktuelle Ordnerstruktur)
  - README.md + Install.txt      (Außenperspektive — S8-Stand)
  - Principles + How2 der aktiven Reihe (nach Sprint-Bedarf)
  - FREEZE_N_Template.md         (Vorlage für Folge-Freezes)


================================================================================
1. SYSTEMÜBERSICHT — WAS IST R+MUNI
================================================================================

R+MUNI ist ein Blueprint-System für Enterprise Architecture Management.
Es verbindet ArchiMate-Modellierung (Archi 5.8) mit strukturierter
Datenverarbeitung über Python-Scripts und Atlassian als optionales
Kundenfrontend.

Kernprinzip: Das Archi-Modell ist die Single Source of Truth.
Alle Artefakte (CSV, XML, XLSX) werden aus dem Modell abgeleitet.
Kein manueller Eingriff in abgeleitete Artefakte — nur im Modell selbst.

R+MUNI ist dauerhaft kostenlos für Endanwender.
Claude ist ein Entwicklungswerkzeug — kein Produktbestandteil.
Archi hat kein Kaufmodell — R+MUNI Kunden erhalten ein Geschenk-Abo
an den Archi-Entwickler als Wertschätzung.

Geschäftsmodell: Open Core / Service around Open Source.
  Software und Dokumentation: dauerhaft kostenlos (GPL-3.0 / CC BY 4.0)
  Kommerzielles Angebot: Installation, Modellierung, Beratung

NEU Stage 1.01:
  DEV-Template-Umgebung vollständig auf S101-Standard gebracht.
  GOV um Kapitel 15 (Claude-Verhaltensregeln) und 16 (Naming Konventionen) erweitert.
  Naming-Konventionen erstmals vollständig normativ verankert.
  Lizenzierung finalisiert (GPL-3.0 + CC BY 4.0) — Sprint-DEV-S101-LIZ dokumentiert.


================================================================================
2. STAGE-MODELL — AKTUELLER STAND
================================================================================

Stage 1   FREEZE  — Proof of Concept (historisch)
Stage 2   FREEZE  — Strukturaufbau (historisch)
Stage 3   FREEZE  — Kernlogik (read-only, kein Eingriff)
Stage 4   FREEZE  — Erweiterungslogik (Bugfix nur mit expliziter Freigabe)
Stage 5   FREEZE  — Betriebsphase / Ökosystem-Enablement (abgeschlossen)
Stage 6   FREEZE  — Beta Feedback Integration & Blueprint Maturity (abgeschlossen)
Stage 7   FREEZE  — Real Beta & Ecosystem Expansion (abgeschlossen)
Stage 8   FREEZE  — Beta 1.0 | Außenwirkung & Abschluss (abgeschlossen)
Stage 1.01 FREEZE — DEV Template Resync & GOV Konsolidierung (abgeschlossen)
Stage 1.02 AKTIV  — [Titel wird bei Stage-Eröffnung definiert]

HINWEIS ZUR STAGE-ZÄHLUNG:
  Nach Stage 8 beginnt eine neue Zählung mit Stage 1.x (Produktivbetrieb).
  Stage 1.x = kein Zusammenhang mit historischem Stage 1.
  Phasenrahmen: STAGE100_ZIELE_S100 — gültig für Phase 1.00–2.00.

Rückkopplungsschutz: Stage-3- bis Stage-8-Scripts sind read-only.
Keine Logikänderung ohne explizite GOV-Freigabe.
Erweiterungen in Stage 1.02 sind immer additiv, nie modifizierend.


================================================================================
3. ORDNERSTRUKTUR (STAGE-5-STANDARD — FIXIERT AB FREEZE 5.5)
================================================================================

<rootfolder>\
  root.cfg                        Einzige Konfigurationsquelle
  .gitignore                      Blueprint-spezifisch (S8-Standard, neu gebaut)
  README.md                       S8-Stand — Associate-Terminologie, Außenperspektive
  Install.txt                     S8-Stand — Associate-Terminologie, Stack aktuell
  structure.txt                   Aktuelle Ordnerauflistung (generiert)

  00-model\                       Archi-Modell (read-only für Scripts)
    00-archimate\
      00-archimateactive\         Aktives Archi-Modell (MUNI EA.archimate)
                                  Archi schreibt log-0.txt + log-0.txt.lck
                                  direkt neben das Modell — in .gitignore erfasst
      01-archimateactivesub\      Submodelle (MUNI FLOW, MUNI IMPO)
      99-mappingmodel\            OEF Mapping-Modell (ECM-Reihe)
    01-bpmn\
    02-xyvision\

  01-artifacts\                   Alle abgeleiteten Artefakte
    00-xml\
      00-master\                  master.xml
      01-mapping\
      02-sync\
      03-child\
        00-archimatechild\
        01-bpmnchild\
        02-xychild\
      04-import\
      99-exports\
    01-scripts\                   ALLE Python-Scripts
    02-csv\
      00-master\                  elements.csv, relations.csv, properties.csv
      01-mapping\                 csvmapping.txt
      02-sync\
      03-child\
      04-import\
      99-exports\
    03-XLSX\
    04-flow\                      FLW-Reihe + flowmapping.txt + flowtriggers.txt
    05-reports\                   Archi HTML Reports (HLP09 Server)

  02-stages\
    model-scope.txt               Laufzeit — in .gitignore
    run-scope.txt                 Laufzeit — in .gitignore
    00-archimatearchive\
    01-bpmnarchive\
    02-xyarchive\
    99-logs\                      ALLE Logs — in .gitignore

  R+MUNI Doku-public\
    00-governance\
    01-principles\
    02-how2\
    03-rosetta_stone\
    04-notes\
    visuals\

  R+MUNI Doku-internal\
    backlog\
    infocfg\
    sprints\

  R+MUNI Doku-creative\           Creative Assets (eigenes Repo)


================================================================================
4. KONFIGURATION — root.cfg
================================================================================

root.cfg ist die einzige Konfigurationsquelle.
Alle Scripts lösen Pfade daraus auf — niemals hardcoded.

Aufbau root.cfg:
  rootfolder=C:\...\r-muni        Absoluter Pfad zum Projektordner
  model=00-model
  artifacts=01-artifacts
  stages=02-stages
  scripts=01-artifacts\01-scripts

HLP00_resolve_root.py — zentrale Import-Bibliothek:
  from HLP00_resolve_root import get_root_cfg
  cfg = get_root_cfg()
  basepath = cfg["artifacts"]

File-Extension-Konvention (verbindlich ab Freeze 5.5):
  .py     Python Scripts
  .cfg    Konfiguration
  .txt    Workflow-Artefakt
  .md     Dokumentation
  .log    Debug-Log (nur in 02-stages\99-logs)
  .bak    Archi-Backup (nie in GitHub)
  .ajs    jArchi Scripts
  .svg    Visuelle Artefakte (in visuals\)


================================================================================
5. SCRIPT-REIHEN — ÜBERSICHT UND STATUS
================================================================================

Alle Script-Reihen unverändert seit Stage 8 — vollständig read-only.

5.1 HLP-Reihe (HLP00–HLP10) — Hilfsfunktionen
------------------------------------------------
  HLP00  Zentrale Root-Auflösung (öffentliche Bibliothek)
  HLP01  Kopieren
  HLP02  Verschieben
  HLP03  Generischer Ordner-Clean
  HLP04  Verzeichnis-Log
  HLP05  Kontext-Struktur
  HLP06  Backup erstellen
  HLP07  Restore
  HLP08  Struktur → XML/CSV
  HLP09  Report Server (lokaler HTTP-Server für Archi HTML Reports)
  HLP10  Property Definitions bereinigen
Status: READ-ONLY. Keine Änderungen in Stage 1.01.

5.2 CSV-Reihe (CSV00–CSV09, CSV98, CSV99) — Kern-Datenverarbeitung
--------------------------------------------------------------------
  CSV00  Umgebungs-Validierung → CSV00-root.resolved.txt
  CSV01  Modell-Validierung → model-scope.txt
  CSV02  Leer (Platzhalter)
  CSV03  Run-Scope auflösen → run-scope.txt (SOURCE=archi)
  CSV04  Modell-Übersicht → run-scope.txt erweitert + gefiltert
  CSV05  Master-CSVs anlegen
  CSV06  Child → Master append
  CSV07  XLSX → Master CSV
  CSV08  Properties → CSV
  CSV09  master.xml → CSV
  CSV98  Quality Gate (Formula-Prefix FIX, Backtick→Apostroph FIX)
  CSV99  Export Snapshot → 04-import
Status: READ-ONLY. Keine Änderungen in Stage 1.01.

5.3 XML-Reihe (XML00–XML07) — XML-Verarbeitung
------------------------------------------------
  XML00–XML07 vollständig implementiert.
Status: READ-ONLY. Keine Änderungen in Stage 1.01.

5.4 M2B-Reihe (M2B00–M2B07) — Master to BPMN
-----------------------------------------------
  M2B00–M2B07 vollständig implementiert. M2B01-Fix aus Stage 5.0 aktiv.
Status: READ-ONLY. Keine Änderungen in Stage 1.01.

5.5 ATL-Reihe (ATL00–ATL02) — Atlassian Integration
------------------------------------------------------
  ATL00  Scope-Validierung
  ATL01  master.xml → ATL CSV
  ATL02  ATL CSV → Jira CSV (importfertig)
Status: READ-ONLY. Keine Änderungen in Stage 1.01.
Atlassian-Nutzung: nur auf explizite Aufforderung durch EUMAXL.

5.6 FLW-Reihe (FLW00–FLW02) — Scriptrunner / Flow-Steuerung
--------------------------------------------------------------
  FLW00  Scriptrunner (FLW00-scriptrunner.py) — trigger- und mappinggesteuert
  FLW01  Discover
  FLW02  Map Elements
Steuerung: flowmapping.txt + flowtriggers.txt
Python-Version: 3.14.2
Status: READ-ONLY. Keine Änderungen in Stage 1.01.

5.7 CLE-Reihe (CLE00–CLE53) — Cleaning Utilities
--------------------------------------------------
Schema: CLE00 Basis | CLE1x XML | CLE2x CSV | CLE3x XLSX | CLE4x Reports | CLE5x Stages
Zwei Modi: Modus A Ordner-Clean | Modus B Datei-Delete (CLE26)
WICHTIG: CLE-Scripts löschen sofort ohne Bestätigung. Kein Undo.
Status: READ-ONLY. Keine Änderungen in Stage 1.01.

5.8 ECM-Reihe (ECM00–ECM03) — EasyCSVMapper
---------------------------------------------
  ECM00  Umgebungs-Validierung
  ECM01  CSV-Felder → Artefakte
  ECM02  CSV → Mapping → CSV (via OEF Mapping-Modell)
  ECM03  ID-Merge
Mapping-Modell: 99-mappingmodel\ als ArchiMate OEF XML.
Status: READ-ONLY. Keine Änderungen in Stage 1.01.
Offener Folge-Sprint (zurückgestellt): ECM-Script-Erweiterung (CSV10+).


================================================================================
6. ATLASSIAN FRONTEND — KUNDENKONFIGURATION
================================================================================

Atlassian Free Bundle (Confluence + Jira) als optionales Kunden-Interface.
Atlassian ist ADDON — nicht Default-Setup.
IST-Situation des Kunden bestimmt ob Atlassian gebraucht wird.

Atlassian MCP in Claude: nur auf explizite Aufforderung durch EUMAXL.
GitHub wird primäre Kommunikationsschiene in Stage 1.x.
Jira: weiterhin verfügbar, aber nicht mehr primäres Tracking-Tool.

Atlassian Zugangsdaten (DEV-intern):
  cloudId     : 6975e52c-335a-4f9a-95b2-d8f8999b3210
  Jira-Projekt: MUNIEA
  Confluence Besprechungsnotizen Parent: 30441477 | Space ID: 622595

Beta-Kunden Status (Stand Stage 1.01 Abschluss):
  Betakunde_01   Status: OFFBOARDED — operativ abgeschlossen.
                 Sprint-DEV-Abschlussdoku: ausstehend → Backlog Stage 1.02.

  Betakunde_02   Status: AKTIV — vollständig ongeboardet.
  (ASC)          Surface: eigener Windows-Account (Rollentrennung GOV 13.8).
                 DEFAULT Setup vollständig, GitHub Sync aktiv, CSV00 grün.
                 Feedbackschleifen aktiv.
                 EUMAXL = Obmann = DEV in einer Person — Rollentrennung physisch.


================================================================================
7. GITHUB / VERSIONIERUNG
================================================================================

Zwei-Repo-Modell (vollständig umgesetzt Stage 8 — unverändert):
  Public Repo (Release):  Saubere, freigegebene Stände.
                          GitHub Release v1.0-beta aktiv (Tag: v1.0-beta).
                          URL bleibt stabil — externe Links gültig.
                          DEV-Inhalte: nicht enthalten.

  DEV Repo (privat):      Vollständige History. Aktive Entwicklung.
                          .gitignore: Blueprint-spezifisch S8-Standard.

History-Reset Public Repo: bewusst zurückgestellt. Kein Blocker.

GitHub Desktop: primäres GUI-Tool für Repo-Operationen.
PowerShell 7: reserviert für orphan-branch-Reset (gezielter Einsatz).
GitHub Pages: aktiv (R+MUNI Doku-Portal öffentlich).

Kunden-Repo-Modell: Kunde erstellt eigenes Repo, gibt DEV Zugriff frei.
Grundsatz: Nur saubere, dokumentierte Zustände werden gepusht.
Keine automatischen Pushes aus Scripts.

GitHub in Claude: nicht direkt zugänglich (dokumentiert AI_DRIVEN_DEV_METHODE Kap. 13).


================================================================================
8. OBSIDIAN — BLUEPRINT-NAVIGATIONSWERKZEUG
================================================================================

Obsidian ist das MD-basierte Navigationswerkzeug für den Blueprint.
Alle Dokumente sind Obsidian-kompatibel aufgebaut (double-bracket-Links).

SVG-Einbettung: ![[asset.svg]] mit Plain SVG Format (Freeze-8-Regel).
structure.txt-Scripts: arbeiten relativ zu root.cfg — kein Script-Referenzpfad.

Obsidian-Struktur: eigener Sprint (MUNIEA-152) — noch nicht umgesetzt.


================================================================================
9. TOOLSTACK — AKTUELLER STAND
================================================================================

Kernwerkzeuge:
  Archi 5.8        ArchiMate EA-Modellierung — Single Source of Truth
  jArchi           Aktiviert nur für dedizierte Archi-Sessions
  Obsidian         MD-Navigation und Dokumentenverwaltung
  Python 3.14.2    Script-Basis für alle Automatisierungen
  GitHub Desktop   Zentraler Repo-Handler (GUI)
  Notepad++        Texteditor für alle .md / .txt / .cfg Dateien
  Inkscape         SVG-Bearbeitung
  Streamlabs OBS   Video/Screen-Aufzeichnung (reaktiviert — nicht neu aufgebaut)
  VCam             Virtuelle Kamera (Lizenz aktiv)

AI-Werkzeuge:
  Claude (dieses Projekt)
               Primär für alle technischen und konzeptionellen Arbeiten.
               Atlassian MCP: nur auf explizite Aufforderung.
               Projektordner-Push: durch EUMAXL — nicht durch Claude.
  Copilot      Bewusst kontextfrei — keine R+MUNI-Dokumente.
               Visuelle Assets, Exploration, Sales-Dokumentation.
               Für Logo/Mascot-Workflow besser geeignet als ChatGPT.
               Erkenntnisse fließen als [CUSTO→RMUNI] kontrolliert zurück.

Hardware (relevant für Streamlabs):
  Zwei Logitech Webcams
  Elgato 4K Pro Capture Card (zweiter PC — Fallback)
  Physisches Flipchart

Tagging-Konvention:
  [CUSTO]        Chat-Input aus externem Kontext — nicht in R+MUNI einbauen
  [CUSTO→RMUNI]  Expliziter Transfer-Auftrag — einbauen nach Freigabe


================================================================================
10. DOKUMENTATIONS-ARCHITEKTUR — STAND STAGE 1.01
================================================================================

DEV-Dokumentumgebung vollständig wiederhergestellt und auf S101-Standard gebracht.

10.1 Normative Dokumente (DEV-intern)
---------------------------------------
  Global_GOV_DEV_S101.md              Governance — 16 Kapitel, S101-Stand
  AI_DRIVEN_DEV_METHODE_DEV_S101.md   Methodik — 17 Kapitel, S101-Stand
  naming_and_structure_S101.md        Ablagestruktur + Namenskonventionen
  STAGE100_ZIELE_S100.md              Phasenrahmen Phase 1.xx

10.2 Templates (DEV)
----------------------
  principles_Template_S101.md         Principles-Vorlage — rollenübergreifend
  how2_DEV_Template_S101.md           How2-Vorlage — DEV-spezifisch
  Sprint-DEV-Doku_Template_S8.md      Sprint-Vorlage — unverändert seit S8
  BACKLOG_Template_DEV_S101.md        Backlog-Vorlage — DEV-spezifisch
  DUMMY_Blueprint_MD_Obsidian_DEV_S101.md  Obsidian-Blueprint-Vorlage
  FREEZE_N_Template.md                Freeze-Vorlage — stage-agnostisch
  LL_Template_S101.md                 Lessons-Learned-Vorlage
  Rosetta-Stone_Template_S101.md      Rosetta-Stone-Vorlage

10.3 Beta-Kunden Prozessdokumente
------------------------------------
  BETA_OFFBOARDING_principles_DEV_S101.md
  BETA_OFFBOARDING_How2_DEV_S101.md
  BETA_OFFBOARDING_Checkliste_Template_S101.md
  BETA_ONBOARDING_Checkliste_Template_S101.md

10.4 Suffix-Logik (verbindlich)
---------------------------------
  _S101          Stage 1.01 — aktueller Standard
  _S8            Unverändert seit Stage 8 — kein Eingriff nötig
  _S7, _S6       Ältere Stände — read-only, historisch
  _DEV_          DEV-spezifisches Dokument
  kein Prefix    Rollenübergreifend

Pendant-Logik: *_ASSOCIATE_S101.md ←→ *_DEV_S101.md (gleicher Ordner, Suffix trennt)


================================================================================
11. ZWEI-WELTEN-PRINZIP — INTERN / PUBLIC
================================================================================

Normativ verankert in GOV 14. Strukturelle Umsetzung läuft ab Stage 1.x.

R+MUNI trennt konsequent:
  INTERN (DEV-Welt):   Blueprint, GOV, Principles, Scripts, Sprint-Dokumentation.
                       Für DEV-Mitglieder und Betreiber.
                       Sprache: technisch, präzise, GOV-konform.

  PUBLIC (MGT-Welt):   Außenwirkung, Einstieg ohne Rulebook-Wissen.
                       Für User, Interessenten, nicht-technische Leser.
                       Sprache: direkt, ergebnisorientiert, ohne Jargon.

MGT-Prinzip (Magic: The Gathering Analogie):
  Einfache erste Karten — sofort spielbar ohne Regelwerk.
  Emergent Complexity — wer tiefer will findet den Weg.

Phasen:
  Phase 1 — Beta 1.0 Paket: abgeschlossen (Stage 8).
  Phase 2 — MGT Layout bauen: Stage 1.x und folgende.

Grenze: PUBLIC ersetzt nicht INTERN — sie ergänzt sie.
MUNIEA-148 (strukturelle GOV-Umsetzung Zwei-Welten): separater Sprint, ausstehend.


================================================================================
12. NAMING KONVENTIONEN — STAND STAGE 1.01
================================================================================

Normativ verankert in GOV 16. Details in naming_and_structure_S101.md.

Sprachprinzip: Denglish — bewusste Entscheidung, keine Inkonsistenz.
  Englisch: Stage, Freeze, AccessLevel, Blueprint, Sprint, Associate
  Deutsch:  Betreiber, Ablage, Erweiterung, Grenzbereich

Property-Naming: CamelCase (verbindlich ab Stage 7)
  AccessLevel, SourceModel, 3PartyID (bestehend)
  Werte mit kontrolliertem Vokabular: GROSSBUCHSTABEN
  AccessLevel-Werte: INTERN · PUBLIC · GRENZBEREICH

R-MUNI vs. R+MUNI:
  R-MUNI-<Kürzel>    GitHub-Sync-Umgebung (DEV-intern)
  R+MUNI <Kürzel>    Echte Kundeninstallation (lokal)
  Vollständige Fixierung nach weiteren Beta-Durchläufen — Backlog offen.

File-Naming: vollständig in naming_and_structure_S101.md dokumentiert.


================================================================================
13. BETA-ONBOARDING UND OFFBOARDING — STAND STAGE 1.01
================================================================================

Offboarding (DEV):
  Principles, How2 und Checkliste vollständig auf S101-Standard gebracht.
  Tier-basierte Offboarding-Logik etabliert und dokumentiert.
  BKO1 Sprint-DEV-Abschlussdoku: ausstehend → Backlog Stage 1.02.

Onboarding (DEV):
  Checkliste auf S101-Standard gebracht.
  MINIMAL-Tier als Pflicht-Einstieg.
  Erste Runde spielbar in unter 60 Minuten. Sichtbares Ergebnis.
  Atlassian ist ADDON — kein Default-Setup.
  Kunden-Repo-Modell: Kunde erstellt, gibt frei.
  Rollentrennung physisch erzwingbar (eigener Windows-User).

Drei MGT-Setup-Varianten (Konzeptnotiz — noch nicht umgesetzt):
  Setup 1: DEV Hardcore — volle GOV, audit-fest
  Setup 2: Human Biz — seriöser Mittelweg, KMU ohne Compliance-Zwang
  Setup 3: MGT Leicht — Verein, privat, spielerisch


================================================================================
14. README UND ÖFFENTLICHE DOKUMENTATION
================================================================================

README.md:   S8-Stand — Außenperspektive, Associate-Terminologie, stabil
Install.txt: S8-Stand — Stack & Setup, Associate-Terminologie, stabil

ASSOCIATE als Zielgruppen-Begriff (ab Stage 7):
  Externe Mitstreiter die nicht DEV und nicht Betakunde sind.
  Viewer, Interessenten, externe Contributor — mit eigenem Onboarding-Pfad.

LinkedIn: silent beta aktiv — Logo im Profil. Post-Timing: Betreiber-Entscheidung.

Einheitlicher Header-Standard: alle Dokumente ab Stage 7.


================================================================================
15. AI-DRIVEN DEVELOPMENT METHODIK — STAND STAGE 1.01
================================================================================

Methodik-Dokument: AI_DRIVEN_DEV_METHODE_DEV_S101.md

Kerninhalte (kumulativ — alle Stages):
  Kap. 1–8    Grundprinzip, Rahmenbedingungen, Session-Ablauf, Qualitätssicherung
  Kap. 9      Grenzen — chirurgische Eingriffe statt Neugenerierung
  Kap. 10     DEV als Default-Rolle (kein expliziter Auftrag nötig)
  Kap. 11     Rollen-Parallelbetrieb — Beta-Kanal, Transfer-Logik
  Kap. 12     Template-Methodik — Konzeptnotiz als eigenständiger Typ
  Kap. 13     GitHub-Handling — Claude hat keinen direkten Repo-Zugang
  Kap. 14     Claude und externe Quellen — Fetch-Regel
  Kap. 15     Kontext-Optimierung — Mittelmaß-Prinzip, Memory/Skills
  Kap. 16     Chat-Struktur und Drift-Prävention
  Kap. 17     KI-Tool-Rollentrennung und Asset-Pipeline

Verhaltensregeln für Claude (normativ verankert in GOV 15):
  - Scope-Disziplin: kein strategisches Reinterpretieren ohne Freigabe
  - Kurze/neutrale Antworten = Zustimmung, kein Expansions-Trigger
  - Freies Denken von EUMAXL = kein impliziter Arbeitsauftrag
  - Verhaltensänderungen explizit melden — keine stille Adaptation
  - Atlassian MCP: nur auf explizite Aufforderung
  - Jira-Sync: nur auf explizite Aufforderung
  - Kein Push in Projektordner ohne explizite Bestätigung
  - Keine Jira-Issues ohne explizite Aufforderung
  - CUSTO-Tags ([CUSTO] / [CUSTO→RMUNI]) für externen Kontext-Transfer
  - DEV ist Default-Rolle — andere Rollen nur auf explizite Anforderung
  - Projektordner-Inhalt = was gepusht wurde; Rest ist für Claude nicht sichtbar

Claude-Projektsetup für Stage 1.02:
  Pflicht im Projektordner:
    - FREEZE_1.01.md              (dieses Dokument)
    - Global_GOV_DEV_S101.md
    - AI_DRIVEN_DEV_METHODE_DEV_S101.md
    - naming_and_structure_S101.md
    - structure.txt
    - README.md + Install.txt
    - FREEZE_N_Template.md
    - Principles + How2 der aktiven Reihe (nach Sprint-Bedarf)

  Nicht initial laden:
    - Einzelne Scripts (.py)
    - Dev-Dokumentationen vergangener Sprints
    - Rosetta Stone Dokumente (nur bei Onboarding)


================================================================================
16. GOVERNANCE-ECKPFEILER FÜR NEUE SPRINTS
================================================================================

Jeder Sprint in Stage 1.02 folgt diesen GOV-Regeln (Kurzform):

GOV 10.3  Zulässige Auslöser: Bugfix, Erweiterung, Kundenbedarf,
          Strukturbereinigung, Entwicklerwunsch

GOV 10.5  Fachlicher Mehrwert muss explizit benennbar sein.
          Keine implizite GOV-Änderung durch Seiteneffekte.

GOV 10.6  Ziel explizit und überprüfbar definiert bevor Umsetzung startet.

GOV 10.7  Zwischenschritte dokumentieren (reihenweise, nachvollziehbar).

GOV 10.8  Dev-Doku erstellen für jede Entwicklungsaktivität.
          Verpflichtend für Nachvollziehbarkeit — nicht auditpflichtig.

GOV 10.9  Stage-Ende Dokumentation: fällig bei Stage-Gesamtabschluss.

GOV 10.10 Keine GOV-Regel darf stillschweigend aufgehoben werden.

Rückkopplungsschutz (absolut):
  - Stage-3 bis Stage-8-Scripts: read-only, kein Eingriff
  - Keine Logikänderung ohne Stage-Entscheid
  - Neue Funktionen: eigene Stages oder Spin-outs
  - Bugfixes: explizite Freigabe + Dokumentation

Rollentrennung (GOV 13):
  - R+MUNI DEV-Rolle strikt getrennt von anderen Rollen
  - ASC-Rolle strikt getrennt von DEV-Rolle
  - Externe Erkenntnisse nur mit [CUSTO→RMUNI] Tag transferieren
  - Anonymisierungspflicht für alle externen Inhalte

Session-Regel (ab Stage 7):
  In stabilen Kontexten kann eine Session-Regel eine dokumentierte Regel
  ersetzen wenn Auslöser klar und Kontext stabil ist.
  Kein Backlog-Eintrag nötig — GOV bleibt schlank.

Phasenrahmen Stage 1.x (STAGE100_ZIELE_S100):
  - Session-basiert — kein Tagesziel, kein Abarbeitungsdruck
  - Backlog-Sprints on demand — nicht verpflichtend
  - Phase endet mit Beta 2.0 — Ziel September 2026
  - Laufende Sprints fallen bei Stage-Wechsel automatisch in Backlog zurück


================================================================================
17. OFFENE PUNKTE — BEWUSST IN STAGE 1.02 VERSCHOBEN
================================================================================

1.01.1 BKO1 Sprint-DEV-Abschlussdoku
  - Operativer Teil des Offboardings: abgeschlossen (Stage 8)
  - Sprint-DEV-Abschlussdoku: noch nicht erstellt
  - Backlog-Eintrag vorhanden: Sprint-DEV-BACKLOG_BKO1-Offboarding_S7.md
  - Priorität: mittel — kein akuter Blocker

1.01.2 R-MUNI / R+MUNI Namenskonvention vollständige Fixierung
  - Konvention beschrieben, noch nicht abschließend über alle Kontexte validiert
  - Backlog-Eintrag vorhanden: BACKLOG_Namenskonvention-GitHub-Sync_DEV_S101.md
  - Priorität: mittel — nach weiteren Beta-Kunden-Durchläufen

1.01.3 MUNIEA-148 — Zwei-Welten GOV-Umsetzung strukturell
  - GOV 14 verankert das Prinzip normativ
  - Strukturelle Umsetzung (Templates INTERN/PUBLIC kennzeichnen) ausstehend
  - Komplexitätswarnung: mindestens 2–3 fokussierte Sessions
  - Priorität: mittel — nicht dringend

1.01.4 Obsidian Struktur-Sprint (MUNIEA-152)
  - Obsidian-Struktur für DEV-interne Dokumentation noch nicht formalisiert
  - Priorität: niedrig — bei Kapazität

1.01.5 ECM-Script-Erweiterung (CSV10+)
  - SOURCE=CSV in run-scope.txt aktivieren
  - Setzt SPRINT-CSV-Refactoring als Kontext voraus
  - Priorität: mittel

1.01.6 SPRINT-CSV-Refactoring
  - CSV10+, XLSX00+, MaM00+ aufbauen
  - Priorität: mittel

1.01.7 Public Repo History-Reset (Orphan Branch)
  - Bewusst zurückgestellt bis offizieller Release
  - DEV Repo hat vollständige History als Sicherung
  - Kein Blocker

1.01.8 ELITE und MGT Templates
  - Eigener Sprint, eigene Phase — nicht forcieren
  - Priorität: niedrig

1.01.9 LinkedIn Kommunikationsstrategie
  - Silent Beta aktiv: Logo im Profil
  - Post-Zeitpunkt: Betreiber-Entscheidung — kein Druck
  - Priorität: niedrig

1.01.10 Visual Asset Pipeline (Stable Diffusion / LoRA)
  - MUNIEA-Backlog-Eintrag vorhanden
  - Priorität: niedrig — Phase 2

1.01.11 Streamlabs OBS Reaktivierung
  - Szenen, Animationen, Sounds: reaktivieren (nicht neu aufbauen)
  - Equipment vorhanden, VCam-Lizenz aktiv
  - Priorität: niedrig — bei konkretem Anlass

1.01.12 GOV-Header-Review
  - Ältere Kapitel (1–12) noch nicht auf S101-Header-Standard geprüft
  - Priorität: niedrig — bei Kapazität


================================================================================
18. STAGE 1.01 — ABSCHLUSSFESTSTELLUNG
================================================================================

Stage 1.01 — DEV Template Resync & GOV Konsolidierung

Sprint-Übersicht Stage 1.01 (alle abgeschlossen):

  ✓ Sprint-DEV-S101-DEV-TMPL-RESYNC
    DEV-Template-Umgebung vollständig wiederhergestellt.
    Alle 5 Dokumenttypen als _DEV_S101-Varianten erstellt.
    Zusätzlich: BETA_OFFBOARDING/ONBOARDING, LL, BACKLOG, DUMMY Templates.
    Lessons Learned: Entkernungslogik darf nie wieder greifen.

  ✓ Sprint-DEV-S101-Namenskonvention-GitHub-Sync
    naming_and_structure_S101.md erstellt — Ablagestruktur + Naming dokumentiert.
    Block D1 des TMPL-RESYNC-Sprints formal abgeschlossen.

  ✓ Sprint-DEV-S101-LIZ
    Lizenzierung finalisiert: GPL-3.0 (Code) + CC BY 4.0 (Dokumentation).
    AI-Training explizit erlaubt.
    Philosophie: Weiternutzung durch andere = höchste Auszeichnung.

  ✓ Sprint-DEV-S101-PublicStone-Kosten-Template
    Abgeschlossen — Inhalt in Stage 1.01 eingearbeitet.

Zusätzliche Erkenntnisse aus Stage 1.01 (nicht in Sprint-Zielen):
  ✓ GOV Kapitel 15 [NEU S101]: Claude-Verhaltensregeln normativ verankert
  ✓ GOV Kapitel 16 [NEU S101]: Naming-Konventionen (Denglish, CamelCase) normativ verankert
  ✓ Projektordner-Push-Regel etabliert: Claude sieht nur was gepusht wurde
  ✓ FREEZE_N_Template erstmals als vollständige Vorlage für alle Folge-Freezes einsatzbereit
  ✓ S8-Suffix-Semantik explizit geklärt: bedeutet "unverändert seit Stage 8" — kein Fehler
  ✓ CUSTO-Tags ersetzen MLAT-Tags systemweit

Stage-Ende Dokumentation (GOV 10.9): ERFÜLLT durch diesen Freeze.


================================================================================
19. FORMALE ABSCHLUSSFESTSTELLUNG
================================================================================

FREEZE-1.01 gilt als vollständige Baseline für Stage 1.02, da:

  ✓ Stage-1.01-Sprints dokumentiert und bewertet (alle abgeschlossen)
  ✓ Alle Erkenntnisse aus Stage 1.01 eingearbeitet
  ✓ Rückkopplungsschutz vollständig eingehalten (Stage-3 bis Stage-8 unberührt)
  ✓ DEV-Template-Umgebung vollständig und nutzbar
  ✓ GOV auf S101-Stand — Kapitel 15 und 16 neu hinzugefügt
  ✓ Naming-Konventionen normativ verankert und operativ dokumentiert
  ✓ Lizenzierung finalisiert und dokumentiert
  ✓ Offene Punkte vollständig in Kapitel 17 dokumentiert
  ✓ GOV-Regeln für Stage 1.02 in Kapitel 16 festgehalten
  ✓ Freeze-Nummerierungs-Konvention eingehalten
  ✓ ASSOCIATE-Dokumente unverändert — Rückkopplungsschutz eingehalten
  ✓ Zwei-Repo-Modell unverändert stabil
  ✓ Beta 1.0 Release (v1.0-beta) weiterhin aktiv und öffentlich

Stage 1.01 ist vollständig abgeschlossen.
Stage 1.02 startet auf sauberer, konsolidierter, vollständig
dokumentierter Basis — im neuen Claude-Projekt.

Der Esel steht. 🧱


================================================================================
FREEZE 1.01 — BESTÄTIGT | 2026-04-01
R+MUNI Blueprint | Stage 1.01 ABGESCHLOSSEN | Stage 1.02 VORBEREITET
Erstellt durch: EUMAXL + Claude (Pair-Session)
================================================================================
