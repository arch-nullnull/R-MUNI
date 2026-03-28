================================================================================
FREEZE <N> — R+MUNI BLUEPRINT
Stage <N> – <STAGE-TITEL> — Abschluss / Startpunkt Stage <N+1>
================================================================================
Projekt             : R+MUNI Blueprint
Dokument            : FREEZE-<N>
Erstellt            : <YYYY-MM-DD>
Stage               : <N> — ABGESCHLOSSEN
Status              : FREEZE BESTÄTIGT — Stage <N> vollständig
Vorgänger           : FREEZE-<N-1> (<YYYY-MM-DD>)
Nachfolger          : FREEZE-<N+1> (Startpunkt Stage <N+1> — neues Claude-Projekt)
Erstellt durch      : EUMAXL + Claude (Pair-Session)
================================================================================


================================================================================
FREEZE-NUMMERIERUNGS-KONVENTION
================================================================================

Freeze-Nummer = Startpunkt des gleichnamigen Stage (verbindlich ab Freeze 7)
  FREEZE-<N>   = autarke Wissensbasis für Stage <N> (abgeschlossen)
  FREEZE-<N+1> = autarke Wissensbasis für Stage <N+1> (folgt)

Dieses Dokument ist die vollständige, autarke Wissensbasis für ein neues
Claude-Projekt ab Stage <N+1>. Es enthält alles was Claude benötigt um
inkrementelle Sprints in Stage <N+1> eigenständig durchzuführen — ohne
Nachladen von Scripts, Dev-Dokumentationen oder Vorgänger-Freeze-Dokumenten.

Dieses Dokument ersetzt für neue Claude-Sessions vollständig:
  - FREEZE-<N-1>.md
  - STAGE<N>_ZIELE.md
  - Alle Stage-<N>-Sprint-Dokumentationen (als Erkenntnisse eingearbeitet)

Ergänzend bereitgestellt im neuen Projekt (nicht in diesem Dokument):
  - Global_GOV.md                (normative Governance — vollständig)
  - SCRIPT-BAUKASTEN.md          (Script-Konventionen)
  - structure.txt                (aktuelle Ordnerstruktur)
  - README.md                    (Außenperspektive)
  - Install.txt                  (Stack & Setup)
  - Aktive Templates             (nach Bedarf)
  - Principles und How2 der aktiven Reihen (nach Bedarf)


================================================================================
1. SYSTEMÜBERSICHT — WAS IST R+MUNI
================================================================================

<!-- Kurzfassung — bleibt über alle Stages konsistent, nur Ergänzungen wenn nötig -->

R+MUNI ist ein Blueprint-System für Enterprise Architecture Management.
Es verbindet ArchiMate-Modellierung (Archi 5.8) mit strukturierter
Datenverarbeitung über Python-Scripts und Atlassian als optionales Kundenfrontend.

Kernprinzip: Das Archi-Modell ist die Single Source of Truth.
Alle Artefakte (CSV, XML, XLSX) werden aus dem Modell abgeleitet.
Kein manueller Eingriff in abgeleitete Artefakte — nur im Modell selbst.

R+MUNI ist dauerhaft kostenlos für Endanwender.
Claude ist ein Entwicklungswerkzeug — kein Produktbestandteil.

<ERGÄNZUNGEN STAGE <N> falls vorhanden>


================================================================================
2. STAGE-MODELL — AKTUELLER STAND
================================================================================

Stage 1  FREEZE  — <Titel> (historisch)
Stage 2  FREEZE  — <Titel> (historisch)
Stage 3  FREEZE  — Kernlogik (read-only, kein Eingriff)
Stage 4  FREEZE  — Erweiterungslogik (Bugfix nur mit expliziter Freigabe)
Stage 5  FREEZE  — <Titel> (abgeschlossen)
Stage 6  FREEZE  — <Titel> (abgeschlossen)
Stage 7  FREEZE  — <Titel> (abgeschlossen)
Stage 8  FREEZE  — <Titel> (abgeschlossen)
Stage <N> AKTIV  — [Titel wird in Stage-<N+1>-Eröffnung definiert]

<!-- Jede Stage beim Abschluss auf FREEZE setzen und Titel ergänzen -->

Rückkopplungsschutz: Stage-3- bis Stage-<N>-Scripts sind read-only.
Keine Logikänderung ohne explizite GOV-Freigabe.
Erweiterungen in Stage <N+1> sind immer additiv, nie modifizierend.


================================================================================
3. ORDNERSTRUKTUR (STAGE-5-STANDARD — FIXIERT AB FREEZE 5.5)
================================================================================

