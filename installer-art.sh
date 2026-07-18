#!/bin/bash
# =====================================================================
# installer-art.sh
# Installe ou met a jour ART (l'editeur) depuis le bundle officiel
# (Releases GitHub artraweditor/ART) qui inclut DEJA le CTL + l'OCIO.
# Pose des liens ~/.local/bin/ART et ~/.local/bin/ART-cli.
# Ne touche QUE l'espace utilisateur (~/programs et ~/.local/bin).
#
# Options : --yes (ne pas demander confirmation)  --force (installer
#           le bundle meme si un ART avec CTL est deja present)
# =====================================================================
set -u

REPO="artraweditor/ART"
API="https://api.github.com/repos/${REPO}/releases/latest"
INSTALL_PARENT="${HOME}/programs"
BINDIR="${HOME}/.local/bin"

ASSUME_YES=0; FORCE=0
for a in "$@"; do
    case "$a" in
        --yes|-y) ASSUME_YES=1 ;;
        --force)  FORCE=1 ;;
    esac
done

G='\033[0;32m'; Y='\033[1;33m'; R='\033[0;31m'; B='\033[0;34m'; N='\033[0m'
info(){ echo -e "${B}==>${N} $1"; }
ok(){   echo -e "${G}OK ${N} $1"; }
warn(){ echo -e "${Y}!! ${N} $1"; }
err(){  echo -e "${R}ERREUR${N} $1"; }
has(){ command -v "$1" >/dev/null 2>&1; }

# Confirmation oui/non (zenity si dispo, sinon terminal). Retourne 0 si "oui".
ask_yes(){
    if has zenity; then
        zenity --question --no-wrap --title="$1" --text="$2" 2>/dev/null
    else
        echo -e "$2"; read -r -p "[o/N] " _r; case "$_r" in o|O|y|Y) return 0 ;; *) return 1 ;; esac
    fi
}

dl(){ # url dest
    if   has curl; then curl -fSL "$1" -o "$2"
    elif has wget; then wget -O "$2" "$1"
    else err "Ni curl ni wget disponibles."; return 1; fi
}
fetch(){ # url -> stdout
    if   has curl; then curl -fsSL "$1"
    elif has wget; then wget -qO- "$1"
    else return 1; fi
}

# --- Architecture -> tag de l'asset ---
case "$(uname -m)" in
    x86_64)        ARCH_TAG="linux64" ;;
    aarch64|arm64) ARCH_TAG="linux-aarch64" ;;
    *) err "Architecture non geree : $(uname -m). Telecharge ART a la main sur $REPO."; exit 1 ;;
esac

# --- Un ART deja present a-t-il le CTL ? (dynamique OU statique via AboutThisBuild) ---
has_ctl(){
    local art="$1" real dir
    ldd "$art" 2>/dev/null | grep -qi 'IlmCtl' && return 0
    real="$(readlink -f "$art" 2>/dev/null)"; dir="$(dirname "$real")"
    grep -qi 'CTL interpreter' "$dir/AboutThisBuild.txt" 2>/dev/null && return 0
    grep -qi 'CTL interpreter' "$dir/../share/doc/ART/AboutThisBuild.txt" 2>/dev/null && return 0
    return 1
}

echo -e "${B}=== Installation / mise a jour d'ART (bundle officiel, CTL + OCIO inclus) ===${N}"

