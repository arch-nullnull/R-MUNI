================================================================================
ROSETTA STONE – R+MUNI
Block 2: Artifacts und Scripts
================================================================================
Zweck dieses Dokuments:
Mapping zwischen R+MUNI internen Begriffen und der offiziellen
ArchiMate 3.2 / TOGAF Terminologie.

Erstellt: Dienstag, 03. März 2026
================================================================================


--------------------------------------------------------------------------------
VORBEMERKUNG – ARTIFACT-SCOPE
--------------------------------------------------------------------------------
R+MUNI enthält 127 Artifacts im Modell.
Davon werden in Block 2 ausgeblendet:
  - Ordnerstruktur (00- bis 99- Folder-Artifacts)
    → reine Infrastruktur, kein Architekturinhalt
    → im ArchiMate Kontext nur über Namen relevant

Fokus liegt auf:
  - Script-Familien
  - Integrations-Flows
  - Konfigurationsdateien
  - Dokumentations-Artefakte
  - Modell-Referenzen


================================================================================
TEIL 1 – INTEGRATIONS-ARCHITEKTUR GESAMT
================================================================================

--------------------------------------------------------------------------------
master.xml – Canonical Aggregation Hub
--------------------------------------------------------------------------------
Intention:
  Zentrales Aggregations-XML das zwischen allen Welten vermittelt.
  Archi-IDs werden als globaler ID Handler genutzt.
  ID-lose Objekte werden über den CSV Flow aufgelöst.
  Temporär im Lebenszyklus — wird nach Verwendung verworfen.
  Aktuell angebundene Quellen: OEF XML, BPMN 2.0 XML.
  Weitere Quellen können andocken (offene Architektur).

Norm-Begriff:
  Canonical Aggregation Hub
  Transient Integration Artifact

TOGAF Einordnung:
  Phase E/F — Transition Architecture
  Temporäres Artefakt das keinen dauerhaften Architekturzustand definiert

Rosetta:
  "Aggregiert zwischen Welten"        →  Canonical Aggregation Hub
  "Archi IDs zweckentfremdet"         →  Surrogate Key Pattern
  "ID-lose Objekte → CSV Flow"        →  Identity Resolution via Canonical Channel
  "X Quellen können andocken"         →  Open Integration Architecture
  "Temporär, wird verworfen"          →  Transient Artifact
  "Aktuell OEF + BPMN"                →  Realized Integration Points
  "Weitere Quellen möglich"           →  Extensible Integration Pattern

Bewertung:
  Architektonisch sauber — Archi als Identity Authority ist eine
  explizite Architecture Decision, kein Missbrauch.
  Surrogate Key Pattern ist in Enterprise Integration anerkannt.
  Offene Erweiterbarkeit entspricht Open Integration Architecture.


--------------------------------------------------------------------------------
GESAMTÜBERSICHT INTEGRATION FLOWS
--------------------------------------------------------------------------------

  Flow 1 – CSV Input Channel (Canonical Input)
  Flow 2 – XML Internal Flow (OEF Exchange)
  Flow 3 – M2B Cross-Domain Transform (Master to BPMN)
  Flow 4 – flow.py Model-Driven Execution (Script Runner)

Grundprinzip aller Flows:
  Archi ist die einzige Identity Authority.
  master.xml ist der einzige Aggregationspunkt.
  CSV ist der einzige Eingangskanal für ID-Auflösung.
  Kein Flow erzeugt neue Identität außerhalb dieses Rahmens.


================================================================================
TEIL 2 – SCRIPT-FAMILIEN
================================================================================

--------------------------------------------------------------------------------
FLOW 1 – CSV-Scripts (CSV Input Channel)
--------------------------------------------------------------------------------
Scripts:
  CSV00  validate_environment.py
  CSV01  validate_model.py
  CSV02  (Platzhalter — Beta)
  CSV03  resolve_run_scope.py
  CSV04  model-overview.py
  CSV05  create_master_csvs.py
  CSV06  append_child_to_master.py
  CSV07  xlsx_2_csv.py
  CSV08  properties2csv.py
  CSV09  masterxml2csv.py
  CSV99  export_snapshot.py

Intention:
  Universeller Eingangskanal für alle externen und internen Objekte.
  Archi vergibt über diesen Kanal IDs für ID-lose Objekte —
  ein Verhalten das OEF nicht bietet.
  Gilt für alle Objekte — auch bereits bekannte — weil der Kanal
  selbst die ID-Stabilität im Zyklus garantiert.
  Keine Ausnahmen vom CSV-Kanal für die ID-Auflösung.

