================================================================================
FLOW_SCRIPTRUNNER – PRINCIPLES
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : FLOW_SCRIPTRUNNER_principles_S4
Tag             : #dev #principles #flowscriptrunner #flw #s4 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-02
Aktualisiert    : 2026-03-07 — FLW-Reihe Umbenennung + FLW02 ergänzt
Ablageort       : 00-concept/01-principles/FLOW_SCRIPTRUNNER_principles_S4.txt
================================================================================


1. ZWECK UND DESIGNPHILOSOPHIE
--------------------------------------------------------------------------------
Die FLW-Serie ist der modellgetriebene Orchestrator des Blueprints.
Sie verbindet ArchiMate-Arbeitspakete und BPMN-Service-Tasks mit konkreten
Python-Scripts – ohne Hardcoding, ohne Engine-Semantik.

Kernprinzip: Das Modell entscheidet was läuft. Der Mensch entscheidet wann.
FLW00 fragt nicht – FLW00 führt aus was das Modell sagt, wenn du es startest.

FLW00 ist kein Scheduler, kein Trigger-System, keine Automatisierungslösung.
Es ist die Sichtbarmachung impliziter Abläufe als ausführbare Sequenz.
MUNI ist die Stufe VOR der Automatisierung.


2. FLW-SERIE – ÜBERSICHT UND AUFGABENTRENNUNG
--------------------------------------------------------------------------------
Die FLW-Serie besteht aus drei Scripts und zwei Konfigurationsfiles:

FLW00-scriptrunner.py  (Orchestrator)
  Liest flowtriggers.txt und flowmapping.txt.
  Scannt XML/BPMN/Archimate-Dateien, erkennt Trigger, führt Scripts aus.
  Das einzige Script das andere Scripts startet.

FLW01-discover.py  (Typ-Scanner)
  Zeigt welche xsi:type Werte und BPMN-Tags in den Quelldateien vorhanden sind.
  Zeigt ob diese bereits in flowtriggers.txt konfiguriert sind.
  Verändert nichts. Referenz für: flowtriggers.txt

FLW02-map_elements.py  (Element-ID-Scanner)
  Zeigt welche konkreten Elemente (ID + Name + Typ) in den Quelldateien sind.
  serviceTask mit Trigger:Ja + Scriptname als Name → fertige Mapping-Zeile.
  Verändert nichts. Referenz für: flowmapping.txt

flowtriggers.txt  (Detection-Konfiguration)
  Definiert welche Modellelemente als Trigger erkannt werden.
  Kein Script-Name hier.

flowmapping.txt  (Dispatch-Konfiguration)
  Verbindet dispatch_key mit Script-Name.
  Kein Modell-Kontext hier.


3. DREI-PHASEN-MODELL (FLW00)
--------------------------------------------------------------------------------
Phase 1 – SCAN:
  Alle XML/BPMN/Archimate Dateien in 02-artifacts/00-xml/03-child/ werden
  gescannt. Für jede Datei werden Trigger gemäß flowtriggers.txt erkannt.
  Ergebnis: Liste aller Trigger mit order-Wert.

Phase 2 – SORT:
  Alle gesammelten Trigger werden nach dem order-Wert sortiert.
  Die order-Reihenfolge ist die einzige garantierte Ausführungsreihenfolge.
  Dateisystem-Reihenfolge, Modell-Reihenfolge, Fundort – alles irrelevant.

Phase 3 – EXEC:
  Scripts werden in order-Reihenfolge via subprocess ausgeführt.
  CWD ist immer BLUEPRINT_ROOT.
  returncode != 0 → ABORT. Kein Script nach einem Fehler.


4. KONFIGURATIONSTRENNUNG
--------------------------------------------------------------------------------
Zwei separate Konfigurationsfiles mit klar getrennten Aufgaben:

flowtriggers.txt (Detection):
  Definiert WELCHE Modellelemente als Trigger erkannt werden.
  Format: INI-Sektionen mit order, source, element_tag, element_type,
          conditions, dispatch_key.
  Kein Script-Name hier.

flowmapping.txt (Dispatch):
  Verbindet dispatch_key mit Script-Name.
  Format: <dispatch_key>=<script_name.py>
  Kein Modell-Kontext hier.

Konsequenz: Ein dispatch_key der in flowmapping.txt nicht vorkommt
→ SKIP (mit Log), kein Abbruch.
Ein Script in flowmapping.txt das nicht gefunden wird → ABORT.


5. DETECTION-ENGINE: ARCHI vs BPMN
--------------------------------------------------------------------------------
Archi-Detection (source=archi):
  Arbeitet mit Property-Indirektion. Archi OEF speichert Property-Namen
  in <propertyDefinition> Elementen und referenziert sie via
  propertyDefinitionRef. FLW00 baut zuerst einen propdefs-Index auf
  (id → name Mapping), dann liest er Properties der Elemente.

  Voraussetzung für Archi-Trigger:
  - element_tag matcht lokalen Tag-Namen des Elements
  - element_type matcht xsi:type Attribut (wenn konfiguriert)
  - ALLE conditions erfüllt (AND-Verknüpfung)
  - dispatch_key liefert nicht-leeren Wert

