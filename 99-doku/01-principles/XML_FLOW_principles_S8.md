================================================================================
XML FLOW – PRINCIPLES
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : XML_FLOW_principles_S3
Tag             : #dev #principles #xmlflow #s3 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-02
Rückkopplungsschutz : S3 — Inhalt read-only, kein inhaltlicher Eingriff
Ablageort       : 00-concept/01-principles/XML_FLOW_principles_S3.txt
================================================================================


1. ZWECK UND DESIGNPHILOSOPHIE
--------------------------------------------------------------------------------
Der XML Flow aggregiert heterogene Modellquellen (ArchiMate OEF + Camunda BPMN)
in ein stabiles master.xml. Dieses Dokument ist das zentrale Identitäts-
Fundament des gesamten Blueprints.

Kernprinzip: master.xml ist kein Arbeitsdokument – es ist ein Aggregat.
Niemand editiert master.xml direkt. Es entsteht ausschließlich durch den Flow.

Jede Stage hat eine klar abgegrenzte Verantwortung. Der Flow ist sequenziell
und deterministisch. Gleiches Input-Set → gleiches master.xml.


2. STUFEN-PRINZIP (STAGE-ISOLATION)
--------------------------------------------------------------------------------
Abhängigkeitskette:
  XML00 → XML01 → XML02 → XML03 → XML04 → XML05 → XML06 → XML07

Zwischenartefakte (XML01-sources.resolved.txt, XML02-parsed.txt,
XML03-index.xml, master.generated.xml, master.cleared.xml) sind temporär.
XML07 räumt sie auf. Nur master.xml und die XML06/XML07 Logs bleiben.

Unterbrechungsregel: Fehler = Abbruch. Kein partielles master.xml.


3. ROOT-AUFLÖSUNG
--------------------------------------------------------------------------------
XML00 ist die einzige Quelle der Wahrheit für BLUEPRINT_ROOT im XML Flow.
Ergebnis: 03-stages/99-logs/XML00-root.resolved.txt

Alle nachgelagerten Stages lesen ausschließlich dieses Artefakt.
XML05 und XML06 verwenden einen eigenen resolve_root()-Walker (sucht root.txt
aufwärts im Verzeichnisbaum) – das ist konsistent, da sie im selben
Blueprint-Verzeichnisbaum liegen.


4. QUELLEN-DEKLARATION VIA child_mapping.txt
--------------------------------------------------------------------------------
Welche Verzeichnisse als Quellen dienen, ist ausschließlich in
02-artifacts/00-xml/child_mapping.txt deklariert.

Format:
  <source_type>-<relativer Pfad zum Quellverzeichnis>

Beispiel:
  archi-02-artifacts/00-xml/03-child/00-archimatechild
  bpmn-02-artifacts/00-xml/03-child/01-bpmnchild

Kein Script sucht selbstständig nach Quelldateien. Nur deklarierte Quellen
werden verarbeitet. Unbekannte Erweiterungen werden ignoriert.

Dateifilter nach source_type:
  archi → .xml Dateien
  bpmn  → .bpmn Dateien


5. INDEX-PRINZIP (XML03)
--------------------------------------------------------------------------------
XML03 erstellt einen schlanken Index aller Objekte pro Modell – kein
Content-Duplikat, nur Referenzen mit Core-Attributen (id, kind, xsi_type,
name).

Der Index ist die Entscheidungsgrundlage für XML04. Nur was im Index steht
kann gemapped werden. Das Original-XML wird erst beim Merge (XML04) geladen.

Archi-Indexierung: identifier-basiert, xsi:type wird ausgelesen
BPMN-Indexierung:  id-basiert, Tag-Lokalname wird als kind gespeichert


6. MAPPING-PRINZIP (XML04)
--------------------------------------------------------------------------------
mapping.txt ist der einzige Ort wo entschieden wird, welche Objekte ins
master.xml wandern. Es gibt keine impliziten Regeln, keine Defaults.

Syntax:
  <source>[<model-filter>]-<entry-point>+<filter>+<filter>

Trennzeichen:
  - (nach source/model-filter) → trennt vom entry-point
  + (nach entry-point)         → hängt Attributfilter an (AND-verknüpft)

Wichtig: entry-point darf intern : enthalten (z.B. bpmn:serviceTask).
Der - als Trennzeichen gilt nur nach dem optionalen [...] Block.

Regel: IDs werden NIEMALS modifiziert. XML04 annotiert nur sourceSystem
und sourceModel auf dem kopierten Subtree.

Deduplication im Index: Überlappende Regeln die dasselbe Objekt aus
demselben Modell matchen → wird nur einmal eingefügt (by model_file + entry_id).


7. KONSOLIDIERUNG (XML05)
--------------------------------------------------------------------------------
XML05 verwendet lxml (nicht stdlib ET) – das ist die einzige Stelle im
gesamten Blueprint die lxml erfordert.

sync.txt steuert die Konsolidierungslogik:
  Format: <selector>::<action>
  Actions: merge | keep | ignore

merge: Ein Element ohne identifier aber mit id wird in das kanonische
       Element mit identifier gemergt (Duplikat wird entfernt).
       Bedingung: genau 1 Kandidat mit identifier für diese id.
       Bei 0 oder >1 Kandidaten: AMBIGUOUS, kein merge.

Selector-Matching arbeitet mit lokalen Tag-Namen (strip_ns).
Source-Checks via sourceSystem-Attribut ODER typische lokale Tag-Namen.


8. FINALISIERUNG UND CLEANUP (XML06/XML07)
--------------------------------------------------------------------------------
XML06: Kopiert master.cleared.xml → master.xml. Keine Transformation.
       master.xml ist ab diesem Moment die stabile Referenz.

XML07: Entfernt alle Zwischenartefakte mit Prefix XML00- bis XML05-.
       Entfernt entsprechende Logs.
       Behält: master.xml, XML06-finalize-master.log, XML07-cleanup-artifacts.log

Nach XML07 ist der Flow-Zustand sauber. master.xml ist die einzige Spur.


9. NAMESPACE-AGNOSTIZITÄT
--------------------------------------------------------------------------------
XML00–XML04: stdlib ET, lokale Namen via tag.split("}")[-1]
XML05: lxml, lokale Namen via strip_ns() Hilfsfunktion
Beide Ansätze sind äquivalent in der Wirkung.

Kein Script verlässt sich auf Namespace-URIs oder Präfixe.


10. GRENZEN DES XML FLOWS
--------------------------------------------------------------------------------
- Erzeugt kein neues Modellwissen – aggregiert nur was vorhanden ist
- Löst keine semantischen Konflikte zwischen Archi und BPMN
- Versteht keine ArchiMate oder BPMN Semantik
- master.xml ist kein valides OEF-Dokument – es ist ein Blueprint-internes
  Aggregatformat das OEF als strukturelles Vorbild verwendet
- XML05 merge gilt nur für id/identifier Duplikate – inhaltliche
  Duplikate (gleicher Name, andere ID) werden nicht erkannt
