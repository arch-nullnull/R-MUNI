================================================================================
BACKLOG | Externe Trigger-Ebene — M365 Ökosystem (Power Automate / Azure)
================================================================================
Jira-Ticket   : MUNIEA-142
Typ           : Story
Status        : Backlog
Stage         : Nicht Stage 5 — spätere Stage (offen)
Erstellt      : 2026-03-15
Erstellt durch: EUMAXL + Claude (Pair-Session)
================================================================================


--------------------------------------------------------------------------------
1. KONTEXT
--------------------------------------------------------------------------------
Der FLW-Scriptrunner (FLW-Reihe) ist bewusst kein Trigger-System und kein
Scheduler — er reagiert nicht auf externe Reize.
Für R+MUNI interne Abläufe ist das korrekt und gewollt.

Kernprinzip FLW: "Der Mensch entscheidet wann."
MUNI ist die Stufe VOR der Automatisierung.

Für weitergehende Automatisierung (Email-Eingang, File-Ablage, externe Events)
braucht es eine dedizierte Trigger-Ebene OBERHALB von FLOW.

Diese Story adressiert Option B: Andocken an das Microsoft 365 Ökosystem.
Ein DEV-Account (EUMAXL) steht für Tests zur Verfügung.
Gegenstück: MUNIEA-141 (Camunda 7 On-Premise)


--------------------------------------------------------------------------------
2. GOV-EINORDNUNG
--------------------------------------------------------------------------------
- Nicht notwendig für Stage 5 — reiner Backlog-Eintrag für spätere Stages
- Kein Feature-Zuwachs der in laufende Sprints eingreift
- Cloud-Abhängigkeit muss bei Umsetzung explizit begründet werden (GOV 1.6)
- Bewusste Abweichung von GOV 1.7 (Stabilität über Komfort) → erfordert
  explizite Entscheidungsdokumentation zum Umsetzungszeitpunkt
- DEV Account (EUMAXL) steht für Tests zur Verfügung


--------------------------------------------------------------------------------
3. ZIEL
--------------------------------------------------------------------------------
M365-Dienste als externe Trigger-Ebene nutzen, die auf externe Reize reagiert
und daraufhin FLW-Scripts oder Python-Calls auslöst.

Architektur-Gedanke:
  Externer Reiz (M365) → Power Automate / Azure → FLW-Script → R+MUNI Ablauf


--------------------------------------------------------------------------------
4. TYPISCHE TRIGGER-SZENARIEN
--------------------------------------------------------------------------------
- Email-Eingang (Exchange/Outlook) → Prozess starten
- File-Drop in SharePoint / OneDrive → Script auslösen
- Teams-Nachricht → Reaktion
- Zeitgesteuerter Start via Power Automate (Scheduled)


--------------------------------------------------------------------------------
5. MÖGLICHE TECHNOLOGIEN (M365 ÖKOSYSTEM)
--------------------------------------------------------------------------------
- Power Automate     (Low-Code, direkt aus M365)
- Azure Logic Apps   (Pro-Code, mehr Kontrolle)
- Microsoft Graph API (direkte Integration)
- Azure Functions    (Serverless, Python-kompatibel)


--------------------------------------------------------------------------------
6. OFFENE PUNKTE FÜR SPÄTERE BEWERTUNG
--------------------------------------------------------------------------------
- Welcher M365-Dienst passt am besten zum R+MUNI Modell?
- Lizenzmodell und Kosten DEV vs. Produktionsbetrieb klären
- Cloud-Abhängigkeit explizit GOV-konform begründen und dokumentieren
- Evaluierung im Vergleich zu MUNIEA-141 (Camunda 7) vor finalem Entscheid


--------------------------------------------------------------------------------
7. ABGRENZUNG
--------------------------------------------------------------------------------
- Kein Ersatz für FLW-Reihe
- FLW bleibt interner 1-Button-Orchestrator für R+MUNI interne Abläufe
- Diese Ebene sitzt OBERHALB und löst FLOW aus — nicht innerhalb
- Parallele Option: MUNIEA-141 (Camunda 7 On-Premise)


================================================================================
BACKLOG | MUNIEA-142 | M365 Ökosystem
R+MUNI Blueprint | EUMAXL + Claude (Pair-Session) | 2026-03-15
================================================================================
