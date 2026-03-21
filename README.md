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

Es verbindet drei Dinge, die in kleinen und mittleren Organisationen oft getrennt oder nur in den Köpfen einzelner existieren:

- **Strukturmodellierung** über ArchiMate 3.2 mit Archi 5.8 | *Das Warum*
- **Prozessabbildung** über BPMN 2.0 mit dem Camunda Modeler | *Das Wie*
- **Offene, freie Dokumentationsplattform & Informationsmapping** | *Die allen zugängliche Information dazu*

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

## Script-Reihen

R+MUNI stellt aktuell folgende Script-Reihen zur Verfügung:

| Reihe | Zweck |
|---|---|
| **HLP** | Hilfsfunktionen — Basis für alles andere (Kopieren, Backup, Server, etc.) |
| **CSV** | Kern-Datenverarbeitung — vom Archi-Export bis zum fertigen Import-Artefakt |
| **XML** | XML-Verarbeitung und Master-XML-Pflege |
| **M2B** | Model-to-Blueprint — Strukturübernahme und Mapping |
| **ATL** | Atlassian-Integration — Confluence und Jira aus dem Modell heraus |
| **CLE** | Cleaning und Quality Gate — sauber rein, sauber raus |
| **ECM** | Enterprise Content Management — Artefakte und IDs |
| **FLW** | Flow-Orchestrierung — Scripts sequenziell ausführen über den Scriptrunner |

Aktuellen Sprint- und Stage-Stand findest du unter:
[github.com/arch-nullnull/R-MUNI-Doku-public](https://github.com/arch-nullnull/R-MUNI-Doku-public)

Jede Reihe hat ihre eigenen **Principles** (wie sie funktioniert) und **How2-Dokumente** (wie man sie bedient).

---

## Baukasten — nicht Monolith

Das Prinzip hinter R+MUNI lässt sich in einem Satz beschreiben:

> *1 Ding = 1 Outcome.*

Kein Baustein macht zwei Dinge. Kein Flow enthält versteckte Logik. Kein Konfigurationsfile liegt an drei Stellen gleichzeitig.

Das macht R+MUNI **wartbar**, **erklärbar** und **reproduzierbar** — auch wenn man sechs Monate nicht hineingeschaut hat.

Die Ordnerstruktur folgt einem klaren Schema:

- `00-model` → das Archi-Modell (read-only für Scripts)
- `01-artifacts` → alle abgeleiteten Artefakte
- `02-stages` → Entwicklungsstände und Logs

Konfiguration läuft ausschließlich über `root.cfg` — eine Datei, ein Ort, keine Ausnahmen.

Filtermöglichkeiten sind granularer und in der jeweiligen Reihe zu finden...

---

## Mitmachen — als Beta-Kunde oder als Developer

R+MUNI wird aktiv weiterentwickelt und befindet sich aktuell in **Stage 6 — Beta Feedback Integration & Blueprint Maturity**.

**Als Beta-Kunde** kannst du R+MUNI in deiner Organisation einsetzen, Feedback geben und damit direkt beeinflussen wie das System weiterentwickelt wird. Der Feedback-Weg ist klar geregelt — kein schwarzes Loch, keine leeren Versprechen.

**Als Developer** kannst du auf der Blueprint-Basis aufbauen. Die Dokumentation ist offen, die Prinzipien sind nachvollziehbar, und jede Entscheidung hat einen dokumentierten Grund. R+MUNI ist **AI-driven entwickelt** — der gesamte Entwicklungsprozess mit Claude als Pair-Partner ist dokumentiert und reproduzierbar.

Interesse? Meld dich — über GitHub Issues oder das Atlassian-Portal:
[ims-blueprint-ticketsystem.atlassian.net/helpcenter/RMNP](https://ims-blueprint-ticketsystem.atlassian.net/helpcenter/RMNP)

---

## Technologie-Stack

R+MUNI setzt bewusst auf **frei verfügbare, stabile Werkzeuge**.

Den aktuellen Stand — was, wie und wann installiert wird — findest du in der Installationsanleitung:
[[Install.txt]]

Der Grundsatz: **Kein Tool im Kern-Stack kostet Geld.** Ergänzungen sind möglich — aber immer optional, immer transparent.

---

## Dank & Anerkennung

### Grafik & visuelle Identität

Die Flipchart-Illustrationen und die initiale visuelle Sprache von R+MUNI wurden inspiriert durch die Arbeit von **Nadine Rossa**, Grafikerin und Illustratorin.

Ihre handgezeichnete, klare Bildsprache hat geholfen, komplexe Zusammenhänge sichtbar zu machen — auf Whiteboards, Flipcharts und in der Kommunikation mit Kunden. Die initiale Logo-Idee hat dort ihre Inspiration gefunden.

Die Grafiken selbst wurden eigenständig erstellt bzw. auf Basis eigener Entwürfe mit KI-Unterstützung weiterentwickelt.

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
- Es gibt noch **kein fertiges Download-Paket** — wer R+MUNI heute nutzt, begleitet die Entwicklung aktiv
- Änderungen passieren — dokumentiert, GOV-konform, aber sie passieren
- Ohne Nachverfolgung der aktuellen Stage und Sprints kann es holprig werden

**[Claude.ai](https://claude.ai/)** ist dabei meine verlässliche Stütze im Entwicklungsprozess — als Pair-Partner, Sparringspartner und Fehlersucher. Ohne diese Kombination wäre R+MUNI nicht da wo es heute ist.

Das Ziel ist klar: Aus der Stage 6 Beta wird ein **stabiles, downloadbares Paket** — zum Installieren, Loslegen, Nutzen. Bis dahin: herzlich willkommen im Bauprozess. 🧱

---

*R+MUNI Blueprint — entwickelt von EUMAXL | Stage 6 aktiv | 2026*
