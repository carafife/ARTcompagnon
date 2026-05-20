# 📚 Installation des Dépendances Optionnelles

**Pour : ART (ArtrawEditor) + Le ARTherapee Compagnon**
**Version:** v2.0 | **Date:** Mai 2026 | **Langue:** Français

---

## ⚠️ Important

**Le ARTherapee Compagnon fonctionne GARANTIE avec ART compilé uniquement.**

Les dépendances ci-dessous sont **optionnelles** :
- **SMART Masking** - Créer des masques intelligents avec IA
- **nind-denoise** - Débruiter les images RAW avec IA
- **Scripts CTL** - Appliquer des scripts de couleur avancés

---

## 🎯 1. SMART Masking

### Qu'est-ce que c'est?
SMART utilise l'IA (SAM2) pour créer des masques intelligents sur vos images.

**Format d'entrée:** JPG, TIF, PNG (export RAW en JPG d'abord)

### Installation générale

#### Étape 1 : Cloner SMART
```bash
cd ~/Programmes
git clone https://github.com/artraweditor/SMART.git
cd SMART
```

#### Étape 2 : Virtual Environment
```bash
python3 -m venv SMART-env
source SMART-env/bin/activate
```

#### Étape 3 : Installer dépendances Python
```bash
pip install PyQt5 opencv-python Pillow
```

#### Étape 4 : Cloner SAM2 (modèle IA)
```bash
cd ~/Programmes
git clone https://github.com/facebookresearch/sam2.git
cd sam2
source ~/Programmes/SMART/SMART-env/bin/activate
pip install -e .
```

#### Étape 5 : Télécharger les modèles
```bash
cd ~/Programmes/sam2/checkpoints
bash download_ckpts.sh
```

#### Étape 6 : Configurer les chemins
```bash
mkdir -p ~/Programmes/SMART/models
mkdir -p ~/Programmes/SMART/data

# Copier les configs et modèles
cp ~/Programmes/sam2/sam2/configs/sam2.1_hiera_*.yaml ~/Programmes/SMART/data/
cp ~/Programmes/sam2/checkpoints/sam2.1_hiera_*.pt ~/Programmes/SMART/models/
```

#### Étape 7 : Vérifier l'installation
```bash
cd ~/Programmes/SMART
source SMART-env/bin/activate
python src/main.py --help
```

### Utilisation avec ARTcompagnon

1. **Sélectionnez une image RAW** dans ART
2. **Exportez en JPG** (ART → File → Export as JPEG)
3. **Ouvrez ARTcompagnon** (clic droit → "Le ARTherapee Compagnon")
4. **Cliquez sur SMART Masking**
5. **Créez vos masques :**
   - `Shift + Clic gauche` = ajouter un point
   - `Shift + Clic droit` = retirer un point
6. **Sauvegardez** le masque

---

## 🎯 2. nind-denoise

### Qu'est-ce que c'est?
nind-denoise utilise l'IA (Deep Learning) pour débruiter les images RAW.

**Format d'entrée:** RAW uniquement

⚠️ **Attention:** Très lent sur CPU (AMD/Intel sans GPU CUDA)

### Installation générale

#### Étape 1 : Cloner nind-denoise
```bash
cd ~/Programmes
git clone --depth 1 https://github.com/agriggio/nind-denoise
cd nind-denoise
```

#### Étape 2 : Virtual Environment
```bash
python3 -m venv nind-denoise-env
source nind-denoise-env/bin/activate
```

#### Étape 3 : Installer les dépendances
```bash
pip install torch torchvision ConfigArgParse opencv-python pyyaml
```

#### Étape 4 : Configurer pour CPU
Éditer `nind_denoise_raw.sh` et s'assurer:
```bash
DEVICE=cpu
PYTHON=$HOME/Programmes/nind-denoise-env/bin/python
NIND_DENOISE_DIR=$HOME/Programmes/nind-denoise
```

#### Étape 5 : Configurer ART usercommand
```bash
mkdir -p ~/.config/ART/usercommands/bash
cp ~/Programmes/nind-denoise/nind_denoise_raw.sh ~/.config/ART/usercommands/bash/
chmod +x ~/.config/ART/usercommands/bash/nind_denoise_raw.sh
```

### Utilisation avec ARTcompagnon

1. **Sélectionnez une image RAW** dans ART
2. **Ouvrez ARTcompagnon** (clic droit → "Le ARTherapee Compagnon")
3. **Cliquez sur nind-denoise**
4. **Attendez le traitement** (peut être long sur CPU)
5. **L'image débruitée est créée** avec le suffix `-denoised.tif`

