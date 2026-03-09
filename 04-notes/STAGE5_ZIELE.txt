Stage 5 – Real Operation & Ecosystem Enablement
Normative Definition und Geltungsbereich
Datum: 2026-03-09

1. Zweck von Stage 5
Stage 5 dient dem realen Betrieb von R+MUNI im Kundenumfeld und dem
gezielten Aufbau eines tragfähigen Ökosystems rund um den Blueprint.
Im Fokus stehen:
	• realer Livebetrieb mit echten Kunden (Beta und darüber hinaus)
	• organisatorischer Aufbau eines R+MUNI Teams
	• Stabilisierung durch Bugfixing und Optimierung im Betrieb
	• Verwendung von Claude in R+MUNI definieren und dokumentieren
	• schrittweise Erweiterung der BPMN Default Flows nach Bedarf
	• Weiterentwicklung der AI-Driven Development Methodik
	• Integration & Wunschanbindungen aus dem realen Kundenbedarf
Stage 5 ist die erste echte Außenwirkungsphase von R+MUNI –
kein Labor mehr, sondern Realität.

2. Ausgangsbasis
Stage 5 baut auf dem eingefrorenen Stage-4-Zustand auf.
	• Stage-3- und Stage-4-Scripts sind read-only
	• Bestehende Logik gilt als normativ stabil
	• Erweiterungen erfolgen additiv, nicht modifizierend
	• Bugfixing ist zulässig – ohne Logikveränderung
	• Technische Optimierungen im Beta-Kundenumfeld sind zulässig,
	  sofern keine Kernlogik verändert wird
Ein Rückgriff auf Stage-3/4-Artefakte ist zulässig, Eingriffe sind es nicht.
Ausnahme: Bugfixes mit expliziter Freigabe durch den Entwickler.

3. Charakter von Stage 5
Stage 5 ist die erste Phase mit aktiver Außenwirkung und
organisatorischem Wachstum.
	• Erster Beta-Kunde aktiv im Livebetrieb
	• Öffnung für weitere Kunden möglich
	• Aufbau eines R+MUNI Teams als organisatorischer Meilenstein
	• Geschäftsmodell wird in Stage 5 konkretisiert und erprobt
	• Realität schlägt Planung: Kundenbedarf steuert Prioritäten
Stage 5 darf wachsen – kontrolliert und rückkopplungssicher.

4. Zulässige Inhalte in Stage 5

4.1 Atlassian Frontend für Kunden
	• Einrichtung des Atlassian Free Bundle (Confluence + Jira) als
	  Kundeninterface für R+MUNI
	• Standardisiertes Atlassian-Setup als wiederholbares Onboarding-Artefakt
	• Dokumentation des Setup-Prozesses im Blueprint
	• Ziel: Kunde arbeitet selbstständig im Atlassian-Frontend

4.2 Onboarding R+MUNI Team
	• Organisatorischer Meilenstein: R+MUNI wird vom Ein-Mann-Projekt
	  zur strukturierten Zusammenarbeit
	• Onboarding-Prozess definieren und dokumentieren
	• Rollen und Verantwortlichkeiten festlegen
	• Wissenstransfer sicherstellen (Blueprint als Grundlage)
	• GOV um Team-relevante Regeln erweitern

	Atlassian Service Collection Bundle – User-Struktur (bis 10 User):
		○ Betreiber (Markus Resel): volle Rechte, Projektverantwortung
		○ Service User 1 (Claude): AI-Unterstützung im Atlassian Umfeld –
		  konkrete Form (Rovo AI oder Prozessrolle) wird in Stage 5 geklärt
		○ Service User 2: Reserve / noch nicht vergeben
		○ Team User mit vollen Rechten: konkrete Person bekannt,
		  unterstützt im Atlassian Umfeld, erhält alle Rechte
		○ Restliche User: Kunden und Team nach Bedarf

	Grundsatz: Das Bundle wird optimal genutzt –
	kein ungenutztes Potential, keine unnötige Komplexität.

4.3 Bugfixing & Optimierung im Livebetrieb
	• Bugfixing ist explizit zulässig – Livebetrieb deckt auf was Lab nicht sieht
	• Optimierungen ohne Logikveränderung sind erlaubt
	• Jeder Bugfix wird dokumentiert (Sprint Dev-Doku, GOV-konform)
	• Kein stiller Fix – was geändert wird, wird festgehalten
Grenze: Keine Veränderung der normativen Kernlogik ohne Stage-Entscheid.

4.4 GOV-Erweiterung
	• GOV wird um Beta-Kunden-Regeln erweitert:
		○ Umgang mit Kundenfeedback
		○ Fehlermeldungen aus dem Livebetrieb
		○ Kommunikationsregeln mit Kunden
		○ Freigabeprozess für Fixes im Kundenumfeld
	• GOV bleibt das normative Fundament – Erweiterung, keine Revision

4.5 AI-Driven Development Methodik weiterentwickeln
	• Zusammenarbeit mit Claude wird weiter optimiert und formalisiert
	• Bewährte Session-Muster werden dokumentiert und in den Blueprint
	  aufgenommen
	• Ziel: Methodik ist für Dritte nachvollziehbar und reproduzierbar
	• Claude-Nutzung wird von persönlicher Arbeitsweise zur
	  dokumentierten Blueprint-Komponente

