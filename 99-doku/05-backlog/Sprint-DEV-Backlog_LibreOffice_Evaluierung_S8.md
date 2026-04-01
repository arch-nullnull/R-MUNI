================================================================================
LibreOffice Evaluierung — BACKLOG (Associate)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : ASSOCIATE_Backlog_LibreOffice_Evaluierung_S8
Tag             : #associate #backlog #libreoffice #xlsx #csv #txt #trennzeichen #s8
Datum           : 2026-03-27
Stage           : S8 — AKTIV
Status          : BACKLOG — nicht gestartet
Verantwortlich  : EUMAXL
Review          : offen
Jira-Sync       : NEIN — Jira nach explizitem EUMAXL-Input
================================================================================


================================================================================
1. AUSGANGSLAGE UND KONTEXT
================================================================================

Warum existiert dieser Backlog-Eintrag?
  LibreOffice wird als kostenlose, open-source Desktop-Alternative zu
  Microsoft Office evaluiert. XLSX kommt als Format in der R+MUNI-Umgebung
  vor und bleibt ein reales Austauschformat — das ist keine Frage der
  Strategie sondern der Realität.

  Zwei konkrete Testthemen werden evaluiert:
    Block A — XLSX Kompatibilität mit der R+MUNI-Umgebung
    Block B — TXT / CSV Integration, Exports und Trennzeichen-Thematik
              inkl. Lokalisierungsproblematik

  Diese beiden Blöcke sind voneinander unabhängig — können separat
  gestartet und abgeschlossen werden.

Was ist der gewünschte Zielzustand?
  Für Block A: Klares Bild ob LibreOffice Calc XLSX-Dateien öffnen,
  bearbeiten und in der R+MUNI-Umgebung (CSV07, openpyxl-Flow) sauber
  verarbeiten kann — ohne Datenverlust, ohne Formatbruch.

  Für Block B: Klares Bild wie LibreOffice mit CSV / TXT-Dateien umgeht —
  insbesondere welche Trennzeichen (Komma, Semikolon, Pipe |) erkannt und
  exportiert werden, wie die Lokalisierungseinstellungen (Deutsch / Österreich)
  das Verhalten beeinflussen, und ob TXT als alternatives Exportformat
  sauber in den R+MUNI-Flow integrierbar ist.

Warum jetzt noch nicht?
  Stage 8 hat laufende Prioritäten (Beta-Release S8-Z1). Evaluierung
  erfordert dedizierten Testblock — kein Tagesgeschäft. LibreOffice muss
  zunächst installiert sein (kein Aufwand, aber expliziter Schritt).


================================================================================
2. SCOPE
================================================================================

Was gehört dazu:

  BLOCK A — XLSX Kompatibilität:
  - LibreOffice Calc: XLSX öffnen und auf Darstellungsqualität prüfen
  - Speichern als XLSX aus LibreOffice → Verarbeitung durch CSV07 testen
  - Verhalten bei Formeln, Umlauten (ä, ö, ü), Sonderzeichen prüfen
  - Encoding-Verhalten beim XLSX-Export aus LibreOffice prüfen (UTF-8?)
  - Vergleich: Excel-generierte XLSX vs. LibreOffice-generierte XLSX
    → Macht CSV07 (openpyxl) einen Unterschied?

  BLOCK B — TXT / CSV Integration und Trennzeichen:
  - LibreOffice Calc: CSV öffnen mit Trennzeichen-Dialog testen
    (Komma vs. Semikolon — welches wird erkannt, welches vorgeschlagen?)
  - Lokalisierungsthematik dokumentieren:
    Deutsch/Österreich → Windows-Standard ist Semikolon als Listentrennzeichen
    → wie verhält sich LibreOffice beim Öffnen und beim Export?
    → weicht das Verhalten von Excel ab oder ist es identisch?
  - Export aus LibreOffice Calc → CSV / TXT mit definiertem Trennzeichen testen
    (kann man Komma erzwingen obwohl System auf Semikolon steht?)
  - Ergebnis-CSV aus LibreOffice durch CSV98 Quality Gate laufen lassen
  - Encoding-Verhalten beim CSV/TXT-Export prüfen (UTF-8 ohne BOM?)

