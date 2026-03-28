================================================================================
TMP – DOKUMENTTYPEN & TEMPLATES – PRINCIPLES
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : TMP_principles_S6
Tag             : #dev #principles #tmp #dokumenttypen #s6 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-18
Ablageort       : R+MUNI Doku-public\01-principles\TMP_principles_S6.md
================================================================================


1. ZWECK UND DESIGNPHILOSOPHIE
--------------------------------------------------------------------------------
Das R+MUNI Dokumentationssystem kennt keine freie Dokumentenform.
Jedes Dokument gehört zu einem definierten Typ — mit festem Zweck,
verbindlicher Struktur und klarer Ablage.

Kernprinzip: Form vor Sprache. Die Struktur eines Dokuments ist nicht
Gegenstand von Interpretation oder Kreativität. Sie ist vorgegeben,
prüfbar und stabil.

Dieses Principles-Dokument beschreibt alle verbindlichen Dokumenttypen
des R+MUNI Blueprints — ihren Zweck, ihre Regeln, ihre Ablage und ihr
Publizierungsverhalten.

Es richtet sich an DEV-Mitglieder die Dokumente erstellen, pflegen
und freigeben.


2. GRUNDREGELN FÜR ALLE DOKUMENTTYPEN
--------------------------------------------------------------------------------
Diese Regeln gelten für jeden Dokumenttyp ohne Ausnahme:

  - Ein Dokument behandelt genau ein klar abgegrenztes Thema.
  - Dokumenttypen dürfen nicht vermischt werden.
  - Jedes Dokument folgt dem verbindlichen Template seines Typs.
  - Abweichungen von der Struktur sind nur zulässig wenn sie
    explizit definiert und dokumentiert sind.
  - Formstabilität hat Vorrang vor sprachlicher Variation.
  - Dokumente mit Stage-Suffix (_S6, _S7 ...) tragen den
    Erstellungszustand als Information für DEV-interne Planung.
    Im öffentlichen Release-Zustand (Beta 1.0+) entfällt der Suffix.
  - Dokumente in Arbeit leben im privaten Repo (sprints-Ordner)
    bis zur expliziten Freigabe durch den Betreiber.
  - Die Freigabe für public ist ein bewusster, expliziter Akt —
    kein automatischer Vorgang.


3. REPO- UND ABLAGELOGIK
--------------------------------------------------------------------------------
R+MUNI nutzt drei getrennte Repositories mit klar definiertem Zweck:

  PUBLIC — R+MUNI Doku-public
    GitHub: https://github.com/arch-nullnull/MLAT-Doku-public
    Zugriff: jeder
    Inhalt:  normative, lernende und freigegeben Dokumentation
    Format:  ausschließlich .md

  INTERNAL — R+MUNI Doku-internal
    GitHub: https://github.com/arch-nullnull/R-MUNI-Doku-internal
    Zugriff: nur dedizierte DEV-Mitglieder
    Inhalt:  Arbeitsdokumentation, Backlog, Info, Sprints in Arbeit
    Format:  .md für strukturierte Typen, frei für Info

  CREATIVE — R+MUNI Doku-creative
    GitHub: https://github.com/arch-nullnull/R-MUNI-Doku-creative
    Zugriff: Sales + dedizierte DEV-Mitglieder
    Inhalt:  Creative Assets, Sales-Material
    Format:  frei

Sprints in Arbeit (Types 5–7 vor Freigabe) leben temporär in:
  R+MUNI Doku-internal\sprints\


4. DOKUMENTTYPEN — ÜBERSICHT
--------------------------------------------------------------------------------

  Type 1   GOV_Global          normatives Regelwerk
  Type 2   principles          Leitprinzipien einer Reihe oder eines Themas
  Type 3   how2                Anleitungen für User und Flows
  Type 4   Rosetta-Stone       Lern- und Translation-Dokument
  Type 5   FREEZE              stabiler, freigegebener Versionsstand
  Type 6   Stage_Ziele         Begründung und Ziele hinter einem Stage
  Type 7   Sprint-DEV-Doku     abgeschlossener, gesyncter Sprint
  Type 8   Sprint-DEV-BACKLOG  Planung für spätere Stages und Zeitpunkte
  Type 9   Info                erklärendes Dokument ohne festen Typ — frei
  Type 10  Creative            Creative Asset — frei

