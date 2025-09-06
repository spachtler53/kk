#!/usr/bin/env python3
"""
Lokales Automatisierungsskript für Discord-Logo GIF-Erstellung
Automatisiert die GIF-Generierung mit vordefinierten Presets
"""

import os
import sys
import argparse
import json
from pathlib import Path
import subprocess

# Standard-Konfiguration
DEFAULT_CONFIG = {
    "presets": {
        "discord": {
            "size": 512,
            "frames": 40,
            "fps": 20,
            "glow": "medium",
            "circle": True,
            "description": "Standard Discord Icon (512px, mittleres Glow)"
        },
        "discord-klein": {
            "size": 256,
            "frames": 30,
            "fps": 15,
            "glow": "dezent",
            "circle": True,
            "description": "Kleines Discord Icon (256px, dezentes Glow)"
        },
        "discord-gross": {
            "size": 1024,
            "frames": 50,
            "fps": 25,
            "glow": "kraeftig",
            "circle": True,
            "description": "Großes Discord Icon (1024px, kräftiges Glow)"
        },
        "banner": {
            "size": 512,
            "frames": 60,
            "fps": 30,
            "glow": "medium",
            "circle": False,
            "description": "Quadratisches Banner ohne Rundung"
        }
    },
    "paths": {
        "input": "assets/logo.png",
        "output": "assets/discord_logo.gif",
        "script": ".github/workflows/scripts/glow_pulse.py"
    },
    "glow_settings": {
        "dezent": {"pulse_bright": 0.28, "pulse_blur": 6.0, "max_rotate": 1.0},
        "medium": {"pulse_bright": 0.38, "pulse_blur": 7.0, "max_rotate": 1.5},
        "kraeftig": {"pulse_bright": 0.50, "pulse_blur": 8.5, "max_rotate": 2.0}
    }
}