4.6 Verwendung von Claude in R+MUNI
R+MUNI ist und bleibt dauerhaft gratis – das ist ein Grundprinzip, keine
Marketingaussage. Claude ist ein Werkzeug das in R+MUNI seinen Platz findet,
kein Produkt und kein Geschäft.

Für Claude gilt:
	• R+MUNI läuft ohne Claude vollständig und kostenlos
	• Claude wird als AI-Driven Development Werkzeug im Blueprint dokumentiert
	• Wer Claude nutzen möchte, findet den Weg selbst – kein Push, kein Zwang
	• Claude erhält einen definierten, sichtbaren Platz im Blueprint

Ökosystem-Philosophie für alle Tools:
	• Alle in R+MUNI verwendeten Tools finden ihren sichtbaren Platz im Blueprint
	• Wer den Wert eines Tools erkennt, schließt selbst ab – organisch, ohne Druck
	• R+MUNI macht transparent womit gearbeitet wird und warum

Sonderfall Archi:
	• Archi hat kein Kaufmodell – der Entwickler lebt von freiwilligen Beiträgen
	• R+MUNI Kunden die Archi produktiv nutzen, erhalten bewusst ein
	  Geschenk-Abo an den Archi-Entwickler als Wertschätzung
	• Das ist kein Marketing – das ist Haltung
	• Verankert im R+MUNI Blueprint und README als gelebter Wert

4.7 BPMN Default Flows mit Scriptrunner
	• Bestehende Script-Reihen werden schrittweise als BPMN Default Flows
	  abgebildet – nach Bedarf im Livebetrieb, nicht auf Vorrat
	• flowmapping.txt wächst mit den Flows
	• Jeder neue Flow folgt dem bestehenden FLW-Muster (1 Flow, 1 Outcome)
	• Reihenfolge wird durch Kundenbedarf und Entwicklerkapazität bestimmt

4.8 Integration & Wunschanbindungen
	• Realer Betrieb zeigt welche Anbindungen tatsächlich gebraucht werden
	• Wunschanbindungen werden gesammelt, bewertet und nach GOV priorisiert
	• Neue Integrationen folgen dem Add-on-Scope Prinzip aus Stage 4:
		○ eigene Stages oder Spin-outs
		○ kein Eingriff in Stage-3/4-Kernlogik
	• Aufwandsabschätzung nach Vision: Stage 5 liefert erste Realitätsdaten

5. Umgang mit Stage-4-Erkenntnissen
Erkenntnisse aus Stage 4 und dem Beta-Betrieb dürfen:
	• in Stage 5 verwertet werden
	• als Grundlage für GOV-Erweiterungen dienen
	• den Wachstumspfad für BPMN Flows informieren
Sie dürfen jedoch:
	• Stage-3/4-Artefakte nicht verändern
	• keine rückwirkende Logikverschiebung erzeugen
Stage 5 ist Verwertung und Wachstum, nicht Revision.

6. Rückkopplungsschutz
	• Stage-3/4-Scripts bleiben read-only
	• Bugfixes erfordern explizite Freigabe und Dokumentation
	• Neue Add-ons und Integrationen erhalten eigene Stages oder Spin-outs
	• Claude Add-on greift nicht in Blueprint-Kernlogik ein
	• Atlassian Frontend ist Präsentations- und Arbeitsschicht –
	  keine Logik, keine Führung

7. Dokumentation in Stage 5
	• Stage 5 besitzt eigene Dokumentation im neuen Claude-Projekt
	• Sprint Dev-Dokumentationen für alle Entwicklungsaktivitäten
	• GOV-Erweiterungen werden formal dokumentiert
	• AI-Driven Dev Methodik wird als Blueprint-Dokument ausgebaut
	• Fokus: Außenwirkung, Reproduzierbarkeit, Teamfähigkeit

8. Abgrenzung zu späteren Stages
Nicht Teil von Stage 5 sind:
	• vollständig automatisierter Onboarding-Prozess ohne manuelle Begleitung
	• fertiges Claude-Produkt mit definiertem Preismodell
	• vollständige BPMN-Abdeckung aller Script-Reihen
	• skalierbare Multi-Tenant-Architektur
Diese Themen wachsen aus Stage 5 heraus – sie sind Ergebnis, nicht Voraussetzung.

9. Formale Feststellung
Mit dieser Definition ist Stage 5:
	• logisch eröffnet
	• klar abgegrenzt von Stage 3 und Stage 4
	• rückkopplungssicher
	• GOV-konform
	• auf realen Betrieb und Außenwirkung ausgerichtet
Stage 3 und Stage 4 bleiben fixiert und geschützt.
Stage 5 darf wachsen, ohne zu verzerren.

================================================================================
Stage 5 – Real Operation & Ecosystem Enablement
ZIELE DEFINIERT | 2026-03-09
R+MUNI Blueprint | Erstellt durch: Markus Resel + Claude (Pair-Session)
================================================================================