Types 1–8 haben verbindliche Templates.
Types 9–10 haben kein Template — Format ist frei.


5. TYPE 1 — GOV_GLOBAL
--------------------------------------------------------------------------------
Zweck:
  Definiert das normative Regelwerk des R+MUNI Blueprints.
  Es ist das "Gesetz" des Systems — unveränderlich bis zur
  expliziten Stage-Entscheidung des Betreibers.

Charakter:
  - Enthält Regeln und erklärende Inhalte — Erklärungen dienen dem Verständnis, Regeln sind verbindlich (GOV Kap. 3.8)
  - Jede Regel ist genau eine Aussage
  - Jede Regel ist prüfbar
  - Implizite Logik ist unzulässig

Ablage:
  Repo:    R+MUNI Doku-public
  Ordner:  00-governance\
  Datei:   GOV_Global_S<N>.md

Publizierung:
  Public — jeder
  Änderungen nur durch explizite Freigabe des Betreibers

Template:
  GOV_Global_Template_S6.md


6. TYPE 2 — PRINCIPLES
--------------------------------------------------------------------------------
Zweck:
  Beschreibt die Leitprinzipien einer Reihe oder eines Themas.
  Principles erklären warum etwas so ist wie es ist — nicht wie
  es angewendet wird. Das ist Aufgabe der How2.

Charakter:
  - Beschreibt Designentscheidungen und ihre Begründung
  - Enthält keine operativen Schritt-für-Schritt-Anleitungen
  - Ist eigenständig lesbar ohne Kenntnis anderer Dokumente
  - Richtet sich an DEV und technisch versierte User

Benennung:
  <REIHE>_principles_S<N>.md
  Beispiel: CSV_principles_S6.md

Ablage:
  Repo:    R+MUNI Doku-public
  Ordner:  01-principles\
  Datei:   <REIHE>_principles_S<N>.md

Publizierung:
  Public — jeder

Template:
  principles_Template_S6.md


7. TYPE 3 — HOW2
--------------------------------------------------------------------------------
Zweck:
  Beschreibt konkret wie etwas angewendet wird — Schritt für Schritt.
  How2 ist die operative Umsetzung der Principles.

Ausprägungen:
  How2 existiert in zwei klar getrennten Ausprägungen:

  DEV  — technische Referenz für DEV und Poweruser
         Kompakte Script-Aufrufe, Ausgaben, Flags, Fehlerbilder
         Setzt technisches Grundverständnis voraus

  USER — erklärende Anleitung für Anwender und Einsteiger
         Schrittweise Führung, Kontext, Erwartungsmanagement
         Setzt kein technisches Vorwissen voraus
         Entsteht aus anonymisierten Beta-Erfahrungen —
         nicht hier im DEV-Prozess, sondern in der Feedback-Schleife

  Beide Ausprägungen sind eigenständige Dokumente.
  Ein Dokument darf nicht beide Ausprägungen vermischen.

Charakter DEV:
  - Kompakte Referenz — Befehl, Ziel, Ausgabe
  - Kurzreferenz aller Scripts der Reihe
  - Typische Fehlerbilder und direkte Lösung
  - Varianten und Flags explizit dokumentiert

Charakter USER:
  - Schritt-für-Schritt mit Kontext und Begründung
  - Erwartungsmanagement am Anfang
  - Konkrete Beispiele aus der Praxis
  - Klare Voraussetzungen und typische Stolperfallen

Benennung:
  <REIHE>_How2_DEV_S<N>.md     Beispiel: CSV_How2_DEV_S6.md
  <REIHE>_How2_USER_S<N>.md    Beispiel: CSV_How2_USER_S6.md

Ablage:
  Repo:    R+MUNI Doku-public
  Ordner:  02-how2\
  Datei:   <REIHE>_How2_DEV_S<N>.md / <REIHE>_How2_USER_S<N>.md

Publizierung:
  Public — jeder

Templates:
  how2_DEV_Template_S6.md
  how2_USER_Template_S6.md


