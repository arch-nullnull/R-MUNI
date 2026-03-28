================================================================================
HOW2 – FEEDBACKSCHLEIFEN IN R+MUNI (STAGE 7 → S8)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : HOW2_Feedbackschleifen_S8
Tag             : #dev #how2 #feedbackschleifen #s7 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-25
Bezug           : STAGE7_ZIELE.md (S7-Z3) → STAGE8_ZIELE_S8
Vorgänger       : [[HOW2_Feedbackschleifen_S6]]
================================================================================

================================================================================
ZWECK DIESES DOKUMENTS
================================================================================

Dieses Dokument beschreibt wie Feedback in R+MUNI fließt — nach Zielgruppe
getrennt, auf Basis der S7-Realität mit ASC als aktivem Beta-Kontext.

Das Setup ist erprobt und validiert (ASC-Betrieb, Stage 7).
Dieses Dokument ersetzt HOW2_Feedbackschleifen_S6 als aktive Referenz.

Charakter: Beschreibung der aktuellen, funktionierenden Realität.
Nicht ideal-theoretisch, sondern pragmatisch-werkend.

Änderungen gegenüber S6:
  - Kanalmodell nach Zielgruppe statt nach Schleife strukturiert
  - Solo-DEV-Realität (lokal first) explizit abgebildet
  - Jira/Confluence Rolle präzisiert — nur bei Freeze / auf Anweisung
  - GitHub Kundenrepo-Modell neu beschrieben
  - Ordnerstruktur DEV ≠ Kundenumgebung festgehalten
  - E-Mail als Kanal gestrichen — kein aktiver Kanal mehr
  - ASC-Validierung: beide Kanäle (GitHub Issues + Portal) erprobt


================================================================================
1. ÜBERBLICK — DIE FEEDBACKLANDSCHAFT
================================================================================

Feedback in R+MUNI folgt dem Prinzip: jede Zielgruppe hat einen
definierten primären Kanal. Kein Einheitskanal für alle.

Kanalmatrix S7:

  | Zielgruppe          | Primärkanal                                    |
  |---------------------|------------------------------------------------|
  | Internes DEV Team   | Jira + Confluence                              |
  | Viewer / Ext. DEV   | GitHub Issues ODER Jira Support Portal         |
  | Kunden              | Jira Support Portal (Support Pages)            |
  | Public              | GitHub Public (read-only)                      |
  | Interne Stage Doku  | GitHub Intern (privat)                         |
  | Persönliches Feedb. | Confluence (direkt, nur wenn EUMAXL triggert)  |

Grundprinzip bleibt:
  GitHub ist Quelle der Wahrheit für Code und öffentliche Dokumentation.
  Jira/Confluence sind Spiegel und Verlängerungen — kein Sync-Zwang.

Solo-DEV-Realität (S7):
  Aktuell entwickelt nur EUMAXL. Sprint-Arbeit bleibt lokal während
  der Stage. GitHub intern/public ist die primäre Ablage.
  Jira wird spätestens beim Freeze ausgecheckt — nicht laufend.
  Jira/Confluence als vollwertiger DEV-Kanal erst relevant wenn
  echtes Multi-DEV-Team vorhanden.


================================================================================
2. DEV-FEEDBACKSCHLEIFE (INTERN)
================================================================================

2.1 Einstiegspunkte für DEV-Feedback
-------------------------------------

DEV-Feedback kommt aus mehreren Quellen:

  a) Lokal — direkter Entwicklungskontext (primär)
  b) GitHub Issues — intern oder extern ausgelöst
  c) Jira Tickets — bei Freeze oder auf explizite EUMAXL-Anweisung
  d) Persönliches Feedback direkt in Confluence — nur wenn EUMAXL triggert


2.2 GitHub — Quelle der Wahrheit
----------------------------------

GitHub bleibt die zentrale Ablage:

  GitHub intern (privat):
  - Sprint-Artefakte während der Stage
  - Interne Stage-Dokumentation
  - Entwicklungsstand zwischen Freezes

  GitHub public:
  - Freigegebene Blueprint-Inhalte
  - README als primärer Einstieg für externe Leser
  - Issues für externe DEV und Viewer

