================================================================================
ROSETTA STONE – R+MUNI
Block 8: Stage 8 – Beta 1.0 | Außenwirkung & Abschluss
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : Rosetta-Stone_Stage8_S8
Zweck           : Mapping der in Stage 8 eingeführten und konsolidierten
                  R+MUNI Konzepte auf TOGAF ADM und ArchiMate 3.2
Erstellt        : 2026-03-28
Stage           : S8 – ABGESCHLOSSEN / FREEZE-8 BESTÄTIGT
Ablageort       : R+MUNI Doku-public\03-rosetta_stone\Rosetta-Stone_Stage8_S8.md
Erstellt durch  : EUMAXL + Claude (Pair-Session, Stage-Abschluss)
================================================================================


================================================================================
EINLEITUNG
================================================================================

Dieses Dokument mappt R+MUNI interne Konzepte aus Stage 8 (Beta 1.0 |
Außenwirkung & Abschluss) auf die offizielle Terminologie von TOGAF ADM und
ArchiMate 3.2.

Ziel-Framework:   TOGAF ADM + ArchiMate 3.2 (dual)
R+MUNI Kontext:   Beta 1.0 Release, Repo-Restrukturierung, Associate-Migration,
                  Außenwirkung und Übergabe in Produktivbetrieb
ADM Phase:        Preliminary + Phase A + Phase D + Phase F + Phase G + Phase H

Stage 8 ist der letzte Beta-Stage. Er führt keine neuen technischen
Kernreihen ein — er konsolidiert das System für die erste echte Außenwirkung.
Schwerpunkte: Release-Vorbereitung, Zielgruppen-Terminologie, Repo-Trennung
und Übergang in den Produktivbetrieb (Stage 1 neue Zählung).

Dieses Mapping:
  - dient der Einordnung der Stage-8-Erkenntnisse in etablierte EA-Frameworks
  - macht R+MUNI-interne Konzepte für framework-basierte Kommunikation nutzbar
  - zeigt wo R+MUNI bewusst vom Framework abweicht — und warum das legitim ist
  - ist Abschlussdokumentation des gesamten Beta-Zyklus (Stages 1–8)

Thematische Blöcke dieses Dokuments:
  Block 8A  Release-Konzepte         (Beta 1.0, Versionsbezeichnung, GitHub Release)
  Block 8B  Zielgruppen-Terminologie (Associate, DEV-Rollentrennung, USER-Migration)
  Block 8C  Repo-Architektur         (Zwei-Repo-Modell, History-Reset, .gitignore)
  Block 8D  Außenwirkung             (README, Install.txt, Außenperspektive)
  Block 8E  Übergang Produktivbetrieb (Stage 1, Rückkopplungsschutz, Freeze-8)


================================================================================
BLOCK 8A — RELEASE-KONZEPTE
================================================================================


--------------------------------------------------------------------------------
8A00 – BETA 1.0 RELEASE
--------------------------------------------------------------------------------
Intention:
  Beta 1.0 ist der erste nach außen kommunizierbare, download-fähige Stand
  von R+MUNI. Er markiert den Übergang von geschütztem Entwicklungsbetrieb
  zur echten Außenwelt. Beta 1.0 ist kein Feature-Release — er ist der
  erste Moment wo das System auf Augen trifft die nicht im inneren Kreis sind.

Norm-Begriff:
  Architecture Release (TOGAF ADM — Phase F/G)

Ergänzende Norm-Konzepte:
  Transition Architecture (TOGAF — Phase F)
  Deployed Architecture (TOGAF — Phase G)
  Release Point (ArchiMate 3.2 — Implementation & Migration Viewpoint)

TOGAF ADM Einordnung:
  Phase F (Migration Planning) definiert Transition Architectures als
  Zwischenstände auf dem Weg zur Target Architecture. Der R+MUNI Beta-1.0-
  Release ist genau das: ein validierter Zwischenstand — vollständig,
  kommunizierbar, aber noch nicht Produktivbetrieb. Phase G (Implementation
  Governance) begleitet den ersten echten Einsatz durch externe Nutzer.

Rosetta:
  "Beta 1.0 Release"                 →  Architecture Release (Phase F/G)
  "Download-fähiges Paket"           →  Deployable Architecture Package
  "Erster externer Betakunde"        →  Pilot Implementation (Phase G)
  "GitHub Release v1.0-beta"         →  Release Baseline / Tagged Version
  "Tag: v1.0-beta"                   →  Release Identifier (ArchiMate)

Bewertung:
  Sehr gutes Mapping. TOGAF unterscheidet klar zwischen Transition Architecture
  (Zwischenstand) und Target Architecture (Zielzustand) — Beta 1.0 ist exakt
  eine Transition Architecture. Die Ehrlichkeit des "Beta"-Tags entspricht
  TOGAF-Werten: ein Release benennt seinen Reifegrad explizit.
  TOGAF würde formal einen Architecture Definition Document fordern —
  R+MUNI liefert das durch README + Sprint-DEV-Doku-Kombination.


