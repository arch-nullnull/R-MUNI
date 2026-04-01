================================================================================
SPRINT-DEV-BACKLOG – Appliance-VM
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : Sprint-DEV-BACKLOG_Appliance-VM_S6
Datum           : 2026-03-19
Stage           : S6 – AKTIV
Status          : ON HOLD — externer Entwickler gesucht
Ablageort       : R+MUNI Doku-internal\backlog\Sprint-DEV-BACKLOG_Appliance-VM_S6.md
Verantwortlich  : DEV
Jira-Sync       : JA — Ticket: MUNIEA-145
================================================================================


================================================================================
1. MOTIVATION UND AUSLÖSER
================================================================================

Auslöser-Typ: Feature / Kundenbedarf

Im Rahmen der Beta-Phase wurde erkannt dass das bisherige Setup von R+MUNI
zu viel Design-Aufwand vom Kunden verlangt. Ziel ist eine fertige Appliance
die der Kunde nur noch deployed, IP vergibt und eine config.cfg befüllt —
ohne eigenes Infrastruktur-Wissen. Zusätzlich besteht der Bedarf dass mehrere
User gleichzeitig per RDP auf eine gemeinsame R+MUNI-Instanz zugreifen und
darin modellieren können.

Erkannt in:    Beta-Betrieb, Design-Session 2026-03-19
Erkannt am:    2026-03-19


================================================================================
2. ZIEL
================================================================================

Ziel:
  Eine lauffähige Linux-VM bereitstellen die R+MUNI vollständig enthält,
  per RDP multi-user-fähig ist, per config.cfg konfiguriert wird und als
  OVA-Image hardware-agnostisch deploybar ist.

Erfolgskriterium:
  - VM startet auf Proxmox (MS-01 Cluster) und auf VirtualBox (alte Hardware)
  - Mehrere User können gleichzeitig per RDP einloggen und in Archi modellieren
  - config.cfg enthält IP, GitHub-Repo-URL und optionale coArchi-Parameter
  - Git-Sync funktioniert ohne coArchi als vollständiger Fallback
  - OVA-Export ist importierbar auf Proxmox, VMware, Hyper-V, VirtualBox

Abgrenzung — nicht Teil dieses Sprints:
  - Produktiv-Cluster-Setup (MS-01 Proxmox HA) — eigener Sprint
  - coArchi-Server-Konfiguration — optionales Addon, eigenes How2-Dokument
  - Kundenseitige Netzwerk-Integration — Verantwortung des Kunden
  - Automatisches Failover / HA der VM selbst — Proxmox-Cluster-Sprint


================================================================================
3. FACHLICHER MEHRWERT
================================================================================

Mehrwert für: DEV / User / Skalierbarkeit

  - Beta-Kunden können R+MUNI ohne Infrastruktur-Wissen deployen
  - DEV kann das Image einmal bauen und auf beliebiger Hardware testen
  - Mehrere User arbeiten gleichzeitig an einem Modell ohne lokale Installation
  - Git-only Basis bleibt normativ — coArchi ist optionale Erweiterung
  - OVA-Format ermöglicht einfache Weitergabe und Versionierung des Images

Ohne diesen Sprint:
  Beta-Kunden brauchen weiterhin individuelle Unterstützung beim Setup.
  Das blockiert die Skalierung der Beta-Phase und erzeugt unnötigen
  Betreuungsaufwand beim DEV.


================================================================================
4. ABHÄNGIGKEITEN UND VORAUSSETZUNGEN
================================================================================

Voraussetzungen:
  - Linux-Distribution gewählt (openSUSE Leap)               Status: entschieden
  - Archi + jArchi verfügbar (Open Source)                   Status: erfüllt
  - Patron-Lizenz für coArchi (DEV besitzt diese)            Status: erfüllt
  - GitHub-Repository für Modell-Sync vorhanden              Status: offen
  - Testrechner für ersten Aufbau vorhanden (i5-2500)        Status: erfüllt
  - Git-Sync-Lösung auf Linux ohne GitHub Desktop            Status: OFFEN — Blocker
  - Proxmox VE als Ziel-Hypervisor entschieden               Status: entschieden