Workflow GitHub intern:
  1. Entwickler arbeitet lokal
  2. Artefakte werden in GitHub intern gepusht
  3. Bei Freeze: gefilterte Inhalte → GitHub public oder Jira/Confluence
  4. Nur saubere, dokumentierte Zustände werden gepusht

Vorteil:
  - Lokal first — kein Overhead während aktiver Entwicklung
  - Freeze als natürlicher Übergabepunkt
  - History ist sauber und nachvollziehbar


2.3 Jira → bei Freeze und auf Anweisung
-----------------------------------------

Jira wird nicht laufend befüllt — bewusste Entscheidung:

  - Sprint-Arbeit bleibt lokal und in GitHub intern
  - Jira wird spätestens beim Freeze ausgecheckt
  - Backlog und gefilterte Infos werden bei Bedarf übertragen
  - Jira-Story nur auf explizite EUMAXL-Anweisung

Workflow Jira:
  1. EUMAXL hat GitHub Issue / lokalen Backlog-Eintrag
  2. Bei Freeze oder expliziter Anweisung: Übertrag in Jira
  3. Team sieht Jira für Überblick (wenn Multi-DEV aktiv)
  4. Quelle der Wahrheit bleibt GitHub

Wichtig:
  Jira ist kein automatischer Sync mit GitHub.
  Fragmentierung ist akzeptabel — Jira ist Notiz-Spiegel, nicht Quelle.
  Solo-DEV: Jira-Overhead vermeiden — nur wenn es wirklich hilft.


2.4 Confluence → Tiefe Dokumentation und persönliches Feedback
----------------------------------------------------------------

Confluence dient zwei Zwecken:

  a) Tiefe Dokumentation (wie S6):
     - Technische Details die GitHub-Issue zu komplex wären
     - How2-Dokumentation für Entwickler
     - Tiefere Analysen zu Problemen

  b) Persönliches Feedback (neu S7):
     - Direkte Ablage von Erkenntnissen aus dem Betrieb
     - Handlungspunkte und Entscheidungen werden abgeleitet
     - Ausgang: Jira-Story oder Doku-Update
     - Abhängigkeit: nur aktiv wenn EUMAXL triggert
     - Realität Solo-DEV: schleppend — kein strukturelles Defizit

Workflow Confluence:
  1. EUMAXL triggert Ablage (persönliches Feedback oder Analyse)
  2. Erkenntnis wird direkt in Confluence dokumentiert
  3. Handlungspunkt wird abgeleitet: Jira ODER Doku ODER nichts
  4. Verlinkung auf GitHub Issue wenn vorhanden


2.5 GitHub Kundenrepo-Modell (neu S7)
--------------------------------------

Für Kunden mit eigenem GitHub-Setup gilt ab S7:

  - Kunde erstellt eigene Repos nach seinem Bedarf
  - Kunde gibt Repos an EUMAXL frei
  - Spin-off vom Kunden jederzeit möglich — keine Abhängigkeit
  - EUMAXL kann, muss aber nicht einspielen

  Zwei Liefermodelle:
    Git Sync:  Kunde erhält Bereich als aktiven Git Sync
    Manuell:   Kunde lädt ZIP via GitHub-Seite in eigenen Folder

  Vorteil:
  - Kundensouveränität bleibt erhalten
  - Wartung und Reproduzierbarkeit möglich ohne Zwang
  - Spin-off jederzeit sauber möglich

  Ordnerstruktur:
  DEV-Umgebung und Kundenumgebung haben unterschiedliche Strukturen.
  Das Installationspaket wird entsprechend dem Kundensetup
  korrigiert ausgeliefert — kein Einheitspaket für beide.


================================================================================
3. KUNDENFEEDBACK-SCHLEIFE (EXTERN)
================================================================================

3.1 Entry Point: Portal + GitHub README
-----------------------------------------

Kunden erhalten Feedback-Instruktionen über zwei Wege:

  a) Jira Support Portal (primär, strukturiert)
  b) GitHub README (verlinkt auf Portal und Issues)

Workflow Kunde:
  1. Kunde liest GitHub README
  2. README verweist auf Portal für strukturiertes Feedback
  3. Oder: Kunde öffnet GitHub Issue direkt (für externe DEV)
  4. Beide Kanäle sind im ASC-Betrieb validiert und funktionieren


3.2 Zwei aktive Kundenfeedback-Kanäle (S7 validiert)
------------------------------------------------------

