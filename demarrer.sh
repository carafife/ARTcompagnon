#!/bin/bash
# =====================================================================
# demarrer.sh — Accueil apres "git clone".
# Explique les 2 installateurs et propose de les lancer, dans le bon
# ordre (ART d'abord, Compagnon ensuite). Fenetre zenity si dispo,
# sinon menu terminal.
# =====================================================================
DIR="$(cd "$(dirname "$0")" && pwd)"
ART_SCRIPT="$DIR/installer-art.sh"
COMP_SCRIPT="$DIR/install.sh"

INTRO="Bienvenue dans ART Compagnon !

Vous avez recupere 2 installateurs dans :
$DIR

  1) installer-art.sh
     -> installe / met a jour ART (bundle officiel, CTL + OCIO inclus)

  2) install.sh
     -> installe le Compagnon (lanceur de scripts dans ART)

Conseil : installez d'abord ART, puis le Compagnon.
Si vous avez deja un ART complet, l'installateur ART vous le dira
et ne touchera a rien."

run_art(){  [ -f "$ART_SCRIPT" ]  && bash "$ART_SCRIPT" "$@"  || echo "installer-art.sh introuvable dans $DIR"; }
run_comp(){ [ -f "$COMP_SCRIPT" ] && bash "$COMP_SCRIPT"      || echo "install.sh introuvable dans $DIR"; }

if command -v zenity >/dev/null 2>&1; then
    CHOICE=$(zenity --list --title="ART Compagnon — Demarrage" \
        --text="$INTRO" \
        --column="Choix" --column="Action" \
        "art"       "1) Installer / mettre a jour ART (a faire en premier)" \
        "compagnon" "2) Installer le Compagnon" \
        "deux"      "Faire les deux : ART puis Compagnon" \
        --width=680 --height=380 2>/dev/null)
    case "$CHOICE" in
        art)       run_art ;;
        compagnon) run_comp ;;
        deux)      run_art && run_comp ;;
        *)         echo "Aucune action. A bientot !" ;;
    esac
else
    echo "======================================================"
    echo "$INTRO"
    echo "======================================================"
    echo "  [1] Installer / mettre a jour ART"
    echo "  [2] Installer le Compagnon"
    echo "  [3] Les deux (ART puis Compagnon)"
    echo "  [autre] Ne rien faire"
    read -r -p "Votre choix ? " r
    case "$r" in
        1) run_art ;;
        2) run_comp ;;
        3) run_art && run_comp ;;
        *) echo "Aucune action. A bientot !" ;;
    esac
fi
