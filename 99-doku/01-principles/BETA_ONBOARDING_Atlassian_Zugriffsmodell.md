R+MUNI | BETA ONBOARDING — ATLASSIAN ZUGRIFFSMODELL
Erstellt: 2026-03-09 | Stage 4 AKTIV
Ablage: lokal bei EUMAXL / kein Projektfolder-Artefakt
========================================================

1. ZWECK
--------
Dieses Dokument beschreibt das Zugriffsmodell für Beta-Teilnehmer
auf die R+MUNI Beta-Atlassian-Infrastruktur.
Es gilt für alle Onboarding-Aktivitäten in Stage 4.


2. INFRASTRUKTUR-ÜBERSICHT
---------------------------
Plattform:   Atlassian Cloud Free Plan
             → Dedizierte Beta-Instanz, ausschließlich für R+MUNI
             → NICHT die Atlassian Datacenter-Umgebung der Gruppe
             → Enthält ausschließlich R+MUNI relevante Inhalte
Produkte:    Jira Software Free (max. 10 User)
             Confluence Free (max. 10 User)
             Service Collection Free / JSM (max. 3 Agents)


3. ABGRENZUNG — WICHTIG
------------------------
  ┌─────────────────────────────────────────────────────────┐
  │  Die R+MUNI Beta-Atlassian-Instanz ist vollständig      │
  │  getrennt von der Atlassian Datacenter-Umgebung         │
  │  der Gruppe. Es gibt keine Verbindung, keine            │
  │  gemeinsamen User, keine gemeinsamen Daten.             │
  └─────────────────────────────────────────────────────────┘

  Gruppen-Datacenter:   internes Arbeitsmittel — nicht im Scope
  R+MUNI Beta-Cloud:    dedizierte Free-Instanz — nur R+MUNI


4. ZUGRIFFSEBENEN
-----------------

EBENE 1 — AGENT (nur EUMAXL / R+MUNI Dev)
  Produkt:    Service Collection / JSM
  Rechte:     Tickets bearbeiten, lösen, konfigurieren
  Limit:      1 von 3 verfügbaren Agent-Slots belegt
  Regel:      Diese Rolle wird NICHT an Beta-Teilnehmer vergeben.

EBENE 2 — BETA-TESTER (aktive Mitarbeiter)
  Produkt:    Jira Software + Confluence
  Rechte:     Tickets kommentieren, Doku lesen, R+MUNI EA Projekt
              aktiv mitverfolgen
  Limit:      bis max. 8-9 User (Free-Limit 10, minus EUMAXL)
  Regel:      Kein Service Collection / JSM Agent-Slot.
              Zuweisung erfolgt manuell durch EUMAXL beim Einladen:
              ✅ Jira Software aktivieren
              ✅ Confluence aktivieren
              ❌ Service Collection NICHT aktivieren

EBENE 3 — BETA-KUNDE / FEEDBACK-GEBER (externe Nutzer)
  Produkt:    Service Collection Portal (Customer / Portal-only)
  Rechte:     Tickets über Portal einreichen, Status verfolgen,
              Kommentare schreiben
  Limit:      UNBEGRENZT — kostenlos, kein User-Slot
  Regel:      Zugang NUR über die Portal-URL (nicht über Site-Root).
              Portal-only Account wird beim ersten Portalzugriff
              automatisch angelegt (wenn so konfiguriert).


5. CONFLUENCE — DOKU-ZUGANG OHNE USER-SLOT
-------------------------------------------
Für Personen die NUR Doku lesen sollen (kein Jira nötig):
  → Confluence-Seiten als öffentlichen Share-Link teilen
  → Kein Atlassian Account, kein User-Slot, kein Login nötig
  → Empfohlen für: Interessenten, passive Beobachter, Kunden


6. TECHNISCHE UMSETZUNG BEIM EINLADEN
---------------------------------------
Schritt 1:  admin.atlassian.com öffnen (Beta-Instanz)
Schritt 2:  Organisation auswählen → "Benutzer einladen"
Schritt 3:  E-Mail-Adresse eingeben
Schritt 4:  Produktzuweisung prüfen:
            EBENE 2: Jira ✅ | Confluence ✅ | Service Collection ❌
            EBENE 3: Keines — Zugang nur über Portal-URL
Schritt 5:  Einladung versenden


7. LIMITTABELLE — ÜBERSICHT
-----------------------------

Produkt               | Free Limit | Belegt durch  | Verfügbar Beta
----------------------|------------|---------------|---------------
Jira Software         | 10 User    | 1 (EUMAXL)    | ~9 User
Confluence            | 10 User    | 1 (EUMAXL)    | ~9 User
Service Collection    | 3 Agents   | 1 (EUMAXL)    | 0 — nicht vergeben
Portal Customers      | unbegrenzt | —             | unbegrenzt


8. GRUNDREGELN
---------------
- Die Beta-Instanz ist ausschließlich für R+MUNI Inhalte.
- Service Collection bleibt ausschließliches Arbeitsmittel von EUMAXL.
- Beta-Tester erhalten Jira + Confluence, aber keinen Agent-Zugang.
- Beta-Kunden nutzen ausschließlich das Service Portal als Customers.
- Confluence-Doku für passive Nutzer: öffentlicher Share-Link, kein Login.
- Lizenz-Upgrade wird erst geprüft wenn Free-Limits real erreicht werden.