Kanal 1: Jira Support Portal (primär für Kunden)
  - Kunde füllt Formular im Portal
  - Kategorien: Bug, Feature Request, DEV Anfrage
  - Ticket landet in Jira (EUMAXL prüft)
  - EUMAXL erstellt GitHub Issue und verlinkt zurück
  - Im ASC-Betrieb erprobt: funktioniert gut

Kanal 2: GitHub Issues (für Viewer und externe DEV)
  - Direkter Kanal zur Quelle der Wahrheit
  - DEV antwortet auf GitHub
  - Keine Umleitung nötig
  - Im ASC-Betrieb erprobt: funktioniert gut

Kanal 3: E-Mail — nicht mehr aktiv
  - E-Mail ist kein definierter Kanal mehr
  - Bei eingehender E-Mail: Kunde wird auf Portal oder GitHub verwiesen
  - Kein Routing über E-Mail in den DEV-Prozess


3.3 Kundensicht: Was sieht der Beta-Kunde?
--------------------------------------------

Aus Kundenperspektive sieht es so aus:

  "Ich will Feedback geben:"

  1. Ich öffne GitHub README (primary entry point)
     → Dort steht: "Report Bugs / Requests hier"

  2. Ich lese: "GitHub Issues oder Portal verfügbar"
     → Portal:  Strukturiert, Kategorien — empfohlen für Kunden
     → GitHub:  Direkt, schnell — für externe DEV und Viewer

  3. Ich wähle:
     - Portal-Formular ausfüllen (strukturiert, Antwort via Portal)
     - GitHub Issue öffnen (direkt, öffentlich)

  4. Ich bekomme Antwort:
     - Portal: EUMAXL antwortet via Jira/Portal
     - GitHub: DEV antwortet auf Issue

Kunde sieht nicht: Die interne Jira/Confluence Maschinerie.
Kunde sieht: Portal ist Anlaufstelle, GitHub ist Quelle.


3.4 Feedback-Kategorien (Portal)
----------------------------------

  [ BUG ]
    - Etwas funktioniert nicht richtig
    - Beschreibung + Schritte zur Reproduktion
    → Landet in Jira, wird zu GitHub Issue

  [ FEATURE REQUEST ]
    - Wunsch für neue Funktionalität
    - Beschreibung + Usecase
    → Landet in Jira, wird in Backlog-Analyse geleitet

  [ DEV ANFRAGE ]
    - Technische Frage oder Entwicklungsanfrage
    - Wird gelesen und situativ bewertet
    → Kapazität und Workload sind legitime Entscheidungskriterien


================================================================================
4. ROLLEN UND VERANTWORTUNG
================================================================================

EUMAXL (Entwickler / Gatekeeper)
──────────────────────────────────
  Verantwortung:
  - GitHub Issues prüfen und triagieren
  - Jira-Tickets (extern eingegangen) zu GitHub-Issues verbinden
  - Confluence-Ablage bei persönlichem Feedback triggern
  - Portal-Inhalte manuell aktualisieren
  - Jira nur bei Freeze oder expliziter Anweisung befüllen

  Entscheidungshoheit:
  - Wann wird Issue im Backlog priorisiert?
  - Welchem Sprint wird zugeordnet?
  - Wie wird Kunde geantwortet?
  - Wann wird Jira-Story angelegt?

DEV-Team (aktuell nur EUMAXL)
───────────────────────────────
  - Sprint-Arbeit bleibt lokal während Stage
  - GitHub intern ist primäre Ablage
  - Jira bei Freeze oder Anweisung
  - Rollen können wachsen wenn Multi-DEV-Team entsteht

Kunden (Beta)
──────────────
  Verantwortung:
  - Feedback strukturiert einbringen (Portal oder GitHub)
  - Schritte zur Reproduktion bei Bugs
  - Ausreichend Details für Verständnis

  Erwartung:
  - Portal: Rückmeldung sobald möglich — keine SLA, kein Versprechen
  - GitHub: DEV antwortet auf Issue


================================================================================
5. KONKRETE WORKFLOWS
================================================================================

