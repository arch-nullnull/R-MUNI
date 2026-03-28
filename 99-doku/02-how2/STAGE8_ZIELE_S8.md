================================================================================
STAGE 8 – Beta 1.0 | Außenwirkung & Abschluss
Normative Definition und Geltungsbereich
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : STAGE8_ZIELE_S8
Tag             : #stage #ziele #s8 #beta10
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt durch  : EUMAXL + Claude (Pair-Session)
================================================================================


================================================================================
1. ZWECK VON STAGE 8
================================================================================

Stage 8 dient der Vorbereitung und Durchführung des Beta-1.0-Release —
dem ersten Moment wo R+MUNI auf Augen trifft die nicht im inneren Kreis sind.

Im Fokus stehen:
  - Beta 1.0 Release als Download-fähiges, öffentlich kommunizierbares Paket
  - Außenwirkung — README, öffentliche Doku, erste echte Visitenkarte
  - Onboarding-Basis für externe Betakunden ohne freundschaftliche Begleitung
  - Methodik-Konsolidierung (AI-Driven DEV Update, Jira-Neuausrichtung)
  - Keine inhaltlichen Weiterentwicklungen an R+MUNI selbst

Stage 8 ist der letzte Beta-Stage — kein Entwicklungs-Stage mehr.
Nach Abschluss startet Stage 1 = Produktivbetrieb (neue Zählung).


================================================================================
2. AUSGANGSBASIS
================================================================================

Stage 8 baut auf dem eingefrorenen Stage-7-Zustand auf.

  - Stage-3/4/5/6/7-Scripts: read-only, kein Eingriff
  - Zwei-Welten-Entscheid: normativ gültig, strukturelle Umsetzung zurückgestellt
  - ASC (Betakunde_02): ongeboardet und produktiv
  - BKO1-Offboarding: operativ eingeleitet, Doku ausstehend
  - Jira: bereinigt — sauberer Start, Sync nur noch explizit
  - AI_DRIVEN_DEV_METHODE_S8: vorhanden, 4 Erkenntnisse noch einzuarbeiten

Zulässig in Stage 8:
  - Bugfixes mit expliziter Freigabe
  - Erweiterungen die Beta-1.0-Release direkt dienen
  - Dokumentations- und Kommunikationsarbeit

Nicht zulässig:
  - Strukturelle Änderungen an R+MUNI-Kernlogik
  - Neue Script-Reihen
  - GOV-Umbauten die Stage 1 vorwegnehmen

Bezug auf vorherigen Freeze:
  [[FREEZE_7]]             Ausgangszustand für Stage 8


================================================================================
3. CHARAKTER VON STAGE 8
================================================================================

Stage 8 ist der Übergang von der geschützten Beta-Welt zur echten Außenwelt.
Zum ersten Mal trifft R+MUNI auf Menschen die nicht wissen wie es entstanden ist.

  - Erster Außenauftritt — Visitenkarte statt Werkzeugkasten
  - Abschluss-Stage — kein Aufbau mehr, sondern Fertigstellung
  - Kommunikation vor Entwicklung — was vermittelt wird zählt
  - Qualitätssicherung durch Außenperspektive — würde das jemand verstehen?
  - Methodik-Konsolidierung — was in Stage 7 erkannt wurde wird jetzt verankert

Stage 8 darf polieren — nicht umbauen.


================================================================================
4. ZIELE VON STAGE 8
================================================================================

4.1 S8-Z1 — Beta 1.0 Release
------------------------------
  - Download-fähiges Paket erstellen (GitHub Release)
  - README finalisieren — verständlich ohne Begleitung
  - Öffentliche Doku auf Stand bringen
  - Ziel: Erster externer Betakunde kann R+MUNI selbstständig evaluieren

Grenze: Kein neues Feature — nur was bereits existiert wird kommuniziert.


4.2 S8-Z2 — Kommunikation nach außen
--------------------------------------
  - README + öffentliche Doku so aufbereiten dass sie ohne inneren Kreis
    verständlich sind
  - Sprache prüfen: Denglish ja — aber konsistent und erklärend
  - Ziel: Fremde verstehen was R+MUNI ist und was es kann

Grenze: Keine inhaltliche Überarbeitung des Blueprints selbst.


4.3 S8-Z3 — Onboarding-Basis für externe Betakunden
-----------------------------------------------------
  - Onboarding-Materialien für nicht-freundschaftliche Umgebung aufbereiten
  - Weniger Handhalten, mehr Selbsterklärung
  - Ziel: Onboarding funktioniert ohne EUMAXL als Begleiter

Grenze: Kein neues Onboarding-System — bestehende Materialien werden
        überarbeitet und für externe Augen geprüft.


4.4 S8-Z4 — AI-Driven Methodik Update
---------------------------------------
  - 4 offene Erkenntnisse aus Stage-7-Chats in AI_DRIVEN_DEV_METHODE einarbeiten:
      — Überkorrektur-Reflex bei neutralem Feedback vermeiden
      — Exploration ≠ Transfer (explizite Anweisung nötig)
      — Backlog ≠ Konzeptnotiz (GOV-Overhead nur bei spruchreifen Sprints)
      — SVG-Drift durch Neugenerierung → chirurgische Änderung als Standard
  - Jira-Sync-Neuausrichtung dokumentieren (Konvention aus Sprint-DEV-BACKLOG_Jira-Konventionen_S8)
  - Ziel: Methodik-Dokument spiegelt die gelebte Realität von Stage 7+8

