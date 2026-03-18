@echo off
:: ================================================================================
:: R+MUNI - SETUP: Grundordnerstruktur anlegen
:: Stage 5 | Aktiv | R+MUNI Blueprint
:: ================================================================================
:: Erstellt    : 2026-03-17
:: Stage       : S5 - AKTIV
:: Zweck       : Legt die vollstaendige R+MUNI Ordnerstruktur an.
::               Alle Hauptordner erhalten das Kuerzel als Suffix.
::               Nach dem Setup: ZIP-Inhalt in R+MUNI <KUERZEL>\ entpacken -
::               die Dateien landen direkt in die vorhandenen Ordner.
::               Leere Ordner werden vom Script angelegt, GitHub-Problem geloest.
::               R+MUNI Apps wird NICHT angelegt - Tools manuell installieren.
:: ================================================================================

chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo   R+MUNI - Grundordnerstruktur Setup
echo ================================================================================
echo.

:: --- Abfrage 1: Installationsordner ---
echo Abfrage 1 von 2: Installationsordner
echo   Wo soll R+MUNI installiert werden?
echo   Standard: C:\Prototyping
echo   Enter druecken fuer Standard oder eigenen Pfad eingeben.
echo   Beispiel: D:\Projekte oder C:\Users\Max\Dokumente
echo.
set /p ROOT_INPUT="Installationsordner: "

if "!ROOT_INPUT!"=="" (
    set ROOT=C:\Prototyping
) else (
    set ROOT=!ROOT_INPUT!
)

if "!ROOT:~-1!"=="\" set ROOT=!ROOT:~0,-1!

echo   Gewaehlt: !ROOT!
echo.

:: --- Abfrage 2: Kuerzel ---
echo Abfrage 2 von 2: Kuerzel (max. 4 Zeichen)
echo   Dieses Kuerzel wird an alle Hauptordner angehaengt.
echo   Beispiel: ABCD ergibt R+MUNI ABCD, R+MUNI Archiv ABCD, usw.
echo   Auch als Kundenordner-Name: R+MUNI Doku-ABCD
echo.

:KUERZEL_EINGABE
set /p KUERZEL_INPUT="Kuerzel (1-4 Zeichen): "

if "!KUERZEL_INPUT!"=="" (
    echo   Bitte ein Kuerzel eingeben.
    goto KUERZEL_EINGABE
)

set KUERZEL=!KUERZEL_INPUT!

set LEN=0
set STR=!KUERZEL!
:LEN_LOOP
if "!STR!"=="" goto LEN_DONE
set STR=!STR:~1!
set /a LEN+=1
goto LEN_LOOP
:LEN_DONE

if !LEN! GTR 4 (
    echo   Bitte maximal 4 Zeichen eingeben.
    goto KUERZEL_EINGABE
)

echo   Gewaehlt: !KUERZEL!
echo.

:: --- Vorschau ---
echo ================================================================================
echo   Folgende Struktur wird angelegt unter: !ROOT!
echo ================================================================================
echo.
echo   R+MUNI !KUERZEL!\          ^(Blueprint - ZIP danach entpacken^)
echo   R+MUNI Archiv !KUERZEL!\
echo   R+MUNI Doku !KUERZEL!\
echo.

set /p CONFIRM="Weiter? (J/N): "
if /i "!CONFIRM!" NEQ "J" (
    echo.
    echo   Abgebrochen. Keine Aenderungen vorgenommen.
    echo.
    pause
    exit /b
)

echo.
echo   Lege Ordnerstruktur an...
echo.

:: ================================================================================
:: R+MUNI <KUERZEL>\ - Blueprint Root mit vollstaendiger innerer Struktur
:: ================================================================================
echo [ R+MUNI !KUERZEL! ]
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!"

:: 00-model
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\00-model"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\00-model\00-archimate"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\00-model\00-archimate\00-archimateactive"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\00-model\00-archimate\01-archimateactivesub"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\00-model\00-archimate\99-mappingmodel"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\00-model\01-bpmn"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\00-model\01-bpmn\00-bpmnactive"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\00-model\01-bpmn\99-bpmnMUNI"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\00-model\02-xyvision"

:: 01-artifacts
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts"

