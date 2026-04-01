# BACKLOG — Image Library für Präsentationen & Archi
**Stage 100 | Phase 1.xx | Ablage: R+MUNI Doku-internal\backlog\**
**Status: OFFEN | Erstellt: 2026-03-29 | Autor: EUMAXL | Rev: 2026-03-29-G**

---

## 1. ZIEL UND SCOPE

Die Image Library ist eine **zentrale, versionierte Sammlung von visuellen Assets**
für zwei Verwendungszwecke:

| Verwendung | Beschreibung |
|---|---|
| **Präsentationen** | PowerPoint / PPTX-Folien |
| **Archi / ArchiMate** | Kachel-Icons, Fill-Bilder in Views, Inline-Objekte |

Die Library ist **kein One-Time-Shoot** — sie ist eine lebende Sammlung mit
Governance, Drift-Kontrolle und definiertem Freigabe-Workflow.

---

## 2. LIZENZ UND VERWENDUNGSRECHT

Selbst erstellte Assets sind **frei verwendbar** — keine Einschränkung.

Ausnahme: Assets in einem gesondert gekennzeichneten Ordner
(Ordner werden von EUMAXL vorgegeben) gelten als lizenzrechtlich eingeschränkt.

---

## 3. ENTSCHIEDENE GRUNDPRINZIPIEN

### E1 — Dual-Format-Strategie (ENTSCHIEDEN)
Jedes Asset existiert in **zwei Dateiformaten**, beide werden versioniert:

```
PNG  →  Primärformat (KI-Erstellung, Archi-Kacheln, PPTX)
SVG  →  Sekundärformat (MD-Doku, Obsidian — abgeleitet aus PNG via Inkscape)
```

PNG ist das einzige Format das Archi für Kachel-Icons akzeptiert (→ Abschnitt 4).
SVG wird in Obsidian und GitHub MD direkt gerendert: `![label](pfad/asset.svg)`

**Workflow PNG → SVG:**
1. PNG in Inkscape öffnen → `Pfad → Bitmap nachzeichnen`
2. Als **Plain SVG** exportieren (nicht "Inkscape SVG")
3. Oder: Batch-Konvertierung via `IMG_convert.py` (→ BL-IMG-04)

**Hinweis Erstellungsweg:**
Kurzfristig: Claude / Copilot erzeugen PNG-Ausgangsmaterial.
Mittelfristig: Stable Diffusion + LoRA sobald Pipeline aus
`Sprint-DEV-BACKLOG_VisualAsset-SD-LoRA_S7` aktiv ist (→ Abschnitt 11).

### E2 — Inventar läuft über Obsidian MD (ENTSCHIEDEN)
Eine MD-Datei pro Asset-Gruppe, verlinkt über eine zentrale Index-MD.
Frontmatter für Metadaten (Status, Format, Version).
Obsidian Graph-View macht Verlinkungen zwischen Assets und Doku sichtbar.

### E3 — Freigabe-Workflow (ENTSCHIEDEN)
```
intern (DEV)  →  review  →  public  →  associate (wenn relevant)
```
Dieser Zyklus steuert die **Freigabe** — nicht die Zielgruppe.
Assets sind nach Freigabe für alle Zielgruppen verwendbar.

### E4 — SVG-Einbindung in Obsidian per externem File-Link (ENTSCHIEDEN)
Freeze-8-Regel: `![[asset.svg]]` — kein Inline-SVG. Plain SVG Pflicht.

---

## 4. FORMAT- UND GRÖSSEN-MATRIX

### 4.1 Archi — drei Verwendungsorte, unterschiedliche Anforderungen

Archi unterstützt **kein SVG als Import-Format**.
SVG ist in Archi nur ein Export-Format (View → Bild exportieren).
Für alle Einbindungen in Archi gilt: **ausschließlich PNG**.

