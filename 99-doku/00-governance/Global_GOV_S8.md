================================================================================
R+MUNI GLOBAL GOVERNANCE
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : Global_GOV
Tag             : #gov #global #rmuni
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Letzte Änderung : 2026-03-27 — S8-Update: Kap. 10 erweitert, Kap. 13 Terminologie, Kap. 14+15 neu | zuvor: 2026-03-26 Header S8-konform | 2026-03-18 Stage 5 Erweiterung (Kapitel 13)
Erstellt durch  : Markus Resel + Claude (Pair-Session)
================================================================================


--------------------------------------------------------------------------------
1. ZWECK, INTENTION UND CHARAKTER DER GOVERNANCE
--------------------------------------------------------------------------------

1.1 Zweck dieser Governance
-----------------------------
Diese Governance definiert die verbindlichen Regeln, Prinzipien und Leitplanken
für das Blueprint-Projekt.

Ziel dieser Governance ist es:
- ein konsistentes, langfristig stabiles Architektur- und Integrationsmodell
  zu ermöglichen
- explizite, nachvollziehbare und auditfähige Entscheidungen sicherzustellen
- implizite Annahmen, verdeckte Logik und stillschweigende Abweichungen
  systematisch auszuschließen
- ein bewusstes Lern- und Reifemodell für Architektur-, Integrations- und
  Automatisierungsdisziplin zu etablieren

Diese Governance ist kein Begleitdokument, sondern integraler Bestandteil
des Blueprint-Systems.


1.2 Charakter des Blueprint-Projekts
--------------------------------------
Das Blueprint-Projekt ist bewusst als Lern- und Reifeprojekt konzipiert.

Es verfolgt nicht das Ziel, kurzfristig maximale Effizienz zu erreichen,
sondern:
- strukturelle Klarheit aufzubauen
- langfristige Stabilität zu sichern
- disziplinierte Modellierung zu erlernen und zu verankern
- die Konsequenzen expliziter Governance erfahrbar zu machen

Lerninhalte, Reifezustände und bewusste Einschränkungen sind daher kein
Nebenprodukt, sondern Teil der Governance.


1.3 Governance als Lerninstrument
-----------------------------------
Governance wird in diesem Projekt nicht als Kontrollmechanismus verstanden,
sondern als Lerninstrument.

Sie dient dazu:
- Denkdisziplin zu erzwingen
- implizite Abkürzungen sichtbar zu machen
- Modellierungs- und Integrationsfehler frühzeitig zu erkennen
- langfristige Auswirkungen von Entscheidungen nachvollziehbar zu machen

Die Strenge der Governance ist bewusst gewählt und Teil des Lernziels.


1.4 Abgrenzung zu Prozess- und Projektgovernance
--------------------------------------------------
Diese Governance ist:
- keine Projektmanagement-Governance
- keine Prozessbeschreibung
- keine Rollen- oder Verantwortlichkeitsdefinition

Sie definiert ausschließlich:
- was modelliert, integriert und automatisiert werden darf
- wie Identität, Führung und Ableitung zu erfolgen haben
- welche Regeln unveränderlich gelten

Organisatorische oder operative Prozesse sind nicht Bestandteil dieser
Governance.


1.5 Verbindlichkeit und Geltungsbereich
-----------------------------------------
Diese Governance gilt verbindlich für:
- alle Architektur-, Integrations- und Automatisierungsartefakte
- alle Modellierungs-, Synchronisations- und Re-Materialisierungsprozesse
- alle manuellen und automatisierten Eingriffe in das Blueprint-System

Es existieren keine governance-freien Bereiche.


1.6 Explizitheit als Grundprinzip
-----------------------------------
Ein zentrales Ziel dieser Governance ist die vollständige Explizitheit aller
relevanten Entscheidungen.

Für das gesamte Blueprint-System gilt:
- Entscheidungen werden explizit getroffen
- Regeln werden explizit formuliert
- Abweichungen werden explizit dokumentiert
- Ableitungen erfolgen explizit

Implizite Logik ist unzulässig.


1.7 Langfristige Perspektive
------------------------------
Diese Governance ist auf langfristige Nutzung ausgelegt.

Sie priorisiert:
- Stabilität über Komfort
- Nachvollziehbarkeit über Geschwindigkeit
- Disziplin über kurzfristige Optimierung

Kurzfristige Vereinfachungen rechtfertigen keine Abweichungen von den
definierten Regeln.


1.8 Abschluss des Kapitels
----------------------------
Dieses Kapitel definiert Zweck, Intention und Charakter der Governance des
Blueprint-Projekts.

Die folgenden Kapitel konkretisieren diese Intention in Form von:
- Begriffsklärungen
- Architektur- und Modellprinzipien
- Integrations- und Ableitungslogik
- verbindlichen Regeln und Hard Facts


--------------------------------------------------------------------------------
2. GRUNDBEGRIFFE UND ABGRENZUNGEN
--------------------------------------------------------------------------------

2.1 Zweck dieses Kapitels
---------------------------
Dieses Kapitel definiert die grundlegenden Begriffe und Abgrenzungen, die für
das Verständnis und die korrekte Anwendung dieser Governance erforderlich sind.

Ziel ist es:
- Mehrdeutigkeiten zu vermeiden
- implizite Interpretationen auszuschließen
- eine einheitliche Lesart aller folgenden Kapitel sicherzustellen

Alle Begriffe werden normativ verwendet.


2.2 Objekt
-----------
Ein Objekt ist eine eindeutig identifizierbare Einheit innerhalb des
Blueprint-Systems.

Ein Objekt:
- besitzt eine stabile Identität
- existiert unabhängig von Darstellung, Tool oder Format
- kann in unterschiedlichen Artefakten repräsentiert werden

Ein Objekt ist nicht gleichzusetzen mit seiner visuellen Darstellung oder
seinem technischen Vorkommen.


2.3 Identität
--------------
Die Identität eines Objekts beschreibt dessen eindeutige und dauerhafte
Existenz.

Für die Identität gilt:
- sie ist unabhängig von Name, Typ oder Darstellung
- sie bleibt über alle Iterationen hinweg stabil
- sie ist die Grundlage aller Integrations- und Ableitungsprozesse

Identität ist nicht interpretierbar.


2.4 Objekt-ID
--------------
Die Objekt-ID ist die technische Repräsentation der Identität eines Objekts.

Für die Objekt-ID gilt:
- sie ist eindeutig
- sie ist stabil
- sie ist repository-weit gültig
- sie ist der alleinige Referenzanker für Integration und Automatisierung

Objektnamen oder Tool-IDs ersetzen keine Objekt-ID.


2.5 Name
---------
Der Name eines Objekts dient der menschlichen Lesbarkeit und Wiedererkennung.

Für den Namen gilt:
- er ist nicht identitätsstiftend
- er kann geändert werden, ohne die Identität zu verändern
- er enthält keine implizite Semantik

Der Name ist ein Hilfsmittel, kein Steuerungsinstrument.


2.6 Semantik
-------------
Semantik beschreibt die fachliche Bedeutung eines Objekts.

Semantik:
- ist explizit zu dokumentieren
- ist nicht Bestandteil der Identität
- darf nicht implizit aus Namen, Typen oder Beziehungen abgeleitet werden

Semantik entsteht durch Beschreibung, nicht durch Interpretation.


2.7 Führung
------------
Führung beschreibt, welche Quelle für eine Information verbindlich ist.

Für Führung gilt:
- sie wird explizit festgelegt
- sie kann feldgenau variieren
- sie ist nicht implizit

Ohne explizite Führungsdefinition existiert keine Führung.


2.8 Integration
----------------
Integration bezeichnet die kontrollierte Zusammenführung von Informationen
aus unterschiedlichen Quellen.

Integration:
- erfolgt regelbasiert
- ist deterministisch
- ist reproduzierbar
- respektiert die definierte Führungslogik

Integration ist kein Zusammenkopieren von Daten.


2.9 Ableitung
--------------
Ableitung beschreibt die Überführung von Architektur- oder
Integrationsinformationen in andere Artefakte oder Formate.

Für Ableitung gilt:
- sie ist explizit definiert
- sie ist nachvollziehbar
- sie erzeugt keine neue Identität
- sie wirkt nicht rück auf die Quelle

Ableitung ist keine Interpretation.


2.10 Rückwirkung
-----------------
Rückwirkung bezeichnet jede Veränderung eines führenden Artefakts durch ein
abgeleitetes Artefakt.

