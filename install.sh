#!/bin/bash
set -e

echo "🚀 Installation du ARTherapee Compagnon..."

# Chemins
CONFIG_DIR="$HOME/.config/ART/usercommands"
APP_DIR="$HOME/Programmes/ARTcompagnon"
TASKS_DIR="$APP_DIR/custom-tasks"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Créer les dossiers
echo "📁 Création des dossiers..."
mkdir -p "$CONFIG_DIR"
mkdir -p "$TASKS_DIR"

# 2. Copier les fichiers
echo "📋 Installation du programme..."
cp "$SCRIPT_DIR/select-editor.py" "$APP_DIR/"
cp "$SCRIPT_DIR/select-editor-config.json" "$APP_DIR/"
cp "$SCRIPT_DIR/logo.png" "$APP_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/install.sh" "$APP_DIR/"
chmod +x "$APP_DIR/select-editor.py"

# 3. Créer le fichier de config ART
echo "⚙️  Configuration ART..."
cat > "$CONFIG_DIR/select-editor.txt" << 'EOF'
[select-editor]
name=Select Editor
description=Le ARTherapee Compagnon - Gérez vos éditeurs et scripts
executable=$HOME/Programmes/ARTcompagnon/select-editor.py
output-file-extension=dng
EOF

# Remplacer $HOME par le chemin réel
sed -i "s|\$HOME|$HOME|g" "$CONFIG_DIR/select-editor.txt"

echo "✅ Installation réussie!"
echo ""
echo "📍 Chemins créés:"
echo "   - Config ART: $CONFIG_DIR/"
echo "   - Programme: $APP_DIR/"
echo "   - Custom-tasks: $TASKS_DIR/"
echo ""
echo "🎯 Prêt! Relancez ART et cliquez sur 'External Editor'"