| Verwendungsort in Archi | Format | Empfohlene Größe | Transparenz |
|---|---|---|---|
| **Specialization Icon** (Kachel, oben rechts) | PNG | 64×64 px | Pflicht (Alpha) |
| **Specialization Fill** (ganze Kachelfläche) | PNG | 512×512 px | empfohlen |
| **Inline-Bild-Objekt** (frei im View) | PNG, JPG | beliebig | optional |
| **View-Export** (Archi → Ausgabe) | PNG, SVG, PDF, JPG, BMP | — | n/a |

### 4.2 Vollständige Format-Matrix

| Verwendungsort | Format | Größe | Transparenz |
|---|---|---|---|
| Archi — Specialization Icon | **PNG** | 64×64 px | Pflicht |
| Archi — Specialization Fill | **PNG** | 512×512 px | empfohlen |
| Archi — Inline-Objekt | PNG, JPG | beliebig | optional |
| Archi — HTML-Report (HLP09) | PNG | wie im View | — |
| MD-Doku / Obsidian | **SVG** | vektorbasiert | — |
| GitHub MD (public Doku) | SVG | vektorbasiert | — |
| PPTX — Präsentation | PNG | 512×512 — 1024×1024 px | empfohlen |

### 4.3 Drei Dateivarianten pro Asset

| Variante | Größe | Format | Verwendung |
|---|---|---|---|
| **icon** | 64×64 px | PNG mit Alpha | Archi Specialization Icon |
| **full** | 512×512 px | PNG mit Alpha | Archi Fill + PPTX + Bestand |
| **svg** | vektorbasiert | Plain SVG | MD-Doku, Obsidian, GitHub |

SVG wird aus der **full-Variante** abgeleitet.

---

## 5. NAMING-KONVENTION

```
[thema]_[set]_[groesse]_v[n].[ext]

Beispiele:
  firewall_dev_icon_v1.png     ← 64×64px, Archi Icon-Position
  firewall_dev_full_v1.png     ← 512×512px, Archi Fill + PPTX
  firewall_dev_full_v1.svg     ← aus full, MD-Doku
  brain_shared_full_v2.svg

Regeln:
  - Kleinbuchstaben, kein Leerzeichen, kein Umlaut (oe/ue/ae)
  - set:     dev | elite | associate | mgt | shared
  - groesse: icon (64×64) | full (512×512)
  - v[n]:    v1 = Erstversion, v2 = erste Überarbeitung
  - ext:     png | svg
```

---

## 6. THEMATISCHER SCOPE DER INHALTE

- **R+MUNI Stack** — Archi, Python, GitHub, Obsidian, Jira, Confluence, Claude, Excel, BPMN
- **Klassisches RZ-Inventar** — Firewall bis Client OS
- **Konzept-Illustrationen** — bestehende Zeichnungen aus `07-creative\images\draw\`
- **Logos und Marken-Assets** — Streaming-Dienste als Kontext-Illustrationen

---

## 7. ASSET-LIFECYCLE UND FREIGABE-WORKFLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                    ASSET-LIFECYCLE                              │
│                                                                 │
│  [1] ERSTELLUNG        PNG-Ausgabe aus KI-Tool                  │
│       ↓                Kurzfristig: Claude / Copilot            │
│                        Mittelfristig: Stable Diffusion + LoRA   │
│                        2 Größen: icon (64px) + full (512px)     │
│                                                                 │
│  [2] INKSCAPE-PASS     full-PNG → SVG (Plain SVG)               │
│       ↓                via Inkscape GUI oder IMG_convert.py     │
│                                                                 │
│  [3] INTERN            Alle 3 Dateien in Library                │
│       ↓                Status: "intern"                         │
│                                                                 │
│  [4] REVIEW            Stil? Lizenz? Archi OK?                  │
│       ↓                Status: "review"                         │
│                                                                 │
│  [5] PUBLIC            Freigabe für R+MUNI Doku-public          │
│       ↓                Status: "public"                         │
│                                                                 │
│  [6] ASSOCIATE         Wenn relevant: in Associate-Doku         │
│                        Status: "associate"                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. OBSIDIAN-INVENTAR-STRUKTUR

Die Ordnerstruktur wird von EUMAXL vorgegeben — kein Eingriff durch Scripts.
Referenz-Struktur:

```
image-library\
  00-index\
    IMG_INDEX.md
    IMG_GOVERNANCE.md
  01-stack\
    IMGGRP_stack.md
    dev\   elite\   shared\
  02-rz-inventar\
    IMGGRP_rz.md
    dev\   elite\   shared\
  03-draw\
    IMGGRP_draw.md
    shared\
  04-logos\
    IMGGRP_logos.md
    approved\   review\
  05-archi-inline\
    IMGGRP_archi.md
    stack\   rz\   draw\