--------------------------------------------------------------------------------
8A01 – VERSIONSBEZEICHNUNG (DEV VS. RELEASE)
--------------------------------------------------------------------------------
Intention:
  Stage 8 führt eine explizite Trennung der Versionsbezeichnungen ein:
  Die DEV-Welt spricht von "Stage 8 / S8" — die Außenwelt sieht
  "R+MUNI BETA 1.0" mit Tag v1.0-beta. Beide Bezeichnungen sind korrekt —
  sie adressieren unterschiedliche Zielgruppen mit unterschiedlichem Kontext.

Norm-Begriff:
  Architecture Version Control (TOGAF — Architecture Repository)

Ergänzende Norm-Konzepte:
  Release Identifier (ArchiMate 3.2)
  Baseline Identification (TOGAF — Configuration Management)

TOGAF ADM Einordnung:
  TOGAF Architecture Repository erfordert klare Versionskennzeichnung aller
  Architekturdokumente. Die Zweiteilung DEV-Version / Release-Version ist
  eine bewusste Stakeholder-Segmentierung: interne Entwicklungsrealität vs.
  externe Kommunizierbarkeit. Beide müssen konsistent und nachvollziehbar sein.

Rosetta:
  "S8 / Stage 8"                     →  Internal Development Version
  "R+MUNI BETA 1.0"                  →  External Release Designation
  "Tag: v1.0-beta"                   →  Formal Release Identifier (Git Tag)
  "_S8-Suffix (DEV-Dokumente)"       →  Version Tag (Architecture Repository)
  "Kein Suffix (Public-Dokumente)"   →  Release-Ready Artifact (stakeholder-facing)

Bewertung:
  Elegante Lösung. TOGAF empfiehlt Versionsmanagement — die R+MUNI Umsetzung
  geht weiter: sie trennt Versions-Sprache nach Zielgruppe. Das ist operational
  klüger als TOGAF-Standardempfehlungen und für ein öffentliches Projekt
  praktisch notwendig. Keine Abweichung von TOGAF-Werten — nur Erweiterung.


================================================================================
ZUSAMMENFASSUNG BLOCK 8A
================================================================================

Release-Konzepte Mapping Gesamt:

  "Beta 1.0 Release"           →  Architecture Release (Phase F/G)         ✅
  "GitHub Release v1.0-beta"   →  Release Baseline / Tagged Version         ✅
  "Tag: v1.0-beta"             →  Release Identifier                        ✅
  "S8 vs. BETA 1.0"           →  Internal vs. External Version              ✅
  "_S8-Suffix"                 →  Version Tag (Architecture Repository)     ✅

Kernverständnis:
  TOGAF fragt nicht: "Wie nennen wir den Release intern vs. extern?"
  Sondern: "Wie wird der Versionsstand für alle relevanten Stakeholder
  transparent und konsistent kommuniziert?"
  R+MUNI beantwortet das mit einer klaren Zweiteilung — DEV-Sprache für
  interne Nachvollziehbarkeit, Release-Sprache für externe Kommunizierbarkeit.

Gesamtbewertung:
  Hohe Konformität. Beta 1.0 entspricht dem TOGAF Transition Architecture
  Konzept sehr gut. Die Versionsbezeichnungs-Trennung ist eine pragmatische
  Erweiterung die TOGAF nicht explizit fordert — aber empfehlen würde.

Nächster Block:
  Block 8B — Zielgruppen-Terminologie


================================================================================
BLOCK 8B — ZIELGRUPPEN-TERMINOLOGIE
================================================================================


--------------------------------------------------------------------------------
8B00 – ASSOCIATE ALS DEFINIERTE ZIELGRUPPE
--------------------------------------------------------------------------------
Intention:
  "Associate" ist der in Stage 8 konsequent eingeführte Begriff für
  Endanwender von R+MUNI ohne technisches Vorwissen. Er ersetzt den
  unschärferen internen Begriff "USER" und ist nach außen kommunizierbar.
  Associate ist keine Rolle im klassischen Sinne — es ist eine Zielgruppen-
  Bezeichnung die Erwartungen, Betreuungsintensität und Dokumentationstiefe
  definiert. Ein Associate versteht das System — ohne zu wissen wie es gebaut ist.

Norm-Begriff:
  Architecture User (TOGAF — Stakeholder Management, Phase A)

Ergänzende Norm-Konzepte:
  Stakeholder (TOGAF — Preliminary Phase)
  Architecture Consumer (TOGAF — Phase G)
  Business Actor (ArchiMate 3.2 — Motivation Aspect)

TOGAF ADM Einordnung:
  TOGAF Preliminary Phase definiert Stakeholder-Kategorien und ihre
  Beziehung zur Architektur. Phase A verlangt einen Stakeholder Management-
  Ansatz. Der R+MUNI Associate entspricht dem TOGAF Architecture User —
  jemandem der die Architektur nutzt ohne sie zu entwickeln. Phase G
  (Implementation Governance) stellt sicher dass Architecture Users
  das System korrekt anwenden können — das entspricht dem R+MUNI
  Anspruch dass ein Associate selbstständig onboarden kann.

Rosetta:
  "Associate"                        →  Architecture User / Stakeholder
  "Associate-Dokumentation"          →  Stakeholder-Viewpoint Document
  "Associate kann selbst onboarden"  →  Architecture Consumer (Phase G)
  "Kein technisches Vorwissen nötig" →  Non-Technical Stakeholder Profile
  "_Associate-Suffix (Dokumente)"    →  Stakeholder-Targeted Artifact

