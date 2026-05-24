#!/bin/bash

################################
# Setup - ARTherapee Compagnon
# Version 2.0 (Améliorate)
################################

echo ""
echo "========================================="
echo "Configuration d'ARTherapee Compagnon v2.0"
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
echo "🔍 Recherche d'ART compilé..."

# Paramètre de test pour simuler l'absence d'ART
if [ "$1" = "--test-no-art" ]; then
    echo "🧪 MODE TEST: Simulation d'absence d'ART compilé"
    ART_FOUND="non"
    echo "⚠️  ART compilé non détecté"
else
    # Détection normale
    ART_FOUND="non"
    
    if command -v ART &> /dev/null; then
        ART_FOUND="natif"
        echo "✅ ART compilé trouvé (installation native)"
    elif command -v flatpak &> /dev/null && flatpak list --app 2>/dev/null | grep -q "us.pixls.art.ART"; then
        ART_FOUND="flatpak"
        echo "⚠️  ART Flatpak détecté"
    else
        ART_FOUND="non"
        echo "⚠️  ART compilé non détecté"
    fi
fi

echo ""

# Si ART pas trouvé, afficher fenêtre de confirmation
if [ "$ART_FOUND" = "non" ]; then
    zenity --question \
        --title="Attention - ART compilé non détecté" \
        --text="Vous n'avez pas d'ART compilé.\n\nCela n'empêche pas l'installation toutefois.\nEn fin d'installation, vous aurez des chemins\nde dossier à vérifier.\n\nVoulez-vous continuer ?" \
        --no-wrap
    
    if [ $? -ne 0 ]; then
        echo "❌ Installation annulée par l'utilisateur"
        exit 0
    fi
    echo "✅ L'utilisateur a choisi de continuer"
    echo ""
fi

# ============================================
# ÉTAPE 3 : Créer les dossiers
# ============================================
echo "📁 Création des dossiers de configuration..."
mkdir -p ~/.config/ART/usercommands
mkdir -p ~/.config/ARTcompagnon

echo "✅ Dossiers créés"
echo ""

# ============================================
# ÉTAPE 4 : Générer le fichier select-editor.txt
# ============================================
echo "⚙️  Génération de select-editor.txt..."

cat > ~/.config/ART/usercommands/select-editor.txt << EOF
[ART UserCommand]
Label=Le ARTherapee Compagnon
Command=$SCRIPT_DIR/select-editor.py
FileType=raw|jpg|jpeg|tif|tiff|png
NumArgs=1
EOF

echo "✅ Fichier généré :"
echo "   ~/.config/ART/usercommands/select-editor.txt"
echo ""

# ============================================
# ÉTAPE 5 : Générer le fichier de config ARTcompagnon
# ============================================
echo "⚙️  Génération d'artcompagnon-config.json..."

cat > ~/.config/ARTcompagnon/artcompagnon-config.json << EOFCONFIG
{
  "theme": "defaut",
  "language": "fr"
}
EOFCONFIG

echo "✅ Fichier généré :"
echo "   ~/.config/ARTcompagnon/artcompagnon-config.json"
echo ""

# ============================================
# ÉTAPE 6 : Vérification finale
# ============================================
echo "🔍 Vérification..."

if [ -f ~/.config/ART/usercommands/select-editor.txt ] && [ -f ~/.config/ARTcompagnon/artcompagnon-config.json ]; then
    echo "✅ Configuration correcte!"
    echo ""
else
    echo "❌ ERREUR : Un fichier n'a pas pu être créé"
    zenity --error \
        --title="Erreur d'installation" \
        --text="Un ou plusieurs fichiers n'ont pas pu être créés.\nVérifiez les permissions de votre répertoire personnel."
    exit 1
fi

# ============================================
# ÉTAPE 7 : Fenêtre de récap finale
# ============================================
RECAP_MESSAGE="✅ ARTcompagnon installé avec succès!

⚠️ ATTENTION: Certains chemins de dossier pourraient 
être différents sur votre install. Vérifiez les 
chemins des dossiers ci-dessous.

📁 CHEMINS DES SCRIPTS:
   • Bash: ~/.config/ART/usercommands/bash/
   • Python: ~/.config/ART/usercommands/python/
   • Lua: ~/.config/ART/usercommands/lua/
   • CTL: ~/.config/ART/ctlscripts/
   • Aide: ~/Documents/ARTcompagnon-Scripts-Help/

(~/.config/ est un dossier caché - appuyez sur Ctrl+H 
dans le gestionnaire de fichiers pour l'afficher)

📝 À FAIRE MAINTENANT (IMPORTANT):
   1. Lancez ART
   2. Allez dans Préférences de ART → Onglet Général 
      → Editeur externe
   3. Copiez ce chemin et collez-le dans 
      \"Ligne de commande personnalisée\":

$SCRIPT_DIR/select-editor.py

   4. Cliquez OK

🎉 C'est fait!"

zenity --info \
    --title="ARTcompagnon - Installation terminée" \
    --text="$RECAP_MESSAGE" \
    --no-wrap \
    --width=700 \
    --height=500

echo ""
echo "🎉 ARTcompagnon est prêt!"
echo ""
