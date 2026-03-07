================================================================================
ROSETTA STONE – R+MUNI
Block 1: Views
================================================================================
Zweck dieses Dokuments:
Mapping zwischen R+MUNI internen Begriffen und der offiziellen
ArchiMate 3.2 / TOGAF Terminologie.

Erstellt: Dienstag, 03. März 2026
================================================================================


--------------------------------------------------------------------------------
VIE00 – Motivation View
--------------------------------------------------------------------------------
Intention:
  Warum existiert R+MUNI — und wie bin ich darauf gekommen.
  Output der eigenen Motivation als erstes Architekturartefakt.

Norm-Begriff:
  Motivation Viewpoint (ArchiMate 3.2 — offizieller Standard-Viewpoint)

Stakeholder:
  Ich selbst / zukünftige Investoren oder Partner

Zeigt:
  Driver → Assessment → Goal → Outcome
  Kausalkette vom Problem zur Lösung

TOGAF Einordnung:
  Input für Architecture Vision — Phase A

Rosetta:
  "Warum tue ich das überhaupt"   →  Driver + Assessment
  "Wie komme ich auf MUNI"        →  CourseOfAction → Outcome
  "Output meiner Motivation"      →  Architecture Vision Statement

Bewertung:
  Norm-konform. Intuitiv korrekt benannt und inhaltlich sauber befüllt.


--------------------------------------------------------------------------------
VIE01 – Strategy View
--------------------------------------------------------------------------------
Intention:
  Was habe ich zur Verfügung — und was ist notwendig um Funktionen
  bereitzustellen. Grob, ohne Tracing.

Norm-Begriff:
  Strategy Viewpoint (ArchiMate 3.2 — offizieller Standard-Viewpoint)

Stakeholder:
  Ich selbst / Geschäftsführungsebene

Zeigt:
  Resource + Capability → ValueStream
  Was vorhanden ist und was es ermöglicht

TOGAF Einordnung:
  Herzstück von Phase A und Preliminary
  Voraussetzung für jede Planungsaktivität

Rosetta:
  "Was hab ich zur Verfügung"     →  Resource + Capability
  "Was ist notwendig"             →  Capability Gap
  "Funktionen bereitstellen"      →  ValueStream Enablement
  "Grob ohne Tracing"             →  High-Level / Summary Viewpoint

Bewertung:
  Norm-konform. "Ohne Tracing" ist eine bewusste Abstraktion —
  in der Norm als Abstraction Level bezeichnet.


--------------------------------------------------------------------------------
VIE02 – Business View
--------------------------------------------------------------------------------
Intention:
  Herzstück des Verstehens für alles aus geschäftlicher Sicht.
  Schnittstelle zu BPMN 2.0. Verantwortlichkeiten und Leistungen
  für den Benutzer. Optisch am reifsten — wird am häufigsten mit
  Außenstehenden verwendet.

Norm-Begriff:
  Business Layer Viewpoint (composite / custom)
  Kein einzelner Standard-Viewpoint — bewusst kombiniert.
  In ArchiMate 3.2 als "Other Viewpoints" zulässig.

Stakeholder:
  Extern — Kunden, Geschäftsführer, Nicht-Techniker

Zeigt:
  BusinessProcess + BusinessRole + BusinessService + BusinessObject

TOGAF Einordnung:
  Architecture Communication View — Phase A
  Primärer Stakeholder-View für externe Kommunikation

Rosetta:
  "Herzstück des Verstehens"      →  Primary Business Architecture View
  "Geschäftliche Sicht"           →  Business Layer
  "Schnittstelle BPMN 2.0"        →  Process Interface / Choreography Boundary
  "Verantwortlichkeiten"          →  BusinessRole Assignment
  "Was bekommt der Benutzer"      →  BusinessService → Value Delivered
  "Optisch am reifsten"           →  Communication View / Stakeholder View

Bewertung:
  Bewusster Custom Viewpoint — explizit erlaubt in ArchiMate 3.2.
  Publikumsoptimiert statt norm-rein. In Phase A explizit gefordert.


--------------------------------------------------------------------------------
VIE03 – Application View
--------------------------------------------------------------------------------
Intention:
  Zeigt den Tool-Footprint der aktuell verwendet wird.
  Agnostisch in den Formaten — Tools müssen jedoch immer
  austauschbar sein. Aktueller Lock mit Archi ist dokumentiert
  und hat eine explizite Exit-Strategie.

Norm-Begriff:
  Application Layer Viewpoint (tailored)

Stakeholder:
  Ich selbst / technische Mitarbeiter

