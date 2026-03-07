================================================================================
M2B FLOW – PRINCIPLES
Stage 3 | Frozen | R+MUNI Blueprint
================================================================================
Erstellt    : 2026-03-02
Stage       : S3 – FROZEN (read-only Referenz)
Ablageort   : 00-concept/01-principles/M2B_FLOW_principles_S3.txt
================================================================================


1. ZWECK UND DESIGNPHILOSOPHIE
--------------------------------------------------------------------------------
Der M2B Flow (Master-to-BPMN) verbindet die ArchiMate-Welt mit der
BPMN-Welt. Er extrahiert BusinessProcess-Elemente aus master.xml, erzeugt
BPMN-Hüllen für Camunda, ermöglicht die Anreicherung in Camunda Modeler
und schreibt das Ergebnis zurück in master.xml.

Kernprinzip: Archi ist immer der Ursprung der Identität. BPMN ist die
Ausdrucksform der Prozessdetails. M2B ist die Brücke – in beide Richtungen.

master.xml ist sowohl Input als auch Output des M2B Flows.


2. RICHTUNGSUMKEHR – DER KREISLAUF
--------------------------------------------------------------------------------
M2B ist bidirektional aufgebaut:

  Hinweg  (M2B01/02): master.xml → BPMN Hüllen → active BPMN Verzeichnis
  Rückweg (M2B04/05): active BPMN (angereichert) → master.xml

Der Kreislauf lautet:
  Archi (master.xml) → BPMN Hull → Camunda Anreicherung → master.xml update

Jeder Zyklus kann wiederholt werden. M2B01 erstellt niemals eine BPMN-Datei
die bereits existiert (no-overwrite). M2B05 überschreibt bestehende
Definitionen im master.xml (bpmn wins).


3. ROOT-AUFLÖSUNG (AUTONOM)
--------------------------------------------------------------------------------
M2B00 ist vollständig autonom. Er versucht zuerst XML00-root.resolved.txt
wiederzuverwenden (Fast-Path). Fehlt dieses Artefakt, löst er selbst via
root.txt auf (Fallback).

Wichtig: M2B00 schreibt NUR M2B00-root.resolved.txt. Er beschreibt nie
das XML00-Artefakt. Die Flows sind in der Root-Auflösung unabhängig.


4. HARD FILTER VIA M2Bmapping.txt
--------------------------------------------------------------------------------
M2Bmapping.txt ist der einzige Steuerungspunkt dafür, welche Elemente
aus master.xml als BPMN extrahiert werden.

Format:
  archi[model=<pattern>]-element-xsi:type="<Typ>"

Beispiel:
  archi[model=*Process*]-element-xsi:type="BusinessProcess"

Das ist kein Soft-Filter – es ist ein HARD FILTER. Nur was explizit
konfiguriert ist, wird extrahiert. Kein Wildcard-Default.

Der Wildcard * im model-Pattern matcht jeden sourceModel-Wert.


5. NO-OVERWRITE PRINZIP (M2B01/M2B02)
--------------------------------------------------------------------------------
M2B01 erstellt keine BPMN-Datei für einen Prozess der bereits im
bpmnarchive/ existiert (Prüfung via process id im BPMN-Dokument).

M2B02 kopiert keine Datei ins active BPMN-Verzeichnis wenn dort bereits
eine gleichnamige Datei liegt.

Konsequenz: Einmal in Camunda angereicherte BPMN-Dateien werden durch
einen erneuten M2B Lauf nicht überschrieben. Die Anreicherung ist sicher.


6. BOOTSTRAP-MECHANISMUS (M2B04)
--------------------------------------------------------------------------------
Der Bootstrap löst einen speziellen Fall: Eine BPMN-Hülle wurde mit dem
Placeholder-ID "Process_Example_001" erstellt (Camunda Default) und muss
mit der echten Archi-Identifier verknüpft werden.

Bootstrap-Bedingung:
  - Process id im active BPMN = "Process_Example_001"
  - Genau 1 matching Archi BusinessProcess im mapping-Kontext

Bei 0 Kandidaten: Placeholder bleibt, kein Abbruch.
Bei >1 Kandidaten: Warnung, kein Upgrade, kein Abbruch.
  → Workaround: M2Bmapping.txt präzisieren um Ambiguität aufzulösen.

Bootstrap ist KEIN Massenvorgang. Er betrifft genau einen Placeholder
pro BPMN-Datei.


7. PROZESS-ID GUARDRAIL (M2B04)
--------------------------------------------------------------------------------
M2B04 nimmt einen Snapshot aller Prozess-IDs vor und nach der Anreicherung.
Wenn sich die ID-Menge illegal verändert hat (neue IDs ohne Bootstrap-
Erklärung), bricht das Script mit ABORT ab.

Erlaubte Änderungen: nur explizit dokumentierte Bootstrap-Upgrades
(Process_Example_001 → echte ID).

Alle anderen ID-Änderungen = ABORT. IDs sind unveränderlich.


8. WRITEBACK-STRATEGIE (M2B05)
--------------------------------------------------------------------------------
M2B05 schreibt alle active BPMN Dateien zurück in master.xml.

Strategie:
  - Prozess-ID aus BPMN = Archi identifier → Suchschlüssel in master.xml
  - Gefunden in master.xml: REPLACE (BPMN gewinnt, Position bleibt)
  - Nicht gefunden: APPEND

master.xml.bak wird vor jedem Schreiben erstellt (Safety-Backup).
Archi-Elemente (sourceSystem=archi) werden NIEMALS angefasst.
Nur <definitions> Blöcke werden ersetzt/ergänzt.

Hull-only BPMN (keine Tasks, Events etc.) werden als solche geloggt
aber trotzdem zurückgeschrieben – leere Hüllen sind valider Zustand.


9. SCOPE-SNAPSHOT (M2B06)
--------------------------------------------------------------------------------
M2B06 scannt master.xml nach allen (sourceSystem, sourceModel) Kombinationen
und schreibt einen Snapshot-Block in run-scope.txt.

Der Snapshot ist ausschließlich Dokumentation:
  #SNAPSHOT_SOURCE=...
  #SNAPSHOT_MODEL=...

Aktive SOURCE= Einträge werden NIE berührt. Bestehende Snapshot-Blöcke
werden ersetzt. M2B06 ist idempotent.


10. GRENZEN DES M2B FLOWS
--------------------------------------------------------------------------------
- Erzeugt keine Prozessinhalte – nur Hüllen (hull-only BPMN)
- Versteht keine BPMN-Semantik – transportiert Subtrees
- Kann keine ID-Konflikte zwischen Archi und BPMN lösen
- M2B04 Enrichment ist minimal: nur name= wird aus Archi übertragen
- Der Flow funktioniert nur wenn master.xml existiert und valide ist
- M2B01 filename = safe_filename(process_name) – Sonderzeichen werden
  entfernt (erlaubt: Leerzeichen, - _ . +)