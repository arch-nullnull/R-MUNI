================================================================================
AI DRIVEN DEVELOPMENT – METHODE R+MUNI
================================================================================
Erstellt    : 2026-03-06
Autor       : Markus Resel
Charakter   : Persönliche Arbeitsmethode / Entwicklungsphilosophie
Ablageort   : 00-concept/01-principles/AI_DRIVEN_DEV_METHODE.txt
================================================================================


================================================================================
1. ZWECK DIESES DOKUMENTS
================================================================================

Dieses Dokument beschreibt die persönliche AI Driven Development Methode
die im Rahmen des R+MUNI Projekts entwickelt und gelebt wird.

Sie ist keine abstrakte Theorie sondern eine aus der Praxis gewachsene
Arbeitsweise die es einem nicht-technischen Entwickler ermöglicht
professionelle Software-Systeme zu entwickeln, zu betreiben und zu
dokumentieren — ohne eigenes Programmierwissen.

Die Methode ist bewusst auf die Person und ihre Arbeitsweise zugeschnitten.
Sie ist kein allgemeingültiges Framework sondern eine persönliche Disziplin.


================================================================================
2. GRUNDPRINZIP
================================================================================

Der Entwickler liefert:
  - Fachliche Tiefe (Domänenwissen, Systemlogik, Entscheidungen)
  - Governance (Regeln, Grenzen, Freigaben)
  - Qualitätskontrolle (Test, Abnahme, Ablage)
  - Kontext (Projektfolder, Dokumentation, Historie)

Die KI (Claude) liefert:
  - Code-Umsetzung
  - Technische Übersetzung von Fachlogik
  - Dokumentation
  - Debugging und Analyse

Kernaussage:
  Der Entwickler denkt das System.
  Die KI schreibt es auf.
  Entscheidungen bleiben immer beim Menschen.


================================================================================
3. RAHMENBEDINGUNGEN
================================================================================

3.1 Persönliches Profil des Entwicklers
-----------------------------------------
  - IT-Erfahrung: Presales Datacenter (20 Jahre),
                  Projektmanagement (6 Jahre),
                  Prozess- & Changemanagement (3 Jahre)
  - IMS-Betreuer: ISO 9001 (vollständig), ISO 27001, ISO 14001 (begleitend)
  - Kein Programmierwissen (kein Code Know-how)
  - GUI-orientiert, CLI kein Komfortbereich
  - Stärke: Systemdenken, Governance, Fachlogik, Domänenwissen

3.2 Werkzeuge
--------------
  - KI: Claude (Anthropic, Pro Plan)
  - Editor: Notepad++
  - Konsole: PowerShell 7
  - Ticketing: Atlassian Jira (Free Plan)
  - Dokumentation: Atlassian Confluence (Free Plan)
  - Versionierung: Projektfolder (manuell, strukturiert)


================================================================================
4. DIE METHODE – SCHRITT FÜR SCHRITT
================================================================================

4.1 Kontext herstellen (Session-Start)
----------------------------------------
Vor jeder Arbeits-Session wird sichergestellt dass Claude den vollständigen
Projektkontext kennt.

Mittel:
  - Projektfolder in Claude Desktop mit allen aktuellen Dokumenten
  - Alle Scripts, Config-Files und Dokumentations-TXTs sind aktuell
  - Bei Bedarf: kurze Kontext-Zusammenfassung im Chat

Prinzip:
  Claude arbeitet nie ohne vollständigen Kontext.
  Ein unvollständiger Kontext führt zu falschen Ergebnissen.

4.2 Problem beschreiben — nicht lösen
---------------------------------------
Der Entwickler beschreibt das Problem in eigenen Worten —
so wie er es versteht, nicht wie ein Techniker es formulieren würde.

Wichtig:
  - Keine technische Vorformulierung nötig
  - Alltagssprache ist ausdrücklich erlaubt
  - Halbfertige Gedanken sind willkommen
  - Claude übersetzt in technische Präzision