<!-- Nur ändern wenn sich die Struktur tatsächlich geändert hat -->

<rootfolder>\
  root.cfg                        Einzige Konfigurationsquelle
  .gitignore                      Blueprint-spezifisch (S8-Standard)
  README.md                       <Stand Stage <N>>
  Install.txt                     <Stand Stage <N>>
  structure.txt                   Aktuelle Ordnerauflistung (generiert)

  00-model\                       Archi-Modell (read-only für Scripts)
    00-archimate\
      00-archimateactive\         Aktives Archi-Modell (MUNI EA.archimate)
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
      04-import\
      99-exports\
    01-scripts\                   ALLE Python-Scripts
    02-csv\
      00-master\                  elements.csv, relations.csv, properties.csv
      01-mapping\
      02-sync\
      03-child\
      04-import\
      99-exports\
    03-XLSX\
    04-flow\                      FLW-Reihe + flowmapping.txt + flowtriggers.txt
    05-reports\                   Archi HTML Reports (HLP09 Server)

  02-stages\
    model-scope.txt
    run-scope.txt
    00-archimatearchive\
    01-bpmnarchive\
    02-xyarchive\
    99-logs\

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

<!-- Unveränderlich seit Freeze 5.5 — nur bei echten Änderungen anpassen -->

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

<!-- Status je Reihe aktualisieren — READ-ONLY wenn keine Änderungen in diesem Stage -->

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

Status: READ-ONLY.


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

Referenz-Flow:
  CSV00 → CSV01 → CSV03 → CSV04 → CSV05 → CSV06 →
  CSV07 → CSV08 → CSV98 → CSV99

Status: READ-ONLY.


5.3 XML-Reihe (XML00–XML07) — XML-Verarbeitung
------------------------------------------------
  XML00–XML07 vollständig implementiert.
Status: READ-ONLY.


5.4 M2B-Reihe (M2B00–M2B07) — Master to BPMN
-----------------------------------------------
  M2B00–M2B07 vollständig implementiert.
Status: READ-ONLY.


5.5 ATL-Reihe (ATL00–ATL02) — Atlassian Integration
------------------------------------------------------
  ATL00  Scope-Validierung
  ATL01  master.xml → ATL CSV
  ATL02  ATL CSV → Jira CSV (importfertig)

Jira-Import-Struktur: Komponente = ArchiMate Layer, Stichwort = Typ.
Status: READ-ONLY.


5.6 FLW-Reihe (FLW00–FLW02) — Scriptrunner / Flow-Steuerung
--------------------------------------------------------------
  FLW00  Scriptrunner (trigger- und mappinggesteuert)
  FLW01  Discover
  FLW02  Map Elements

Steuerung: flowmapping.txt + flowtriggers.txt
Status: READ-ONLY.


5.7 CLE-Reihe (CLE00–CLE53) — Cleaning Utilities
--------------------------------------------------
Schema: CLE00 Basis | CLE1x XML | CLE2x CSV | CLE3x XLSX | CLE4x Reports | CLE5x Stages
Zwei Modi: Modus A Ordner-Clean | Modus B Datei-Delete (CLE26)
WICHTIG: CLE-Scripts löschen sofort ohne Bestätigung. Kein Undo.
Status: READ-ONLY.


5.8 ECM-Reihe (ECM00–ECM03) — EasyCSVMapper
---------------------------------------------
  ECM00  Umgebungs-Validierung
  ECM01  CSV-Felder → Artefakte
  ECM02  CSV → Mapping → CSV (via OEF Mapping-Modell)
  ECM03  ID-Merge

Mapping-Modell: 99-mappingmodel\ als ArchiMate OEF XML.
Status: READ-ONLY.


<!-- Neue Reihen nach demselben Muster ergänzen -->


================================================================================
6. ATLASSIAN FRONTEND — KUNDENKONFIGURATION
================================================================================

Atlassian Free Bundle (Confluence + Jira) als optionales Kunden-Interface.
Atlassian ist ADDON — nicht Default-Setup.
IST-Situation des Kunden bestimmt ob Atlassian gebraucht wird.

Atlassian-Nutzung in Claude-Sessions: nur auf explizite Aufforderung.

Beta-Kunden Status (Stand Stage <N> Abschluss):
  <BETAKUNDE>   Status: <AKTIV / OFFBOARDED>
                <Kurzbeschreibung Stand>

<!-- Kundenstatus je Stage aktualisieren -->


================================================================================
7. GITHUB / VERSIONIERUNG
================================================================================

