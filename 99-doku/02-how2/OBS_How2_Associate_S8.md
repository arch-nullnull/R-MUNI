================================================================================
OBS – Obsidian im Blueprint nutzen — HOW2 (Associate)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : OBS_How2_Associate_S6
Tag             : #associate #how2 #obs #obsidian #s6 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-21
Ablageort       : R+MUNI Doku-public\02-how2\OBS_How2_Associate_S6.md
================================================================================


VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- Du hast Zugriff auf R+MUNI Blueprint (Repos oder Dokumentation)
- Du willst verstehen wie Dokumentation und Bilder zusammenhängen
- [[OBS_How2_DEV_S8]] hast du nicht nötig — das ist nur für Developer
- Du hast grundsätzlich keine Angst vor Tools — aber auch kein Deep-Wissen nötig


================================================================================
ABSCHNITT 1 – ERWARTUNGSMANAGEMENT
================================================================================

1.1 Was dieser How2 dir ermöglicht
-----------------------------------

Mit diesem How2 kannst du:
  - Obsidian öffnen und dich im Blueprint orientieren
  - Dokumente finden die zusammenhängen
  - Diagramme und Bilder direkt im Blueprint sehen
  - Verstehen wie alles verlinkt ist

Was dieser How2 nicht leistet:
  - Dich zum Obsidian-Experten ausbilden
  - Neue Diagramme erstellen (das machen Developer)
  - Code schreiben oder ändern

Realistischer Aufwand:
  - Installation und erste Orientierung:  10–15 Minuten
  - Effektives Nutzen:                     nach wenigen Sessions


1.2 Der richtige Einstieg
--------------------------

Nicht mit der Maus anfangen — mit der Frage anfangen:
  - "Wo hängt dieses Dokument mit anderen zusammen?"
  - "Welche Bilder und Diagramme helfen mir zu verstehen?"
  - "Wie kann ich die Struktur des Blueprint sehen?"

Häufiger Fehler beim Einstieg:
  User klickt wild auf Links ohne zu wissen wo sie sind.
  Ergebnis: Verloren im Netzwerk von Dokumenten.
  Besser: Mit einer klaren Frage starten — dann den Links folgen.


================================================================================
ABSCHNITT 2 – OBSIDIAN INSTALLIEREN
================================================================================

2.1 Was ist Obsidian?
---------------------

Obsidian ist ein kostenloses Programm das Markdown-Dokumente (die gleichen
wie im Blueprint) auf deinem Computer liest und ansprechend darstellt.

Besonderheit: Obsidian zeigt wie Dokumente zusammenhängen.
  → Du siehst nicht nur einzelne Dokumente
  → Du siehst auch welche Dokumente miteinander verlinkt sind
  → Du siehst visuelle Diagramme und Bilder direkt

Das ist wie der Unterschied zwischen:
  "Ein Buch lesen" vs. "Ein Buch lesen + alle Querverweise sehen"


2.2 Obsidian herunterladen und installieren
---------------------------------------------

Schritt 1: Obsidian öffnen
  Gehe zu obsidian.md
  Klick auf "Download"
  Installiere wie jedes andere Programm
  Starte Obsidian
  Du siehst: Ein leeres Fenster mit "Choose a folder"

Schritt 2: Ordner wählen (der Blueprint)
  Klick auf "Browse"
  Navigiere zu dem Ordner wo R+MUNI liegt
  WICHTIG: Wähle den Parent-Ordner — nicht einen Unterordner
           (Das ist der Ordner in dem R+MUNI, R+MUNI Doku-public
            und R+MUNI Doku-internal nebeneinander liegen)
  Klick "Öffnen"
  Du siehst: Obsidian zeigt alle Dokumentationen auf der linken Seite

Schritt 3: Fertig — Obsidian ist bereit
  Der Blueprint ist jetzt in Obsidian geladen
  Du kannst navigieren, lesen, Bilder sehen


================================================================================
ABSCHNITT 3 – NAVIGIEREN IM BLUEPRINT
================================================================================

3.1 Grundidee: Links sind wie Wegweiser
---------------------------------------

Im Blueprint gibt es viele Links zwischen Dokumenten.
Ein Link sieht so aus:  [[Global_GOV_S8]]

Das bedeutet: "Schau dir auch GOV_Global_S6 an — es hängt damit zusammen"

Wenn du einen Link siehst:
  Klick drauf → du landest im verknüpften Dokument
  Ein Zurück-Button bringt dich zurück

Beispiel aus der Praxis:
  Du liest ein How2-Dokument
  Am Ende siehst du:  [[OBS_How2_DEV_S8]] — das ist für Developer
  Und:               [[FREEZE-6]] — der aktuelle Stand des Blueprint
  Klick auf einen Link wenn du mehr wissen willst


3.2 Bilder und Diagramme finden
-------------------------------

Der Blueprint hat viele Diagramme (SVG und PNG).

Sie sehen im Obsidian so aus:
  Ein Bild wird direkt im Dokument angezeigt — nicht nur als Link

Wenn du ein Diagramm siehst:
  → Es zeigt meistens wie etwas zusammenhängt
  → Z.B. ein Feedbackfluss oder die Architektur

Die Bilder sind beschriftet — du siehst sofort worum es geht.

Wenn ein Bild nicht angezeigt wird:
  Das ist selten — aber könnte technische Gründe haben
  Merk dir einfach den Namen und frag im Portal nach


3.3 Graph-View: Die Übersicht aller Verbindungen
-------------------------------------------------

