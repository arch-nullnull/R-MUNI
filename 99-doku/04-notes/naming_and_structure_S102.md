================================================================================
NAMING AND STRUCTURE — R+MUNI BLUEPRINT
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : naming_and_structure_S102
Tag             : #naming #structure #ablage #s101 #global
Datum           : 2026-03-31
Stage           : S1.02 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Ablageort       : C:\Prototyping\R+MUNI Doku\R+MUNI Doku-internal\04-notes\naming_and_structure_S102.md
Erstellt durch  : EUMAXL + Claude (Pair-Session)
Letzte Änderung : 2026-04-01 — Kap. 1 Rollenprefix EXP/ASC/MGT neu, Kap. 3 Pendant-Logik erweitert, Kap. 4 Varianten-Kürzel ab S102 neu | Freigabe: EUMAXL
================================================================================


================================================================================
ZWECK DIESES DOKUMENTS
================================================================================

Dieses Dokument ist die Single Source of Truth für Namenskonventionen
und Ablagestruktur aller R+MUNI Dokumente und Templates.

Es gilt rollenübergreifend — DEV, ASSOCIATE, und künftige Rollen (ELITE, MGT).
Splitting in rollenspezifische Varianten erfolgt nur wenn der Umfang es erfordert.

Dieses Dokument ersetzt keine operativen Anleitungen (How2) und
keine normativen Regeln (GOV). Es beschreibt die Struktur — nicht den Prozess.


================================================================================
1. SUFFIX-LOGIK UND STAGE-HERKUNFT
================================================================================

Jedes R+MUNI Dokument trägt einen Stage-Suffix. Dieser macht die
Herkunft und den Reifestand eines Dokuments direkt lesbar.

  _S101        Stage 1.01 — aktueller Standard
  _S8          Stage 8 — letzter stabiler Pre-S101-Stand (Freeze 8)
  _S7, _S6     ältere Stände — read-only, kein Eingriff

Grundregel: Suffix nie weglassen. Ohne Suffix ist kein Versionskontext erkennbar.

Letzter stabiler Stand (Ausgangspunkt S101):
  Freeze 8 / R1 — gilt für ASSOCIATE wie DEV (intern wie extern).
  1.01-Freeze steht noch aus.

  Der R+MUNI Sync-Prefix (R-MUNI-) bleibt über alle Stages konstant —
  er ist kein Stage-Artefakt sondern ein Infrastruktur-Merkmal.
  Sync-Fixierung für S101 steht noch aus.

Rollenprefix-Logik:
  Kein Rollenprefix  = rollenübergreifend (z.B. dieses Dokument)
  _DEV_              = nur DEV-Kontext (z.B. how2_DEV_Template_S101.md)
  _EXP_              = Expert-Variante — neu ab S102 (kein DEV-Anteil, Prinzip + Verhalten)
  _ASC_              = Associate-Variante — Kürzel neu ab S102 (vorher kein expliziter Prefix)
  _MGT_              = MGT-Variante — Platzhalter, noch nicht aktiv

Beispiele:
  principles_Template_S101.md              rollenübergreifend
  how2_DEV_Template_S101.md                DEV-spezifisch
  AI_DRIVEN_DEV_METHODE_EXP_S102.md        Expert-Variante (neu ab S102)
  AI_DRIVEN_DEV_METHODE_ASC_S102.md        Associate-Variante (Kürzel neu ab S102)
  BETA_OFFBOARDING_How2_DEV_S101.md        DEV-spezifisch mit Prozessbezug
  naming_and_structure_S101.md             rollenübergreifend (dieses Dokument)


================================================================================
2. ABLAGESTRUKTUR — ÜBERSICHT
================================================================================

── 2.1 ROOT-EBENE ───────────────────────────────────────────────────────────────

Wurzel: C:\Prototyping\

  R+MUNI\              Produktiv-Repo — Modell, Skripte, Artefakte (Public Repo)
  R+MUNI Apps\         Eigenständige Applikationen rund um R+MUNI
  R+MUNI Archiv\       Archivierte Stände und ZIP-Snapshots
  R+MUNI Custo\        Kundenspezifische Anpassungen
  R+MUNI DEV\          DEV-Arbeitsumgebung (nicht publiziert)
  R+MUNI Doku\         Dokumentation — enthält internal und public (siehe 2.2/2.3)
  R+MUNI Installer\    Installationspakete
  R+MUNI Norm\         Normen, Standards, Referenzdokumente (ISO, TOGAF etc.)
  R+MUNI TEMP\         Temporäre Arbeitsdateien