Zwei-Repo-Modell (ab Beta 1.0 / Stage 8):
  Public Repo (Release):  Nur saubere, freigegebene Stände. Keine DEV-Inhalte.
                          URL bleibt stabil — externe Links gültig.
                          GitHub Release: v1.0-beta (Tag) → ab Stage 8.
  DEV Repo (privat):      Vollständige History. Aktive Entwicklung.
                          Kein öffentlicher Zugang.

.gitignore: Blueprint-spezifisch (S8-Standard) — beide Repos.
GitHub Pages: aktiv (R+MUNI Doku-Portal öffentlich).

Kunden-Repo-Modell (etabliert Stage 7):
  Kunde erstellt eigenes Repo — gibt DEV Zugriff frei.
  Kein R+MUNI-seitiger Zugang zum Kundensystem erforderlich.

Grundsatz: Nur saubere, dokumentierte Zustände werden gepusht.
Keine automatischen Pushes aus Scripts.


================================================================================
8. OBSIDIAN — BLUEPRINT-NAVIGATIONSWERKZEUG
================================================================================

Obsidian ist das MD-basierte Navigationswerkzeug für den Blueprint.

Kernregeln:
  - Lesewerkzeug und Navigationshilfe — keine neue Logikschicht
  - Kein Eingriff in bestehende Dateistruktur oder Dateinamen
  - Vault liegt im Blueprint — portabel, kein Cloud-Zwang
  - .obsidian/ in .gitignore ausgeschlossen
  - SVG-Einbettung: nur externe Datei via ![[]] — kein Inline-SVG

<ERGÄNZUNGEN STAGE <N> falls vorhanden>


================================================================================
9. TOOLBAUKASTEN — TRANSPARENZ UND STRUKTUR
================================================================================

Tier-Struktur:
  MINIMAL    Pflichttools — R+MUNI läuft nicht ohne sie
  DEFAULT    Empfohlene Tools — Standard-Setup für alle Associate
  ADDON      Optionale Erweiterungen — nach Bedarf (Atlassian = ADDON)
  AGNOSTIC   Tool-unabhängige Komponenten

Kern-Stack (0 EUR):
  Archi 5.8 | Camunda Modeler | Python 3.9+ | jArchi 1.11.0 | OpenJDK 11+
  Notepad++ | Git | GitHub Desktop | Obsidian | PowerShell 7

<ÄNDERUNGEN STAGE <N> falls vorhanden>


================================================================================
10. DOKUMENTEN-TEMPLATES — BLUEPRINT STANDARD
================================================================================

Aktive Templates (Stand Stage <N>):
  Sprint-DEV-Dokumentation        Sprint-DEV-Doku_Template_S8.md
  Sprint-DEV-Backlog              Sprint-DEV-BACKLOG_Template_S8.md
  Stage-Ziele Dokument            Stage_Ziele_Template_S8.md
  GOV-Ergänzung                   GOV_Global_Template_S8.md
  Freeze-Dokument                 dieses Dokument als Referenz

  ASSOCIATE Templates:
    ASSOCIATE_principles_Template_S8.md
    ASSOCIATE_How2_Template_S8.md
    ASSOCIATE_Sprint_Template_S8.md
    ASSOCIATE_Backlog_Template_S8.md
    ASSOCIATE_Notes_Template_S8.md

Stage-Bezeichnungs-Konvention: Alle Dokumente im Beta-Zustand erhalten _S<N>.
Einheitlicher Header-Standard: verbindlich ab Stage 7 für alle Dokumente.
ASSOCIATE als Zielgruppen-Begriff: im Blueprint verankert ab Stage 7.

Dokumenttypen-Unterscheidung:
  Sprint-DEV-BACKLOG   = geplanter Sprint mit Ziel, Abgrenzung, GOV-Check
  Konzeptnotiz         = destillierte Erkenntnis, noch nicht spruchreif — kein GOV-Overhead


================================================================================
11. FEEDBACKSCHLEIFEN — KANALMODELL
================================================================================

Kernregel: "GitHub ist Quelle der Wahrheit.
            Jeder Kanal hat seine Zielgruppe.
            Jira und Confluence sind Spiegel — kein Sync-Zwang."

Kanal-Struktur:
  Interne DEV-Schleife:        Lokal first → GitHub DEV intern → Jira/Confluence
  Externe Feedback-Schleife:   GitHub Issues für externe DEV und Viewer
                               Portal für Kunden (strukturiert)
  Persönliches Feedback:       Confluence nur wenn EUMAXL triggert