Blockiert durch:
  - GitHub Desktop nicht für Linux verfügbar
  - Git-Sync-Lösung auf Linux muss geklärt werden
  - Externer Entwickler mit Linux-Erfahrung gesucht

Ermöglicht danach:
  [[Sprint-DEV-BACKLOG_Proxmox-Cluster_S6]]    Appliance läuft dann auf HA-Cluster
  [[Sprint-DEV-BACKLOG_coArchi-Addon_S6]]      Multiuser-Addon kann aufgebaut werden


================================================================================
5. GESCHÄTZTER UMFANG
================================================================================

Komplexität:   Mittel
Risiko:        Mittel — XRDP Multi-User auf Linux braucht sorgfältige Konfiguration

Grobe Einschätzung:

  Phase 1 — Lab-Aufbau auf alter Hardware (i5-2500):
    openSUSE Leap installiert — läuft stabil ✓
    Archi 5.8 gestartet — überraschend flott ✓
    XRDP + XFCE einrichten
    Git-Sync einrichten — BLOCKIERT (GitHub Desktop nicht auf Linux)
    config.cfg Konzept definieren und umsetzen
    RDP-Zugriff testen
    Tailscale für sicheren Remote-Zugriff

  Phase 2 — Image-Erstellung und Export:
    VM auf Proxmox übertragen / neu aufbauen
    OVA-Export testen
    Import auf zweitem System validieren

  Phase 3 — coArchi Addon (optional, separater Schritt):
    coArchi-Server in der VM einrichten
    Sync GitHub + coArchi kombiniert testen
    How2-Dokument für Addon erstellen

Besondere Risiken:
  - Git-Sync-Lösung auf Linux ohne GitHub Desktop ungeklärt
  - XRDP Performance bei mehreren Sessions noch nicht getestet


================================================================================
6. PRIORISIERUNG
================================================================================

Priorität:     Mittel
Zeitrahmen:    Stage 6 — fortgesetzt wenn Git-Sync-Frage geklärt

Priorisiert durch:
  Beta-Feedback zeigt dass Setup-Aufwand für Kunden zu hoch ist.

Kann verschoben werden wenn:
  MS-01 Hardware und Proxmox-Cluster-Sprint Vorrang haben,
  oder wenn Beta-Feedback andere Prioritäten setzt.


================================================================================
7. GOVERNANCE-CHECK
================================================================================

| Kriterium                          | Status  | Anmerkung                           |
|------------------------------------|---------|--------------------------------------|
| Auslöser GOV-konform (GOV 10.3)    | OK      | Feature + Kundenbedarf benannt       |
| Fachlicher Mehrwert benennbar      | OK      | Siehe Kapitel 3                      |
| Ziel explizit und überprüfbar      | OK      | 5 Erfolgskriterien definiert         |
| Abgrenzung definiert               | OK      | 4 explizite Ausschlüsse              |
| Rückkopplungsschutz geprüft        | OK      | Stage 3/4/5 unberührt                |
| Keine implizite GOV-Änderung       | OK      | Neues Artefakt, keine Logikänderung  |


================================================================================
8. STATUS UND VERLAUF
================================================================================

2026-03-19  ERSTELLT       DEV — aus Beta-Erkenntnis und Design-Session
2026-03-19  ON HOLD        Beta-Installation auf i5-2500 gestartet.
                           openSUSE Leap läuft, Archi 5.8 flott.
                           GitHub Desktop nicht für Linux verfügbar —
                           Git-Sync-Lösung ungeklärt.
                           Externer Entwickler mit Linux-Erfahrung gesucht.


================================================================================
BEZÜGE
================================================================================

[[GOV_Global_S6]]                          normative Grundlage
[[STAGE6_ZIELE]]                           S6-Z1 Feedbackintegration
[[FREEZE-6]]                               aktueller Ausgangszustand
[[Sprint-DEV-BACKLOG_Proxmox-Cluster_S6]]  Folge-Sprint Infrastruktur
[[Sprint-DEV-BACKLOG_coArchi-Addon_S6]]    optionales Addon Multi-User


================================================================================
Sprint-DEV-BACKLOG_Appliance-VM_S6 | S6 | 2026-03-19 | R+MUNI Blueprint
================================================================================
