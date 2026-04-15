# STG03 — Template_context

#S102 #player/USER #zone/library

**Cost:** 0 | **Color:** Weiß | **Type:** Artifact

---

## Hinweis

Dieses File ist der Kontext-Anker für die KI.
Es wird zu Sessionbeginn mitgeladen — in der Projektfolder-Variante zusammen mit den anderen STG Files, in der Chat-Variante als einziges File direkt in den Prompt.

Es wächst mit dem Projekt mit. Neue Sprints, Entscheidungen und Erkenntnisse werden hier eingetragen.

Die KI liest es — der USER pflegt es.

---

## Das Projekt

**Name:** <Projektname>
**Typ:** <Verein | Buch | Privates Projekt | Unternehmen | ...>
**Stage:** #S102
**Horizont:** <Wie lange läuft das Projekt? Gibt es eine Exit-Bedingung?>

**In einem Satz:**
<Was ist das Projekt — worum geht es wirklich?>

---

## Die Welt

Dieses Projekt arbeitet mit dem **R+MUNI CARD-System**.

Begriffe die die KI kennen muss:

| Begriff | Bedeutung |
|---|---|
| **Deck** | Aktueller Projektzustand |
| **Karte** | Ein Dokument, eine Entscheidung, ein Vorhaben |
| **Mana** | Ressourcen — menschlich und/oder finanziell |
| **Land** | Personen / Supporter — liefern Mana |
| **Creature** | Lokation — Keller, Halle, Grundstück etc. |
| **Artifact** | Ressource — frei einsetzbar, standalone oder in Abhängigkeit |
| **Instant** | Einmalige Aktion — Bewerb, Event |
| **Enchantment** | Dauerhafte Aktion — Training, Mähen, laufende Aktivitäten |

Arbeitsprinzip:
- USER beschreibt frei — KI strukturiert auf Abruf
- Trigger **„du bist"** = KI gibt jetzt Struktur
- Output immer als `.md` File im Karten-Format
- Entscheidungen trifft immer der USER

---

## Ressourcen — Land

| # | Land | Beschreibung | Status |
|---|---|---|---|
| L1 | <Name/Rolle> | <Was liefert diese Ressource?> | <aktiv / knapp / bewusst reduziert> |

---

## Was läuft — aktive Karten

| Karte | Type | Status | Anmerkung |
|---|---|---|---|
| <Kartenname> | Creature / Spell | ✅ aktiv | <kurze Anmerkung> |

---

## Was schläft — Schlummer-Karten

| Karte | Was sie könnte | Was fehlt |
|---|---|---|
| <Kartenname> | <Potenzial> | <Blockade> |

---

## Sprints & Entscheidungen — was es schon gibt

> Dieser Abschnitt wächst mit. Neue Erkenntnisse hier eintragen.

| Stage | Was wurde entschieden / erarbeitet | Ergebnis |
|---|---|---|
| S102 | <Beschreibung> | <Ergebnis oder offen> |

---

## Offene Punkte

> Was liegt gerade auf dem Stack — was ist noch nicht gespielt?

- <Offener Punkt 1>
- <Offener Punkt 2>

---

## Hinweis für die KI

Du hast jetzt den vollständigen Kontext dieses Projekts.

Deine Aufgabe:
- Verweise gezielt auf bestehende Karten statt alles neu zu erklären
- Frage nach wenn etwas unklar ist — rate nicht
- Gib Struktur erst wenn der USER den Trigger „du bist" verwendet
- Output immer im Karten-Format — Template liegt als `TMP00-Template_card_S102.md`

Bestätige dass du den Kontext geladen hast mit: **READY**

---

**Damage:** KI kann sofort arbeiten ohne mündliche Erklärung | **Life:** Hoch — wächst mit dem Projekt