```

### Aufbau eines Asset-Eintrags (Beispiel):

```markdown
## Firewall
- **ID:** RZ-001
- **Status:** intern
- **Formate:**
  - `firewall_dev_icon_v1.png`   ← 64×64px — Archi Icon
  - `firewall_dev_full_v1.png`   ← 512×512px — Archi Fill + PPTX
  - `firewall_dev_full_v1.svg`   ← MD-Doku
- **Erstellungsweg:** Claude PNG → Inkscape → SVG
- **Letzte Prüfung:** 2026-03-29
- **Verwendet in:** —
- **Notiz:** —

![[firewall_dev_full_v1.svg]]
```

### `IMG_INDEX.md` — Gerüst:

```markdown
---
title: Image Library Index
stage: S101
typ: image-index
---

# Image Library — Master-Index

| Gruppe | MD-Link | Assets | Status |
|---|---|---|---|
| R+MUNI Stack | [[IMGGRP_stack]] | 0 | geplant |
| RZ-Inventar | [[IMGGRP_rz]] | 0 | geplant |
| Konzept-Draw | [[IMGGRP_draw]] | 40+ | migration |
| Logos | [[IMGGRP_logos]] | 5 | aktiv |
| Archi-Inline | [[IMGGRP_archi]] | 0 | geplant |

Governance: [[IMG_GOVERNANCE]]

## Letzte Review
<!-- Datum + 3-Zeilen-Notiz bei jedem Stage-Abschluss -->
```

---

## 9. TECHNISCHER WORKFLOW — PNG ZU SVG

### 9.1 Manuell via Inkscape GUI

1. Inkscape öffnen (im Stack vorhanden)
2. `Datei → Öffnen` → full-PNG wählen
3. `Pfad → Bitmap nachzeichnen`
   - Einfarbig: `Helligkeit-Schwellenwert`
   - Mehrfarbig: `Farben`, Scans 8–16 → `OK`
4. Original-Bitmap löschen (anklicken → Entf)
5. `Datei → Speichern als` → **Plain SVG**

### 9.2 Batch via IMG_convert.py

```powershell
# Einzeldatei:
python 01-artifacts\01-scripts\IMG_convert.py --input firewall_dev_full_v1.png

# Ganzer Ordner:
python 01-artifacts\01-scripts\IMG_convert.py --folder image-library\02-rz-inventar\dev\

