Stage  Freeze – Formale Fixierung
1. Zweck des Freeze
Der Stage‑Freeze erklärt den aktuellen Zustand des Systems als gültigen, tragfähigen Referenzzustand.
Er dient nicht der Finalisierung, sondern der Stabilisierung , aber funktionalen Kreislaufs.
Mit dem Freeze wird festgelegt:
	• welche Funktionen als gegeben gelten
	• welche Reibungspunkte bewusst akzeptiert sind
	• welche Themen explizit nicht Teil von Stage 3 sind

2. Geltungsbereich des Freeze
Der Freeze umfasst:
	• Toolset‑Installation
	• Modell‑ → Export‑ → Import‑Kreislauf
	• Archi -> XML -> BPMN -> CSV -> Archi
	• Konfigurations‑ und Mapping‑Logik
	• Dokumentationsstand
	• Backup‑ und Wiederherstellungsfähigkeit
Nicht umfasst sind:
	• Automatisierung (aber vorbereitet) 
	• Produktisierung
	• Komfort‑ oder UX‑Optimierung
	• Endnutzer‑Abstraktion

3. Fixierter Funktionsumfang (Stage‑Baseline)
3.1 Installation & Umgebung
	• Installation auf einem frischen Notebook möglich
	• Keine nicht‑standardisierten Add‑ons oder Fremd‑Apps erforderlich
	• Toolset läuft reproduzierbar in definierter Umgebung
Status: fixiert

3.2 Modellgetriebener Kreislauf
	• Archi‑ und BPMN‑Modelle sind führende semantische Quellen
	• Exporte (OEF, BPMN‑XML) sind abgeleitete Artefakte
	• Keine semantische Rückführung aus Aggregationsartefakten
Status: fixiert

3.3 FLOW & MUNI WALK
	• FLOW stabil, eigenständig, Stage‑x‑fähig
	• MUNI WALK vollständig durchgetestet
	• Fehlerfall „Camunda 7 ohne zugehörigen Archi‑BP“: 
		○ reproduzierbar bekannt
		○ dokumentierter manueller Workaround (File‑Cleanup)
		○ kein impliziter Fix
Status: fixiert

3.4 Import‑ & Integrationsformate
	• CSV, XML, M2B funktionieren ohne: 
		○ Platzhalter
		○ In‑Script‑Notlösungen
	• 3rd‑Party‑IDs werden übernommen und als Attribut geführt
	• Integration über XLSX/CSV technisch möglich
Status: fixiert

3.5 Logging & Diagnose
	• Logging‑Verhalten verbessert
	• Console‑Output bereinigt
	• Fehlerbilder nachvollziehbar
Status: fixiert

4. Konfiguration & Filterlogik
4.1 Filter
	• Einsatz von Wildcards und offenen Filtern
	• Relevanz wird primär durch Lokationen der Files bestimmt
	• Filterlogik ist verteilt, aber logisch konsistent
Bewertung:
	• funktional ausreichend
	• bewusst nicht gehärtet
	• kein Komfort‑ oder Performance‑Ziel
Status: bewusst akzeptiert

4.2 mapping.xml
	• Keine führende Rolle
	• Temporärer Aggregator und Beobachtungsraum
	• Jederzeit rekonstruierbar
	• Stage‑abhängig adaptierbar
Status: fixiert als nicht‑führend

5. Backup‑ & Wiederherstellung
	• Backups vorhanden
	• Manuell ausgeführt
	• Wiederherstellung möglich
	• Keine Automatisierung HLP Script vorbereitet nicht angepasst. 
Bewertung:
	• ausreichend für Stage 3
	• bewusst nicht optimiert
Status: bewusst akzeptiert

6. Dokumentationsstand (Stage‑3‑Doku)
6.1 Dokumentationsarten
	• Principles pro Flow
	• How2 pro Flow
	• DEV‑Dokumentation
	• ergänzende ReadMe‑Files bei Parsing‑Grenzen
6.2 Charakter der Doku
	• erklärend, nicht abstrahierend
	• rücksprungfähig
	• reproduzierbar
	• nicht auf Endnutzerkomfort optimiert
Wichtig: Dokumentation ist Teil der Systemlogik, kein Abschlussartefakt.
Status: Stage‑3‑konform fixiert

7. Explizite No‑Go‑Zonen (Stage‑3‑Freeze)
In Stage 3 nicht zulässig:
	• Automatisierung von Backups oder Flows
	• Frontend oder UI‑Abstraktion
	• Komfort‑ oder Performance‑Optimierung
	• Workflow‑Normierung
	• Produkt‑ oder Endnutzerdenken
Diese Punkte sind bewusst ausgeschlossen, nicht vergessen.

8. Reproduzierbarkeits‑Statement
Mit:
	• dem fixierten Toolset
	• der vorhandenen Dokumentation
	• den bekannten Reibungspunkten
ist der Stage‑3‑Zustand:
	• jederzeit rekonstruierbar
	• nachvollziehbar
	• nachbaubar
	• überprüfbar

9. Formale Abschlussfeststellung
Stage gilt als abgeschlossen, da:
	• der Kreislauf unter realistischen Bedingungen funktioniert
	• typische Fehlerbilder bekannt und dokumentiert sind
	• Konfigurationen robust genug sind
	• Reibungspunkte bewusst akzeptiert wurden
	• keine Führungs‑ oder Wahrheitsverschiebung stattgefunden hat
Ein „fertiges“ System war nie Ziel von Stage 3 und ist kein Kriterium.

10. Übergangshinweis (ohne Stage‑Eröffnung)
Alle weiteren Aktivitäten wie:
	• Flow‑Runs definieren
	• reale Prozess‑ oder EA‑Modelle umsetzen
	• 3rd‑Party‑Integration ausbauen
	• Filterlogiken härten
	• Backups automatisieren
gehören nicht mehr zum Stage.
Sie sind Anwendung oder Ausbau und werden erst nach expliziter Stage‑Eröffnung behandelt.
