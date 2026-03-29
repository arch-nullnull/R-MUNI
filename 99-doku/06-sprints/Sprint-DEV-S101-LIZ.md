================================================================================
SPRINT-DEV — LIZENZIERUNG R+MUNI BLUEPRINT
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : Sprint-DEV-S101-LIZ
Tag             : #sprint #dev #lizenz #s101 #governance
Datum           : 2026-03-29
Stage           : S101 — AKTIV
Status          : ABGESCHLOSSEN
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt durch  : EUMAXL + Claude (Pair-Session)
================================================================================


================================================================================
1. ZWECK UND KONTEXT
================================================================================

Dieser Sprint dokumentiert die Lizenzentscheidungen für das R+MUNI Blueprint
Ökosystem. Auslöser war die Feststellung dass die bestehende LICENSE Datei
im Code-Repo zwar GPL-3.0 gesetzt hatte, aber keinen Copyright-Header mit
Autorennennung enthielt. Im Zuge der Klärung wurden alle Lizenzfragen für
beide öffentlichen Repositories vollständig geklärt und umgesetzt.

Geltungsbereich:
  R-MUNI              Code-Repository (public)
  R-MUNI-Doku-public  Dokumentations-Repository (public)

Nicht betroffen:
  Kunden-Repos        Lizenzierung liegt beim jeweiligen Kunden
  DEV-Repo (privat)   Kein öffentlicher Zugriff — keine Lizenzpflicht


================================================================================
2. AUSGANGSLAGE
================================================================================

  - LICENSE Datei in R-MUNI vorhanden — GPL-3.0 Standard-Template
  - Copyright-Header fehlte — kein Autorenname, kein Projektname eingetragen
  - R-MUNI-Doku-public hatte keine LICENSE Datei
  - README.md enthielt veraltete Versionsangaben (OpenJDK 11+, Python 3.9+)
  - Footer README: "entwickelt von EUMAXL" — kein realer Name
  - Stage-Angabe README: "Stage 8 — Beta 1.0" — nicht mehr aktuell


================================================================================
3. ENTSCHEIDUNGEN UND BEGRÜNDUNGEN
================================================================================

--------------------------------------------------------------------------------
3.1 Lizenzwahl Code-Repository — GPL-3.0 bestätigt
--------------------------------------------------------------------------------
Entscheidung:
  GPL-3.0 bleibt die Lizenz für R-MUNI (Code, Scripts, Blueprint).

Begründung:
  - Passt zur Philosophie: alles offen, Quellcode sowieso public
  - Copyleft-Prinzip: wer R+MUNI weiterentwickelt und weitergibt muss
    ebenfalls offenlegen — Offenheit bleibt in der Kette erhalten
  - Dienstleistungsmodell ist kompatibel: GPL erlaubt kommerzielle
    Dienstleistung rund um die Software — nur die Software selbst
    muss offen bleiben
  - Haftungsausschluss (GPL §15/16) gilt unabhängig von Beta/Release-Status

Bewusst nicht gewählt:
  MIT — zu permissiv, würde kommerzielle Closed-Source-Nutzung erlauben
  AGPL — zu restriktiv für den aktuellen Use Case
  Business Source License — widerspricht der Offenheits-Philosophie

--------------------------------------------------------------------------------
3.2 Copyright-Header — Markus Resel
--------------------------------------------------------------------------------
Entscheidung:
  Copyright-Header in LICENSE (R-MUNI) ergänzt:

    R+MUNI Blueprint — Reusable Standards-Based Communication
    and Integration Framework
    Copyright (C) 2026  Markus Resel

Begründung:
  - Realer Name statt Kürzel (EUMAXL) für rechtliche Eindeutigkeit
  - EUMAXL ist ein internes Arbeitskürzel — kein juristisch verwertbarer Name
  - R+MUNI steht für "Resel's Multi Usable Norm Interface" —
    Markus Resel ist der namentliche Urheber

--------------------------------------------------------------------------------
3.3 Lizenzwahl Dokumentations-Repository — CC BY 4.0
--------------------------------------------------------------------------------
Entscheidung:
  R-MUNI-Doku-public erhält eine eigene LICENSE Datei mit CC BY 4.0.

Begründung:
  - Creative Commons ist die passende Lizenzfamilie für Dokumentation,
    Anleitungen und konzeptuelle Inhalte — nicht GPL (die für Code gemacht ist)
  - CC BY 4.0 = maximal offen: lesen, nutzen, verändern, weitergeben,
    auch kommerziell — einzige Pflicht ist Namensnennung
  - Bewusste Entscheidung für totale Offenheit: KI-Training, Weiterentwicklung,
    Übersetzung, kommerzielle Nutzung — alles erlaubt
  - Konsequente Umsetzung der R+MUNI Philosophie: "Das höchste Prädikat
    wäre wenn jemand die Idee weiterentwickelt oder einfach benutzt"

