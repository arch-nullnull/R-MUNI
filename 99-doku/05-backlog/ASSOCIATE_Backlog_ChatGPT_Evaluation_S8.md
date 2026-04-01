================================================================================
ChatGPT Evaluation – KI-Tool Exploration für R+MUNI (BACKLOG)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : ASSOCIATE_Backlog_ChatGPT_Evaluation
Tag             : #associate #backlog #ki #chatgpt #evaluation
Datum           : 2026-03-28
Stage           : S8 — AKTIV
Status          : BACKLOG — pausiert
Verantwortlich  : EUMAXL
Review          : offen
Jira-Sync       : NEIN
================================================================================


================================================================================
1. AUSGANGSLAGE UND KONTEXT
================================================================================

Warum existiert dieser Backlog-Eintrag?
ChatGPT wurde als experimenteller Ersatz für Copilot in der DEV-Umgebung
getestet. Auslöser war die Entfernung von Copilot und die Suche nach einem
geeigneten KI-Tool für visuelle Workflows (Mascot/Logo-Serie R+MUNI Esel)
sowie Dokumentenkonsolidierung.

Was ist der gewünschte Zielzustand?
Klare Entscheidungsgrundlage: Welche KI-Tools eignen sich für welche
R+MUNI-Usecases — differenziert nach Usecase, nicht pauschal.

Warum jetzt noch nicht abgeschlossen?
Exploration wurde nach zwei Sessions abgebrochen (Frustlevel, fehlende
Ergebnisse im Haupt-Usecase). Textverarbeitungs-Usecase zeigte Potential
und erfordert separate Bewertung. SVG/Bild-Usecase klar negativ bewertet.


================================================================================
2. EVALUATIONSERGEBNISSE
================================================================================

2.1 Usecase: Visueller Workflow (Logo/PNG/SVG — Mascot Esel)
-------------------------------------------------------------
Ergebnis: NEGATIV — nicht empfohlen

Beobachtete Probleme:
  - Arbeitsregeln werden nicht stabil eingehalten — Rückfall in
    Standardverhalten nach kurzer Zeit
  - Visuelle Entscheidungen ohne Bildvorlage trotz expliziter Regel
  - Referenzbild wird nicht konsequent genutzt — Stil und Proportionen
    driften, neue Figuren statt Ableitungen vom Original
  - Interpretation statt Ausführung — Annahmen ohne Grundlage
  - Bildgenerierungs-Pipeline (DALL-E) technisch unzuverlässig —
    mehrfach leere Rückmeldungen ohne Fehlermeldung
  - Self-Destruct-Check: visueller PNG-Check löst automatisches
    Löschen des Contents aus ohne Korrekturschleife
  - SVG-Centerprobleme persistent über mehrere Aufbauversuche (3x)
  - Projektverwaltung: SVG als Quelldatei in Projekt hinterlegen
    nicht möglich — vorgeschlagene Fehlerbehebung schlägt fehl
  - Korrekturversuche verschlechtern Ergebnis statt es zu verbessern
  - Stimmungslage der Schreibweise beeinflusst Modellverhalten stark
  - Zusätzlicher Steuerungsaufwand macht Workflow langsamer
  - 2h Kalibrierungsaufwand für ursprünglich geplante schnelle
    visuelle Ideensammlung

Vergleich Copilot:
  Copilot liefert in diesem Usecase bessere Ergebnisse.
  ChatGPT SVG/PNG-Workflow ist als Marketing-Feature zu werten.

2.2 Usecase: Dokumentenkonsolidierung (Rosetta Stone / .md-Quellen)
--------------------------------------------------------------------
Ergebnis: POSITIV — weiteres Testing empfohlen

Beobachtungen:
  - Rosetta Stone Dokumente (.md) als Quellen geladen und zu
    Master-Konzept konsolidiert — nach 3–4 Kalibrierungen brauchbar
  - Sprachglättung besser als erwartet
  - Kein Neustart erforderlich für brauchbares Ergebnis
  - Sweetspot identifiziert: Textverarbeitung und
    Dokumentenkonsolidierung aus strukturierten Quellen

2.3 Desktop App — Technische Probleme
--------------------------------------
  - MFA-Aktivierung bei GitHub-Nutzung erforderlich (unerwartet /
    Datenschutzbedenken)
  - Installer nur über Microsoft Store verfügbar
  - Web-Nutzung als Alternative empfohlen (intern von ChatGPT)
  - Anmeldefenster triggert Passkey-Dialog mehrfach trotz Abbruch
  - Domain-Verifizierung erforderlich bei Profil-Domain-Eintrag
  - Voice-Funktion deaktiviert
  - Skills/Custom Instructions: Vorschläge von ChatGPT zur
    Personalisierung waren kontraproduktiv
  - Referenzbild-Hinterlegung in Personalisierung fehlgeschlagen —
    Modell ignoriert Einstellung nach mehrfacher Korrektur
  - Ein Chat lief in Dauerschleife (blaues Rad) ohne Auflösung
  - Lokale Daten nach Session-Reset gelöscht — Vermutung: Services
    waren offline (keine Transparenz seitens ChatGPT)

2.4 Allgemeines Modellverhalten
--------------------------------
  - Modell reagiert stark auf Stimmungslage der Schreibweise —
    frustrierte Schreibweise macht Modell zunehmend vorsichtiger
  - Lange Erklärungen statt kurzer Iterationen
  - Fehlermanagement: Fehler werden erklärt statt automatisch
    wiederholt
  - Keine Transparenz bei technischen Störungen
  - Native Selbstanalyse des Modells (Drift-Erklärung) war ehrlich
    und strukturiert — positiv auffällig


================================================================================
3. SCOPE WEITERES TESTING
================================================================================

Was gehört dazu:
  - Dokumentenkonsolidierung aus .md-Quellen vertiefen
  - 30-Tage-Testzeitraum für ASC-Kundensetup-Erfahrungen nutzen
  - Strukturierten Vergleich ChatGPT vs. Copilot für Textusecases

Was gehört explizit nicht dazu:
  - SVG/PNG/Logo-Workflow — negativ bewertet, kein weiteres Testing
  - DALL-E Bildgenerierung — kein R+MUNI Usecase
  - Desktop App — Web-Nutzung bevorzugt


================================================================================
4. VORAUSSETZUNGEN FÜR FORTSETZUNG
================================================================================

  - Frustlevel neutral (explizite EUMAXL-Entscheidung)
  - Klarer Usecase-Fokus definiert vor Session-Start
  - Kein visueller Workflow — nur Text/Dokument-Usecases


================================================================================
5. OFFENE FRAGEN
================================================================================

| Frage                                          | Wer klärt | Bis wann |
|------------------------------------------------|-----------|----------|
| ChatGPT Textkonsolidierung für R+MUNI formal   | EUMAXL    | offen    |
| tauglich? (separater Test)                     |           |          |
| ASC-Erfahrungen aus 30-Tage-Test dokumentieren | EUMAXL    | offen    |
| Tool-Entscheidung: ChatGPT / Copilot / beide   | EUMAXL    | offen    |
| O365 ADDON Evaluation (formal noch offen)      | EUMAXL    | offen    |


================================================================================
ASSOCIATE_Backlog_ChatGPT_Evaluation | ASSOCIATE | S8 | 2026-03-28 | R+MUNI Blueprint
================================================================================
