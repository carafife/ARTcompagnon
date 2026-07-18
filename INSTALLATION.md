# 📖 Installation — Le ARTherapee Compagnon

## 🚀 Installation (recommandée)

```bash
git clone https://github.com/carafife/ARTcompagnon.git
cd ARTcompagnon
./demarrer.sh
```

`demarrer.sh` ouvre une fenêtre et vous guide en **2 étapes**.

### Étape 1 — ART (`installer-art.sh`)
Télécharge le **bundle officiel d'ART** (dernière version), qui inclut **déjà
le CTL et l'OCIO**. Il est extrait dans `~/programs/`, des liens `ART` et
`ART-cli` sont créés dans `~/.local/bin`, et un **lanceur** est ajouté au menu
Applications (icône ART, démarrage sans terminal).

> - Si vous avez déjà un ART complet (avec CTL), le script le **détecte et ne
>   touche à rien**. Relancé plus tard, il met ART à jour vers la dernière version.
> - Si d'anciennes versions du **bundle** sont présentes dans `~/programs/`, il
>   peut **proposer** de les supprimer — **toujours avec confirmation, jamais
>   automatiquement**, et **jamais** un ART que vous auriez compilé vous-même.

### Étape 2 — Le Compagnon (`install.sh`)
Met en place la configuration ART (éditeur externe) et installe les dépendances
nécessaires — **PyQt5, tkinter, Pillow, reportlab, gnome-terminal** — via le
gestionnaire de paquets de votre distribution (dnf/apt/pacman/zypper).

*(Vous pouvez aussi lancer les scripts à la main : `./installer-art.sh` puis `./install.sh`.)*

## ▶️ Premier lancement
1. Lancez **ART**.
2. Menu **Éditeur externe** (ou clic droit dans le navigateur) → **Le ARTherapee Compagnon**.
3. Onglet **Scripts ART** → **« Installer Pack »** pour récupérer la collection de scripts.
4. Pour la **simulation de film (CTL)** : Préférences → Traitement de l'image →
   **« Dossier CLUT »** = `~/.config/ART/ctlscripts`, puis **redémarrez ART**.

## 🔧 Dépendances (référence)
`install.sh` s'en charge automatiquement. Pour les installer vous-même :

```bash
# Fedora
sudo dnf install python3 python3-qt5-base python3-tkinter python3-pillow python3-pillow-tk python3-reportlab gnome-terminal git

# Ubuntu / Debian
sudo apt install python3 python3-pyqt5 python3-tk python3-pil python3-pil.imagetk python3-reportlab gnome-terminal git

# Arch
sudo pacman -S python python-pyqt5 tk python-pillow python-reportlab gnome-terminal git
```

## 🐛 Dépannage
- **Le Compagnon ne démarre pas** →
  `python3 -c "import PyQt5.QtWidgets; print('PyQt5 OK')"`
- **Mes scripts CTL n'apparaissent pas** → voir la fiche **« Vérifier le support
  CTL »** : votre ART a-t-il le CTL ? le « Dossier CLUT » est-il réglé ? ART a-t-il
  été redémarré ? (Le bundle officiel installé par `installer-art.sh` a le CTL.)
- **« ART-cli : commande introuvable »** → `installer-art.sh` pose les liens dans
  `~/.local/bin`. Vérifiez que ce dossier est dans votre `PATH`.

## 📞 Support
- Forum : https://forum.artherapee.fr
- Dépôt : https://github.com/carafife/ARTcompagnon
