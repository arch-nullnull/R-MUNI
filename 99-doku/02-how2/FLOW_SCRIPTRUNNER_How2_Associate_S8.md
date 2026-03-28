================================================================================
FLOW_SCRIPTRUNNER — HOW2 (Associate)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : FLOW_SCRIPTRUNNER_How2_Associate_S8
Tag             : #associate #how2 #flowscriptrunner #s8
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
Erstellt        : 2026-03-02
Aktualisiert    : 2026-03-07 — FLW-Reihe Umbenennung + FLW02 ergänzt
Ablageort       : 00-concept/02-how2/FLOW_SCRIPTRUNNER_How2_S4.txt
================================================================================


VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- Python 3.10+
- BLUEPRINT_ROOT korrekt in root.txt eingetragen
- flowtriggers.txt und flowmapping.txt in 02-artifacts/04-flow/ vorhanden
- Quelldateien in 02-artifacts/00-xml/03-child/ vorhanden


================================================================================
FLW00 – SCRIPTRUNNER STARTEN
================================================================================

  cd 02-artifacts/04-flow/
  python FLW00-scriptrunner.py

  root.txt wird automatisch zwei Ebenen aufwärts gesucht.
  Log: 03-stages/99-logs/flw00-scriptrunner.log (append)


WAS FLW00 IN DER KONSOLE AUSGIBT
--------------------------------------------------------------------------------
  [FLW00] ... | Blueprint root resolved: <pfad>
  [FLW00] ... | Loaded N mapping entries
  [FLW00] ... | Loaded N trigger rule(s) (order: 10, 20)
  [FLW00] ... | SCAN: 02-artifacts/00-xml/03-child/00-archimatechild/mini.xml
  [FLW00] ... |   TRIGGER [order=10] [archi_workpackage] key=Script info=id-abc
  [FLW00] ... | Detected N trigger(s)
  [FLW00] ... | Execution order: Script(order=10)
  [FLW00] ... | EXEC: .../02-artifacts/01-scripts/CSV02-leer.py
  [FLW00] ... | FLW00 finished: executed=1, total_triggers=1


================================================================================
FLW01 – DISCOVER STARTEN
================================================================================

  python FLW01-discover.py

  Zeigt welche Element-Typen und Tags in den Quelldateien vorhanden sind
  und ob sie bereits in flowtriggers.txt konfiguriert sind.

  Ausgabe:
    03-stages/99-logs/flw01-discover.log  (detailliert, mit Fundorten)
    03-stages/flw01-discover.txt          (kompakt, Referenz)

  Wann verwenden:
  - Neue XML/BPMN-Dateien wurden in 03-child abgelegt
  - Prüfen ob alle Typen in flowtriggers.txt erfasst sind
  - Vor dem Anlegen neuer Trigger-Regeln


================================================================================
FLW02 – MAP_ELEMENTS STARTEN
================================================================================

  python FLW02-map_elements.py

  Scannt alle BPMN/Archi-Dateien und gibt alle Elemente mit
  ID + Name + Typ aus – als fertige Referenz für flowmapping.txt.

  Ausgabe:
    03-stages/99-logs/flw02-map_elements.log
    03-stages/flw02-map_elements.txt

  Wann verwenden:
  - flowmapping.txt befüllen oder aktualisieren
  - Nach Änderungen im BPMN-Modell (neue Tasks, geänderte IDs)
  - Prüfen welche serviceTask IDs mit Trigger:Ja vorhanden sind


================================================================================
FLOWTRIGGERS.TXT – KONFIGURATION
================================================================================

  Datei: 02-artifacts/04-flow/flowtriggers.txt
  Format: INI (configparser kompatibel)

  Minimale Sektion (Archi):
    [archi_workpackage]
    order        = 10
    source       = archi
    element_tag  = element
    element_type = WorkPackage
    condition.1  = property:Trigger=Ja
    dispatch_key = property:Type

  Minimale Sektion (BPMN):
    [bpmn_servicetask]
    order        = 20
    source       = bpmn
    element_tag  = serviceTask
    condition.1  = tag:documentation:Trigger:Ja
    dispatch_key = attr:id

  Pflichtfelder : order, source, element_tag, mind. eine condition, dispatch_key
  Optional      : element_type (nur Archi, filtert xsi:type)
  Kommentare    : Zeilen die mit # beginnen werden ignoriert


================================================================================
FLOWMAPPING.TXT – KONFIGURATION
================================================================================

  Datei: 02-artifacts/04-flow/flowmapping.txt
  Format: <dispatch_key>=<script_dateiname.py>

  Beispiele:
    Script=CSV02-leer.py
    Activity_0uuaxhy=CSV00-validate_environment.py

  Regeln:
  - Kein doppelter Key erlaubt (ABORT)
  - Script-Name ohne Pfad – FLW00 sucht in 02-artifacts/01-scripts/
  - Script muss vorhanden sein – fehlendes Script → ABORT
  - Unmapped dispatch_key → SKIP (kein Abbruch, wird geloggt)
  - Reihenfolge der Einträge egal – Ausführungsreihenfolge kommt aus order

  Empfehlung: flowmapping.txt nicht manuell befüllen.
  Stattdessen FLW02 verwenden → Abschnitt 1 aus flw02-map_elements.txt
  direkt kopieren.