Solo-DEV-Realität: EUMAXL = einziger DEV = Entscheider aller Kanäle.
Jira/Confluence-Sync: nur bei Freeze oder expliziter Anweisung.
GitHub wird primäre Kommunikationsschiene — Jira läuft aus.


================================================================================
12. ZWEI-WELTEN-ENTSCHEID — INTERN / PUBLIC
================================================================================

Normativ gültig ab Stage 7. Strukturelle Umsetzung ab Stage 1 (Produktivbetrieb).

R+MUNI trennt konsequent zwei Welten:
  INTERN (DEV-Welt):   Blueprint, GOV, Principles, Scripts, Sprint-Dokumentation.
                       Für DEV-Mitglieder und Betreiber.
                       Sprache: technisch, präzise, GOV-konform.

  PUBLIC (MGT Layout): Außenwirkung, Einstieg ohne Rulebook-Wissen.
                       Für Kunden, potenzielle Beta-Kunden, nicht-technische Leser.
                       Sprache: direkt, ergebnisorientiert, ohne Jargon.

MGT-Prinzip (Magic: The Gathering Analogie):
  Einfache erste Karten — sofort spielbar ohne Regelwerk.
  Emergent Complexity — wer tiefer will findet den Weg.

Phasen:
  Phase 1 — Beta 1.0 Paket: abgeschlossen (Stage 8).
  Phase 2 — MGT Layout bauen: Stage 1 und folgende.

Grenze: PUBLIC-Welt ersetzt nicht die INTERN-Welt — sie ergänzt sie.


================================================================================
13. BETA-ONBOARDING UND OFFBOARDING — STAND STAGE <N>
================================================================================

Offboarding:
  Principles und How2 DEV vollständig dokumentiert (BETA_OFFBOARDING_*_S<N>).
  Tier-basierte Offboarding-Logik etabliert.
  <AKTUELLER STAND>

Onboarding:
  MINIMAL-Tier als Pflicht-Einstieg.
  Erste Runde spielbar in unter 60 Minuten. Sichtbares Ergebnis.
  Atlassian ist ADDON — kein Default-Setup.
  Kunden-Repo-Modell: Kunde erstellt, gibt frei.
  Rollentrennung physisch erzwingbar (eigener Windows-User).

  Drei MGT-Setup-Varianten (Konzeptnotiz — noch nicht umgesetzt):
    Setup 1: DEV Hardcore — volle GOV, audit-fest
    Setup 2: Human Biz — seriöser Mittelweg, KMU ohne Compliance-Zwang
    Setup 3: MGT Leicht — Verein, privat, spielerisch

<ERGÄNZUNGEN / ÄNDERUNGEN STAGE <N>>


================================================================================
14. README UND ÖFFENTLICHE DOKUMENTATION
================================================================================

README.md:          <Stand Stage <N>> — Außenperspektive, Associate-Terminologie
Install.txt:        <Stand Stage <N>> — Stack & Setup, Associate-Terminologie

ASSOCIATE als Zielgruppen-Begriff (ab Stage 7):
  Externe Mitstreiter die nicht DEV sind und nicht Betakunde sind.
  Viewer, Interessenten, externe Contributor — mit eigenem Onboarding-Pfad.

Einheitlicher Header-Standard: alle neuen Dokumente ab Stage 7.

<OFFENE PUNKTE / ÄNDERUNGEN STAGE <N>>


================================================================================
15. AI-DRIVEN DEVELOPMENT METHODIK — STAND STAGE <N>
================================================================================

Methodik-Dokument: AI_DRIVEN_DEV_METHODE_S<N>.md

Kerninhalte (kumulativ — alle Stages):
  Kap. 1–8    Grundprinzip, Rahmenbedingungen, Session-Ablauf, Qualitätssicherung
  Kap. 9      Grenzen — inkl. chirurgische Eingriffe statt Neugenerierung
  Kap. 11     Rollen-Parallelbetrieb — Beta-Kanal, Transfer-Logik
  Kap. 12     Template-Methodik — Konzeptnotiz als eigenständiger Typ
  Kap. 14     Claude und externe Quellen — Fetch-Regel
  Kap. 15     Kontext-Optimierung — Mittelmaß-Prinzip, Memory/Skills
  Kap. 16     Chat-Struktur und Drift-Prävention
  Kap. 17     KI-Tool-Rollentrennung und Asset-Pipeline

