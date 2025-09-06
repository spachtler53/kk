#!/bin/bash
# Discord Logo GIF Generator - Unix/Linux/MacOS Script
# Vereinfachtes Interface für die GIF-Erstellung

set -e

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktionen
print_header() {
    echo -e "${BLUE}🎬 Discord Logo GIF Generator${NC}"
    echo "=================================="
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

check_dependencies() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 ist nicht installiert!"
        exit 1
    fi
    
    if ! python3 -c "import PIL" &> /dev/null; then
        print_warning "Pillow nicht gefunden, installiere..."
        pip3 install --user pillow
    fi
}

show_help() {
    print_header
    echo
    echo "Verwendung: $0 [OPTION]"
    echo
    echo "Optionen:"
    echo "  discord          Standard Discord Icon (512px)"
    echo "  discord-small    Kleines Discord Icon (256px)" 
    echo "  discord-large    Großes Discord Icon (1024px)"
    echo "  banner           Quadratisches Banner"
    echo "  custom           Benutzerdefinierte Einstellungen"
    echo "  watch            Datei-Überwachung starten"
    echo "  list             Verfügbare Presets anzeigen"
    echo "  help             Diese Hilfe anzeigen"
    echo
    echo "Beispiele:"
    echo "  $0 discord       # Standard Discord GIF erstellen"
    echo "  $0 watch         # Automatische Regenerierung"
    echo "  $0 list          # Alle Presets anzeigen"
}

# Hauptfunktion
main() {
    local preset=${1:-"help"}
    
    case $preset in
        "help"|"-h"|"--help")
            show_help
            ;;
        "discord"|"discord-small"|"discord-large"|"banner"|"custom")
            print_header
            check_dependencies
            print_info "Erstelle GIF mit Preset: $preset"
            
            if [[ "$preset" == "discord-small" ]]; then
                preset="discord-klein"
            elif [[ "$preset" == "discord-large" ]]; then
                preset="discord-gross"
            fi
            
            if python3 generate-discord-gif.py "$preset"; then
                print_success "GIF erfolgreich erstellt!"
                if [[ -f "assets/discord_logo.gif" ]]; then
                    local size=$(ls -lh assets/discord_logo.gif | awk '{print $5}')
                    print_info "Dateigröße: $size"
                    print_info "Speicherort: assets/discord_logo.gif"
                fi
            else
                print_error "Fehler bei der GIF-Erstellung!"
                exit 1
            fi
            ;;
        "watch")
            print_header
            check_dependencies
            print_info "Starte Datei-Überwachung..."
            print_warning "Drücke Ctrl+C zum Beenden"
            python3 generate-discord-gif.py discord --watch
            ;;
        "list")
            print_header
            check_dependencies
            python3 generate-discord-gif.py --list
            ;;
        *)
            print_error "Unbekannte Option: $preset"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Script ausführen
main "$@"