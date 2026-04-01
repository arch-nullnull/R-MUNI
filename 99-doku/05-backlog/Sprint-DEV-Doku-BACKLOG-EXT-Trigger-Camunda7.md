================================================================================
BACKLOG | Externe Trigger-Ebene — Camunda 7 (On-Premise BPMN Engine)
================================================================================
Jira-Ticket   : MUNIEA-141
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

Diese Story adressiert Option A: Camunda 7 als On-Premise BPMN Engine.
Gegenstück: MUNIEA-142 (M365 Ökosystem)


--------------------------------------------------------------------------------
2. GOV-EINORDNUNG
--------------------------------------------------------------------------------
- Nicht notwendig für Stage 5 — reiner Backlog-Eintrag für spätere Stages
- Kein Feature-Zuwachs der in laufende Sprints eingreift
- GOV-konform: On-Premise, kein Cloud-Lock-in, Stabilität über Komfort (GOV 1.7)
- EOL-Situation muss bei Umsetzung explizit begründet und dokumentiert werden
  (GOV 1.6 Explizitheit)
- Camunda 7 ist EOL aber stabil — keine aktive Abschaltung geplant


--------------------------------------------------------------------------------
3. ZIEL
--------------------------------------------------------------------------------
Camunda 7 als lokale BPMN Engine einsetzen, die auf externe Reize reagiert
und daraufhin FLW-Scripts (oder direkte Python-Calls) auslöst.

Architektur-Gedanke:
  Externer Reiz → Camunda 7 (BPMN Prozess) → FLW-Script → R+MUNI Ablauf


--------------------------------------------------------------------------------
4. TYPISCHE TRIGGER-SZENARIEN
--------------------------------------------------------------------------------
- Email-Eingang       → Prozess starten
- File-Drop           → Script auslösen
- Webhook / HTTP-Event → Reaktion
- Zeitgesteuerter Start (Scheduled)


--------------------------------------------------------------------------------
5. OFFENE PUNKTE FÜR SPÄTERE BEWERTUNG
--------------------------------------------------------------------------------
- Camunda 7 Community Edition auf Docker (lokal)
- BPMN-Prozess als Wrapper für FLW-Scripts
- Kein Produktionsbetrieb geplant — Lern- und Evaluierungszweck
- Camunda 8 / Zeebe als Nachfolger im Blick behalten
- Evaluierung im Vergleich zu MUNIEA-142 (M365) vor finalem Entscheid


--------------------------------------------------------------------------------
6. ABGRENZUNG
--------------------------------------------------------------------------------
- Kein Ersatz für FLW-Reihe
- FLW bleibt interner 1-Button-Orchestrator für R+MUNI interne Abläufe
- Diese Ebene sitzt OBERHALB und löst FLOW aus — nicht innerhalb
- Parallele Option: MUNIEA-142 (M365 Ökosystem)


================================================================================
BACKLOG | MUNIEA-141 | Camunda 7
R+MUNI Blueprint | EUMAXL + Claude (Pair-Session) | 2026-03-15
================================================================================