Grenze: Kein Eingriff in R+MUNI-Kernlogik — reine Methodik-Arbeit.


4.5 S8-Z5 — BKO1-Offboarding Doku
-----------------------------------
  - Sprint-DEV-Abschlussdokumentation nach operativem Abschluss erstellen
  - Ziel: BKO1-Offboarding vollständig dokumentiert und abgeschlossen

Grenze: Nur wenn operativer Teil abgeschlossen und Feedback vorhanden.


================================================================================
5. OPTIONALE ZIELE (nach Kapazität / Lust)
================================================================================

  S8-OPT-1   BPMN Flows
              Additiv, kein Blocker. Nur bei Kapazität und Interesse.

  S8-OPT-2   MGT Prinzip experimentell
              Experimentieren und Erkenntnisse sammeln.
              Kein fixer Deliverable — Phase 2 vorbereiten.
              "Nach Lust und Laune" — kein Sprint-Zwang.

  S8-OPT-3   Bugfixing reaktiv
              Kein definierter Scope. Auslöser: gemeldete Fehler,
              Beobachtungspunkt CSV98.

  S8-OPT-4   GOV-Header-Review
              Alle bestehenden Dokumente auf einheitlichen Header prüfen.
              Am Stage-Ende oder bei Kapazität — kein Blocker.


================================================================================
6. BEWUSST NICHT IN STAGE 8
================================================================================

Nicht Teil von Stage 8 sind:
  - SPRINT-CSV-Refactoring — eigener Stage (Stage 1 oder später)
  - Zwei-Welten-Umsetzung (MUNIEA-148) — 2–3 fokussierte Sessions,
    eigener Sprint wenn Kapazität vorhanden
  - MGT Layout Phase 2 vollständig — erst wenn Beta 1.0 steht
  - O365-Integration — zurückgestellt
  - EXPERT Templates — Phase 2
  - IDHandler-Reihe — Stage 1 Thema
  - jEX-Reihe OEF Export — Stage 1 Thema
  - Appliance VM — Stage 1 Thema

Diese Themen wachsen aus Stage 8 heraus — sie sind Stage-1-Arbeit,
nicht Beta-Abschluss-Arbeit.


================================================================================
7. RÜCKKOPPLUNGSSCHUTZ
================================================================================

  - Stage-3/4/5/6/7-Scripts: read-only ohne Ausnahme
  - Bugfixes erfordern explizite Freigabe und Dokumentation
  - Keine Logikänderung ohne expliziten Entscheid
  - Neue Script-Reihen gehören in Stage 1 — nicht in Stage 8
  - Jira-Sync: nur explizit ausgelöst — kein automatischer Reflex
  - Rollentrennung GOV 13: DEV-Rolle / ASC-Rolle / EUMAXL-Rolle strikt getrennt


================================================================================
8. DOKUMENTATION IN STAGE 8
================================================================================

  - Stage 8 besitzt eigenes Claude-Projekt — neuer Kontext, sauberer Start ✓
  - Sprint-Bezeichnung: Sprint-DEV-S8-<Kürzel>
  - Sprint-Dev-Dokumentationen für alle Entwicklungsaktivitäten (GOV 10.8)
  - Jira-Konvention gilt ab sofort (Sprint-DEV-BACKLOG_Jira-Konventionen_S8.md)
  - Jira-Sync nur explizit — kein automatischer Reflex
  - FREEZE-8 am Stage-Ende: autarke Wissensbasis für Stage 1

Fokus: Was nach außen geht muss für Dritte verständlich und reproduzierbar sein.


================================================================================
9. ABGRENZUNG ZU STAGE 1
================================================================================

Nicht Teil von Stage 8 sind:
  - Produktivbetrieb mit realen Kunden (das ist Stage 1)
  - Preismodell oder kommerzielle Strukturen
  - Multi-Tenant-Architektur
  - Vollständige Script-Automatisierung ohne manuelle Eingriffe
  - Skalierbare Community-Infrastruktur

Stage 8 legt die Visitenkarte — Stage 1 öffnet die Tür.


================================================================================
10. FORMALE FESTSTELLUNG
================================================================================

Mit dieser Definition ist Stage 8:
  - logisch eröffnet
  - klar abgegrenzt von Stage 7
  - rückkopplungssicher
  - GOV-konform
  - auf Beta-1.0-Release und erste Außenwirkung ausgerichtet

Stage 3, 4, 5, 6 und 7 bleiben fixiert und geschützt.
Stage 8 darf polieren und kommunizieren — ohne die Basis zu verändern.


================================================================================
BEZÜGE
================================================================================
[[Global_GOV_S8]]                         normative Grundlage
[[FREEZE_7]]                           Ausgangszustand — letzter stabiler Stand
[[AI_DRIVEN_DEV_METHODE_S8]]              Methodik-Basis für S8
[[Sprint-DEV-BACKLOG_Jira-Konventionen_S8]]  Jira-Konvention ab Stage 8


================================================================================
Stage 8 – Beta 1.0 | Außenwirkung & Abschluss
ZIELE DEFINIERT | 2026-03-26
R+MUNI Blueprint | Erstellt durch: EUMAXL + Claude (Pair-Session)
================================================================================
