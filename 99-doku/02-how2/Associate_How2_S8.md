================================================================================
ASSOCIATE – HOW2
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : Associate_How2_S5
Tag             : #associate #how2 #rmuni #s5 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-18
Ablageort       : R+MUNI Doku-public\02-how2\Associate_How2_S5.md
================================================================================


VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- Associate_principles_S5.md gelesen und verstanden
- R+MUNI Blueprint installiert und lauffähig
- Atlassian Free Bundle eingerichtet (optional — nur für Atlassian-Workflows)
- Grundverständnis des eigenen Anwendungsfalls vorhanden


================================================================================
ABSCHNITT 1 – WIE MAN MIT R+MUNI STARTET
================================================================================

1.1 Das richtige Erwartungsmanagement
---------------------------------------
R+MUNI ist kein Klick-Fertig-Tool.
Es ist ein Werkzeugkasten der Struktur schafft — aber Denkarbeit voraussetzt.

Was R+MUNI für dich tut:
  - Bringt deine Unternehmensarchitektur in eine strukturierte Form
  - Verbindet Prozesse und IT-Architektur in einem System
  - Macht Abhängigkeiten sichtbar die vorher implizit waren
  - Erzeugt wiederverwendbare, konsistente Dokumentation

Was R+MUNI nicht tut:
  - Dein Unternehmen automatisch verstehen
  - Entscheidungen für dich treffen
  - Sofortige Ergebnisse ohne Vorbereitung liefern

Realistischer Zeithorizont für erste sinnvolle Ergebnisse:
  - Einrichtung und Orientierung:     1–2 Tage
  - Erste eigene Inhalte im System:   1–2 Wochen
  - Produktiver Regelbetrieb:         ab ca. 4–6 Wochen


1.2 Der richtige Einstieg
--------------------------
Nicht mit dem Tool anfangen — mit der Frage anfangen.

Vor der ersten Nutzung beantworten:
  - Was will ich sichtbar machen? (Prozesse? IT-Landschaft? Beides?)
  - Für wen erstelle ich diese Dokumentation?
  - Was ist der erste konkrete Anwendungsfall?

Empfohlene Einstiegsreihenfolge:
  1. Einen einzigen Kernbereich auswählen
  2. Diesen vollständig und konsistent aufbauen
  3. Verstehen wie das Tool damit umgeht
  4. Konventionen ableiten
  5. Erst dann: auf weitere Bereiche ausweiten

Häufiger Fehler beim Einstieg:
  Alles auf einmal modellieren wollen.
  Ergebnis: Überforderung, Inkonsistenz, Frust.
  Besser: klein anfangen, Muster verstehen, dann skalieren.


================================================================================
ABSCHNITT 2 – WIE MAN DOKUMENTE AUFBAUT DIE FUNKTIONIEREN
================================================================================

2.1 Das Prinzip des expliziten Dokuments
------------------------------------------
Ein Dokument das funktioniert enthält alles was jemand braucht um es zu
verstehen — ohne mündliche Erklärung, ohne Vorkenntnisse, ohne Rückfragen.

Das gilt für:
  - Dokumente die du mit anderen teilst
  - Dokumente die du in einem Jahr selbst wieder liest
  - Dokumente die in digitale oder automatisierte Workflows eingebracht werden

Ein explizites Dokument beantwortet immer:
  - Worum geht es? (Zweck)
  - Warum wurde das so gemacht? (Begründung)
  - Was gilt als gegeben? (Ausgangslage)
  - Was darf nicht angenommen werden? (Grenzen)