Rückwirkungen sind grundsätzlich unzulässig, sofern sie nicht explizit
geregelt sind.


2.11 Reife und Lernen
----------------------
Reife beschreibt den Grad der Disziplin, Explizitheit und Stabilität im
Umgang mit dem Blueprint-System.

Lernen ist integraler Bestandteil dieser Governance und umfasst:
- das bewusste Einhalten von Regeln
- das Erkennen von Abkürzungen und impliziten Annahmen
- das Verstehen langfristiger Konsequenzen

Reife entsteht durch Anwendung der Governance, nicht durch Umgehung.


2.12 Implizit vs. Explizit
---------------------------
Implizit bedeutet:
- nicht dokumentiert
- nicht nachvollziehbar
- interpretationsabhängig

Explizit bedeutet:
- klar formuliert
- dokumentiert
- reproduzierbar

Diese Governance bevorzugt explizite Lösungen in allen Fällen.


2.13 Abschluss des Kapitels
-----------------------------
Dieses Kapitel definiert die grundlegenden Begriffe und Abgrenzungen für das
Blueprint-Governance-System.

Alle folgenden Kapitel setzen diese Definitionen voraus und verwenden die
Begriffe ausschließlich in diesem Sinne.


--------------------------------------------------------------------------------
3. GOVERNANCE-VERSTÄNDNIS UND REGELCHARAKTER
--------------------------------------------------------------------------------

3.1 Zweck dieses Kapitels
---------------------------
Dieses Kapitel definiert das grundlegende Verständnis von Governance innerhalb
des Blueprint-Projekts.

Ziel ist es:
- den Charakter der Governance eindeutig festzulegen
- Missverständnisse über Rolle, Reichweite und Verbindlichkeit auszuschließen
- klarzustellen, dass Governance in diesem Projekt bewusst Teil des Lern- und
  Reifemodells ist

Dieses Kapitel beschreibt wie Governance zu verstehen ist, nicht wie sie
umgesetzt wird.


3.2 Governance als Regelwerk
------------------------------
Governance wird in diesem Projekt als verbindliches Regelwerk verstanden.

Governance:
- definiert zulässige und unzulässige Zustände
- legt unveränderliche Prinzipien fest
- begrenzt den Lösungsraum bewusst
- ist unabhängig von Werkzeugen, Technologien oder Organisationsformen

Governance ist kein Prozess, keine Empfehlung und keine Sammlung von
Best Practices.


3.3 Normativer Charakter
-------------------------
Alle in dieser Governance definierten Regeln sind normativ.

Das bedeutet:
- sie sind verbindlich
- sie gelten unabhängig von Kontext oder Bequemlichkeit
- sie sind nicht optional
- sie sind nicht interpretationsabhängig

Abweichungen sind nur zulässig, wenn sie explizit geregelt sind.


3.4 Governance als Bestandteil des Lern- und Reifemodells
----------------------------------------------------------
Das Blueprint-Projekt ist bewusst als Lern- und Reifeprojekt angelegt.

Governance ist dabei:
- kein externes Kontrollinstrument
- kein nachgelagerter Qualitätssicherungsmechanismus
- sondern integraler Bestandteil des Lernziels

Die Anwendung der Governance dient dazu, Disziplin, Explizitheit und
langfristiges Denken zu erlernen und zu verankern.


3.5 Bewusste Einschränkung als Gestaltungsprinzip
--------------------------------------------------
Die Governance schränkt bewusst ein.

Diese Einschränkungen dienen dazu:
- implizite Abkürzungen zu verhindern
- verdeckte Komplexität sichtbar zu machen
- langfristige Auswirkungen von Entscheidungen erfahrbar zu machen

Einschränkungen sind kein Mangel, sondern ein zentrales Gestaltungsmittel
dieses Projekts.


3.6 Umgang mit Abweichungen
-----------------------------
Abweichungen von Governance-Regeln sind grundsätzlich unerwünscht.

Sofern Abweichungen zugelassen sind, gelten folgende Grundsätze:
- Abweichungen müssen explizit benannt werden
- Abweichungen müssen nachvollziehbar begründet sein
- Abweichungen erzeugen keine Präzedenzwirkung

Implizite oder stillschweigende Abweichungen sind unzulässig.


3.7 Keine implizite Weiterentwicklung
--------------------------------------
Diese Governance entwickelt sich nicht implizit weiter.

Das bedeutet:
- neue Regeln entstehen nicht durch Gewohnheit
- neue Standards entstehen nicht durch Wiederholung
- neue Bedeutungen entstehen nicht durch Interpretation

Änderungen erfolgen ausschließlich durch bewusste, explizite Entscheidungen.


3.8 Verhältnis von Erklärung und Regel
----------------------------------------
Diese Governance enthält sowohl erklärende als auch regelsetzende Inhalte.

Dabei gilt:
- erklärende Inhalte dienen dem Verständnis und der Lernintention
- regelsetzende Inhalte sind verbindlich und nicht verhandelbar

Beide sind gleichwertige Bestandteile dieser Governance.


3.9 Abschluss des Kapitels
----------------------------
Dieses Kapitel definiert das grundlegende Governance-Verständnis des
Blueprint-Projekts.

Die folgenden Kapitel konkretisieren dieses Verständnis in Form von:
- Architektur- und Modellprinzipien
- Integrations- und Ableitungslogik
- Artefaktrollen
- Automatisierungs- und Validierungsregeln
- expliziten Hard Facts


--------------------------------------------------------------------------------
4. ARCHITEKTUR- UND MODELLPRINZIPIEN
--------------------------------------------------------------------------------

4.1 Zweck dieses Kapitels
---------------------------
Dieses Kapitel definiert die grundlegenden Architektur- und Modellprinzipien
des Blueprint-Systems.

Ziel ist es:
- eine konsistente und langfristig stabile Modellstruktur sicherzustellen
- explizite, nachvollziehbare Modellierungsentscheidungen zu erzwingen
- implizite Semantik, verdeckte Logik und tool-spezifische Abhängigkeiten
  auszuschließen
- Architekturdisziplin als bewusstes Lern- und Reifeziel zu verankern

Die hier definierten Prinzipien gelten systemweit.


4.2 Identitätsprimat
---------------------
Die Identität eines Objekts ist das zentrale Ordnungsprinzip des
Blueprint-Systems.

Für das Identitätsprimat gilt:
- Identität ist unabhängig von Name, Typ oder Darstellung
- Identität ist über alle Artefakte hinweg stabil
- Identität ist Grundlage aller Integrations- und Ableitungsprozesse

Alle Architektur- und Modellentscheidungen haben die Identität zu
respektieren.


4.3 Trennung von Struktur, Semantik und Darstellung
-----------------------------------------------------
Das Blueprint-System trennt strikt zwischen:
- Struktur (Objekte, Beziehungen, Rollen)
- Semantik (fachliche Bedeutung, Beschreibung)
- Darstellung (Visualisierung, Tool-spezifische Repräsentation)

Diese Trennung ist verbindlich und darf nicht aufgehoben werden.

Semantik darf nicht aus Struktur oder Darstellung implizit abgeleitet werden.


4.4 Explizitheit als Modellierungsprinzip
------------------------------------------
Alle relevanten Modellierungsentscheidungen sind explizit zu treffen.

Für das Modell gilt:
- keine impliziten Annahmen
- keine verdeckte Logik
- keine stillschweigende Interpretation

Explizitheit ist Voraussetzung für Nachvollziehbarkeit, Integration und
Automatisierung.


4.5 Determinismus
------------------
Das Blueprint-System ist deterministisch aufgebaut.

Das bedeutet:
- gleiche Eingaben führen zu gleichen Ergebnissen
- Integrations- und Ableitungsprozesse sind reproduzierbar
- Modellzustände sind eindeutig bestimmbar

Nicht-deterministisches Verhalten ist unzulässig.


4.6 Langfristige Stabilität
-----------------------------
Architektur- und Modellentscheidungen sind auf langfristige Stabilität
ausgelegt.

Dabei gilt:
- kurzfristige Vereinfachungen rechtfertigen keine strukturellen Kompromisse
- Komfort ist kein Architekturprinzip
- Stabilität hat Vorrang vor Geschwindigkeit

Dieses Prinzip ist bewusst Teil des Lern- und Reifeziels.


4.7 Tool-Unabhängigkeit
------------------------
Das Blueprint-Modell ist unabhängig von konkreten Werkzeugen oder Plattformen.

