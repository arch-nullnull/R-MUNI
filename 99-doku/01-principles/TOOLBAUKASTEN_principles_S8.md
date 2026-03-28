================================================================================
TOOLBAUKASTEN – PRINCIPLES
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : TOOLBAUKASTEN_principles_S6
Tag             : #dev #principles #toolbaukasten #s6 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-21
Basis           : Install.txt (2026-03-17) + Betakundenfeedback
Ablageort       : 00-concept/01-principles/TOOLBAUKASTEN_principles_S6.md
================================================================================


ZWECK DIESES DOKUMENTS
================================================================================

Interne DEV-Referenz für R+MUNI Toolbaukasten-Struktur (S6-Z6).

Richtet sich an:
  → EUMAXL (Developer)
  → Zukünftige Dev-Teams
  → Technische Partner

Aufgaben:
  ✓ Klare Struktur: MINIMAL | DEFAULT | ADDON ENTERPRISE
  ✓ Kostenmodell transparent
  ✓ Community-Support-Philosophie (Patron-Modell)
  ✓ Abhängigkeiten abbilden
  ✓ Basis für How2 DEV und How2 USER


================================================================================
1. TOOLBAUKASTEN-STRUKTUR
================================================================================

R+MUNI folgt einer **bewussten Skalierungsstruktur:**

MINIMAL
  Absolutes Kernpaket für R+MUNI Basis-Funktionen
  → Modellieren, Exportieren, Scripten
  → Alles kostenlos, stabil, quelloffen
  → User-Einstieg: hier anfangen

DEFAULT (Standard-Empfehlung)
  Vollständiger Betrieb für produktiven Einsatz
  → Alle MINIMAL-Komponenten + erweiterte Tools
  → Automatisierung, IDE-Komfort, Zusammenarbeit
  → 100% kostenlos

ADDON ENTERPRISE
  Opt-in Erweiterungen für spezifische Use Cases
  → BOC Group (Enterprise EA/BPMN)
  → Atlassian Full (kostenpflichtig)
  → O365 (geplant)


1.2 Philosophie: Kostenlos ist die Basis
------------------------------------------

Kern-Versprechen:
  "Der Kern bleibt kostenlos. Erweiterte Features sind optional."

EUMAXL's Prinzip (GOV 13.x):
  "Alle sollen leben und Spaß haben.
   Es soll Sinn machen und funktionieren."

Praktisch:
  → 1 Stunde/Woche EUMAXL's Arbeitszeit = Archi Patron
  → Beta-Kunden profitieren von Community-Finanzierung
  → Wenn Qualität + Mehrwert da sind → Investition ist intelligent


================================================================================
2. MINIMAL – KERN-PAKET
================================================================================

2.1 Archi 5.8
  → Download: https://www.archimatetool.com/download/
  → EPL 2.0 (kostenlos)
  → Single Source of Truth für Enterprise Architecture
  → CSV-Export = Master-ID-Quelle
  → Patron-Modell: https://www.patreon.com/cw/architool
  → Kosten: 0 EUR

2.2 Camunda Modeler
  → https://camunda.com/download/modeler/
  → Kostenlos (Elastic License)
  → BPMN 2.0 Modellierung
  → XML-basiert, versionierbar
  → Kosten: 0 EUR

2.3 Python 3.9+
  → https://www.python.org/
  → PSF License (kostenlos)
  → CSV/XML Automation
  → Standard Library reicht
  → Kosten: 0 EUR

2.4 jArchi 1.11.0 (Free Edition)
  → GitHub: https://github.com/archimatetool/archi
  → EPL 2.0 (kostenlos, Free Edition)
  → JavaScript Scripting in Archi
  → Plugin via Archi Plugin Manager installierbar
  → Kosten: 0 EUR

2.5 OpenJDK 11+
  → https://adoptium.net/
  → GPL 2 (kostenlos)
  → Runtime für Archi, Camunda, jArchi
  → Kosten: 0 EUR

SUMME MINIMAL: 0 EUR


================================================================================
3. DEFAULT – VOLLSTÄNDIGER BETRIEB
================================================================================

Setzt MINIMAL voraus. Erweitert um produktive Tools.