5.1 Workflow A: Kunde meldet Bug über Portal
──────────────────────────────────────────────
  1. Kunde füllt Portal-Formular: Bug + Beschreibung
  2. Ticket landet in Jira
  3. EUMAXL prüft Jira-Ticket
  4. EUMAXL prüft Reproduzierbarkeit
  5. EUMAXL erstellt GitHub Issue (oder verlinkt existierenden)
  6. GitHub Issue wird im Jira-Ticket verlinkt
  7. Kunde erhält Rückmeldung via Portal
  8. Bei Fix: GitHub Issue geschlossen, Jira-Ticket geschlossen


5.2 Workflow B: Externe DEV meldet über GitHub Issue
──────────────────────────────────────────────────────
  1. Externe DEV öffnet GitHub Issue im Repository
  2. Beschreibung: Was, was erwartet, was ist falsch
  3. EUMAXL nimmt zur Kenntnis und priorisiert
  4. Implementierung lokal
  5. Commit mit Verweis auf Issue: "fixes #123"
  6. Issue wird geschlossen mit Commit-Link


5.3 Workflow C: Interne Erkenntnis → lokal → GitHub
──────────────────────────────────────────────────────
  1. EUMAXL entdeckt Problem bei Entwicklung
  2. Lokal dokumentiert / behoben
  3. GitHub Issue wenn öffentlich relevant
  4. Optional: Confluence für tiefere Analyse
  5. Bei Freeze: relevante Punkte in Jira ausgecheckt


5.4 Workflow D: Persönliches Feedback → Confluence
────────────────────────────────────────────────────
  1. EUMAXL triggert Ablage in Confluence (persönliche Erkenntnis)
  2. Erkenntnis direkt in Confluence dokumentiert
  3. Handlungspunkt ableiten:
     → Jira-Story (wenn EUMAXL es explizit entscheidet)
     → Doku-Update (wenn Blueprint-relevant)
     → Nichts (wenn nur Notiz)
  4. Realität: schleppend in Solo-DEV — kein Defizit


5.5 Workflow E: Feature Request Kundenseite
──────────────────────────────────────────────
  1. Kunde meldet Feature Request über Portal oder GitHub
  2. EUMAXL bewertet: Backlog oder nicht
  3. GitHub Issue mit Label "enhancement" + "backlog"
  4. Fließt in strategische Planung
  5. Bei Entscheidung zur Umsetzung: In Sprint aufnehmen


================================================================================
6. BESONDERHEITEN UND GRENZEN
================================================================================

6.1 GitHub public ist öffentlich
----------------------------------
  ✓ Vorteil: Transparenz, Kunden können mitverfolgen
  ✓ Vorteil: Suchbar für andere mit ähnlichen Problemen
  ✗ Limit: Keine internen Diskussionen dort

  Regelung: Interne Details gehen in GitHub intern oder Confluence,
  nicht in GitHub public Issues.


6.2 GitHub intern ist privat
------------------------------
  ✓ Sprint-Artefakte während aktiver Entwicklung
  ✓ Kein Overhead durch öffentliche Sichtbarkeit
  ✓ Freeze als natürlicher Freigabepunkt
  ✓ Kundenrepo-Modell: Kunde verwaltet sein eigenes Repo


6.3 Jira ist fragmentiert — das ist ok
----------------------------------------
  ✓ Jira muss nicht 1:1 mit GitHub synced sein
  ✓ Jira ist Spiegel — keine Quelle der Wahrheit
  ✓ Divergenz ist akzeptabel und bewusst
  ✓ Solo-DEV: Jira nur wenn es wirklich hilft

  Bsp: GitHub Issue hat 3 Sub-Tasks, Jira-Ticket hat nur 1 Notiz.
  Das ist bewusst, kein Fehler.


6.4 Confluence ist für Tiefe und persönliches Feedback
--------------------------------------------------------
  GitHub Issue:  "CSV Import fehlgeschlagen — Fehler X"
  Confluence:    "Tiefere Analyse, Root Cause, gelöste Alternative"
  Persönlich:    "Erkenntnis aus Betrieb — Handlungspunkt abgeleitet"

  Nicht alles gehört in kurze Issues.
  Confluence ist Lehr-Raum und persönlicher Notizbereich.


6.5 Portal wird manuell gepflegt
----------------------------------
  ✓ EUMAXL kontrolliert Portal-Inhalte manuell
  ✓ Keine automatische Sync aus GitHub
  ✓ Portal zeigt Status, Link zu GitHub, Kategorien
  ✓ Dynamische Anpassung ohne Doku-Nachzug nötig