Bewertung:
  Sehr hohe Konformität. TOGAF Stakeholder-Konzept ist funktional äquivalent
  zum R+MUNI Associate. Abweichung: TOGAF bleibt bei "Stakeholder" generisch —
  R+MUNI präzisiert auf eine konkrete Zielgruppe mit definierten Erwartungen.
  Diese Präzisierung ist eine Verbesserung gegenüber TOGAF-Standard.


--------------------------------------------------------------------------------
8B01 – USER → ASSOCIATE MIGRATION
--------------------------------------------------------------------------------
Intention:
  Stage 8 führt eine vollständige terminologische Migration durch:
  "USER" (intern, unscharf) wird in allen Dokumenten, Templates und
  Referenzen durch "Associate" ersetzt. Dies ist kein kosmetischer Eingriff —
  es ist eine Präzisierung der Zielgruppen-Sprache die nach außen trägt.

Norm-Begriff:
  Architecture Communication Plan Update (TOGAF — Phase H)

Ergänzende Norm-Konzepte:
  Terminology Governance (TOGAF — Architecture Principles)
  Controlled Vocabulary (TOGAF — Architecture Repository)

TOGAF ADM Einordnung:
  Phase H (Architecture Change Management) verwaltet terminologische und
  konzeptuelle Updates an bestehenden Architekturdokumenten. Eine Migration
  von "USER" zu "Associate" ist genau das: eine kontrollierte, vollständige
  Terminologie-Aktualisierung mit klarer Begründung und nachvollziehbarer
  Durchführung.

Rosetta:
  "USER → Associate Migration"        →  Controlled Terminology Update (Phase H)
  "Alle Dokumente betroffen"          →  System-wide Terminology Governance
  "Begründung: extern kommunizierbar" →  Stakeholder Communication Rationale
  "Sprint-dokumentiert"               →  Change Management Record

Bewertung:
  Gutes Mapping. TOGAF sieht terminologische Konsistenz als Governance-
  Aufgabe. R+MUNI erfüllt das mit einem expliziten Sprint der die Migration
  vollständig und nachvollziehbar durchführt. Besonders stark: die
  Begründung ist explizit festgehalten (extern kommunizierbar, klar abgegrenzt).


--------------------------------------------------------------------------------
8B02 – ASSOCIATE + DEV VARIANTEN PRO REIHE
--------------------------------------------------------------------------------
Intention:
  Jede Dokumentreihe erhält in Stage 8 explizit zwei Varianten:
  eine DEV-Variante (vollständig, technisch) und eine Associate-Variante
  (zielgruppengerecht, ohne DEV-Overhead). Inhalt ist in S8 vorerst ident —
  die inhaltliche Trennung ist Stage-1-Arbeit. Der Akt des Anlegens
  der Associate-Varianten schließt den blinden Fleck: ab S8 existiert
  für jede Reihe eine adressierbare Associate-Perspektive.

Norm-Begriff:
  Architecture Viewpoint (TOGAF — Phase A)

Ergänzende Norm-Konzepte:
  Stakeholder View (TOGAF — Views and Viewpoints)
  Audience-Specific Documentation (TOGAF — Communication Plan)

TOGAF ADM Einordnung:
  TOGAF unterscheidet Viewpoints (generische Perspektiven) von Views
  (konkrete Darstellungen für einen Stakeholder). Jede Reihe mit DEV +
  Associate Variante entspricht diesem Schema: DEV-Sicht für technische
  Stakeholder, Associate-Sicht für Architecture Users. Phase A definiert
  welche Viewpoints für welche Stakeholder relevant sind.

Rosetta:
  "DEV-Variante"                     →  Architecture View (Technical Stakeholder)
  "Associate-Variante"               →  Architecture View (Non-Technical Stakeholder)
  "Inhalt vorerst ident — Trennung S1" →  Deferred Viewpoint Differentiation
  "Alle Reihen betroffen"            →  Complete Viewpoint Coverage

Bewertung:
  Sehr gutes Mapping auf TOGAF Views und Viewpoints. Die Entscheidung,
  die Varianten in S8 anzulegen und die Differenzierung auf Stage 1
  zu verschieben, ist pragmatisch und GOV-konform. TOGAF würde das als
  korrektes iteratives Vorgehen anerkennen: Struktur zuerst, Inhalt folgt.


================================================================================
ZUSAMMENFASSUNG BLOCK 8B
================================================================================

Zielgruppen-Terminologie Mapping Gesamt:

  "Associate"                →  Architecture User / Stakeholder               ✅
  "Associate-Dokumentation"  →  Stakeholder-Targeted Artifact                 ✅
  "USER → Associate"         →  Controlled Terminology Update (Phase H)       ✅
  "DEV-Variante"             →  Architecture View (Technical)                  ✅
  "Associate-Variante"       →  Architecture View (Non-Technical)              ✅