2.2 Die vier Pflichtfelder für robuste Dokumente
-------------------------------------------------
Für Dokumente die langfristig funktionieren — egal ob alleine gelesen,
im Team verwendet oder in digitale Workflows eingebracht:

  ZWECK / KONTEXT
  ----------------
  Was ist der Gegenstand dieses Dokuments?
  Für wen und wozu wurde es erstellt?
  In welchem Zusammenhang steht es?

  Beispiel:
    "Dieses Dokument beschreibt den Onboarding-Prozess für neue Mitarbeiter
     in der Abteilung Einkauf. Erstellt für die Prozessdokumentation im
     Rahmen des IMS-Aufbaus. Zielgruppe: HR und Abteilungsleiter."

  AUSGANGSLAGE
  -------------
  Was war bekannt / gegeben bevor dieses Dokument entstand?
  Welche Rahmenbedingungen galten?

  Beispiel:
    "Der Prozess wird bisher mündlich weitergegeben. Es gibt keine
     schriftliche Version. Zwei Mitarbeiter kennen ihn vollständig,
     drei kennen nur Teilschritte."

  ERKENNTNIS / ENTSCHEIDUNG
  --------------------------
  Was wurde dokumentiert, entschieden oder erkannt?
  Warum wurde so entschieden?
  Was wurde bewusst nicht getan?

  Beispiel:
    "Der Prozess wurde in vier Hauptschritte gegliedert. Schritt 3
     (IT-Zugang) wurde bewusst ausgelagert — IT hat eigene Prozesse
     die hier nur referenziert werden."

  GRENZEN / GÜLTIGKEITSBEREICH
  -----------------------------
  Was gilt nicht für dieses Dokument?
  Was muss separat geklärt werden?

  Beispiel:
    "Gilt nur für Vollzeit-Mitarbeiter. Freelancer und Praktikanten
     haben abweichende Prozesse die nicht Teil dieses Dokuments sind."


2.3 Warum diese Struktur wichtig ist
--------------------------------------
Dokumente ohne explizite Struktur erzeugen Drift.

Drift bedeutet:
  - Jeder Leser interpretiert das Dokument anders
  - Sechs Monate später ist der Kontext verloren
  - Entscheidungen sind nicht mehr nachvollziehbar
  - Neue Mitarbeiter können das Dokument nicht sinnvoll nutzen

Explizite Dokumente verhindern Drift — nicht durch Ausführlichkeit,
sondern durch Klarheit an den richtigen Stellen.


2.4 Templates verwenden statt neu erfinden
--------------------------------------------
Für wiederkehrende Dokumenttypen lohnt sich ein Template.

Ein Template:
  - erzwingt die vier Pflichtfelder
  - gibt Struktur vor bevor der Inhalt entsteht
  - macht Dokumente konsistent über Zeit und Autoren
  - spart Denkarbeit beim Erstellen

Templates für R+MUNI Standarddokumente können über das Portal
angefragt werden:
  https://ims-blueprint-ticketsystem.atlassian.net/helpcenter/RMNP/


================================================================================
ABSCHNITT 3 – WIE MAN IN EINGESCHRÄNKTEN UMGEBUNGEN ARBEITET
================================================================================

3.1 Das Problem mit eingeschränkten Werkzeugumgebungen
--------------------------------------------------------
In manchen Unternehmen oder Projekten sind bestimmte digitale Werkzeuge
nicht zugelassen — aus Compliance-, Datenschutz- oder Sicherheitsgründen.

Das bedeutet nicht dass strukturiertes Arbeiten unmöglich ist.
Es bedeutet: die Vorbereitung passiert mit verfügbaren Mitteln.
Die Weiterverarbeitung kann später — in einer erlaubten Umgebung — erfolgen.

Voraussetzung dafür: Dokumente müssen so aufgebaut sein dass sie
ohne mündliche Nachbriefung weiterverwendbar sind
(→ Abschnitt 2: die vier Pflichtfelder).


3.2 Was in der eingeschränkten Umgebung passiert
--------------------------------------------------
Dokumente erstellen:
  - Vier Pflichtfelder bewusst befüllen
  - Kontext explizit machen — nichts implizit lassen
  - Vertrauliche Inhalte klar kennzeichnen
  - Format: strukturierter Text, kein proprietäres Format wenn vermeidbar

Entscheidungen dokumentieren:
  - Nicht nur Was — immer auch Warum
  - Alternativen die geprüft und verworfen wurden kurz festhalten
  - Datum und Kontext immer dabei

Grenzen markieren:
  - Was ist vertraulich?
  - Was ist spezifisch für diese Umgebung und nicht übertragbar?
  - Was muss bereinigt werden bevor es weitergegeben werden darf?