:: 01-artifacts\00-xml
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\00-xml"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\00-xml\00-master"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\00-xml\01-mapping"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\00-xml\02-sync"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\00-xml\03-child"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\00-xml\03-child\00-archimatechild"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\00-xml\03-child\01-bpmnchild"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\00-xml\03-child\02-xychild"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\00-xml\04-import"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\00-xml\99-exports"

:: 01-artifacts\01-scripts
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\01-scripts"

:: 01-artifacts\02-csv
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\02-csv"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\02-csv\00-master"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\02-csv\01-mapping"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\02-csv\02-sync"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\02-csv\03-child"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\02-csv\04-import"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\02-csv\99-exports"

:: 01-artifacts\03-XLSX
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\03-XLSX"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\03-XLSX\00-master"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\03-XLSX\01-mapping"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\03-XLSX\02-sync"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\03-XLSX\03-child"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\03-XLSX\03-child\00-archimatechild"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\03-XLSX\03-child\01-bpmnchild"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\03-XLSX\03-child\02-xychild"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\03-XLSX\04-import"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\03-XLSX\99-exports"

:: 01-artifacts\04-flow
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\04-flow"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\04-flow\00-archimateFLW"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\04-flow\01-bpmnFLW"

:: 01-artifacts\05-reports
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\05-reports"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\05-reports\00-archimate"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\05-reports\01-bpmn"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\01-artifacts\05-reports\99-html"

:: 02-stages
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\02-stages"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\02-stages\00-archimatearchive"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\02-stages\01-bpmnarchive"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\02-stages\02-xyarchive"
call :MKDIR "!ROOT!\R+MUNI !KUERZEL!\02-stages\99-logs"

:: ================================================================================
:: R+MUNI Archiv <KUERZEL>\
:: ================================================================================
echo.
echo [ R+MUNI Archiv !KUERZEL! ]
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\backup"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\doku"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\doku\R+MUNI Doku-!KUERZEL!"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\doku\R+MUNI Doku-!KUERZEL!\00-governance"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\doku\R+MUNI Doku-!KUERZEL!\01-principles"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\doku\R+MUNI Doku-!KUERZEL!\02-how2"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\doku\R+MUNI Doku-!KUERZEL!\03-roesetta_stone"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\doku\R+MUNI Doku-!KUERZEL!\04-notes"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\doku\R+MUNI Doku-!KUERZEL!\05-backlog"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\doku\R+MUNI Doku-!KUERZEL!\06-sprints"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\model"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\restore"
call :MKDIR "!ROOT!\R+MUNI Archiv !KUERZEL!\scripts"

:: ================================================================================
:: R+MUNI Doku <KUERZEL>\
:: ================================================================================
echo.
echo [ R+MUNI Doku !KUERZEL! ]
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!"

call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku-creative"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku-creative\custo"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku-creative\flip"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku-creative\images"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku-creative\images\logo"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku-creative\images\r+muni"

call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku\00-governance"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku\01-principles"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku\02-how2"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku\03-roesetta_stone"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku\04-notes"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku\05-backlog"
call :MKDIR "!ROOT!\R+MUNI Doku !KUERZEL!\R+MUNI Doku\06-sprints"

:: ================================================================================
:: ABSCHLUSS
:: ================================================================================
echo.
echo ================================================================================
echo   Setup abgeschlossen.
echo ================================================================================
echo.
echo   Naechste Schritte:
echo   1. R+MUNI ZIP entpacken nach !ROOT!\R+MUNI !KUERZEL!\
echo      Dateien landen direkt in die vorhandenen Ordner.
echo   2. root.cfg oeffnen und Pfad pruefen:
echo      !ROOT!\R+MUNI !KUERZEL!\root.cfg
echo   3. Tools installieren gemaess Install.txt ^(Abschnitt STAMM^)
echo   4. CSV00 ausfuehren als erster Funktionstest
echo.
echo   Dokumentation: !ROOT!\R+MUNI !KUERZEL!\Install.txt
echo.
pause
exit /b

:: ================================================================================
:: HILFSFUNKTION: Ordner anlegen mit Feedback
:: ================================================================================
:MKDIR
if not exist %1 (
    mkdir %1 >nul 2>&1
    echo   [OK] Angelegt : %~1
) else (
    echo   [--] Existiert: %~1
)
exit /b
