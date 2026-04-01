================================================================================
ATLASSIAN-ADMINISTRATIONS-SCHEMA — BACKLOG (DEV)
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : BACKLOG_Atlassian-Admin-Schema_DEV_S101
Tag             : #dev #backlog #atlassian #offboarding #s101
Datum           : 2026-03-31
Stage           : S1.01 — AKTIV
Status          : BACKLOG — nicht gestartet
Verantwortlich  : EUMAXL
Review          : —
Jira-Sync       : NEIN — Jira nach explizitem EUMAXL-Input
Ablageort       : C:\Prototyping\R+MUNI Doku\R+MUNI Doku-internal\05-backlog\
================================================================================


================================================================================
1. AUSGANGSLAGE UND KONTEXT
================================================================================

Warum existiert dieser Backlog-Eintrag?
Aus dem Offboarding MLAT (LL_MLAT_S101) ist hervorgegangen dass die
Atlassian-Instanz ohne klares Administrations-Schema eingerichtet wurde.
Mehrere verbundene Instanzen (Jira, Confluence, Service Bundle) ohne
definierte Space-Trennung haben bei Bereinigungsversuchen Folgefehler
erzeugt (Landing URL, Default Gateway). Vollständiges Offboarding war
nicht automatisiert möglich — Restfragmente verbleiben bis
Inaktivitätslöschung durch Atlassian oder explizites Support-Ticket.

Was ist der gewünschte Zielzustand?
Vor dem nächsten Beta-Kunden mit Atlassian-Stack existiert ein definierter
Administrationspfad: Instanz-Verwaltung, Space-Trennung je Kunde,
und ein sauberer Offboarding-Pfad für Atlassian-Komponenten.

Warum jetzt noch nicht?
Laufendes Kundenprojekt mit eigenem Atlassian-Account verhindert
risikofreie Experimentierumgebung. Atlassian-Restfragmente MLAT
sind noch nicht vollständig bereinigt — Bereinigung ist Voraussetzung
für die Schema-Definition.


================================================================================
2. SCOPE
================================================================================

Was gehört dazu:
  - Administrationspfad für Atlassian-Instanz-Verwaltung definieren
  - Space-Trennung je Beta-Kunde dokumentieren
  - Offboarding-Pfad für Atlassian-Komponenten in How2 verankern
  - Atlassian-Restfragmente MLAT bereinigen (Support-Ticket)

Was gehört explizit nicht dazu:
  - Änderungen am bestehenden Zwei-Repository-Prinzip (GitHub)
  - Änderungen an Tier-Logik oder Onboarding-Ablauf generell
  - Neue Atlassian-Produkte oder Lizenzmodelle evaluieren


================================================================================
3. VORAUSSETZUNGEN FÜR UMSETZUNG
================================================================================

Bevor dieser Backlog-Punkt gestartet werden kann:
  - Laufendes Kundenprojekt mit eigenem Atlassian-Account abgeschlossen
    oder Testumgebung klar getrennt
  - Atlassian-Restfragmente MLAT bereinigt oder explizit als
    nicht bereinigbar dokumentiert


================================================================================
4. OFFENE FRAGEN
================================================================================

| Frage | Wer klärt | Bis wann |
|-------|-----------|----------|
| Support-Ticket Atlassian für MLAT-Restfragmente — wann? | EUMAXL | nach Kapazität |
| Ist eine separate Atlassian-Testumgebung realistisch? | EUMAXL | vor Sprint-Start |


================================================================================
BEZÜGE
================================================================================
[[LL_MLAT_S101]]                    Ursprung dieses Backlog-Eintrags
[[BETA_OFFBOARDING_How2_DEV_S101]]  Betroffenes Dokument
[[Global_GOV_DEV_S101]]             Normative Grundlage


================================================================================
ATLASSIAN-ADMINISTRATIONS-SCHEMA | DEV | S1.01 | 2026-03-31 | R+MUNI Blueprint
================================================================================
