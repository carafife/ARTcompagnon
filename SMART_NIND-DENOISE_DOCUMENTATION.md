# 📚 Guide Complet : SMART et nind-denoise avec ARTcompagnon

**Pour : ART (ArtrawEditor) + Le ARTherapee Compagnon**
**Date : Mai 2026**
**Niveau : Débutant**

## Installation de SMART
SMART est un outil d'IA pour créer des masques intelligents.

### Étape 1 : Cloner
cd ~/Programmes
git clone https://github.com/artraweditor/SMART.git

### Étape 2 : Venv
python3 -m venv SMART-env
source SMART-env/bin/activate

### Étape 3 : Dépendances
pip install PyQt5 wxPython opencv-python Pillow

### Étape 4 : SAM2
cd ~/Programmes
git clone https://github.com/facebookresearch/sam2.git
cd sam2
source ~/Programmes/SMART/SMART-env/bin/activate
pip install -e .

### Étape 5 : Modèles
cd ~/Programmes/sam2/checkpoints
bash download_ckpts.sh

### Étape 6-10 : Config
mkdir -p ~/Programmes/SMART/models
mkdir -p ~/Programmes/SMART/data
cp ~/Programmes/sam2/sam2/configs/sam2.1_hiera_*.yaml ~/Programmes/SMART/data/
cp ~/Programmes/sam2/checkpoints/sam2.1_hiera_*.pt ~/Programmes/SMART/models/

## Installation de nind-denoise
nind-denoise réduit le bruit des images.

### Étape 1 : Cloner
cd ~/Programmes
git clone --depth 1 https://github.com/agriggio/nind-denoise

### Étape 2 : Venv
python3 -m venv nind-denoise-env
source nind-denoise-env/bin/activate

### Étape 3 : Dépendances
pip install torch torchvision ConfigArgParse opencv-python pyyaml piqa

### Étape 4-7 : Config
cd ~/Programmes/nind-denoise
wget https://artraweditor.github.io/resources/nind_denoise_raw.sh
chmod +x nind_denoise_raw.sh
sed -i 's|DEVICE=mps|DEVICE=cpu|' nind_denoise_raw.sh
sed -i 's|PYTHON=$HOME/src/ART-AI-venv/bin/python|PYTHON=$HOME/Programmes/nind-denoise-env/bin/python|' nind_denoise_raw.sh
sed -i 's|NIND_DENOISE_DIR=$HOME/src/nind-denoise|NIND_DENOISE_DIR=$HOME/Programmes/nind-denoise|' nind_denoise_raw.sh
wget https://artraweditor.github.io/resources/nind_denoise.txt -O ~/.config/ART/usercommands/nind_denoise.txt
sed -i "s|\$HOME|$HOME|" ~/.config/ART/usercommands/nind_denoise.txt

## Intégration ARTcompagnon

### SMART
cat > ~/Programmes/ARTcompagnon/custom-tasks/smart_masking.sh << 'EOF'
#!/bin/bash
SMART_DIR="$HOME/Programmes/SMART"
cd "$SMART_DIR"
source SMART-env/bin/activate
python src/main.py "$@"
EOF
chmod +x ~/Programmes/ARTcompagnon/custom-tasks/smart_masking.sh

### Formats
sed -i 's/FileType=raw/FileType=jpg|jpeg|tif|tiff|png/' ~/.config/ART/usercommands/select-editor.txt

## Mode d'emploi

### SMART
1. Ouvrez RAW dans ART
2. Exportez en JPG
3. Clic droit → ARTherapee Compagnon → SMART
4. Shift+clic gauche = ajouter point
5. Shift+clic droit = retirer point
6. Sauvegardez le masque

### nind-denoise
1. Ouvrez RAW dans ART
2. Clic droit → AI denoise (nind-denoise)
3. Attendez le traitement
4. Image débruitée créée

## Limitations
- SMART : JPG/TIF/PNG uniquement (exporter RAW en JPG d'abord)
- nind-denoise : Lent sur CPU

## Ressources
- ART : https://artherapee.fr/
- SMART : https://github.com/artraweditor/SMART
- SAM2 : https://github.com/facebookresearch/sam2
- nind-denoise : https://github.com/agriggio/nind-denoise

**Bonne utilisation ! 🎨**