Zeigt:
  ApplicationComponent + ApplicationFunction + ApplicationInterface
  Baseline (As-Is) und implizite Target Architecture (To-Be)

TOGAF Einordnung:
  Phase C — Application Architecture
  Baseline Architecture + Architecture Roadmap Item (Exit-Strategie)

Rosetta:
  "Tool Footprint"                →  Application Landscape / Software Map
  "Agnostisch in Formaten"        →  Technology Independence Principle
  "Tools austauschbar"            →  Interoperability Requirement
  "Lock mit Archi"                →  Vendor Dependency / Binding Constraint
  "ID Handler Script als Exit"    →  Migration Path / Decommission Strategy
  "Aktuell verwendet"             →  Baseline Architecture (As-Is)

Bewertung:
  Enthält unbewusst zwei TOGAF-Konzepte gleichzeitig:
  Baseline Architecture + Target Architecture.
  Exit-Strategie ist ein Architecture Roadmap Item — Phase E.


--------------------------------------------------------------------------------
VIE04 – Technology View
--------------------------------------------------------------------------------
Intention:
  Kleiner aber stabiler Hardware-Footprint. Router, Internet und
  Zugang zu freien Normen sind notwendige Abhängigkeiten.
  Python und Ordnerstruktur bewusst hier abgebildet da sie
  keine Applikation im TOGAF-Sinne sind.

Norm-Begriff:
  Technology Layer Viewpoint

Stakeholder:
  Ich selbst / technische Einrichtung

Zeigt:
  Node + Device + SystemSoftware + CommunicationNetwork
  TechnologyFunction + Artifact (Scripts, Ordnerstruktur)

TOGAF Einordnung:
  Phase D — Technology Architecture

Rosetta:
  "HW Footprint"                  →  Technology Asset Catalog
  "Dev Rechner + Fritzbox"        →  Node + Device + CommunicationNetwork
  "Zugriff auf freie Normen"      →  External Service Dependency
  "Python + Ordnerstruktur"       →  System Software + Artifact
  "Keine App im TOGAF Sinne"      →  Technology Function vs Application Function

Bewertung:
  Korrekte Layer-Zuordnung — intuitiv erkannt ohne die Regel zu kennen.
  Leitfrage für künftige Imports:
  "Ist es eine App die einen Service erbringt — oder ein Baustein der läuft?"
  → Application Layer oder Technology Layer.


--------------------------------------------------------------------------------
VIE05 – Tracing Core Layer
--------------------------------------------------------------------------------
Intention:
  Tracing zwischen den Core Layern (Application, Technology).
  Zeigt wie technische Bausteine Applikationsfunktionen unterstützen
  und wie Applikationen Business-Funktionen realisieren.
  Aus iterativen Versuchen entstanden — historisch gewachsen.

Norm-Begriff:
  Implementation & Migration Viewpoint (partial)
  Technology Usage View

Stakeholder:
  Ich selbst / Architektur-Review

Zeigt:
  TechnologyFunction → ApplicationComponent → ApplicationFunction
  → BusinessFunction (cross-layer Realization + Serving)

TOGAF Einordnung:
  Phase B/C/D — Architecture Traceability
  Phase G — Architecture Compliance Review

Rosetta:
  "Tracing Core Layer"            →  Architecture Traceability Matrix
  "Historisch gewachsen"          →  Emergent Architecture
  "Iterative Versuche"            →  ADM Iteration Cycles

Hinweis Beziehungen:
  Verwendung von Association als Fallback wo normkonforme Beziehung
  nicht möglich — gemäß GOV 4.9 / 9.12 explizit zulässig.

Bewertung:
  Inhaltlich logisch und nachvollziehbar.
  Beziehungstypen teilweise als Association-Fallback — GOV-konform.


--------------------------------------------------------------------------------
VIE06 – Tracing Bus-Str-Mot Layer
--------------------------------------------------------------------------------
Intention:
  Minimales Tracing zwischen den oberen Layern:
  Motivation → Strategy → Business.
  Macht alles über alle Layer traceable.
  Bewusst getrennt von VIE05 um Überladung zu verhindern.

Norm-Begriff:
  Layered Viewpoint (ArchiMate 3.2)
  Motivation & Strategy Cross-Layer View

Stakeholder:
  Ich selbst / Architektur-Review / Zertifizierung

Zeigt:
  Driver → Goal → Capability → ValueStream → BusinessProcess
  Vertikale Kausalkette über drei Layer

TOGAF Einordnung:
  Phase A/B — Strategy to Business Traceability

