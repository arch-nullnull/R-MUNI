================================================================================
STAGE <N> – <STAGE-TITEL>
Normative Definition und Geltungsbereich
================================================================================
Projekt         : R+MUNI Blueprint
Dokument        : Stage<N>_Ziele_S<N>
Datum           : <YYYY-MM-DD>
Erstellt durch  : <ROLLE> + Claude (Pair-Session)
================================================================================
<!-- HINWEIS FÜR DEV
     Dieses Template ist die verbindliche Vorlage für alle Stage_Ziele-Dokumente.
     Platzhalter in <GROSSBUCHSTABEN> sind zu ersetzen.
     Kommentarblöcke (wie dieser) werden im fertigen Dokument entfernt.

     CHARAKTER DES STAGE_ZIELE-DOKUMENTS — verbindlich einzuhalten:
     - Strategisch, nicht operativ
     - Beantwortet: Warum existiert dieser Stage? Was soll er leisten?
     - Enthält keine technischen Implementierungsdetails
     - Enthält Ausgangsbasis, Charakter, zulässige Inhalte und Abgrenzung
     - Wird zu Beginn eines Stage erstellt
     - Kann bei wesentlichen Erkenntnissen im Stage ergänzt werden
     - Ist nach Stage-Abschluss read-only
     - Formale Feststellung am Ende ist Pflicht

     Obsidian-Links sind optional — dort einsetzen wo Bezüge bestehen.
     Formstabilität hat Vorrang vor sprachlicher Variation.
-->


================================================================================
1. ZWECK VON STAGE <N>
================================================================================
<!-- Was ist der Kern-Zweck dieses Stage?
     Eine klare Aussage — kein Fließtext.
     Im Fokus stehen: die wichtigsten 3–5 Themen dieses Stage. -->

Stage <N> dient <KERNZWECK IN EINEM SATZ>.

Im Fokus stehen:
  - <Schwerpunkt 1>
  - <Schwerpunkt 2>
  - <Schwerpunkt 3>
  - <Schwerpunkt 4>

<Abschlusssatz der den Charakter auf den Punkt bringt>
Beispiel: "Stage <N> ist <Charakterisierung> — <Abgrenzung zum vorherigen Stage>"


================================================================================
2. AUSGANGSBASIS
================================================================================
<!-- Auf welchem Zustand baut Stage N auf?
     Was ist read-only, was darf verändert werden, was ist zulässig?
     Explizit — keine impliziten Annahmen. -->

Stage <N> baut auf dem eingefrorenen Stage-<N-1>-Zustand auf.

  - <Was ist read-only>
  - <Was gilt als normativ stabil>
  - <Was ist zulässig — Erweiterungen, Bugfixes, etc.>
  - <Was ist nicht zulässig>

<Ausnahmeregel wenn vorhanden>
Beispiel: Rückgriff auf Stage-<N-1>-Artefakte ist zulässig, Eingriffe sind es nicht.
Ausnahme: Bugfixes mit expliziter Freigabe durch den Betreiber.

Bezug auf vorherigen Freeze:
  [[FREEZE-<N-1>_S<N>]]             Ausgangszustand für Stage <N>


================================================================================
3. CHARAKTER VON STAGE <N>
================================================================================
<!-- Was macht diesen Stage besonders?
     Was ist neu gegenüber dem vorherigen Stage?
     Welche Realität tritt ein die vorher nicht existiert hat? -->

<Kernaussage über den Charakter dieses Stage>

  - <Charaktermerkmal 1>
  - <Charaktermerkmal 2>
  - <Charaktermerkmal 3>
  - <Charaktermerkmal 4>

<Leitprinzip für diesen Stage>
Beispiel: "Stage <N> darf wachsen — kontrolliert und rückkopplungssicher."