8. TYPE 4 — ROSETTA-STONE
--------------------------------------------------------------------------------
Zweck:
  Übersetzt R+MUNI interne Konzepte in etablierte Frameworks
  (ArchiMate 3.2, TOGAF) und umgekehrt.
  Dient als Lern- und Referenzdokument für DEV und fortgeschrittene User.

Charakter:
  - Mapping-Logik: R+MUNI Begriff → Norm-Begriff
  - Einordnung in Framework-Kontext
  - Bewertung der Konformität
  - Kein operativer Inhalt — rein konzeptuell

Benennung:
  Rosetta-Stone_<THEMA>_S<N>.md
  Beispiel: Rosetta-Stone_Preliminary-Phase_S6.md

Ablage:
  Repo:    R+MUNI Doku-public
  Ordner:  03-rosetta_stone\
  Datei:   Rosetta-Stone_<THEMA>_S<N>.md

Publizierung:
  Public — jeder

Template:
  Rosetta-Stone_Template_S6.md


9. TYPE 5 — FREEZE
--------------------------------------------------------------------------------
Zweck:
  Dokumentiert einen stabilen, freigegebenen Versionsstand.
  Ein Freeze ist ein expliziter Akt des Betreibers — kein automatischer
  Zustand. Er definiert was gilt, was ausgeschlossen ist und was
  bewusst zurückgestellt wurde.

Charakter:
  - Beschreibt den fixierten Zustand zum Freeze-Zeitpunkt
  - Enthält Geltungsbereich, Ausschlüsse und Validierung
  - Ist nach Freigabe unveränderlich
  - Dient als Baseline für nachfolgende Sprints

Benennung:
  FREEZE-<Stagenummer>_S<N>.md
  Beispiel: FREEZE-6_S6.md

Ablage:
  Während Arbeit: R+MUNI Doku-internal\sprints\
  Nach Freigabe:  R+MUNI Doku-public\04-notes\

Publizierung:
  Public nach expliziter Freigabe durch Betreiber

Template:
  FREEZE_Template_S6.md


10. TYPE 6 — STAGE_ZIELE
--------------------------------------------------------------------------------
Zweck:
  Definiert Begründung, Charakter und Ziele eines Stage.
  Beantwortet warum dieser Stage existiert und was er leisten soll —
  nicht wie er technisch umgesetzt wird.

Charakter:
  - Strategisch, nicht operativ
  - Enthält Ausgangsbasis, Ziele und Abgrenzung
  - Wird zu Beginn eines Stage erstellt und bei Bedarf ergänzt
  - Ist nach Stage-Abschluss read-only

Benennung:
  Stage<Nummer>_Ziele_S<N>.md
  Beispiel: Stage6_Ziele_S6.md

Ablage:
  Während Arbeit: R+MUNI Doku-internal\sprints\
  Nach Freigabe:  R+MUNI Doku-public\04-notes\

Publizierung:
  Public nach expliziter Freigabe durch Betreiber

Template:
  Stage_Ziele_Template_S6.md


11. TYPE 7 — SPRINT-DEV-DOKU
--------------------------------------------------------------------------------
Zweck:
  Vollständiges Arbeitsgedächtnis eines abgeschlossenen Sprints.
  Die Sprint-DEV-Doku muss es einem DEV-Mitglied ermöglichen den Sprint
  in einem Jahr ohne Rückfragen vollständig nachzuvollziehen —
  Kontext, Entscheidungen, Umsetzung, Ergebnis und offene Punkte inklusive.

  Sie ist kein schlankes Nachweis-Dokument — sie ist die vollständige
  Dokumentation einer Entwicklungsaktivität.

Charakter:
  - Beschreibt Ausgangslage, Motivation und Kontext vollständig
  - Enthält alle wesentlichen Entscheidungen mit Begründung
  - Dokumentiert verworfene Alternativen explizit
  - Enthält Script-Inhalte oder Auszüge wo sie für das Verständnis
    der Umsetzung relevant sind
  - Diagramme auf .md-unterstützter Basis (Mermaid o.ä.) sind
    ausdrücklich erwünscht wenn sie Zusammenhänge klären
  - Verlinkungen zu Creative-Assets im Doku-creative Repo sind zulässig
    und erwünscht wenn visuelle Materialien die Doku ergänzen
  - Enthält Validierung, Governance-Check und Lessons Learned
  - Baut explizit auf dem letzten Freeze auf und benennt die Delta
  - Wird nach Abschluss gesynct und ist dann unveränderlich

