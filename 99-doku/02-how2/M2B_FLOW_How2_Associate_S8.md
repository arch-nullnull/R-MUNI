================================================================================
M2B FLOW — HOW2 (Associate)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : M2B_FLOW_How2_Associate_S8
Tag             : #associate #how2 #m2bflow #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : ENTWURF
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Hinweis         : Inhalt initial ident mit DEV-Gegenstück — inhaltliche Trennung in Stage 1
================================================================================



VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- Python 3.10+
- master.xml muss vorhanden und valide sein
  (erzeugt durch XML Flow oder manuell gepflegt)
- M2Bmapping.txt korrekt konfiguriert
- Ordnerstruktur gemäß structure.txt vorhanden


KOMPLETTER FLOW – SCHRITT FÜR SCHRITT
--------------------------------------------------------------------------------

Schritt 1: Root auflösen
  python M2B00-root_resolve.py
  → Fast-Path: versucht XML00-root.resolved.txt zu nutzen
  → Fallback: liest root.txt direkt
  → Erzeugt: 03-stages/99-logs/M2B00-root.resolved.txt

Schritt 2: BusinessProcess Hüllen extrahieren
  python M2B01-master_extract.py
  → Liest master.xml
  → Filtert via M2Bmapping.txt (HARD FILTER)
  → Erstellt BPMN-Hüllen für jeden neuen Prozess
  → Erzeugt: 03-stages/01-bpmnarchive/<Prozessname>.bpmn
  → Überschreibt NICHT wenn Datei bereits existiert

Schritt 3: Hüllen aktivieren
  python M2B02-activate_model.py
  → Kopiert neue BPMN-Hüllen aus bpmnarchive/ ins active Verzeichnis
  → Ziel: 01-model/01-bpmn/00-bpmnactive/
  → Überschreibt NICHT wenn Datei bereits existiert

Schritt 4: Zwischenartefakte leeren
  python M2B03-clear.py
  → Leert bpmnarchive/ (M2B Artefakte)
  → Löscht M2B01/M2B02 Logs
  → Behält: M2B00-root.resolved, M2B03 Log

--- MANUELLE PHASE: Camunda Anreicherung ---
  Die active BPMN Dateien in 01-model/01-bpmn/00-bpmnactive/ können nun
  in Camunda Modeler geöffnet und mit Prozessinhalt angereichert werden.
  Danach zurück zum Flow:

Schritt 5: Anreicherung mit Archi-Daten abgleichen
  python M2B04-reconcile_enrich.py
  → Liest alle active BPMN Dateien
  → Bootstrap: Process_Example_001 → echte Archi-ID (wenn eindeutig)
  → Überträgt name= aus master.xml auf BPMN-Prozess
  → Guardrail: Prozess-ID-Menge darf sich nicht illegal ändern
  → Schreibt BPMN-Dateien zurück (in-place)

Schritt 6: Zurückschreiben in master.xml
  python M2B05-writeback_master.py
  → Erstellt master.xml.bak (Safety)
  → Liest alle active BPMN Dateien
  → REPLACE wenn Prozess-ID in master.xml gefunden
  → APPEND wenn neu
  → Annotiert sourceSystem=bpmn, sourceModel=<filename>
  → Aktualisiert last-updated Timestamp auf master.xml root

Schritt 7: Scope-Snapshot aktualisieren
  python M2B06-scope_snapshot.py
  → Scannt master.xml nach sourceSystem/sourceModel Kombinationen
  → Schreibt Snapshot-Block in 03-stages/run-scope.txt
  → Ersetzt bestehenden Snapshot, berührt keine aktiven Einträge


KONFIGURATIONSDATEIEN – KURZREFERENZ
--------------------------------------------------------------------------------

02-artifacts/00-xml/01-mapping/M2Bmapping.txt
  Format: archi[model=<pattern>]-element-xsi:type="<Typ>"
  Zweck: Definiert welche Elemente aus master.xml als BPMN extrahiert werden.
  Beispiel:
    archi[model=*]-element-xsi:type="BusinessProcess"
    archi[model=*Importer*]-element-xsi:type="BusinessProcess"
  Wildcard * matcht alles. Spezifischer Pattern = engere Selektion.