BPMN-Detection (source=bpmn):
  Liest Kind-Elemente direkt (keine Indirektion).
  condition.tag: prüft ob ein Kind-Element mit gegebenem Tag-Namen
  den gesuchten Text enthält.

  Voraussetzung für BPMN-Trigger:
  - element_tag matcht lokalen Tag-Namen des Tasks
  - ALLE conditions erfüllt (AND-Verknüpfung)
  - dispatch_key via attr: (meist id-Attribut)


6. ORDER-PRINZIP
--------------------------------------------------------------------------------
order ist ein Integer in jeder flowtriggers.txt Sektion. Er bestimmt
ausschließlich die globale Ausführungsreihenfolge aller erkannten Trigger –
über alle Dateien und alle Modelltypen hinweg.

Gleiche order-Werte zwischen Sektionen sind zulässig aber nicht empfohlen
(Reihenfolge bei Gleichstand undefiniert).

Wichtig: order hat NICHTS mit der Position im Modell zu tun. Ein WorkPackage
das im Archi-Diagramm "oben links" steht läuft nicht vor einem das "unten
rechts" steht – es läuft in der Reihenfolge seines order-Werts.


7. CONDITION-AUSWERTUNG
--------------------------------------------------------------------------------
Alle conditions in einer Sektion werden AND-verknüpft ausgewertet.
Ein Element triggert nur wenn ALLE conditions erfüllt sind.

Archi condition-Typen:
  property:<n>=<Wert>
    Prüft ob das Element eine Property mit Name=<n> und Wert=<Wert> hat.

BPMN condition-Typen:
  tag:<TagName>:<Text>
    Prüft ob ein Kind-Element mit lokalem Tag <TagName> den Text <Text> enthält.


8. DISPATCH-KEY PRINZIP
--------------------------------------------------------------------------------
Der dispatch_key ist der Schlüssel den FLW00 nach Erkennung eines Triggers
in flowmapping.txt nachschlägt.

Archi dispatch_key Typen:
  property:<PropertyName>  → Wert der genannten Property des Elements
  attr:<Attributname>      → Wert des genannten XML-Attributs

BPMN dispatch_key Typen:
  attr:<Attributname>      → Wert des genannten XML-Attributs (meist "id")

Ist der dispatch_key leer (Property nicht vorhanden, Attribut fehlt) →
Trigger wird ignoriert, kein Abbruch.


9. FLW02 SONDERREGEL – SCRIPTNAME AUS TASK-NAME
--------------------------------------------------------------------------------
FLW02-map_elements.py liest bei BPMN serviceTask mit Trigger:Ja
den name-Wert des Tasks direkt als Scriptnamen.

Voraussetzung im Camunda Modeler:
  - serviceTask name    = Scriptname (z.B. "CSV01-validate_model.py")
  - documentation       = "Trigger:Ja"

Ergebnis in flw02-map_elements.txt:
  Activity_0abc123=CSV01-validate_model.py
  → direkt kopierbar in flowmapping.txt, kein manuelles Ergänzen

Fehlt der Name trotz Trigger:Ja:
  → Platzhalter <SCRIPT_HIER_EINTRAGEN> + Warnung in Konsole und Log
  → Lösung: Scriptnamen im Modell nachtragen, FLW02 erneut ausführen

Diese Sonderregel gilt ausschließlich für serviceTask.
Alle anderen Element-Typen erscheinen in Abschnitt 2 (nur Referenz).


10. FLW01 UND FLW02 ALS BEGLEITWERKZEUGE
--------------------------------------------------------------------------------
Beide Tools sind eigenständig – sie importieren nichts aus FLW00.
Beide verändern nichts – sie sind reine Lesewerkzeuge.
Beide schreiben nach 03-stages/ – nie in die Quelldateien.

FLW01 → Referenz für flowtriggers.txt
  Frage: Welche Typen/Tags sind vorhanden und konfiguriert?

FLW02 → Referenz für flowmapping.txt
  Frage: Welche IDs/Namen haben die konkreten Elemente?

Empfohlene Reihenfolge beim Aufsetzen neuer Trigger:
  FLW01 ausführen → flowtriggers.txt anpassen
  FLW02 ausführen → flowmapping.txt befüllen
  FLW00 ausführen → Ergebnis prüfen


11. GRENZEN DER FLW-SERIE
--------------------------------------------------------------------------------
- Keine parallele Ausführung – strikt sequenziell
- Kein Retry bei Fehler – ein fehlgeschlagenes Script stoppt alles
- Kein Rollback – bereits ausgeführte Scripts werden nicht rückgängig gemacht
- Kein Scheduling – FLW00 startet nur wenn manuell aufgerufen
- Kein Monitoring – nur Log-Datei als Rückmeldung
- Versteht keine Modellsemantik – erkennt Tags und Properties, nicht Bedeutung
- Scripts werden als Kindprozesse gestartet – kein gemeinsamer Zustand
- FLW02 Sonderregel nur für serviceTask – andere Typen nie automatisch


================================================================================
FLW-SERIE – PRINCIPLES  |  S4  |  ENDE
================================================================================