Tiefe:
  Die Dokumentationstiefe richtet sich nach der Komplexität des Sprints.
  Einfache Bugfixes können kürzer sein.
  Strukturelle Änderungen, neue Reihen oder Logikentscheidungen
  erfordern volle Tiefe — inkl. Vorher/Nachher, Script-Beispiele
  und expliziter Begründung jeder wesentlichen Entscheidung.

Benennung:
  Sprint-DEV-<BEZEICHNUNG>_S<N>.md
  Beispiel: Sprint-DEV-CleaningRun_S6.md

Ablage:
  Während Arbeit: R+MUNI Doku-internal\sprints\
  Nach Freigabe:  R+MUNI Doku-public\04-notes\

Publizierung:
  Public nach expliziter Freigabe durch Betreiber

Template:
  Sprint-DEV-Doku_Template_S6.md


12. TYPE 8 — SPRINT-DEV-BACKLOG
--------------------------------------------------------------------------------
Zweck:
  Plant und beschreibt Sprints für spätere Stages und Zeitpunkte.
  Der Backlog ist kein Versprechen — er ist strukturierte Vorausschau.

Charakter:
  - Enthält Motivation, Ziel und Abgrenzung geplanter Sprints
  - Bleibt internal bis zur expliziten Entscheidung zur Umsetzung
  - Wird im DEV-Modus zusätzlich nach Jira gespiegelt
  - Kann jederzeit priorisiert, verschoben oder verworfen werden

Benennung:
  Sprint-DEV-BACKLOG_<BEZEICHNUNG>_S<N>.md
  Beispiel: Sprint-DEV-BACKLOG_CSV-Refactoring_S6.md

Ablage:
  Repo:    R+MUNI Doku-internal
  Ordner:  backlog\
  Datei:   Sprint-DEV-BACKLOG_<BEZEICHNUNG>_S<N>.md

Publizierung:
  Bleibt internal — kein automatischer Public-Weg
  Jira-Sync im DEV-Modus aktiv

Template:
  Sprint-DEV-BACKLOG_Template_S6.md


13. TYPE 9 — INFO
--------------------------------------------------------------------------------
Zweck:
  Aufnahme für alle erklärenden Dokumente die keinem anderen Typ
  entsprechen aber für DEV-interne Arbeit benötigt werden.

Charakter:
  - Kein verbindliches Template
  - Format ist frei
  - Dient der internen Orientierung und Kommunikation
  - Kein normatives Gewicht

Ablage:
  Repo:    R+MUNI Doku-internal
  Ordner:  infocfg\

Publizierung:
  Bleibt internal

Template:
  Keines — Format frei


14. TYPE 10 — CREATIVE
--------------------------------------------------------------------------------
Zweck:
  Aufnahme für alle Creative Assets und Sales-Materialien.

Charakter:
  - Kein verbindliches Template
  - Format ist frei
  - Richtet sich an Sales und ausgewählte DEV-Mitglieder

Ablage:
  Repo:    R+MUNI Doku-creative
  Ordner:  R+MUNI Doku-creative\

Publizierung:
  Privat — nur Sales + dedizierte DEV-Mitglieder

Template:
  Keines — Format frei


15. LEBENSZYKLUS EINES DOKUMENTS
--------------------------------------------------------------------------------
Jedes Dokument mit verbindlichem Template durchläuft diesen Zyklus:

  1. ENTWURF
     Dokument wird in R+MUNI Doku-internal\sprints\ erstellt.
     Stage-Suffix trägt den Erstellungszustand.
     Kein Public-Zugriff.

  2. REVIEW
     Betreiber prüft Konformität mit Template und GOV.
     Korrekturen erfolgen im internen Zustand.

  3. FREIGABE
     Expliziter Akt durch Betreiber.
     Dokument wird nach R+MUNI Doku-public verschoben.
     Ab diesem Zeitpunkt unveränderlich — außer bei
     expliziter Stage-Entscheidung.

  4. CLEANING RUN (vor Beta 1.0)
     Alle public Dokumente werden auf finale Stage-Konformität geprüft.
     Stage-Suffix entfällt in der Release-Version.
     DEV-interne Planung nutzt den Suffix weiterhin.

  5. ARCHIV
     Dokumente vergangener Stages werden nicht gelöscht.
     Sie bleiben als historische Referenz erhalten.


