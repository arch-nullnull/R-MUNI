# R+MUNI
### Open Source EA & Process Modeling Toolset Beta 0.3x

---

## Über das Projekt

R+MUNI ist mein persönliches Projekt — entstanden in meiner Freizeit, aus echtem Interesse und mit echter Überzeugung.

Ja, im Kern sind es ein paar Scripts die irgendwas machen. Aber für mich ist es weit mehr als das.

R+MUNI ist eine Perspektive: etwas Sinnstiftendes zu schaffen, das vielleicht wirklich jemandem helfen kann — **ohne schlechtes Gewissen, ohne versteckte Abo-Fallen, ohne Hintertüren.**

Das ist die Idee hinter R+MUNI. Und deshalb ist diese Lösung **kostenlos** — und das ist ein Prinzip, das für diesen Blueprint und alle seine Weiterentwicklungen gilt.

**R+MUNI** steht für **Multi Usable Norm Interface** — ein XML-basiertes Kreislaufsystem das Enterprise Architecture Visualisierung mit Prozessmodellierung vereint. Entwickelt für österreichische KMU bis maximal 50 User, die komplexe Fragestellungen (IT-Landschaften, Verwaltungsprozesse, Unternehmensentwicklung) mit freien Tools ganzheitlich darstellen wollen.

---

### Was R+MUNI macht