---

## 🎯 3. Scripts CTL

### Qu'est-ce que c'est?
CTL (Color Transformation Language) permet d'appliquer des corrections couleur avancées.

**Format:** Scripts `.ctl` (déjà intégrés dans ART)

### Installation sur Fedora

#### Étape 1 : Installer les dépendances système
```bash
sudo dnf install ctl CTL-devel openexr openexr-devel
```

#### Étape 2 : Compiler ART avec CTL
```bash
cd ~/Programmes/ART
mkdir build
cd build
cmake .. -DENABLE_CTL=ON -DCTL_INCLUDE_DIR=/usr/include/CTL
make -j4
sudo make install
```

#### Étape 3 : Cloner les scripts CTL
```bash
cd ~/Programmes
git clone https://github.com/artraweditor/ART-ctlscripts.git
```

#### Étape 4 : Configurer ART
1. Ouvrez ART
2. Edit → Preferences
3. Color Management → CLUT / CTL folder
4. Sélectionnez: `~/Programmes/ART-ctlscripts`

### Installation sur Arch Linux/Manjaro

#### Étape 1 : Installer les dépendances système
```bash
sudo pacman -S ctl openexr
```

#### Étape 2 : Compiler ART avec CTL
```bash
cd ~/Programmes/ART
mkdir build
cd build
cmake .. -DENABLE_CTL=ON -DCTL_INCLUDE_DIR=/usr/include/CTL
make -j4
sudo make install
```

#### Étape 3 : Cloner les scripts CTL
```bash
cd ~/Programmes
git clone https://github.com/artraweditor/ART-ctlscripts.git
```

#### Étape 4 : Configurer ART
1. Ouvrez ART
2. Edit → Preferences
3. Color Management → CLUT / CTL folder
4. Sélectionnez: `~/Programmes/ART-ctlscripts`

### Installation sur Ubuntu/Debian

#### Étape 1 : Installer les dépendances système
```bash
sudo apt update
sudo apt install libctl-dev libopenexr-dev
```

#### Étape 2 : Compiler ART avec CTL
```bash
cd ~/Programmes/ART
mkdir build
cd build
cmake .. -DENABLE_CTL=ON -DCTL_INCLUDE_DIR=/usr/include/CTL
make -j4
sudo make install
```

#### Étape 3 : Cloner les scripts CTL
```bash
cd ~/Programmes
git clone https://github.com/artraweditor/ART-ctlscripts.git
```

#### Étape 4 : Configurer ART
1. Ouvrez ART
2. Edit → Preferences
3. Color Management → CLUT / CTL folder
4. Sélectionnez: `~/Programmes/ART-ctlscripts`

### Utilisation

1. **Ouvrez une image RAW** dans ART
2. **Tools → Color Management → CTL Scripts**
3. **Sélectionnez un script** (ex: color_harmonizer.ctl)
4. **Appliquez** les modifications

---

## 🔧 Configuration de ARTcompagnon

Les scripts doivent être intégrés dans ARTcompagnon via les **usercommands**:

### SMART
- Chemin: `~/.config/ART/usercommands/bash/smart_masking.sh`
- Format: JPG|JPEG|TIF|TIFF|PNG

### nind-denoise
- Chemin: `~/.config/ART/usercommands/bash/nind_denoise_raw.sh`
- Format: RAW

### CTL
- Intégré directement dans ART (pas de usercommand nécessaire)

---

## 🐛 Dépannage

### SMART ne démarre pas
```bash
# Vérifier l'installation
cd ~/Programmes/SMART
source SMART-env/bin/activate
python src/main.py
```

### nind-denoise est très lent
- Normal sur CPU! Considérez un GPU NVIDIA avec CUDA pour accélération

### Scripts CTL n'apparaissent pas
```bash
# Vérifier le chemin dans ART
# Preferences → Color Management → CLUT/CTL folder
# Doit pointer vers: ~/Programmes/ART-ctlscripts
```

---

## 📞 Support

- **ART:** https://github.com/agriggio/art
- **SMART:** https://github.com/artraweditor/SMART
- **SAM2:** https://github.com/facebookresearch/sam2
- **nind-denoise:** https://github.com/agriggio/nind-denoise
- **CTL Scripts:** https://github.com/artraweditor/ART-ctlscripts

---

**Bon traitement d'images ! 🎨**
