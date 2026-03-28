================================================================================
AI DRIVEN DEVELOPMENT – METHODE R+MUNI
================================================================================
Erstellt        : 2026-03-06
Letzte Änderung : 2026-03-26 — S8-Vorbereitung: Kap. 9, 11, 12, 15, 16.3, 17
Autor           : EUMAXL
Charakter       : Persönliche Arbeitsmethode / Entwicklungsphilosophie
Ablageort       : 00-concept/01-principles/AI_DRIVEN_DEV_METHODE.txt
================================================================================


================================================================================
1. ZWECK
================================================================================

Persönliche AI Driven Development Methode für R+MUNI.
Aus der Praxis gewachsen — kein Framework, eine Disziplin.
Ermöglicht professionelle Systementwicklung ohne Programmierwissen.


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

Profil:
  IT-Erfahrung: Presales Datacenter (20J), Projektmanagement (6J),
                Prozess- & Changemanagement (3J)
  Kein Programmierwissen | GUI-orientiert | Stärke: Systemdenken, Governance

Werkzeuge Core (MINIMAL):
  Archi 5.8 | Camunda Modeler | Python 3

Werkzeuge Core (DEFAULT):
  Notepad++ | Git | GitHub | Obsidian | draw.io | Inkscape | PowerShell 7
  Claude Pro | KeePass | Projektfolder (manuell versioniert)

Addon DEV-only:
  Atlassian Jira + Confluence (Free Plan) — Ticketing, Sprint-Verwaltung, Doku


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


================================================================================
5. KOMMUNIKATION MIT CLAUDE
================================================================================

  - Deutsch, Alltagssprache, Halbsätze: erlaubt und erwünscht
  - Schritt-für-Schritt immer | Kommandozeilen immer mit Erklärung
  - Claude fragt nach bevor er annimmt
  - Kein "ich mache jetzt einfach mal" ohne Freigabe
  - Stage 3 Freeze / GOV / 1 Script 1 Outcome: Claude kennt und respektiert das


================================================================================
6. KONTEXTMANAGEMENT
================================================================================

Der Projektfolder ist die einzige verlässliche Wahrheit.
Was drin steht gilt. Was nicht drin ist muss im Chat erklärt werden.

Aktualisierung: nach jeder Session mit Änderungen — ersetzen, hinzufügen, löschen.
Session-Ende:   klarer Stand + offene Punkte + aktualisierter Folder.


================================================================================
7. QUALITÄTSSICHERUNG
================================================================================

Vier-Augen-Prinzip:    Claude erklärt → Entwickler nimmt ab (ohne Code zu lesen)
                       Prüfung: Absicht? GOV? Stage? Rückwärtskompatibilität?
Testpflicht:           Kein Script fertig ohne lokalen Testlauf
Dokumentationspflicht: Kein Sprint ohne Doku. Kein Stage-Ende ohne Vollständigkeit.


================================================================================
8. STÄRKEN
================================================================================

  + Kein Programmierwissen erforderlich
  + Domänenwissen bleibt führend
  + Governance und Qualität bleiben beim Menschen
  + Vollständige Nachvollziehbarkeit durch Dokumentation
  + Reproduzierbar, skalierbar, offen für Weiterentwicklung


================================================================================
9. GRENZEN
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
10. WEITERENTWICKLUNG
================================================================================

Diese Methode ist lebendig. Erkenntnisse aus der Praxis fließen direkt ein.
Änderungen folgen denselben GOV-Regeln wie alle Blueprint-Dokumente.


================================================================================
11. ROLLEN-PARALLELBETRIEB
================================================================================

Der Entwickler agiert in mehreren Rollen: DEV / Beta-Tester / Berater.
Ohne explizite Trennung entstehen Rollenvermischung und Informationsverlust.

Kanal: [BETA] = Erfahrungsbericht, kein Transfer
       [BETA→RMUNI] = explizit gewünschter Transfer in R+MUNI

Transfer-Logik (3 Stufen):
  1. Erfahrungsbericht aufnehmen
  2. Transfer explizit auslösen
  3. Entwickler gibt Ergebnis frei — kein Einbau ohne Freigabe

