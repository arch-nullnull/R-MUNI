================================================================================
ATL FLOW – PRINCIPLES
Stage 4 | Aktiv | R+MUNI Blueprint
================================================================================
Erstellt    : 2026-03-08
Stage       : S4 – AKTIV
Ablageort   : 00-concept/01-principles/ATL_FLOW_principles_S4.txt
================================================================================


1. ZWECK UND DESIGNPHILOSOPHIE
--------------------------------------------------------------------------------
Der ATL Flow transformiert ArchiMate-Objekte aus master.xml in
Atlassian-kompatible Formate (Jira CSV-Import) und stellt diese über
das native Jira-Issues-Makro in Confluence dar.

Kernprinzip: ATL ist ein eigenständiger Spin-Off der CSV-Reihe. Er liest
master.xml direkt (nicht die Archi-CSVs aus CSV09) und erzeugt temporäre
Import-Fragmente — keine dauerhaften Reports.

Der ATL Flow erzeugt KEINEN Modellinhalt. Er transportiert bestehende
ArchiMate-Objekte in ein für Atlassian importierbares Format.

Abgrenzung: ATL ersetzt CSV10 (Jira Assets Export, inaktiv seit Free-Downgrade).
ATL hat keinen Einfluss auf CSV-, XML-, M2B- oder HLP-Flows.


2. STUFEN-PRINZIP (STAGE-ISOLATION)
--------------------------------------------------------------------------------
Jede Stage ist autark ausführbar und hängt nur von den Artefakten der
vorherigen Stages ab.

Abhängigkeitskette:
  ATL00 → ATL01 → ATL02

Unterbrechungsregel: Schlägt eine Stage fehl, bricht der Flow ab.
Kein Silent-Fail, kein Weiterlaufen mit Teilresultat.

ATL00 ist Pflicht-Voraussetzung für alle Folge-Scripts. Ohne
ATL00-root.resolved.txt starten ATL01 und ATL02 nicht.


3. ROOT-AUFLÖSUNG
--------------------------------------------------------------------------------
ATL00 löst BLUEPRINT_ROOT auf und schreibt das Ergebnis nach:
  03-stages/99-logs/ATL00-root.resolved.txt

ATL01 und ATL02 lesen ausschließlich aus ATL00-root.resolved.txt.
Kein Script darf den Pfad hardcoden.

Die resolved.txt ist der Beweis dass ATL00 erfolgreich war.
Fehlt sie → Folge-Scripts brechen mit klarer Fehlermeldung ab.


4. SOURCE=ATL ALS SCOPE-STEUERUNG
--------------------------------------------------------------------------------
run-scope.txt steuert welche Modelle ATL01 verarbeitet.
ATL-Scripts lesen ausschließlich SOURCE=ATL Pairs.
Alle anderen SOURCE-Typen werden von ATL ignoriert.

Format eines aktiven ATL-Eintrags:
  SOURCE=ATL
  MODEL=<Dateiname des Modells>

Beispiel:
  SOURCE=ATL
  MODEL=R+Muni Architecture Modell.xml