Bewusst nicht gewählt:
  CC BY-SA 4.0 — Copyleft für Doku nicht notwendig, da Offenheit Grundsatz ist
  CC BY-NC 4.0 — Non-Commercial würde KI-Training und freie Nutzung einschränken,
                 widerspricht der Philosophie

--------------------------------------------------------------------------------
3.4 README-Korrekturen
--------------------------------------------------------------------------------
Entscheidung:
  Folgende Anpassungen in README.md (R-MUNI):

  | Feld          | Vorher              | Nachher                        |
  |---------------|---------------------|--------------------------------|
  | Python        | 3.9+                | 3.x                            |
  | OpenJDK       | 11+                 | 21                             |
  | Stage-Angabe  | Stage 8 — Beta 1.0  | Beta 1.0 — Phase 1.xx          |
  | Footer        | entwickelt von EUMAXL | entwickelt von Markus Resel (EUMAXL) |

  Unverändert:
  - Git-Zeile: "Technischer Unterbau — Bash & VS Code Integration für Claude"
    → bewusst so belassen, Beschreibung ist inhaltlich korrekt

Begründung:
  - Versionsangaben waren nicht mehr synchron mit Install.txt
  - Footer-Name konsistent mit Copyright-Header
  - Stage-Angabe spiegelt aktuellen Stand (Phase 1.xx) korrekt wider


================================================================================
4. UMGESETZTE ARTEFAKTE
================================================================================

  ✅ LICENSE (R-MUNI)
       Copyright-Header ergänzt — Markus Resel, 2026
       Ablage: R-MUNI\ (Root)

  ✅ LICENSE (R-MUNI-Doku-public)
       Neu erstellt — CC BY 4.0
       Copyright: Markus Resel, 2026
       Ablage: R-MUNI-Doku-public\ (Root)

  ✅ README.md (R-MUNI)
       Versionsangaben korrigiert, Stage-Angabe aktualisiert, Footer angepasst
       Ablage: R-MUNI\ (Root)


================================================================================
5. ERKENNTNISSE
================================================================================

Lizenz-Grundsatz für R+MUNI:
  Code          →  GPL-3.0   Copyleft, Offenheit bleibt in der Kette
  Dokumentation →  CC BY 4.0 Maximal offen, nur Namensnennung Pflicht

Wichtige Differenzierung:
  GPL-3.0 schließt Haftung explizit aus (§15/16) — unabhängig von
  Beta- oder Release-Status. "Beta" ist kein rechtlicher Begriff,
  kein zusätzlicher Haftungsschutz und keine Lizenzvoraussetzung.

Namensnennung:
  EUMAXL ist ein internes Kürzel. Für alle öffentlichen Rechtsdokumente
  (LICENSE, Copyright-Header) gilt: Markus Resel.
  EUMAXL kann als Klammer weiterhin verwendet werden (z.B. Footer README).

GitHub Standard-Template:
  GitHub legt bei Lizenzwahl "GPL-3.0" nur den reinen Lizenztext an —
  ohne Projektname und Autorenname. Diese müssen manuell ergänzt werden.
  Das ist kein Fehler von GitHub, sondern erwartetes Verhalten.

Transferierbarkeit:
  Dieses Lizenzmodell (GPL für Code, CC BY für Doku) ist ein etabliertes
  Open-Source-Muster und direkt auf andere Projekte übertragbar.


================================================================================
6. GOV-CHECK
================================================================================

  GOV 10.3  Auslöser: Strukturbereinigung + rechtliche Klarheit          ✅
  GOV 10.5  Fachlicher Mehrwert: Rechtssicherheit, Urheberschaft klar    ✅
  GOV 10.6  Ziel war explizit: Lizenz vollständig und korrekt aufsetzen  ✅
  GOV 10.7  Zwischenschritte dokumentiert (diese Sprint-Doku)            ✅
  GOV 10.8  Dev-Doku erstellt                                            ✅
  Rückkopplungsschutz: keine Scripts, keine Logik berührt                ✅
  Rollentrennung GOV 13: keine externen Inhalte transferiert             ✅


================================================================================
BEZÜGE
================================================================================

[[Global_GOV_S8]]                    Normative Grundlage
[[FREEZE_8]]                         Ausgangszustand Phase 1.xx
[[STAGE100_ZIELE_S100]]              Phase-Rahmen 1.xx
[[README]] (R-MUNI)                  Angepasstes Artefakt
[[LICENSE]] (R-MUNI)                 Angepasstes Artefakt
[[LICENSE]] (R-MUNI-Doku-public)     Neues Artefakt


================================================================================
ENDE | Sprint-DEV-S101-LIZ | 2026-03-29
R+MUNI Blueprint | Stage 101 — Phase 1.xx | Erstellt: EUMAXL + Claude (Pair-Session)
================================================================================