Claude-Nutzung in R+MUNI (Rahmenbedingungen):
  Bereitgestellte Dokumente minimal:
    - FREEZE-<N>-Dokument (dieses Dokument)
    - Global_GOV.md
    - SCRIPT-BAUKASTEN.md
    - structure.txt
    - README.md + Install.txt
    - Principles + How2 der aktiven Reihe (nach Sprint-Bedarf)

  Nicht initial laden:
    - Einzelne Scripts (.py)
    - Dev-Dokumentationen vergangener Sprints
    - Rosetta Stone Dokumente (nur bei Onboarding neuer Personen)

<ERGÄNZUNGEN STAGE <N>>


================================================================================
16. GOVERNANCE-ECKPFEILER FÜR NEUE SPRINTS
================================================================================

Jeder Sprint in Stage <N+1> folgt diesen GOV-Regeln (Kurzform):

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
  - Stage-3 bis Stage-<N>-Scripts: read-only, kein Eingriff
  - Keine Logikänderung ohne Stage-Entscheid
  - Neue Funktionen: eigene Stages oder Spin-outs
  - Bugfixes: explizite Freigabe + Dokumentation

Rollentrennung (GOV 13):
  - R+MUNI DEV-Rolle strikt getrennt von anderen Rollen
  - ASC-Rolle strikt getrennt von DEV-Rolle
  - Externe Erkenntnisse nur mit [BetaKunde→RMUNI] Tag transferieren
  - Anonymisierungspflicht für alle externen Inhalte

Session-Regel (ab Stage 7):
  In stabilen Kontexten kann eine Session-Regel eine dokumentierte Regel
  ersetzen wenn Auslöser klar und Kontext stabil ist.
  Kein Backlog-Eintrag nötig — GOV bleibt schlank.


================================================================================
17. OFFENE PUNKTE — BEWUSST IN STAGE <N+1> VERSCHOBEN
================================================================================

<!-- Alle offenen Punkte die bewusst verschoben wurden — vollständig und ehrlich -->

<N>.1 <THEMA>
  <Beschreibung>
  <Auswirkung / Priorität>

<N>.2 <THEMA>
  <Beschreibung>
  <Auswirkung / Priorität>

<!-- Vorlage für jeden Punkt:
     - Was ist offen
     - Warum jetzt nicht
     - Priorität für nächsten Stage
     - Kein Blocker für diesen Freeze? → explizit bestätigen -->


================================================================================
18. STAGE <N> — ABSCHLUSSFESTSTELLUNG
================================================================================

Stage <N> — <STAGE-TITEL>

Zielstatus (<X> von <Y> Zielen abgeschlossen):

  ✓ S<N>-Z1  <ZIEL-TITEL>
             <Kurzbeschreibung was erreicht wurde — konkret>

  ✓ S<N>-Z2  <ZIEL-TITEL>
             <Kurzbeschreibung>

  —  S<N>-Z<X>  <ZIEL-TITEL> (OPTIONAL / VERSCHOBEN)
             <Warum nicht — bewusste Entscheidung>

<!-- Zusätzliche Erkenntnisse die nicht in den Stage-Zielen standen -->
Zusätzliche Erkenntnisse aus Stage <N>:
  ✓ <Erkenntnis>
  ✓ <Erkenntnis>

Stage-Ende Dokumentation (GOV 10.9): ERFÜLLT durch diesen Freeze.


================================================================================
19. FORMALE ABSCHLUSSFESTSTELLUNG
================================================================================

FREEZE-<N> gilt als vollständige Baseline für Stage <N+1>, da:

  ✓ Stage-<N>-Ziele dokumentiert und bewertet
  ✓ Alle abgeschlossenen Sprints in Erkenntnissen eingearbeitet
  ✓ Rückkopplungsschutz vollständig eingehalten
  ✓ Offene Punkte vollständig in Kapitel 17 dokumentiert
  ✓ GOV-Regeln für Stage <N+1> in Kapitel 16 festgehalten
  ✓ Freeze-Nummerierungs-Konvention eingehalten
  ✓ <WEITERE PUNKTE DIE FÜR DIESEN FREEZE SPEZIFISCH RELEVANT SIND>

Stage <N> ist vollständig abgeschlossen.
Stage <N+1> startet auf sauberer, konsolidierter, vollständig
dokumentierter Basis — im neuen Claude-Projekt.


================================================================================
FREEZE <N> — BESTÄTIGT | <YYYY-MM-DD>
R+MUNI Blueprint | Stage <N> ABGESCHLOSSEN | Stage <N+1> VORBEREITET
Erstellt durch: EUMAXL + Claude (Pair-Session)
================================================================================
