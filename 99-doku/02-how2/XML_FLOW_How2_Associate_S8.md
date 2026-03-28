================================================================================
XML FLOW — HOW2 (Associate)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : XML_FLOW_How2_Associate_S8
Tag             : #associate #how2 #xmlflow #s8
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : ENTWURF
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Hinweis         : Inhalt initial ident mit DEV-Gegenstück — inhaltliche Trennung in Stage 1
================================================================================



VORAUSSETZUNGEN
--------------------------------------------------------------------------------
- Python 3.10+
- lxml installiert (pip install lxml) → zwingend für XML05
- BLUEPRINT_ROOT korrekt in root.txt eingetragen
- Quelldateien in den deklarierten child_mapping.txt Verzeichnissen vorhanden


KOMPLETTER FLOW – SCHRITT FÜR SCHRITT
--------------------------------------------------------------------------------

Schritt 1: Root auflösen
  python XML00-resolve_root.py
  → Liest root.txt, löst BLUEPRINT_ROOT auf
  → Erzeugt: 03-stages/99-logs/XML00-root.resolved.txt
  → Erzeugt: 03-stages/99-logs/XML00-root.log

Schritt 2: Quellen einsammeln
  python XML01-collect_sources.py
  → Liest child_mapping.txt
  → Sammelt alle .xml / .bpmn Dateien aus deklarierten Verzeichnissen
  → Erzeugt je Quellentyp:
      03-stages/00-archimatearchive/XML01-sources.resolved.txt
      03-stages/01-bpmnarchive/XML01-sources.resolved.txt

Schritt 3: XML-Metadaten parsen
  python XML02-parse_child_xml.py
  → Öffnet jede Quelldatei, liest Root-Tag und Namespace
  → Nur Metadaten, kein Content-Kopieren
  → Erzeugt: XML02-parsed.txt pro Archiv-Verzeichnis

Schritt 4: Index aufbauen
  python XML03-build_index.py
  → Erstellt schlanken Objektindex pro Modell
  → Archi: identifier + xsi:type + name
  → BPMN: id + Tag-Lokalname + name
  → Erzeugt: XML03-index.xml pro Archiv-Verzeichnis

Schritt 5: Merger ausführen
  python XML04-merge_master.py
  → Liest mapping.txt
  → Matched Index-Einträge gegen Mapping-Regeln
  → Lädt Original-XML nur für gematchte Objekte
  → Annotiert sourceSystem + sourceModel auf jedem Subtree
  → Erzeugt: 02-artifacts/00-xml/00-master/master.generated.xml

Schritt 6: Konsolidieren
  python XML05-clear_merge.py
  → Liest sync.txt
  → Löst id/identifier Duplikate auf (merge-Action)
  → Erfordert lxml
  → Erzeugt: 02-artifacts/00-xml/00-master/master.cleared.xml

Schritt 7: Finalisieren
  python XML06-finalize-master.py
  → Kopiert master.cleared.xml → master.xml
  → Keine Transformation, keine Validierung
  → Erzeugt: master.xml (stabile Referenz)

Schritt 8: Aufräumen
  python XML07-cleanup-artifacts.py
  → Löscht alle XML00-XML05 Zwischenartefakte und Logs
  → Behält: master.xml, XML06/XML07 Logs


KONFIGURATIONSDATEIEN – KURZREFERENZ
--------------------------------------------------------------------------------

02-artifacts/00-xml/child_mapping.txt
  Format: <source_type>-<relativer Pfad>
  Zweck: Deklariert welche Verzeichnisse als Quellen dienen.
  Beispiel:
    archi-02-artifacts/00-xml/03-child/00-archimatechild
    bpmn-02-artifacts/00-xml/03-child/01-bpmnchild

02-artifacts/00-xml/01-mapping/mapping.txt
  Format: <source>[<model-filter>]-<entry-point>+<filter>
  Zweck: Steuert welche Objekte ins master.xml kommen.
  Beispiele:
    archi[*]-element+xsi:type="BusinessProcess"
    bpmn[*]-*
    archi[*Importer*]-element

02-artifacts/00-xml/02-sync/sync.txt
  Format: <selector>::<action>
  Zweck: Konsolidierungsregeln für XML05.
  Beispiel:
    bpmn-process+has:id+no:identifier::merge
    archi-element+has:identifier::keep


MAPPING.TXT – SYNTAX DETAIL
--------------------------------------------------------------------------------
Grundform:
  <source>[<model-filter>]-<entry-point>+<filter>+<filter>

source:         archi | bpmn
model-filter:   Dateiname-Pattern mit * als Wildcard. [*] = alle Modelle.
entry-point:    Lokalname des XML-Tags (z.B. "element", "process", "serviceTask")
                bpmn:serviceTask ist auch gültig (: wird als Präfix behandelt)
                * oder leer = alle Tags
filter:         xsi:type="Wert" filtert nach xsi:type Attribut

Trenner WICHTIG:
  - (Minus) nach ] → trennt source vom entry-point
  + (Plus)         → trennt entry-point von Filtern

Beispiele:
  archi[*]-element+xsi:type="BusinessProcess"
    → Alle BusinessProcess Elemente aus allen Archi-Modellen

  bpmn[*BUP01*]-*
    → Alle Objekte aus BPMN-Modellen die "BUP01" im Namen haben

  archi[*]-*
    → Alles aus allen Archi-Modellen (Wildcard)


HÄUFIGE FEHLER UND LÖSUNGEN
--------------------------------------------------------------------------------

Fehler: "index not found, skipping"
  Ursache: XML03 wurde nicht ausgeführt oder ist fehlgeschlagen.
  Lösung: Reihenfolge einhalten, XML03 prüfen.

Fehler: "subtree not found: <id>"
  Ursache: Der Index enthält eine ID die im Original-XML nicht mehr vorhanden
  ist (z.B. Datei wurde geändert nach XML03 Lauf).
  Lösung: Flow komplett neu starten ab XML01.

Fehler: "lxml not found" bei XML05
  Lösung: pip install lxml

master.xml enthält unerwartete Elemente
  Ursache: mapping.txt Regel ist zu weit gefasst (z.B. archi[*]-* matcht alles).
  Lösung: mapping.txt präzisieren mit xsi:type Filter.

master.xml enthält Duplikate nach XML05
  Ursache: sync.txt hat keine Regel für den betroffenen Typ.
  Lösung: sync.txt ergänzen. Format: <selector>::merge

XML05 meldet AMBIGUOUS für eine ID
  Ursache: Mehr als ein Element mit identifier für dieselbe id.
  Das ist ein Datenproblem in den Quellen.
  Lösung: Quellmodelle prüfen, Duplikat-IDs bereinigen.


MASTER.XML STRUKTUR – ÜBERSICHT
--------------------------------------------------------------------------------
master.xml hat folgende Struktur nach einem vollständigen Lauf:

  <master last-updated="..." last-updated-by="...">
    <!-- Archi Elemente (direkte Subtrees aus OEF) -->
    <element xsi:type="BusinessProcess"
             identifier="id-..."
             sourceSystem="archi"
             sourceModel="R+Muni Architecture Modell.xml">
      <name xml:lang="de">Prozessname</name>
      ...
    </element>

    <!-- BPMN Definitionen (nach M2B05 writeback) -->
    <definitions sourceSystem="bpmn"
                 sourceModel="BUP01-Entwicklung.bpmn">
      <process id="id-..." name="Prozessname" .../>
      ...
    </definitions>
  </master>

sourceSystem und sourceModel sind immer gesetzt – sie sind die
Rückverfolgbarkeit zu den Originalquellen.