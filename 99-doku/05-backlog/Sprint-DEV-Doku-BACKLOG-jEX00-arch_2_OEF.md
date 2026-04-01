================================================================================
BACKLOG | jEX-Reihe — Archi OEF Export via ACLI (jEX00)
================================================================================
Jira-Ticket   : offen — bei Erstellung in Jira eintragen
Typ           : Story
Status        : Backlog — Script vorbereitet, Umsetzung in Stage 5.7
Stage         : 5.7 (aktiv) — jEX-Reihe vorbereitet, noch nicht eingebunden
Erstellt      : 2026-03-16
Erstellt durch: EUMAXL + Claude (Pair-Session)
================================================================================


--------------------------------------------------------------------------------
1. KONTEXT
--------------------------------------------------------------------------------
Im R+MUNI Blueprint wird der OEF Export (Open Exchange Format / ArchiMate XML)
bisher manuell aus Archi heraus durchgeführt (GUI: Datei → Exportieren →
Open Exchange XML).

Ziel der jEX-Reihe ist die Automatisierung dieses Exports via Python + ACLI
(Archi Command Line Interface) — vollständig integrierbar in den bestehenden
flow.py Scriptrunner.

Ausgangspunkt dieser Story war eine Pair-Session zur Evaluierung ob der Export
via jArchi (Archi Scripting Plugin) oder via ACLI erfolgen soll.

Ergebnis der Evaluierung: ACLI ist der korrekte Weg (siehe Abschnitt 4).


--------------------------------------------------------------------------------
2. GOV-EINORDNUNG
--------------------------------------------------------------------------------
- Feature-Zuwachs gemäß GOV 10.5 (Entwicklerwunsch)
- Additiver Ausbau — keine Änderung bestehender Script-Logik
- Rückkopplungsschutz: Stage-3/4-Scripts bleiben unverändert
- Tool-Unabhängigkeit (GOV 4.7): ACLI ist offizieller Archi-Standard,
  keine proprietäre Abhängigkeit
- Explizitheit (GOV 1.6): Alle Entscheidungen dieser Session dokumentiert
- 1 Script = 1 Outcome (GOV 7.4): jEX00 exportiert ausschließlich OEF


--------------------------------------------------------------------------------
3. ZIEL
--------------------------------------------------------------------------------
Automatisierter OEF Export aus Archi-Modellen ohne manuelle GUI-Interaktion.

Ablauf:
  run-scope.txt → jEX00-arch_2_OEF.py → ACLI → OEF XML im Zielordner

Konkret:
  - Quellordner : 00-model\00-archimate\00-archimateactive\
                  00-model\00-archimate\01-archimateactivesub\
  - Zielordner  : 01-artifacts\00-xml\03-child\00-archimatechild\
  - Namensschema: <modellname>.archimate → <modellname>.xml
  - Überschreiben bestehender Files: erlaubt (kein Fehler)


--------------------------------------------------------------------------------
4. ENTSCHEIDUNG — jARCHI vs. ACLI
--------------------------------------------------------------------------------
In der Pair-Session wurde evaluiert ob der OEF Export via jArchi Script (.ajs)
oder via Python + ACLI (.py) erfolgen soll.

Evaluierung:

  Option A — jArchi (.ajs):
    Vorteil  : Läuft direkt in Archi, kein separater Prozess
    Nachteil : model.save() unterstützt nur natives .archimate Format
               Model Functions ($.model) bieten nur PNG/SVG/PDF Render
               → OEF Export ist in der jArchi API nicht vorgesehen
               → Einziger Ausweg wäre java.lang.Runtime.exec() → ACLI
               → Das würde eine zweite Archi-Instanz starten = Konflikt

  Option B — Python + ACLI (.py):  ← GEWÄHLT
    Vorteil  : --xmlexchange.export ist offizieller ACLI-Parameter
               Passt nahtlos in bestehenden flow.py Scriptrunner
               Keine zweite Archi-Instanz wenn Archi bereits offen
               Sauber trennbar: jEX-Reihe bleibt Python-Reihe
    Nachteil : Archi muss via ACLI headless gestartet werden

Entscheid: Option B — Python + ACLI
Begründung: API-Limitation von jArchi, sauberere Blueprint-Integration,
            kein Instanz-Konflikt.

Referenz Wiki:
  jArchi Model API    : https://github.com/archimatetool/archi-scripting-plugin/wiki/Model
  jArchi Model Funct. : https://github.com/archimatetool/archi-scripting-plugin/wiki/Model-Functions
  Archi ACLI          : https://github.com/archimatetool/archi/wiki/Archi-Command-Line-Interface


--------------------------------------------------------------------------------
5. ZUKUNFT — jARCHI STAGE (EIGENE STAGE)
--------------------------------------------------------------------------------
Die Frage nach jArchi als "Script Cockpit" (Archi als Startpunkt für alle
Flows) wurde bewusst zurückgestellt.

Konzept für spätere Stage:
  Archi Script Manager → COCKPIT.ajs → startet flow.py via java.lang.Runtime
  → flow.py orchestriert alle Python Scripts inkl. ACLI-Calls

Voraussetzungen für diese Stage:
  - Alle jEX-Scripts als Python fertig und getestet
  - ACLI-Aufruf aus Python stabil
  - jArchi Cockpit Script als separater Baustein

Wichtig: Das COCKPIT.ajs startet flow.py — es ruft ACLI nicht direkt auf.
         Damit wird der Instanz-Konflikt (Katze/Schweif) vermieden.
         jArchi → flow.py → ACLI (neue headless Instanz, kein Konflikt)