Kernverständnis:
  TOGAF fragt nicht: "Wie nennen wir unsere Endanwender?"
  Sondern: "Welche Stakeholder-Perspektiven müssen durch Viewpoints und Views
  abgedeckt sein — und welche Dokumentation erreicht jeden Stakeholder?"
  R+MUNI beantwortet das mit präziser Terminologie (Associate) und
  strukturierter Doppel-Variante pro Reihe.

Gesamtbewertung:
  Hohe Konformität. Die Associate-Einführung ist methodisch stärker als
  ein generisches TOGAF-Stakeholder-Label — sie definiert eine Zielgruppe
  mit konkreten Erwartungen und zieht das durch alle Dokumente konsequent durch.

Nächster Block:
  Block 8C — Repo-Architektur


================================================================================
BLOCK 8C — REPO-ARCHITEKTUR
================================================================================


--------------------------------------------------------------------------------
8C00 – ZWEI-REPO-MODELL
--------------------------------------------------------------------------------
Intention:
  Ab Beta 1.0 existieren zwei getrennte Git-Repositories:
  Public Repo (Release-Stand, extern sichtbar) und DEV Repo (privat,
  vollständige Entwicklungsrealität). Entwicklung findet ausschließlich
  im DEV Repo statt. Fertige Stände werden manuell von DEV nach Public
  übertragen. Die GitHub-URL des Public Repo bleibt unverändert —
  externe Links bleiben gültig.

Norm-Begriff:
  Architecture Repository Partitioning (TOGAF — Architecture Repository)

Ergänzende Norm-Konzepte:
  Federated Architecture Repository (TOGAF)
  Architecture Partition (TOGAF — Preliminary Phase)
  Technology Portfolio (ArchiMate 3.2 — Technology Layer)

TOGAF ADM Einordnung:
  TOGAF Architecture Repository kann partitioniert werden — öffentliche
  Teile für Stakeholder-Kommunikation, interne Teile für Entwicklungsarbeit.
  Das R+MUNI Zwei-Repo-Modell ist die operative Umsetzung: Public Repo =
  Stakeholder-Partition, DEV Repo = Development Partition. TOGAF empfiehlt
  diese Trennung explizit wenn sensitive Entwicklungsinhalte von
  kommunizierbaren Artefakten getrennt werden müssen.

Rosetta:
  "Public Repo (Release)"            →  Architecture Repository (Public Partition)
  "DEV Repo (privat)"                →  Architecture Repository (Development Partition)
  "Manueller Transfer DEV → Public"  →  Controlled Release Process
  "GitHub-URL bleibt gleich"         →  Architecture Repository Stability
  "Zwei-Repo-Modell"                 →  Federated Architecture Repository

Bewertung:
  Sehr hohe Konformität. Das Zwei-Repo-Modell entspricht dem TOGAF-Konzept
  einer federierten Architecture Repository-Landschaft sehr gut. Stärke:
  die Entscheidung für URL-Stabilität des Public Repo schützt externe
  Referenzen — das ist ein TOGAF-konformes Denken in Stakeholder-Abhängigkeiten.


--------------------------------------------------------------------------------
8C01 – HISTORY-RESET VIA ORPHAN BRANCH
--------------------------------------------------------------------------------
Intention:
  Das Public Repo enthielt in seiner Git-History Inhalte die nicht hätten
  veröffentlicht werden sollen (Modell-Dateien, Example Scripts). Diese
  sind technisch abrufbar auch wenn die Dateien längst entfernt wurden.
  Der History-Reset via orphan branch entfernt die alte History vollständig
  und setzt einen sauberen Initialcommit = Beta 1.0 Stand.
  Das DEV Repo trägt die vollständige alte History weiter.

Norm-Begriff:
  Architecture Repository Baseline Reset (TOGAF — Architecture Repository)

Ergänzende Norm-Konzepte:
  Baseline Architecture (TOGAF — Phase A/H)
  Configuration Cleanup (TOGAF — Configuration Management)

TOGAF ADM Einordnung:
  TOGAF Configuration Management (Phase H) schreibt vor dass Architecture
  Repositories korrekte und vollständige Inhalte enthalten. Ein bewusster
  Baseline-Reset der unbeabsichtigt veröffentlichte Inhalte entfernt ist
  ein legitimer Configuration Management-Akt — mit klarer Begründung und
  Sicherung im DEV Repo.

Rosetta:
  "Orphan branch History-Reset"      →  Architecture Repository Baseline Reset
  "Sauberer Initialcommit = Beta 1.0" →  New Baseline Establishment
  "DEV Repo trägt alte History"      →  Baseline History Preservation (internal)
  "Force Push nach Reset"            →  Controlled Repository Override

Bewertung:
  Gut abbildbar. Der technische Weg (orphan branch, force push) hat kein
  direktes TOGAF-Pendant — TOGAF spricht nicht über Git-Operationen.
  Konzeptuell jedoch vollständig konform: unbeabsichtigt veröffentlichte
  Inhalte zu entfernen und eine saubere Baseline zu setzen ist
  Configuration Management in TOGAF-Sinne.


