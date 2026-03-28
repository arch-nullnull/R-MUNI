================================================================================
DUMMY BLUEPRINT MD OBSIDIAN TEMPLATE
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : DUMMY_Blueprint_MD_Obsidian_S8
Tag             : #dev #template #obsidian #dummy #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
================================================================================

---
title: "<Dokumenttitel>"
stage: <STAGE>
status: "<ENTWURF / AKTIV / ARCHIV>"
typ: "<How2 / Sprint / GOV / Prinzipien / Backlog>"
datum: "<YYYY-MM-DD>"
autor: EUMAXL
tags: [rmuni, blueprint, <stage-tag>]
---

================================================================================
<TITEL DES DOKUMENTS>
Stage <N> | <Status> | R+MUNI Blueprint
================================================================================

---

## Kontext

Kurze Einleitung in 2–3 Sätzen. Was ist dieses Dokument, warum existiert es,
für wen ist es gedacht. Kein Roman – nur das Nötigste damit der Leser
sofort weiß ob er hier richtig ist.

---

## Verwandte Dokumente

- [[GOV_Global_S<aktuell>]]                normative Grundlage
- [[FREEZE-<N-1>]]                         aktueller Ausgangszustand
- [[<weiteres verwandtes Dokument>]]       <warum relevant>

---

## Inhalt

### Abschnitt 1

Text hier. Markdown unterstützt **fett** und *kursiv* – sparsam einsetzen.
Fett nur für echte Schlüsselbegriffe, nicht zur Dekoration.

### Abschnitt 2

Weitere Inhalte. Überschriften maximal bis H3 (###) verwenden –
tiefer wird es unübersichtlich und ist im Blueprint selten nötig.

---

## Tabelle

| Spalte 1     | Spalte 2        | Spalte 3     |
|--------------|-----------------|--------------|
| Wert A       | Beschreibung A  | Status A     |
| Wert B       | Beschreibung B  | Status B     |
| Wert C       | Beschreibung C  | Status C     |

---

## Diagramm – SVG aus Archi

> Archi → View auswählen → Datei → Exportieren → Bild exportieren → SVG
> Ablage: R+MUNI Doku-creative\images\r+muni\diagrams\
> Namenskonvention: <reihe>_<beschreibung>_S<N>.svg

![Diagrammbeschreibung](../../R+MUNI Doku-creative/images/r+muni/diagrams/<name>_S<N>.svg)

---

## Diagramm – SVG von Claude generiert

> SVG-Code aus Claude kopieren → Notepad++ → als .svg speichern
> Ablage: R+MUNI Doku-creative\images\r+muni\diagrams\
> Namenskonvention: <reihe>_<beschreibung>_claude_S<N>.svg

![Diagrammbeschreibung](../../R+MUNI Doku-creative/images/r+muni/diagrams/<name>_claude_S<N>.svg)

---

## Diagramm – PNG Fallback

> Nur wenn SVG nicht möglich – SVG ist immer bevorzugt.
> Ablage: R+MUNI Doku-creative\images\r+muni\diagrams\

![Diagrammbeschreibung](../../R+MUNI Doku-creative/images/r+muni/diagrams/<name>_S<N>.png)

---

## Optische Elemente – Referenz

Trennlinie – nur zwischen großen Abschnitten, sparsam:

---

Blockquote – für Hinweise, Warnungen, Kontext:

> Das ist ein Hinweis der aus dem Fließtext heraussticht.
> Für Warnungen, Tipps oder Kontextinformationen.

Code-Block – für Scripts, Pfade, Befehle:

```python
# Python Beispiel
print("R+MUNI Blueprint")
```

```
# Pfad oder Befehl
R+MUNI Doku-public\02-how2\<Dokumentname>.md
```

Aufzählung ungeordnet – für gleichwertige Punkte:

- Punkt A
- Punkt B
- Punkt C

Aufzählung geordnet – für Schritte mit Reihenfolge:

1. Schritt 1
2. Schritt 2
3. Schritt 3

---

## Bezüge

[[GOV_Global_S<aktuell>]]           normative Grundlage
[[FREEZE-<N-1>]]                    aktueller Ausgangszustand
[[<weiteres verwandtes Dokument>]]  <warum relevant>

---

================================================================================
<TITEL> | S<N> | <YYYY-MM-DD> | R+MUNI Blueprint
================================================================================