Norm-Begriff:
  Canonical Input Channel
  Identity Stabilization Pattern
  Single Entry Point Pattern

TOGAF Einordnung:
  Phase C — Information Systems Architecture
  Integration Interface Definition

Rosetta:
  "Import Schnittstelle Blueprint"    →  Canonical Input Channel
  "ID-Vergabe für ID-lose Objekte"    →  Identity Resolution Mechanism
  "OEF kann das nicht"                →  Tool Capability Constraint
  "Globaler Input Channel"            →  Single Entry Point Pattern
  "Master ID stabilisieren"           →  Identity Stabilization Pattern
  "Auch bekannte Objekte durch CSV"   →  Enforced Canonical Channel
  "Zyklus ID-stabil machen"           →  Identity Governance at Integration Layer
  "3rd Party Systeme"                 →  External System Integration

Bewertung:
  Architektonisch einer der stärksten Entscheide in R+MUNI.
  Keine Ausnahmen im Eingangskanal = konsequente Umsetzung
  von GOV 5.2 Integrationswahrheit.
  CSV07 xlsx_2_csv.py zeigt die bewusste Brücke zu XLSX-Quellen.


--------------------------------------------------------------------------------
FLOW 2 – XML-Scripts (Internal Integration Bus)
--------------------------------------------------------------------------------
Scripts:
  XML00  resolve_root.py
  XML01  collect_sources.py
  XML02  parse_child_xml.py
  XML03  build_index.py
  XML04  merge_master.py
  XML05  clear_merge.py
  XML06  finalize-master.py
  XML07  cleanup-artifacts.py

Intention:
  Interner Flow zwischen den Welten über OEF XML.
  Befüllt und verwaltet das master.xml aus OEF-Quellen.
  Zusätzlich undokumentierte Option: BPMN-Objekte die zuerst
  in Camunda entstanden sind können über CSV in den Zyklus
  zurückkehren — nur mit manuellem Eingriff zulässig um das
  Henne-Ei Problem zu vermeiden.

Norm-Begriff:
  Internal Integration Bus
  Canonical Exchange Format (OEF)
  Controlled Exception / Manual Gate

TOGAF Einordnung:
  Phase C/D — Integration Architecture
  Internal Data Flow Definition

Rosetta:
  "OEF XML stabiler Austausch"        →  Canonical Exchange Format
  "Interner Flow zwischen Welten"     →  Internal Integration Bus
  "BPMN Objekte zuerst in Camunda"    →  External System Origination
  "Nur manueller Eingriff"            →  Controlled Exception / Manual Gate
  "Henne-Ei Problem"                  →  Circular Dependency / Bootstrap Problem
  "Attribute ohne ID"                 →  Unresolved Identity Reference
  "cleanup-artifacts"                 →  Repository Hygiene Automation

Bewertung:
  Manual Gate ist eine bewusste Governance-Entscheidung —
  Automatisierung ist hier explizit unzulässig (GOV 7.2).
  XML05 clear_merge + XML07 cleanup entsprechen dem
  Transient Artifact Prinzip des master.xml.


--------------------------------------------------------------------------------
FLOW 3 – M2B-Scripts (Cross-Domain Transform)
--------------------------------------------------------------------------------
Scripts:
  M2B00  root_resolve.py
  M2B01  master_extract.py
  M2B02  activate_model.py
  M2B03  clear.py
  M2B04  reconcile_enrich.py

Intention:
  Master to BPMN 2.0 — Austausch zwischen OEF Business Prozess
  und BPMN 2.0 Welt.
  Trigger-gesteuert: bereitet BPMN 2.0 XML vor.
  Camunda Modeler reichert an — nur Norm-Felder erlaubt.
  Angereichertes BPMN XML kehrt zurück an master.xml.
  Script überträgt an CSV.
  BPMN Prozess-ID wird zur 3rd Party ID für ArchiMate —
  ermöglicht spätere Zusammenführung und Zyklus-Stabilität.

Norm-Begriff:
  Cross-Domain Identity Mapping
  Canonical to Domain Transform
  Event-Driven Integration
  Controlled Enrichment

TOGAF Einordnung:
  Phase C — Application & Information Architecture
  Cross-System Integration / Identity Federation