Für die Modellierung gilt:
- keine Tool-Semantik im Architekturmodell
- keine impliziten Tool-Abhängigkeiten
- keine Vermischung von Architektur und Ausführung

Werkzeuge dienen der Umsetzung, nicht der Definition der Architektur.


4.8 Architektur als Referenz, nicht als Ausführung
----------------------------------------------------
Architekturmodelle beschreiben:
- Struktur
- Rollen
- Beziehungen

Sie beschreiben nicht:
- Ausführungslogik
- technische Steuerung
- Laufzeitverhalten

Die Architektur ist Referenz, nicht Implementierung.


4.9 Beziehungsprimat der Objektstabilität
------------------------------------------
Die Stabilität von Objekten hat Vorrang vor der Präzision von Beziehungen.

Für Beziehungen gilt:
- Objekttypen werden nicht geändert um Beziehungen zu ermöglichen
- Ist keine normkonforme Beziehung zwischen zwei Objekten möglich, ist
  Association als normkonformer Fallback zulässig
- Beziehungstypen werden nicht semantisch überladen um fehlende
  Beziehungstypen zu kompensieren
- Import-Regelwerk definiert Objekttypen fix — kontextabhängige
  Uminterpretation eines Objekttyps ist unzulässig

Dieses Prinzip macht die Grenzen der ArchiMate-Norm sichtbar ohne die
Objektstabilität zu opfern.


4.10 Lern- und Reifeaspekt der Architekturprinzipien
-----------------------------------------------------
Die Einhaltung dieser Architektur- und Modellprinzipien ist bewusst Teil des
Lern- und Reifemodells.

Sie dient dazu:
- diszipliniertes Denken zu fördern
- langfristige Auswirkungen von Architekturentscheidungen sichtbar zu machen
- implizite Abkürzungen zu erkennen und zu vermeiden

Verstöße gegen diese Prinzipien untergraben das Lernziel des Projekts.


4.11 Abschluss des Kapitels
-----------------------------
Dieses Kapitel definiert die verbindlichen Architektur- und Modellprinzipien
des Blueprint-Systems.

Die folgenden Kapitel konkretisieren diese Prinzipien in Form von:
- Integrations- und Führungslogik
- Artefaktrollen und Ebenentrennung
- Automatisierungs- und Ableitungsregeln
- verbindlichen Hard Facts


--------------------------------------------------------------------------------
5. INTEGRATION, FÜHRUNG UND ABLEITUNG
--------------------------------------------------------------------------------

5.1 Zweck dieses Kapitels
---------------------------
Dieses Kapitel definiert die verbindlichen Regeln für Integration, Führung und
Ableitung innerhalb des Blueprint-Systems.

Es legt fest:
- wie Informationen zusammengeführt werden
- welche Quelle für welche Information verbindlich ist
- wie Ableitungen erfolgen dürfen
- welche Rückwirkungen ausgeschlossen sind

Integration und Ableitung sind zentrale Mechanismen des Blueprint-Systems und
unterliegen strikter Governance.


5.2 Integrationswahrheit
-------------------------
Für jede Information im Blueprint-System existiert genau eine
Integrationswahrheit.

Das bedeutet:
- jede Information hat eine eindeutig definierte führende Quelle
- konkurrierende Wahrheiten sind unzulässig
- Integration ohne definierte Integrationswahrheit ist unzulässig

Integrationswahrheit ist Voraussetzung für Konsistenz und Stabilität.


5.3 Führung
------------
Führung beschreibt, welche Quelle für eine Information verbindlich ist.

Für Führung gilt:
- Führung wird explizit festgelegt
- Führung kann feldgenau definiert werden
- Führung ist unabhängig von Tool, Format oder Darstellung

Ohne explizite Führungsdefinition existiert keine Führung.


5.4 Überschreibung
-------------------
Überschreibungen erfolgen ausschließlich auf Basis der definierten
Führungslogik.

Dabei gilt:
- führende Informationen überschreiben nicht-führende
- nicht-führende Informationen dürfen führende nicht verändern
- Überschreibungen sind deterministisch und reproduzierbar

Implizite oder opportunistische Überschreibungen sind unzulässig.


5.5 Integration
----------------
Integration bezeichnet die regelgeleitete Zusammenführung von Informationen
aus unterschiedlichen Quellen.

Integration:
- respektiert Identität und Führung
- erzeugt keine neue Identität
- erzeugt keine neue Semantik
- verändert keine führenden Informationen

Integration ist kein Zusammenkopieren von Daten.


5.6 Ableitung
--------------
Ableitung beschreibt die Überführung von Informationen in andere Artefakte
oder Formate.

Für Ableitung gilt:
- sie ist explizit definiert
- sie ist nachvollziehbar
- sie erzeugt keine neue Identität
- sie verändert keine führenden Informationen

Ableitung ist eine Einbahnstraße.


5.7 Keine Rückwirkung
----------------------
Abgeleitete Artefakte besitzen keine Rückwirkung auf ihre Quelle.

Das bedeutet:
- Änderungen in abgeleiteten Artefakten verändern keine Architektur- oder
  Integrationsmodelle
- Ausführungs- oder Darstellungsartefakte definieren keine neue Wahrheit
- Rückwirkungen sind normativ ausgeschlossen

Dieses Prinzip ist unverhandelbar.


5.8 Trennung von Integration und Ableitung
-------------------------------------------
Integration und Ableitung sind strikt voneinander getrennt.

- Integration führt Informationen zusammen
- Ableitung materialisiert Informationen in andere Kontexte

Eine Vermischung beider Konzepte ist unzulässig.


5.9 Lern- und Reifeaspekt
--------------------------
Die strikte Regelung von Integration, Führung und Ableitung ist bewusst Teil
des Lern- und Reifemodells dieses Projekts.

Sie dient dazu:
- implizite Annahmen sichtbar zu machen
- langfristige Auswirkungen von Integrationsentscheidungen zu verstehen
- disziplinierte Modellpflege zu erlernen

Abkürzungen untergraben dieses Ziel.


5.10 Abschluss des Kapitels
-----------------------------
Dieses Kapitel definiert die verbindlichen Regeln für Integration, Führung
und Ableitung im Blueprint-System.

Die folgenden Kapitel konkretisieren diese Regeln in Bezug auf:
- Artefaktrollen und Ebenentrennung
- Automatisierung und Scripts
- Qualität, Validierung und Audit
- verbindliche Hard Facts


--------------------------------------------------------------------------------
6. ARTEFAKTROLLEN UND EBENENTRENNUNG
--------------------------------------------------------------------------------

6.1 Zweck dieses Kapitels
---------------------------
Dieses Kapitel definiert die Rollen unterschiedlicher Artefakte innerhalb des
Blueprint-Systems sowie deren zulässige Beziehungen zueinander.

Ziel ist es:
- eine klare Trennung von Verantwortlichkeiten sicherzustellen
- Vermischung von Architektur, Integration und Ausführung zu verhindern
- Rückwirkungen und implizite Bedeutungsverschiebungen auszuschließen
- die langfristige Stabilität des Modells zu sichern

Artefaktrollen sind verbindlich und nicht austauschbar.


6.2 Artefakt
-------------
Ein Artefakt ist eine konkrete Repräsentation von Informationen in einem
bestimmten Kontext, Format oder Werkzeug.

Ein Artefakt:
- repräsentiert Objekte, besitzt aber keine eigene Identität
- ist kontext- und zweckgebunden
- unterliegt einer klar definierten Rolle

Artefakte sind Träger von Information, nicht deren Ursprung.


6.3 Führendes Artefakt
-----------------------
Ein führendes Artefakt definiert die verbindliche Wahrheit für bestimmte
Informationen.

Für führende Artefakte gilt:
- sie sind explizit als führend definiert
- sie besitzen keine implizite Führung
- sie sind Referenz für Integration und Ableitung

Ohne explizite Definition existiert kein führendes Artefakt.


6.4 Architekturartefakte
-------------------------
Architekturartefakte beschreiben die strukturelle Referenz des
Blueprint-Systems.

Sie enthalten:
- Objekte und deren Beziehungen
- Rollen und Struktur
- keine Ausführungslogik
- keine Tool- oder Plattformsemantik

Architekturartefakte sind führend für Struktur, nicht für Ausführung.


6.5 Integrationsartefakte
--------------------------
Integrationsartefakte dienen der Zusammenführung von Informationen aus
unterschiedlichen Quellen.

Für Integrationsartefakte gilt:
- sie folgen der definierten Integrations- und Führungslogik
- sie erzeugen keine neue Identität
- sie verändern keine Architekturprinzipien
- sie enthalten keine implizite Semantik

