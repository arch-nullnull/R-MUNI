================================================================================
HOW2 – BETA-FEEDBACK SAMMELN UND BEWERTEN (EUMAXL-PROZESS)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : HOW2_S6-Z1_BetaFeedback_S6
Tag             : #dev #how2 #betafeedback #s6
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-21
Bezug           : STAGE6_ZIELE.md (S6-Z1)
================================================================================

================================================================================
ZWECK DIESES DOKUMENTS
================================================================================

Dieses Dokument beschreibt wie Beta-Feedback in R+MUNI fließt.

Wichtig: Das ist EUMAXL's Prozess — nicht ein Team-Prozess.
EUMAXL empfängt Feedback, bewertet es, kategorisiert es.
Das DEV-Team nimmt optional aus dem Jira-Backlog auf wenn es interessiert.

Charakter: Dokumentation der gelebten Praxis.
Nicht idealistisch, nicht erzwungen — sondern realistisch und human.

================================================================================
1. GRUNDPRINZIP
================================================================================

Beta-Feedback ist wertvoll — aber nicht alles ist gleichzeitig urgent.

Das Modell:
  EUMAXL empfängt → EUMAXL bewertet → Optional: Jira-Eintrag
                                    → DEV-Team nimmt freiwillig auf

Das ist nicht:
  - Keine automatische Ticket-Erstellung
  - Kein Druck aufs Team
  - Kein Mention/Ping
  - Keine Deadlines
  - Keine erzwungene Bearbeitung

Das ist:
  - Transparenz im Backlog
  - Freiwillige Entnahme
  - Respekt vor Volunteer-Arbeit
  - Menschlich, nicht automatisiert
  - Persönliches Feedback bleibt vertrauensvoll


================================================================================
2. FEEDBACK-EMPFANG — KANÄLE UND KATEGORIEN
================================================================================

2.1 Feedback kommt über verschiedene Kanäle
------------------------------------------

Kanäle wo Feedback reinkommt:
  - Portal (strukturiert, Kategorien: Bug, Feature, Frage)
  - GitHub Issues (direkt von Kunden oder Team)
  - E-Mail (Fallback, wenn Kunde nicht weiß wohin)
  - Mündlich/Video-Call (persönliche Gespräche, Face-to-Face)
  - Chat / Slack (ad-hoc Meldungen)

EUMAXL empfängt alle diese Kanäle.
Das ist nicht automatisiert — EUMAXL kennt seinen Kunden-Base.


2.2 Persönliches Feedback → Confluence Besprechungsnotizen
-----------------------------------------------------------

Wenn Feedback persönlich kommt (Telefon, Call, direktes Gespräch):
  
  Ort: Confluence R+MUNI Bereich → "Besprechungsnotizen"
  Wer: EUMAXL dokumentiert dort
  Format: Datum + Kunde + Was besprochen + Ergebnisse
  
  Beispiel:
    2026-03-21 | Betakunde X | Call 14:30 Uhr
    Besprochen: CSV-Import funktioniert nicht mit großen Dateien
    Aktion: EUMAXL notiert, bewertet später ob kritisch
    
  Vorteil:
    - Persönliche Inhalte bleiben vertrauensvoll (Confluence = privat)
    - Gesprächskontext ist dokumentiert
    - Team kann nachlesen wenn es relevant wird
    - Nicht in öffentlichem GitHub


2.3 Strukturiertes Feedback → Portal/GitHub
---------------------------------------------

Wenn Feedback über strukturierte Kanäle kommt (Portal, GitHub):
  
  Das ist bereits kategorisiert (Bug, Feature, Frage)
  EUMAXL sieht es dort
  Dokumentation erfolgt im Kanal selbst (Jira oder GitHub)


================================================================================
3. FEEDBACK-BEWERTUNG — EUMAXL ENTSCHEIDET
================================================================================

Nach Empfang bewertet EUMAXL:

  Ist das Feedback relevant für mehrere interne DEV-Team-Mitglieder?
    JA  → Optional: ins Jira-Backlog
    NEIN → Notiz, zurückgestellt, oder als "Feature für später"

  Ist es zeitkritisch (ein Bug der blockiert)?
    JA  → Höhere Priorität in Jira
    NEIN → Normale Backlog-Einordnung

  Ist es persönliches Feedback von diesem einen Kunden?
    JA  → Bleibt in Confluence Besprechungsnotizen
    NEIN → Wenn relevant für Team: ins Jira-Backlog


