# R+MUNI Blueprint — Beta 1.0

> Der Esel steht. Noch auf wackeligen Beinen — aber er steht. 🧱

---

## Was ist Beta 1.0?

Beta 1.0 ist der erste öffentlich kommunizierbare Stand von R+MUNI Blueprint.
Kein Marketing-Release. Kein Feature-Freeze-Versprechen. Aber ein sauberer,
dokumentierter Ausgangspunkt — für Associates die einsteigen wollen, und für
Developer die auf der Basis aufbauen wollen.

---

## Was ist drin?

- **Vollständige Blueprint-Struktur** — Ordnerstruktur, root.cfg, Konfigurationslogik
- **Script-Baukasten** — alle aktiven Reihen: CSV, XML, M2B, ATL, CLE, ECM, FLW
- **Scriptrunner** — FLW00-scriptrunner.py als zentraler Einstiegspunkt
- **Mapping-Dateien** — csvmapping.txt und alle zugehörigen .txt-Artefakte
- **Dokumentation** — README, Install.txt
- **Associate-Perspektive** — Terminologie und Rollenkonzept konsequent umgesetzt

---

## Was noch nicht drin ist?

- Associate-Inhalte und DEV-Inhalte sind inhaltlich noch nicht getrennt — kommt in Stage 1
- MGT-Welt ist in Entwicklung — noch nicht enthalten
- Manche Schritte brauchen noch manuelle Begleitung
- Änderungen passieren — dokumentiert, GOV-konform, aber sie passieren

---

## Voraussetzungen

Alle Tools im Stack sind kostenlos und frei verfügbar.
Details und Installationsreihenfolge: siehe `Install.txt` im Repo-Root.

Kern: Archi 5.8 · Camunda Modeler · Python 3.9+ · jArchi 1.11.0 · OpenJDK 11+

---

## Einstieg

```
root.cfg öffnen → rootfolder= auf dein lokales Verzeichnis setzen → fertig.
```

Alles weitere läuft über den Scriptrunner oder direkt über PowerShell.
Vollständige Anleitung: `Install.txt`

---

## Feedback & Kontakt

Fehler, Fragen, Ideen → GitHub Issues in diesem Repo.
Wer jetzt einsteigt hilft direkt mit das System weiterzuentwickeln.

---

*R+MUNI Blueprint — entwickelt von EUMAXL | Stage 8 — Beta 1.0 | 2026*
*AI-driven entwickelt mit Claude als Pair-Partner — [claude.ai](https://claude.ai/)*