Was gehört explizit nicht dazu:
  - LibreOffice Writer, Impress, Base — kein R+MUNI Kontext in diesem Block
  - Makros oder Scripting in LibreOffice
  - Migration bestehender Kundendokumente
  - Visio / Draw.io Thematik (separater Backlog falls gewünscht)
  - Entscheidung ob LibreOffice in den Toolbaukasten aufgenommen wird
    (folgt nach Evaluierung — ist Ergebnis, nicht Scope)


================================================================================
3. TESTGRUNDLAGE — BESTEHENDE R+MUNI ARTEFAKTE
================================================================================

Relevante Scripts und Artefakte für die Evaluierung:

  CSV07-xlsx_2_csv.py       XLSX → Master CSV — Kernscript für Block A
  CSV98-clean_master.py     Quality Gate — relevant für Block B Ausgabe
  openpyxl                  Python-Paket das XLSX verarbeitet (pip install)
  01-artifacts\02-csv\      CSV-Artefakt-Ordner — Referenz für Trennzeichen
  01-artifacts\03-XLSX\     XLSX-Artefakt-Ordner — Referenz für Block A

  Encoding-Standard R+MUNI: UTF-8 ohne BOM (Ausnahme: ATL02 mit BOM)
  Trennzeichen-Standard R+MUNI: in csvmapping.txt definiert — vor Test prüfen


================================================================================
4. BEKANNTE RISIKEN UND VORAB-ERKENNTNISSE
================================================================================

  Lokalisierung Semikolon-Falle:
    Windows mit Regionaleinstellung Deutsch/Österreich verwendet Semikolon
    als Standard-Listentrennzeichen. LibreOffice Calc übernimmt diese
    Einstellung beim CSV-Export wenn nicht explizit anders konfiguriert.
    → R+MUNI erwartet ein definiertes Trennzeichen — Abweichung bricht den Flow.

  openpyxl und LibreOffice XLSX:
    LibreOffice speichert XLSX im OOXML-Format — technisch identisch mit
    Excel. openpyxl kann beides lesen. Risiko: Formeln, benannte Bereiche
    oder spezielle Excel-Features könnten fehlen oder abweichen.
    → Für R+MUNI relevant sind nur Datenfelder — keine Formeln erwartet.


================================================================================
5. VORAUSSETZUNGEN FÜR UMSETZUNG
================================================================================

  - LibreOffice aktuelle Stable-Version installiert (Download: libreoffice.org)
  - Mindestens eine reale R+MUNI XLSX-Datei als Testdatei verfügbar
  - Mindestens eine reale R+MUNI CSV-Datei als Testdatei verfügbar
  - CSV07 läuft in der aktuellen Umgebung (CSV00 grün)
  - Notepad++ mit CSV Lint Plugin für Encoding-Kontrolle bereit


================================================================================
6. OFFENE FRAGEN
================================================================================

| Frage                                              | Wer klärt | Bis wann |
|----------------------------------------------------|-----------|----------|
| Welches Trennzeichen nutzt csvmapping.txt aktuell? | EUMAXL    | offen    |
| Ist Pipe | bereits in einem R+MUNI Script als      | EUMAXL    | offen    |
| Trennzeichen definiert oder konfigurierbar?        |           |          |
| Soll Block A und Block B gemeinsam oder getrennt   | EUMAXL    | offen    |
| als Sprint durchgeführt werden?                    |           |          |
| Welche XLSX-Datei dient als Referenz für Block A?  | EUMAXL    | offen    |


================================================================================
7. VERWANDTE DOKUMENTE UND VERKNÜPFUNGEN
================================================================================

  [[Install.txt]]                  openpyxl als Pflichtpaket, XLSX-Flow
  [[FREEZE_7]]                     FREEZE 7 — Offener Punkt 17.3 CSV-Refactoring
  [[STAGE8_ZIELE_S8]]              Stage-Prioritäten — Einordnung dieses Backlogs
  [[GOV_Global_S8]]                GOV 9.7 CSV als Transportformat (normative Basis)
  [[ASSOCIATE_Backlog_O365_S8]]    Verwandter Backlog O365 Integration

  Externe Referenzen:
    https://www.libreoffice.org/download/libreoffice-still/   Stable Release
    https://wiki.documentfoundation.org/Faq/Calc/022          CSV Trennzeichen FAQ


================================================================================
LibreOffice Evaluierung | ASSOCIATE | S8 | 2026-03-27 | R+MUNI Blueprint
================================================================================