Das beste Feature von Obsidian ist die Graph-View.
Das ist wie eine Karte des Blueprint — du siehst alles auf einen Blick.

Graph-View öffnen:
  Rechts oben im Fenster → kleine Icons
  Such das Icon das wie ein Netzwerk aussieht
  Klick drauf
  Du siehst: Alle Dokumente als Punkte, alle Verbindungen als Linien

Was du siehst:
  Große Hubs (viele Verbindungen): Das sind wichtige Dokumente
                                   (wie GOV und FREEZE)
  Einzelne Punkte: Das sind spezialisierte Dokumente
  Linien: Das sind die Verbindungen

Du kannst mit der Maus:
  → Zoomen (Mausrad)
  → Verschieben (Klick + ziehen)
  → Auf Punkte klicken um zum Dokument zu gehen

Oben rechts gibt es Filter — wenn du nur bestimmte Dokumente sehen willst
(z.B. nur How2-Dokumente)


================================================================================
ABSCHNITT 4 – ALLTAGSNUTZUNG
================================================================================

4.1 Ein Dokument schnell finden
-------------------------------

Schritt 1: Strg+O drücken (oder Cmd+O auf Mac)
  Ein Suchfenster öffnet sich
  Du siehst eine Liste aller Dokumente

Schritt 2: Name tippen
  Tippe die ersten Buchstaben des Dokumentnamens
  Z.B. "HOW2" um alle How2-Dokumente zu sehen
  Du siehst: Die Dokumente filtern sich live

Schritt 3: Rauf/Runter Pfeile, dann Enter
  Wähle das Dokument das du willst
  Enter drücken — du bist jetzt drin

Ergebnis: Du siehst das Dokument mit allen Bildern und Links


4.2 Ein Thema erforschen
------------------------

Beispiel: Du willst wissen wie Feedback funktioniert.

Schritt 1: Öffne ein Dokument zu diesem Thema
  Z.B. [[HOW2_Feedbackschleifen_S6]]

Schritt 2: Lese das Dokument
  Bilder helfen dir zu verstehen
  Links am Ende zeigen verwandte Themen

Schritt 3: Folge den Links wenn dich etwas interessiert
  Klick auf [[FREEZE-6]] um den aktuellen Stand zu sehen
  Klick auf [[Global_GOV_S8]] um die Regeln zu verstehen

Schritt 4: Nutze die Graph-View
  Öffne Graph-View (Icon oben rechts)
  Du siehst alle Dokumente die damit zusammenhängen
  Klick auf Punkte um sie zu erkunden


4.3 Offline arbeiten
--------------------

Obsidian braucht keine Internet-Verbindung!

Das ist praktisch wenn du:
  → Im Zug oder Flugzeug arbeitest
  → In einem Bereich ohne Internet bist
  → Einfach den Blueprint offline haben willst

Wichtig: Änderungen sparst du lokal.
Wenn du Änderungen machen willst (Entwickler-Aufgabe):
  → Das machst du nicht im Obsidian
  → Du arbeitest mit GitHub wie üblich
  → Obsidian ist reines Lese- und Orientierungswerkzeug


================================================================================
TYPISCHE STOLPERFALLEN
================================================================================

  STOLPERFALLE: "Ich kann ein Dokument nicht öffnen"
  → Was dann passiert: Obsidian zeigt das Dokument nicht
  → Besser: Prüf ob der Ordner korrekt ausgewählt ist
           (Parent-Ordner mit allen R+MUNI Sub-Ordnern nebeneinander)

  STOLPERFALLE: "Ein Bild wird nicht angezeigt"
  → Was dann passiert: Du siehst einen Link statt des Bildes
  → Besser: Das ist selten — ist wahrscheinlich eine Pfad-Sache
           Frag im Portal nach mit dem Namen des Bildes

  STOLPERFALLE: "Ich bin verloren im Dokumenten-Netzwerk"
  → Was dann passiert: Du klickst irgendwelchen Links und weißt nicht
                       mehr wo du bist
  → Besser: Nutze Graph-View um zu sehen wo du bist
           Oder drück Strg+O um ein bekanntes Dokument zu suchen

  STOLPERFALLE: "Ich will ein Dokument ändern"
  → Was dann passiert: Du klickst drauf aber kannst es nicht ändern
  → Besser: Obsidian ist nur zum Lesen — für Änderungen brauchst du
           GitHub oder kontaktier die Developer direkt


================================================================================
VARIANTEN UND ERWEITERUNGEN
================================================================================

Es gibt zwei Wege Obsidian zu nutzen:

Variante 1 — Casual Reader:
  Du öffnest Obsidian wenn du ein How2 oder Dokument lesen willst.
  Du nutzt die Graph-View um Zusammenhänge zu sehen.
  Du folgst Links um mehr zu verstehen.
  
  Aufwand: Minimal, nur wenn du es brauchst

Variante 2 — Aktive Nutzung (Developer):
  [[OBS_How2_DEV_S8]] lesen
  Du arbeiten mit Frontmatter, erstellst Links, embedest Diagramme
  
  Das ist die Developer-Seite — nicht für normale User


================================================================================
NÄCHSTE SCHRITTE
================================================================================

Wenn du Obsidian jetzt nutzen kannst:
  → [[HOW2_Feedbackschleifen_S6]]    Verstehe wie Feedback fließt
  → [[FREEZE-6]]                      Schau dir den aktuellen Blueprint-Stand an
  → Öffne Graph-View und erkunde      Sehe wie alles zusammenhängt


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
OBS_How2_Associate | S6 | 2026-03-21 | R+MUNI Blueprint
================================================================================
