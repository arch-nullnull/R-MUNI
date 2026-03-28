================================================================================
TMP DOKUMENTTYPEN — HOW2 (Associate)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : TMP_How2_Associate_S8
Tag             : #associate #how2 #tmp #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : ENTWURF
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Hinweis         : Inhalt initial ident mit DEV-Gegenstück — inhaltliche Trennung in Stage 1
================================================================================

Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-18
Ablageort       : R+MUNI Doku-public\02-how2\TMP_How2_DEV_S6.md
================================================================================


VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- [[TMP_principles_S6]] gelesen und verstanden
- [[Global_GOV_S8]] bekannt — insbesondere Kapitel 10 (Sprint-Governance)
- Zugriff auf R+MUNI Doku-internal (sprints-Ordner) vorhanden
- Zugriff auf R+MUNI Doku-public vorhanden
- GitHub Sync eingerichtet und funktionsfähig


================================================================================
ÜBERSICHT
================================================================================

Diese How2 beschreibt wie DEV-Mitglieder Dokumente des R+MUNI Blueprint
korrekt erstellen, pflegen und freigeben.

Sie deckt ab:
  - Welches Template für welchen Anwendungsfall
  - Wo ein Dokument in Arbeit lebt
  - Wie ein Dokument freigegeben und publiziert wird
  - Was beim Ausfüllen eines Templates zu beachten ist

Sie deckt nicht ab:
  - Den inhaltlichen Aufbau der einzelnen Templates
    (→ DEV-Hinweisblock im jeweiligen Template)
  - Governance-Regeln des Gesamtsystems
    (→ [[Global_GOV_S8]])


================================================================================
SCHRITT 1 – DOKUMENTTYP BESTIMMEN
================================================================================

Vor jedem neuen Dokument: Typ klären.

  Ich will verbindliche Regeln festlegen             →  Type 1: GOV_Global
  Ich will Leitprinzipien einer Reihe beschreiben    →  Type 2: principles
  Ich will eine Anleitung erstellen                  →  Type 3: how2
  Ich will R+MUNI auf TOGAF / ArchiMate mappen       →  Type 4: Rosetta-Stone
  Ich will einen stabilen Stand einfrieren           →  Type 5: FREEZE
  Ich will Ziele eines Stage definieren              →  Type 6: Stage_Ziele
  Ich will einen abgeschlossenen Sprint dokumentieren →  Type 7: Sprint-DEV-Doku
  Ich will einen künftigen Sprint vorplanen          →  Type 8: Sprint-DEV-BACKLOG
  Ich brauche ein erklärendes Dokument ohne Typ      →  Type 9: Info (frei)
  Ich erstelle ein Creative Asset                    →  Type 10: Creative (frei)

Zweifelsfälle:
  Mehr als ein Typ trifft zu       →  Dokument aufteilen — ein Dokument, ein Typ
  Kein Typ trifft zu               →  Type 9 Info verwenden
  Neuer Typ scheint nötig          →  [[Global_GOV_S8]] prüfen, Betreiber fragen


================================================================================
SCHRITT 2 – RICHTIGES TEMPLATE ÖFFNEN
================================================================================

Templates liegen in:
  R+MUNI Doku-internal\infocfg\   (oder nach Ablageentscheidung des Betreibers)

Template je Typ:

  Type 1   GOV_Global_Template_S6.md
  Type 2   principles_Template_S6.md
  Type 3   how2_DEV_Template_S6.md     (für DEV / Poweruser)
           how2_USER_Template_S6.md    (für Anwender — aus Beta-Erfahrungen)
  Type 4   Rosetta-Stone_Template_S6.md
  Type 5   FREEZE_Template_S6.md       (nur auf Wunsch Betreiber / Stage-Ende)
  Type 6   Stage_Ziele_Template_S6.md
  Type 7   Sprint-DEV-Doku_Template_S6.md
  Type 8   Sprint-DEV-BACKLOG_Template_S6.md
  Type 9   Kein Template — Format frei
  Type 10  Kein Template — Format frei

Vorgehen:
  1. Template kopieren — niemals das Original bearbeiten
  2. Kopie in R+MUNI Doku-internal\sprints\ ablegen
  3. Dateinamen nach Konvention setzen (→ Schritt 3)


================================================================================
SCHRITT 3 – DATEI KORREKT BENENNEN
================================================================================

Benennungskonvention je Typ:

  Type 1   GOV_<TITEL>_S<N>.md
           Beispiel: GOV_Kunden_S6.md

  Type 2   <REIHE>_principles_S<N>.md
           Beispiel: CSV_principles_S6.md

  Type 3   <REIHE>_How2_DEV_S<N>.md  /  <REIHE>_How2_USER_S<N>.md
           Beispiel: CSV_How2_DEV_S6.md

  Type 4   Rosetta-Stone_<THEMA>_S<N>.md
           Beispiel: Rosetta-Stone_Phase-A_S6.md

  Type 5   FREEZE-<Stagenummer>_S<N>.md
           Beispiel: FREEZE-6_S6.md

  Type 6   Stage<Nummer>_Ziele_S<N>.md
           Beispiel: Stage7_Ziele_S6.md

  Type 7   Sprint-DEV-<BEZEICHNUNG>_S<N>.md
           Beispiel: Sprint-DEV-CSV-Refactoring_S6.md

  Type 8   Sprint-DEV-BACKLOG_<BEZEICHNUNG>_S<N>.md
           Beispiel: Sprint-DEV-BACKLOG_BPMN-Flows_S6.md