================================================================================
NEUEN TRIGGER ANLEGEN – SCHRITT FÜR SCHRITT
================================================================================

  Beispiel: serviceTask "CSV01-validate_model.py" soll ausgeführt werden.

  SCHRITT 1 – Camunda Modeler
    serviceTask anlegen oder öffnen
    name        = CSV01-validate_model.py
    documentation = Trigger:Ja

  SCHRITT 2 – BPMN exportieren
    Datei speichern nach:
    02-artifacts/00-xml/03-child/01-bpmnchild/

  SCHRITT 3 – flowtriggers.txt prüfen
    Sektion [bpmn_servicetask] bereits vorhanden? → weiter mit Schritt 4
    Neue Sektion anlegen falls neuer Element-Typ:
      FLW01-discover.py ausführen → flw01-discover.txt prüfen
      Neue Sektion in flowtriggers.txt ergänzen

  SCHRITT 4 – FLW02 ausführen
    python FLW02-map_elements.py
    flw02-map_elements.txt öffnen
    Abschnitt 1 kopieren → in flowmapping.txt einfügen

  SCHRITT 5 – FLW00 ausführen und prüfen
    python FLW00-scriptrunner.py
    flw00-scriptrunner.log prüfen


================================================================================
HÄUFIGE FEHLER UND LÖSUNGEN
================================================================================

Fehler: "flowtriggers.txt not found"
  Datei in 02-artifacts/04-flow/ anlegen oder root.txt prüfen.

Fehler: "flowmapping.txt not found"
  Datei in 02-artifacts/04-flow/ anlegen.

Fehler: "mapped script not found"
  Script in flowmapping.txt eingetragen aber Datei fehlt in
  02-artifacts/01-scripts/ → Script-Datei prüfen.

Fehler: "[section] order is required"
  order = <Zahl> in der betroffenen flowtriggers.txt Sektion ergänzen.

Fehler: "script failed"
  Script direkt ausführen und Fehler analysieren.
  Das Script selbst schreibt Details in sein eigenes Logfile.

FLW00 erkennt keine Trigger (Detected 0 trigger(s))
  1. Quelldateien nicht in 02-artifacts/00-xml/03-child/?
     → Dateien in den richtigen Unterordner legen
  2. element_tag stimmt nicht überein?
     → FLW01 ausführen um vorhandene Tags zu sehen
  3. condition nicht erfüllt?
     → documentation / Property direkt im Modell prüfen
  4. dispatch_key liefert leeren Wert?
     → id-Attribut / Property im Modell prüfen

FLW02 findet keine BPMN-Dateien
  02-artifacts/00-xml/03-child/01-bpmnchild/ ist leer.
  → BPMN-Dateien aus 01-model/01-bpmn/00-bpmnactive/ dorthin kopieren.

FLW02 Warnung: "Trigger:Ja aber kein Scriptname"
  serviceTask hat Trigger:Ja aber keinen name-Wert.
  → Im Camunda Modeler Scriptnamen als Task-Name eintragen.
  → FLW02 erneut ausführen.


================================================================================
ORDER-WERTE – EMPFEHLUNGEN
================================================================================

  Empfohlene Staffelung:
    10, 20, 30 ... → grobe Schritte zwischen Trigger-Gruppen
    11, 12, 13 ... → Feinschritte innerhalb einer Gruppe

  Bereits vergeben (S3/S4 Baseline):
    order=10 → archi_workpackage  (Archi WorkPackage Trigger)
    order=20 → bpmn_servicetask   (BPMN serviceTask Trigger)

  Neue Trigger ab order=30 aufwärts vergeben.


================================================================================
ABLAGE DER FLW-SERIE
================================================================================

  Scripts:
    02-artifacts/04-flow/FLW00-scriptrunner.py
    02-artifacts/04-flow/FLW01-discover.py
    02-artifacts/04-flow/FLW02-map_elements.py

  Konfiguration:
    02-artifacts/04-flow/flowtriggers.txt
    02-artifacts/04-flow/flowmapping.txt

  Ausgaben (generiert, nicht manuell bearbeiten):
    03-stages/flw01-discover.txt
    03-stages/flw02-map_elements.txt
    03-stages/99-logs/flw00-scriptrunner.log
    03-stages/99-logs/flw01-discover.log
    03-stages/99-logs/flw02-map_elements.log


================================================================================
FLW-SERIE – HOW2  |  S4  |  ENDE
================================================================================