6.6 Ordnerstruktur DEV ≠ Kundenumgebung
-----------------------------------------
  DEV-Umgebung hat eigene Ordnerstruktur für Entwicklungsarbeit.
  Kundenumgebung hat angepasste Struktur für den Betrieb.
  Das Installationspaket wird entsprechend dem Kundensetup
  korrigiert ausgeliefert — kein Einheitspaket.


================================================================================
7. FEHLER VERMEIDEN
================================================================================

❌ NICHT TUN:
  - GitHub und Jira laufend synced halten (Doppelarbeit)
  - E-Mail als Kanal verwenden (kein definierter Kanal mehr)
  - Kundenfeedback nur in Jira speichern (nicht öffentlich)
  - Confluence als Ticket-System nutzen (dafür ist GitHub)
  - Jira laufend befüllen in Solo-DEV (Overhead ohne Mehrwert)
  - Einheitliches Installationspaket DEV = Kunde (falsche Struktur)

✓ TUN:
  - GitHub Issue bei jedem relevanten öffentlichen Feedback
  - Jira bei Freeze oder auf explizite Anweisung
  - Confluence für Tiefe und persönliche Erkenntnisse (wenn getriggert)
  - Portal primär für Kunden
  - GitHub Issues primär für externe DEV und Viewer
  - README in GitHub immer aktuell (Primary URL)
  - Kundenpaket angepasst ausliefern


================================================================================
8. VALIDIERUNG DER SCHLEIFEN (S7-STAND)
================================================================================

Im ASC-Betrieb (Stage 7) validiert:

  ✓ GitHub Issues im Vereinskontext funktionieren gut
  ✓ Jira Support Portal im Vereinskontext funktioniert gut
  ✓ Lokal first — GitHub intern als primäre Ablage funktioniert
  ✓ Freeze als Übergabepunkt zu Jira/Confluence funktioniert
  ✓ Kundenrepo-Modell (Kunde erstellt, gibt frei) funktioniert
  ✓ Beide Kanäle (Portal + GitHub Issues) parallel einsetzbar

Nicht mehr erprobt / gestrichen:
  ✗ E-Mail als Kanal — kein aktiver Kanal mehr
  ✗ Automatischer GitHub/Jira Sync — kein Mehrwert Solo-DEV


================================================================================
9. ZUSAMMENFASSUNG FÜR SCHNELLEINSTIEG
================================================================================

Wenn jemand neu ist — kurz und knackig:

DEV-Schleife (Solo-DEV):
  → Lokal arbeiten
  → GitHub intern pushen
  → Bei Freeze: gefiltert zu Jira/Confluence
  → Jira nur auf EUMAXL Anweisung

Kundenschleife:
  → Portal für Kunden (strukturiert)
  → GitHub Issues für externe DEV und Viewer
  → Beides landet am Ende bei GitHub
  → EUMAXL routet intern

Persönliches Feedback:
  → Confluence — nur wenn EUMAXL triggert
  → Handlungspunkt ableiten: Jira, Doku oder nichts

Kernregel:
  "GitHub ist Quelle der Wahrheit.
   Jeder Kanal hat seine Zielgruppe.
   Jira und Confluence sind Spiegel — kein Sync-Zwang."


================================================================================
10. BEZÜGE
================================================================================

[[STAGE7_ZIELE_S7]]               S7-Z3 Ziel (Feedbackschleifen erproben)
[[Sprint-DEV-S7-Z3-Feedbackschleifen_S7]]  Sprint-Doku dieser Aktualisierung
[[HOW2_Feedbackschleifen_S6]]     Vorgänger-Dokument (S6-Stand)
[[FREEZE-6_konsolidiert]]         Baseline S7
[[Global_GOV_S8]]                 GOV 11-13 (Feedback-Kanäle)
README.md (GitHub)                Entry Point für externe Kunden


================================================================================
HOW2 – Feedbackschleifen in R+MUNI | S7→S8 | 2026-03-26 | R+MUNI Blueprint
Nachfolger von: HOW2_Feedbackschleifen_S6
Erstellt durch: EUMAXL + Claude (Pair-Session)
================================================================================
