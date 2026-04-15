# ==============================================================================
# SVG05-resize.py
# ==============================================================================
# Reihe   : SVG — Image to SVG Konvertierung
# Aufgabe : Bilder auf A4 Querformat Auflösung optimieren (optional)
# Output  : 02-stages\99-logs\SVG05-resize.log
# Abhängig: HLP00_resolve_root.py, Pillow (pip install pillow)
# ==============================================================================
# Zielauflösung: 150 DPI, max 1754px Breite (A4 Querformat, gute Bildschirmqualität)
# Originaldateien bleiben erhalten — optimierte Kopien werden im
# svg_source_folder abgelegt (überschreiben das Original nur wenn
# svg_overwrite=true gesetzt ist).
#
# Reihenfolge mit diesem Script:
#   SVG00 → SVG01 → SVG02 → SVG05 → SVG01 (nochmal) → SVG03/SVG04 → SVG06
#
# Abhängigkeit: Pillow
#   pip install pillow
# ==============================================================================
# R+MUNI Blueprint | Stage S1.04 | 2026-04-12
# ==============================================================================

import os
import sys
from datetime import datetime

# ------------------------------------------------------------------------------
# Pillow prüfen
# ------------------------------------------------------------------------------
try:
    from PIL import Image
except ImportError:
    print("[SVG05] FEHLER: Pillow nicht installiert.")
    print("        Installieren mit: pip install pillow")
    sys.exit(1)

# ------------------------------------------------------------------------------
# HLP00 einbinden
# ------------------------------------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from HLP00_resolve_root import get_root_cfg
except ImportError:
    print("[SVG05] FEHLER: HLP00_resolve_root.py nicht gefunden.")
    sys.exit(1)

# ------------------------------------------------------------------------------
# Konstanten
# ------------------------------------------------------------------------------
SCRIPT_ID    = "SVG05"
CONFIG_NAME  = "svg_config.txt"
INVENTAR_LOG = "SVG01-inventory.log"
LOG_NAME     = "SVG05-resize.log"

# A4 Querformat bei 150 DPI = 1754 x 1240px
MAX_BREITE = 1754
MAX_HOEHE  = 1240

# ------------------------------------------------------------------------------
# Hilfsfunktionen
# ------------------------------------------------------------------------------