HÄUFIGE FEHLER UND LÖSUNGEN
--------------------------------------------------------------------------------

Fehler: "master.xml not found"
  Ursache: XML Flow wurde nicht ausgeführt oder master.xml fehlt.
  Lösung: XML Flow komplett ausführen (XML00–XML07).

Keine BPMN-Hüllen werden erstellt (created=0)
  Ursache 1: M2Bmapping.txt filtert alle Elemente heraus.
    Lösung: Pattern in M2Bmapping.txt prüfen. archi[model=*] matcht alle Modelle.
  Ursache 2: Alle Prozesse existieren bereits im bpmnarchive/.
    Lösung: M2B03 ausführen um Archiv zu leeren, dann M2B01 neu.
  Ursache 3: master.xml enthält keine BusinessProcess Elemente.
    Lösung: XML Flow prüfen, mapping.txt auf BusinessProcess prüfen.

Bootstrap schlägt fehl (>1 Kandidaten)
  Ursache: Mehrere BusinessProcess in master.xml passen zum Mapping-Kontext.
  Lösung: M2Bmapping.txt präzisieren (z.B. model=*ArchitectureModell*).
  Ergebnis: Bootstrap überspringen, Placeholder bleibt → manuell in Camunda
  die richtige ID setzen.

M2B04 ABORT: "process set changed illegally"
  Ursache: Eine Prozess-ID wurde außerhalb des Bootstrap-Mechanismus geändert.
  Das sollte nicht passieren wenn nur M2B04 die BPMN-Dateien bearbeitet.
  Lösung: BPMN-Dateien im active Verzeichnis auf manuelle ID-Änderungen prüfen.

master.xml.bak ist veraltet
  Hinweis: M2B05 überschreibt master.xml.bak bei jedem Lauf.
  Wenn ein älterer Stand benötigt wird → HLP06 Backup verwenden.

BPMN-Datei erscheint nicht im active Verzeichnis nach M2B02
  Ursache: Datei mit gleichem Namen existiert bereits im active Verzeichnis.
  Lösung: Bestehende Datei im active Verzeichnis prüfen – sie ist die
  aktuelle Version. M2B02 überschreibt nie.


TYPISCHER ARBEITSABLAUF – NEUEN PROZESS ANLEGEN
--------------------------------------------------------------------------------
1. BusinessProcess in Archi anlegen und Modell exportieren (OEF)
2. XML Flow ausführen → master.xml aktualisiert
3. M2B00 → M2B01 → M2B02 → M2B03 ausführen
4. Neue BPMN-Hülle in Camunda Modeler öffnen
5. Prozess modellieren (Tasks, Events, Gateways etc.)
6. BPMN speichern (Camunda 7 Format empfohlen)
7. M2B04 → M2B05 → M2B06 ausführen
8. master.xml enthält nun den angereicherten Prozess


TYPISCHER ARBEITSABLAUF – BESTEHENDEN PROZESS AKTUALISIEREN
--------------------------------------------------------------------------------
1. BPMN-Datei in 01-model/01-bpmn/00-bpmnactive/ in Camunda öffnen
2. Änderungen vornehmen, speichern
3. M2B04 → M2B05 → M2B06 ausführen
   (M2B00–M2B03 sind nicht notwendig wenn keine neuen Prozesse entstehen)
4. master.xml enthält den aktualisierten Stand


SCOPE-SNAPSHOT LESEN
--------------------------------------------------------------------------------
Nach M2B06 enthält run-scope.txt einen Block wie:

  # SNAPSHOT_START
  # ==========================================================
  # MASTER.XML SNAPSHOT - generated by M2B06-scope_snapshot.py
  # Last updated: 2026-03-02T...
  # ==========================================================
  # --- sourceSystem: archi ---
  #SNAPSHOT_SOURCE=archi
  #SNAPSHOT_MODEL=R+Muni Architecture Modell.xml
  # --- sourceSystem: bpmn ---
  #SNAPSHOT_SOURCE=bpmn
  #SNAPSHOT_MODEL=BUP01-Entwicklung.bpmn
  # SNAPSHOT_END

Dieser Block ist rein dokumentarisch. Er zeigt was aktuell in master.xml
enthalten ist. Er steuert nichts.