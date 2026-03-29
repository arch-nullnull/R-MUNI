# R+MUNI Blueprint

> *Eine Vorgehensweise, viele Werkzeuge. Eine Philosophie. Gebaut für die, die wirklich visuell abbilden wollen wie ihre Organisation funktioniert.*

---

## Was ist R+MUNI?

Es ist mein persönliches Projekt — entstanden in meiner Freizeit, aus echtem Interesse und mit echter Überzeugung.

Ja, im Kern sind es eine Vorgehensweise, ein paar Open-Source-Tools und Python-Scripts die irgendwas machen. Aber für mich ist es weit mehr als das — und wer sich die Zeit nimmt, es zu durchschauen, wird es für sich vielleicht auch entdecken...

R+MUNI ist eine Perspektive: etwas **sinnstiftendes** zu schaffen, das vielleicht wirklich jemandem helfen kann — **ohne schlechtes Gewissen, ohne versteckte Abo-Fallen, ohne Hintertüren.**

Das ist die Idee hinter R+MUNI. Und deshalb ist diese Lösung **kostenlos** — und das ist ein Prinzip, das für diesen Blueprint und alle seine Weiterentwicklungen gilt.

**R+MUNI** steht unter anderem 😉 für **Multi Usable Norm Interface** — ein XML-basiertes Kreislaufsystem, das Enterprise Architecture Visualisierung mit Prozessmodellierung vereint.

Entwickelt für österreichische KMU, die komplexe Fragestellungen (IT-Landschaften, Verwaltungsprozesse, Unternehmensentwicklung uvm.) mit freien Tools ganzheitlich darstellen wollen — mit klaren Grenzen.

Es verbindet vier Dinge, die in kleinen und mittleren Organisationen oft getrennt oder nur in den Köpfen einzelner existieren:

- **Visualisierung** — ArchiMate 3.2, BPMN 2.0, SVG für alles dazwischen | *Das Bild*
- **Strukturierung** — Tagging, Mapping, Review-Logiken ohne Overhead | *Die Ordnung*
- **Automatisierung** — maschinenlesbare Prozesse, Scriptrunner & mehr 😉 | *Der erste Schritt*
- **Integration** — offen und transparent, nach individueller Anpassung der Scripts und Logiken in 3rd-Party-Welten | *Die Anschlussfähigkeit*

R+MUNI ist dabei die *Single Source of Truth* — alles andere wird daraus abgeleitet. Keine parallelen Wahrheiten, keine manuelle Synchronisation, fast 😉 kein Chaos.

---

## Die Philosophie dahinter

R+MUNI ist kein Produkt. Es ist eine **Vorgehensweise** nach offenen Normen, mit einer Open-Source-Toollandschaft als **Werkzeugkasten** — der dann auf einen Script-**Baukasten** für die Interaktion unter den Werkzeugen aufbaut.

Jeder Baustein hat seine klare Aufgabe. Jede Reihe hat einen klaren Zweck. Jede Erweiterung baut auf dem auf, was vorher stabil war — und verändert es nicht.

Das klingt nach Engineering. Es ist aber vor allem **Haltung**:
Dinge sollen funktionieren. Dauerhaft. Nachvollziehbar. Ohne versteckte Abhängigkeiten.

Der "Esel" ist und bleibt **kostenlos für Endanwender**. Das ist kein Zufall — das ist Grundsatz.
Archi ist kostenlos. Die Scripts sind kostenlos.
Wer R+MUNI nutzt, bekommt kein verstecktes Abo und keinen Lock-in.

---

## Der Toolbaukasten — welche Tools brauchst du?

R+MUNI setzt ausschließlich auf frei verfügbare, stabile Open-Source-Werkzeuge. Der gesamte Kern-Stack kostet nichts — das ist kein Zufall, sondern Grundsatz.

![Toolbaukasten Übersicht](99-doku/07-creative/images/svg%20claude/toolbaukasten.svg)

> [[toolbaukasten.svg]]