3.1 Notepad++ mit Plugins
  → https://notepad-plus-plus.org/
  → GPL 2.0 (kostenlos)
  → XML Tools, CSV Lint, NPPEXEC, Compare Plugins
  → Editorierung + Validierung für alle Dateitypen
  → Kosten: 0 EUR

3.2 Git (2.53.0.2+) — Technischer Unterbau
  → https://git-scm.com/
  → Open Source (kostenlos)
  → Basis für VS Code + Claude Integration (BASH)
  → Enables GitHub Sync
  → Kosten: 0 EUR

3.3 GitHub — Core Component (Versionskontrolle & Sync)
  → https://github.com/
  → Kostenlos (Public + Private Repos)
  → Repository-Verwaltung, Backup, Team-Sync
  → Core Component im R+MUNI Standard-Setup
  → Kosten: 0 EUR

3.3 Obsidian
  → https://obsidian.md/
  → Free Core (optional: Sync/Publish kostenpflichtig)
  → Markdown-Vault Navigation
  → MD-Zusammenhänge visualisieren
  → Für Doku-Struktur essenziell
  → Kosten: 0 EUR (Core)

3.4 draw.io
  → https://www.drawio.com/
  → Open Source (kostenlos)
  → Rein visuelle Diagramme (nicht ArchiMate/BPMN)
  → Infrastruktur-Skizzen, ad-hoc Visualisierungen
  → Kosten: 0 EUR

3.5 Inkscape
  → https://inkscape.org/
  → GPL (kostenlos)
  → SVG-Bearbeitung (Archi 5.7 SVG Export)
  → Grafik-Nachbearbeitung
  → Kosten: 0 EUR

3.6 PowerShell 7
  → https://github.com/PowerShell/PowerShell
  → MIT License (kostenlos)
  → Batch-Automation, Python-Orchestrierung
  → Task-Scheduling, Dateisystem-Operationen
  → Kosten: 0 EUR

3.7 Claude Desktop (DEV-only)
  → https://claude.ai/
  → Pro Abo: 20 USD/Monat (für EUMAXL)
  → AI Driven Development
  → Code, Dokumentation, Struktur-Arbeit
  → Kosten: 20 USD/Monat (DEV-only, nicht User-relevant)

3.8 Copilot (optional, falls M365/GitHub Pro)
  → Microsoft 365 oder GitHub Pro
  → Oft bereits in Lizenzen enthalten
  → Code-Assist, Office-Integration
  → Kosten: 0 EUR (usually already licensed)

3.9 KeePass
  → https://keepass.info/
  → GPL (kostenlos)
  → Zentrale Credential-Verwaltung
  → AES-256 Verschlüsselung
  → Kosten: 0 EUR

SUMME DEFAULT (für User): 0 EUR
SUMME DEFAULT (für DEV/EUMAXL): 20 USD/Monat


================================================================================
4. EBENE 3 – DEV-ONLY (nur Entwicklung, User-irrelevant)
================================================================================

DEV-ONLY Tools sind ausschließlich für EUMAXL und zukünftige Dev-Teams.
User sehen diese nicht und brauchen sie nicht.


4.1 Atlassian (Jira & Confluence)
  → https://www.atlassian.com/
  → Free Plan: 0 EUR (bis 10 User, intern)
  → Standard Plan: 6-7 EUR/User/Monat (optional)
  → Interne Ticketing, Sprint-Verwaltung, Dokumentation
  → DEV-ONLY: User haben keinen Zugang, sehen das nicht
  → Basis für interne Dev-Prozesse (nicht User-Frontend)
  → Kosten: 0 EUR (Free Plan, intern) oder nach Bedarf

4.2 VS Code + MCP (DEV-IDE, optional für Zukunft)
  → https://code.visualstudio.com/
  → VS Code: kostenlos
  → MCP Integration mit Claude: 20 USD/Monat
  → IDE für erweiterte Entwicklung (optional, nicht aktuell in Verwendung)
  → Notepad++ reicht vollständig aus für Standard-Betrieb
  → Interessant wenn: Größeres Team, erweiterte IDE-Features gewünscht
  → Kosten: 0 EUR (VS Code) + 20 USD (Claude)


================================================================================
5. EBENE 4 – ADDON ENTERPRISE (agnostisch importierbar)
================================================================================

