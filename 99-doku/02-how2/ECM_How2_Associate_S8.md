================================================================================
ECM – EasyCSVMapper – HOW2 (Associate)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : ECM_How2_Associate_S6
Tag             : #associate #how2 #ecm #easycsvmapper #s6 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-21
Ablageort       : R+MUNI Doku-public\02-how2\ECM_How2_Associate_S6.md
================================================================================


VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- R+MUNI ist installiert und läuft auf deinem Rechner
- Archi 5.8 ist installiert
- Du hast eine externe CSV-Datei die du ins Modell bringen möchtest
- Du weißt grob welche Spalten der CSV welchen Bedeutungen entsprechen
  (z.B. "Spalte Buchungstext = das ist der Prozessname")


================================================================================
ABSCHNITT 1 – ERWARTUNGSMANAGEMENT
================================================================================

1.1 Was dir dieser Ablauf ermöglicht
--------------------------------------
Mit diesem Ablauf kannst du:
  - Eine beliebige externe CSV-Datei (z.B. Excel-Export, Systemexport)
    sauber in dein ArchiMate-Modell importieren
  - Selbst festlegen welche Spalten zu Modellelementen werden und
    welche als Attribute (Properties) an Elementen hängen
  - Denselben Import jederzeit wiederholen wenn neue Daten kommen —
    ohne den Einrichtungsaufwand nochmal zu haben

Was dieser Ablauf nicht leistet:
  - Automatische Erkennung was eine Spalte "bedeutet" — das entscheidest du
  - Vollautomatischer Import ohne manuelle Schritte in Archi —
    zwei Archi-Schritte bleiben manuell
  - Import von Excel-Dateien direkt — die CSV muss vorliegen

Realistischer Aufwand:
  - Erstmaliger Einrichtungsaufwand (Phase 1):   30–60 Minuten
  - Wiederholter Import (Phase 2):               5–10 Minuten


1.2 Der richtige Einstieg
--------------------------
Nicht einfach die CSV umbenennen und das Script starten — zuerst überlegen:
  - Welche Spalte wird zum Hauptelement im Modell?
  - Welche Spalten sind Attribute dieses Elements?
  - Welche Spalten werden eigenständige Elemente?

Häufiger Fehler beim Einstieg:
  Die CSV direkt importieren ohne Mapping-Modell.
  Ergebnis: Alle Spalten landen als gleichwertige Objekte — keine Struktur.
  Besser: Erst Phase 1 einmalig durchlaufen — dann ist jeder spätere
          Import automatisch strukturiert.


================================================================================
ABSCHNITT 2 – PHASE 1: EINMALIGE EINRICHTUNG
================================================================================

2.1 Was in Phase 1 passiert
-----------------------------
Du zeigst R+MUNI einmalig wie deine CSV-Struktur ins Modell übersetzt werden
soll. Das Ergebnis ist ein Mapping-Modell in Archi — eine Art "Übersetzungsregel"
die bei jedem späteren Import automatisch angewendet wird.

Beispiel:
  Deine CSV hat Spalten: Datum, Fälligkeit, Vorschreibung, Zahlung, Buchungstext
  Du entscheidest:
    Buchungstext → wird ein eigenständiges Archi-Element (Artifact)
    Vorschreibung → wird ein eigenständiges Element (Requirement)
    Zahlung → wird ein eigenständiges Element (Goal)
    Datum → wird ein Attribut von Buchungstext
    Fälligkeit → wird ein Attribut von Buchungstext

Warum das so ist:
  ArchiMate-Modelle haben Semantik — nicht alles ist gleichwertig.
  Du definierst einmal die Bedeutung, danach läuft der Import automatisch.


2.2 Schritt-für-Schritt — Phase 1
-----------------------------------
Schritt 1: CSV vorbereiten
  Benenne deine CSV-Datei um — sie muss mit trash_ beginnen:
    Beispiel: trash_rechnungen.csv
  Leg die Datei ab unter:
    01-artifacts\02-csv\03-child\00-archimatechild\
  Du siehst danach: Die Datei liegt im richtigen Ordner.

