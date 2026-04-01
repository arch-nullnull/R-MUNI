================================================================================
AI DRIVEN DEVELOPMENT – METHODE R+MUNI
================================================================================
Erstellt        : 2026-03-06
Letzte Änderung : 2026-04-01 — Kap. 1 Varianten-Logik DEV/EXP/ASC/MGT, Kap. 4 Atlassian-Trigger + Output-Regel, Kap. 15.3 Meldepflicht ausgebaut | Freigabe: EUMAXL
                  zuvor: 2026-03-29 — DEV_S101-Resync: Header S101, Kap. 11/12/13 DEV-Inhalte zurück
                  zuvor: 2026-03-26 — S8-Vorbereitung: Kap. 9, 11, 12, 15, 16.3, 17
Autor           : EUMAXL
Charakter       : Persönliche Arbeitsmethode / Entwicklungsphilosophie
Ablageort       : 00-concept/01-principles/AI_DRIVEN_DEV_METHODE_DEV_S102.md
Stage           : S1.02 — AKTIV
Tag             : #dev #methode #aidriven #s102
================================================================================

---
title: "AI Driven Development – Methode R+MUNI"
stage: S1.02
status: "AKTIV"
typ: "Prinzipien"
datum: "2026-04-01"
autor: EUMAXL
tags: [rmuni, blueprint, dev, methode, prinzipien, s102]
---


================================================================================
1. ZWECK
================================================================================

Persönliche AI Driven Development Methode für R+MUNI.
Aus der Praxis gewachsen — kein Framework, eine Disziplin.
Ermöglicht professionelle Systementwicklung ohne Programmierwissen.

Diese Methode existiert in vier Varianten (ab Stage 1.02):
  DEV    Dieses Dokument — interne Arbeitsgrundlage, vollständig, GOV-konform
  EXP    Expert-Variante — Prinzip + Verhalten, kein DEV-Anteil (eigener Chat)
  ASC    Associate-Variante — für Betakunden (R+MUNI Repo)
  MGT    Platzhalter — noch nicht aktiv


================================================================================
2. GRUNDPRINZIP
================================================================================

Der Entwickler liefert:  Domänenwissen, Governance, Qualitätskontrolle, Kontext
Die KI liefert:          Code, Dokumentation, Debugging, Übersetzung

Der Entwickler denkt das System. Die KI schreibt es auf.
Entscheidungen bleiben immer beim Menschen.


================================================================================
3. RAHMENBEDINGUNGEN
================================================================================

Profil, Werkzeuge und Verzeichnisstruktur sind Single Source of Truth
in den Referenzdokumenten gepflegt — nicht hier.

  Install.txt      Werkzeugkasten (Minimal / Default / Addon), Installationspfade,
                   Versionsstand, Encoding-Hinweise
  README.md        Hintergrund, Gedanke, Kontext, weiterführende Informationen
  structure.txt    Verzeichnisübersicht — Scripts arbeiten relativ zu root.cfg


================================================================================
4. DIE METHODE – SESSION-ABLAUF
================================================================================

  1. Kontext herstellen    Projektfolder aktuell laden — kein Start ohne Kontext
  2. Problem beschreiben   Alltagssprache, Halbsätze, Gedankensprünge — alles ok
  3. Knoten finden         Dialog: Claude erklärt → Entwickler korrigiert → Lösung
  4. Governance vor Code   Sprint-Doku, Auslöser, Stage-Zuordnung, Freigabe
  5. Freigabe erteilen     Explizit — keine Annahmen in kritischen Bereichen
  6. Code Review           Claude erklärt in Alltagssprache — Entwickler nimmt ab
  7. Test & Abnahme        Lokal testen, Logs lesen, bei Fehler: Debugging mit Claude
  8. Ablage                Altes ersetzen, Folder aktualisieren, Jira schließen

Prinzip: Was nicht abgelegt ist existiert nicht. Routine schlägt Improvisation.

Ablage-Regeln:
  - Nicht lesbare Formate (.xlsx) nicht im Projektfolder ablegen
  - Mappings und Konfigurationen immer als .txt
  - GitHub ist zentraler Dreh- und Angelpunkt für Repos und Kundenkommunikation
  - Atlassian nur nach expliziter Aufforderung — kein automatischer Reflex:
      Backlog2Jira   → Claude erstellt Story im Jira-Bereich R+MUNI EA
      MD2Confluence  → Claude erstellt Beitrag im Confluence R+MUNI Bereich
                       Basis: letztes .md im Chat — bei Unklarheit nachfragen
  - Kunden halten ihre eigenen Repos — DEV-Zugriff nur auf explizite Freigabe

