================================================================================
SPRINT-DEV-BACKLOG – IDHandler
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : Sprint-DEV-BACKLOG_IDHandler_S7
Datum           : 2026-03-21
Stage           : S7 – BACKLOG
Status          : BACKLOG — nicht gestartet
Verantwortlich  : EUMAXL (R+MUNI Entwickler)
Jira-Sync       : NEIN — bei Priorisierung nachziehen
================================================================================


================================================================================
1. MOTIVATION UND AUSLÖSER
================================================================================

Auslöser-Typ: Entwicklerwunsch / Strukturbereinigung

Der aktuelle R+MUNI Backend-Flow ist in einem zentralen Punkt von Archi
strukturell abhängig: Element-IDs entstehen ausschließlich durch den
Archi CSV-Import. Das bedeutet, dass jeder Backend-Durchlauf (XML FLOW,
CSV FLOW, ECM-Reihe) an mindestens einem Punkt manuell unterbrochen
werden muss — Archi öffnen, Import durchführen, OEF exportieren —
bevor der Flow weiterlaufen kann.

Diese Unterbrechung ist kein fachliches Erfordernis. Sie ist eine
technische Kopplung. R+MUNI braucht stabile, eindeutige IDs für
Elemente — aber es gibt keinen Grund warum ausgerechnet Archi
diese vergeben muss.

Erkenntnisquelle: HLP08 ID-Merge-Run (zwei Archi-Unterbrechungen pro
ECM-Lauf) sowie ECM03 Reihenfolge-Join als Workaround für fehlende
native ID-Persistenz.

Erkannt in:    Stage 6 / ECM-Sprint + Rosetta Stone FreezeReal Diskussion
Erkannt am:    2026-03-21


================================================================================
2. ZIEL
================================================================================

Ziel:
  Eine zentrale IDHandler-Reihe (IDH) entwickeln die stabile,
  eindeutige Element-IDs eigenständig vergibt und verwaltet —
  sodass Archi-IDs als gleichwertige 3rd-Party-IDs behandelt werden
  können, analog zur bestehenden BPMN-ID-Behandlung im XML FLOW.

Erfolgskriterium:
  Ein vollständiger Backend-Durchlauf (XML FLOW + CSV FLOW oder
  ECM-Reihe) kann ohne Archi-Unterbrechung zur ID-Vergabe
  abgeschlossen werden. Archi bleibt Import-Ziel und Frontend,
  nicht ID-Quelle.

Abgrenzung — nicht Teil dieses Sprints:
  - Kein Eingriff in XML FLOW Scripts (XML00–XML07, frozen S3)
  - Kein Eingriff in CSV FLOW Scripts (CSV00–CSV09, frozen S3)
  - Kein Eingriff in ECM-Reihe (ECM00–ECM03, frozen S6)
  - Kein Ersatz des Archi CSV-Imports — Archi bleibt Consumer
  - Keine Änderung an master.xml Struktur oder sourceSystem-Logik
  - Kein automatisierter Archi-Import (bleibt manuell)
  - Keine Relations-ID-Vergabe im ersten Schritt (nur Elements)


================================================================================
3. FACHLICHER MEHRWERT
================================================================================

Mehrwert für: DEV + System-Stabilität + Skalierbarkeit + Toolbaukasten

  - Backend-Flows laufen vollständig ohne manuelle Archi-Unterbrechung —
    Testzyklen werden drastisch kürzer
  - Archi wird zum echten Frontend-Werkzeug (Modellierung, Visualisierung)
    und verliert seine ungewollte Rolle als ID-Gatekeeper im Backend
  - Archi-ID wird zur 3rd-Party-ID — gleichgestellt mit BPMN-ID,
    analog zu sourceSystem=bpmn heute bereits im XML FLOW
    (XML_FLOW_principles_S3, Kap. 6: "IDs werden NIEMALS modifiziert")
  - Tool-Austauschbarkeit steigt: jedes Tool das CSV oder XML exportiert
    kann Archi ersetzen ohne dass die ID-Logik bricht
  - Toolbaukasten-Prinzip wird architektonisch erfüllt: kein Tool ist
    privilegierter Backend-Enabler mehr — alle Tools sind gleichwertige
    Bausteine
  - ECM03 Reihenfolge-Join-Workaround wird langfristig obsolet
  - Grundlage für künftige SOURCE=CSV Aktivierung ohne Archi-Pflicht

