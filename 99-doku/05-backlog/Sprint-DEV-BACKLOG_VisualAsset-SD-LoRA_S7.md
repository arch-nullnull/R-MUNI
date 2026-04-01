================================================================================
SPRINT-DEV-BACKLOG – VISUAL ASSET PIPELINE — STABLE DIFFUSION + LORA
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : Sprint-DEV-BACKLOG_VisualAsset-SD-LoRA_S7
Datum           : 2026-03-22
Stage           : S7 – AKTIV
Status          : BACKLOG — nicht gestartet
Verantwortlich  : EUMAXL
Jira-Sync       : NEIN — noch kein Ticket
================================================================================


================================================================================
1. MOTIVATION UND AUSLÖSER
================================================================================

Auslöser-Typ: Feature / Entwicklerwunsch

Visuelle Assets (MUNI-Figuren, Flipcharts, Präsentationsbilder) entstehen
aktuell ohne definierten Stil-Workflow. Es gibt keine reproduzierbare Pipeline
die sicherstellt dass Bilder über Stages und Projekte hinweg konsistent wirken.

Die Evaluierung von Copilot als Creative-Tool hat gezeigt: cloud-basierte
Bildgeneratoren sind für diesen Usecase nicht stabil genug — kein fixierbarer
Stil, kein deterministisches Ergebnis, kein Blueprint-fit.

Stable Diffusion mit LoRA-Training löst das strukturell: einmaliges Training
auf vorhandenen MUNI-Assets erzeugt einen fixen, wiederholbaren Stil der lokal
ausführbar ist und keine Cloud-Abhängigkeit erzeugt.

Erkannt in:    Copilot-Evaluierung + AI Driven DEV Methodik-Chat
Erkannt am:    2026-03-22


================================================================================
2. ZIEL
================================================================================

Ziel:
  Stabile, lokal ausführbare Visual-Asset-Pipeline auf Basis von
  Stable Diffusion + LoRA aufbauen — DEV-only, nicht User-relevant.

Erfolgskriterium:
  - Stable Diffusion läuft lokal (ComfyUI oder Automatic1111)
  - LoRA auf vorhandenen MUNI-Assets trainiert
  - Mindestens 3 reproduzierbare Outputs im MUNI-Stil erzeugt
  - Pipeline im TOOLBAUKASTEN_principles dokumentiert

Abgrenzung — nicht Teil dieses Sprints:
  - Kein User-facing Output — rein DEV-internal
  - Kein vollständiger Stil-Guide (folgt nach erstem Training)
  - Keine Integration in automatisierte R+MUNI Scripts
  - Keine Entscheidung über Midjourney / andere externe Tools


================================================================================
3. FACHLICHER MEHRWERT
================================================================================

Mehrwert für: DEV / Außenwirkung / Skalierbarkeit

  - Visueller Stil ist reproduzierbar — kein kreativer Drift zwischen Assets
  - Lokale Ausführung = keine Cloud-Kosten, keine Datenschutzfragen
  - Vorhandene MUNI-Grafiken werden als Trainingsbasis genutzt — kein Neustart
  - Blueprint-Prinzip "deterministisch und wiederholbar" gilt jetzt auch für Visuals
  - Entkopplung von Cloud-Anbietern (Copilot, Midjourney) für Kern-Assets

Ohne diesen Sprint:
  Visuelle Identität bleibt ad-hoc. Jede neue Grafik ist eine neue
  Stilentscheidung. Außenwirkung (README, Doku, Präsentationen) bleibt
  inkonsistent und skaliert nicht mit dem Projekt.


================================================================================
4. ABHÄNGIGKEITEN UND VORAUSSETZUNGEN
================================================================================

Voraussetzungen:
  - GPU-fähige Hardware vorhanden              Status: zu prüfen
  - Vorhandene MUNI-Assets als Trainingsdaten  Status: erfüllt
  - Stable Diffusion Toolwahl getroffen        Status: offen (ComfyUI vs. A1111)

Blockiert durch:
  - GPU-Check (VRAM-Anforderung für LoRA-Training klären)

Ermöglicht danach:
  [[TOOLBAUKASTEN_principles_S7]]    Eintrag Creative-Pipeline ergänzen
  [[AI_DRIVEN_DEV_METHODE_S7U1]]     Copilot-Rollentrennung + SD-Pipeline dokumentiert
  Stil-Guide Sprint                  Erst nach erstem erfolgreichem Training sinnvoll


================================================================================
5. GESCHÄTZTER UMFANG
================================================================================

Komplexität:   Hoch — neues Toolset, neue Technologie, lokales Setup
Risiko:        Mittel — Hardware-Abhängigkeit (VRAM), Lernkurve LoRA-Training

Grobe Einschätzung:
  Phase 1 — Setup:     Stable Diffusion lokal installieren + Basisfunktion testen
  Phase 2 — Training:  LoRA auf MUNI-Assets trainieren (iterativ)
  Phase 3 — Validierung: Outputs prüfen, Stil-Konsistenz bewerten
  Phase 4 — Doku:      Pipeline in TOOLBAUKASTEN und Methodik eintragen

Besondere Risiken:
  - VRAM unter 8GB → LoRA-Training nicht lokal möglich → Fallback klären
  - Trainingsdaten-Qualität entscheidet Stil-Ergebnis — Kuratierung nötig


================================================================================
6. PRIORISIERUNG
================================================================================

Priorität:     Mittel
Zeitrahmen:    Stage 7 — nach S7-Z1 und S7-Z2

Priorisiert durch:
  Außenwirkung Stage 7 (S7-Z4/Z5/Z6) profitiert von konsistenten Visuals.
  Kein harter Blocker — aber je früher das Training läuft desto früher
  stehen Assets für GitHub Paketierung und README bereit.

Kann verschoben werden wenn:
  Hardware-Voraussetzungen nicht erfüllt → dann Stage 8 Einstieg


================================================================================
7. GOVERNANCE-CHECK
================================================================================

| Kriterium                          | Status | Anmerkung                              |
|------------------------------------|--------|----------------------------------------|
| Auslöser GOV-konform (GOV 10.3)    | OK     | Feature / Entwicklerwunsch             |
| Fachlicher Mehrwert benennbar      | OK     | Siehe Kapitel 3                        |
| Ziel explizit und überprüfbar      | OK     | Erfolgskriterien definiert             |
| Abgrenzung definiert               | OK     | DEV-only, kein User-Scope              |
| Rückkopplungsschutz geprüft        | OK     | Kein Eingriff in Stage 3/4/5/6 Scripts |
| Keine implizite GOV-Änderung       | OK     | TOOLBAUKASTEN-Erweiterung additiv      |


================================================================================
8. STATUS UND VERLAUF
================================================================================

2026-03-22  ERSTELLT     EUMAXL + Claude (Pair-Session, Methodik-Chat S7)
                         Auslöser: Copilot-Evaluierung + AI Driven DEV Update


================================================================================
BEZÜGE
================================================================================
[[GOV_Global_S6]]                        normative Grundlage
[[FREEZE-6_konsolidiert]]                aktueller Ausgangszustand
[[AI_DRIVEN_DEV_METHODE_S7U1]]           Methodik-Update mit Copilot-Rollentrennung
[[TOOLBAUKASTEN_principles_S6]]          wird nach Sprint um Creative-Pipeline ergänzt
[[STAGE7_ZIELE]]                         S7-Z4/Z5/Z6 Außenwirkung als Kontext


================================================================================
Sprint-DEV-BACKLOG_VisualAsset-SD-LoRA | S7 | 2026-03-22 | R+MUNI Blueprint
================================================================================