def parse_svg_config(config_path):
    result = {}
    with open(config_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                result[key.strip()] = value.strip()
    return result


def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_log(log_path, lines):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def format_groesse(path):
    try:
        b = os.path.getsize(path)
        if b < 1024:
            return f"{b} B"
        elif b < 1024 * 1024:
            return f"{b/1024:.1f} KB"
        else:
            return f"{b/(1024*1024):.1f} MB"
    except Exception:
        return "?"


def parse_inventar(inventar_path):
    """Liest SVG01-inventory.log — OK und RENAME_REQUIRED Einträge."""
    ergebnis = []
    STATUS_START    = 2
    DATEINAME_START = 2 + 18
    DATEINAME_ENDE  = DATEINAME_START + 45

    with open(inventar_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if len(line) < DATEINAME_START:
                continue
            status_teil = line[STATUS_START:STATUS_START + 18].strip()
            if status_teil in ("OK", "RENAME_REQUIRED"):
                dateiname = line[DATEINAME_START:DATEINAME_ENDE].strip()
                if dateiname and "." in dateiname and not dateiname.startswith(":"):
                    ergebnis.append((status_teil, dateiname))

    return ergebnis


def berechne_neue_groesse(breite, hoehe):
    """Berechnet neue Dimensionen unter Beibehaltung des Seitenverhältnisses.
    Nur verkleinern — niemals hochskalieren."""
    if breite <= MAX_BREITE and hoehe <= MAX_HOEHE:
        return breite, hoehe, False  # Kein Resize nötig

    faktor_breite = MAX_BREITE / breite
    faktor_hoehe  = MAX_HOEHE / hoehe
    faktor        = min(faktor_breite, faktor_hoehe)

    neue_breite = int(breite * faktor)
    neue_hoehe  = int(hoehe * faktor)
    return neue_breite, neue_hoehe, True


def ermittle_qualitaet(ext):
    """Gibt optimale Komprimierungsqualität je Format zurück."""
    if ext in ("jpg", "jpeg"):
        return 85   # JPEG: 85% — guter Sweet Spot Qualität/Größe
    return None     # PNG: verlustfrei, Qualität nicht relevant


# ------------------------------------------------------------------------------
# Hauptlogik
# ------------------------------------------------------------------------------

def main():
    log_lines = []
    zaehler   = {"OPTIMIERT": 0, "SKIP": 0, "UNVERAENDERT": 0, "FEHLER": 0}

    def log(status, message):
        line = f"[{ts()}] [{status:<7}] {message}"
        log_lines.append(line)
        print(line)

    log_lines.append("=" * 72)
    log_lines.append(f"  {SCRIPT_ID} — Resize / Compress (A4 Querformat, 150 DPI)")
    log_lines.append(f"  R+MUNI Blueprint | SVG-Reihe | {ts()}")
    log_lines.append("=" * 72)
    log_lines.append(f"  Ziel: max {MAX_BREITE} x {MAX_HOEHE} px | nur verkleinern, nie hochskalieren")
    log_lines.append(f"  JPEG Qualität: 85% | PNG: verlustfrei")
    log_lines.append(f"  Reihenfolge: SVG05 → SVG01 (nochmal) → SVG03/SVG04")
    log_lines.append("")

    # --- 1. root.cfg ---
    log_lines.append("--- 1. root.cfg ---")
    try:
        cfg        = get_root_cfg()
        rootfolder = cfg.get("<rootfolder>", "")
        stages     = cfg.get("<stages>", "")
        if not rootfolder:
            log("FEHLER", "<rootfolder> leer — root.cfg prüfen.")
            sys.exit(1)
        log("OK", f"rootfolder = {rootfolder}")
    except Exception as e:
        log("FEHLER", f"root.cfg Fehler: {e}")
        sys.exit(1)

    log_lines.append("")

    # --- 2. svg_config.txt ---
    log_lines.append("--- 2. svg_config.txt ---")
    config_path = os.path.join(rootfolder, "99-doku", CONFIG_NAME)
    if not os.path.isfile(config_path):
        log("FEHLER", f"svg_config.txt nicht gefunden: {config_path}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    try:
        svg_cfg = parse_svg_config(config_path)
    except Exception as e:
        log("FEHLER", f"svg_config.txt nicht lesbar: {e}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    source_folder = svg_cfg.get("svg_source_folder", "").strip()
    overwrite     = svg_cfg.get("svg_overwrite", "false").strip().lower() == "true"

    if not source_folder:
        log("FEHLER", "svg_source_folder leer — svg_config.txt prüfen.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    log("OK", f"svg_source_folder = {source_folder}")
    log("OK", f"svg_overwrite     = {str(overwrite).lower()}")
    log_lines.append("")

    # --- 3. Quellordner prüfen ---
    log_lines.append("--- 3. Quellordner ---")
    if not os.path.isdir(source_folder):
        log("FEHLER", f"svg_source_folder nicht gefunden: {source_folder}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)
    log("OK", f"Quellordner gefunden: {source_folder}")
    log_lines.append("")

    # --- 4. SVG01-inventory.log lesen ---
    log_lines.append("--- 4. SVG01-inventory.log ---")
    inventar_path = os.path.join(stages, "99-logs", INVENTAR_LOG)

    if not os.path.isfile(inventar_path):
        log("FEHLER", f"SVG01-inventory.log nicht gefunden: {inventar_path}")
        log("FEHLER", "SVG01 zuerst ausführen.")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    try:
        inventar = parse_inventar(inventar_path)
    except Exception as e:
        log("FEHLER", f"SVG01-inventory.log nicht lesbar: {e}")
        _finalize(log_lines, stages, LOG_NAME)
        sys.exit(1)

    log("OK", f"SVG01-inventory.log gelesen — {len(inventar)} Datei(en)")
    log_lines.append("")

    if not inventar:
        log("INFO", "Keine verarbeitbaren Dateien im Inventar — Abbruch.")
        _finalize(log_lines, stages, LOG_NAME)
        return

    # --- 5. Resize / Compress ---
    log_lines.append("--- 5. Resize / Compress ---")
    log_lines.append("")
    log_lines.append(f"  {'DATEINAME':<40} {'ORIGINAL':<15} {'NEU':<15} {'VORHER':<10} {'NACHHER':<10} STATUS")
    log_lines.append(f"  {'-'*40} {'-'*15} {'-'*15} {'-'*10} {'-'*10} {'-'*12}")

    for inv_status, dateiname in inventar:
        src_path = os.path.join(source_folder, dateiname)

        if not os.path.isfile(src_path):
            zeile = f"  {dateiname:<40} {'—':<15} {'—':<15} {'—':<10} {'—':<10} FEHLER (nicht gefunden)"
            log_lines.append(zeile)
            print(zeile)
            zaehler["FEHLER"] += 1
            continue

        ext = os.path.splitext(dateiname)[1].lstrip(".").lower()
        groesse_vorher = format_groesse(src_path)

        try:
            img = Image.open(src_path)

            # EXIF-Orientierung korrigieren (relevant für JPG von Kamera/Handy)
            try:
                from PIL import ImageOps
                img = ImageOps.exif_transpose(img)
            except Exception:
                pass

            orig_breite, orig_hoehe = img.size
            orig_str = f"{orig_breite}x{orig_hoehe}"

            neue_breite, neue_hoehe, resize_noetig = berechne_neue_groesse(
                orig_breite, orig_hoehe
            )
            neu_str = f"{neue_breite}x{neue_hoehe}"

            # Bereits klein genug — nur JPEG-Kompression anwenden wenn sinnvoll
            if not resize_noetig and ext not in ("jpg", "jpeg"):
                zeile = (f"  {dateiname:<40} {orig_str:<15} {neu_str:<15} "
                         f"{groesse_vorher:<10} {'—':<10} UNVERAENDERT")
                log_lines.append(zeile)
                print(zeile)
                zaehler["UNVERAENDERT"] += 1
                img.close()
                continue

            # Overwrite-Prüfung — Originaldatei wird überschrieben
            if not overwrite and resize_noetig:
                zeile = (f"  {dateiname:<40} {orig_str:<15} {neu_str:<15} "
                         f"{groesse_vorher:<10} {'—':<10} SKIP (overwrite=false)")
                log_lines.append(zeile)
                print(zeile)
                zaehler["SKIP"] += 1
                img.close()
                continue

            # Resize wenn nötig
            if resize_noetig:
                img = img.resize((neue_breite, neue_hoehe), Image.LANCZOS)

            # Speichern — Format beibehalten
            save_kwargs = {}
            if ext in ("jpg", "jpeg"):
                # RGB sicherstellen für JPEG (kein Alpha-Kanal)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                save_kwargs["quality"]  = 85
                save_kwargs["optimize"] = True
            elif ext == "png":
                save_kwargs["optimize"] = True

            img.save(src_path, **save_kwargs)
            img.close()

            groesse_nachher = format_groesse(src_path)
            zeile = (f"  {dateiname:<40} {orig_str:<15} {neu_str:<15} "
                     f"{groesse_vorher:<10} {groesse_nachher:<10} OPTIMIERT")
            log_lines.append(zeile)
            print(zeile)
            zaehler["OPTIMIERT"] += 1

        except Exception as e:
            zeile = (f"  {dateiname:<40} {'—':<15} {'—':<15} "
                     f"{groesse_vorher:<10} {'—':<10} FEHLER ({str(e)[:40]})")
            log_lines.append(zeile)
            print(zeile)
            zaehler["FEHLER"] += 1

    log_lines.append("")

    # --- Zusammenfassung ---
    gesamt = sum(zaehler.values())
    log_lines.append("=" * 72)
    log_lines.append(f"  ZUSAMMENFASSUNG")
    log_lines.append(f"  Verarbeitet       : {gesamt}")
    log_lines.append(f"  Optimiert         : {zaehler['OPTIMIERT']}")
    log_lines.append(f"  Unverändert       : {zaehler['UNVERAENDERT']}")
    log_lines.append(f"  Übersprungen      : {zaehler['SKIP']}")
    log_lines.append(f"  Fehler            : {zaehler['FEHLER']}")

    if zaehler["SKIP"] > 0:
        log_lines.append(f"")
        log_lines.append(f"  HINWEIS: {zaehler['SKIP']} Datei(en) übersprungen.")
        log_lines.append(f"           svg_overwrite=true setzen um Resize durchzuführen.")

    if zaehler["FEHLER"] > 0:
        log_lines.append(f"")
        log_lines.append(f"  WARNUNG: {zaehler['FEHLER']} Datei(en) fehlgeschlagen.")
        log_lines.append(f"           Log prüfen.")

    log_lines.append(f"")
    log_lines.append(f"  NÄCHSTER SCHRITT: SVG01 erneut ausführen um Inventar")
    log_lines.append(f"  zu aktualisieren, dann SVG03 oder SVG04 starten.")
    log_lines.append("=" * 72)

    print(f"\n[{SCRIPT_ID}] Optimiert: {zaehler['OPTIMIERT']} | "
          f"Unverändert: {zaehler['UNVERAENDERT']} | "
          f"Übersprungen: {zaehler['SKIP']} | Fehler: {zaehler['FEHLER']}")

    _finalize(log_lines, stages, LOG_NAME)


def _finalize(log_lines, stages, log_name):
    if not stages:
        print(f"\n[{SCRIPT_ID}] Log konnte nicht geschrieben werden — stages Pfad leer.")
        return
    try:
        log_path = os.path.join(stages, "99-logs", log_name)
        write_log(log_path, log_lines)
        print(f"[{SCRIPT_ID}] Log geschrieben: {log_path}")
    except Exception as e:
        print(f"[{SCRIPT_ID}] Log konnte nicht geschrieben werden: {e}")


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