- R+MUNI ist ein Arbeitstoolset für Modellierer im KMU und Mittelstand, das man durch das agnostische XML-Konzept für so ziemlich alles zweckentfremden kann (aber nicht muss 😉)
- Der "ESEL" verbindet **ArchiMate 3.2** (EA-Modellierung) [opengroup.org](https://www.opengroup.org/) und **BPMN 2.0** [bpmn.org](https://www.bpmn.org/) (Prozessmodellierung) über ein gemeinsames XML-Master-Child-Kreislaufkonzept
- Nutzt **Archi 5.8** als Master-ID-gebendes System über die CSV-Schnittstelle und OEF-Export-Mechanismen
- Automatisiert Workflows über einen Python-basierten Scriptrunner (`flw00-scriptrunner.py`)
- Bleibt **tool-agnostisch** — strikt nach offenen Normen, keine proprietären Abhängigkeiten
- Exportiert valide BPMN 2.0 und ArchiMate OEF — direkt importierbar in Enterprise-Tools (z.B. ADONIS/ADOIT der BOC-Group)
- Startet Archi HTML Reports und hostet diese unter eigenem Namen (mehrere HTML Reports auf Port-Ebene)
- 3rd Party Integration über CSV-Routinen in ArchiMate 3.2 bzw. master.xml Kreislauf
- Archi XLSX Export – CSV Importformat damit man auch über XLSX arbeiten und wieder zurückführen kann (manuelle 3rd Party Integration über Excel) ⚠️ Archi Patron sowie Excel Voraussetzung
- Archi Modell Import in Jira als Issue um es auch in der Freeedition als "Assetlight" verwenden zu können. 

---

### Methodik

- Reduziertes **TOGAF ADM** als Leitplanke für Entwicklung und Arbeitsmodell
- **ArchiMate 3.2** als bevorzugte Ausdrucksweise für Enterprise Architecture
- **BPMN 2.0** als bevorzugte Ausdrucksweise für Prozesse
- Beide Notationen strikt nach Standard — maximale Tool-Agnostik

---

### Was noch geplant ist

- Filterlogiken vereinfachen (Usability verbessern)
- Asset Lookup im Netzwerk über Python Scripting und anschließendes Archimate Modell über CSV
- Camunda 7 Community Edition (Version noch nicht klar) für Prozessautomatisierung in den Blueprint integrieren. 

---

## 🛠️ Tech Stack

| Tool | Rolle |
|------|-------|
| [Archi 5.8](https://www.archimatetool.com/) — [Den Entwickler unterstützen ❤️](https://www.archimatetool.com/donate/) | EA Modellierung · Master-ID-System · CSV-Schnittstelle |
| [Camunda Modeler (Camunda 7)](https://camunda.com/download/modeler/) | BPMN 2.0 Prozessmodellierung |
| [Python 3](https://www.python.org/) | Automatisierung · Script Flows · Datenverarbeitung |
| [Notepad++](https://notepad-plus-plus.org/) | Konfiguration & Script-Bearbeitung |
| [Claude (claude.ai)](https://claude.ai/) | KI-gestützte Entwicklung von Anthropic |

---

## 🤖 KI-gestützte Entwicklung

Dieses Projekt wurde nach dem Prinzip des **AI-Driven Development** umgesetzt.

Der gesamte Code wurde mit **Claude (claude.ai) von Anthropic** erarbeitet — geführt von jemandem ohne klassisches Coding-Hintergrundwissen, dafür mit tiefer Expertise in Enterprise Architecture, Prozessmodellierung und komplexen organisatorischen Fragestellungen.

> **~320 Stunden** Lernen, Entwickeln und Methoden verfeinern
> **~€ 550** persönlicher Invest
> **1 Person. Freizeit. Echte Überzeugung.**

Die AI-Driven Development Methodik ist als Teil des R+MUNI Blueprints dokumentiert (`AI_DRIVEN_DEV_METHODE.txt`).

---

## 📄 Lizenz

Dieses Projekt ist Open Source und kostenlos nutzbar. Keine Abos. Keine versteckten Kosten. Kein Haken.

---

*R+MUNI — entwickelt von [EUMAXL](https://github.com/EUMAXL) · Österreich*

---

## 🇬🇧 English

R+MUNI is my personal project — built in my free time, driven by genuine interest and real conviction.

Yes, at its core it's a handful of scripts that do things. But to me, it's so much more than that.

R+MUNI is a perspective: to create something meaningful that might actually help someone — **no bad conscience, no hidden subscriptions, no catch.**

That's the idea behind R+MUNI. And that's why this solution is **free** — and that is a principle that applies to this blueprint and all its future developments.

**R+MUNI** stands for **Multi Usable Norm Interface** — an XML-based circular system that combines Enterprise Architecture visualization with process modeling. Designed for Austrian SMEs with up to 50 users who want to represent complex topics (IT landscapes, administrative processes, organizational development) holistically using free tools.

---

### What R+MUNI does

- R+MUNI is a working toolset for modelers in SMEs and mid-sized organizations — thanks to its agnostic XML concept it can be repurposed for just about anything (but doesn't have to be 😉)
- The "DONKEY" connects **ArchiMate 3.2** (EA modeling) [opengroup.org](https://www.opengroup.org/) and **BPMN 2.0** [bpmn.org](https://www.bpmn.org/) (process modeling) through a shared XML master-child circular concept
- Uses **Archi 5.8** as the master ID-providing system via CSV interface and OEF export mechanisms
- Automates workflows through a Python-based script runner (`flw00-scriptrunner.py`)
- Stays **tool-agnostic** — strictly based on open standards, no proprietary dependencies
- Exports valid BPMN 2.0 and ArchiMate OEF — directly importable into enterprise tools (e.g. ADONIS/ADOIT by BOC Group)
- Launches Archi HTML Reports and hosts them under their own name (multiple HTML reports at port level)
- 3rd party integration via CSV routines into ArchiMate 3.2 and the master.xml cycle
- Archi XLSX Export – CSV import format so you can work via XLSX and feed it back in (manual 3rd party integration via Excel) ⚠️ Requires Archi Patron and Excel

---

### Methodology

- Reduced **TOGAF ADM** as guiding framework for development and working model
- **ArchiMate 3.2** as the preferred language for Enterprise Architecture
- **BPMN 2.0** as the preferred language for process modeling
- Both notations strictly according to standard — maximum tool-agnosticism

---

### What's planned

- Atlassian Free integration for the ArchiMate world
- Simplifying filter logic (improving usability)