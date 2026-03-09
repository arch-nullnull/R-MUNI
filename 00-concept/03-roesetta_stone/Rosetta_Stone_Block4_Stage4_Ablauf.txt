================================================================================
ROSETTA STONE – R+MUNI
Block 4: Stage 4 Ablauf – TOGAF & ArchiMate Einordnung
================================================================================
Zweck dieses Dokuments:
Mapping zwischen den R+MUNI Stage-4-Aktivitäten und der offiziellen
TOGAF ADM / ArchiMate 3.2 Terminologie.
Lernziel: Verstehen wo Stage 4 im ADM sitzt und was die eigene
Arbeit in Normsprache bedeutet.

Erstellt: 2026-03-09
================================================================================


--------------------------------------------------------------------------------
STAGE 4 GESAMT – Was ist das in TOGAF?
--------------------------------------------------------------------------------
R+MUNI Originalton:
  "Controlled Application & Systemic Enablement"
  Stage 4 = realer Einsatz des in Stage 3 fixierten Systems,
  mit kontrollierten Erweiterungen und striktem Rückkopplungsschutz.

Norm-Begriff:
  Transition Architecture Phase (TOGAF ADM Phase E/F)
  Architecture Realization

TOGAF Einordnung:
  Phase E — Opportunities & Solutions
    → Identifikation was gebaut / integriert werden muss
    → Transition Architecture Definition
  Phase F — Migration Planning
    → Priorisierung der Umsetzungsschritte
    → Incremental Delivery Planning
  Phase G — Implementation Governance
    → Sicherstellung dass Umsetzung architekturkonform bleibt
    → Architecture Compliance Reviews

Rosetta:
  "Controlled Application"            →  Governed Implementation
  "Systemic Enablement"               →  Architecture Realization
  "Stage 3 Freeze als Basis"          →  Baseline Architecture (fixiert)
  "Stage 4 Erweiterungen additiv"     →  Incremental Transition Architecture
  "Rückkopplungsschutz"               →  Architecture Governance / Compliance
  "Kein Eingriff in Stage-3-Logik"    →  Baseline Integrity Principle

Bewertung:
  Stage 4 ist klassisches ADM Phase E/F/G —
  Transition Planning + Governed Delivery.
  Der Rückkopplungsschutz ist Architecture Governance in Reinform.


--------------------------------------------------------------------------------
FLW-REIHE – Scriptrunner, Discover, Map Elements
--------------------------------------------------------------------------------
R+MUNI Originalton:
  "Scriptrunner für Default-Flow-Abläufe —
   Entlastung im Alltag, nicht Verstecken von Logik."

Norm-Begriff:
  Automation of Architecture Governance Processes
  Architecture Building Block (ABB) — Operational

TOGAF Einordnung:
  Phase G — Implementation Governance
    → Automatisierte Prüfung ob Abläufe architekturkonform ausgeführt werden
  Phase F — Migration Planning
    → Default Flows als Incremental Delivery Units

ArchiMate Einordnung:
  ApplicationComponent    →  FLW00 Scriptrunner als ausführende Komponente
  ApplicationFunction     →  Trigger-Erkennung, Mapping-Auflösung, Ausführung
  ApplicationProcess      →  Der gesteuerte Ablauf (Flow) selbst
  Artifact                →  flowtriggers.txt, flowmapping.txt als Steuerungsartefakte
  TechnologyFunction      →  Python Runtime als Ausführungsebene

Rosetta:
  "Scriptrunner"                      →  Orchestration Engine (Application Layer)
  "Default Flow"                      →  Standardized Execution Path
  "flowtriggers.txt"                  →  Trigger Rule Catalog (Architecture Artifact)
  "flowmapping.txt"                   →  Service Mapping Catalog (Architecture Artifact)
  "Entlastung im Alltag"              →  Operational Efficiency durch Automation
  "Logik bleibt sichtbar"             →  Transparency Principle / No Black Box

Bewertung:
  Der Scriptrunner ist eine Orchestration Engine auf Application Layer.
  Die txt-Steuerungsdateien sind Architecture Catalogs —
  sie dokumentieren und steuern gleichzeitig.
  Das ist ein elegantes Beispiel für Architecture as Code.


--------------------------------------------------------------------------------
HLP09 – Report Server
--------------------------------------------------------------------------------
R+MUNI Originalton:
  "Lokaler Webserver für Archi HTML Reports —
   mehrere Reports gleichzeitig, kein Cloud-Zwang."

Norm-Begriff:
  Architecture Communication Infrastructure
  Stakeholder Engagement Enablement

TOGAF Einordnung:
  Phase A — Architecture Vision (Kommunikationsmittel)
    → Reports sind das primäre Stakeholder-Kommunikationsartefakt
  Phase G — Implementation Governance
    → Reports ermöglichen Architecture Compliance Checks