Rosetta:
  "Minimal Tracing"               →  Filtered View / Focused Viewpoint
  "Motivation → Strategy → Bus."  →  Cross-Layer Traceability
  "Alles traceable"               →  End-to-End Architecture Traceability
  "Separat von VIE05"             →  Separation of Concerns im Viewpoint-Design

Bewertung:
  Bewusste Aufteilung in VIE05 + VIE06 ist sauberer als der
  ArchiMate Standard-Layered Viewpoint der alles in einem zeigt.


--------------------------------------------------------------------------------
VIE07 – Struktur View
--------------------------------------------------------------------------------
Intention:
  Lebendiges Inhaltsverzeichnis aller Scripts und Artefakte.
  Zeigt warum etwas existiert und ermöglicht Wiederverwendung
  vor Neuerstellung. Historisch gewachsen — Clearing geplant.

Norm-Begriff:
  Architecture Catalog View (custom)
  Solution Building Block Catalog (TOGAF)

Stakeholder:
  Ich selbst — Entwicklung und Wartung

Zeigt:
  Artifact + ApplicationFunction + DataObject
  Struktur, Zweck und Abhängigkeiten aller Scripts

TOGAF Einordnung:
  Phase F/G — Solution Building Blocks + Architecture Compliance

Rosetta:
  "Warum gibt es das"             →  Architecture Decision Record
  "Auf bestehendem aufbauen"      →  Building Block Reuse
  "Mapping 237492 verhindern"     →  Redundancy Control / Catalog Governance
  "Historisch gewachsen"          →  Technical Debt
  "Clearing sauber machen"        →  Consolidation Sprint (GOV Kapitel 10)

Bewertung:
  Direktes Pendant zum TOGAF Architecture Catalog.
  Geplantes Clearing ist ein valider Sprint-Auslöser
  gemäß GOV 10.4 — Fehlerbehebung durch Konsolidierung.


--------------------------------------------------------------------------------
Work View
--------------------------------------------------------------------------------
Intention:
  Bewusster Arbeits-Scratch-Pad direkt im Modell.
  Archi wird besser über Views als über den Baum bedient.
  Nach der Arbeit wird der View gelöscht — der Baum bleibt sauber.
  Kein VIE-Prefix bewusst gewählt um sich von echten Views abzuheben.

Norm-Begriff:
  Working View / Scratch View (kein offizieller Standard-Viewpoint)
  Transient Artifact

Stakeholder:
  Ich selbst — aktive Modellierungsarbeit

TOGAF Einordnung:
  Kein TOGAF-Artefakt — bewusste operative Ausnahme.
  Entspricht dem Konzept eines Transient Artifact in Phase E/F.

Rosetta:
  "Arbeitsraum"                   →  Working View / Scratch View
  "Anschließend löschen"          →  Transient Artifact
  "Baum bleibt sauber"            →  Repository Hygiene
  "Kein VIE-Prefix"               →  Explicit Non-Architectural Marker

Bewertung:
  Kein Norm-Verstoß — bewusste operative Entscheidung.
  Konsequente Anwendung des Transient-Prinzips das auch
  im Master XML und anderen Flows sichtbar ist.


================================================================================
ZUSAMMENFASSUNG BLOCK 1
================================================================================

Viewpoint-Übersicht:

  VIE00  Motivation View          →  Motivation Viewpoint            ✅ Norm-konform
  VIE01  Strategy View            →  Strategy Viewpoint              ✅ Norm-konform
  VIE02  Business View            →  Business Layer (custom)         ✅ Explizit erlaubt
  VIE03  Application View         →  Application Layer (tailored)    ✅ Norm-konform
  VIE04  Technology View          →  Technology Layer Viewpoint      ✅ Norm-konform
  VIE05  Tracing Core Layer       →  Technology Usage View           ✅ Norm-konform
  VIE06  Tracing Bus-Str-Mot      →  Layered Viewpoint               ✅ Sauberer als Standard
  VIE07  Struktur View            →  Architecture Catalog View       ✅ TOGAF-konform
  Work   Work View                →  Transient Working View          ✅ Bewusste Ausnahme

Gesamtbewertung:
  Alle 9 Views sind architektonisch begründet und verteidigbar.
  Keine ungeplanten Abweichungen von der Norm.
  Custom Viewpoints sind explizit dokumentiert und zulässig.
  Beziehungs-Fallbacks sind durch GOV 4.9 / 9.12 abgedeckt.

Nächster Block:
  Block 2 — Artifacts und Scripts → TOGAF Artefakte

================================================================================
ENDE BLOCK 1
================================================================================