# --- Derniere version publiee ---
info "Recherche de la derniere version d'ART sur GitHub..."
JSON="$(fetch "$API")" || { err "Impossible de contacter GitHub."; exit 1; }
LATEST_VER="$(printf '%s' "$JSON" | grep -oE '"tag_name":[[:space:]]*"[^"]+"' | head -1 | grep -oE '[0-9]+(\.[0-9]+)+')"
ASSET_URL="$(printf '%s' "$JSON" | grep -oE '"browser_download_url":[[:space:]]*"[^"]+"' | grep -oE 'https[^"]+' | grep -E "ART-.*-${ARCH_TAG}\.tar\.xz$" | head -1)"
{ [ -n "$LATEST_VER" ] && [ -n "$ASSET_URL" ]; } || { err "Version/asset introuvable pour $ARCH_TAG."; exit 1; }
ok "Derniere version : ART ${LATEST_VER} (${ARCH_TAG})"

FOLDER="ART-${LATEST_VER}-${ARCH_TAG}"
DEST="${INSTALL_PARENT}/${FOLDER}"

# --- Deja un ART avec CTL ? ---
CUR="$(command -v ART 2>/dev/null || true)"
if [ "$FORCE" != "1" ] && [ -n "$CUR" ] && has_ctl "$CUR"; then
    real_cur="$(readlink -f "$CUR" 2>/dev/null)"
    real_latest="$(readlink -f "${DEST}/ART" 2>/dev/null || true)"
    if [ -n "$real_latest" ] && [ "$real_cur" = "$real_latest" ]; then
        ok "Tu as deja ART ${LATEST_VER} (bundle officiel) avec le CTL. Rien a faire."; exit 0
    fi
    if printf '%s' "$real_cur" | grep -qE "^${INSTALL_PARENT}/ART-.*-${ARCH_TAG}/ART$"; then
        info "Un bundle ART plus ancien est installe -> mise a jour vers ${LATEST_VER}."
    else
        ok "Tu as deja un ART avec le CTL : $CUR"
        echo "   Rien a installer. (Pour forcer le bundle officiel : relance avec --force.)"
        exit 0
    fi
fi

# --- Confirmation ---
MSG="Installer ART ${LATEST_VER} (bundle officiel, ~90 Mo) ?

- Inclut DEJA le CTL + l'OCIO (scripts de simulation de film).
- Emplacement : ${DEST}
- Liens crees : ${BINDIR}/ART  et  ${BINDIR}/ART-cli

Le telechargement fait ~90 Mo : cela peut prendre quelques minutes.
Continuer ?"
if [ "$ASSUME_YES" != "1" ]; then
    if has zenity; then
        zenity --question --width=540 --title="Installer ART ${LATEST_VER}" --text="$MSG" 2>/dev/null || { echo "Annule."; exit 0; }
    else
        echo -e "$MSG"; read -r -p "[o/N] " r; case "$r" in o|O|y|Y) ;; *) echo "Annule."; exit 0 ;; esac
    fi
fi

# --- Telechargement + extraction ---
has tar || { err "tar est requis."; exit 1; }
mkdir -p "$INSTALL_PARENT" "$BINDIR"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
info "Telechargement d'ART ${LATEST_VER} (~90 Mo)..."
dl "$ASSET_URL" "$TMP/art.tar.xz" || { err "Telechargement echoue."; exit 1; }
info "Extraction dans ${INSTALL_PARENT}/ ..."
tar -xf "$TMP/art.tar.xz" -C "$INSTALL_PARENT" || { err "Extraction echouee."; exit 1; }
[ -x "${DEST}/ART" ] || { err "Binaire ART introuvable apres extraction : ${DEST}/ART"; exit 1; }

# --- Liens ---
ln -sf "${DEST}/ART"     "${BINDIR}/ART"
ln -sf "${DEST}/ART-cli" "${BINDIR}/ART-cli"
ok "Liens crees : ${BINDIR}/ART  et  ${BINDIR}/ART-cli"

# --- Lanceur d'application (icone dans le menu, sans terminal) ---
APPS="${HOME}/.local/share/applications"
ICONS="${HOME}/.local/share/icons"
mkdir -p "$APPS" "$ICONS"
ICON="ART"
for sz in 256 128 512 64 48; do
    if [ -f "${DEST}/images/ART-logo-${sz}.png" ]; then
        cp -f "${DEST}/images/ART-logo-${sz}.png" "${ICONS}/ART.png" && ICON="${ICONS}/ART.png"
        break
    fi
done
cat > "${APPS}/ART.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=ART
GenericName=Éditeur RAW
Comment=ARTherapee — développement photo RAW
Exec=${BINDIR}/ART %F
Icon=${ICON}
Terminal=false
Categories=Graphics;Photography;
MimeType=image/x-canon-cr2;image/x-nikon-nef;image/x-sony-arw;image/tiff;image/jpeg;image/png;
StartupNotify=true
EOF
chmod +x "${APPS}/ART.desktop"
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APPS" >/dev/null 2>&1
ok "Lanceur créé : menu Applications → ART (clic pour lancer, sans terminal)"

# --- Optionnel : proposer de supprimer d'ANCIENNES releases bundle ---
# On ne propose JAMAIS de suppression automatique, et UNIQUEMENT des bundles
# téléchargés par ce script (~/programs/ART-*-<arch>). Un ART compilé (ex.
# /usr/local) n'est JAMAIS concerné. Ignoré en mode --yes (pas d'interaction).
if [ "$ASSUME_YES" != "1" ]; then
    mapfile -t _found < <(find "$INSTALL_PARENT" -maxdepth 1 -type d -name "ART-*-${ARCH_TAG}" 2>/dev/null)
    OLD_BUNDLES=()
    for _d in "${_found[@]}"; do [ "$_d" != "$DEST" ] && OLD_BUNDLES+=("$_d"); done
    if [ "${#OLD_BUNDLES[@]}" -gt 0 ]; then
        _LIST="$(printf '   %s\n' "${OLD_BUNDLES[@]}")"
        if ask_yes "Nettoyer d'anciennes versions d'ART ?" \
"D'anciennes versions du bundle ART ont été trouvées :

$_LIST

Voulez-vous les SUPPRIMER pour faire de la place ?

Note : on ne supprime QUE ces releases téléchargées.
Un ART que vous auriez compilé vous-même (ex. /usr/local)
n'est JAMAIS touché."; then
            if ask_yes "Confirmation" \
"⚠️ Êtes-vous VRAIMENT sûr ? Cette suppression est IRRÉVERSIBLE.

Dossiers qui seront supprimés :
$_LIST"; then
                for _d in "${OLD_BUNDLES[@]}"; do rm -rf "$_d" && ok "Supprimé : $_d"; done
            else
                info "Suppression annulée."
            fi
        else
            info "Anciennes versions conservées."
        fi
    fi
fi

# --- ~/.local/bin dans le PATH ? ---
case ":$PATH:" in
    *":${BINDIR}:"*) : ;;
    *) warn "${BINDIR} n'est pas dans ton PATH."
       echo "   Ajoute cette ligne a la fin de ~/.bashrc puis rouvre un terminal :"
       echo -e "       ${G}export PATH=\"\$HOME/.local/bin:\$PATH\"${N}" ;;
esac

# --- Verif CTL ---
if grep -qi 'CTL interpreter' "${DEST}/AboutThisBuild.txt" 2>/dev/null; then
    ok "CTL + OCIO confirmes dans le build."
else
    warn "'CTL interpreter' non confirme dans AboutThisBuild.txt (a verifier)."
fi

# --- Recap ---
RECAP="ART ${LATEST_VER} installe !

Dossier  : ${DEST}
Commande : ART        (via ${BINDIR}/ART)
CLI      : ART-cli

Le CTL et l'OCIO sont inclus : tes scripts de simulation de film
fonctionneront. Dans ART : Preferences -> Traitement de l'image ->
regle le 'Dossier CLUT' sur ~/.config/ART/ctlscripts, puis REDEMARRE ART."
echo -e "${G}==================================================${N}"
echo -e "$RECAP"
echo -e "${G}==================================================${N}"
has zenity && zenity --info --width=560 --title="ART ${LATEST_VER} installe" --text="$RECAP" 2>/dev/null
exit 0