Ohne diesen Sprint:
  Archi bleibt strukturell nicht austauschbar — unabhängig davon wie
  gut die Toolbaukasten-Prinzipien formuliert sind. Die Kopplung ist
  technisch, nicht dokumentarisch. Jeder neue Flow der IDs braucht
  reproduziert dieselbe Archi-Unterbrechung.


================================================================================
4. ABHÄNGIGKEITEN UND VORAUSSETZUNGEN
================================================================================

Voraussetzungen:
  - FREEZE-7 als Baseline                          Status: offen (Stage 7)
  - ECM-Reihe stabil und produktiv getestet        Status: erfüllt (Stage 6)
  - Verständnis der bestehenden ID-Entstehung      Status: erfüllt (HLP08)
  - GOV-Entscheid zur Umsetzung durch EUMAXL       Status: offen

Blockiert durch:
  - Keine technischen Blocker
  - Konzeptentscheid offen: ID-Format (siehe Kapitel 5.2)

Ermöglicht danach:
  - CSV-Refactoring Sprint (SOURCE=CSV ohne Archi-Unterbrechung)
  - ECM-Erweiterung Sprint (ECM03 Workaround ablösbar)
  - Jeder künftige Flow der neue Element-Typen einführt startet
    auf sauberer ID-Basis ohne Archi-Pflicht


================================================================================
5. TECHNISCHE KONZEPTIDEEN
================================================================================

Hinweis: Diese Ideen sind Vorausschau — keine Implementierungsentscheidung.
Entscheidungen fallen im Sprint selbst nach GOV 10.6.


5.1 Grundprinzip — Analogie zur BPMN-ID-Behandlung
----------------------------------------------------
Im XML FLOW gilt heute (XML_FLOW_principles_S3, Kapitel 6):

  "IDs werden NIEMALS modifiziert. XML04 annotiert nur
   sourceSystem und sourceModel auf dem kopierten Subtree."

BPMN-Elemente bringen ihre eigene ID mit — Camunda vergibt sie,
R+MUNI respektiert sie. Archi-IDs sollen auf dieselbe Stufe gestellt
werden:

  sourceSystem=bpmn   →  ID kommt von Camunda     (heute)
  sourceSystem=archi  →  ID kommt von Archi        (heute, soll sich ändern)
  sourceSystem=archi  →  ID kommt von IDHandler    (Ziel)
                         wenn kein Archi-Element vorhanden

Wenn ein Archi-Element bereits eine ID hat → IDHandler respektiert sie.
Wenn kein Archi-Element vorhanden → IDHandler vergibt eigene ID.
Das ist exakt das Verhalten das BPMN heute schon hat.


5.2 ID-Format Optionen (Konzeptdiskussion für Sprint)
------------------------------------------------------
Option A — UUID v4 (zufällig):
  Format: id-<uuid4>
  Vorteil: keine Kollisionen, kein Algorithmus nötig
  Nachteil: nicht reproduzierbar bei Neuanlage
  Eignung: gut für einmalige Neuerstellung

Option B — Content-Hash (deterministisch):
  Format: id-<sha256(Type+Name)[:12]>
  Vorteil: gleicher Input → gleiche ID (reproduzierbar)
  Nachteil: bricht bei Umbenennung
  Eignung: gut für stabile Entitäten

Option C — Sequenziell mit Persistenz:
  Format: id-rmuni-<YYYYMMDD>-<seq>
  Vorteil: menschenlesbar, nachvollziehbar
  Nachteil: braucht persistente Zähler-Datei
  Eignung: gut für kontrollierten Einzelbetrieb

Option D — Hybrid (Empfehlung zur Diskussion):
  Extern vergebene ID vorhanden → übernehmen (wie BPMN heute)
  Keine ID vorhanden → UUID v4 + Eintrag in IDH-Register
  IDH-Register: id_registry.csv in 01-artifacts\06-idh\


5.3 IDH-Register als zentrales Artefakt
-----------------------------------------
Eine persistente id_registry.csv speichert alle IDHandler-vergebenen IDs.

Mögliche Spalten:
  id, type, name, source, created_date, last_seen

