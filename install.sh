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
# ÉTAPE 6 : Vérifier / installer les dépendances (Python + terminal)
# ============================================
echo "🐍 Vérification des dépendances (Python + gnome-terminal)..."

# Détection du gestionnaire de paquets + noms de paquets adaptés à la distro
PKG_MGR=""; PKG_INSTALL=""
PYQT_PKG=""; TK_PKG=""; PIL_PKG=""; RL_PKG=""
if command -v dnf &>/dev/null; then
    PKG_MGR="dnf"; PKG_INSTALL="sudo dnf install -y"
    PYQT_PKG="python3-qt5-base"; TK_PKG="python3-tkinter"
    PIL_PKG="python3-pillow python3-pillow-tk"; RL_PKG="python3-reportlab"
elif command -v apt &>/dev/null; then
    PKG_MGR="apt"; PKG_INSTALL="sudo apt install -y"
    PYQT_PKG="python3-pyqt5"; TK_PKG="python3-tk"
    PIL_PKG="python3-pil python3-pil.imagetk"; RL_PKG="python3-reportlab"
elif command -v pacman &>/dev/null; then
    PKG_MGR="pacman"; PKG_INSTALL="sudo pacman -S --noconfirm"
    PYQT_PKG="python-pyqt5"; TK_PKG="tk"
    PIL_PKG="python-pillow"; RL_PKG="python-reportlab"
elif command -v zypper &>/dev/null; then
    PKG_MGR="zypper"; PKG_INSTALL="sudo zypper install -y"
    PYQT_PKG="python3-qt5"; TK_PKG="python3-tk"
    PIL_PKG="python3-Pillow python3-Pillow-tk"; RL_PKG="python3-reportlab"
fi

# Repérer les modules manquants et cumuler les paquets correspondants
TO_INSTALL=""
python3 -c "import PyQt5.QtWidgets" &>/dev/null || TO_INSTALL="$TO_INSTALL $PYQT_PKG"
python3 -c "import tkinter"          &>/dev/null || TO_INSTALL="$TO_INSTALL $TK_PKG"
python3 -c "import PIL.ImageTk"      &>/dev/null || TO_INSTALL="$TO_INSTALL $PIL_PKG"
python3 -c "import reportlab"        &>/dev/null || TO_INSTALL="$TO_INSTALL $RL_PKG"
# gnome-terminal : requis par les scripts (terminal de référence ; même nom de paquet partout)
command -v gnome-terminal            &>/dev/null || TO_INSTALL="$TO_INSTALL gnome-terminal"
TO_INSTALL="$(echo $TO_INSTALL | xargs)"

if [ -z "$TO_INSTALL" ]; then
    echo "✅ Toutes les dépendances Python sont présentes"
elif [ -z "$PKG_MGR" ]; then
    zenity --warning --no-wrap --title="Dépendances Python manquantes" \
        --text="Modules manquants : $TO_INSTALL\n\nGestionnaire de paquets non reconnu.\nInstallez ces paquets via votre distribution, puis relancez ART."
else
    echo "📦 Dépendances manquantes : $TO_INSTALL"
    if zenity --question --no-wrap --title="Installer les dépendances Python ?" \
        --text="ARTcompagnon doit installer :\n\n   $TO_INSTALL\n\nCommande :\n   $PKG_INSTALL $TO_INSTALL\n\n(le mot de passe administrateur vous sera demandé)\n\nContinuer ?"; then
        [ "$PKG_MGR" = "apt" ] && sudo apt update
        $PKG_INSTALL $TO_INSTALL
    else
        echo "ℹ️  Installation des dépendances ignorée par l'utilisateur"
    fi
    # PyQt5 est INDISPENSABLE au lancement de l'appli : re-vérifier
    if python3 -c "import PyQt5.QtWidgets" &>/dev/null; then
        echo "✅ PyQt5 opérationnel"
    else
        zenity --warning --no-wrap --title="PyQt5 toujours absent" \
            --text="PyQt5 n'a pas pu être installé automatiquement.\n\nInstallez-le à la main :\n   $PKG_INSTALL $PYQT_PKG\n\nRepli universel (si le paquet distro manque) :\n   python3 -m pip install --user PyQt5"
    fi
fi
echo ""

# ============================================
# ÉTAPE 7 : Vérification finale
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
# ÉTAPE 8 : Fenêtre de récap finale
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