Eine kommentierte Zeile (#) macht den Eintrag inaktiv.
Kein aktives SOURCE=ATL Pair → ATL00 bricht ab (Hard fail).

Rückwärtskompatibilität: Bestehende SOURCE=ARCHIMATE, SOURCE=BPMN etc.
Einträge bleiben unverändert. Zero Impact auf andere Flows.


5. OUTPUT-KLASSEN UND ABLAGEORTE
--------------------------------------------------------------------------------
Der ATL Flow kennt ausschließlich temporäre Outputs (Import-Fragmente).
Es gibt keinen dauerhaften Report-Output.

Temporäre Outputs (nach Verwendung wertlos):
  03-stages/00-archimatearchive/
    atl_<layer>.csv       Eine CSV pro Layer der Objekte enthält
                          (nur befüllte Layer erzeugen eine Datei)
    jira_ea_import.csv    Jira Issue Import (alle Layer zusammen)

Kein Report-Ordner. 02-artifacts/05-reports/ wird von ATL nicht verwendet.
Ordner 02-artifacts/05-reports/00-archimate/99-ATL/ wird nicht angelegt.


6. LAYER-STRUKTUR (1:1 ARCHIMATE 3.2)
--------------------------------------------------------------------------------
ATL01 gruppiert ArchiMate-Elemente nach dem offiziellen ArchiMate 3.2
Layer-Modell. Dateiname und Layer-Name sind direkt abgeleitet.

  atl_strategy.csv        Strategy
    Capability, ValueStream, CourseOfAction, Resource

  atl_business.csv        Business
    BusinessActor, BusinessRole, BusinessCollaboration,
    BusinessInterface, BusinessProcess, BusinessFunction,
    BusinessInteraction, BusinessEvent, BusinessService,
    BusinessObject, Contract, Representation, Product

  atl_application.csv     Application
    ApplicationComponent, ApplicationCollaboration,
    ApplicationInterface, ApplicationFunction,
    ApplicationInteraction, ApplicationProcess,
    ApplicationEvent, ApplicationService, DataObject

  atl_technology.csv      Technology & Physical
    Node, Device, SystemSoftware, TechnologyCollaboration,
    TechnologyInterface, Path, CommunicationNetwork,
    TechnologyFunction, TechnologyInteraction,
    TechnologyProcess, TechnologyEvent, TechnologyService,
    Artifact, Equipment, Facility, DistributionNetwork, Material

  atl_motivation.csv      Motivation
    Stakeholder, Driver, Assessment, Goal, Outcome,
    Principle, Requirement, Constraint, Meaning, Value

  atl_implementation.csv  Implementation & Migration
    WorkPackage, Deliverable, ImplementationEvent, Plateau, Gap

  atl_relations.csv       Relations
    AssociationRelationship, CompositionRelationship,
    AggregationRelationship, AssignmentRelationship,
    RealizationRelationship, ServingRelationship,
    AccessRelationship, InfluenceRelationship,
    TriggeringRelationship, FlowRelationship,
    SpecializationRelationship

  atl_other.csv           Other
    Grouping, Location, Junction
    (+ alle unbekannten Typen als Fallback)

Hinweis: Nur Layer die Objekte enthalten erzeugen eine CSV-Datei.
Nicht klassifizierte Typen landen in atl_other (Warnung im Log).

Hinweis Views: Views (DiagramModel etc.) sind keine Elemente in master.xml
und erzeugen keine CSV. Die Jira-Komponente "Views" ist für manuelle
Einträge reserviert.


7. ZWEISTUFIGE FILTERUNG IN JIRA
--------------------------------------------------------------------------------
ATL02 befüllt zwei Jira-Felder für unterschiedliche Filtergranularität:

  Component/s  =  Layer-Name     (grob — 9 vordefinierte Werte)
                                  z.B. "Application"
  Labels       =  ArchiType      (fein — alle ArchiTypes als Stichwort)
                                  z.B. "ApplicationComponent"

Vorteil: Grob-Filter via Komponente (wenige, stabile Werte, vordefiniert
im Projekt). Fein-Filter via Stichwort (automatisch, kein manueller Aufwand).
Beide Filter gleichzeitig nutzbar in Jira-Suche und Confluence-Makro.

Labels-Regel: Leerzeichen → Underscore (Jira-Anforderung).
Komponenten-Regel: Exakter Name muss im Jira-Projekt vordefiniert sein.

Jira-Projekt R+MUNI EA (MUNIEA) — 9 Komponenten:
  Strategy, Business, Application, Technology & Physical,
  Motivation, Implementation & Migration, Relations, Other, Views


8. MERGE-LOGIK (EXTERNAL ISSUE ID)
--------------------------------------------------------------------------------
ATL02 schreibt den objectKey (Archi-ID) in das Feld "External issue ID".

Erster Import  → Issue wird neu angelegt
                 External issue ID = objectKey gespeichert

Zweiter Import → Jira findet External issue ID
                 → Update statt Duplikat

Voraussetzung: Beim Jira-Import muss "External issue ID" auf
"Externe Vorgangs-ID" gemappt werden.

Konsequenz: Der ATL Flow ist beliebig oft wiederholbar ohne manuelle
Bereinigung in Jira.


9. ID-KOLLISIONSSTRATEGIE (ATL01)
--------------------------------------------------------------------------------
Gleiche identifier über mehrere sourceModels → merge (Default).
Erste Instanz gewinnt. SourceModel wird komma-separiert zusammengeführt.

Der ATL-Scope-Filter (SOURCE=ATL MODEL=...) reduziert ID-Kollisionen
bereits erheblich — nur das konfigurierte Modell wird verarbeitet.


10. BPMN-INTEGRATION
--------------------------------------------------------------------------------
BPMN-Prozesse die per Name mit einem ArchiMate-Element matchen →
Enrich-Prinzip: bestehendes Element erhält BPMN_ID Spalte.

Ungematchte BPMN-Prozesse → neues Stub-Element (ArchiType=BusinessProcess,
Layer=Business).

Konsistent mit bpmnmastercsvsync.txt.


11. JIRA CSV-FORMAT
--------------------------------------------------------------------------------
ATL02 erzeugt Standard-Jira-Issues-CSV (nicht Jira Assets).
Encoding: UTF-8 mit BOM.
Issue Type: immer "Task".

Spalten (in Reihenfolge):
  Summary           Pflicht — Name des EA-Objekts
  Issue Type        Pflicht — "Task"
  Description       Beschreibung + EA-Kontext
  Component/s       Layer-Name (Jira Komponente, vordefiniert)
  Labels            ArchiType (Stichwort, fein)
  External issue ID objectKey (Merge-Schlüssel)
  EA-ObjectKey      objectKey (Referenz-ID für Verlinkung)
  EA-ArchiType      ArchiType (lesbar)
  EA-Layer          Layer-Name (redundant zu Component/s)
  EA-SourceModel    Herkunftsmodell


12. CONFLUENCE-DARSTELLUNG
--------------------------------------------------------------------------------
EA-Objekte in Confluence via natives Jira-Issues-Makro — kein HTML-Script.

Voraussetzung: Jira-Import (ATL02) abgeschlossen.

JQL-Beispiele:
  Grob (Layer):   component = "Application"
  Fein (Typ):     labels = "ApplicationComponent"
  Kombiniert:     component = "Business" AND labels = "BusinessProcess"
  Alles:          project = MUNIEA

Live-Darstellung — Änderungen in Jira sofort in Confluence sichtbar.


13. MKDIR-VERBOT
--------------------------------------------------------------------------------
ATL-Scripts legen keine Ordner an.
ATL00 prüft Existenz und bricht ab wenn ein Ordner fehlt.

Benötigte Ordner (manuell anlegen):
  03-stages/00-archimatearchive/
  03-stages/99-logs/


14. LOG-VERHALTEN
--------------------------------------------------------------------------------
Jede Stage schreibt ein eigenes Log nach 03-stages/99-logs/:
  ATL00-validate_atl_scope.log
  ATL01-masterXml2AtlCsv.log
  ATL02-atlCsv2JiraCsv.log

Logs werden bei jedem Lauf überschrieben.
Konsolen-Output ist identisch zum Log-Output.


================================================================================
ATL FLOW PRINCIPLES | S4 | ENDE
================================================================================