Integrationsartefakte sind abgeleitet, nicht führend.


6.6 Abgeleitete Artefakte
--------------------------
Abgeleitete Artefakte materialisieren Informationen für spezifische Zwecke.

Beispiele sind:
- Prozessmodelle
- Ausführungsmodelle
- technische Konfigurationen
- Visualisierungen

Für abgeleitete Artefakte gilt:
- sie besitzen keine Führungswirkung
- sie erzeugen keine neue Wahrheit
- sie wirken nicht rück auf Architektur oder Integration


6.7 Ebenentrennung
-------------------
Das Blueprint-System trennt strikt zwischen folgenden Ebenen:
- Architektur
- Integration
- Ableitung / Ausführung

Diese Ebenen sind logisch getrennt und dürfen nicht vermischt werden.

Eine Ebene darf keine Regeln für eine andere Ebene definieren.


6.8 Keine Rückwirkung zwischen Ebenen
--------------------------------------
Rückwirkungen zwischen Ebenen sind normativ ausgeschlossen.

Das bedeutet:
- Änderungen in abgeleiteten Artefakten verändern keine Architektur
- Integrationsartefakte definieren keine neue Architektursemantik
- Ausführungsartefakte besitzen keine Governance-Wirkung

Dieses Prinzip ist unverhandelbar.


6.9 Lern- und Reifeaspekt der Ebenentrennung
---------------------------------------------
Die strikte Ebenentrennung ist bewusst Teil des Lern- und Reifemodells dieses
Projekts.

Sie dient dazu:
- Verantwortlichkeiten klar zu erkennen
- implizite Bedeutungsverschiebungen zu vermeiden
- langfristige Auswirkungen von Vermischung sichtbar zu machen

Disziplin in der Ebenentrennung ist ein zentrales Reifeziel.


6.10 Abschluss des Kapitels
-----------------------------
Dieses Kapitel definiert die verbindlichen Artefaktrollen und die
Ebenentrennung im Blueprint-System.

Die folgenden Kapitel konkretisieren diese Regeln in Bezug auf:
- Automatisierung und Scripts
- Qualität, Validierung und Audit
- verbindliche Hard Facts


--------------------------------------------------------------------------------
7. AUTOMATISIERUNG UND SCRIPTS
--------------------------------------------------------------------------------

7.1 Zweck dieses Kapitels
---------------------------
Dieses Kapitel definiert die verbindlichen Regeln für den Einsatz von
Automatisierung und Scripts im Blueprint-System.

Ziel ist es:
- Automatisierung kontrolliert und nachvollziehbar einzusetzen
- implizite Logik und verdeckte Semantik zu verhindern
- Reproduzierbarkeit und Auditierbarkeit sicherzustellen
- Automatisierung als Lern- und Reifeinstrument zu nutzen

Automatisierung dient der Unterstützung der Governance, nicht deren Umgehung.


7.2 Rolle von Automatisierung
------------------------------
Automatisierung ist ein Hilfsmittel zur Umsetzung explizit definierter Regeln.

Für Automatisierung gilt:
- sie ersetzt keine Governance-Entscheidungen
- sie interpretiert keine Modellinhalte
- sie erzeugt keine neue Semantik
- sie trifft keine impliziten Annahmen

Automatisierung folgt Regeln, sie definiert keine.


7.3 Script als Governance-Artefakt
------------------------------------
Scripts sind explizite Governance-Artefakte.

Ein Script:
- erfüllt genau eine fachlich klar beschreibbare Aufgabe
- ist deterministisch
- ist reproduzierbar
- ist nachvollziehbar

Scripts sind Teil des Systems und unterliegen denselben Governance-Regeln wie
andere Artefakte.


7.4 Script-Disziplin
---------------------
Für Scripts gelten verbindliche Disziplinregeln:
- ein Script erfüllt genau eine fachliche Wirkung
- Scripts enthalten keine implizite Semantik
- Scripts interpretieren keine Modellinhalte
- Scripts verändern keine Governance-Regeln

Mehrdeutige oder multifunktionale Scripts sind unzulässig.


7.5 Script-Benennung
---------------------
Scripts unterliegen verbindlichen Benennungsregeln.

Für die Benennung gilt:
- der Name beschreibt die fachliche Wirkung
- der Name enthält keine technischen Implementierungsdetails
- der Name enthält keine Versions- oder Laufzeitinformationen

Script-Namen dienen der Nachvollziehbarkeit, nicht der Steuerung.


7.6 Automatisierung und Identität
-----------------------------------
Automatisierung respektiert die Identität von Objekten.

Für automatisierte Prozesse gilt:
- keine automatische Erzeugung neuer Identitäten
- keine implizite Änderung bestehender Identitäten
- keine Rekonstruktion von Identität durch Heuristiken

Identität ist nicht automatisierbar.


7.7 Automatisierung und Integration
-------------------------------------
Automatisierung folgt der definierten Integrations- und Führungslogik.

Das bedeutet:
- automatisierte Integration respektiert Führungsdefinitionen
- automatisierte Prozesse überschreiben keine führenden Informationen
- automatisierte Prozesse erzeugen keine neue Integrationswahrheit

Automatisierung verstärkt Regeln, sie ersetzt sie nicht.


7.8 Automatisierung und Ableitung
----------------------------------
Automatisierte Ableitungen:
- sind explizit definiert
- sind nachvollziehbar
- erzeugen keine neue Identität
- besitzen keine Rückwirkung

Automatisierte Ableitung ist eine technische Umsetzung expliziter Regeln.


7.9 Lern- und Reifeaspekt der Automatisierung
----------------------------------------------
Der Einsatz von Automatisierung ist bewusst Teil des Lern- und Reifemodells.

Er dient dazu:
- die Grenzen automatisierbarer Entscheidungen zu erkennen
- implizite Annahmen sichtbar zu machen
- Disziplin im Umgang mit Regeln zu erlernen

Automatisierung ohne Disziplin untergräbt das Lernziel.


7.10 Abschluss des Kapitels
-----------------------------
Dieses Kapitel definiert die verbindlichen Regeln für Automatisierung und
Scripts im Blueprint-System.

Die folgenden Kapitel konkretisieren diese Regeln in Bezug auf:
- Qualität, Validierung und Audit
- verbindliche Hard Facts


--------------------------------------------------------------------------------
8. QUALITÄT, VALIDIERUNG UND AUDIT
--------------------------------------------------------------------------------

8.1 Zweck dieses Kapitels
---------------------------
Dieses Kapitel definiert die Anforderungen an Qualität, Validierung und
Auditierbarkeit des Blueprint-Systems.

Ziel ist es:
- die Konsistenz und Stabilität des Modells sicherzustellen
- Fehler, Inkonsistenzen und implizite Annahmen frühzeitig zu erkennen
- die Nachvollziehbarkeit aller relevanten Entscheidungen zu gewährleisten
- das Blueprint-System dauerhaft prüf- und erklärbar zu halten

Qualität ist kein nachgelagerter Schritt, sondern integraler Bestandteil
der Governance.


8.2 Qualitätsverständnis
-------------------------
Qualität im Blueprint-System bedeutet:
- strukturelle Konsistenz
- eindeutige Identität
- explizite Semantik
- regelkonforme Integration und Ableitung

Qualität wird nicht subjektiv bewertet, sondern regelbasiert festgestellt.


8.3 Validierung
----------------
Validierung bezeichnet die systematische Prüfung des Blueprint-Systems gegen
die definierten Governance-Regeln.

Für Validierung gilt:
- sie ist deterministisch
- sie ist reproduzierbar
- sie ist regelbasiert
- sie ist unabhängig von Werkzeugen oder Darstellungen

Validierung prüft Konformität, nicht Zweckmäßigkeit.


8.4 Validierungsgegenstände
-----------------------------
Validiert werden insbesondere:
- Identitätskonsistenz
- Einhaltung der Führungs- und Integrationslogik
- korrekte Ebenentrennung
- regelkonforme Ableitung
- Einhaltung der Script-Disziplin

Nicht validierbare Zustände sind unzulässig.


8.5 Fehler und Abweichungen
-----------------------------
Fehler sind Abweichungen von den definierten Regeln.

Für Fehler gilt:
- sie sind explizit zu identifizieren
- sie sind nachvollziehbar zu dokumentieren
- sie sind nicht stillschweigend zu korrigieren

Abweichungen ohne Dokumentation sind unzulässig.