ArchiMate Einordnung:
  ApplicationComponent    →  HLP09 als lokaler HTTP-Server
  ApplicationService      →  Report-Bereitstellung als Service
  DataObject              →  Archi HTML Report (index.html + Assets)
  Node                    →  Lokaler Rechner als Hosting-Umgebung
  CommunicationNetwork    →  Lokales Netzwerk (LAN) als Verteilungskanal
  Artifact                →  webconfig.txt als Konfigurationsartefakt

Rosetta:
  "Lokaler Webserver"                 →  On-Premise Application Service
  "Mehrere Reports gleichzeitig"      →  Multi-Instance Service Delivery
  "webconfig.txt"                     →  Service Configuration Artifact
  "Kein Cloud-Zwang"                  →  Deployment Independence Principle
  "Im lokalen Netzwerk erreichbar"    →  LAN-based Service Distribution
  "Archi HTML Report"                 →  Architecture Communication Artifact

Bewertung:
  HLP09 löst ein klassisches Phase-A-Problem:
  Wie bekomme ich Architektur-Inhalte zu Stakeholdern
  ohne externe Abhängigkeiten?
  Die Antwort ist tool-agnostisch, einfach und reproduzierbar.
  In TOGAF-Sprache: Lightweight Architecture Communication Infrastructure.


--------------------------------------------------------------------------------
ATL-REIHE – Atlassian Integration
--------------------------------------------------------------------------------
R+MUNI Originalton:
  "ArchiMate-Objekte aus master.xml in Jira verlinkbar machen —
   ohne kostenpflichtige Features, vollständig auf Free-Tier."

Norm-Begriff:
  Architecture Repository Integration
  Cross-Tool Traceability
  Federated Architecture Management

TOGAF Einordnung:
  Phase B — Business Architecture
    → Jira-Tickets als Business Process Instances sichtbar machen
  Phase C — Application Architecture
    → Integration zwischen Archi (EA-Tool) und Jira (Ticket-System)
  Phase G — Implementation Governance
    → Traceability zwischen EA-Objekten und konkreten Aufgaben

ArchiMate Einordnung:
  ApplicationComponent    →  ATL00/01/02 als Integrations-Scripts
  ApplicationInterface    →  CSV als Austauschformat zwischen Systemen
  DataObject              →  ATL CSV, Jira CSV als Transferartefakte
  BusinessObject          →  ArchiMate-Element (Layer + Typ) als fachliches Objekt
  ApplicationService      →  Jira als empfangender Service

Rosetta:
  "master.xml als Quelle"             →  Canonical Data Source
  "ATL CSV"                           →  Canonical Transfer Object
  "Jira CSV"                          →  Target System Import Format
  "Layer = Komponente in Jira"        →  Architecture Domain Mapping
  "ArchiType = Stichwort in Jira"     →  Architecture Element Classification
  "Free-Tier only"                    →  Constraint-driven Architecture Decision
  "Kein kostenpflichtiges Feature"    →  Vendor Independence Principle

Bewertung:
  Die ATL-Reihe realisiert Cross-Tool Traceability —
  eines der anspruchsvollsten Ziele in Enterprise Architecture.
  Archi-Objekte werden in Jira sichtbar ohne direkten API-Zugriff.
  Das ist Federation über CSV — pragmatisch, robust, normkonform.


--------------------------------------------------------------------------------
BOC EXIT POINT – BPMN / OEF Export
--------------------------------------------------------------------------------
R+MUNI Originalton:
  "BPMN 2.0 und ArchiMate OEF direkt importierbar in
   ADONIS und ADOIT (BOC-Group) — validiert."

Norm-Begriff:
  Architecture Portability Validation
  Interoperability Proof-of-Concept
  Open Standard Compliance

TOGAF Einordnung:
  Phase E — Opportunities & Solutions
    → Exit-Strategie aus R+MUNI in Enterprise-Tools validiert
  Phase H — Architecture Change Management
    → Migration Path zu größeren EA-Tools bei Bedarf nachgewiesen

ArchiMate Einordnung:
  Artifact                →  BPMN XML, OEF XML als portable Artefakte
  ApplicationInterface    →  Standardisierte Export-Schnittstellen
  ApplicationComponent    →  ADONIS, ADOIT als Ziel-Systeme

Rosetta:
  "Exit Point"                        →  Migration Path / Decommission Strategy
  "BPMN 2.0 Export validiert"         →  Open Standard Compliance (OMG BPMN)
  "OEF Export validiert"              →  Open Standard Compliance (ArchiMate OEF)
  "Importierbar in ADONIS"            →  Interoperability Validated
  "Importierbar in ADOIT"             →  Interoperability Validated
  "Kein Round-Trip"                   →  Uni-directional Integration (by design)
  "Tool-Agnostik nachgewiesen"        →  Vendor Neutrality Principle

Bewertung:
  Der BOC Exit Point beweist das Kernversprechen von R+MUNI:
  Tool-Agnostik ist kein Wunsch — es ist eine validierte Eigenschaft.
  In TOGAF-Sprache: Architecture Portability ist demonstriert.
  Ein Architecture Decision Record (ADR) der sich selbst beweist.


