================================================================================
BETA GITHUB NUTZUNG — BETA BETRIEB
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : BETA_GitHub_Nutzung_S5
Tag             : #dev #github #beta #repo #s5
Datum           : 2026-03-26
Stage           : S8 — AKTIV
Status          : AKTIV
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN
Erstellt        : 2026-03-09
Ablageort       : R+MUNI Doku-public\01-principles\BETA_GitHub_Nutzung_S5.md
================================================================================

1. ZWECK
--------
Dieses Dokument regelt die Nutzung von GitHub im Kontext der
R+MUNI Beta. Es definiert klar welche Repositories für welchen
Zweck genutzt werden und wo Entwicklung stattfindet.


2. ZWEI-REPOSITORY-PRINZIP
---------------------------

REPOSITORY A — R+MUNI Blueprint (öffentlich)
  GitHub:       github.com/EUMAXL
  Sichtbarkeit: PUBLIC
  Inhalt:       Blueprint-Scripts, Konfigurationen, Dokumentation,
                Clean-ZIP für Schnellinstallation
  Zweck:        Öffentliche Distribution des R+MUNI Toolsets
  Zielgruppe:   Alle — Community, Interessenten, Beta-Nutzer

REPOSITORY B — Beta Installation (privat, pro Firma)
  Sichtbarkeit: PRIVATE
  Inhalt:       Firmenspezifische Archi-Modelle, angepasste
                Konfigurationen, interne Daten der Beta-Firma
  Zweck:        Versionierung der Beta-Installation beim Kunden
  Zielgruppe:   Nur EUMAXL + ggf. 1-2 interne Ansprechpartner
                der jeweiligen Beta-Firma


3. ENTWICKLUNGS-GRUNDREGEL — WICHTIG
--------------------------------------
  ┌─────────────────────────────────────────────────────────┐
  │  Entwicklung an R+MUNI findet AUSSCHLIESSLICH           │
  │  im R+MUNI Blueprint Repository (Repo A) statt.        │
  │                                                         │
  │  Die Beta-Installation (Repo B) ist KEIN               │
  │  Entwicklungsumfeld.                                    │
  └─────────────────────────────────────────────────────────┘

Begründung:
  - R+MUNI ist ein Open-Source Blueprint — Weiterentwicklung
    gehört ins öffentliche Modell, nicht in eine Kundeninstallation
  - Beta-Firmen arbeiten auf einem definierten Stand des Blueprints
  - Änderungen an Kundenmodellen sind firmenspezifisch und
    dürfen nicht in den öffentlichen Blueprint zurückfließen
  - Saubere Trennung schützt die Integrität des Blueprints


4. UPDATE-FLUSS
----------------

  R+MUNI Blueprint (Repo A, PUBLIC)
          │
          │  neue Version / Bugfix wird released
          ▼
  Beta-Installation (Repo B, PRIVATE)
          │
          │  EUMAXL spielt Update manuell ein
          │  (kein automatischer Pull in Beta)
          ▼
  Firmenspezifische Modelle bleiben unberührt


5. MODELLE IN DER BETA
-----------------------
  - Archi-Modelle der Beta-Firma: PRIVAT, in Repo B
  - Werden NICHT veröffentlicht
  - Werden NICHT in Repo A eingecheckt
  - Unterliegen keiner Open-Source-Lizenz
  - Gehören ausschließlich der jeweiligen Firma


6. WAS KOMMT AUS REPO A IN DIE BETA?
--------------------------------------
  ✅ Blueprint-Scripts (CSV, XML, M2B, HLP, FLOW, ATL)
  ✅ Konfigurationsdateien (mapping.txt, sync.txt, etc.)
  ✅ Dokumentation (Install.txt, README.md, How2, Principles)
  ✅ Clean-ZIP für Erstinstallation

  ❌ Firmenmodelle (Archi .archimate Files)
  ❌ Interne Daten der Beta-Firma
  ❌ Firmenspezifische Anpassungen


7. FEEDBACK AUS DER BETA
--------------------------
Erkenntnisse aus dem Beta-Betrieb die den Blueprint verbessern:
  → werden als GitHub Issue in Repo A eingetragen
  → oder als Jira Ticket im RMUNI Projekt erfasst
  → Umsetzung erfolgt im Blueprint (Repo A)
  → Beta-Firma erhält das Update über den normalen Update-Fluss

  Regel: Kein direktes Eingreifen in Repo A durch Beta-Firmen.
         Feedback ja — direkter Commit nein.


8. ZUSAMMENFASSUNG
-------------------

  Frage                              | Antwort
  -----------------------------------|----------------------------------
  Wo wird R+MUNI entwickelt?         | Repo A — Blueprint (public)
  Wo liegen Kundenmodelle?           | Repo B — Beta-Firma (private)
  Werden Modelle veröffentlicht?     | Nein — immer privat
  Können Beta-Firmen committen?      | Nein — nur Feedback geben
  Wie kommen Updates zur Beta-Firma? | Manuell durch EUMAXL aus Repo A