--------------------------------------------------------------------------------
6. SCRIPT-SPEZIFIKATION — jEX00-arch_2_OEF.py
--------------------------------------------------------------------------------
Ablageort  : 01-artifacts\01-scripts\jEX00-arch_2_OEF.py
Typ        : Python 3
Aufruf     : Direkt via PowerShell ODER via flow.py Scriptrunner

Logik:

  Schritt 1 — run-scope.txt parsen
    Pfad   : 02-stages\run-scope.txt (relativ zu root)
    Regel  : Nur aktive (nicht auskommentierte) Zeilen
             Zeilen mit # am Anfang = ignoriert
             SOURCE=archi + folgendes MODEL= = aktiver Eintrag

  Schritt 2 — Einträge prüfen
    Aktiv    : Mindestens 1 aktiver SOURCE=archi Eintrag vorhanden
               → nur die definierten MODEL= Dateien verarbeiten
    Kein     : Kein aktiver SOURCE=archi Eintrag vorhanden
               → ABBRUCH mit Hinweis, keine Verarbeitung
               → Grundregel Blueprint: "Ist kein Modell ausgewählt wird
                 im FLOW KEINES berücksichtigt."
               → Wildcard-Logik ist in nachgelagerten Filterfiles umgesetzt
                 — NICHT in run-scope.txt

  Schritt 3 — OEF Export via ACLI
    Pro Datei:
      Archi.exe -application com.archimatetool.commandline.app
                -consoleLog -nosplash
                --loadModel "<quellpfad>\<modell>.archimate"
                --xmlexchange.export "<zielpfad>\<modell>.xml"

  Schritt 4 — Logging + Zusammenfassung
    Log    : 02-stages\99-logs\jEX00-arch_2_OEF.log (append)
    Konsole: Fortschritt + Zusammenfassung (OK / Fehler)

Konfiguration:
  root.cfg   : Pfad zu BLUEPRINT_ROOT (Standard R+MUNI Konvention)
  Archi.exe  : Pfad zur Archi Installation — in root.cfg oder eigener Konfig

Offener Punkt:
  Archi.exe Pfad variiert je Installation → Konfigurationsstrategie
  für Betakunden klären (root.cfg Eintrag vs. eigene archi.cfg)


--------------------------------------------------------------------------------
7. ACLI PARAMETER REFERENZ (OEF EXPORT)
--------------------------------------------------------------------------------
Vollständiger Befehl (Windows):

  Archi -application com.archimatetool.commandline.app -consoleLog -nosplash
        --loadModel "pfad\modell.archimate"
        --xmlexchange.export "pfad\output.xml"

Optionale Parameter:
  --xmlexchange.exportFolders    Ordnerstruktur als <organization> exportieren
  --xmlexchange.exportLang <xx>  Sprachcode (z.B. de, en)

Ausführungsreihenfolge ACLI (fix, unabhängig von Parameterreihenfolge):
  Priorität 10: Load/Create Model
  Priorität 20: Import
  Priorität 30: Script ausführen
  Priorität 40: Export / Report
  Priorität 50: Save Model


--------------------------------------------------------------------------------
8. ARCHI PLUGIN KONTEXT
--------------------------------------------------------------------------------
EUMAXL ist Patreon-Mitglied (ab $5/Monat) — folgende Plugins verfügbar:

  jArchi (kompiliert)       : Scripting Plugin für .ajs Scripts
  Excel Export Plugin 1.1.1 : --excel.export via ACLI
                              Exportiert Elements, Relations, Properties,
                              Specializations je als eigenes XLSX Sheet

Jeder neue R+MUNI Betakunde erhält ein Jahres-Patreon-Abo als Geschenk
→ Betakunden haben dieselbe Plugin-Basis wie EUMAXL.

Relevanz für jEX-Reihe:
  jEX00 : OEF Export   → ACLI --xmlexchange.export (kein Plugin nötig)
  jEX01 : XLSX Export  → ACLI --excel.export (Excel Plugin 1.1.1)
  (jEX01 ist noch nicht spezifiziert — Backlog für spätere Session)


--------------------------------------------------------------------------------
9. ABGRENZUNG
--------------------------------------------------------------------------------
- jEX00 exportiert ausschließlich OEF XML — kein CSV, kein XLSX
- jEX00 verändert keine Modelle — reiner Export, keine Rückwirkung
- jEX00 ist kein Ersatz für den manuellen GUI-Export — Ergänzung
- jEX-Reihe sitzt VOR der XML-Reihe im Flow (Export → dann Weiterverarbeitung)
- jArchi Scripts (.ajs) sind für diese Reihe bewusst zurückgestellt


--------------------------------------------------------------------------------
10. OFFENE PUNKTE FÜR UMSETZUNG
--------------------------------------------------------------------------------
- Archi.exe Pfad Konfigurationsstrategie festlegen (root.cfg vs. archi.cfg)
- Jira Ticket anlegen und mit dieser Doku verlinken
- jEX00-arch_2_OEF.py fertigstellen und testen
- FLW flowmapping.txt Eintrag für jEX00 anlegen
- BPMN Default Flow für jEX00 definieren (Stage 5.7)
- jEX01 (XLSX Export) als Folge-Story spezifizieren


================================================================================
BACKLOG | jEX-Reihe | jEX00-arch_2_OEF
R+MUNI Blueprint | EUMAXL + Claude (Pair-Session) | 2026-03-16
================================================================================