3.3 Was danach in der regulären Umgebung möglich ist
-----------------------------------------------------
Wenn Dokumente nach 3.2 vorbereitet wurden kann in einer regulären
Umgebung folgendes sinnvoll passieren:

  - Weiterverarbeitung des Inhalts ohne mündliche Nachbriefung
  - Ableitung von Prinzipien und Mustern aus mehreren Dokumenten
  - Übersetzung in andere Formate (Präsentation, Checkliste, etc.)
  - Qualitätsprüfung auf Vollständigkeit und Konsistenz

Was nicht möglich ist — auch mit guten Dokumenten:
  - Fehlende Entscheidungen können nicht rekonstruiert werden
  - Implizite Annahmen können nicht erraten werden
  - Vertraulichkeitsregeln müssen explizit markiert sein um zu wirken


3.4 Praktische Konsequenz
--------------------------
Wer heute in einer eingeschränkten Umgebung dokumentiert und morgen
die Inhalte weiterverwenden will:

  Sofort umsetzen:
  - Alle neuen Dokumente mit den vier Pflichtfeldern aufbauen
  - Entscheidungsbegründungen explizit festhalten
  - Vertrauliche und nicht übertragbare Inhalte klar markieren

  Mittelfristig:
  - Bestehende Schlüsseldokumente nachbereiten
  - Templates einführen für Standarddokumenttypen

  Nicht tun:
  - Bestehende Dokumente ohne Kontextaufbereitung direkt weitergeben
  - Darauf hoffen dass der Empfänger den Kontext aus dem Inhalt erschließt


================================================================================
ABSCHNITT 4 – WIE MAN ATLASSIAN ALS USER NUTZT
================================================================================

4.1 Das Atlassian Free Bundle im R+MUNI Kontext
-------------------------------------------------
R+MUNI arbeitet mit dem Atlassian Free Bundle (Jira + Confluence).

Für alle User gilt:
  - Das Free Bundle ist ausreichend für alle R+MUNI Kernfunktionen
  - Kein kostenpflichtiger Plan erforderlich
  - Limits des Free Plans sind bekannt und im Blueprint berücksichtigt

Was das Free Bundle bietet:
  - Jira:       Ticketing, Aufgabenverwaltung, strukturierte Register
  - Confluence: Dokumentation, Wissensbasis, Berichte
  - Verknüpfung zwischen beiden Tools

Was das Free Bundle nicht bietet:
  - Erweiterte Automatisierungen (nur in kostenpflichtigen Plänen)
  - Erweiterte Reporting-Funktionen
  - Mehr als 10 User ohne Upgrade


4.2 Wie man Jira sinnvoll für R+MUNI nutzt
--------------------------------------------
Jira im R+MUNI Kontext ist kein klassisches Projektmanagement-Tool.
Es ist ein strukturiertes Register für Architektur-Objekte und Prozesse.

Grundregel:
  Jira-Issues repräsentieren Architektur-Objekte — keine Aufgaben.
  Aufgaben und Tickets sind ein separater Anwendungsfall.

Empfohlene Nutzung:
  - Architektur-Objekte aus R+MUNI via Import in Jira bringen
  - Jira als Suchmaschine für die eigene Architektur nutzen
  - Über Confluence live auf Jira-Daten zugreifen

Nicht empfohlen:
  - Manuelle Pflege von Jira-Issues parallel zum Architekturmodell
  - Jira als Ersatz für das Architekturmodell verwenden
  - Issues ohne Importbezug anlegen (erzeugt Inkonsistenz)


4.3 Wie man Confluence sinnvoll für R+MUNI nutzt
--------------------------------------------------
Confluence ist im R+MUNI Kontext die Präsentations- und Kommunikationsebene.

Was in Confluence gehört:
  - Berichte und Übersichten die aus R+MUNI abgeleitet werden
  - Prozessdokumentation für das Team
  - Live-Tabellen mit Jira-Verknüpfung
  - Entscheidungsdokumentation

Was nicht in Confluence gehört:
  - Das Architekturmodell selbst
  - Rohdaten aus dem Blueprint
  - Technische Konfigurationsdetails