================================================================================
4. ZULÄSSIGE INHALTE IN STAGE <N>
================================================================================
<!-- Was darf in diesem Stage konkret passieren?
     Jeder Inhalt bekommt einen eigenen Unterabschnitt.
     Grenze am Ende jedes Abschnitts explizit benennen wenn relevant. -->

4.1 <Inhalt 1>
---------------
  - <Was konkret passiert>
  - <Was konkret passiert>
  - <Was konkret passiert>
  - Ziel: <Was am Ende erreicht sein soll>

Grenze: <Was in diesem Bereich explizit nicht passieren darf>


4.2 <Inhalt 2>
---------------
  - <Was konkret passiert>
  - <Was konkret passiert>

Grenze: <Was in diesem Bereich explizit nicht passieren darf>


4.3 <Inhalt 3>
---------------
  - <Was konkret passiert>


<!-- Weitere Unterabschnitte nach demselben Muster -->


================================================================================
5. UMGANG MIT ERKENNTNISSEN AUS VORHERIGEN STAGES
================================================================================
<!-- Was darf aus früheren Stages verwertet werden?
     Was darf nicht verändert werden?
     Klare Grenzlinie ziehen. -->

Erkenntnisse aus Stage <N-1> und früheren Stages dürfen:
  - <Was verwertet werden darf 1>
  - <Was verwertet werden darf 2>

Sie dürfen jedoch nicht:
  - <Was nicht verändert werden darf 1>
  - <Was nicht verändert werden darf 2>

Stage <N> ist <Charakterisierung> — nicht Revision.


================================================================================
6. RÜCKKOPPLUNGSSCHUTZ
================================================================================
<!-- Was ist absolut geschützt?
     Welche Grenzen gelten ohne Ausnahme?
     Explizit und prüfbar formulieren. -->

  - <Schutzregel 1>
  - <Schutzregel 2>
  - <Schutzregel 3>
  - <Schutzregel 4>


================================================================================
7. DOKUMENTATION IN STAGE <N>
================================================================================
<!-- Wie wird dieser Stage dokumentiert?
     Was ist Pflicht, was ist optional?
     Welche Dokumente entstehen? -->

  - <Dokumentationspflicht 1>
  - <Dokumentationspflicht 2>
  - <Dokumentationspflicht 3>

Fokus: <Was die Dokumentation in diesem Stage leisten soll>


================================================================================
8. ABGRENZUNG ZU SPÄTEREN STAGES
================================================================================
<!-- Was ist bewusst nicht Teil dieses Stage?
     Was wächst aus diesem Stage heraus — ist aber noch nicht hier? -->

Nicht Teil von Stage <N> sind:
  - <Abgrenzung 1>
  - <Abgrenzung 2>
  - <Abgrenzung 3>

<Diese Themen wachsen aus Stage <N> heraus — sie sind Ergebnis, nicht Voraussetzung.>


================================================================================
9. FORMALE FESTSTELLUNG
================================================================================
<!-- Abschlussfeststellung — Pflicht.
     Stage gilt als formal eröffnet wenn diese Feststellung getroffen ist.
     Prüfpunkte müssen alle erfüllt sein. -->

Mit dieser Definition ist Stage <N>:
  - logisch eröffnet
  - klar abgegrenzt von Stage <N-1>
  - rückkopplungssicher
  - GOV-konform
  - auf <ZIEL> ausgerichtet

<Aussage über den Schutz früherer Stages>
Stage <N> darf wachsen, ohne zu verzerren.


================================================================================
BEZÜGE
================================================================================
[[Global_GOV_S8]]                    normative Grundlage
[[FREEZE-<N-1>_S<N>]]               Ausgangszustand — letzter stabiler Stand
[[<verwandtes Dok>]]                 <Bezug>


================================================================================
Stage <N> – <STAGE-TITEL>
ZIELE DEFINIERT | <YYYY-MM-DD>
R+MUNI Blueprint | Erstellt durch: <ROLLE> + Claude (Pair-Session)
================================================================================
