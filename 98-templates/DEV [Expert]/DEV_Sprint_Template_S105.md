================================================================================
<TITEL> — SPRINT (DEV)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : DEV_Sprint_<BEZEICHNUNG>_S105
Tag             : #dev #sprint #<thema> #s105
Datum           : <YYYY-MM-DD>
Stage           : S105 — AKTIV
<!-- HINWEIS FÜR DEV
     Stage = der Stage in dem dieses Dokument erstellt wird.
     Nicht der Stage des Templates — der Stage des befüllten Dokuments. -->
Status          : <IN ARBEIT / ABGESCHLOSSEN>
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : <JA — Ticket <NR> / NEIN>
================================================================================

---
title: "<TITEL> — Sprint"
stage: S105
status: "<IN ARBEIT / ABGESCHLOSSEN>"
typ: "Sprint"
datum: "<YYYY-MM-DD>"
autor: EUMAXL
tags: [rmuni, blueprint, dev, sprint, s105, <thema>]
---

================================================================================
<TITEL> — SPRINT (DEV)
Stage S105 | <Status> | R+MUNI Blueprint
================================================================================

---

## Kontext

Kurze Einleitung: Was ist der Gegenstand dieses Sprints, warum existiert er,
welcher Kontext ist für den Leser relevant.

---

## Verwandte Dokumente

- [[Global_GOV_DEV_S105]]                  normative Grundlage
- [[AI_DRIVEN_DEV_METHODE_DEV_S105]]       operative Arbeitsmethode
- [[<weiteres verwandtes Dokument>]]       <warum relevant>

---

================================================================================
1. SPRINT-DEFINITION
================================================================================

1.1 Auslöser (GOV 7.3)
------------------------
<!-- Pflichtfeld. Einer der folgenden zulässigen Auslöser muss explizit benannt sein:
     Fehlerbehebung | Feature-Zuwachs | Strukturbereinigung | Kundenbedarf | Entwicklerwunsch -->

Auslöser:     <Fehlerbehebung / Feature-Zuwachs / Strukturbereinigung / Kundenbedarf / Entwicklerwunsch>
Beschreibung: <Was hat den Sprint ausgelöst — in Alltagssprache>


1.2 Zieldefinition (GOV 7.6)
------------------------------
<!-- Pflichtfeld. Ohne explizite Zieldefinition existiert kein Sprint (GOV 7.6). -->

Ziel:         <Was soll am Ende dieses Sprints erreicht sein — eindeutig und überprüfbar>
Abgrenzung:   <Was ist explizit NICHT Gegenstand dieses Sprints>


1.3 Ausgangslage
-----------------

Ist-Zustand vor dem Sprint:
<Was war vorher der Stand — konkret und sachlich>

Soll-Zustand nach dem Sprint:
<Was soll danach anders sein — überprüfbar>


1.4 Rolle (AI Driven Kap. 10)
------------------------------
<!-- Aktive Rolle beim Start dieses Sprints benennen.
     Default ist DEV. Andere Rollen nur bei expliziter Anforderung. -->

Aktive Rolle:               <DEV / [CUSTO] / [CUSTO→RMUNI]>
Rollenwechsel während Sprint: <JA — dokumentiert in Abschnitt 3 / NEIN>


================================================================================
2. ERGEBNISSE
================================================================================

<!-- Dev-Dokumentation während des Sprints (GOV 7.8).
     Zwischenschritte müssen nicht vollständig dokumentiert werden (GOV 7.7).
     Vollständige Rekonstruktion muss möglich sein. -->

2.1 <Ergebnis 1>
-----------------
<Was konkret entstanden oder entschieden wurde>

Artefakte:    <Dateiname / Pfad / kein Artefakt>
GOV-Konform:  <JA / NEIN — Begründung bei NEIN>


2.2 <Ergebnis 2>
-----------------
<Was konkret entstanden oder entschieden wurde>

Artefakte:    <Dateiname / Pfad / kein Artefakt>
GOV-Konform:  <JA / NEIN — Begründung bei NEIN>


================================================================================
3. ENTSCHEIDUNGEN
================================================================================