Strukturempfehlung für neue Confluence-Spaces:
  - Ein Space pro Hauptthema (Architektur, Prozesse, IMS, etc.)
  - Klare Seitenstruktur von Anfang an — schwer im Nachhinein zu ändern
  - Berechtigungen früh definieren — nicht erst wenn Probleme entstehen


4.4 Atlassian-Support für User
--------------------------------
R+MUNI unterstützt bei Basis-Fragen rund um das Atlassian Free Bundle
im Rahmen der verfügbaren Kapazität.

Für komplexe Atlassian-Themen gilt:
  - Atlassian ist nicht das Kerngeschäft von R+MUNI
  - Bei Bedarf werden spezialisierte Atlassian-Experten vermittelt
  - Kein User wird zu einem kostenpflichtigen Atlassian-Plan gedrängt

Support-Anfragen über das Portal:
  https://ims-blueprint-ticketsystem.atlassian.net/helpcenter/RMNP/


4.5 Typische Anfängerfehler und wie man sie vermeidet
------------------------------------------------------
  FEHLER: Alles in einem Jira-Projekt anlegen
  → Unterschiedliche Anwendungsfälle brauchen eigene Projekte
  → Architektur-Register, Sprint-Backlog und Bug-Tracking trennen

  FEHLER: Confluence als Word-Ersatz nutzen
  → Confluence lebt von Verlinkungen und Live-Daten
  → Statische Seiten ohne Verknüpfung verschenken das Potenzial

  FEHLER: Berechtigungen ignorieren bis es zu spät ist
  → Free Plan hat eingeschränkte Berechtigungsoptionen
  → Von Anfang an überlegen wer was sehen und bearbeiten darf

  FEHLER: Inhalte manuell pflegen statt strukturiert zu importieren
  → Führt zu Inkonsistenz zwischen Modell und Jira
  → Import-Mechanismus von R+MUNI konsequent nutzen


================================================================================
ABSCHNITT 5 – WIE MAN FEEDBACK SINNVOLL EINBRINGT
================================================================================

5.1 Feedback ist kein Angriff — es ist Rohstoff
-------------------------------------------------
R+MUNI lebt von Feedback aus der Praxis.

Gutes Feedback beschreibt:
  - Was konkret nicht funktioniert hat (nicht: "es geht nicht")
  - In welchem Kontext das Problem aufgetreten ist
  - Was erwartet wurde und was stattdessen passiert ist
  - Ob es ein einmaliges oder wiederkehrendes Problem ist

Schlechtes Feedback (wenig hilfreich):
  - "Das Tool ist kompliziert"
  - "Das hat nicht funktioniert"
  - "Ich verstehe das nicht"

Gutes Feedback (hilfreich):
  - "Beim Import erscheint Fehler X wenn Bedingung Y vorliegt"
  - "Schritt Z in der Anleitung ist unklar weil Voraussetzung W fehlt"
  - "Feature X fehlt mir weil ich Anwendungsfall Y damit nicht abdecken kann"


5.2 Der richtige Kanal
-----------------------
Feedback wird ausschließlich über das R+MUNI Portal eingebracht:
  https://ims-blueprint-ticketsystem.atlassian.net/helpcenter/RMNP/

Drei Request-Typen stehen zur Verfügung:
  Bug            → Etwas funktioniert nicht wie beschrieben
  Feature Request → Etwas fehlt das ich brauche
  DEV Anfrage    → Ich brauche Unterstützung bei einem spezifischen Thema

Kein E-Mail, kein Direktkontakt als Standardweg.
Das Portal sichert dass kein Feedback verloren geht.


5.3 Was mit Feedback passiert
-------------------------------
Feedback wird gelesen und bewertet.

Es gibt keine SLA und kein Versprechen zur Umsetzung.
Was es gibt:
  - Ehrliche Rückmeldung ob und wann etwas umgesetzt werden kann
  - Transparenz über Kapazität und Prioritäten
  - Keine implizite Zusage durch Annahme des Feedbacks

Feedback das zu einer Verbesserung führt:
  - wird im Blueprint dokumentiert
  - fließt in die USER-Dokumentation ein wenn es allgemeingültig ist
  - wird — wenn möglich — in der Release-Note erwähnt


================================================================================
ASSOCIATE HOW2 | S5 | 2026-03-18
================================================================================