Output-Regel (verbindlich):
  - Claude gibt Dokumente immer als .md File im Chat aus — nie als Rohtext
  - Nie in den Projektfolder schreiben ohne expliziten Auftrag
  - "Push" durch EUMAXL = .md File im Chat zur Review
  - EUMAXL entscheidet über Ablage, GitHub-Sync und Projektfolder-Push selbst

Kontextmanagement:
  - Projektfolder ist die einzige verlässliche Wahrheit
  - Was drin steht gilt — was nicht drin ist muss im Chat erklärt werden
  - Session-Ende: klarer Stand + offene Punkte + aktualisierter Folder


================================================================================
5. KOMMUNIKATION MIT CLAUDE
================================================================================

  - Deutsch, Alltagssprache, Halbsätze: erlaubt und erwünscht
  - Schritt-für-Schritt immer | Kommandozeilen immer mit Erklärung
  - Claude fragt nach bevor er annimmt
  - Kein "ich mache jetzt einfach mal" ohne Freigabe
  - Stage 3 Freeze / GOV / 1 Script 1 Outcome: Claude kennt und respektiert das
  - Missverständnisse werden sofort aufgelöst — kein Raten, kein implizites Annehmen


================================================================================
6. QUALITÄTSSICHERUNG
================================================================================

Vier-Augen-Prinzip:    Claude erklärt → Entwickler nimmt ab (ohne Code zu lesen)
                       Prüfung: Absicht? GOV? Stage? Rückwärtskompatibilität?
Testpflicht:           Kein Script fertig ohne lokalen Testlauf
Dokumentationspflicht: Kein Sprint ohne Doku. Kein Stage-Ende ohne Vollständigkeit.


================================================================================
7. STÄRKEN
================================================================================

  + Kein Programmierwissen erforderlich
  + Domänenwissen bleibt führend
  + Governance und Qualität bleiben beim Menschen
  + Vollständige Nachvollziehbarkeit durch Dokumentation
  + Reproduzierbar, skalierbar, offen für Weiterentwicklung


================================================================================
8. GRENZEN
================================================================================

  - KI-Verfügbarkeit als Abhängigkeit
  - Zu wenig Kontext → Drift durch Annahmen | zu viel → Drift durch Überlastung
  - Dauerhaft aktive Skills können andere Regeln überschatten
  - Keine automatische Versionierung
  - Testing bleibt beim Entwickler
  - Komplexe Fehler brauchen gute Fehlerbeschreibung
  - GitHub-Sync-Status für Claude ohne Fetch nicht sichtbar
  - Fetch mitten in Session bricht den Fluss — gehört an den Anfang
  - Iterative Neugenerierung akkumuliert Drift — chirurgische Eingriffe
    statt Neugenerierung bei bestehenden Artefakten


================================================================================
9. WEITERENTWICKLUNG
================================================================================

Diese Methode ist lebendig. Erkenntnisse aus der Praxis fließen direkt ein.
Änderungen folgen denselben GOV-Regeln wie alle Blueprint-Dokumente.


================================================================================
10. ROLLEN-PARALLELBETRIEB
================================================================================

Default-Rolle: DEV. Andere Rollen nur auf explizite Anforderung.
Der Entwickler agiert in mehreren Rollen: DEV / Kundensupport / Berater.
Ohne explizite Trennung entstehen Rollenvermischung und Informationsverlust.

Kennzeichnung für Chat-Eingaben:
  [CUSTO]        → Erfahrungsbericht aus Kundenumgebung
                   Claude nimmt auf, baut nichts ein, kein Transfer ohne Auftrag
  [CUSTO→RMUNI]  → Expliziter Transfer-Auftrag
                   Claude übersetzt, anonymisiert automatisch
  Kein Tag       → DEV-Kontext — Claude arbeitet im R+MUNI DEV-Rahmen

Dokument-Identifikation via Header:
  Projekt ≠ R+MUNI und ≠ ASC → Betakunde → Anonymisierungspflicht gilt automatisch
  Kein expliziter Tag erforderlich — Claude liest den Header.

Freigabe für Kundenkontakt: aktuell durch ASC und R+MUNI selbst erteilt.

Claudes Verhalten:
  [CUSTO]        aufnehmen, nichts einbauen, auf Nachfrage antworten
  [CUSTO→RMUNI]  übersetzen, anonymisieren, Ergebnis zur Freigabe vorlegen
  Unklarheit     → nachfragen, nicht raten, nicht annehmen

Kontrolle bleibt beim Entwickler — Claude folgt der Rolle, definiert sie nicht.
Claude meldet aktiv wenn er sein Verhalten verändert (→ Kap. 15.3).
Vollständige Governance: GOV Kapitel 13. Bei Widerspruch gilt GOV 13.


================================================================================
11. TEMPLATE-METHODIK FÜR AI-FÄHIGE DOKUMENTE
================================================================================