--------------------------------------------------------------------------------
BETA-EINSATZ – Erster externer Anwender
--------------------------------------------------------------------------------
R+MUNI Originalton:
  "Erster Beta-Kunde hat R+MUNI installiert —
   Einsatz unter realen Bedingungen außerhalb der Entwicklungsumgebung."

Norm-Begriff:
  Architecture Pilot / Proof of Value
  Transition from Development to Operations (Dev-to-Ops)
  Architecture Socialization

TOGAF Einordnung:
  Phase G — Implementation Governance
    → Erster realer Compliance-Check unter Produktivbedingungen
  Phase H — Architecture Change Management
    → Feedbackschleife aus realem Betrieb öffnet sich
  Phase A (nächster Zyklus) — Architecture Vision
    → Kundenfeedback informiert nächste ADM-Iteration

ArchiMate Einordnung:
  BusinessActor           →  Beta-Kunde als externer Stakeholder
  BusinessRole            →  Anwender / Tester / Feedback-Geber
  BusinessProcess         →  Installation, Konfiguration, erster Betrieb
  BusinessEvent           →  "Erster externer Einsatz" als Architektur-Meilenstein

Rosetta:
  "Beta-Kunde"                        →  Early Adopter / Architecture Pilot User
  "Außerhalb der Entwicklungsumgebung" →  Production Environment (Baseline)
  "Reale Bedingungen"                 →  Architecture in Operations
  "Expliziter Hinweis auf Beta-Status" →  Risk Communication / Stakeholder Transparency
  "Installiert und läuft"             →  Proof of Value Achieved

Bewertung:
  Der Beta-Einsatz ist in TOGAF der Moment wo
  Transition Architecture zur Baseline Architecture wird.
  Stage 4 endet mit einem validierten Proof of Value —
  das ist der stärkste mögliche Abschluss einer ADM-Phase.


--------------------------------------------------------------------------------
STAGE 4 FREEZE – Was ist das in TOGAF?
--------------------------------------------------------------------------------
R+MUNI Originalton:
  "Der Freeze erklärt den aktuellen Zustand als
   gültigen, tragfähigen Referenzzustand."

Norm-Begriff:
  Architecture Baseline Update
  Transition Architecture → neue Baseline Architecture
  Architecture Repository Snapshot

TOGAF Einordnung:
  Ende Phase G / Übergang zu neuem ADM-Zyklus
    → Die Transition Architecture von Stage 4 wird zur neuen Baseline
    → Architecture Repository wird aktualisiert
    → Nächster ADM-Zyklus (Stage 5) startet auf dieser Basis

ArchiMate Einordnung:
  Plateau                 →  Stage 4 Freeze = Architecture Plateau
  (ArchiMate Implementation & Migration Layer)
  Ein Plateau ist ein stabiler Zustand zwischen zwei Transitions.

Rosetta:
  "Freeze"                            →  Architecture Baseline / Plateau
  "Referenzzustand"                   →  Normative Baseline Architecture
  "Rückkopplungsschutz bestätigt"     →  Architecture Integrity Validated
  "Stage 3 bleibt unangetastet"       →  Baseline Preservation Principle
  "Übergang zu Stage 5"               →  ADM Cycle Transition


================================================================================
ZUSAMMENFASSUNG BLOCK 4
================================================================================

Stage 4 Aktivitäten in TOGAF/ArchiMate:

  FLW-Reihe         →  Orchestration Engine + Architecture Catalogs    Phase F/G
  HLP09             →  Architecture Communication Infrastructure        Phase A/G
  ATL-Reihe         →  Cross-Tool Traceability via CSV Federation       Phase B/C/G
  BOC Exit Point    →  Architecture Portability Validation              Phase E/H
  Beta-Einsatz      →  Proof of Value / Dev-to-Ops Transition           Phase G/H
  Stage 4 Freeze    →  Architecture Baseline / Plateau                  Ende Phase G

ADM Phasen die Stage 4 dominieren:
  Phase E  Opportunities & Solutions    →  Was wird gebaut / integriert
  Phase F  Migration Planning           →  Schrittweise Umsetzung
  Phase G  Implementation Governance   →  Architekturkonformität sichern
  Phase H  Architecture Change Mgmt    →  Feedback aus Betrieb aufnehmen

Gesamtbewertung:
  Stage 4 ist ein vollständiger ADM-Durchlauf der Phasen E bis H.
  Alle Aktivitäten sind architektonisch begründet und normkonform.
  Der Beta-Einsatz als Abschluss ist ein Lehrbuchbeispiel für
  Architecture Realization — vom Modell zur gelebten Realität.

Nächster Block:
  Block 5 — Stage 5 Ziele und organisatorisches Wachstum in TOGAF-Sprache

================================================================================
ENDE BLOCK 4
================================================================================