Rosetta:
  "Master to BPMN"                    →  Canonical to Domain Transform
  "Trigger-gesteuert"                 →  Event-Driven Integration
  "Nur Norm-Felder bereichern"        →  Controlled Enrichment / Schema Compliance
  "Zurück an master.xml"              →  Reverse Aggregation
  "BPMN ID → 3rd Party ID für Archi" →  Cross-Domain Identity Mapping
  "Stabil im Zyklus"                  →  Identity Continuity across Integration Cycles
  "reconcile_enrich"                  →  Reconciliation + Enrichment Pattern

Bewertung:
  "Nur Norm-Felder" in Camunda ist GOV 5.4 Überschreibung
  in der Praxis — explizit eingeschränkter manueller Eingriff.
  Cross-Domain Identity Mapping über BPMN Prozess-ID ist
  eine elegante Lösung für das domänenübergreifende
  Identitätsproblem.


--------------------------------------------------------------------------------
FLOW 4 – flow.py (Model-Driven Execution)
--------------------------------------------------------------------------------
Scripts:
  flow.py        (Script Runner / Orchestrator)
  flowmapping.txt (Trigger → Script Mapping)

Intention:
  Externer Script Flow — trigger-gesteuert aus BPMN 2.0
  Service Tasks oder ArchiMate Arbeitspaketen.
  flow.py liest seinen Ausführungskontext direkt aus
  master.xml, BPMN XML oder OEF XML.
  Verbindet Modell-Trigger mit Python Script Ausführung.
  Die Architektur selbst definiert was ausgeführt wird —
  nicht der Runner.

Norm-Begriff:
  Model-Driven Automation
  Lightweight Orchestrator
  Context-Driven Execution Engine

TOGAF Einordnung:
  Phase F/G — Architecture becomes Executable
  Implementation Governance

Rosetta:
  "Script Runner"                     →  Execution Engine / Orchestration Layer
  "BPMN Service Task als Trigger"     →  Service Task Invocation
  "Arbeitspaket als Trigger"          →  Work Package Execution Trigger
  "Holt Info aus master.xml"          →  Context-Driven Execution
  "Direkt aus BPMN/OEF Quellen"       →  Model-Driven Automation
  "flow.py als Runner"                →  Lightweight Orchestrator
  "flowmapping.txt"                   →  Trigger-to-Script Binding Registry

Bewertung:
  Das ist der Punkt wo R+MUNI von Dokumentation zu
  Ausführung wird — Architecture becomes Executable.
  Model-Driven Automation ist der heilige Gral von EA
  in der Praxis. R+MUNI hat das implementiert.


--------------------------------------------------------------------------------
jArchi-Scripts (In-Tool Validation)
--------------------------------------------------------------------------------
Scripts:
  jA01  Validierung Namen.ajs

Intention:
  Interner Qualitätscheck direkt in Archi.
  Prüft ob Objekte der Namenskonvention entsprechen.
  Gibt Ergebnis im Archi-Fenster aus.
  Verändert nichts — rein lesend.

Norm-Begriff:
  In-Tool Validation Script
  Naming Convention Compliance Check
  Non-Destructive Audit

TOGAF Einordnung:
  Phase G — Architecture Compliance Review
  Automated Governance Check

Rosetta:
  "Nur intern in Archi"               →  In-Tool Validation
  "Check Namenskonvention"            →  Naming Convention Compliance
  "Gibt im Fenster aus"               →  Validation Report / Audit Output
  "Sonst macht es nichts"             →  Read-Only / Non-Destructive Validation

Bewertung:
  GOV 8.3 Validierung in Reinform:
  deterministisch ✅  reproduzierbar ✅
  verändert nichts ✅  prüft Konformität ✅
  Automated Governance — Phase G TOGAF.


================================================================================
TEIL 3 – KONFIGURATIONSDATEIEN
================================================================================

  root.txt            →  Architecture Repository Root Definition
  context.txt         →  Execution Context Configuration
  child_mapping.txt   →  Source Folder Registry / Integration Scope
  mapping.txt         →  Canonical Filter / Transform Rules
  csvmapping.txt      →  CSV Field Mapping Configuration
  propmapping.txt     →  Property Filter Rules (global)
  flowmapping.txt     →  Trigger-to-Script Binding Registry
  run-scope.txt       →  Dynamic Scope Definition (Script Output)
  model-scope.txt     →  Model Availability Registry (Script Output)
  csvexport.txt       →  CSV Export Field Definition
  fields.csv          →  Field Schema Definition
  struktur.txt        →  Repository Structure Snapshot (Powershell)