── 2.2 R+MUNI DOKU-INTERNAL ─────────────────────────────────────────────────────

Pfad: C:\Prototyping\R+MUNI Doku\R+MUNI Doku-internal\

DEV-interne Dokumentation — nicht publiziert, kein Public-Repo-Push.
Templates, Freeze-Dokumente und Referenzdokumente liegen in 04-notes.

  00-governance\       GOV-Dokumente, Methodik (Global GOV, AI Driven Dev)
  01-principles\       Principles je Thema (DEV + ASSOCIATE Varianten)
  02-how2\             How2-Anleitungen je Thema (DEV + ASSOCIATE Varianten)
  03-roesetta_stone\   Framework-Mappings (ArchiMate, TOGAF) — Tippfehler im
                       echten Ordnernamen, wird so belassen
  04-notes\            Templates, Freeze-Dokumente, Konzepte, Stage-Ziele,
                       Backlog-Roheinträge, dieses Dokument
  05-backlog\          Backlog-Einträge (nicht gestartete Themen)
  06-sprints\          Sprint-DEV-Dokus — aktuelle und historische Sprints,
                       je Stage in Unterordner
  07-creative\         Kreative Artefakte — MUNI Bildmaterial, SVGs, Assets
  99-infocfg\          Konfigurationsdateien, Mappings, Cheat Sheets


── 2.3 R+MUNI DOKU-PUBLIC ───────────────────────────────────────────────────────

Pfad: C:\Prototyping\R+MUNI Doku\R+MUNI Doku-public\

Öffentliche Dokumentation — GitHub-Repo R-MUNI-Doku-public.
Spiegelt den publizierten Stand für ASSOCIATE und DEV (soweit freigegeben).

  00-governance\       GOV-Dokumente (publizierte Varianten)
  01-principles\       Principles je Thema (publizierte Varianten)
  02-how2\             How2-Anleitungen je Thema (publizierte Varianten)
  03-roesetta_stone\   Framework-Mappings (publizierte Varianten)
  04-notes\            Templates und Referenzdokumente (publizierte Varianten)


── 2.4 R+MUNI (PUBLIC REPO) ─────────────────────────────────────────────────────

Pfad: C:\Prototyping\R+MUNI\

Produktiv-Repo — GitHub-Repo R-MUNI. Enthält Modell, Skripte, Artefakte
und eine eingebettete Doku-Struktur (99-doku) als ASSOCIATE-Spiegel.

  00-model\            EA-Modelle — ArchiMate (aktiv + Archiv), BPMN, xyvision
  01-artifacts\        XML-Artefakte, Python-Skripte, jArchi-Skripte
  02-stages\           Stage-Archive (ArchiMate, BPMN, xy) und Logs
  99-doku\             Eingebettete Dokumentation (ASSOCIATE-Spiegel)
    00-governance\     GOV-Dokumente (publizierter Stand)
    01-principles\     Principles je Thema (ASSOCIATE-Varianten)
    02-how2\           How2-Anleitungen je Thema (ASSOCIATE-Varianten)
    03-roesetta_stone\ Framework-Mappings (publizierter Stand)
    04-notes\          Templates, Freeze, Stage-Ziele
    05-backlog\        Backlog (publizierter Stand)
    06-sprints\        Sprint-Dokus (publizierter Stand)
    07-creative\       Assets — Flipchart-Fotos, Bilder, SVGs, Logos


================================================================================
3. PENDANT-LOGIK DEV / ASSOCIATE
================================================================================

DEV- und ASSOCIATE-Varianten eines Dokumenttyps liegen im selben Ordner.
Der Suffix trennt die Welten — nicht der Ordner.

Schema:
  <Dokumentname>_DEV_S102.md           DEV-Variante
  <Dokumentname>_EXP_S102.md           Expert-Variante (neu ab S102)
  <Dokumentname>_ASC_S102.md           Associate-Variante (Kürzel neu ab S102)
  <Dokumentname>_MGT_S102.md           MGT-Variante (Platzhalter — noch nicht aktiv)