# Mit icon-Crop (erzeugt zusätzlich 64×64):
python 01-artifacts\01-scripts\IMG_convert.py --folder image-library\02-rz-inventar\dev\ --icon
```

---

## 10. ARCHI SPECIALIZATION MANAGER — KURZANLEITUNG

**Schritt 1:** `Tools → Specializations Manager → Neu`
Name vergeben → ArchiMate-Typ wählen

**Schritt 2:** Tab "Image" → `Add Image...`
→ icon-PNG für `Top Right` | full-PNG für `Fill`

**Schritt 3:** Specialization auf Element anwenden
Element auswählen → Properties → Tab "Main" → Feld "Specialization"

**Hinweis:** .archimate-File wird nach Bildzuweisung als ZIP gespeichert — normal.

---

## 11. BACKLOG-ITEMS

### BL-IMG-01 — Governance-Dokument anlegen
**Priorität:** HOCH | **Aufwand:** S

`IMG_GOVERNANCE.md` anlegen mit Format-Matrix, Naming-Konvention,
Lizenz-Grundregel und Drift-Regeln (→ BL-IMG-06).

**Akzeptanzkriterium:** Datei in `00-index\` abgelegt und befüllt.

---

### BL-IMG-02 — Bestand migrieren und inventarisieren
**Priorität:** HOCH | **Aufwand:** M

40+ Assets aus `07-creative\images\draw\` nach Naming-Konvention umbenennen,
nach `image-library\03-draw\shared\` kopieren, in `IMGGRP_draw.md` eintragen.
Pilot: 5 Assets → SVG + Obsidian-Test. 2 Assets → Archi-Test.

```powershell
# Encoding-Fehler finden:
Get-ChildItem "07-creative\images\draw\" | Where-Object {$_.Name -match '[^a-zA-Z0-9._\-]'}
```

Originale bleiben in `draw\` — Migration kopiert, löscht nicht.

**Akzeptanzkriterium:** Alle Assets inventarisiert. Pilot SVG + Archi OK.

---

### BL-IMG-03 — Logos inventarisieren
**Priorität:** NIEDRIG | **Aufwand:** S

Streaming-Dienste (Netflix, Spotify, YouTube, WhatsApp, Teams, Zoom)
mit Lizenz-Status in `IMGGRP_logos.md` eintragen.

**Akzeptanzkriterium:** Alle Kandidaten mit Status eingetragen.

---

### BL-IMG-04 — Python-Script IMG_convert.py bauen
**Priorität:** MITTEL | **Aufwand:** M

PNG → SVG via Inkscape CLI + icon-Crop via Pillow.
HLP00-Pattern, Logging, Fehlerbehandlung.

```
root.cfg Erweiterung:
inkscape_path=C:\Program Files\Inkscape\bin\inkscape.exe
```

Ablage: `01-artifacts\01-scripts\IMG_convert.py`

**Akzeptanzkriterium:** 5 Test-PNGs konvertiert. `--icon` erzeugt 64×64. Log OK.

---

### BL-IMG-05 — Obsidian Index-MD und Gruppen-MDs anlegen
**Priorität:** HOCH | **Aufwand:** S

`IMG_INDEX.md` + alle 5 `IMGGRP_*.md` anlegen.
Ordner werden von EUMAXL vorgegeben — nur MD-Dateien.

**Akzeptanzkriterium:** Index verlinkt alle Gruppen. Obsidian Graph OK.

---

### BL-IMG-06 — Drift-Kontrolle verankern
**Priorität:** MITTEL | **Aufwand:** S

| Drift-Auslöser | Aktion |
|---|---|
| R+MUNI Branding-Änderung | Assets reviewen |
| Neues Tool im Stack | Content-Sprint auslösen |
| SD+LoRA Pipeline aktiv | Erstellungsweg in `IMG_GOVERNANCE.md` aktualisieren |
| Stage-Abschluss | Spot-Check, Datum in `IMG_INDEX.md` |

**Akzeptanzkriterium:** Drift-Tabelle in `IMG_GOVERNANCE.md`.

---

## 12. GOV-CHECK

| Prüfpunkt | Ergebnis |
|---|---|
| Rückkopplungsschutz berührt? | Nein |
| Ordnerstruktur | Von EUMAXL vorgegeben |
| IMG_convert.py | IMG-Reihe, keine Überschneidung |
| Obsidian SVG-Regel | Ja — Plain SVG, `![[]]` |
| GOV-Freigabe | Nur für IMG_convert.py |
| Stage-Einordnung | Stage 100 / Phase 1.xx |

---

## 13. BEZÜGE

```
[[GOV_Global_S6]]
[[FREEZE_8]]
[[Sprint-DEV-BACKLOG_VisualAsset-SD-LoRA_S7]]   ← zukünftiger PNG-Erstellungsweg
[[TOOLBAUKASTEN_principles_S8]]                  ← Inkscape im Stack
[[AI_DRIVEN_DEV_METHODE_S8]]
```

---

*Ablage: `R+MUNI Doku-internal\backlog\BACKLOG_ImageLibrary_S101.md`*