8.6 Auditierbarkeit
--------------------
Das Blueprint-System ist auditierbar aufgebaut.

Auditierbarkeit bedeutet:
- alle relevanten Entscheidungen sind nachvollziehbar
- alle Regeln sind explizit dokumentiert
- alle automatisierten Schritte sind reproduzierbar
- alle Abweichungen sind sichtbar

Auditierbarkeit ist Voraussetzung für langfristige Stabilität.


8.7 Reproduzierbarkeit
-----------------------
Reproduzierbarkeit ist ein zentrales Qualitätsmerkmal.

Für das System gilt:
- gleiche Eingaben führen zu gleichen Ergebnissen
- Integrations- und Ableitungsprozesse sind wiederholbar
- Modellzustände sind eindeutig rekonstruierbar

Nicht reproduzierbare Zustände sind unzulässig.


8.8 Lern- und Reifeaspekt von Qualität und Audit
-------------------------------------------------
Qualitätssicherung und Audit sind bewusst Teil des Lern- und Reifemodells.

Sie dienen dazu:
- diszipliniertes Arbeiten zu verankern
- implizite Annahmen sichtbar zu machen
- langfristige Auswirkungen von Regelverstößen zu verstehen

Qualität entsteht durch Regelbefolgung, nicht durch Korrektur im Nachhinein.


8.9 Abschluss des Kapitels
----------------------------
Dieses Kapitel definiert die verbindlichen Anforderungen an Qualität,
Validierung und Audit im Blueprint-System.

Das folgende Kapitel fasst die nicht verhandelbaren Regeln des Systems in
Form von Hard Facts zusammen.


--------------------------------------------------------------------------------
9. HARD FACTS
--------------------------------------------------------------------------------

9.1 Allgemeiner Regelcharakter
--------------------------------
Die in diesem Kapitel aufgeführten Regeln sind nicht verhandelbar.

Sie gelten:
- systemweit
- unabhängig von Kontext, Werkzeug oder Zweck
- ohne Ausnahmen, sofern nicht explizit geregelt

Verstöße gegen diese Regeln sind unzulässig.


9.2 Identität
--------------
- Jedes Objekt besitzt genau eine Identität.
- Identität ist ausschließlich über die Objekt-ID definiert.
- Namen, Typen oder Darstellungen sind nicht identitätsstiftend.
- Objekt-IDs sind stabil und dürfen nicht geändert werden.
- Automatische Erzeugung neuer Objekt-IDs ist unzulässig.


9.3 ID-Reparatur und Blockade
------------------------------
- ID-Reparatur ist nur zulässig, wenn die Identität eindeutig
  rekonstruierbar ist.
- ID-Reparatur darf keine semantische Annahme erfordern.
- Ist Identität nicht eindeutig bestimmbar, ist der Vorgang zu blockieren.
- Blockade ist einem falschen Import vorzuziehen.


9.4 Namen
----------
- Namen dienen ausschließlich der Lesbarkeit.
- Namen enthalten keine implizite Semantik.
- Namensänderungen verändern keine Identität.
- Namen dürfen nicht zur Steuerung von Integration oder Ableitung
  verwendet werden.


9.5 Führung und Integrationswahrheit
--------------------------------------
- Für jede Information existiert genau eine führende Quelle.
- Führung ist explizit festzulegen.
- Führung kann feldgenau definiert werden.
- Ohne definierte Führung ist keine Integration zulässig.
- Nicht-führende Informationen dürfen führende nicht überschreiben.


9.6 Integration
----------------
- Integration erfolgt ausschließlich regelbasiert.
- Integration erzeugt keine neue Identität.
- Integration erzeugt keine neue Semantik.
- Integration respektiert die definierte Führungslogik.
- Implizite Integration ist unzulässig.


9.7 CSV und Transportformate
-----------------------------
- CSV-Dateien sind reine Transportformate.
- CSV-Dateien enthalten keine implizite Semantik.
- CSV-Dateien erzeugen keine Identität.
- CSV-Dateien überschreiben keine führenden Informationen.


9.8 Ableitung
--------------
- Ableitung ist explizit definiert.
- Ableitung erzeugt keine neue Identität.
- Ableitung verändert keine führenden Informationen.
- Ableitung wirkt nicht rück auf die Quelle.
- Ableitung ist eine Einbahnstraße.


9.9 Artefaktrollen
-------------------
- Architekturartefakte sind führend für Struktur.
- Integrationsartefakte sind nicht führend.
- Abgeleitete Artefakte besitzen keine Führungswirkung.
- Ausführungsartefakte definieren keine Architektur.


9.10 Ebenentrennung
--------------------
- Architektur, Integration und Ableitung sind strikt getrennt.
- Eine Ebene definiert keine Regeln für eine andere Ebene.
- Rückwirkungen zwischen Ebenen sind unzulässig.


9.11 Automatisierung und Scripts
---------------------------------
- Scripts erfüllen genau eine fachliche Wirkung.
- Scripts sind deterministisch und reproduzierbar.
- Scripts interpretieren keine Modellinhalte.
- Scripts erzeugen keine neue Semantik.
- Scripts verändern keine Governance-Regeln.


9.12 Tool-Unabhängigkeit
-------------------------
- Architekturmodelle enthalten keine Tool-Semantik.
- Tool-spezifische Einschränkungen rechtfertigen keine Architekturänderungen.
- Werkzeuge besitzen keine Governance-Wirkung.
- Objekttypen sind stabil und werden nicht zur Ermöglichung von Beziehungen
  geändert.
- Ist keine normkonforme Beziehung möglich, ist Association als zulässiger
  Fallback zu verwenden.
- Beziehungstypen werden nicht semantisch überladen.


9.13 Qualität und Validierung
------------------------------
- Modellzustände müssen validierbar sein.
- Validierung ist deterministisch und reproduzierbar.
- Nicht validierbare Zustände sind unzulässig.
- Fehler dürfen nicht stillschweigend korrigiert werden.


9.14 Audit
-----------
- Alle relevanten Entscheidungen sind nachvollziehbar.
- Alle automatisierten Schritte sind reproduzierbar.
- Alle Abweichungen sind dokumentiert.
- Nicht auditierbare Zustände sind unzulässig.


9.15 Abschluss des Kapitels
-----------------------------
Dieses Kapitel definiert die verbindlichen Hard Facts des
Blueprint-Governance-Systems.

Alle vorhergehenden Kapitel dienen dem Verständnis dieser Regeln.
Dieses Kapitel definiert ihre Geltung.


--------------------------------------------------------------------------------
10. SPRINTS
--------------------------------------------------------------------------------
Erweiterung Stage 8 | 2026-03-27

10.1 Zweck dieses Kapitels
----------------------------
Dieses Kapitel definiert die verbindlichen Regeln für den Einsatz von Sprints
innerhalb der MUNI-Governance.

Ziel ist es:
- zielorientierte Umsetzungsphasen unter bewusst reduzierter Prozesssicht
  zu ermöglichen
- auf Fehler oder Feature-Zuwachs kontrolliert reagieren zu können
- die Lern- und Reifeintention der Governance nicht zu unterlaufen

Sprints sind kein Ersatz für die bestehende Governance, sondern eine explizit
geregelte Sonderform ihrer Anwendung.


10.2 Definition Sprint
-----------------------
Ein Sprint ist eine zeitlich begrenzte Umsetzungsphase, die auf ein vorab
explizit definiertes Ziel ausgerichtet ist.

Für einen Sprint gilt:
- das Ziel ist verbindlich
- der Weg zum Ziel ist nicht vollständig vorgegeben
- die vollständige Abbildung aller Zwischenschritte ist nicht erforderlich

Ein Sprint ist kein governance-freier Raum.


10.3 Zulässige Auslöser für Sprints                              [UPDATE S8]
-------------------------------------
Ein Sprint ist ausschließlich zulässig, wenn er durch einen der folgenden
Auslöser begründet ist:
- Fehlerbehebung
- Feature-Zuwachs
- Strukturbereinigung
- Kundenbedarf
- Entwicklerwunsch

Andere Auslöser sind unzulässig.


10.4 Fehler als Sprint-Auslöser
---------------------------------
Ein Sprint darf ausgelöst werden, wenn:
- ein fachlicher, struktureller oder technischer Fehler vorliegt
- der Fehler explizit benannt und abgegrenzt ist
- eine reguläre Umsetzung den Fehler nicht angemessen adressieren würde

Fehler im Sinne dieses Kapitels sind Abweichungen vom intendierten
Systemzustand, nicht Abweichungen von Governance-Regeln.