Beispiele:
  how2_DEV_Template_S101.md            DEV
  TMP_How2_Associate_S8.md             ASSOCIATE (S8-Stand, Kürzel noch alt)

  BETA_OFFBOARDING_How2_DEV_S101.md        DEV
  BETA_OFFBOARDING_principles_DEV_S101.md  DEV

Grundregel: ASSOCIATE-Dokumente werden nie aus DEV-Dokumenten abgeleitet
            (Entkernungslogik ist abgeschafft ab S101).
            DEV-, EXP- und ASC-Varianten entstehen parallel — unabhängig.

Renaming-Regel: ASC-Kürzel wird beim nächsten Editieren eines bestehenden
                ASSOCIATE-Dokuments eingeführt — kein forciertes Bulk-Renaming.


================================================================================
4. VARIANTEN-KÜRZEL — GÜLTIG AB STAGE 1.02
================================================================================

Ab Stage 1.02 gelten vier offizielle Varianten-Kürzel für alle R+MUNI Dokumente.

  DEV    Development       Interne Arbeitsgrundlage — EUMAXL + Claude Sparring.
                           Hart, fair, vollständig, GOV-konform.
                           Kürzel unverändert — war bereits etabliert.

  EXP    Expert            Externe Expert-Variante — neu ab S102.
                           Ableitung aus DEV-Prinzipien und -Verhalten,
                           ohne DEV-Anteil. Für erfahrene externe Nutzer.

  ASC    Associate         Bisherige ASSOCIATE-Variante — Kürzel neu ab S102.
                           Renaming erfolgt beim nächsten Editieren,
                           kein forciertes Bulk-Renaming.

  MGT    Management        Platzhalter — noch nicht aktiv.
                           ChatGPT/Copilot-Prompt-Variante ohne Folder/Files.
                           Eigener Sprint wenn Phase gestartet wird.

Dateinamen-Schema ab S102:
  <Dokumentname>_DEV_S102.md
  <Dokumentname>_EXP_S102.md
  <Dokumentname>_ASC_S102.md
  <Dokumentname>_MGT_S102.md   (noch nicht aktiv)

Übergangsregel:
  Bestehende _DEV_S101 Dokumente bleiben unverändert bis zum nächsten Editieren.
  Bestehende ASSOCIATE-Dokumente ohne _ASC_ Kürzel bleiben bis zum nächsten Editieren.
  Kein Zwang zur sofortigen Umbenennung — Kontinuität vor Perfektion.


================================================================================
5. NAMENSKONVENTION R-MUNI VS. R+MUNI
================================================================================

⚠ NOCH NICHT VOLLSTÄNDIG FIXIERT — siehe Backlog

Hintergrund:
GitHub unterstützt kein +-Zeichen in Ordnernamen. Dadurch entsteht
automatisch eine visuelle Unterscheidung zwischen Sync-Umgebung und
echter Kundeninstallation:

  R-MUNI-<Kürzel>    GitHub-Sync-Umgebung (DEV-intern)
  R+MUNI <Kürzel>    echte Kundeninstallation (lokal beim Kunden)

Diese Konvention ist über alle Kontexte noch nicht abschließend validiert.
Eine vollständige Fixierung erfolgt nach weiteren Beta-Kunden-Durchläufen.

Verweis: [[BACKLOG_Namenskonvention-GitHub-Sync_DEV_S101]]


================================================================================
BEZÜGE
================================================================================

[[Global_GOV_DEV_S101]]                      Normative Grundlage
[[AI_DRIVEN_DEV_METHODE_DEV_S102]]           Methodik und Rollenkontext
[[FREEZE_101]]                               Letzter stabiler Stand
[[BACKLOG_Namenskonvention-GitHub-Sync_DEV_S101]]  Offene Namenskonvention
[[Sprint-DEV-S101-DEV-TMPL-RESYNC]]          Entstehungskontext dieses Dokuments


================================================================================
naming_and_structure_S102 | 2026-04-01
R+MUNI Blueprint | Stage 1.02 | Erstellt: EUMAXL + Claude (Pair-Session)
Letzte Änderung: 2026-04-01 — Varianten-Kürzel DEV/EXP/ASC/MGT definiert
================================================================================