def load_config():
    """Lädt Konfiguration aus discord-gif-config.json falls vorhanden"""
    config_file = Path("discord-gif-config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            # Merge with defaults
            config = DEFAULT_CONFIG.copy()
            config.update(user_config)
            return config
        except Exception as e:
            print(f"Warnung: Fehler beim Laden der Konfiguration: {e}")
            print("Verwende Standard-Konfiguration")
    return DEFAULT_CONFIG

def save_config(config):
    """Speichert aktuelle Konfiguration"""
    config_file = Path("discord-gif-config.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"Konfiguration gespeichert in {config_file}")

def list_presets(config):
    """Zeigt verfügbare Presets an"""
    print("Verfügbare Presets:")
    print("-" * 50)
    for name, preset in config["presets"].items():
        print(f"{name:15} - {preset['description']}")
        print(f"{'':15}   {preset['size']}px, {preset['frames']} Frames, {preset['fps']} FPS, Glow: {preset['glow']}")
        print()

def generate_gif(config, preset_name, input_path=None, output_path=None, watch=False):
    """Generiert GIF mit angegebenem Preset"""
    if preset_name not in config["presets"]:
        print(f"Fehler: Preset '{preset_name}' nicht gefunden!")
        return False
    
    preset = config["presets"][preset_name]
    glow_settings = config["glow_settings"][preset["glow"]]
    
    # Pfade bestimmen
    if input_path is None:
        input_path = config["paths"]["input"]
    if output_path is None:
        output_path = config["paths"]["output"]
    
    script_path = config["paths"]["script"]
    
    # Prüfe ob Eingabedatei existiert
    if not Path(input_path).exists():
        print(f"Fehler: Eingabedatei '{input_path}' nicht gefunden!")
        return False
    
    # Prüfe ob Script existiert
    if not Path(script_path).exists():
        print(f"Fehler: Script '{script_path}' nicht gefunden!")
        return False
    
    # Erstelle Ausgabeordner falls nötig
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Baue Kommando
    cmd = [
        "python3", script_path,
        "--in", input_path,
        "--out", output_path,
        "--size", str(preset["size"]),
        "--frames", str(preset["frames"]),
        "--fps", str(preset["fps"]),
        "--pulse-bright", str(glow_settings["pulse_bright"]),
        "--pulse-blur", str(glow_settings["pulse_blur"]),
        "--max-rotate", str(glow_settings["max_rotate"])
    ]
    
    if preset["circle"]:
        cmd.append("--keep-circle")
    
    print(f"Generiere GIF mit Preset '{preset_name}'...")
    print(f"Eingabe: {input_path}")
    print(f"Ausgabe: {output_path}")
    print(f"Größe: {preset['size']}px, Frames: {preset['frames']}, FPS: {preset['fps']}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ GIF erfolgreich erstellt!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler bei der GIF-Erstellung:")
        print(f"Befehl: {' '.join(cmd)}")
        print(f"Fehler: {e.stderr}")
        return False

def watch_and_generate(config, preset_name):
    """Überwacht Eingabedatei und regeneriert automatisch"""
    try:
        import time
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("Fehler: 'watchdog' Paket nicht installiert.")
        print("Installiere mit: pip install watchdog")
        return
    
    input_path = Path(config["paths"]["input"])
    
    class LogoHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path == str(input_path.absolute()):
                print(f"Logo-Datei geändert: {event.src_path}")
                time.sleep(1)  # Kurz warten falls Datei noch geschrieben wird
                generate_gif(config, preset_name)
    
    observer = Observer()
    observer.schedule(LogoHandler(), str(input_path.parent), recursive=False)
    observer.start()
    
    print(f"👀 Überwache {input_path} für Änderungen...")
    print(f"🎬 Verwende Preset: {preset_name}")
    print("⏹️  Drücke Ctrl+C zum Beenden")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n✋ Überwachung beendet")
    observer.join()

def main():
    parser = argparse.ArgumentParser(
        description="Automatisierte Discord-Logo GIF-Erstellung",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  %(prog)s --list                          # Zeige verfügbare Presets
  %(prog)s discord                         # Generiere mit Discord-Preset
  %(prog)s discord-klein --watch           # Generiere und überwache Änderungen
  %(prog)s --custom --size 256 --glow dezent  # Benutzerdefinierte Einstellungen
  %(prog)s --init-config                   # Erstelle Konfigurationsdatei
        """
    )
    
    parser.add_argument("preset", nargs="?", help="Preset-Name (verwende --list um alle zu sehen)")
    parser.add_argument("--list", action="store_true", help="Zeige verfügbare Presets")
    parser.add_argument("--watch", action="store_true", help="Überwache Logo-Datei für Änderungen")
    parser.add_argument("--input", help="Eingabe-PNG-Datei (überschreibt Standard)")
    parser.add_argument("--output", help="Ausgabe-GIF-Datei (überschreibt Standard)")
    parser.add_argument("--init-config", action="store_true", help="Erstelle Konfigurationsdatei")
    
    # Custom-Optionen
    parser.add_argument("--custom", action="store_true", help="Verwende benutzerdefinierte Einstellungen")
    parser.add_argument("--size", type=int, help="Größe in Pixeln")
    parser.add_argument("--frames", type=int, help="Anzahl Frames")
    parser.add_argument("--fps", type=int, help="Frames pro Sekunde")
    parser.add_argument("--glow", choices=["dezent", "medium", "kraeftig"], help="Glow-Intensität")
    parser.add_argument("--no-circle", action="store_true", help="Keine runde Beschneidung")
    
    args = parser.parse_args()
    
    config = load_config()
    
    if args.init_config:
        save_config(config)
        return
    
    if args.list:
        list_presets(config)
        return
    
    if args.custom:
        # Erstelle temporäres Preset mit benutzerdefinierten Einstellungen
        custom_preset = {
            "size": args.size or 512,
            "frames": args.frames or 40,
            "fps": args.fps or 20,
            "glow": args.glow or "medium",
            "circle": not args.no_circle,
            "description": "Benutzerdefiniert"
        }
        config["presets"]["custom"] = custom_preset
        preset_name = "custom"
    else:
        if not args.preset:
            print("Fehler: Bitte gebe einen Preset-Namen an oder verwende --custom")
            print("Verwende --list um verfügbare Presets zu sehen")
            return 1
        preset_name = args.preset
    
    if args.watch:
        watch_and_generate(config, preset_name)
    else:
        success = generate_gif(config, preset_name, args.input, args.output)
        return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())