Vorteil: Nachvollziehbarkeit, Debugging, spätere Deduplizierung.
Ablageort (Vorschlag): 01-artifacts\06-idh\id_registry.csv
  → neuer Unterordner, kein Eingriff in bestehende Struktur.

Diese Datei wäre R+MUNI-eigenes ID-Gedächtnis — unabhängig von Archi.


5.4 Neue Reihe IDH (Vorschlag)
--------------------------------
  IDH00   Umgebung validieren + IDH-Register prüfen / anlegen
  IDH01   Bestehende IDs einlesen (aus master.xml oder CSV)
           → ins Register laden, keine Überschreibung
  IDH02   Neue Elemente ohne ID erkennen
           → neue IDs vergeben → Register aktualisieren
  IDH03   Annotierte CSV / XML ausgeben (mit IDH-IDs)
           → bereit für direkten Archi-Import ohne vorherige
             Archi-Unterbrechung zur ID-Vergabe

Integrationspunkt: IDH03-Output ersetzt den
"Archi Import → Export"-Zwischenschritt in ECM und anderen Flows.


5.5 Was Archi dann noch tut
-----------------------------
  ✓ Modellieren                    (Frontend — unverändert)
  ✓ Visualisieren                  (Frontend — unverändert)
  ✓ CSV-Import als Consumer        (Import-Ziel — unverändert)
  ✓ OEF-Export als XML FLOW Quelle (3rd-Party-Quelle — unverändert)
  ✗ IDs vergeben                   (entfällt — übernimmt IDHandler)

Archi bleibt vollständig im Stack — aber als gleichwertiger Baustein,
nicht als privilegierter Backend-Enabler.


================================================================================
6. PRIORISIERUNG
================================================================================

Priorität:     Mittel — kein akuter Blocker, strategisch wertvoll
Zeitrahmen:    Stage 7 — nach ASC-Onboarding-Sprint, wenn Kapazität da

Priorisiert durch:
  Entwicklerwunsch + langfristige Toolbaukasten-Konformität.
  Kein externer Kundenbedarf der diesen Sprint erzwingt.
  Richtig wenn Backend-Flows häufiger genutzt werden und die
  Archi-Unterbrechung spürbar Zeit kostet.

Kann verschoben werden wenn:
  ASC-Onboarding oder O365-Integration höhere Priorität haben.
  Der bestehende Flow funktioniert weiterhin — IDH ist additiv.


================================================================================
7. GOVERNANCE-CHECK
================================================================================

| Kriterium                          | Status | Anmerkung                           |
|------------------------------------|--------|--------------------------------------|
| Auslöser GOV-konform (GOV 10.3)    | OK     | Entwicklerwunsch / Strukturberein.   |
| Fachlicher Mehrwert benennbar      | OK     | Siehe Kapitel 3                      |
| Ziel explizit und überprüfbar      | OK     | Kein Archi-Break im Backend-Flow     |
| Abgrenzung definiert               | OK     | Frozen Scripts S3/S6 unberührt       |
| Rückkopplungsschutz geprüft        | OK     | IDH ist neue Reihe — kein Eingriff   |
| Keine implizite GOV-Änderung       | OK     | Toolbaukasten-Prinzip wird gestärkt  |


================================================================================
8. STATUS UND VERLAUF
================================================================================

2026-03-21  ERSTELLT    EUMAXL + Claude (Pair-Session, Stage 6 Abschluss)


================================================================================
BEZÜGE
================================================================================

[[FREEZE-6_konsolidiert]]            aktuelle Baseline
[[GOV_Global_S6]]                    normative Grundlage
[[XML_FLOW_principles_S3]]           ID-Behandlung sourceSystem-Prinzip (Kap. 6)
[[ECM_principles_S6]]                ECM03 Reihenfolge-Join als Auslöser
[[HLP08_How2_ID-Merge-Run]]          Archi-Unterbrechung konkret dokumentiert
[[TOOLBAUKASTEN_principles_S6]]      Tool-Entscheidungsprinzipien
[[Sprint-DEV-EasyMapper_S6]]         ECM-Reihe als Bezugskontext


================================================================================
Sprint-DEV-BACKLOG_IDHandler_S7 | S7 | 2026-03-21 | R+MUNI Blueprint
Erstellt durch: EUMAXL + Claude (Pair-Session)
================================================================================