================================================================================
4. KATEGORISIERUNG
================================================================================

EUMAXL kategorisiert Feedback gedanklich in:

  BUG
    Etwas funktioniert nicht wie erwartet
    Beispiel: "CSV-Import crasht mit großen Dateien"
    
  FEATURE REQUEST
    Kunde möchte neue Funktionalität
    Beispiel: "Ich brauche einen Dunkelmodus"
    
  VERBESSERUNG
    Nicht broken, aber könnten besser sein
    Beispiel: "Die Fehlerausgabe ist kryptisch"
    
  FRAGE / SUPPORT
    Kunde versteht nicht wie was funktioniert
    Beispiel: "Wie kann ich das Modell synchronisieren?"
    
  PERSÖNLICH / VERTRAUENSVOLL
    Feedback das nicht öffentlich gehört
    Beispiel: Betakunde erzählt von Problemen in ihrer Org
    → Bleibt in Confluence Besprechungsnotizen


================================================================================
5. JIRA-EINTRAG — OPTIONAL UND FREIWILLIG
================================================================================

Wenn EUMAXL entscheidet: "Das sollte das Team sehen":

  Schritt 1: Jira-Ticket anlegen
    Projekt: R+MUNI
    Typ: Bug / Feature / Improvement (je nach Kategorie)
    Titel: Aussagekräftig, aber nicht dramatisierend
    Beschreibung: Was der Kunde sagte, Kontext, Reproduzierbarkeit
    
  Schritt 2: Backlog platzieren
    Keine Assignee (freiwillig!)
    Keine Deadline
    Kein Priority-Druck
    
  Schritt 3: Team informieren
    KEINE automatische Benachrichtigung
    KEINE Mentions
    KEINE "du musst das machen"
    
    Stattdessen: "Wer Lust hat, schaut ins Backlog"
    Das ist ein Angebot, kein Befehl


================================================================================
6. DEV-TEAM NIMMT AUF (ODER AUCH NICHT)
================================================================================

Das DEV-Team ist freiwillig.

Wer einen Jira-Eintrag nimmt:
  - Weil es ihn interessiert
  - Weil er gerade Zeit hat
  - Weil er diesen Bug auch schon nervig fand
  - Weil er "lustlos" ist und sich was Cooles aussucht

Wer nicht nimmt:
  - Das ist ok
  - Kein Stress
  - Nicht jeder muss alles machen
  - Die Person arbeitet an anderen Dingen

Das ist der Kern: Freiwilligkeit + Respekt.


================================================================================
7. ABLAUF-BEISPIEL
================================================================================

Beispiel 1: Strukturiertes Feedback (Portal)
─────────────────────────────────────────

Kunde meldet über Portal: "CSV-Import schlägt mit großen Dateien fehl"
  ↓
EUMAXL erhält Ticket im Portal/Jira
  ↓
EUMAXL bewertet: "Ist das für mehrere wichtig? Naja, nur dieser eine Kunde."
  ↓
EUMAXL notiert: Ins Backlog, aber nicht dringend
  ↓
Optional: Jira-Ticket anlegen ("CSV Import mit großen Dateien optimieren")
  ↓
Team sieht Ticket im Backlog
  ↓
Developer interessiert sich: "Ah ja, das habe ich auch bemerkt!"
  ↓
Developer nimmt Ticket und bearbeitet es
  ↓
Ergebnis: Problem gelöst, Kunde hat Antwort


Beispiel 2: Persönliches Feedback (Call)
──────────────────────────────────────

Betakunde ruft an: "Hey EUMAXL, bei uns im Unternehmen ist das so,
dass die Datenqualität ein Riesenproblem ist..."
  ↓
EUMAXL notiert in Confluence → "Besprechungsnotizen R+MUNI"
  Datum, Kunde, Kontext, was besprochen
  ↓
EUMAXL bewertet: "Ist das für Team relevant? Eher nicht jetzt.
Das ist ein Organisationsproblem des Kunden, nicht unser Bug."
  ↓