Schritt 2: Strukturerkennung starten
  Öffne PowerShell und wechsle in den Scripts-Ordner:
    cd <rootfolder>\01-artifacts\01-scripts
  Führe aus:
    py .\ECM00-validate_environment.py
    py .\ECM01-csv_fields_to_artifacts.py
  Du siehst danach: Beide Scripts laufen durch ohne Fehler.
  Ergebnis: In 01-artifacts\02-csv\04-import\ liegt eine elements.csv
            mit allen Spaltenköpfen deiner CSV als Einträge.

Schritt 3: Struktur in Archi importieren
  Öffne Archi.
  Gehe zu: File → Import → CSV
  Wähle den Ordner: 01-artifacts\02-csv\04-import\
  Bestätige den Import.
  Du siehst danach: Deine Spaltenköpfe erscheinen als Artifact-Elemente
                    im Modell.

Schritt 4: Mapping-Modell in Archi bauen
  Das ist der kreative Schritt — du entscheidest die Bedeutung:

  a) Elemente auf richtige Typen umwandeln:
     Klicke auf ein Element (z.B. "Buchungstext")
     Ändere den Typ auf den gewünschten ArchiMate-Typ
     Wiederhole für alle Elemente

  b) Attribute verbinden:
     Für Spalten die Attribute sein sollen (z.B. Datum, Fälligkeit):
     Ziehe eine Association-Linie vom Attribut-Element zum Hauptelement
     Beispiel: Datum ──→ Buchungstext

  Du siehst danach: Ein übersichtliches Modell das zeigt welche Spalten
                    Elemente werden und welche Attribute.

Schritt 5: Mapping-Modell exportieren
  Gehe zu: File → Export → Model to Open Exchange XML File
  Speichere die Datei unter:
    00-model\00-archimate\99-mappingmodel\
  Dateiname: beliebig, z.B. rechnungen_mapping.xml
  Du siehst danach: Die XML-Datei liegt im Mapping-Modell-Ordner.

Schritt 6: run-scope.txt ergänzen
  Öffne die Datei 02-stages\run-scope.txt in Notepad++
  Füge am Ende hinzu (nach bestehendem Inhalt):
    SOURCE=CSV
    MODEL=trash_rechnungen.csv
    MAPPING=rechnungen_mapping.xml
  Speichern.
  Du siehst danach: Der Eintrag steht in der Datei.

Phase 1 ist abgeschlossen — ab jetzt läuft jeder Import über Phase 2.


================================================================================
ABSCHNITT 3 – PHASE 2: REGULÄRER IMPORT
================================================================================

3.1 Was in Phase 2 passiert
-----------------------------
Phase 2 ist der eigentliche Import — du bringst die aktuellen Daten aus
deiner CSV ins Modell. Das Mapping aus Phase 1 wird automatisch angewendet.

Phase 2 besteht aus zwei Script-Läufen mit einem manuellen Archi-Schritt
dazwischen. Das ist nötig weil Archi die IDs der Elemente erst beim
Import vergibt — die Properties brauchen diese IDs.


3.2 Schritt-für-Schritt — Phase 2
-----------------------------------
Schritt 1: Neue CSV bereitstellen
  Leg deine aktuelle CSV (mit Prefix trash_) ab unter:
    01-artifacts\02-csv\03-child\00-archimatechild\
  Achtung: Nur eine trash_*.csv darf im Ordner liegen.

Schritt 2: Ersten Script-Lauf starten
  Öffne PowerShell im Scripts-Ordner und führe aus:
    py .\ECM00-validate_environment.py
    py .\ECM02-csv_to_mapping_to_csv.py
  Du siehst danach: Beide Scripts laufen durch ohne Fehler.
  Ergebnis: In 04-import\ liegt elements.csv mit den Modellelementen.
            In 02-stages\00-archimatearchive\ liegen properties.csv
            und relations.csv (noch ohne IDs — das ist normal).