Dokumente ohne Claude entstanden + ohne Kontext eingebracht = Drift-Risiko.
Prinzip: Explizitheit verhindert Drift.

Ein AI-fähiges Dokument enthält immer:
  ZWECK / KONTEXT | AUSGANGSLAGE | ERKENNTNIS | TRANSFERIERBARKEIT | ANONYMISIERUNG

AI-fähig = Claude kann es ohne mündliche Erklärung verarbeiten.
Nicht AI-fähig → vor Session aufbereiten oder aufbereitungs-Session starten.
Templates generieren: Dokumenttyp + Zielumgebung nennen → Claude liefert.

Dokumenttypen im Blueprint:
  Sprint-DEV-Doku   Vollständige Sprint-Dokumentation mit GOV-Check
  Konzeptnotiz      Erkenntnis benennen → kurz dokumentieren → später Sprint?
  ASSOCIATE-Doku    Zielgruppen-spezifische Dokumentation (→ GOV/Freeze)


================================================================================
12. WISSENSTRANSFER ZWISCHEN ROLLEN — CUSTO-KANAL
================================================================================

Anonymisierung vor jedem Transfer:
  Personen → User/Stakeholder | Organisationen → nicht nennen | Systeme → Kundenumgebung

Transferierbar:       Prozess-Erkenntnisse, Prinzipien, Muster, How-to-Strukturen
Nicht transferierbar: Konfigurationen, Personenbezüge, Rohdaten, interne Bezeichnungen

Transfer-Workflow:
  1. [CUSTO] einbringen     Claude liest, baut nichts ein, keine Zusammenfassung ohne Auftrag
  2. [CUSTO→RMUNI] auslösen  Optional: Zieldokument | Zielgruppe | Einschränkungen
  3. Claude übersetzt        Anonymisierung automatisch, nur transferierbare Erkenntnis
  4. Entwickler prüft        Inhalt | Anonymisierung | Ton | Transferierbarkeit
  5. Freigabe + Einbau       CUSTO-Quelle bleibt unverändert und separat

Erfolgreich wenn: keine echten Namen | ohne Quellkenntnis verständlich |
                  Quelle nicht rekonstruierbar | Entwickler hat freigegeben

Ergebnisse → ASSOCIATE-Reihe (interner Input, nicht öffentlich).
Vollständige Governance: GOV Kapitel 13.


================================================================================
13. CLAUDE UND EXTERNE QUELLEN
================================================================================

Claude KANN:       Projektfolder lesen, auf Auftrag URLs fetchen
Claude KANN NICHT: GitHub-Sync-Status prüfen, Folder vs. Repo vergleichen

Fetch-Regel:  Fetches an den Session-Anfang — nicht mitten hinein.
              Mitten in der Session → separate Session öffnen.
GitHub-Sync prüft EUMAXL selbst.


================================================================================
14. KONTEXT-OPTIMIERUNG — PRAXISERKENNTNISSE AUS STAGE 6
================================================================================

Mittelmaß-Prinzip:
  IMMER laden:      Freeze, Stage-Ziele, GOV, relevante Principles
  NUR BEI BEDARF:   Scripts, How2, Sprint-Doku
  NICHT LADEN:      veraltete .md, fremde Flow-Serien, mehrere Sprint-Dokus

Memory: stärkster Anker für Regeln die niemals driften dürfen
        Praxisregel: dreimal korrigiert → Memory | einmal verletzt → Skill

Skills: grundsätzlich deaktiviert.
        Aktivieren nur wenn explizit gebraucht — danach wieder deaktivieren.
        jArchi: aktivieren für dedizierte Archi-Sessions (noch nicht vollständig verinnerlicht)
        Alle anderen Skills: nur auf explizite Entscheidung, nicht als Reflex.

Template-first: Gibt es ein Template → Template laden, kein altes .md.
                Templates sind im Projektfolder hinterlegt.
                Bei Unklarheit welches Template passt → nachfragen.


================================================================================
15. PROJEKTMANAGEMENT MIT CLAUDE — CHAT-STRUKTUR UND DRIFT-PRÄVENTION
================================================================================

15.1 Chat-Aufteilung nach Funktion
------------------------------------
Ein Chat, eine Funktion. Themenüberlappung = Drift-Einladung.

  Zielbegleitung   — Stage-Überblick, Statusverfolgung. Kein operativer Inhalt.
  Methodik-Chat    — Reflexion, Methodik-Weiterentwicklung. Kein Sprint-Output.
  Sprint-Chats     — Je ein Ziel oder Sprint. Fokus bleibt im Scope.

15.2 Chat-Initialisierung — Rolle explizit definieren
------------------------------------------------------
Jeder neue Chat beginnt mit einer expliziten Rollenaussage.
Claude startet ohne Gedächtnis — die Rolle gibt sofort Orientierung.