Beispiel aus der Praxis:
  "ich hab das problem dass das master.xml alles in den scope nimmt
   obwohl es in run-scope.txt anders definiert ist"
  → Claude analysiert, stellt gezielte Rückfragen, findet den Knoten

4.3 Gemeinsam den Knoten finden
---------------------------------
Claude und der Entwickler erarbeiten gemeinsam das Problem —
im Dialog, nicht durch Monolog.

Vorgehen:
  - Claude erklärt was er versteht
  - Entwickler korrigiert wo nötig
  - Schritt für Schritt zum echten Problem
  - Keine Lösung bevor das Problem klar ist

Typisches Muster:
  Entwickler erklärt → Claude zeichnet auf → Entwickler korrigiert →
  Claude präzisiert → gemeinsames Verständnis → dann erst: Lösung

4.4 Governance vor Code
------------------------
Bevor Code geschrieben wird:
  - Sprint Doku erstellen (GOV-konform)
  - Auslöser klassifizieren (Bugfix oder Feature)
  - Stage-Zuordnung klären (Stage 3 Freeze oder Stage 4)
  - Freigabe explizit erteilen

Prinzip:
  Kein Script ohne dokumentierten Grund.
  Die Dokumentation ist Teil der Arbeit — kein Abschlussartefakt.

4.5 Freigabe erteilen
----------------------
Der Entwickler erteilt explizit Freigabe für:
  - Stage 3 Eingriffe (Bugfix-Ausnahme)
  - Neue Scripts (Stage 4 Features)
  - Änderungen an bestehenden Config-Files

Die Freigabe ist immer bewusst und begründet.
Claude handelt nie ohne Freigabe in kritischen Bereichen.

4.6 Code Review durch Erklärung
---------------------------------
Der Entwickler reviewed Code nicht durch Lesen —
sondern durch Erklärung.

Vorgehen:
  - Claude erklärt was das Script macht (in Alltagssprache)
  - Entwickler prüft ob die Erklärung zur Absicht passt
  - Bei Abweichung: Korrektur und Neuversuch
  - Erst dann: Download und Test

4.7 Testen und Abnehmen
------------------------
  1. Script herunterladen
  2. Lokal ausführen (PowerShell)
  3. Ergebnis prüfen (Logs, Output, Verhalten)
  4. Bei Fehler: Fehlermeldung an Claude, gemeinsames Debugging
  5. Bei Erfolg: Abnahme

4.8 Ablage und Aktualisierung
-------------------------------
Nach erfolgreicher Abnahme:
  1. Altes Script/Dokument ersetzen
  2. Projektfolder aktualisieren
  3. Confluence Dokumentation pflegen
  4. Jira Ticket schließen

Prinzip:
  Was nicht abgelegt ist existiert nicht.
  Routine schlägt Improvisation.


================================================================================
5. KOMMUNIKATIONSPRINZIPIEN MIT CLAUDE
================================================================================

5.1 Sprache
------------
  - Deutsch als Arbeitssprache
  - Alltagssprache ist erlaubt und erwünscht
  - Technische Präzision liefert Claude — nicht der Entwickler
  - Umgangssprache, Halbsätze, Gedankensprünge sind normal

5.2 Erklärungsprinzip
----------------------
  - Schritt-für-Schritt Erklärungen immer
  - Kommandozeilen immer mit Erklärung
  - Konkrete Beispiele bevorzugen
  - Keine Annahmen über Vorwissen

5.3 Dialogführung
------------------
  - Entwickler unterbricht wenn etwas unklar ist
  - Claude fragt nach bevor er annimmt
  - Missverständnisse werden sofort aufgelöst
  - Kein "ich mache jetzt einfach mal" ohne Freigabe