Opt-in Erweiterungen. Usecase-abhängig. Nicht erzwungen.

5.1 BOC Group (ADOIT/ADONIS)
  → https://www.boc-group.com/de/
  → Kostenpflichtig (Enterprise)
  → Exitpoint für Enterprise EA/BPMN
  → Archi → OEF Export → BOC importierbar
  → Nur bei Customer-Bedarf
  → Kosten: Customer-abhängig

5.2 O365 Integration (geplant)
  → Noch nicht implementiert
  → Zeithorizont: Stage 7+
  → Kosten: abhängig von O365 Lizenzen


================================================================================
5. ZUSAMMENFASSUNG: KOSTENMODELL
================================================================================

MINIMAL (absolut notwendig):
  0 EUR für User

DEFAULT (Standard, empfohlen):
  0 EUR für User
  20 USD/Monat für EUMAXL (DEV)

ADDON ENTERPRISE:
  0-200+ EUR/Monat (Customer-abhängig, nie erzwungen)

COMMUNITY-SUPPORT MODELL:
  → 1 Stunde/Woche EUMAXL's Zeit = Archi Patron
  → Beta-Kunden profitieren von nachhaltiger Finanzierung
  → "Alle sollen leben und Spaß haben"


================================================================================
6. ABHÄNGIGKEITSMATRIX
================================================================================

MINIMAL:
  Archi 5.8 ─→ OpenJDK
  Camunda ──→ OpenJDK
  jArchi ───→ Archi + OpenJDK 21
  Python ───(standalone)
  OpenJDK ──(standalone)

DEFAULT (auf MINIMAL aufbauend):
  Notepad++ ─→ alle Dateitypen editieren
  Git ───────→ Versionskontrolle
  GitHub D. ─→ benötigt Git
  Obsidian ──→ liest MD aus Blueprint
  draw.io ───(standalone)
  Inkscape ──→ SVG-Export aus Archi 5.7
  PowerShell ─→ orchestriert Python Scripts
  Claude ────→ Dev-Support (intern)
  KeePass ────→ speichert Credentials

ADDON:
  Atlassian → optional
  BOC ──────→ optional
  VS Code ──→ optional DEV-Addon


================================================================================
7. ARCHITEKTUR-PRINZIPIEN (nicht verhandelbar)
================================================================================

✓ Kern bleibt kostenlos (Archi, Python, Camunda)
✓ Keine proprietären Single-Source-of-Truth Tools
✓ Agnostisch importierbar (aber nicht erzwungen)
✓ Community-Support ist Governance-Prinzip
✓ Wenn Mehrwert erkannt → investieren ist nicht peinlich


================================================================================
8. VERSIONSSTABILITÄT (aktuell 2026-03-21)
================================================================================

STABIL (sicher)
  Archi 5.8 ─ seit 2022, regelmäßige Updates
  Camunda 4.x ─ regelmäßige Updates, no breaking changes
  Python 3.9+ ─ LTS bis 2025
  OpenJDK 21 ─ LTS
  PowerShell 7 ─ Cross-platform, stabil
  Git ───────── Standard, etabliert
  Notepad++ ─── aktiv gepflegt
  Obsidian ──── aktive Community

OPTIONAL (häufigere Updates)
  Claude ────── Updates häufiger, neue Features


================================================================================
ABSCHLUSS
================================================================================

Dieses Dokument definiert die interne DEV-Struktur des Toolbaukastens.

Dient als:
  → Referenz für EUMAXL und zukünftige Dev-Teams
  → Basis für How2 DEV S6
  → Basis für How2 USER S6
  → Governance-Fundament (GOV 13.x)

Nächste Schritte (S6-Z6):
  1. How2 DEV S6 — Developer-fokussierte Anleitung (aus Principles)
  2. How2 USER S6 — User-freundliche Anleitung (vereinfacht aus Principles)
  3. README Update — mit Links auf How2 USER


================================================================================
TOOLBAUKASTEN – PRINCIPLES
Status: AKTIV | Datum: 2026-03-21
R+MUNI Blueprint | Erstellt durch EUMAXL + Claude | Basis: Install.txt 2026-03-17
================================================================================