Der laufende Stage ist gleichzeitig Lernlabor für die Methodik.
Claude meldet aktiv wenn er sein Verhalten verändert (→ Kap. 16.3).
Vollständige Governance: GOV Kapitel 13.


================================================================================
12. TEMPLATE-METHODIK FÜR AI-FÄHIGE DOKUMENTE
================================================================================

Dokumente ohne Claude entstanden + ohne Kontext eingebracht = Drift-Risiko.

Ein AI-fähiges Dokument enthält immer:
  ZWECK / KONTEXT     — Was, wofür, für wen?
  AUSGANGSLAGE        — Was war gegeben, was war das Problem?
  ERKENNTNIS          — Was wurde entschieden, warum, was bewusst nicht?
  TRANSFERIERBARKEIT  — Was ist allgemein gültig, was nicht übertragbar?
  ANONYMISIERUNG      — Was unterliegt GOV 13.4?

Prinzip: Explizitheit verhindert Drift.
Templates generieren lassen: Dokumenttyp + Zielumgebung beschreiben → Claude liefert.

Dokumenttypen im Blueprint:
  Sprint-DEV-Doku     Vollständige Sprint-Dokumentation mit GOV-Check
  Konzeptnotiz        Destillierte Erkenntnis, noch nicht spruchreif —
                      kein GOV-Overhead, kein Sprint erforderlich
  ASSOCIATE-Doku      Zielgruppen-spezifische Dokumentation (→ GOV/Freeze)

Konzeptnotiz als eigenständiger Typ ist bewusst leichtgewichtig:
Erkenntnis benennen → kurz dokumentieren → später entscheiden ob Sprint.


================================================================================
13. WISSENSTRANSFER ZWISCHEN ROLLEN — BETA-KANAL
================================================================================

Anonymisierung vor jedem Transfer:
  Personen → User/Stakeholder | Organisationen → nicht nennen | Systeme → Beta-Umgebung

Transferierbar:       Prozess-Erkenntnisse, Prinzipien, Muster, How-to-Strukturen
Nicht transferierbar: Konfigurationen, Personenbezüge, Rohdaten, interne Bezeichnungen

Ergebnisse landen in der USER-Reihe (interner Input, nicht öffentlich).
Vollständige Governance: GOV Kapitel 13.


================================================================================
14. CLAUDE UND EXTERNE QUELLEN
================================================================================

Claude KANN:       Projektfolder lesen, auf Auftrag URLs fetchen
Claude KANN NICHT: GitHub-Sync-Status prüfen, Folder vs. Repo vergleichen

Fetch-Regel:  Fetches an den Session-Anfang — nicht mitten hinein.
              Mitten in der Session → separate Session öffnen.
GitHub-Sync prüft EUMAXL selbst.


================================================================================
15. KONTEXT-OPTIMIERUNG — PRAXISERKENNTNISSE AUS STAGE 6
================================================================================

Mittelmaß-Prinzip:
  IMMER laden:      Freeze, Stage-Ziele, GOV, relevante Principles
  NUR BEI BEDARF:   Scripts, How2, Sprint-Doku
  NICHT LADEN:      veraltete .md, fremde Flow-Serien, mehrere Sprint-Dokus

Memory: stärkster Anker für Regeln die niemals driften dürfen
        Praxisregel: dreimal korrigiert → Memory | einmal verletzt → Skill

Skills: nur aktivieren wenn gebraucht, danach deaktivieren
        Aktiv: r-muni-blueprint (immer) | mlat-context-handler (bei Bedarf)
               jArchi (nur bei Archi-Arbeit)

Template-first: Gibt es ein Template → Template laden, kein altes .md.
                Templates sind im Projektfolder hinterlegt.
                Bei Unklarheit welches Template passt → nachfragen.


================================================================================
16. PROJEKTMANAGEMENT MIT CLAUDE — CHAT-STRUKTUR UND DRIFT-PRÄVENTION
================================================================================

