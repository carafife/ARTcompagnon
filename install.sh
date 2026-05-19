#!/bin/bash

################################
# Setup - ARTherapee Compagnon
# Version 1.0
################################

echo ""
echo "========================================="
echo "Configuration d'ARTherapee Compagnon v1.0"
echo "========================================="
echo ""

# ============================================
# ÉTAPE 1 : Se localiser
# ============================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "✅ ARTcompagnon détecté à :"
echo "   $SCRIPT_DIR"
echo ""

# ============================================
# ÉTAPE 2 : Vérifier que ART est installé
# ============================================
echo "🔍 Recherche d'ART..."

if command -v ART &> /dev/null; then
    ART_FOUND="natif"
    echo "✅ ART trouvé (installation native)"
elif command -v flatpak &> /dev/null && flatpak list --app 2>/dev/null | grep -q "us.pixls.art.ART"; then
    ART_FOUND="flatpak"
    echo "⚠️  ART Flatpak détecté"
    echo ""
    echo "ℹ️  ARTcompagnon v1.0 n'est pas compatible avec Flatpak/AppImage"
    echo "   Pour la configuration manuelle, consultez :"
    echo "   📖 README.md → Section 'Flatpak/AppImage - Installation manuelle'"
    echo ""
    exit 0
else
    echo "❌ ERREUR : ART n'a pas été trouvé!"
    echo "   Assurez-vous qu'ART est installé depuis GitHub"
    exit 1
fi
echo ""

# ============================================
# ÉTAPE 3 : Créer les dossiers
# ============================================
echo "📁 Création des dossiers de configuration..."
mkdir -p ~/.config/ART/usercommands

echo "✅ Dossier créé"
echo ""

# ============================================
# ============================================
# ÉTAPE 3bis : Créer dossier ARTcompagnon config
# ============================================
echo "📁 Création du dossier de config ARTcompagnon..."
mkdir -p ~/.config/ARTcompagnon
echo "✅ Dossier créé"
echo ""
# ============================================
# ÉTAPE 4bis : Générer le fichier de config ARTcompagnon
# ============================================
echo "⚙️  Génération d'artcompagnon-config.json..."
cat > ~/.config/ARTcompagnon/artcompagnon-config.json << EOFCONFIG
{
  "theme": "defaut"
}
EOFCONFIG
echo "✅ Fichier généré :"
echo "   ~/.config/ARTcompagnon/artcompagnon-config.json"
echo ""

# ÉTAPE 4 : Générer le fichier de config
# ============================================
echo "⚙️  Génération de select-editor.txt..."

cat > ~/.config/ART/usercommands/select-editor.txt << EOF
[ART UserCommand]
Label=Le ARTherapee Compagnon
Command=$SCRIPT_DIR/select-editor.py
FileType=raw
EOF

echo "✅ Fichier généré :"
echo "   ~/.config/ART/usercommands/select-editor.txt"
echo ""

# ============================================
# ÉTAPE 5 : Vérification finale
# ============================================
echo "🔍 Vérification..."

if [ -f ~/.config/ART/usercommands/select-editor.txt ]; then
    echo "✅ Configuration correcte!"
    echo ""
else
    echo "❌ ERREUR : Le fichier n'a pas pu être créé"
    exit 1
fi

# ============================================
# C'EST FINI !
# ============================================
echo ""
echo "🎉 ARTcompagnon est prêt!"
echo ""
echo "Prochaines étapes :"
echo "1. Relancez ART"
echo "   → ART Préférences → External Editor"
echo ""
echo "   Entrez le chemin complet :"
echo "   $SCRIPT_DIR/select-editor.py"
echo ""
echo "2. Ouvrez une image RAW"
echo ""
echo "3. Cliquez sur le bouton 'Editeur externe' ou appuyez sur Ctrl+E"
echo ""
echo "Bon travail ! 👍"
echo ""
