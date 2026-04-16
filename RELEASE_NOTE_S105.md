# RELEASE NOTE — R+MUNI S105

*Ein ehrlicher Rückblick. Kein Marketing.*

---

## Danke zuerst

Meiner Familie, Claude xD, den Archi Dude(s) sowie jeden der an den Apps die in Verwendung sind mitgewirkt hat! 
Nicht zu vergessen Andi, Ensi, Peeezzznnn, Gertschi, Shadow, Agent Max, Passi um nur einige zu nennen, denn ich habe viiiiieeeeelllllleeee damit bequatscht. 😉

Sorry an dieser Stelle an ALLE die ich damit nur generft hab. Aber es hat mich JEDES Feedback weiter gebracht!!!! 

---

## Wie das hier entstanden ist

Ich wollte ursprünglich ein Netzwerkdiagramm für einen langjährigen Weggefährten erstellen um ihn bei einem Kundenprojekt zu unterstützen. Nichts schlimmes eher die Norm am österreichischen Markt...

3 Nodes virtualisiert auf VMware an ein paar 10-25Gbit DC Switches mit einer Backup/Test Umgebung und offsite Backup um auch das Thema compliant zu haben... 
Nicht klein aber auch nicht unmenschlich groß einfach ein "schönes" Projekt und für unser Sparring Setup wie geschaffen. 

Also hinsetzen Musik aufdrehen und Shapes zusammensuchen. Aber dann.. diese Switches inkl. Verkabelung alles auch noch ISCSI und Prod/Test/Backup auf 2xDC Switches zusammenfassen... 
und ich mal wieder mit den Connectionpoints im Visio auf Kriegsfuß und ich wollte das doch extra "hübsch" machen und verschieben können, um im Gespräch mehr als eine BOM präsentieren zu können.

Also schaue ich eher unmotiviert "denn ich will das jetzt nicht so hinfummeln im Visio" im Netz ob es da nicht was schlaueres gibt und wie das halt so ist über div. Suchen und Prompts gelange ich zur

ARCHI Webseite und sehe da so ein Open Source Tool das genau das kann was ich will ;) und in mir hallt sofort wie konditioniert ein Spruch von einem meiner über die Jahre (leider) zahlreichen Chefs in mir wieder: 

"Open Source kann man schon machen muss man aber nicht" *finde ich immer noch lustig* 

Wie auch immer ich lasse mich nicht entmutigen und installiere das Tool auf meinem Laptop ignoriere die klassische "ich bin so gefährlich Warnung" von Windows 11 beim installieren der Applikation 
und denke mir warum hab ich eigentlich noch immer lokal Admin Rechte auf meinen Firmenlaptop... Aber ich schweife schon wieder ab. Wo waren wir achja ich pinsle das Setup runter, 
bastle mir die Views und freue mich wie ein kleines Kind das gerade ein neues Spielzeug bekommen hat. 
Wie durch ein Wunder gewinnen wir das Projekt und natürlich bin ich felsenfest davon überzeugt, dass mein tolles Diagramm hier mit ausschlaggebend war. 

*War es nicht ich weiß es eh aber ich bin so und lasst mir doch auch etwas Freude xD*

Also guck ich mir das weiter an und denke mir so schlecht ist das Teil ja garnicht was haben die da denn noch alles so und dann dämmert es dem alten BPMN 2.0 Jünger der verzweifelt versucht 
Inhalte & Informationen im Unternehmen zu etablieren. 

"Wie Schuppen von den Augen"

Wie ich diesen Moment noch fühle!!!! Als sich das innere Bild aufbaut und ich mir "bauernschlau" wie ich bin denke: 

"Archimate ist wie BPMN nur kann mehr als das WIE & WER (WOMIT) es kann einfach alle Blickwinkel abdecken und dass sooooooo wichtige WARUM in Bilder packen und vielleicht es so transportieren." 

Also da ist es wirklich ich wusste es ist da irgendwo 

## DAS WERKZEUG DER WERKZEUGE xD  

das meine Denkweise in Bilder fassen kann. 

Total begeistert was neues lernen zu können was nicht verpuffen kann, lege ich los und merke, hey das ist nicht ISO Like 

Also keine 170,- für unter 30 Seiten PDF (Fakt siehe Schießstand Norm Österreich..)