--------------------------------------------------------------------------------
8C02 – BEWUSST GEBAUTE .GITIGNORE
--------------------------------------------------------------------------------
Intention:
  Beide Repos erhalten eine neue, bewusst gebaute .gitignore die der
  Blueprint-Ordnerstruktur folgt. Die bisherige .gitignore war organisch
  gewachsen und generisch — kein klares Bild welche Inhalte ein- oder
  ausgeblendet sind. Die neue .gitignore ist ein versioniertes Blueprint-
  Artefakt mit zwei Varianten: PUBLIC (strikt) und DEV (Modelle erlaubt).

Norm-Begriff:
  Architecture Content Framework (TOGAF — Architecture Repository)

Ergänzende Norm-Konzepte:
  Artifact Governance (TOGAF — Preliminary Phase)
  Content Boundary Definition (TOGAF)

TOGAF ADM Einordnung:
  TOGAF Architecture Content Framework definiert welche Artefakte wo
  abgelegt und verwaltet werden. Die .gitignore ist die technische
  Umsetzung dieser Grenze: sie definiert explizit welche Inhalte in
  welchem Repository erscheinen dürfen. Das Erstellen einer bewussten
  .gitignore ist Architecture Content Governance in Git-Sprache.

Rosetta:
  ".gitignore PUBLIC (strikt)"       →  Content Boundary (Public Repository)
  ".gitignore DEV (Modelle erlaubt)" →  Content Boundary (Development Repository)
  "Bewusst gebaut ≠ organisch gewachsen" →  Governance-Driven Content Control
  ".gitignore als Blueprint-Artefakt" →  Versioned Governance Artifact

Bewertung:
  Gut abbildbar. TOGAF hat keine Git-spezifische Entsprechung — aber das
  Prinzip der bewussten Content Boundary-Definition ist TOGAF-Kern.
  Besonders stark: die Erkenntnis dass .gitignore von Anfang an bewusst
  gebaut werden soll wird als Lessons Learned festgehalten.


================================================================================
ZUSAMMENFASSUNG BLOCK 8C
================================================================================

Repo-Architektur Mapping Gesamt:

  "Zwei-Repo-Modell"         →  Federated Architecture Repository             ✅
  "Public Repo"              →  Architecture Repository (Public Partition)     ✅
  "DEV Repo"                 →  Architecture Repository (Dev Partition)        ✅
  "History-Reset"            →  Architecture Repository Baseline Reset         ✅
  ".gitignore bewusst gebaut" →  Governance-Driven Content Boundary            ✅

Kernverständnis:
  TOGAF fragt nicht: "Wie strukturieren wir unsere Git Repositories?"
  Sondern: "Wie wird das Architecture Repository partitioniert, gesichert
  und gepflegt — so dass interne Entwicklungsrealität und externe
  Kommunikation klar getrennt sind?"
  R+MUNI beantwortet das mit dem Zwei-Repo-Modell und bewusster .gitignore.

Gesamtbewertung:
  Hohe Konformität. Die Repo-Architektur-Entscheidungen entsprechen TOGAF
  Architecture Repository-Konzepten sehr gut — auch wenn TOGAF nicht in
  Git-Begriffen denkt. Die Begründungstiefe der Entscheidungen
  (verworfene Alternativen explizit dokumentiert) entspricht TOGAF-Werten.

Nächster Block:
  Block 8D — Außenwirkung


================================================================================
BLOCK 8D — AUSSENWIRKUNG
================================================================================


--------------------------------------------------------------------------------
8D00 – AUSSENPERSPEKTIVE ALS QUALITÄTSKRITERIUM
--------------------------------------------------------------------------------
Intention:
  Stage 8 führt ein neues Qualitätskriterium ein: "Würde das jemand
  verstehen der nicht weiß wie es entstanden ist?" Diese Frage ist der
  Test für alle Inhalte die nach außen gehen. Sie erzwingt einen
  Perspektivwechsel: weg von Insider-Logik, hin zur Lesbarkeit für
  einen Fremden. Stage 8 darf polieren — nicht umbauen.

Norm-Begriff:
  Stakeholder Communication Quality (TOGAF — Phase A / Communication Plan)

Ergänzende Norm-Konzepte:
  Architecture Communication (TOGAF — Preliminary Phase)
  Fitness for Purpose (TOGAF — Architecture Governance)

TOGAF ADM Einordnung:
  Phase A definiert Architecture Communication als explizite Aufgabe:
  Stakeholder müssen die Architektur verstehen können. Das R+MUNI
  Außenperspektive-Kriterium ist die operative Umsetzung: jedes
  nach-außen-gehende Dokument wird gegen die Frage eines
  informierten Fremden getestet — nicht gegen Insider-Wissen.

Rosetta:
  "Außenperspektive als Test"        →  Stakeholder Communication Quality Check
  "Würde ein Fremder das verstehen?" →  Non-Expert Readability Criterion
  "Polieren, nicht umbauen"          →  Scope Discipline (Phase H)
  "Insider-Jargon vermeiden"         →  Controlled Vocabulary (Architecture Communication)

Bewertung:
  Sehr gut abbildbar. TOGAF verlangt stakeholder-gerechte Kommunikation —
  R+MUNI operationalisiert das mit einer konkreten Prüffrage statt einem
  abstrakten Prinzip. Diese Operationalisierung ist stärker als TOGAF-Standard
  und für ein öffentliches Open-Source-Projekt praktisch notwendig.