Schritt 3: Elemente in Archi importieren
  Öffne Archi.
  Gehe zu: File → Import → CSV
  Wähle den Ordner: 01-artifacts\02-csv\04-import\
  Bestätige den Import.
  Du siehst danach: Die Elemente aus deiner CSV sind im Modell —
                    Archi hat ihnen jetzt stabile IDs vergeben.

  WICHTIG: Ab jetzt keine Elemente umbenennen bis Schritt 6 abgeschlossen!

Schritt 4: Elemente aus Archi exportieren
  Bleib in Archi.
  Gehe zu: File → Export → CSV
  Speichere in denselben Ordner: 01-artifacts\02-csv\04-import\
  Bestätige — bestehende Dateien werden überschrieben (das ist gewollt).
  Du siehst danach: elements.csv in 04-import\ enthält jetzt die IDs
                    die Archi vergeben hat.

Schritt 5: ID-Merge durchführen
  Zurück in PowerShell:
    py .\ECM03-id_merge.py
  Du siehst danach: Script läuft durch ohne Fehler.
  Ergebnis: In 04-import\ liegen jetzt properties.csv und relations.csv
            mit den korrekten IDs.

Schritt 6: Properties und Relations importieren
  Zurück in Archi.
  Gehe zu: File → Import → CSV
  Wähle wieder: 01-artifacts\02-csv\04-import\
  Bestätige den Import.
  Du siehst danach: Die Attribute (Properties) sind jetzt korrekt
                    den richtigen Elementen zugeordnet.

Import abgeschlossen — deine Daten sind im Modell.


================================================================================
TYPISCHE STOLPERFALLEN
================================================================================

  STOLPERFALLE: Zwei trash_*.csv Dateien im Ordner
  → Was dann passiert: ECM01 oder ECM02 bricht mit Fehlermeldung ab
  → Besser: Immer nur eine trash_*.csv im Ordner lassen —
            die andere vorher entfernen oder umbenennen

  STOLPERFALLE: Element in Archi umbenennen zwischen Schritt 3 und 5
  → Was dann passiert: Properties landen am falschen Element —
                       kein sichtbarer Fehler, aber falsche Daten
  → Besser: Erst nach Schritt 6 umbenennen

  STOLPERFALLE: MAPPING= ohne .xml Endung in run-scope.txt
  → Was dann passiert: ECM02 meldet "OEF XML nicht gefunden"
  → Besser: MAPPING=rechnungen_mapping.xml (mit .xml, nicht ohne)

  STOLPERFALLE: Archi CSV-Export vergessen vor ECM03
  → Was dann passiert: ECM03 meldet Fehler — elements.csv ohne IDs
  → Besser: Schritt 4 (Export) nicht überspringen —
            ECM03 braucht den frischen Export mit IDs

  STOLPERFALLE: CSV hat Sonderzeichen und Umlaute werden falsch dargestellt
  → Was dann passiert: Spaltenköpfe oder Werte erscheinen mit Fragezeichen
  → Besser: Script erkennt Encoding automatisch — wenn es trotzdem
            nicht stimmt, bitte über das Portal melden


================================================================================
NÄCHSTE SCHRITTE
================================================================================

Wenn du Phase 2 erfolgreich abgeschlossen hast:
  → Deine Daten sind stabil im Modell mit IDs
  → Du kannst jetzt die XML-Reihe nutzen wenn du das Modell
    in den XML-Flow einbinden möchtest
  → Bei Bedarf: Elemente jetzt umbenennen oder weiter modellieren

Wenn du den Import regelmäßig durchführst:
  → Phase 1 muss nicht wiederholt werden
  → Nur Phase 2 — das dauert 5–10 Minuten


================================================================================
SUPPORT UND FEEDBACK
================================================================================

Etwas funktioniert nicht wie beschrieben oder du hast einen Verbesserungsvorschlag?

Feedback über das R+MUNI Portal:
  https://ims-blueprint-ticketsystem.atlassian.net/helpcenter/RMNP/

Bitte beschreibe:
  - Was du versucht hast
  - Was du erwartet hättest
  - Was stattdessen passiert ist


================================================================================
ECM_How2_Associate | S6 | 2026-03-21 | R+MUNI Blueprint
================================================================================
