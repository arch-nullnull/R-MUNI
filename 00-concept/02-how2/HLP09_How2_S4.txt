================================================================================
HLP09 REPORT SERVER – HOW2 (Poweruser)
Stage 4 | Aktiv | R+MUNI Blueprint
================================================================================
Erstellt    : 2026-03-07
Stage       : S4 – AKTIV
Ablageort   : 00-concept/02-how2/HLP09_How2_S4.txt
================================================================================


VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- Python 3.10+ (keine externen Pakete erforderlich)
- BLUEPRINT_ROOT korrekt in root.txt eingetragen
- webconfig.txt in 02-artifacts/05-reports/ vorhanden und konfiguriert
- Archi HTML Report in den jeweiligen Report-Ordner exportiert


ZWECK
--------------------------------------------------------------------------------
HLP09 startet einen lokalen Webserver fuer jeden in webconfig.txt
konfigurierten HTML Report. Alle Reports laufen gleichzeitig, jeder
auf seinem eigenen Port. Erreichbar lokal und im gesamten lokalen Netz.

Kein Apache, kein IIS, keine Installation — reines Python.
Server laeuft nur solange das Script aktiv ist (kein Hintergrunddienst).


================================================================================
SCHRITT 1 – ARCHI HTML REPORT EXPORTIEREN
================================================================================

In Archi:
  File → Report → HTML

  Zielordner waehlen:
    <BLUEPRINT_ROOT>/02-artifacts/05-reports/00-archimate/<Modellname>/

  Beispiele:
    .../05-reports/00-archimate/MUNI EA Modell/
    .../05-reports/00-archimate/MUNI FLOW/
    .../05-reports/01-bpmn/Business Prozesse/

  Archi legt dabei automatisch index.html und alle Unterordner an.
  Der Zielordner muss vorher existieren.


================================================================================
SCHRITT 2 – WEBCONFIG.TXT KONFIGURIEREN
================================================================================

Datei: 02-artifacts/05-reports/webconfig.txt

Fuer jeden Report einen Block anlegen:

  NAME=Anzeigename des Reports
  PATH=relativer/pfad/zum/report/ordner
  PORT=8080

  NAME=Zweiter Report
  PATH=00-archimate/MUNI FLOW
  PORT=8081

Regeln:
  - PATH ist relativ zu 02-artifacts/05-reports/
  - Jeder PORT darf nur einmal vorkommen
  - Leerzeile trennt Eintraege
  - Zeilen mit # sind Kommentare (Eintrag wird nicht gestartet)
  - Ordner ohne index.html werden beim Start uebersprungen (Warnung)

Ports Empfehlung:
  ArchiMate Reports : 8080 - 8089
  BPMN Reports      : 8090 - 8099
  Struktur Reports  : 8100 - 8109


================================================================================
SCHRITT 3 – SERVER STARTEN
================================================================================

  cd 02-artifacts/01-scripts/
  python HLP09-serve_report.py

  Optionale Parameter:
    --no-browser    Browser nicht automatisch oeffnen

  Beispiel ohne Browser:
    python HLP09-serve_report.py --no-browser

  root.txt wird automatisch zwei Ebenen aufwaerts gesucht.
  Log: 03-stages/99-logs/HLP09-serve_report.log (append)


================================================================================
WAS DAS SCRIPT IM TERMINAL AUSGIBT
================================================================================

  ======================================================================
    R+MUNI Report Server  |  2026-03-07 14:30:00
  ======================================================================
    Report                  Lokal                  IP               Hostname
  ----------------------------------------------------------------------
    MUNI EA Modell          http://localhost:8080   http://192.168.1.42:8080   http://MARKUS-PC:8080
    MUNI FLOW               http://localhost:8081   http://192.168.1.42:8081   http://MARKUS-PC:8081
  ----------------------------------------------------------------------
    Uebersprungen (1 Eintrag):
      Port 8090   Business Prozesse  ->  kein index.html
  ----------------------------------------------------------------------
    Beenden:  STRG+C
  ======================================================================

  Lokal     = nur auf diesem PC erreichbar
  IP        = erreichbar fuer alle Geraete im lokalen Netzwerk
  Hostname  = erreichbar ueber Windows-Computernamen (z.B. http://MARKUS-PC:8080)


================================================================================
NEUEN REPORT HINZUFUEGEN
================================================================================

  1. In Archi HTML Report exportieren nach:
       02-artifacts/05-reports/<weltordner>/<Modellname>/

  2. In webconfig.txt neuen Block ergaenzen:
       NAME=Mein neues Modell
       PATH=00-archimate/Mein neues Modell
       PORT=8083

  3. Script neu starten (STRG+C → python HLP09-serve_report.py)

  Fertig.


================================================================================
REPORT DEAKTIVIEREN (OHNE LOESCHEN)
================================================================================

  In webconfig.txt die drei Zeilen des Eintrags auskommentieren:

    #NAME=Mein Report
    #PATH=00-archimate/Mein Report
    #PORT=8083

  Beim naechsten Start wird dieser Report nicht mehr gestartet.


================================================================================
FEHLERMELDUNGEN UND LOESUNGEN
================================================================================

  FEHLER: webconfig.txt nicht gefunden
  → Datei in 02-artifacts/05-reports/ anlegen
  → Vorlage: webconfig.txt aus Blueprint-Dokumentation verwenden

  WARNUNG: kein index.html — bitte HTML Report exportieren
  → Archi HTML Export fuer dieses Modell noch nicht durchgefuehrt
  → Schritt 1 ausfuehren, dann Script neu starten

  FEHLER: Port 8080 nicht verfuegbar
  → Ein anderes Programm belegt diesen Port bereits
  → In webconfig.txt anderen Port eintragen (z.B. 8085)

  FEHLER: Ordner nicht gefunden
  → PATH in webconfig.txt pruefen
  → Ordner in 02-artifacts/05-reports/ manuell anlegen

  FEHLER: Port wird mehrfach verwendet
  → Jeden PORT nur einmal in webconfig.txt vergeben


================================================================================
DATEIEN UND ABLAGEN
================================================================================

  Script   : 02-artifacts/01-scripts/HLP09-serve_report.py
  Config   : 02-artifacts/05-reports/webconfig.txt
  Log      : 03-stages/99-logs/HLP09-serve_report.log

  Report-Ordner Struktur (Beispiel):
    02-artifacts/05-reports/
      webconfig.txt
      00-archimate/
        MUNI EA Modell/        ← Archi HTML Export (enthaelt index.html)
        MUNI FLOW/             ← Archi HTML Export (enthaelt index.html)
      01-bpmn/
        Business Prozesse/     ← BPMN HTML Export (enthaelt index.html)
      99-struktur/
        Blueprint Struktur/    ← Struktur Report (enthaelt index.html)


================================================================================
HLP09 REPORT SERVER – HOW2  |  S4  |  ENDE
================================================================================