| Tool | Zweck | Link |
|---|---|---|
| **Archi 5.8** | Enterprise Architecture — die Single Source of Truth | [archimatetool.com](https://www.archimatetool.com/) |
| **Camunda Modeler** | BPMN 2.0 Prozessmodellierung | [camunda.com/download/modeler](https://camunda.com/download/modeler/) |
| **Python 3.x** | Automatisierung der Script-Reihen | [python.org](https://www.python.org/) |
| **jArchi 1.11.0** | JavaScript Scripting-Plugin für Archi | [github.com/archimatetool/archi-scripting-plugin](https://github.com/archimatetool/archi-scripting-plugin) |
| **OpenJDK 21** | Java-Runtime (Voraussetzung für Archi & Camunda) | [adoptium.net](https://adoptium.net/) |
| **Notepad++** | Editor für alle Dateitypen (XML, CSV, CFG, MD) | [notepad-plus-plus.org](https://notepad-plus-plus.org/) |
| **Git** | Technischer Unterbau — Bash & VS Code Integration für Claude | [git-scm.com](https://git-scm.com/) |
| **GitHub** | Repository-Verwaltung, Backup, Sync | [github.com](https://github.com/) |
| **Obsidian** | Markdown-Dokumentation, Vault-Navigation | [obsidian.md](https://obsidian.md/) |
| **draw.io** | Rein visuelle Diagramme (kein ArchiMate/BPMN) | [drawio.com](https://www.drawio.com/) |
| **Inkscape** | SVG-Nachbearbeitung | [inkscape.org](https://inkscape.org/) |
| **PowerShell 7** | Batch-Automation, Python-Orchestrierung | [github.com/PowerShell/PowerShell](https://github.com/PowerShell/PowerShell) |
| **KeePass** | Credential-Verwaltung | [keepass.info](https://keepass.info/) |
| **Claude** | Bevorzugte KI-Lösung — Pair-Partner für Entwicklung, Dokumentation und Debugging | [claude.ai](https://claude.ai/) |

**Summe: 0 EUR**

> Archi ist das Herz von R+MUNI. Das Team stellt es kostenlos zur Verfügung — wer Mehrwert sieht, kann als Patron unterstützen: [archimatetool.com/donate](https://www.archimatetool.com/donate/)

---

## Der Script-Baukasten — wie funktioniert die Automatisierung?

R+MUNI automatisiert Datenflüsse zwischen den Tools über Python-Scripts. Das Prinzip dahinter ist bewusst einfach:

> *1 Script = 1 Aufgabe.*

Kein Script macht zwei Dinge gleichzeitig. Kein Flow enthält versteckte Logik. Was ein Script tut, ist aus seinem Namen und seinem Log unmittelbar nachvollziehbar.

### Wie ein Flow funktioniert

Ein **Flow** beschreibt *was* passiert. Die **Scripts** implementieren *wie* es passiert.


### Die Script-Reihen

R+MUNI organisiert seine Scripts in klar abgegrenzte **Reihen**. Jede Reihe hat einen festen Kürzel-Präfix:

| Reihe | Kürzel | Zweck |
|---|---|---|
| **HLP** | `HLP` | Hilfsfunktionen — Basis für alle anderen Reihen (Root-Auflösung, Backup, Server) |
| **CSV** | `CSV` | Kern-Datenverarbeitung — vom Archi-Export bis zum fertigen Import-Artefakt |
| **XML** | `XML` | XML-Verarbeitung und Master-XML-Pflege |
| **M2B** | `M2B` | Master → BPMN — erstellt aus dem Modell heraus BPMN-Prozesshüllen |
| **ATL** | `ATL` | Atlassian-Integration — Confluence und Jira aus dem Modell heraus |
| **CLE** | `CLE` | Cleaning und Quality Gate — sauber rein, sauber raus |
| **ECM** | `ECM` | EasyCSVMapper — externe CSV-Quellen in ArchiMate importieren |
| **FLW** | `FLW` | Flow-Orchestrierung — der Scriptrunner selbst |

Die vollständige Dokumentation aller Reihen — Principles, How2 und Detailbeschreibungen — findest du in der DEV-Dokumentation:
[https://github.com/arch-nullnull/R-MUNI/blob/main/99-doku/README.md](99-doku/README.MD)

### Was du als Associate wissen musst

Als Associate arbeitest du mit R+MUNI — du entwickelst es nicht. Das bedeutet in der Praxis:

**Du konfigurierst einmalig** die `root.cfg` — eine einzige Datei, ein einziger Eintrag:
```
rootfolder=C:\Prototyping\R+MUNI <KUERZEL>
```
Alle Pfade leiten sich automatisch daraus ab. Danach greifst du diese Datei nur an wenn sich dein Basisverzeichnis ändert.

**Du startest Scripts** über den Scriptrunner (`FLW00-scriptrunner.py`) oder direkt über PowerShell.

**Du liest `.txt`-Artefakte** (z.B. `run-scope.txt`, `model-scope.txt`) wenn du den aktuellen Workflow-Stand prüfen möchtest — diese sind bewusst menschenlesbar.

**Du öffnest `.log`-Dateien** (in `02-stages\99-logs\`) nur wenn etwas schiefgelaufen ist — sie sind technische Debug-Ausgaben, kein normaler Workflow-Bestandteil.

---

## Ordnerstruktur — der rote Faden

R+MUNI folgt einer fixen Ordnerstruktur, die einmalig durch `Dir_Setup.bat` angelegt wird. Die **bindende Referenz** für alle Details ist `HLP99`.

Innerhalb von `R+MUNI <KUERZEL>\` gilt:

```
  root.cfg        ← einzige Konfiguration (einmalig anpassen)
  00-model\       ← Archi-Modell (read-only für Scripts)
  01-artifacts\   ← alle abgeleiteten Artefakte
  02-stages\      ← Laufzeit-Artefakte und Logs
```

> Konfiguration läuft ausschließlich über `root.cfg` — eine Datei, ein Ort, keine Ausnahmen.

---

## Wer arbeitet mit R+MUNI? — Drei Rollen, drei Welten

R+MUNI unterscheidet bewusst zwischen drei Rollen — keine Hierarchie, sondern Kontexttrennung.

**Expert** kennt das System von innen. Er arbeitet mit ArchiMate, versteht den Datenfluss, baut Script-Reihen auf und erweitert sie. Vollständige Principles und How2-Dokumente liegen in der öffentlichen Dokumentation: [github.com/arch-nullnull/R-MUNI-Doku-public](https://github.com/arch-nullnull/R-MUNI-Doku-public)

**Associate** nutzt R+MUNI im Organisationskontext — modelliert, dokumentiert, führt Flows aus. Die Struktur ist fix, die Konfiguration einmalig. Associate-Templates und How2-Dokumente sind auf diesen Kontext zugeschnitten.

**MGT** ist die lockere Welt — kein Business-Kontext, keine Compliance, keine Governance. Vom Buchprojekt bis zum Vereinslayout. R+MUNI-Methoden funktionieren auch hier, aber ohne formalen Überbau. In Entwicklung (Phase 2).

---

## Mitmachen — als Associate oder als Developer

R+MUNI wird aktiv weiterentwickelt und befindet sich aktuell in **Beta 1.0 — Phase 1.xx**.

**Als Associate** kannst du R+MUNI in deiner Organisation einsetzen, Feedback geben und damit direkt beeinflussen wie das System weiterentwickelt wird. Der Feedback-Weg ist klar geregelt — kein schwarzes Loch, keine leeren Versprechen.

**Als Developer** kannst du auf der Blueprint-Basis aufbauen. Die Dokumentation ist offen, die Prinzipien sind nachvollziehbar, und jede Entscheidung hat einen dokumentierten Grund. R+MUNI ist **AI-driven entwickelt** — der gesamte Entwicklungsprozess mit Claude als Pair-Partner ist dokumentiert und reproduzierbar.

Interesse? Meld dich — über GitHub Issues:
[github.com/arch-nullnull/R-MUNI-Doku-public](https://github.com/arch-nullnull/R-MUNI-Doku-public)

---

## Technologie-Stack

R+MUNI setzt bewusst auf **frei verfügbare, stabile Werkzeuge**.

Den aktuellen Stand — was, wie und wann installiert wird — findest du in der Installationsanleitung:
[[Install.txt]]

Der Grundsatz: **Kein Tool im Kern-Stack kostet Geld.** Ergänzungen sind möglich — aber immer optional, immer transparent. Wer über die reine Nutzung hinausgeht — etwa in Aufbauarbeiten oder erweitertem Betrieb — wird feststellen dass ein vorübergehender Invest in einzelne Bausteine sinnvoll sein kann. Voraussetzung ist er nie.

---

## Dank & Anerkennung

### Die wichtigsten zuerst

Ensi, Andi, Dad, Kimmy, Mara, Peeezzznnn, Shadow, Columbo, Gertschi — ihr wisst warum. 😉

---

### Grafik & visuelle Identität

Die Flipchart-Illustrationen und die initiale visuelle Sprache von R+MUNI wurden inspiriert durch die Arbeit von **Nadine Rossa**, Grafikerin und Illustratorin. Ihre handgezeichnete, klare Bildsprache hat geholfen, komplexe Zusammenhänge sichtbar zu machen. Die initiale Logo-Idee hat dort ihre Inspiration gefunden.

→ [nadine-rossa.de](https://nadine-rossa.de/) | [sketchnote-love.com](https://sketchnote-love.com/)

---

### Archi Team & Freunde

Das ist der Grund, warum ich überhaupt auf die Idee gekommen bin — ich war so fasziniert von Archi 5.8 und seinen Möglichkeiten, und das noch gratis, dass ich begonnen habe, mir ArchiMate 3.2 anzusehen... Dann TOGAF, dann hab ich langsam verstanden was sich da für eine Welt auftut für einen BPMN 2.0 Jünger 😉

In diesem Sinne: bestes Tool der EU — weiter so! Ich persönlich unterstütze als Person sowie mit jedem Kunden, der eine Installation oder Support bei mir bezieht.

→ [archimatetool.com](https://www.archimatetool.com/) | [Spenden & unterstützen](https://www.archimatetool.com/donate/)

Das Team macht das alles hier erst im Kern möglich! Danke — und Support ist kein Mord, also haut raus!! 😄

---

## Ehrlichkeit zuerst — der "Esel" steht noch auf wackeligen Beinen

R+MUNI ist aktuell **echte Beta** — nicht Marketing-Beta.

Das bedeutet: Ab und zu fällt der Esel noch um. Es gibt Ecken die noch rau sind, Dinge die noch nicht rund laufen, und Schritte die noch manuell begleitet werden müssen. Wer jetzt einsteigt, braucht **Geduld** und die Bereitschaft, dran zu bleiben.

Was das konkret heißt:
- Änderungen passieren — dokumentiert, GOV-konform, aber sie passieren
- Ohne Nachverfolgung der aktuellen Stage und Sprints kann es holprig werden
- Manche Schritte brauchen noch manuelle Begleitung

**[Claude.ai](https://claude.ai/)** ist dabei meine verlässliche Stütze im Entwicklungsprozess — als Pair-Partner, Sparringspartner und Fehlersucher. Ohne diese Kombination wäre R+MUNI nicht da wo es heute ist.

Das Ziel ist klar: Aus der Beta wird ein **stabiles, downloadbares Paket** — zum Installieren, Loslegen, Nutzen. Bis dahin: herzlich willkommen im Bauprozess. 🧱

---

*R+MUNI Blueprint — entwickelt von Markus Resel (EUMAXL) | Beta 1.0 — Phase 1.xx | 2026*