--------------------------------------------------------------------------------
8D01 – README ALS ERSTE VISITENKARTE
--------------------------------------------------------------------------------
Intention:
  Das README ist in Stage 8 die primäre Außenwirkung von R+MUNI.
  Es beantwortet die Fragen die ein Fremder stellt: Was ist R+MUNI?
  Was kann es? Wie starte ich? Es ist kein technisches Handbuch —
  es ist eine Einladung. Ehrlichkeit über Beta-Status ist Teil
  des Designs (Beta = Beta bleibt sichtbar).

Norm-Begriff:
  Architecture Overview Document (TOGAF — Phase A)

Ergänzende Norm-Konzepte:
  Communication Artifact (TOGAF — Stakeholder Communication)
  Entry Point Documentation (TOGAF — Architecture Repository)

TOGAF ADM Einordnung:
  Phase A (Architecture Vision) produziert eine Statement of Architecture
  Work die als Einstiegspunkt für alle Stakeholder dient. Das R+MUNI
  README erfüllt diese Rolle für externe Stakeholder: es vermittelt
  Architecture Vision in verständlicher Sprache ohne Framework-Overhead.

Rosetta:
  "README"                           →  Architecture Overview / Entry Point
  "Was ist R+MUNI? Was kann es?"     →  Architecture Vision Statement (simplified)
  "Wie starte ich?"                  →  Architecture Adoption Path
  "Beta = Beta sichtbar"             →  Honest Baseline Communication
  "Ohne Begleitung verständlich"     →  Self-Service Architecture Communication

Bewertung:
  Gutes Mapping. TOGAF Statement of Architecture Work ist formaler
  als ein README — aber das Ziel ist identisch: Stakeholder verstehen
  was das System ist und wie es genutzt werden kann. R+MUNI README
  ist die pragmatische, zugänglichere Form dieses TOGAF-Artefakts.


================================================================================
ZUSAMMENFASSUNG BLOCK 8D
================================================================================

Außenwirkung Mapping Gesamt:

  "Außenperspektive als Test"  →  Stakeholder Communication Quality Check    ✅
  "README als Visitenkarte"    →  Architecture Overview / Entry Point         ✅
  "Beta = Beta sichtbar"       →  Honest Baseline Communication               ✅
  "Polieren, nicht umbauen"    →  Scope Discipline (Phase H)                  ✅

Kernverständnis:
  TOGAF fragt nicht: "Wie soll das README aussehen?"
  Sondern: "Wie wird Architecture Vision für alle relevanten Stakeholder
  verständlich und zugänglich kommuniziert?"
  R+MUNI beantwortet das mit dem Außenperspektive-Kriterium und einem
  README das als selbsterklärende Einladung gebaut ist.

Gesamtbewertung:
  Hohe Konformität. Die Außenwirkungsarbeit in Stage 8 entspricht
  TOGAF Communication Plan-Anforderungen. Besonders stark:
  die explizite Ehrlichkeit über Beta-Status ist TOGAF-Werten
  (Transparency in Architecture Governance) vollständig konform.

Nächster Block:
  Block 8E — Übergang Produktivbetrieb


================================================================================
BLOCK 8E — ÜBERGANG PRODUKTIVBETRIEB
================================================================================


--------------------------------------------------------------------------------
8E00 – STAGE 8 ALS LETZTER BETA-STAGE
--------------------------------------------------------------------------------
Intention:
  Stage 8 ist der letzte Stage des Beta-Zyklus. Nach Abschluss startet
  Stage 1 = Produktivbetrieb (neue Zählung). Stage 8 legt nicht die
  technische Basis — die ist in Stages 1–7 entstanden. Stage 8 legt
  die Kommunikationsbasis: Was vermittelt wird zählt. Der Übergang
  ist bewusst gesetzt und formal abgesichert durch Freeze-8.

Norm-Begriff:
  Architecture Transition Plan (TOGAF — Phase F)

Ergänzende Norm-Konzepte:
  Transition Architecture (TOGAF — Phase F)
  Architecture Roadmap Entry (TOGAF — Phase E/F)

TOGAF ADM Einordnung:
  Phase F (Migration Planning) definiert den Übergang von der aktuellen
  zur Ziel-Architektur. Stage 8 → Stage 1 ist genau dieser Übergang:
  von Beta-Entwicklung zu Produktivbetrieb. TOGAF erwartet einen
  Architecture Transition Plan — R+MUNI liefert das durch Freeze-8
  als autarke Wissensbasis für Stage 1.

Rosetta:
  "Stage 8 = letzter Beta-Stage"    →  Final Transition Architecture
  "Stage 1 = Produktivbetrieb"      →  Target Architecture (Operational Phase)
  "Freeze-8"                        →  Architecture Transition Baseline
  "Stage 8 darf polieren"           →  Transition Scope Constraint
  "Beta-Zyklus Stages 1–8"          →  Architecture Development Programme

Bewertung:
  Sehr gutes Mapping. Der bewusste Schnitt zwischen Beta-Zyklus und
  Produktivbetrieb entspricht TOGAF Phase F sehr gut. Die Entscheidung
  dass Stage 8 poliert und nicht umbaut ist eine explizite Transition
  Scope Constraint — methodisch exakt das was TOGAF in Phase F fordert.