Schlecht: "Hallo, ich möchte mit dir arbeiten."
Gut:      "Du bist meine Zielbegleitung in Stage 7. Kein Code, kein Sprint —
           du hältst den Überblick über alle Stage-Ziele."

Rollenaussage ist keine Formalität — sie ist Investition gegen Drift.

15.3 Verhaltenstransparenz — Meldepflicht
------------------------------------------
Claude meldet aktiv und explizit im Chat wenn er:
  - Scope überschreitet oder droht zu expandieren ohne Auftrag
  - Annahmen trifft statt nachzufragen
  - Verhalten ändert (Ton, Struktur, Detailtiefe)
  - GOV-Regeln nicht anwenden kann oder will
  - Abdriftet — thematisch oder inhaltlich

Meldeformat: kurz, direkt, kein langer Text.
  Beispiel: "⚠ Verhaltenshinweis: Ich bin dabei scope-mäßig zu expandieren — Freigabe?"
  Beispiel: "⚠ Verhaltenshinweis: Ich treffe hier eine Annahme — stimmt das so?"

Meldepflicht ist keine Formalität — sie ist Frühwarnsystem gegen Drift.
EUMAXL hat explizit bestätigt: Meldungen sind erwünscht, auch wenn müde.

15.4 Strukturierungsmuster — und wann es bremst
------------------------------------------------
Claude strukturiert auf Reflex. Oft hilfreich — nicht immer.

Wann es stört: Entwickler denkt frei | Gespräch vor einer Entscheidung
               Signal: "warte kurz" / Pause / freies Erzählen

Was dann besser ist: Zuhören und spiegeln. Struktur kommt danach — auf Abruf.

Praxiserkenntnis S7: Nach dem Umschalten auf Zuhören entstand mehr in
kürzerer Zeit als in strukturierten Sessions zuvor.

15.5 Erkenntnisse sofort sichern
----------------------------------
Erkenntnisse die Dokumente verändern → sofort Sprint oder Backlog anlegen.
Nicht als losen Chat-Inhalt lassen.

Erkenntnis benennen → Auswirkungen identifizieren → Sprint / Backlog anlegen.


================================================================================
16. KI-TOOL-ROLLENTRENNUNG UND ASSET-PIPELINE
================================================================================

KI-Tools haben unterschiedliche Rollen — Vermischung erzeugt Drift.

  Claude     Vollständiger Blueprint-Kontext, GOV-konform.
             Primär für alle technischen und konzeptionellen Arbeiten.

  Copilot    Bewusst kontextfrei — keine R+MUNI-Dokumente.
             Exploration, Entscheidungsfindung, Sales-Dokumentation,
             visuelle Assets. Erkenntnisse fließen als [CUSTO→RMUNI]
             kontrolliert zurück.

Asset-Prinzip (Tool-Lock-Schutz):
  Konzept- und Strukturarbeit → Claude: Kontext vorhanden, GOV-konform.
  Reale Dateien / Assets      → Spezialisierte Tools je Format und Ziel.
  Begründung: Kein Tool-Lock. Claude ist Denkpartner, kein Grafik-Renderer.


================================================================================
17. NAMENSREGEL — GENERELL
================================================================================

Echte Namen dürfen nie in R+MUNI-Artefakten, Dokumentationen oder
Chat-Outputs erscheinen — weder von Personen noch von Kundenorganisationen.

Gilt systemweit — unabhängig von Kontext, Rolle oder Dokument.
Ausnahme: EUMAXL ist gesetztes Pseudonym — kein Realname.

Zulässige Ersetzungen:
  Personen       → User, Stakeholder, Team-Mitglied, Anwender
  Organisationen → nicht nennen — nur Typ (Betakunde, Kunde, Partner)
  Systeme        → Kundenumgebung, Testinstanz, externe Plattform

Claude wendet die Namensregel automatisch an.
Vollständige Governance: GOV 13.4.


================================================================================
END OF DOCUMENT
AI Driven Development – Methode R+MUNI | 2026-03-06
Erweiterung Kapitel 11-13 | 2026-03-18
Erweiterung Kapitel 9 + 14 | 2026-03-19
Erweiterung Kapitel 15 | 2026-03-20
Erweiterung Kapitel 16 + Schlankheits-Revision | 2026-03-22
S8-Vorbereitung: Kap. 9, 11, 12, 15, 16.3, 17 | 2026-03-26
DEV_S101-Resync: Kap. 3 → Referenzen, Kap. 10-12 DEV-Inhalte, Kap. 17 Namensregel neu | 2026-03-29
S102: Kap. 1 Varianten-Logik, Kap. 4 Atlassian-Trigger + Output-Regel, Kap. 15.3 Meldepflicht | 2026-04-01
================================================================================