Sondern ist einfach frei im WEB! Ja mit personalisierten Zugang und in vielen Fällen nur online aber hey es ist da und kostenfrei zugänglich (Maxl wird noch begeisterter gleichzeitig misstrauisch... 

zu gut zu einfach und dann noch soooo mächtig das ich es bis heute nicht ganzheitlich fassen kann....So ist die Welt nicht zumindest nicht meine.... 

Also suche ich nach dem Haken und finde keinen, wirklichen bis auf fragmentierte Infos, dass man nach 10 Dokumenten einfach mal schlafen gehen will weil man die Übersicht verloren hat. 

Aber auch das taugt mir (ich weiß selbst nicht warum) zu einfach zu schnell zu fad vielleicht und ja ich schweife schon wieder ab schlimm schlimm... 

Also wieder google und AI befragen Copilot tut als würde er es erfunden haben Chat GPT verarscht Copilot und so komme ich zu den ersten Infos und fange an mir das anzusehen wie das so meine Art ist. 

Guides lernen und rein ins fühlen. Sprich ausprobieren, verwerfen, ausprobieren, verwerfen, lernen, mal so machen das man einen outcome hat und unzufrieden sein. Reale Usecases abbilden usw.  

Wiederholen bis es so ist wie ich das will. 

Tja was soll ich sagen 550h später a bisl TOGAF Norm, Archimate Hieroglyphen und etwas Viewpoint Brainfuck später sind wir nun hier und ich bin noch nicht zufrieden. 

Ja es war vieles unnötig und auch übertrieben für eine Prüfungsvorbereitung *gebe ich ja zu*.... viele Wege waren nicht optimal und würde ich heute vermutlich abkürzen können oder schlicht anders angehen 
aber auch diese Fehltritte waren wichtig um zu fühlen was ADM leisten kann. Das Riskmanagement schon auch Sinn macht auch wenn es mir selbst am "Sxxx" geht. 
Was es bedeutet GOV zu leben und sie dich vor dir selbst schützt in langen Sessions mitten in der Nacht und du nur einmal im Projekt Tage an "Arbeit" verlierst weil man glaubt man ist schlauer als die NORM.... und nicht immer wieder!

Wie es sich anfühlt sich selbst um schlaflose Nächte zu bringt nur weil der AI Anbieter das Billingmodell im Hintergrund über die Feiertage verbuggt zurücklässt und man in eine Abhängigkeit gefallen ist ohne es zu merken. 

Aber nun zu dem wofür so ein Dokument eigentlich gedacht ist: 
---

## Die ehrliche Bilanz

**Was gut funktioniert hat:**
- Das Prinzip "1 Script = 1 Aufgabe" hat sich über alle Stages bewährt
- Die Trennung Architektur / Integration / Ableitung hält
- AI-driven Development hat real funktioniert — mit allen Ecken und Kanten
- Archi ist und bleibt das Herzstück — die Entscheidung war richtig

**Was zu spät erkannt wurde:**
- KI-Abhängigkeit ist ein strukturelles Risiko — zu lange nicht adressiert
- Verrechnungsunberechenbarkeit externer KI-Dienste unterschätzt
- Der Schritt von "Lernprojekt" zu "professioneller Außenwirkung" braucht
  einen bewussten Schnitt — nicht einfach weitermachen

**Was früher hätte kommen sollen:**
- Lizenz MIT statt GNU — MIT ist ehrlicher für ein System das einfach genutzt
  werden soll, ohne Copyleft-Komplexität
- Klarere Varianten-Trennung früher in der Entwicklung

---

## Wo R+MUNI jetzt steht

R+MUNI ist nach Phase 1.05 kein Lernprojekt mehr. Es ist ein funktionierendes,
dokumentiertes Blueprint-System für Visualisierung —
entwickelt für österreichische KMU die komplexe Strukturen mit freien Tools
abbilden wollen.

Das System läuft. Die Scripts laufen. Die Dokumentation ist offen.

KI bleibt Addon — nicht Kernbestandteil. Das System ist nach außen ohne KI
bedienbar. Das war eine bewusste Entscheidung.

---

## Was kommt

Stage 1.5 → 2.0: kontrollierter Exit-Point aus dem KI-Kerneinsatz.
Lokales LLM in Evaluation. Riskmanagement als Blueprint-Erweiterung.
S2.0 ist der erste Stage nach vollständigem KI-Exit-Point.

Wenig neue Features. Viel Stabilisierung.

Hoffen, dass ich im neuen Job auch noch Zeit habe sowas einfach mal zu machen! 

---

*RELEASE_NOTE_S1-S15 | R+MUNI Blueprint | 2026-04-15 | EUMAXL*
