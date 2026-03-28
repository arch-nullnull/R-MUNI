================================================================================
INST – INSTALLATION & WERKZEUGKASTEN – PRINCIPLES
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : INST_principles_S5
Tag             : #dev #principles #inst #installation #s5 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-17
Ablageort       : R+MUNI Doku-public\01-principles\INST_principles_S5.md
================================================================================


1. ZWECK UND DESIGNPHILOSOPHIE
--------------------------------------------------------------------------------
R+MUNI ist kein monolithisches Setup. Es ist ein Werkzeugkasten mit einem
stabilen Kern und klar definierten, optionalen Erweiterungen.

Kernprinzip: Jedes Tool, jede Funktion und jede Integration hat genau einen
definierten Platz — entweder im Core (Stamm) oder als Option (Ast).
Nichts ist implizit. Nichts ist versteckt. Was nicht gebraucht wird, wird
nicht installiert.

Dieses Prinzip gilt für Entwickler und Endkunden gleichermassen — mit
unterschiedlichen Ausprägungen aber derselben Grundlogik.


2. DAS BAUM-MODELL
--------------------------------------------------------------------------------
R+MUNI denkt Installation wie einen Baum:

  STAMM
    Der absolute Kern. Läuft bei jedem User, in jeder Umgebung.
    Kein Opt-out. Ohne Stamm kein R+MUNI.

  TRAGENDE ÄSTE (Core einer Achse)
    Pro Funktionsachse gibt es genau einen tragenden Ast.
    Dieser muss gewählt werden — aber die Wahl ist kontextabhängig.
    Beispiel Dokumentation: entweder MD+GitHub oder Confluence — nicht beide.

  WEITERE ÄSTE (Addons)
    Optionale Erweiterungen die additiv wirken.
    Sie heben den tragenden Ast nicht auf — sie ergänzen ihn.
    Beispiel Backup: GitHub private ist Core, lokaler Sync ist Addon.

  ÄSTE DIE IN DEN BODEN GEHEN (Exitpoints)
    Integrationen die eigenständig werden können.
    Der Mutterbaum (R+MUNI) darf danach wegfallen ohne den Exitpoint
    zu beschädigen. Die Methode und die Artefakte bleiben erhalten.
    Beispiel: BOC Group ADOIT — ArchiMate-Modell wandert via OEF,
    R+MUNI wird nicht mehr benötigt.

Exitpoints sind keine Gefahr — sie sind das Ziel.
R+MUNI baut keine Abhängigkeit, es baut Kompetenz.


3. ACHSEN
--------------------------------------------------------------------------------
Eine Achse ist eine Funktionsdimension in der eine Entscheidung getroffen
werden muss. Jede Achse hat:
  - einen tragenden Ast (Core der Achse — Pflicht, wähle genau einen)
  - optionale Addons (ergänzend, kombinierbar)
  - optional einen Exitpoint (ablösend, eigenständig werdend)

Achsen sind unabhängig voneinander. Die Wahl auf einer Achse beeinflusst
nicht die Wahl auf einer anderen.

Achsen werden in Sprint INST01 vollständig definiert — mit tragenden Ästen,
Addons und Exitpoints pro Funktionsdimension.

Bekannte Funktionsdimensionen (noch nicht fixiert):
  Dokumentation, Backup/Sync

Weitere Achsen entstehen aus dem Livebetrieb. Keine Achse wird auf Vorrat
gebaut.


4. CORE vs. ADDON — ABGRENZUNGSREGELN
--------------------------------------------------------------------------------
Ein Tool oder eine Funktion gehört in den CORE wenn:
  - R+MUNI ohne es nicht lauffähig ist, ODER
  - jeder User es in jeder Umgebung benötigt, ODER
  - es Voraussetzung für mindestens einen tragenden Ast ist

Ein Tool oder eine Funktion ist ein ADDON wenn:
  - es eine bestehende Funktion erweitert aber nicht ersetzt, ODER
  - es nur in bestimmten Umgebungen oder Usecases relevant ist, ODER
  - es durch eine Alternative auf derselben Achse ersetzt werden kann

