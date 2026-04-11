# R+MUNI Blueprint

> *Eine Vorgehensweise, viele Werkzeuge. Eine Philosophie. Gebaut für die, die wirklich visuell abbilden wollen wie ihre Organisation funktioniert.*

---

## Was ist R+MUNI?

Es ist mein persönliches Projekt — entstanden in meiner Freizeit, aus echtem Interesse und mit echter Überzeugung.

Ja, im Kern sind es 4 Vorgehensweisen, ein paar Open-Source-Tools und Python-Scripts. Aber für mich ist es weit mehr — und wer sich die Zeit nimmt, wird es vielleicht auch entdecken...

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

## Die vier Säulen

R+MUNI ist in vier Säulen aufgebaut — die ersten drei bilden die Basis, aus der sich die vierte von selbst ergibt.

![Die vier Säulen von R+MUNI](__SVG_SAEULEN_PFAD__)

> [[svg_saeulen.svg]]

| Säule | Inhalt | Kern-Tools |
|---|---|---|
| **01 Visuelle Übersicht** | ArchiMate, BPMN, freie Diagramme | Archi 5.8, Camunda Modeler, draw.io, Inkscape |
| **02 Dokumentation & Wissen** | Markdown-Vault, Repo, Principles, How2 | Obsidian, Notepad++, GitHub, Git |
| **03 Struktur & Vorlagen** | Ordnerstruktur, Scripts, Konfiguration, Templates | Python 3, PowerShell 7, Dir_Setup.bat, root.cfg |
| **04 Step 1 — AI-Nutzung** | Wer 01–03 kennt, hat den Kontext für KI. | Sprachmodell + GOV + AI_DRIVEN_DEV als Basis |

**Alle Kernkomponenten: 0 EUR.** Keine versteckten Kosten, keine Pflicht-Abos, kein Lock-in.

Addons (Atlassian, BOC Integration, VS Code) sind optional und werden in [`Install.txt`](Install.txt) beschrieben.

---

## Für wen ist R+MUNI? — Drei Varianten, eine Basis

![R+MUNI Varianten: CARD, R+MUNI, DEV](__SVG_VARIANTEN_PFAD__)

> [[svg_varianten.svg]]

R+MUNI unterscheidet drei Varianten — keine Hierarchie, sondern Kontexttrennung.

**CARD** ist der spielerische Einstieg — minimal, keine Fachbegriffe, kein formaler Überbau. Vom Buchprojekt bis zum Vereinslayout. In Entwicklung (Phase 2).

**R+MUNI** ist die Produktivvariante — reduzierte Norm-Sprache, KMU-tauglich. Modellieren, dokumentieren, Flows ausführen. Struktur fix, Konfiguration einmalig. Associate-Templates sind auf diesen Kontext zugeschnitten.

**DEV** ist das vollständige Blueprint-System — GOV-konform, AI-driven entwickelt, vollständige Principles und How2. Basis für alle Ableitungen und Weiterentwicklungen.

**EXPERT** entsteht bei Bedarf als Extraktion aus DEV — volle Norm-Konformität, on-demand, kein dauerhafter eigener Dokumentationsbereich.

---

## Step 1 — AI-Nutzung

R+MUNI ist **AI-driven entwickelt** — der gesamte Entwicklungsprozess ist dokumentiert und reproduzierbar.

Wer die drei Säulen kennt — Visuelle Übersicht, Dokumentation und Struktur & Vorlagen — hat automatisch den Kontext der für einen produktiven AI-Einsatz notwendig ist.

```
Schritt 1:  GOV-Dokument laden                     → verbindliche Regeln
Schritt 2:  AI_DRIVEN_DEV_METHODE laden            → operative Arbeitsmethode
Schritt 3:  Projektfolder als Kontext bereitstellen → Single Source of Truth
            → Pair-Development starten
```

Die vollständige Methode — Session-Ablauf, Kommunikationsregeln, Drift-Prävention — ist in [`AI_DRIVEN_DEV_METHODE`](00-governance/AI_DRIVEN_DEV_METHODE_DEV_S102.md) dokumentiert.

Welches Sprachmodell eingesetzt wird, ist in [`Install.txt`](Install.txt) Abschnitt 3.8 beschrieben.

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

Die Script-Reihen (HLP, CSV, XML, ECM, NBX, ATL, M2B, FLW, CLE) sind als eigenständige Funktionseinheiten aufgebaut: **1 Script = 1 Aufgabe.** Kein Script macht zwei Dinge gleichzeitig. Was ein Script tut, ist aus seinem Namen und seinem Log unmittelbar nachvollziehbar.

Die vollständige Dokumentation aller Reihen findest du in der DEV-Dokumentation:
[github.com/arch-nullnull/R-MUNI-Doku-public](https://github.com/arch-nullnull/R-MUNI-Doku-public)

---

## Mitmachen — als Associate oder als Developer

R+MUNI wird aktiv weiterentwickelt und befindet sich aktuell in **Beta 1.0 — Phase 1.xx**.

**Als Associate** kannst du R+MUNI in deiner Organisation einsetzen, Feedback geben und damit direkt beeinflussen wie das System weiterentwickelt wird. Der Feedback-Weg ist klar geregelt — kein schwarzes Loch, keine leeren Versprechen.

**Als Developer** kannst du auf der Blueprint-Basis aufbauen. Die Dokumentation ist offen, die Prinzipien sind nachvollziehbar, und jede Entscheidung hat einen dokumentierten Grund. R+MUNI ist **AI-driven entwickelt** — der gesamte Entwicklungsprozess ist dokumentiert und reproduzierbar.

Interesse? Meld dich — über GitHub Issues:
[github.com/arch-nullnull/R-MUNI-Doku-public](https://github.com/arch-nullnull/R-MUNI-Doku-public)

---

## Optionale Leistungen

Das System ist kostenlos — und das bleibt so. Wer bei Einrichtung, Einführung oder laufendem Betrieb Unterstützung möchte, kann das anfragen.

![Optionale Leistungen: Setup, Schulung, Support](__SVG_LEISTUNGEN_PFAD__)

> [[svg_leistungen.svg]]

| Leistung | Inhalt |
|---|---|
| **Setup** | Ersteinrichtung aller Komponenten, Konfiguration, erster Funktionstest |
| **Schulung** | Einführung in ArchiMate, BPMN, R+MUNI Methode und AI-Nutzung |
| **Support** | Laufende Begleitung, Bug-Analyse, Modell-Review, Sprint-Begleitung |

Kein Automatismus — Kapazität und Workload entscheiden. Kontakt über GitHub Issues:
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