16. OBSIDIAN — OPTIONALE VISUALISIERUNGSEBENE
--------------------------------------------------------------------------------
Obsidian ist die optionale Visualisierungsebene des R+MUNI Blueprint.
Sie ist kein Pflichtbestandteil — aber ein explizit unterstützter Weg
für alle die Dokumentbezüge und Strukturzusammenhänge visuell erfassen
und navigieren wollen.

Grundidee:
  Dokumentbezüge werden nicht in EA-Modell-Ordnerstrukturen abgebildet —
  sondern auf File-Ebene direkt in den .md Dokumenten als Obsidian-Links.
  Obsidian visualisiert diese Links automatisch als Graph.

  Was früher eine verschachtelte EA-Ordnerhölle war wird damit zu
  einem navigierbaren, visuellen Netz auf Basis der Dokumente selbst.

Obsidian-Links in .md Dokumenten:
  Standard Obsidian-Link:   [[Dokumentname]]
  Mit Alias:                [[Dokumentname|Anzeigetext]]
  Mit Abschnitt:            [[Dokumentname#Kapitel]]

  Beispiele:
    [[TMP_principles_S6]]
    [[FREEZE-6_S6|Freeze 6 Baseline]]
    [[Sprint-DEV-CleaningRun_S6#Ergebnis]]

Wo Obsidian-Links eingesetzt werden:
  - In Sprint-DEV-Dokus: Bezug auf referenzierte Freezes, Principles,
    Scripts und vorherige Sprints
  - In Principles: Querverweise auf verwandte Reihen und GOV-Kapitel
  - In How2: Verlinkung auf Voraussetzungs-Dokumente und Folgeschritte
  - In Freeze-Dokumenten: Bezug auf Stage_Ziele und Sprint-DEV-Dokus
    die in diesen Freeze geflossen sind

Verlinkung Creative-Assets:
  Dokumente im Doku-creative Repo können als relative Pfadlinks
  oder Obsidian-Links eingebunden werden wenn sie den Dokumentkontext
  visuell ergänzen.
  Beispiel: Architekturdiagramme, Ablaufgrafiken, Präsentationsfolien
  die zu einem Sprint oder einer Entscheidung gehören.

Obsidian und GitHub:
  .obsidian/ ist in .gitignore ausgeschlossen — Workspace-Einstellungen
  bleiben lokal. Die .md Dateien mit ihren Links sind vollständig
  GitHub-kompatibel. Der Graph entsteht lokal beim DEV-Mitglied das
  Obsidian nutzt — er muss nicht geteilt werden.

Konvention:
  Obsidian-Links sind optional — kein Dokument ist verpflichtet sie
  zu enthalten. Wo sie eingesetzt werden erhöhen sie Navigierbarkeit
  und Nachvollziehbarkeit. Sie dürfen den Fließtext nicht ersetzen —
  der Dokumentinhalt muss auch ohne Obsidian vollständig lesbar sein.


17. ABGRENZUNG ZU ANDEREN DOKUMENTEN
--------------------------------------------------------------------------------
Dieses Dokument beschreibt ausschließlich:
  - Was die Dokumenttypen sind
  - Welche Regeln für sie gelten
  - Wo sie abgelegt werden
  - Wie sie publiziert werden

Dieses Dokument beschreibt nicht:
  - Wie Templates konkret ausgefüllt werden (→ How2)
  - Den Inhalt einzelner Templates (→ jeweiliges Template-Dokument)
  - Operative Prozessschritte der Sprint-Arbeit (→ Sprint-DEV-Doku)
  - Governance-Regeln des Gesamtsystems (→ GOV_Global)


================================================================================
TMP PRINCIPLES | S6 | 2026-03-18
17 Kapitel | Dokumenttypen 1–10 | Obsidian-Option dokumentiert
================================================================================