EUMAXL notiert sich: "Für spätere Kundenkonversation merken"
  ↓
Kein Jira-Ticket
  Vertrauensvoll in Confluence bleiben
  ↓
Wenn später anderer Kunde ähnlich fragt: EUMAXL hat Kontext


Beispiel 3: Kritischer Bug
──────────────────────────

Kunde meldet: "Das Feature XYZ funktioniert gar nicht — blockiert mich völlig!"
  ↓
EUMAXL empfängt Feedback
  ↓
EUMAXL bewertet: "Ja, das ist kritisch. Das sollte schnell repariert werden."
  ↓
EUMAXL erstellt Jira-Ticket mit höherer Sichtbarkeit
  ↓
EUMAXL informiert Team: "Heads up — wir haben einen kritischen Bug, 
   wer kann sich das anschauen? Jira: #2451"
  ↓
Developer nimmt sich sofort an
  ↓
Bug wird behoben, Kunde informiert


================================================================================
8. KEINE AUTOMATISIERUNG, SONDERN MENSCHLICHES URTEIL
================================================================================

Das ist bewusst nicht automatisiert.

Warum nicht:
  - Nicht jedes Feedback ist ein Ticket
  - Kontext ist wichtig
  - Mensch kennt seinen Kunden besser als Scripts
  - Über-Ticketisierung ist schädlich
  
EUMAXL hat das Urteil:
  - Ist das wirklich ein Problem?
  - Ist das für mehrere relevant?
  - Ist das jetzt wichtig oder später?
  - Gehört das in öffentliches Backlog oder privat zu Notizen?

Das ist ein Feature, nicht ein Bug.


================================================================================
9. CONFLUENCE BESPRECHUNGSNOTIZEN — STRUKTUR
================================================================================

Ablageort: R+MUNI Bereich in Confluence
Seite: "Besprechungsnotizen" oder ähnlich

Format (für jedes Gespräch):

  ---
  Datum: 2026-03-21
  Zeit: 14:30 Uhr
  Betakunde: [Name / ID]
  Kanal: Telefonisch / Video / Mail / Chat
  Teilnehmer: EUMAXL + [Kunde]
  ---
  
  THEMA 1 – CSV-Import Probleme
    Kunde berichtet: [konkrete Schilderung]
    Kontext: [Umstände, Unternehmen, Häufigkeit]
    Aktion: Ins Backlog notiert, nicht kritisch
    Folge: [wenn es Follow-up gab]
  
  THEMA 2 – Feature-Anfrage Dunkelmodus
    Kunde möchte: [Beschreibung]
    Nutzen: [warum wichtig für den Kunden]
    EUMAXL-Notiz: Interessant, aber Backlog für später
  
  ALLGEMEIN
    Stimmung: Zufrieden / Kritisch / Fragend
    Nächster Kontakt: [wenn geplant]


================================================================================
10. ZUSAMMENFASSUNG FÜR SCHNELLES VERSTÄNDNIS
================================================================================

S6-Z1 Prozess kurz:

  EUMAXL empfängt Feedback
    ↓ über verschiedene Kanäle
  
  EUMAXL kategorisiert
    ↓ Bug / Feature / Verbesserung / Persönlich
  
  EUMAXL bewertet
    ↓ Ist das für Team relevant?
  
  Falls ja → Jira-Backlog (ohne Druck, ohne Mention)
  Falls nein → Confluence Notiz oder zurückgestellt
  
  Team nimmt freiwillig auf
    ↓ wenn's interessiert
  
  Arbeitet dran wenn Lust
    ↓ oder nicht — kein Stress


Das ist human, respektvoll und pragmatisch.
Keine Erzwingung, keine Automatisierung, reines Vertrauen.


================================================================================
BEZÜGE
================================================================================

STAGE6_ZIELE.md                      S6-Z1 Ziel (Beta-Feedback sammeln)
HOW2_Feedbackschleifen_S6.md         Wo Feedback technisch reinkommt
FREEZE-6.md                          aktueller Ausgangszustand


================================================================================
HOW2 – S6-Z1 Beta-Feedback sammeln und bewerten | S6 | 2026-03-21
R+MUNI Blueprint | EUMAXL-Prozess dokumentiert
================================================================================