--------------------------------------------------------------------------------
8E01 – FREEZE-8 ALS AUTARKE WISSENSBASIS
--------------------------------------------------------------------------------
Intention:
  Freeze-8 ist die vollständige, autarke Wissensbasis für Stage 1
  (Produktivbetrieb). Es enthält alles was für einen autonomen Start
  in Stage 1 benötigt wird — ohne Rückgriff auf frühere Freeze-Dokumente.
  Freeze-8 ist nach Freigabe unveränderlich und dient als offizielle
  Baseline für den Produktivbetrieb.

Norm-Begriff:
  Architecture Baseline (TOGAF — Architecture Repository)

Ergänzende Norm-Konzepte:
  Approved Architecture (TOGAF — Governance)
  Configuration Baseline (TOGAF — Configuration Management)

TOGAF ADM Einordnung:
  TOGAF Architecture Governance verlangt eine formale, genehmigte Baseline
  die als Ausgangspunkt für weitere Entwicklung dient. Freeze-8 ist
  genau das: formale, unveränderliche Baseline — genehmigt durch EUMAXL,
  dokumentiert nach GOV-Standard, autark für Stage 1.

Rosetta:
  "Freeze-8"                         →  Architecture Baseline (verabschiedet)
  "Autarke Wissensbasis"             →  Self-Contained Architecture Record
  "Unveränderlich nach Freigabe"     →  Immutable Baseline Constraint
  "Startpunkt Stage 1"               →  Baseline for Next Development Cycle

Bewertung:
  Sehr hohe Konformität — identisch zum Freeze-Mapping in Block 7A01
  des Stage-7-Rosetta-Stone. Die Freeze-Logik ist über alle Stages
  konsistent und bewährt. Kein Anpassungsbedarf.


--------------------------------------------------------------------------------
8E02 – RÜCKKOPPLUNGSSCHUTZ IM BETA-ABSCHLUSS
--------------------------------------------------------------------------------
Intention:
  Stage 8 schließt den Beta-Zyklus ohne Rückwirkung auf frühere Stages.
  Stage-3/4/5/6/7-Scripts bleiben read-only. Keine Logikänderung ohne
  expliziten Entscheid. Erweiterungen in Stage 8 sind additiv, nie
  modifizierend. Der Rückkopplungsschutz wird am Übergang in den
  Produktivbetrieb nochmals explizit bekräftigt.

Norm-Begriff:
  Architecture Change Control (TOGAF — Phase H)

Ergänzende Norm-Konzepte:
  Baseline Protection (TOGAF — Configuration Management)
  Scope Discipline (TOGAF — Architecture Governance)

TOGAF ADM Einordnung:
  Phase H (Architecture Change Management) definiert Mechanismen um
  unbeabsichtigte Änderungen an bestehenden Baselines zu verhindern.
  Der R+MUNI Rückkopplungsschutz ist die konsequente operative Umsetzung:
  keine Stage ohne explizite Freigabe, keine Logikänderung ohne Entscheid.

Rosetta:
  "Stage-3/4/5/6/7 read-only"       →  Immutable Baseline (Architecture Change Control)
  "Keine Logikänderung ohne Entscheid" →  Change Request Governance (Phase H)
  "Additiv, nie modifizierend"       →  Non-Regressive Architecture Extension
  "Bugfix nur mit Freigabe"          →  Controlled Exception Process

Bewertung:
  Sehr hohe Konformität. Der Rückkopplungsschutz ist das konsistenteste
  Element über alle R+MUNI Stages — er entspricht TOGAF Phase H
  Architecture Change Control präzise. Die Strenge (read-only auch für
  ältere Stages) übertrifft TOGAF-Standard und ist legitim für ein
  System in der Produktivbetrieb-Vorbereitung.


================================================================================
ZUSAMMENFASSUNG BLOCK 8E
================================================================================

Übergang Produktivbetrieb Mapping Gesamt:

  "Stage 8 = letzter Beta-Stage"  →  Final Transition Architecture             ✅
  "Stage 1 = Produktivbetrieb"    →  Target Architecture (Operational)          ✅
  "Freeze-8"                      →  Architecture Baseline (verabschiedet)      ✅
  "Autarke Wissensbasis"          →  Self-Contained Architecture Record         ✅
  "Rückkopplungsschutz"           →  Architecture Change Control (Phase H)      ✅

Kernverständnis:
  TOGAF fragt nicht: "Wann ist Beta-Betrieb zu Ende?"
  Sondern: "Wie wird der Übergang von Transition Architecture zu Target
  Architecture formally abgesichert — mit klarer Baseline, definierten
  Schutzmechanismen und vollständiger Übergabe-Dokumentation?"
  R+MUNI beantwortet das mit Freeze-8 + Rückkopplungsschutz + Stage-Ziel-Abschluss.

Gesamtbewertung:
  Sehr hohe Konformität. Der Beta-Abschluss entspricht TOGAF Phase F/G/H
  sehr gut. Die Kombination aus Freeze-8 (Baseline), Rückkopplungsschutz
  (Change Control) und klarem Stage-1-Startpunkt ist ein vollständiges
  TOGAF-konformes Transition Management-Paket.

