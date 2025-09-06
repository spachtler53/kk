# Discord Logo GIF Automatisierung

Dieses Repository automatisiert die Erstellung von animierten Discord-Logo GIFs mit Glow-Effekten und Pulsanimationen.

## 🚀 Automatische Features

### GitHub Actions Automatisierung

Das Repository erstellt automatisch GIFs in folgenden Situationen:

1. **Bei Logo-Änderungen**: Wenn eine PNG-Datei in `assets/` gepusht wird
2. **Wöchentlich**: Jeden Sonntag um 12:00 UTC
3. **Manuell**: Über GitHub Actions mit vollständiger Anpassung

### Lokale Automatisierung

Mit dem `generate-discord-gif.py` Script können Sie GIFs lokal erstellen:

```bash
# Verfügbare Presets anzeigen
python3 generate-discord-gif.py --list

# Standard Discord Icon erstellen
python3 generate-discord-gif.py discord

# Kleine Version erstellen
python3 generate-discord-gif.py discord-klein

# Mit Datei-Überwachung (regeneriert automatisch bei Änderungen)
python3 generate-discord-gif.py discord --watch
```

## 📁 Dateistruktur

```
├── assets/
│   ├── logo.png           # Quell-Logo (wird überwacht)
│   └── discord_logo.gif   # Generiertes animiertes GIF
├── .github/workflows/
│   ├── discord-logo.yml   # GitHub Actions Workflow
│   └── scripts/
│       └── glow_pulse.py  # Core GIF-Generierungsscript
├── generate-discord-gif.py # Lokales Automatisierungsscript
└── discord-gif-config.json # Optionale Konfigurationsdatei
```

## 🎨 Verfügbare Presets

| Preset | Größe | Frames | FPS | Glow | Beschreibung |
|--------|-------|--------|-----|------|--------------|
| `discord` | 512px | 40 | 20 | medium | Standard Discord Icon |
| `discord-klein` | 256px | 30 | 15 | dezent | Kleines Discord Icon |
| `discord-gross` | 1024px | 50 | 25 | kräftig | Großes Discord Icon |
| `banner` | 512px | 60 | 30 | medium | Quadratisches Banner |

## ⚙️ Konfiguration

### Automatische Triggers konfigurieren

Die GitHub Actions können in `.github/workflows/discord-logo.yml` angepasst werden:

```yaml
on:
  push:
    branches: [main]
    paths: ['assets/*.png']  # Überwacht PNG-Dateien in assets/
  schedule:
    - cron: '0 12 * * 0'     # Sonntags um 12:00 UTC
```

### Lokale Konfiguration

Erstelle eine `discord-gif-config.json` für benutzerdefinierte Einstellungen:

```bash
python3 generate-discord-gif.py --init-config
```

Beispiel-Konfiguration:
```json
{
  "presets": {
    "mein-preset": {
      "size": 400,
      "frames": 30,
      "fps": 15,
      "glow": "medium",
      "circle": true,
      "description": "Mein benutzerdefiniertes Preset"
    }
  },
  "paths": {
    "input": "assets/logo.png",
    "output": "assets/discord_logo.gif"
  }
}
```

## 🛠️ Manuelle Verwendung

### GitHub Actions (Web Interface)

1. Gehe zu "Actions" → "Discord Logo GIF"
2. Klicke "Run workflow"
3. Wähle gewünschte Parameter:
   - **src_path**: Pfad zur PNG-Datei
   - **size**: Größe in Pixeln (z.B. 512)
   - **frames**: Anzahl Animationsframes
   - **fps**: Frames pro Sekunde
   - **glow**: Intensität (dezent/medium/kraeftig)
   - **circle**: Runde Beschneidung für Discord-Style
   - **commit_to_repo**: Automatisch zum Repository hinzufügen

### Lokales Script

```bash
# Mit Standard-Preset
python3 generate-discord-gif.py discord

# Benutzerdefinierte Einstellungen
python3 generate-discord-gif.py --custom --size 256 --glow dezent --no-circle

# Mit eigenen Dateipfaden
python3 generate-discord-gif.py discord --input mein-logo.png --output mein-gif.gif

# Mit Datei-Überwachung (regeneriert bei Änderungen)
python3 generate-discord-gif.py discord --watch
```

### Core Script direkt

```bash
python3 .github/workflows/scripts/glow_pulse.py \
  --in assets/logo.png \
  --out assets/discord_logo.gif \
  --size 512 \
  --frames 40 \
  --fps 20 \
  --pulse-bright 0.38 \
  --pulse-blur 7.0 \
  --max-rotate 1.5 \
  --keep-circle
```

## 🔧 Installation & Requirements

### Python Dependencies
```bash
pip install pillow
```

### Für Datei-Überwachung (optional)
```bash
pip install watchdog
```

### GitHub Repository Setup
1. Stelle sicher, dass Actions aktiviert sind
2. Lege dein Logo als `assets/logo.png` ab
3. Die Automatisierung startet beim nächsten Push oder manuell

## 📊 Glow-Einstellungen

| Intensität | Helligkeit | Blur | Rotation | Verwendung |
|------------|------------|------|----------|------------|
| `dezent` | 0.28 | 6.0px | 1.0° | Subtile Effekte |
| `medium` | 0.38 | 7.0px | 1.5° | Ausgewogener Standard |
| `kraeftig` | 0.50 | 8.5px | 2.0° | Auffällige Animationen |

## 🎯 Verwendungsszenarien

- **Discord Server Icons**: Animierte Serverlogos
- **Profilbilder**: Auffällige animierte Avatare  
- **Banner**: Quadratische animierte Banner ohne Rundung
- **Social Media**: Animierte Logos für verschiedene Plattformen
- **Websites**: Dynamische Logo-Animationen

## 🚨 Troubleshooting

### "Source image not found"
- Stelle sicher, dass `assets/logo.png` existiert
- Prüfe den Dateipfad in der Konfiguration

### "Script not found"
- Stelle sicher, dass `.github/workflows/scripts/glow_pulse.py` existiert
- Repository vollständig geklont?

### Schlechte Qualität
- Verwende hochauflösende PNG-Eingabebilder
- Experimentiere mit verschiedenen Presets
- Reduziere Frames/FPS für kleinere Dateien

### GitHub Actions schlägt fehl
- Prüfe ob Actions in den Repository-Einstellungen aktiviert sind
- Überprüfe die Logs in der Actions-Übersicht
- Stelle sicher, dass die Quell-PNG-Datei committet ist