Ein Tool ist kein Bestandteil des Werkzeugkastens wenn:
  - es keinen nachweisbaren Bezug zu einer R+MUNI Funktion hat, ODER
  - es bereits als Funktion eines anderen installierten Tools enthalten ist
    (Beispiel: Plugin bereits im App-Menü enthalten — kein separater Download)


5. ENTWICKLER vs. ENDKUNDE
--------------------------------------------------------------------------------
Der Stamm ist für beide identisch.
Die Achsen-Entscheide fallen unterschiedlich aus.

Entwickler (R+MUNI Betreiber):
  - Vollständiges GitHub Setup (public + private Repos)
  - Erweiterte Tool-Palette (Git CLI, GitHub Desktop, Obsidian, etc.)
  - Alle Achsen bewusst konfiguriert
  - Eigene GOV-Dokumentation im Blueprint

Endkunde:
  - Stamm identisch
  - GitHub typischerweise nicht erforderlich (kein Developer-Usecase)
  - Dokumentations-Achse: Confluence bevorzugt (Atlassian bereits vorhanden)
  - Backup-Achse: je nach Unternehmensstandard
  - Öffentlicher GitHub-Bereich: nur wenn explizit benötigt,
    dann als eigenständiges unabhängiges Repo — nicht Teil der R+MUNI Struktur

Die Install.txt unterscheidet diese zwei Spuren explizit.
Kein User soll Tools installieren die für seinen Usecase nicht relevant sind.


6. GIT vs. GITHUB — BEGRIFFSKLARHEIT
--------------------------------------------------------------------------------
Diese zwei Begriffe werden im Blueprint strikt getrennt:

  Git       = lokales Versionskontroll-Tool (Kommandozeilen-App)
              Installiert als App unter R+MUNI Apps\Git\
              Bringt Git Bash mit — eine Unix-Shell auf Windows
              Zweck in R+MUNI:
                1. Technische Basis für GitHub Desktop
                2. Voraussetzung für VS Code + Claude MCP Integration
                3. Git Bash als Shell-Erweiterung zu PowerShell

  GitHub    = Cloud-Dienst für Repository-Hosting und Sync
              Kein lokales Tool — ein Service

  GitHub Desktop = GUI-Client für GitHub Sync
                   Benötigt Git als technischen Unterbau
                   Ersetzt Git CLI für alle Standard-Operationen

Konsequenz: Wer weder GitHub noch VS Code + Claude MCP Integration nutzt,
benötigt Git nicht. Git ist kein eigenständiger Core-Baustein.


7. EXITPOINT-PRINZIP
--------------------------------------------------------------------------------
Jeder Exitpoint folgt denselben Regeln:

  - Der Exitpoint ist normkonform vorbereitet (ArchiMate 3.2, BPMN 2.0)
  - Keine R+MUNI-spezifischen Erweiterungen im Modell die den Export blockieren
  - Der Kunde behält alle Artefakte und die gesamte Methode
  - R+MUNI ist nach dem Exitpoint nicht mehr erforderlich — das ist kein
    Verlust sondern der Beweis dass die Methode funktioniert

Bekannte Exitpoints in Stage 5:
  BOC Group ADOIT   ArchiMate OEF Import (empirisch validiert 2026-03-07)
  Camunda 8         BPMN 2.0 normkonform, keine tool-eigenen Extensions
  Confluence/Jira   Inhalte und Strukturen bleiben beim Kunden


8. ABGRENZUNG ZU SPÄTEREN STAGES
--------------------------------------------------------------------------------
Nicht Teil dieser Principles:
  - Vollständige Achsen-Matrix mit allen möglichen Kombinationen
  - Automatisierter Installer oder Packaging-Lösung
  - Kunden-spezifische Werkzeugkasten-Konfiguration als eigenes Artefakt

Diese Themen entstehen aus dem Livebetrieb — sie werden nicht auf Vorrat
definiert. Stage 5 fixiert das Denkmuster, nicht die vollständige Ausprägung.


================================================================================
INST – INSTALLATION & WERKZEUGKASTEN – PRINCIPLES
Stage 5 | Erstellt: 2026-03-17
R+MUNI Blueprint | Erstellt durch: Markus Resel + Claude (Pair-Session)
================================================================================
