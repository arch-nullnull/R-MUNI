================================================================================
BETA_OFFBOARDING — PRINCIPLES (DEV)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : BETA_OFFBOARDING_principles_DEV_S101
Tag             : #dev #principles #beta #offboarding #s101
Datum           : 2026-03-31
Stage           : S1.01 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
================================================================================


1. ZWECK UND DESIGNPHILOSOPHIE
--------------------------------------------------------------------------------
Dieses Dokument beschreibt die Leitprinzipien für das geordnete Offboarding
von Beta-Kunden aus dem R+MUNI Beta-Betrieb.

Offboarding ist kein Versagen — es ist ein definierter Prozessschritt.
Jedes Beta-Verhältnis endet. Die Frage ist nicht ob, sondern wie sauber.

Das Offboarding-Prinzip gilt für alle Beta-Kunden-Verhältnisse —
unabhängig vom Auslöser und unabhängig davon welche Toolbaukasten-Tier-Stufe
beim Beta-Kunden eingerichtet war.

Erstanwendung: Betakunde_01 — Stage 7, Sprint-DEV-S7-BKO1-Offboarding.


2. GRUNDSÄTZE
--------------------------------------------------------------------------------

2.1 Kein stilles Auslaufen
---------------------------
Ein Beta-Verhältnis gilt erst dann als beendet wenn es intern explizit
als beendet dokumentiert ist. Ein faktisch inaktiver Kunde ist kein
offgeboarded Kunde.

  Aktiver Status ohne Nutzung       ≠  Offboarding
  Interner Entscheid + Dokumentation =  Offboarding

2.2 Stiller interner Abschluss ist GOV-konform
------------------------------------------------
Offboarding erfordert keine externe Kommunikation an den Beta-Kunden
wenn der vollständige Kommunikationsweg bereits durchlaufen wurde.

  Vollständiger Kommunikationsweg =
    persönliches Gespräch → Onboarding-E-Mail → Reminder

  Interner Abschluss ohne weiteres Kommunizieren ist in diesem Fall
  die richtige und GOV-konforme Entscheidung.

2.3 R+MUNI deaktiviert was R+MUNI eingerichtet hat
----------------------------------------------------
Beim Offboarding werden alle Zugänge und Syncs deaktiviert die
R+MUNI im Rahmen des Beta-Betriebs für den Kunden eingerichtet hat.
Was beim Kunden verbleibt ist alles was auf seiner Seite liegt —
Tools, Modelle, Daten, Artefakte.

  R+MUNI-seitig eingerichtet   →  wird deaktiviert
  Kundenseitig vorhanden       →  verbleibt beim Kunden

Auf expliziten Kundenwunsch wird auch kundenseitig gelöscht.
Ohne diesen Wunsch gilt: der Kunde behält seine Artefakte und
bleibt handlungsfähig. Das ist der Exitpoint-Gedanke —
R+MUNI baut keine Abhängigkeit, es baut Kompetenz.

2.4 Umfang richtet sich nach der eingerichteten Tier-Stufe
-----------------------------------------------------------
Was beim Offboarding deaktiviert wird hängt davon ab welche
Toolbaukasten-Tier-Stufe beim Beta-Kunden eingerichtet war.

  MINIMAL    →  wenige oder keine R+MUNI-seitigen Zugänge
  DEFAULT    →  GitHub Sync, ggf. weitere Kollaborations-Zugänge
  ADDON      →  zusätzliche Zugänge je nach aktiviertem Addon
               (z.B. kollaborative Plattform, Portal, externe Sync-Tools)

Die konkrete Checkliste ergibt sich aus der Onboarding-Dokumentation
des Beta-Kunden — was eingerichtet wurde ist dort festgehalten.

Bezug: [[TOOLBAUKASTEN_principles_S6]]

2.5 DEV-Umgebung ist vom Offboarding vollständig getrennt
----------------------------------------------------------
Das Offboarding berührt ausschließlich den Beta-Kunden-Kontext.
Die eigene DEV-Umgebung, Scripts, Konfiguration und Blueprint-Logik
sind kein Gegenstand des Offboardings.

  Beta-Kunden-Zugänge    →  werden deaktiviert (Offboarding-Scope)
  DEV-Umgebung           →  bleibt unberührt (außerhalb Scope)
  Blueprint-Logik        →  read-only, kein Eingriff (GOV Rückkopplungsschutz)

2.6 Erkenntnisse sind blueprint-relevant — keine Kundenbewertung
-----------------------------------------------------------------
Die Lessons Learned sind sachlich und blueprint-relevant.
Sie beschreiben was strukturell funktioniert hat, was gefehlt hat
und was beim nächsten Beta-Kunden anders gemacht wird.

Keine Bewertung der Organisation oder Personen des Beta-Kunden.
Diese Grenze ist absolut.

  Zulässig:   "Adoption-Barrier fehlte im Onboarding-Prozess"
  Unzulässig: "Kunde war nicht engagiert genug"

2.7 Offboarding ist ein wiederholbares Blueprint-Artefakt
----------------------------------------------------------
Das Offboarding wird nicht nur durchgeführt — es wird als
reproduzierbares Artefakt dokumentiert. Jeder folgende Beta-Kunde
soll anhand dieses Artefakts offgeboard werden können — ohne
individuelle Anpassung, ohne mündliche Übergabe.


3. SCOPE DES OFFBOARDINGS
--------------------------------------------------------------------------------