Stage-Suffix:
  <N> = Stage in dem das Dokument erstellt wird
  Beispiel: Dokument erstellt in Stage 6 → _S6
  Der Suffix ist DEV-intern — er entfällt in der Release-Version (Cleaning Run)


================================================================================
SCHRITT 4 – DOKUMENT AUSFÜLLEN
================================================================================

Reihenfolge beim Ausfüllen:
  1. Header vollständig ausfüllen (Datum, Stage, Ablageort, Verantwortlich)
  2. DEV-Hinweisblock lesen — er enthält die Spielregeln für diesen Typ
  3. Platzhalter in <GROSSBUCHSTABEN> ersetzen
  4. Optionale Kapitel: behalten wenn relevant, entfernen wenn nicht
  5. DEV-Hinweisblock am Ende entfernen

Pflichtregeln beim Ausfüllen:
  - Ein Dokument behandelt genau ein Thema
  - Formstabilität hat Vorrang — Struktur nicht eigenmächtig ändern
  - Obsidian-Links dort einsetzen wo echte Bezüge bestehen
  - Keine leeren Platzhalter im fertigen Dokument lassen
  - Kommentarblöcke (<!-- ... -->) vollständig entfernen

Typische Fehler:
  Fehler: Platzhalter <BEZEICHNUNG> stehen lassen
    Lösung: Vor Freigabe vollständig prüfen — kein <> darf im Dokument verbleiben

  Fehler: DEV-Hinweisblock nicht entfernt
    Lösung: Vor Freigabe prüfen — Kommentarblöcke gehören nicht ins fertige Dokument

  Fehler: Optionale Kapitel leer lassen statt entfernen
    Lösung: Leere optionale Kapitel konsequent entfernen

  Fehler: Zwei Themen in einem Dokument
    Lösung: Aufteilen — ein Dokument, ein Typ, ein Thema


================================================================================
SCHRITT 5 – DOKUMENT IN ARBEIT VERWALTEN
================================================================================

Solange ein Dokument in Arbeit ist:
  Ablage:  R+MUNI Doku-internal\sprints\
  Status:  Im Datei-Header als "In Arbeit" oder aktuellen Status kennzeichnen
  Zugriff: Nur DEV-Mitglieder (internal Repo — privat)

Versionierung während der Arbeit:
  Kein eigenes Versioning — der sprints-Ordner ist der Arbeitsbereich
  GitHub Sync des internal Repos sichert den Arbeitsstand

Mehrere DEV-Mitglieder am selben Dokument:
  Abstimmung über Betreiber — kein paralleles Bearbeiten ohne Absprache
  Last-Write-Wins ist keine Strategie


================================================================================
SCHRITT 6 – FREIGABE UND PUBLIZIERUNG
================================================================================

Freigabe ist ein expliziter Akt des Betreibers — kein automatischer Vorgang.

Freigabeprozess:
  1. DEV signalisiert Fertigstellung an Betreiber
  2. Betreiber prüft Konformität mit Template und GOV
  3. Betreiber gibt explizit frei (mündlich oder schriftlich im Chat)
  4. Dokument wird in das public Repo verschoben

Zieldordner je Typ nach Freigabe:

  Type 1   R+MUNI Doku-public\00-governance\
  Type 2   R+MUNI Doku-public\01-principles\
  Type 3   R+MUNI Doku-public\02-how2\
  Type 4   R+MUNI Doku-public\03-rosetta_stone\
  Type 5   R+MUNI Doku-public\04-notes\
  Type 6   R+MUNI Doku-public\04-notes\
  Type 7   R+MUNI Doku-public\04-notes\
  Type 8   R+MUNI Doku-internal\backlog\     ← bleibt internal
  Type 9   R+MUNI Doku-internal\infocfg\    ← bleibt internal
  Type 10  R+MUNI Doku-creative\            ← eigenes Repo, Sales + DEV

Nach Freigabe:
  - Dokument ist unveränderlich
  - Änderungen nur durch explizite Stage-Entscheidung des Betreibers
  - Original im sprints-Ordner kann archiviert oder gelöscht werden


================================================================================
SCHRITT 7 – JIRA-SYNC FÜR BACKLOG (NUR TYPE 8)
================================================================================

Sprint-DEV-BACKLOG Dokumente werden im DEV-Modus nach Jira gespiegelt.

Vorgehen:
  1. Backlog-Dokument fertiggestellt in R+MUNI Doku-internal\backlog\
  2. Jira-Ticket anlegen mit Inhalt aus Kapitel 2 (Ziel) und 3 (Mehrwert)
  3. Ticket-ID im Dokument-Header unter "Jira-Sync" eintragen
  4. Statusänderungen im Dokument und Jira synchron halten

Jira-Ticket-Felder:
  Titel:        Sprint-Bezeichnung aus Dokument
  Beschreibung: Ziel + Fachlicher Mehrwert
  Status:       analog Kapitel 8 (Status und Verlauf) im Dokument
  Label:        BACKLOG


================================================================================
BEZÜGE
================================================================================

[[TMP_principles_S6]]               Dokumenttypen — Zweck, Regeln, Ablage
[[Global_GOV_S8]]                   normative Grundlage — insbesondere Kapitel 10


================================================================================
TMP_How2_DEV | S6 | 2026-03-18 | R+MUNI Blueprint
================================================================================
