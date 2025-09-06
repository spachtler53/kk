# Discord Logo GIF Automatisierung - Makefile
# Vereinfacht häufige Operationen

.PHONY: help discord discord-small discord-large banner custom clean watch install list config

# Standard-Ziel
discord: install
	@echo "🎬 Erstelle Standard Discord Logo GIF..."
	python3 generate-discord-gif.py discord

# Verschiedene Presets
discord-small: install
	@echo "🎬 Erstelle kleines Discord Logo GIF..."
	python3 generate-discord-gif.py discord-klein

discord-large: install
	@echo "🎬 Erstelle großes Discord Logo GIF..."
	python3 generate-discord-gif.py discord-gross

banner: install
	@echo "🎬 Erstelle quadratisches Banner GIF..."
	python3 generate-discord-gif.py banner

# Benutzerdefiniert mit häufigen Einstellungen
custom: install
	@echo "🎬 Erstelle benutzerdefiniertes GIF..."
	python3 generate-discord-gif.py --custom --size 512 --glow medium

# Datei-Überwachung
watch: install
	@echo "👀 Starte Datei-Überwachung (Ctrl+C zum Beenden)..."
	python3 generate-discord-gif.py discord --watch

# Verfügbare Presets anzeigen
list: install
	@echo "📋 Verfügbare Presets:"
	python3 generate-discord-gif.py --list

# Konfigurationsdatei erstellen
config: install
	@echo "⚙️ Erstelle Konfigurationsdatei..."
	python3 generate-discord-gif.py --init-config

# Dependencies installieren
install:
	@echo "📦 Installiere Dependencies..."
	@pip install pillow --quiet --user 2>/dev/null || true

# Installiere optionale Dependencies für Datei-Überwachung
install-watch:
	@echo "📦 Installiere Datei-Überwachung Dependencies..."
	pip install watchdog --user

# Aufräumen
clean:
	@echo "🧹 Räume temporäre Dateien auf..."
	rm -rf build/
	rm -f assets/discord_logo.gif

# Alles aufräumen (inkl. Konfiguration)
clean-all: clean
	@echo "🧹 Räume alle generierten Dateien auf..."
	rm -f discord-gif-config.json

# Hilfe anzeigen
help:
	@echo "Discord Logo GIF Automatisierung"
	@echo "================================="
	@echo ""
	@echo "Verfügbare Befehle:"
	@echo "  make discord       - Erstelle Standard Discord GIF (512px)"
	@echo "  make discord-small - Erstelle kleines Discord GIF (256px)"
	@echo "  make discord-large - Erstelle großes Discord GIF (1024px)"
	@echo "  make banner        - Erstelle quadratisches Banner GIF"
	@echo "  make custom        - Erstelle benutzerdefiniertes GIF"
	@echo "  make watch         - Überwache Logo-Datei und regeneriere automatisch"
	@echo "  make list          - Zeige verfügbare Presets"
	@echo "  make config        - Erstelle Konfigurationsdatei"
	@echo "  make install       - Installiere Python Dependencies"
	@echo "  make install-watch - Installiere Dependencies für Datei-Überwachung"
	@echo "  make clean         - Lösche generierte GIFs"
	@echo "  make clean-all     - Lösche alle generierten Dateien"
	@echo "  make help          - Zeige diese Hilfe"
	@echo ""
	@echo "Beispiele:"
	@echo "  make discord                    # Schnelle Standard-Erstellung"
	@echo "  make watch                      # Automatische Regenerierung"
	@echo "  make clean && make discord      # Neu erstellen"
	@echo ""
	@echo "Dateien:"
	@echo "  assets/logo.png        - Quell-Logo (erforderlich)"
	@echo "  assets/discord_logo.gif - Generiertes animiertes GIF"