10.5 Feature-Zuwachs als Sprint-Auslöser
-----------------------------------------
Ein Sprint darf ausgelöst werden, wenn ein Feature-Zuwachs umgesetzt werden
soll.

Feature-Zuwachs kann ausgelöst sein durch:
- einen Entwicklerwunsch
- einen User-Wunsch
- einen Associate-Wunsch
- einen Kundenbedarf

Für Feature-Zuwachs gilt:
- der Wunsch ist explizit zu benennen
- der fachliche Mehrwert ist zu beschreiben
- der Zuwachs erzeugt keine implizite Governance-Änderung

Feature-Zuwachs rechtfertigt keine Abweichung von Architektur-, Integrations-
oder Identitätsprinzipien.


10.6 Zieldefinition als zwingende Voraussetzung
-------------------------------------------------
Für jeden Sprint gilt verbindlich:
- das Ziel ist explizit definiert
- das Ziel ist eindeutig einem zulässigen Auslöser zugeordnet
- das Ziel ist überprüfbar und abgegrenzt

Ohne explizite Zieldefinition existiert kein Sprint.


10.7 Umgang mit Zwischenschritten
----------------------------------
Während eines Sprints gilt:
- Zwischenschritte müssen nicht vollständig dokumentiert werden
- der Ablauf darf Lücken enthalten
- Entscheidungen dürfen situativ getroffen werden

Diese Regelung stellt keine Abweichung von der Governance, sondern eine
normativ zugelassene Einschränkung der Dokumentationspflicht dar.


10.8 Dokumentation während des Sprints
----------------------------------------
Während eines Sprints werden ausschließlich Dev-Dokumentationen erstellt.

Für diese gilt:
- sie dienen der späteren Nachvollziehbarkeit
- sie müssen eine vollständige Rekonstruktion ermöglichen
- sie sind während des Sprints nicht auditpflichtig

Dev-Dokumentationen ersetzen keine finale Dokumentation.


10.9 Dokumentation zum Stage-Ende
-----------------------------------
Spätestens zum Stage-Ende eines Sprints gilt:
- vollständige Dokumentation ist verpflichtend
- alle relevanten Entscheidungen sind explizit nachzudokumentieren
- Governance-Konformität ist herzustellen und prüfbar

Ein Sprint gilt erst mit abgeschlossener Dokumentation als beendet.


10.10 Verhältnis zur bestehenden Governance
--------------------------------------------
Für Sprints gilt:
- keine Governance-Regel wird aufgehoben
- ausschließlich der Zeitpunkt der Dokumentation wird verschoben
- es entsteht keine neue Ausnahme- oder Präzedenzwirkung

Alle Ergebnisse eines Sprints unterliegen vollständig der bestehenden
Governance.


10.11 Lern- und Reifeaspekt von Sprints
-----------------------------------------
Sprints sind bewusst Teil des Lern- und Reifemodells der MUNI-Governance.

Sie dienen dazu:
- Spannungen zwischen Zielorientierung und Disziplin erfahrbar zu machen
- die Grenzen reduzierter Dokumentation zu erkennen
- Verantwortung für nachträgliche Explizitheit zu übernehmen

Missbrauch von Sprints untergräbt das Lernziel.


10.12 Session-Regel                                              [NEU S8]
--------------------
In stabilen, klar abgegrenzten Kontexten kann eine Session-Regel eine
formal dokumentierte Regel ersetzen.

Für die Session-Regel gilt:
- der Auslöser ist klar und explizit benannt
- der Kontext ist stabil und eindeutig
- die Wirkung ist auf die laufende Session begrenzt
- kein Backlog-Eintrag ist erforderlich

Eine Session-Regel erzeugt keine Governance-Wirkung über die Session hinaus.
Sie verändert keine bestehenden Regeln und schafft keine Präzedenz.

Die Session-Regel ist ein bewusstes Instrument zur Schlankheit der Governance
— kein Einfallstor für implizite Abweichungen.


10.13 Stage-Bezeichnungskonvention für Dokumente                [NEU S8]
-------------------------------------------------
Alle Blueprint-Dokumente im Beta-Zustand erhalten das Suffix _S<N>,
wobei <N> die Stage-Nummer zum Zeitpunkt der Erstellung bezeichnet.

Für die Konvention gilt:
- sie gilt für alle neuen Dokumente ab Stage 7
- sie ist einheitlich über alle Dokumentreihen anzuwenden
- sie dient der Nachvollziehbarkeit des Entstehungszeitpunkts
- sie ersetzt keine inhaltliche Versionierung

Beispiel: ASSOCIATE_Sprint_Template_S7.md — erstellt in Stage 7.

Die Konvention gilt nicht rückwirkend für Dokumente vor Stage 7.


--------------------------------------------------------------------------------
11. UMGANG MIT USERN
--------------------------------------------------------------------------------
Erweiterung Stage 5 | 2026-03-09
Terminologie-Korrektur | 2026-03-18

11.1 Zweck dieses Kapitels
---------------------------
Dieses Kapitel definiert die verbindlichen Regeln für den Umgang mit
Usern im R+MUNI Livebetrieb ab Stage 5.

Ziel ist es:
- einen fairen, ehrlichen und transparenten Umgang mit allen Usern
  sicherzustellen
- klare Erwartungen zu definieren ohne Versprechen zu erzeugen die nicht
  gehalten werden können
- die Offenheit von R+MUNI als Grundprinzip im User-Kontakt zu verankern

Begriffsdefinition:
  User    = jeder der R+MUNI nutzt — gratis, ohne Bedingung,
            unabhängig vom Nutzungsumfang
  Kunde   = wer explizit einen bezahlten Service in Anspruch nimmt
            (Installation, Wartung, individuelle Begleitung)


11.2 Grundhaltung gegenüber Usern
-----------------------------------
R+MUNI ist und bleibt kostenlos. Das ist kein Marketing, sondern Haltung.

Für den User-Kontakt gilt:
- Offenheit und Ehrlichkeit sind nicht verhandelbar
- Kritik von Usern ist Feedback — kein Angriff
- Kein User wird zu einem Upgrade, einer Zahlung oder einer Entscheidung
  gedrängt
- Der Entwickler behält das Recht situativ zu entscheiden was er annimmt
  und was nicht — Kapazität ist eine legitime Absage


11.3 Kommunikationskanal
-------------------------
Der definierte Kanal für User-Kommunikation ist das R+MUNI Portal:
  https://ims-blueprint-ticketsystem.atlassian.net/helpcenter/RMNP/

Für das Portal gilt:
- Zugang ist offen für jeden ohne Registrierungszwang
- 3 Request-Typen stehen zur Verfügung: Bug, Feature Request, DEV Anfrage
- Vertriebsanfragen werden nicht über das Portal abgewickelt
- Antworten erfolgen über das Portal — kein E-Mail-Zwang


11.4 Umgang mit User-Anfragen
-------------------------------
Für eingehende Anfragen gilt:

  Bug:
  - wird ernst genommen und geprüft
  - Rückmeldung erfolgt sobald möglich — keine SLA, kein Versprechen
  - Bugfix erfordert explizite Freigabe durch den Entwickler (GOV 10.4)

  Feature Request:
  - wird gesammelt und bewertet
  - kein Automatismus zur Umsetzung
  - User-Wunsch kann Sprint-Auslöser sein (GOV 10.5)

  DEV Anfrage:
  - wird gelesen und situativ bewertet
  - ob daraus eine Leistung wird entscheidet der Entwickler
  - Kapazität und Workload sind legitime Entscheidungskriterien
  - keine implizite Zusage durch Annahme der Anfrage


11.5 User-Feedback als Blueprint-Input
----------------------------------------
Feedback aus dem Livebetrieb darf:
- in Stage-5-Entwicklung einfließen
- als Grundlage für GOV-Erweiterungen dienen
- BPMN Default Flow Prioritäten beeinflussen

Feedback darf nicht:
- Stage-3/4-Kernlogik verändern
- ohne expliziten Entwicklerentscheid umgesetzt werden


11.6 Wertschätzung gegenüber dem Archi-Entwickler
---------------------------------------------------
Archi ist ein kostenloses Open-Source-Tool ohne Kaufmodell.
Der Entwickler lebt von freiwilligen Beiträgen.

R+MUNI wäre ohne Archi nicht möglich — das ist keine Floskel, sondern Fakt.