<!-- Alle relevanten Entscheidungen explizit dokumentieren (GOV 1.4, 6.13).
     Implizite Entscheidungen sind unzulässig. -->

Entscheidung: <Kurztitel>
  Auslöser:    <Was hat diese Entscheidung notwendig gemacht>
  Ergebnis:    <Was wurde entschieden>
  Begründung:  <Warum — sachlich, keine Annahmen>
  GOV-Bezug:   <Kapitel der GOV die diese Entscheidung betrifft — oder "kein direkter Bezug">
  Auswirkung:  <Was das für den laufenden Betrieb oder zukünftige Sprints bedeutet>
  Rückwirkung: <JA — explizit beschreiben / NEIN>


================================================================================
4. ABWEICHUNGEN UND AUSNAHMEN
================================================================================

<!-- Abweichungen von GOV-Regeln müssen explizit benannt und begründet sein (GOV 3.3).
     Implizite oder stillschweigende Abweichungen sind unzulässig.
     Erzeugen keine Präzedenzwirkung.
     Wenn keine Abweichungen: Abschnitt mit "Keine Abweichungen" befüllen. -->

Abweichung: <Kurztitel oder "Keine Abweichungen">
  GOV-Regel:   <Welche Regel betroffen>
  Begründung:  <Warum die Abweichung notwendig war>
  Wirkung:     <Auf diese Session begrenzt / darüber hinaus — dann explizit dokumentieren>


================================================================================
5. VERHALTENSHINWEISE CLAUDE (AI Driven Kap. 13.1)
================================================================================

<!-- Meldungen die Claude während des Sprints aktiv abgesetzt hat — Frühwarnsystem gegen Drift.
     Ziel: Nachvollziehbarkeit und Lerneffekt für künftige Sessions.
     Wenn keine Meldungen: "Keine Verhaltenshinweise während dieses Sprints." -->

<Verhaltenshinweis 1 — z.B.: "⚠ Verhaltenshinweis: Scope-Expansion erkannt — Freigabe eingeholt.">


================================================================================
6. OFFENE PUNKTE
================================================================================

| Punkt | GOV-Bezug | Status | Nächste Aktion |
|-------|-----------|--------|----------------|
| <Offener Punkt> | <GOV Kap. X / keiner> | offen | <Was als nächstes passiert> |


================================================================================
7. STAGE-ABSCHLUSS UND DOKUMENTATIONSPFLICHT (GOV 7.9)
================================================================================

<!-- Dieses Kapitel ist zum Stage-Ende verpflichtend vollständig auszufüllen.
     Ein Sprint gilt erst mit abgeschlossener Dokumentation als beendet (GOV 7.9). -->

Vollständigkeit geprüft:          <JA / NEIN — offen: <was fehlt>>
GOV-Konformität hergestellt:      <JA / NEIN — offen: <was fehlt>>
Alle Entscheidungen dokumentiert: <JA / NEIN>
Artefakte abgelegt:               <JA / NEIN — Pfad: <wo>>
GitHub-Sync:                      <AUSSTEHEND / ERLEDIGT / NICHT ERFORDERLICH>
Atlassian-Sync:                   <AUSSTEHEND — Ticket <NR> / ERLEDIGT / NICHT ERFORDERLICH>


================================================================================
8. LESSONS LEARNED
================================================================================

Was gut funktioniert hat:
  - <Erkenntnis>

Was beim nächsten Mal anders gemacht werden sollte:
  - <Erkenntnis>

Erkenntnisse die Dokumente oder GOV verändern (AI Driven Kap. 13.3):
  - <Erkenntnis → Sprint / Backlog anlegen: JA / NEIN>

---

## Bezüge

[[Global_GOV_DEV_S105]]                    normative Grundlage
[[AI_DRIVEN_DEV_METHODE_DEV_S105]]         operative Arbeitsmethode
[[FREEZE_1_04]]                            Ausgangszustand Stage 105
[[STAGE105_ZIELE_S105]]                    Stage-Ziele Referenz

---

================================================================================
<TITEL> — SPRINT (DEV) | S105 | <YYYY-MM-DD> | R+MUNI Blueprint
================================================================================