5.4 Grenzen kennen
-------------------
  Claude kennt und respektiert:
  - Stage 3 Freeze (kein Eingriff ohne Bugfix-Freigabe)
  - Governance Regeln (GOV-konform handeln)
  - 1 Script 1 Outcome Prinzip
  - Keine Automatisierung ohne expliziten Auftrag


================================================================================
6. KONTEXTMANAGEMENT
================================================================================

6.1 Projektfolder als gemeinsame Wahrheit
-------------------------------------------
Der Projektfolder in Claude Desktop enthält:
  - Alle aktuellen Scripts (.py)
  - Alle Config-Files (.txt)
  - Alle Dokumentations-Dateien (.txt)
  - Stage-Dokumente (Freeze, Ziele)
  - Sprint Dev-Dokumentationen

Prinzip:
  Was im Projektfolder ist — das weiß Claude.
  Was nicht drin ist — muss im Chat erklärt werden.

6.2 Aktualisierungszyklus
---------------------------
  Nach jeder Session mit Änderungen:
  - Geänderte Dateien in Projektfolder ersetzen
  - Neue Dateien hinzufügen
  - Veraltete Dateien entfernen

  Nicht lesbare Formate (.xlsx) werden nicht im Projektfolder abgelegt.
  Mappings und Konfigurationen immer als .txt.

6.3 Session-Ende
-----------------
  Jede Session endet mit:
  - Klarem Stand (was wurde erreicht)
  - Offenen Punkten (was kommt als nächstes)
  - Aktualisierten Dateien im Projektfolder


================================================================================
7. QUALITÄTSSICHERUNG
================================================================================

7.1 Vier-Augen-Prinzip
-----------------------
  Jede Lösung wird von Claude erklärt und vom Entwickler
  inhaltlich abgenommen — auch ohne technisches Verständnis
  des Codes selbst.

  Der Entwickler prüft:
  - Passt die Erklärung zur Absicht?
  - Ist die Governance eingehalten?
  - Ist die Stage-Zuordnung korrekt?
  - Ist die Rückwärtskompatibilität gegeben?

7.2 Testpflicht
----------------
  Kein Script gilt als fertig ohne lokalen Testlauf.
  Logs werden gelesen und interpretiert (mit Claude-Unterstützung).

7.3 Dokumentationspflicht
---------------------------
  Kein Sprint ohne Sprint-Doku.
  Kein Stage-Ende ohne vollständige Dokumentation.
  Dokumentation ist Bestandteil der Leistung — nicht Nacharbeit.


================================================================================
8. STÄRKEN DIESER METHODE
================================================================================

  + Kein Programmierwissen erforderlich
  + Domänenwissen des Entwicklers bleibt führend
  + Governance und Qualität bleiben beim Menschen
  + Schnelle Umsetzung durch KI-Unterstützung
  + Vollständige Nachvollziehbarkeit durch Dokumentation
  + Reproduzierbar und übertragbar
  + Skalierbar auf unterschiedliche Domänen
  + Offen für Weiterentwicklung (Stages, Sprints)


================================================================================
9. GRENZEN DIESER METHODE
================================================================================

  - KI-Verfügbarkeit als Abhängigkeit (kein Internet = kein Entwickeln)
  - Kontextfenster der KI begrenzt (Projektfolder-Disziplin notwendig)
  - Keine automatische Versionierung (manuelle Disziplin erforderlich)
  - Testing bleibt beim Entwickler (KI kann nicht lokal testen)
  - Komplexe Fehlerbilder benötigen gute Fehlerbeschreibung


================================================================================
10. WEITERENTWICKLUNG
================================================================================

Diese Methode ist lebendig und wird mit dem Projekt weiterentwickelt.
Erkenntnisse aus der Praxis fließen in dieses Dokument ein.

Änderungen an dieser Methode folgen denselben Governance-Regeln
wie alle anderen Dokumente im R+MUNI Blueprint.


================================================================================
END OF DOCUMENT
AI Driven Development – Methode R+MUNI | 2026-03-06
================================================================================