Für jeden User der Archi produktiv nutzt gilt daher als Grundsatz:
- Der Entwickler (EUMAXL) vermittelt bewusst ein Geschenk-Abo an den
  Archi-Entwickler als Zeichen der Wertschätzung
- Das ist keine Marketing-Maßnahme und kein Zwang
- Es ist gelebte Haltung: wer von einem Tool profitiert, trägt es mit
- Dieser Grundsatz ist im R+MUNI Blueprint und README verankert

Kurzform: Support ist kein Mord — und wer gute Werkzeuge nutzt,
          sollte denen danken die sie bauen.


11.7 Optionales Atlassian für User
------------------------------------
User können ein eigenes Atlassian Free Bundle aufbauen.

Dafür gilt:
- es ist eine Option, kein Standard und kein Zwang
- der Entwickler unterstützt bei Basis-Fragen im Rahmen seiner Möglichkeiten
- für komplexe Atlassian-Themen vermittelt der Entwickler bei Bedarf
  spezialisierte Expertise weiter — Atlassian ist nicht sein Kerngeschäft
- kein User wird zu einem kostenpflichtigen Atlassian-Plan gedrängt


--------------------------------------------------------------------------------
12. UMGANG MIT DEM R+MUNI TEAM
--------------------------------------------------------------------------------
Erweiterung Stage 5 | 2026-03-09

12.1 Zweck dieses Kapitels
---------------------------
Dieses Kapitel definiert die verbindlichen Regeln für den Aufbau und
den Betrieb des R+MUNI Teams ab Stage 5.

R+MUNI wächst vom Ein-Mann-Projekt zur strukturierten Zusammenarbeit.
Diese Regeln sichern dieses Wachstum ohne die Kernprinzipien zu gefährden.


12.2 Team-Struktur (Stage 5)
------------------------------
Das R+MUNI Team besteht in Stage 5 aus folgenden Rollen:

  Betreiber (EUMAXL):
  - volle Rechte und Projektverantwortung
  - einzige Instanz für Stage-Entscheide und GOV-Änderungen
  - einzige Instanz für Bugfix-Freigaben in Stage 3/4

  Team User (COLUMBO — Einladung offen):
  - volle Atlassian-Rechte im R+MUNI Bundle
  - unterstützt im Atlassian-Umfeld
  - kein eigenständiger Stage-Entscheid ohne Betreiber-Freigabe

  Service User 1 (Claude):
  - AI-Unterstützung im Entwicklungs- und Dokumentationsumfeld
  - konkrete Atlassian-Rolle wird in Stage 5 geklärt
  - kein eigenständiger Entscheid ohne Betreiber-Freigabe

  Service User 2:
  - Reserve — noch nicht vergeben

  User und weitere Team-Mitglieder:
  - nach Bedarf, innerhalb Free-Plan-Limits


12.3 Onboarding neuer Team-Mitglieder
---------------------------------------
Für das Onboarding gilt:
- Blueprint ist die Grundlage — kein Wissenstransfer ohne Blueprint-Basis
- Neue Team-Mitglieder erhalten Zugang zur R+MUNI Dokumentation
  vor dem ersten operativen Einsatz
- Rollen und Rechte werden explizit vergeben — kein impliziter Zuwachs
- Atlassian-Zugang erfolgt gemäß BETA ONBOARDING — MLAT Dokument


12.4 Kommunikation im Team
----------------------------
Für die interne Team-Kommunikation gilt:
- Atlassian (Jira + Confluence) ist die primäre Arbeitsplattform
- Entscheidungen werden dokumentiert — kein stiller Konsens
- Der Betreiber hat das letzte Wort bei Konflikten


12.5 Wissenstransfer und Reproduzierbarkeit
---------------------------------------------
Für den Wissenstransfer gilt:
- Der Blueprint ist so zu pflegen dass ein neues Team-Mitglied
  ohne mündliche Übergabe arbeitsfähig wird
- Sprint Dev-Dokumentationen sind vollständig und nachvollziehbar
- GOV-Entscheide werden immer schriftlich festgehalten


12.6 GOV-Hoheit
-----------------
Die GOV-Hoheit liegt ausschließlich beim Betreiber.

Für GOV-Änderungen gilt:
- nur der Betreiber kann GOV-Änderungen initiieren und freigeben
- GOV-Erweiterungen sind additiv — keine Revision bestehender Kapitel
- jede GOV-Änderung wird dokumentiert mit Datum und Begründung
- Team-Mitglieder können GOV-Änderungen vorschlagen — entscheiden nicht


--------------------------------------------------------------------------------
13. USER-FEEDBACK-KANAL UND EXTERNE ERKENNTNISQUELLEN
--------------------------------------------------------------------------------
Erweiterung Stage 5 | 2026-03-18
Terminologie-Update Stage 8 | 2026-03-27

13.1 Zweck dieses Kapitels
---------------------------
Dieses Kapitel definiert die verbindlichen Regeln für den Umgang mit
Erkenntnissen aus externen Quellen — insbesondere aus Umgebungen in denen
der Betreiber in einer anderen Rolle agiert als der R+MUNI Entwicklerrolle.

Ziel ist es:
- wertvolle Praxiserkenntnisse strukturiert und kontrolliert nutzbar zu machen
- Rollenvermischung und unkontrollierten Wissenstransfer zu verhindern
- die Anonymisierungspflicht gegenüber Dritten verbindlich zu verankern
- einen klaren Kanal für Associate-orientierte Dokumentation zu etablieren


13.2 Definition: Externe Erkenntnisquelle
------------------------------------------
Eine externe Erkenntnisquelle ist jede Informationsquelle die außerhalb der
R+MUNI Entwicklerrolle entsteht.

Im aktuellen Kontext gilt dies insbesondere für:
- Erfahrungen des Betreibers in der Rolle als Beta-Tester in externen
  Atlassian-Umgebungen
- Beobachtungen aus Begleitprojekten
- Erkenntnisse aus Compliance- oder regulierten Umgebungen in denen
  Claude oder andere AI-Tools nicht eingesetzt werden dürfen

Externe Erkenntnisquellen sind wertvoller Rohstoff — aber kein direkter
Blueprint-Input.


13.3 Kennzeichnungspflicht
---------------------------
Jede externe Erkenntnisquelle ist beim Einbringen in den R+MUNI Kontext
explizit zu kennzeichnen.

Verbindliche Kennzeichnung:
- Dokumente: Prefix MLAT- im Dateinamen oder Titel
- Chat-Eingaben: Tag [MLAT] für reine Erfahrungsberichte
- Chat-Eingaben: Tag [MLAT→RMUNI] für explizit gewünschten Transfer

Ohne Kennzeichnung gilt jede Information als R+MUNI-intern und wird
entsprechend behandelt.

Die Kennzeichnung ist Voraussetzung für kontrollierten Transfer.
Unkennzeichnete externe Inhalte dürfen nicht in R+MUNI-Artefakte einfließen.


13.4 Anonymisierungspflicht
-----------------------------
Für alle externen Erkenntnisquellen gilt eine strikte Anonymisierungspflicht.

Es dürfen in keinem R+MUNI-Artefakt, keiner Dokumentation und keinem
öffentlich zugänglichen Output erscheinen:
- echte Namen von Personen aus externen Umgebungen
- Namen von Organisationen aus externen Projekten
- interne Bezeichnungen, Strukturen oder Konfigurationsdetails
  externer Systeme
- Rohdaten aus externen Umgebungen

Zulässige generische Ersetzungen:
- Personen      → User, Team-Mitglied, Stakeholder, Anwender
- Organisationen → nicht nennen — nur Erkenntnistyp beschreiben
- Systeme       → Beta-Umgebung, Testinstanz, externe Plattform

Die Anonymisierungspflicht gilt auch dann wenn der Betreiber selbst die
Originalbezeichnungen im Chat nennt. Claude wendet die Anonymisierung
automatisch an — der Betreiber ist das Kontrollorgan.


13.5 Transfer-Logik
---------------------
Der Transfer von externen Erkenntnissen in R+MUNI-Artefakte folgt einer
expliziten Dreistufenlogik:

  Stufe 1 — Erfahrungsbericht [MLAT]:
  - Erkenntnis wird aufgenommen und intern verarbeitet
  - kein automatischer Transfer in R+MUNI-Strukturen
  - Claude speichert als verfügbares Kontextwissen

  Stufe 2 — Transfer-Anfrage [MLAT→RMUNI]:
  - Betreiber löst explizit einen Transfer aus
  - Claude übersetzt die Erkenntnis in R+MUNI-konforme Formulierung
  - Rohdaten, Namen und Strukturdetails werden dabei herausgefiltert
  - nur die transferierbare Prozess- oder Architektur-Erkenntnis fließt ein

  Stufe 3 — Freigabe durch Betreiber:
  - transferiertes Ergebnis wird vom Betreiber geprüft und freigegeben
  - erst nach Freigabe wird es in R+MUNI-Dokumentation übernommen
  - kein automatischer Einbau ohne explizite Betreiber-Freigabe