16.1 Chat-Aufteilung nach Funktion
------------------------------------
Ein Chat, eine Funktion. Themenüberlappung = Drift-Einladung.

  Zielbegleitung   — Stage-Überblick, Statusverfolgung. Kein operativer Inhalt.
  Methodik-Chat    — Reflexion, Methodik-Weiterentwicklung. Kein Sprint-Output.
  Sprint-Chats     — Je ein Ziel oder Sprint. Fokus bleibt im Scope.

16.2 Chat-Initialisierung — Rolle explizit definieren
------------------------------------------------------
Jeder neue Chat beginnt mit einer expliziten Rollenaussage.
Claude startet ohne Gedächtnis — die Rolle gibt sofort Orientierung.

Schlecht: "Hallo, ich möchte mit dir arbeiten."
Gut:      "Du bist meine Zielbegleitung in Stage 7. Kein Code, kein Sprint —
           du hältst den Überblick über alle Stage-Ziele."

Rollenaussage ist keine Formalität — sie ist Investition gegen Drift.

16.3 Verhaltenstransparenz
--------------------------
Claude meldet aktiv wenn er sein Verhalten verändert.

16.4 Strukturierungsmuster — und wann es bremst
------------------------------------------------
Claude strukturiert auf Reflex. Oft hilfreich — nicht immer.

Wann es stört: Entwickler denkt frei | Gespräch vor einer Entscheidung
               Signal: "warte kurz" / Pause / freies Erzählen

Was dann besser ist: Zuhören und spiegeln. Struktur kommt danach — auf Abruf.

Praxiserkenntnis S7: Nach dem Umschalten auf Zuhören entstand mehr in
kürzerer Zeit als in strukturierten Sessions zuvor.

16.5 Erkenntnisse sofort sichern
----------------------------------
Erkenntnisse die Dokumente verändern → sofort Sprint oder Backlog anlegen.
Nicht als losen Chat-Inhalt lassen.

Erkenntnis benennen → Auswirkungen identifizieren → Sprint / Backlog anlegen.


================================================================================
17. KI-TOOL-ROLLENTRENNUNG UND ASSET-PIPELINE
================================================================================

KI-Tools haben unterschiedliche Rollen — Vermischung erzeugt Drift.

  Claude     Vollständiger Blueprint-Kontext, GOV-konform.
             Primär für alle technischen und konzeptionellen Arbeiten.

  Copilot    Bewusst kontextfrei — keine R+MUNI-Dokumente.
             Exploration, Entscheidungsfindung, Sales-Dokumentation.
             Erkenntnisse fließen als [BETA→RMUNI] kontrolliert zurück.

Asset-Prinzip (Tool-Lock-Schutz):
  Konzept- und Strukturarbeit (Diagramme, Entscheidungen, Architektur)
  → Claude: Kontext vorhanden, GOV-konform, reproduzierbar im Dialog.

  Reale Dateien als verwertbare Assets (SVG, Grafiken, Exportformate)
  → Außerhalb Claude: spezialisierte Tools je nach Format und Zielumgebung.

  Begründung: Kein Tool-Lock. Jedes Werkzeug bleibt in seiner Stärke.
              Claude ist kein Grafik-Renderer — er ist ein Denkpartner.

Visuelle Assets (MUNI-Figuren, Flipcharts):
  Geplant mit Stable Diffusion + LoRA — einmal trainiert, reproduzierbarer Stil.
  Scope: DEV-only. Freigabe durch EUMAXL ausstehend.


================================================================================
END OF DOCUMENT
AI Driven Development – Methode R+MUNI | 2026-03-06
Erweiterung Kapitel 11-13 | 2026-03-18
Erweiterung Kapitel 9 + 14 | 2026-03-19
Erweiterung Kapitel 15 | 2026-03-20
Erweiterung Kapitel 16 + Schlankheits-Revision | 2026-03-22
Erweiterung Kapitel 17 + Konsolidierung S7-final | 2026-03-22
S8-Vorbereitung: Kap. 9, 11, 12, 15, 16.3, 17 | 2026-03-26
================================================================================
