================================================================================
HLP HELPER SCRIPTS – PRINCIPLES
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : HLP_principles_S3
Tag             : #dev #principles #hlp #s3 #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-02
Rückkopplungsschutz : S3 — Inhalt read-only, kein inhaltlicher Eingriff
Ablageort       : 00-concept/01-principles/HLP_principles_S3.txt
================================================================================


1. ZWECK UND DESIGNPHILOSOPHIE
--------------------------------------------------------------------------------
Die HLP-Scripts (HLP00–HLP07) sind autarke, single-responsibility Utilities
für wiederkehrende Betriebsaufgaben im Blueprint-Umfeld: Root-Auflösung,
Dateisystemoperationen, Logging, Backup und Restore.

Kernprinzip: Jedes HLP-Script macht genau eine Sache. Es hat keine
Abhängigkeit zu anderen HLP-Scripts und keine Abhängigkeit zu Flow-Artefakten
(keine Nutzung von root.resolved.txt o.ä.).

HLP-Scripts sind Werkzeuge, keine Flow-Stages. Sie können in beliebiger
Reihenfolge und unabhängig voneinander aufgerufen werden.


2. ROOT-AUFLÖSUNG (AUTARK)
--------------------------------------------------------------------------------
Alle HLP-Scripts lösen ROOT via:
  ROOT = os.path.dirname(os.path.abspath(__file__))

Das bedeutet: ROOT ist immer das Verzeichnis in dem das Script liegt.
Für den Blueprint ist das 02-artifacts/01-scripts/.

Relative Pfad-Angaben in Argumenten werden gegen ROOT aufgelöst via
abs_path() Hilfsfunktion. Absolute Pfade werden direkt verwendet.

Kein HLP-Script liest root.txt oder andere Flow-Artefakte.
Die Autarkie ist bewusst – HLP-Scripts sollen auch dann funktionieren
wenn der Flow noch nicht ausgeführt wurde.


3. LOGGING-PRINZIP
--------------------------------------------------------------------------------
Alle HLP-Scripts schreiben Logs im Append-Modus:
  ROOT/logs/<ScriptName>.log

Logs werden nicht rotiert, nicht geleert. Sie akkumulieren über alle Läufe.
Jeder Eintrag hat einen Timestamp.

HLP04 ist der einzige Script der explizit für Logging-Zwecke gebaut ist
(Verzeichnisbaum-Dokumentation). Die anderen Scripts loggen als Nebeneffekt.


4. FEHLERVERHALTEN
--------------------------------------------------------------------------------
Alle HLP-Scripts geben bei Fehler eine klare Meldung aus und beenden mit
sys.exit(1). Kein Silent-Fail.

Wichtige Fehlerquellen:
  HLP01/HLP02: Quellpfad nicht gefunden → Abbruch
  HLP03: Ordner nicht gefunden → SKIP (kein Abbruch, nur Warnung)
  HLP06: Quellordner nicht gefunden → Abbruch
  HLP07: Backup-Archiv nicht gefunden → Abbruch
         manifest.json fehlt im Archiv → Abbruch (kein gültiges HLP06-Backup)


5. DESTRUKTIVE OPERATIONEN – REGELN
--------------------------------------------------------------------------------
HLP02 (move): Löscht die Quelle nach dem Verschieben. Unwiderruflich.
HLP03 (clean): Löscht alle Inhalte eines Ordners. Der Ordner selbst bleibt.
               Mehrere Ordner können als Argumente übergeben werden.

Regel: HLP03 löscht Dateien UND Unterordner – inklusive aller Inhalte.
       Es gibt keine Bestätigungsabfrage. Vor destruktiven Operationen
       immer HLP06 Backup erstellen.


6. BACKUP-INTEGRITÄT (HLP06/HLP07)
--------------------------------------------------------------------------------
HLP06 erstellt ein vollständiges ZIP-Archiv mit eingebettetem manifest.json.
Das Manifest enthält SHA-256 Checksums aller Dateien.

Archivformat:
  backup/relative/pfad/zur/datei   (im ZIP)
  manifest.json                     (im ZIP root)

HLP07 liest ausschließlich HLP06-kompatible Archive. Ein Archiv ohne
manifest.json wird abgelehnt.

Nach dem Restore führt HLP07 automatisch eine Checksum-Verifikation durch
(kann mit --no-verify übersprungen werden).

DEFAULT_EXCLUDE in HLP06:
  .git, __pycache__, .venv, venv, node_modules, .idea, .vscode,
  .DS_Store, Thumbs.db

Zusätzliche Ausschlüsse via --exclude Argument möglich.


7. KEINE EXTERNE ABHÄNGIGKEITEN
--------------------------------------------------------------------------------
Alle HLP-Scripts (HLP00–HLP07) verwenden ausschließlich Python stdlib:
  os, sys, shutil, zipfile, hashlib, json, platform, datetime, argparse

Keine pip-Pakete erforderlich. HLP-Scripts laufen auf jeder Python 3.10+
Installation ohne Vorbereitung.

Einzige Ausnahme: HLP06/HLP07 verwenden zipfile – das ist stdlib, kein
externes Paket.


8. GRENZEN DER HLP-SCRIPTS
--------------------------------------------------------------------------------
- Kein Verständnis von Blueprint-Semantik – reine Dateisystemoperationen
- Kein Schutz gegen versehentliche Mehrfachausführung (HLP03 ist sofort)
- HLP06 Backup ist kein Versionierungssystem – last-write-wins im backups/
  Ordner wenn gleicher Timestamp (praktisch ausgeschlossen, da Sekunden-genau)
- HLP07 Restore überschreibt bestehende Dateien am Zielpfad ohne Warnung
- HLP05 context.json enthält Hostname – auf geteilten Systemen beachten