Kein Transfer ohne expliziten Auslöser durch den Betreiber.


13.6 ASSOCIATE-Dokumentationsreihe                               [UPDATE S8]
-------------------------------
Erkenntnisse aus externen Quellen die für Associates relevant sind
werden in einer eigenen Dokumentationsreihe geführt: ASSOCIATE-Reihe.

Für die ASSOCIATE-Reihe gilt:
- Kürzel: ASSOCIATE
- Ablageort: eigener Ordner im Blueprint — Bereich interne Dokumentation
- Charakter: anwenderorientiert, nicht technisch
- Inhalte: Principles und How2-Dokumente für Associates
- Anonymisierungspflicht gilt uneingeschränkt

Die ASSOCIATE-Reihe ist interner Entwicklungs-Input — sie wird nicht
öffentlich gestellt und nicht direkt ausgegeben.
Sie dient als Vorarbeit für spätere Associate-Kommunikation.

ASSOCIATE-Dokumente fließen nicht automatisch in den R+MUNI Blueprint ein.
Jede Übernahme erfordert explizite Betreiber-Freigabe (GOV 13.5 Stufe 3).


13.7 Kontext-Hygiene bei eingeschränktem AI-Einsatz
-----------------------------------------------------
In Umgebungen in denen Claude oder andere AI-Tools aus Compliance-Gründen
nicht eingesetzt werden dürfen gilt für Dokumente die später mit Claude
weiterverarbeitet werden sollen:

  Dokumente müssen so aufgebaut sein dass:
  - der Kontext ohne mündliche Erklärung erschließbar ist
  - jedes Dokument eine klare Zweck- und Quellenangabe enthält
  - Entscheidungen und Begründungen explizit im Dokument stehen
  - keine impliziten Annahmen vorausgesetzt werden

  Bewährte Struktur für AI-fähige Dokumente:
  - Zweck / Kontext (1 Absatz)
  - Ausgangslage (Was war gegeben)
  - Erkenntnis / Entscheidung (Was wurde getan / erkannt)
  - Transferierbarkeit (Was davon ist allgemein gültig)
  - Anonymisierungshinweis wenn relevant

Diese Struktur verhindert Kontext-Drift beim späteren Einbringen
in Claude-gestützte Entwicklungssessions.


13.8 Rollentrennung als Governance-Prinzip
-------------------------------------------
Der Betreiber agiert in mehreren Rollen gleichzeitig:
- R+MUNI Entwickler / DEV
- Beta-Tester in externen Umgebungen
- PreSales / Berater

Diese Rollen sind strikt getrennt zu halten.

Für die Rollentrennung gilt:
- Erkenntnisse aus einer Rolle fließen nicht automatisch in eine andere
- der Betreiber ist Kontrollorgan für die Einhaltung der Trennung
- Claude folgt der Kennzeichnungslogik (GOV 13.3) und mischt Rollen nicht
- bei Unklarheit über die aktive Rolle fragt Claude nach

Rollenvermischung ohne explizite Kennzeichnung ist unzulässig.


13.9 Verhältnis zu bestehenden GOV-Kapiteln
--------------------------------------------
Dieses Kapitel ergänzt:
- GOV 11 (Umgang mit Usern): ASSOCIATE-Reihe als vorgelagerte Entwicklungsebene
- GOV 12 (Team): Betreiber-Rolle als Multi-Rollen-Kontext anerkannt
- GOV 10 (Sprints): ASSOCIATE-Erkenntnisse können Sprint-Auslöser sein (GOV 10.5)

Dieses Kapitel verändert keine bestehenden Kapitel.
Es ist additiv und erzeugt keine Präzedenzwirkung für andere Regeln.


13.10 Abschluss des Kapitels
------------------------------
Dieses Kapitel definiert die verbindlichen Regeln für den Umgang mit
externen Erkenntnisquellen und den ASSOCIATE-Feedback-Kanal im R+MUNI Blueprint.

Es schafft die Governance-Grundlage für:
- die AI_DRIVEN_DEV_METHODE Erweiterung (Rollen-Parallelbetrieb)
- die ASSOCIATE-Dokumentationsreihe
- den kontrollierten Transfer-Workflow


--------------------------------------------------------------------------------
14. ZWEI-WELTEN-PRINZIP — INTERN UND PUBLIC                      [NEU S8]
--------------------------------------------------------------------------------
Erweiterung Stage 8 | 2026-03-27

14.1 Zweck dieses Kapitels
---------------------------
Dieses Kapitel verankert das Zwei-Welten-Prinzip als verbindliches
Governance-Grundprinzip des R+MUNI Blueprint.

Das Zwei-Welten-Prinzip wurde in Stage 7 normativ entschieden und gilt
ab Stage 8 als GOV-konformer Standard.


14.2 Definition der zwei Welten
---------------------------------
R+MUNI trennt konsequent zwischen zwei Welten:

  INTERN (DEV-Welt):
  - Blueprint, GOV, Principles, Scripts, Sprint-Dokumentation
  - für DEV-Mitglieder und Betreiber
  - Sprache: technisch, präzise, GOV-konform
  - Zielgruppe: Betreiber, Team, Associates mit DEV-Zugang

  PUBLIC (MGT-Welt):
  - Außenwirkung, Einstieg ohne Rulebook-Wissen
  - für User, potenzielle Beta-Kunden, nicht-technische Leser
  - Sprache: direkt, ergebnisorientiert, ohne Jargon
  - Zielgruppe: User, Interessenten, externe Viewer


14.3 Verbindliche Grundregeln
------------------------------
Für das Zwei-Welten-Prinzip gilt:
- INTERN und PUBLIC sind strikt getrennt — keine Vermischung
- PUBLIC ersetzt nicht die INTERN-Welt, sondern ergänzt sie
- Inhalte aus INTERN fließen nicht automatisch in PUBLIC
- Jede Übernahme von INTERN nach PUBLIC erfordert explizite Betreiber-Freigabe
- PUBLIC-Inhalte besitzen keine Governance-Wirkung auf INTERN


14.4 Abgrenzung zur GOV
------------------------
Die GOV regelt ausschließlich die INTERN-Welt.

Für die PUBLIC-Welt gilt:
- eigene Dokumentationslogik (außerhalb GOV-Scope)
- eigene Sprache und Zielgruppenansprache
- eigene Entwicklungsphase (Phase 2 — Stage 8 und folgende)

Die GOV definiert keine Regeln für PUBLIC-Inhalte.
PUBLIC-Inhalte unterliegen keiner GOV-Prüfpflicht.


14.5 Verhältnis zu bestehenden GOV-Kapiteln
--------------------------------------------
Dieses Kapitel ergänzt:
- GOV 11 (Umgang mit Usern): PUBLIC-Welt als Kommunikationsebene für User
- GOV 13 (ASSOCIATE-Reihe): ASSOCIATE-Inhalte sind INTERN bis zur Freigabe

Dieses Kapitel verändert keine bestehenden Kapitel.
Es ist additiv und erzeugt keine Präzedenzwirkung für andere Regeln.


14.6 Abschluss des Kapitels
-----------------------------
Dieses Kapitel verankert das Zwei-Welten-Prinzip normativ in der Governance.

Die operative Umsetzung — Templates, Dokumentenreihen, MGT-Layout —
erfolgt in eigenen Sprints ab Stage 8 und ist nicht Bestandteil dieser GOV.


================================================================================
R+MUNI GLOBAL GOVERNANCE
Kapitel 1-9 (Stage 3) | Kapitel 10 (Stage 3, erweitert Stage 8) | Kapitel 11-12 (Stage 5 | 2026-03-09) | Kapitel 13 (Stage 5 | 2026-03-18, Terminologie Stage 8 | 2026-03-27) | Kapitel 14 (Stage 8 | 2026-03-27)
Terminologie User/Kunde vereinheitlicht | 2026-03-18
USER-Reihe zu ASSOCIATE-Reihe aktualisiert | 2026-03-27
R+MUNI Blueprint | Markus Resel + Claude (Pair-Session)
================================================================================