Nächster Block:
  (kein weiterer Block — Gesamtzusammenfassung folgt)


================================================================================
GESAMTZUSAMMENFASSUNG STAGE 8 ROSETTA STONE
================================================================================

R+MUNI Stage 8 Mapping auf TOGAF ADM + ArchiMate 3.2 — Gesamtübersicht:

BLOCK 8A — RELEASE-KONZEPTE
  "Beta 1.0 Release"       →  Architecture Release (Phase F/G)             ✅
  "Tag: v1.0-beta"         →  Release Identifier                           ✅
  "S8 vs. BETA 1.0"       →  Internal vs. External Versioning              ✅

BLOCK 8B — ZIELGRUPPEN-TERMINOLOGIE
  "Associate"              →  Architecture User / Stakeholder               ✅
  "USER → Associate"       →  Controlled Terminology Update (Phase H)       ✅
  "DEV-Variante"           →  Architecture View (Technical)                  ✅
  "Associate-Variante"     →  Architecture View (Non-Technical)              ✅

BLOCK 8C — REPO-ARCHITEKTUR
  "Zwei-Repo-Modell"       →  Federated Architecture Repository             ✅
  "Public Repo"            →  Architecture Repository (Public Partition)     ✅
  "DEV Repo"               →  Architecture Repository (Dev Partition)        ✅
  "History-Reset"          →  Architecture Repository Baseline Reset         ✅
  ".gitignore bewusst"     →  Governance-Driven Content Boundary            ✅

BLOCK 8D — AUSSENWIRKUNG
  "Außenperspektive-Test"  →  Stakeholder Communication Quality Check       ✅
  "README als Visitenkarte" →  Architecture Overview / Entry Point           ✅
  "Beta = Beta sichtbar"   →  Honest Baseline Communication                  ✅

BLOCK 8E — ÜBERGANG PRODUKTIVBETRIEB
  "Freeze-8"               →  Architecture Baseline (verabschiedet)         ✅
  "Stage 1 = Produktiv"    →  Target Architecture (Operational Phase)       ✅
  "Rückkopplungsschutz"    →  Architecture Change Control (Phase H)         ✅


Konformitätsübersicht:
  ✅ vollständig abgebildet  :  18 Konzepte
  ⚠  teilweise / mit Hinweis :   0 Konzepte
  ❌  nicht abgebildet        :   0 Konzepte


R+MUNI Stage-8-Erkenntnisse ohne TOGAF-Pendant:
  — Außenperspektive als operativer Qualitätstest ("Würde ein Fremder das verstehen?")
  — Associate als präzisiertes Stakeholder-Label mit definierten Erwartungen
  — .gitignore als versioniertes Governance-Artefakt (Lessons Learned)
  — Zwei-Varianten-Modell (DEV + Associate) als strukturelles Vollständigkeitsprinzip

Diese Konzepte sind R+MUNI-Originale. Sie sind keine Abweichungen —
sie sind Methodikinnovationen in Bereichen die TOGAF nicht operationell abdeckt.
Sie verdienen eigenständige Dokumentation im Blueprint.

Gesamtbewertung Stage 8:
  R+MUNI Blueprint Stage 8 erreicht die höchste TOGAF-Konformität aller
  bisherigen Stages: 18 von 18 Konzepten vollständig abgebildet, keine
  teilweisen Mappings. Das spiegelt den Charakter von Stage 8:
  kein technisches Neuland — Konsolidierung und Außenwirkung.
  In den klassischen EA-Dimensionen (Release, Stakeholder, Repository,
  Transition) ist Stage 8 musterhaft TOGAF-konform.

  Stage 8 markiert den Abschluss des Beta-Zyklus und den formalen Übergang
  in den Produktivbetrieb. Der Rosetta Stone Stage 8 ist damit auch der
  Abschluss der Beta-Dokumentationsreihe.

  Das ist die richtige Balance für ein System das professionelle
  Architektur-Disziplin mit pragmatischer Open-Source-Realität verbindet.


================================================================================
BEZÜGE
================================================================================

[[FREEZE-8_S8]]                      Baseline für Stage 1 — normative Grundlage
[[FREEZE_7]]                         Baseline für Stage 8 — Ausgangszustand
[[GOV_Global_S8]]                    Normatives Regelwerk
[[TMP_principles_S8]]                Dokumenttypen und Templates
[[STAGE8_ZIELE_S8]]                  Stage-8-Zieldefinition
[[Sprint-DEV-Z1-Beta-1-Release-Besprechung_S8]]  Übergeordneter Sprint S8-Z1
[[Sprint-DEV-Z1-BlockC-Repo-Aufspaltung_S8]]     Repo-Architektur Sprint
[[AI_DRIVEN_DEV_METHODE_S8]]         AI-Driven Development Methodik aktuell
[[Rosetta-Stone_Stage7_S7]]          Vorgänger-Dokument — Stage-7-Mapping


================================================================================
ENDE BLOCK 8 | Rosetta-Stone_Stage8_S8 | 2026-03-28
R+MUNI Blueprint | Stage 8 ABGESCHLOSSEN | Erstellt: EUMAXL + Claude
================================================================================