Norm-Begriff gesamt:
  Architecture Configuration Artifacts
  Integration Mapping Registry

Bewertung:
  Alle Konfigurationsdateien sind explizit benannt und
  zweckgebunden — GOV 7.5 Script-Benennung eingehalten.
  run-scope.txt und model-scope.txt sind Script-Outputs —
  Transient Artifacts die den Zyklus steuern.


================================================================================
TEIL 4 – DOKUMENTATIONS-ARTEFAKTE
================================================================================

  Global GOV.pdf          →  Architecture Governance Framework (TOGAF Preliminary)
  How2Flow.txt            →  Architecture Definition Document (operational)
  How2Archi2CSVFlow.txt   →  Integration Procedure Document
  How2MasterXMLFlow.txt   →  Canonical Flow Documentation
  How2Master2BPMNProzess  →  Cross-Domain Transform Documentation
  SCRIPT-BAUKASTEN.txt    →  Solution Building Block Catalog
  Flow.txt                →  Flow Environment Description
  R+MUNI help files       →  Architecture Reference Documentation

Norm-Begriff gesamt:
  Architecture Definition Documents
  Solution Building Block Catalog
  Operational Procedures

TOGAF Einordnung:
  Phase B-D — Architecture Definition Documents
  Phase F — Solution Building Blocks
  Preliminary — Governance Framework

Bewertung:
  How2-Dateien sind operative Ableitungen der Architektur —
  abgeleitete Artefakte gemäß GOV 6.6.
  GOV.pdf ist führendes Artefakt gemäß GOV 6.3.


================================================================================
TEIL 5 – MODELL-REFERENZEN
================================================================================

  Aktives Modell <modelname>.archimate   →  Primary Architecture Repository
  Sub Modell <modelname>.archimate       →  Domain Sub-Model
  master.generated.xml                   →  Generated Canonical Artifact
  <Prozessname>.xml (BPMN)              →  Domain Process Model
  <modelname>.xlsx                       →  XLSX Integration Source
  archimate3_Diagram.xsd                 →  OEF Schema Reference
  archimate3_Model.xsd                   →  OEF Schema Reference
  archimate3_View.xsd                    →  OEF Schema Reference

Norm-Begriff gesamt:
  Architecture Repository Artifacts
  Schema Validation References

Bewertung:
  XSD-Files sind Norm-Referenzen — Schema Compliance Anchors.
  master.generated.xml ist Transient Artifact — wird verworfen.
  Aktives Modell ist führendes Artefakt — Source of Truth.


================================================================================
ZUSAMMENFASSUNG BLOCK 2
================================================================================

Script-Familien Übersicht:

  CSV-Scripts    →  Canonical Input Channel / Identity Stabilization   ✅
  XML-Scripts    →  Internal Integration Bus / OEF Exchange            ✅
  M2B-Scripts    →  Cross-Domain Transform / Event-Driven Integration  ✅
  flow.py        →  Model-Driven Automation / Lightweight Orchestrator ✅
  jArchi-Scripts →  In-Tool Validation / Naming Compliance             ✅

Kern-Architekturentscheide R+MUNI:

  1. Archi ist die einzige Identity Authority
     → Surrogate Key Pattern

  2. CSV ist der universelle Eingangskanal ohne Ausnahmen
     → Enforced Canonical Channel

  3. master.xml ist transient — kein dauerhafter Zustand
     → Transient Aggregation Hub

  4. Manual Gate für Bootstrap-Situationen
     → Controlled Exception (GOV-konform)

  5. flow.py macht Architektur ausführbar
     → Model-Driven Automation

  6. Alle Scripts haben genau eine Aufgabe
     → Single Responsibility (GOV 7.3/7.4)

Gesamtbewertung:
  R+MUNI implementiert eine vollständige Model-Driven
  Integration Architecture mit klarer Identity Governance.
  Alle Flows sind GOV-konform und architektonisch begründbar.
  Die Kombination aus Canonical Channel + Surrogate Key +
  Transient Hub ist ein anerkanntes Enterprise Integration Pattern.

Nächster Block:
  Block 3 — Begriffe und Konzepte → Offizielle Terminologie

================================================================================
ENDE BLOCK 2
================================================================================
