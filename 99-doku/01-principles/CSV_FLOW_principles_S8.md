================================================================================
CSV FLOW – PRINCIPLES
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : CSV_FLOW_principles_S3
Tag             : #dev #principles #csvflow #s3 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-02
Rückkopplungsschutz : S3 — Inhalt read-only, kein inhaltlicher Eingriff
Ablageort       : 00-concept/01-principles/CSV_FLOW_principles_S3.txt
================================================================================


1. ZWECK UND DESIGNPHILOSOPHIE
--------------------------------------------------------------------------------
Der CSV Flow wandelt heterogene Modellquellen (ArchiMate OEF, BPMN, XLSX) in
ein einheitliches CSV-Format um, das Archi 5.8 als Import-Basis dient.

Kernprinzip: Der Flow ist eine deterministische Pipeline. Jede Stage hat genau
eine Aufgabe, einen definierten Input und einen definierten Output. Keine Stage
trifft implizite Entscheidungen – alles was passiert ist explizit konfiguriert
oder wird abgebrochen.

Der CSV Flow erzeugt KEINEN Modellinhalt. Er transportiert bestehende Inhalte
in ein importfähiges Format.


2. STUFEN-PRINZIP (STAGE-ISOLATION)
--------------------------------------------------------------------------------
Jede Stage ist autark ausführbar und hängt nur von den Artefakten der
vorherigen Stages ab – nie von globalem Zustand oder Laufzeitvariablen.

Abhängigkeitskette:
  CSV00 → CSV01 → CSV03 → CSV04 → CSV05 → CSV06 → CSV07 → CSV08 → CSV09 → CSV99

CSV02 ist bewusst leer (Platzhalter / Energiereserve).

Unterbrechungsregel: Schlägt eine Stage fehl, bricht der gesamte Flow ab.
Kein Silent-Fail, kein Weiterlaufen mit Teilresultat.


3. ROOT-AUFLÖSUNG
--------------------------------------------------------------------------------
Jede Stage löst BLUEPRINT_ROOT eigenständig über CSV00-root.resolved.txt auf.
Kein Script darf den Pfad hardcoden. Einzige erlaubte Quelle: das Artefakt.

Format root.txt:
  BLUEPRINT_ROOT=<absoluter oder relativer Pfad>

Relativer Pfad → Auflösung relativ zur Position von root.txt.
Leerer Wert oder fehlender Eintrag → Abbruch.


4. RUN-SCOPE ALS BINDENDES VERTRAGSARTEFAKT
--------------------------------------------------------------------------------
run-scope.txt ist das einzige Steuerungsdokument für den aktiven Lauf.
Alle nachgelagerten Stages lesen ausschließlich daraus.

Format eines aktiven Eintrags (beide Zeilen uncommentiert):
  SOURCE=<archi|OEF|XLSX|CSV>
  MODEL=<Dateiname>

Eine kommentierte Zeile (#) macht den Eintrag inaktiv.
SNAPSHOT_SOURCE / SNAPSHOT_MODEL sind nur Dokumentation, niemals aktiv.
CSV04 überschreibt run-scope.txt vollständig (bekanntes TD-02).


5. MASTER CSV – IDEMPOTENZ UND APPEND-ONLY
--------------------------------------------------------------------------------
CSV05: Erstellt Master CSVs nur wenn fehlend, schreibt nur Header, niemals
       überschreiben. Idempotent.

CSV06/07/08/09: Append-only. Header der Quelle wird übersprungen.
                Trailing Newline wird vor Append sichergestellt.

Der Flow leert Master CSVs nicht selbst. Sauberer Lauf = manuell geleerte
oder frische Master CSVs als Ausgangspunkt.


6. DEDUPLICATION UND EXPORT (CSV99)
--------------------------------------------------------------------------------
CSV99 ist der einzige Stage der dedupliziert. Arbeitet nur auf Master CSVs.

Last-wins: Bei gleichem Schlüssel gewinnt der zuletzt gelesene Eintrag.

Schlüssel:
  elements.csv   → ID (wenn vorhanden), sonst (Type, Name, Documentation, Specialization)
  properties.csv → (ID, Key) wenn ID vorhanden, sonst (Key, Value)
  relations.csv  → (Type, Source, Target, Specialization)

Typ-Ausschluss via csvexport.txt. 04-import/ ist Snapshot, wird überschrieben.


7. XLSX-INTEGRATION
--------------------------------------------------------------------------------
XLSX-Quellen werden über SOURCE=XLSX in run-scope.txt aktiviert.
Ohne XLSX-Eintrag: CSV07 fällt auf Discovery-Modus zurück (alle *.xlsx).

csvmapping.txt  → Spalten-Mapping für Elemente/Relationen (CSV07)
propmapping.txt → Spalten-Mapping für Properties (CSV08)

CSV08 validiert Owner-IDs gegen Master CSVs. Unbekannte ID = Abbruch.


8. NAMESPACE-AGNOSTIZITÄT
--------------------------------------------------------------------------------
Alle XML-Operationen arbeiten mit lokalen Tag-Namen (split("}")).
Kein Script verlässt sich auf eine spezifische Namespace-URI.


9. TECHNISCHE SCHULDEN – FROZEN IN S3
--------------------------------------------------------------------------------
TD-01: CSV03 Parser-Bug
  Kommentiertes SOURCE= + aktives MODEL= wird nicht korrekt als inaktiv
  erkannt. Workaround: Immer beide Zeilen gemeinsam kommentieren.

TD-02: CSV04 überschreibt run-scope.txt vollständig.
  Manuelle Einträge gehen verloren. Workaround: CSV04 deaktivieren wenn
  manuelle run-scope.txt Pflege notwendig.

TD-03: CSV09 BPMN-Scope-Filter unvollständig.
  <definitions> trägt kein sourceModel. BPMN-Quellen können nicht nach
  Modell gefiltert werden. Workaround: globale Verarbeitung.


10. GRENZEN
--------------------------------------------------------------------------------
- Kein Sync-Tool, kein bidirektionaler Abgleich
- Erzeugt keine IDs (Archi vergibt beim Import)
- Löst keine Konflikte (last-wins, keine Warnung)
- Kennt keine Modellsemantik (transportiert Zeilen)