Was Offboarding umfasst:
  - Alle R+MUNI-seitig eingerichteten Zugänge und Syncs deaktivieren
    (Umfang gemäß eingerichteter Tier-Stufe und Onboarding-Dokumentation)
  - Internen Beta-Status des Kunden als OFFBOARDED dokumentieren
  - Lessons Learned sachlich erfassen
  - Sprint-DEV-Doku als Abschluss-Artefakt erstellen

Was Offboarding explizit nicht umfasst:
  - Eingriff in DEV-Umgebung oder Blueprint-Logik
  - Externe Kommunikation wenn Kommunikationsweg vollständig durchlaufen
  - Bewertung der Organisation oder Personen des Beta-Kunden
  - Kundenseitige Löschung ohne expliziten Kundenwunsch
  - Änderung von GOV-Regeln oder Stage-Zielen
  - Entscheidungen über zukünftige Beta-Kunden (separater Prozess)


4. AUSLÖSER FÜR OFFBOARDING
--------------------------------------------------------------------------------

  A — Fehlende Adoption
      Beta-Kunde hat nach vollständigem Kommunikationsweg keine aktive
      Nutzung gezeigt. Keine Reaktion auf Reminder.
      → Stiller interner Abschluss ist korrekte Maßnahme.

  B — Abschluss Beta-Phase
      Beta-Verhältnis war zeitlich oder inhaltlich begrenzt und
      hat sein definiertes Ziel erreicht.
      → Abschluss mit Lessons Learned.

  C — Übergang zu neuem Modell
      Beta-Kunde wird in ein neues Onboarding-Modell überführt.
      → Offboarding der Beta-Rolle, kein Abbruch der Beziehung.

  D — Organisationale Entscheidung Kundenseite
      Beta-Kunde beendet selbst aktiv die Zusammenarbeit.
      → Offboarding bestätigt und dokumentiert was faktisch bereits gilt.

Auslöser Betakunde_01: A — Fehlende Adoption.


5. ZUSAMMENHANG MIT ONBOARDING
--------------------------------------------------------------------------------
Offboarding und Onboarding sind gegenläufige Prozesse desselben
Beta-Kunden-Lebenszyklus.

  ONBOARDING    →  Zugänge einrichten, Tier festlegen, Kommunikation starten
  BETA-BETRIEB  →  Nutzung, Feedback, Iterationen
  OFFBOARDING   →  R+MUNI-Zugänge deaktivieren, Status dokumentieren, Lernen

Die Onboarding-Dokumentation ist die Grundlage für das Offboarding —
sie enthält was eingerichtet wurde und muss daher vollständig sein.

Erkenntnisse aus dem Offboarding fließen direkt in das
Onboarding-Design des nächsten Beta-Kunden.

Bezug: [[BETA_ONBOARDING_Atlassian_Zugriffsmodell]]


6. GOVERNANCE-BEZÜGE
--------------------------------------------------------------------------------
GOV 10.3   Auslöser-Typ: Kundenbedarf / Strukturbereinigung
GOV 10.5   Fachlicher Mehrwert: saubere Trennung, Exitpoint-Integrität,
           reproduzierbares Artefakt, Lessons Learned als Input
GOV 10.6   Ziel explizit: Beta-Kunde vollständig und dokumentiert offboarden
GOV 10.7   Zwischenschritte: Tier-Check, Zugänge, Status, Lessons Learned
GOV 10.8   Dev-Doku verpflichtend für jeden Offboarding-Sprint
Rückkopplungsschutz: Offboarding berührt keine Blueprint-Logik, keine Scripts


7. SONDERFÄLLE — KONTEXTUELLE ANPASSUNG
--------------------------------------------------------------------------------

7.1 Persönliche oder organisationale Nähe zum Beta-Kunden
----------------------------------------------------------
Wenn der Beta-Kunde in einem persönlichen oder beruflichen Nahverhältnis
zum Betreiber steht gelten folgende Anpassungen:

  Was unverändert gilt:
    - Lessons Learned werden sachlich erfasst
    - Phasentrennung wird dokumentiert (Beta-Phase endet explizit)
    - Interner Status wird auf OFFBOARDED gesetzt

  Was angepasst werden kann:
    - Kommunikationsweg und -ton dem persönlichen Verhältnis angepasst
    - Deaktivierung von Zugängen kann bilateral anders gehandhabt werden
    - Kein formaler Abschlussbrief wenn persönliches Gespräch ausreicht

  Was nicht aufgehoben wird:
    - Grenze zur Kundenbewertung in den Lessons Learned gilt absolut
    - Interner Entscheid und Dokumentation sind verpflichtend
    - Beta-Phase gilt als beendet — unabhängig vom weiteren Verhältnis

Erstanwendung dieses Sonderfalls: Betakunde_01 — Stage 7.


================================================================================
BEZÜGE
================================================================================
[[Global_GOV_DEV_S101]]                          normative Grundlage
[[TOOLBAUKASTEN_principles_S6]]                  Tier-Struktur MINIMAL/DEFAULT/ADDON
[[INST_principles_S5]]                           Baum-Modell, Exitpoint-Logik
[[BETA_ONBOARDING_Atlassian_Zugriffsmodell]]     Onboarding-Gegenstück
[[FREEZE-6_konsolidiert]]                        Ausgangszustand — Status Betakunde_01
[[STAGE7_ZIELE_S7]]                              S7-Z1 Betakunde_01 Offboarding


================================================================================
BETA_OFFBOARDING_principles_DEV | S1.01 | 2026-03-31 | R+MUNI Blueprint
================================================================================
