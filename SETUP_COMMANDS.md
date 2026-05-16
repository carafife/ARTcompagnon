# 🚀 Commandes d'Installation Complètes

## ART (avec CTL)

### Ubuntu/Debian
```bash
sudo apt install -y git cmake build-essential libgtk-3-dev liblensfun-dev libexpat1-dev libcurl4-openssl-dev liblcms2-dev libpng-dev libtiff-dev libjpeg-dev liblapack-dev libfftw3-dev libexiv2-dev libopenjpeg2-7-dev libwebp-dev libxerces-c-dev libssl-dev ctl ctl-devel libopenexr-dev ilmbase-dev openexr

mkdir -p ~/Programmes && cd ~/Programmes
git clone https://bitbucket.org/agriggio/art.git
cd art && mkdir build && cd build

find /usr -name "CTL" -type d 2>/dev/null
# Trouver le chemin CTL (ex: /usr/include/CTL)

cmake .. -DCMAKE_BUILD_TYPE=Release -DENABLE_CTL=ON -DCTL_INCLUDE_DIR=/usr/include/CTL -DENABLE_OCIO=ON -DWITH_LTO=ON
make -j$(nproc)
sudo make install
```

### Arch Linux
```bash
sudo pacman -S --noconfirm git cmake base-devel gtk3 lensfun expat curl lcms2 libpng libtiff libjpeg lapack fftw exiv2 openjpeg2 libwebp xerces-c openssl ctl openexr ilmbase

mkdir -p ~/Programmes && cd ~/Programmes
git clone https://bitbucket.org/agriggio/art.git
cd art && mkdir build && cd build

cmake .. -DCMAKE_BUILD_TYPE=Release -DENABLE_CTL=ON -DCTL_INCLUDE_DIR=/usr/include/CTL -DENABLE_OCIO=ON -DWITH_LTO=ON
make -j$(nproc)
sudo make install
```

### Fedora
```bash
sudo dnf install -y git cmake gcc gcc-c++ gtk3-devel lensfun-devel expat-devel libcurl-devel lcms2-devel libpng-devel libtiff-devel libjpeg-turbo-devel lapack-devel fftw-devel exiv2-devel openjpeg2-devel libwebp-devel xerces-c-devel openssl-devel ctl CTL-devel openexr-devel ilmbase-devel

mkdir -p ~/Programmes && cd ~/Programmes
git clone https://bitbucket.org/agriggio/art.git
cd art && mkdir build && cd build

cmake .. -DCMAKE_BUILD_TYPE=Release -DENABLE_CTL=ON -DCTL_INCLUDE_DIR=/usr/include/CTL -DENABLE_OCIO=ON -DWITH_LTO=ON
make -j$(nproc)
sudo make install
```

## SMART

```bash
cd ~/Programmes
git clone https://github.com/artraweditor/SMART.git
cd SMART
python3 -m venv SMART-env
source SMART-env/bin/activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu pyyaml opencv-python pillow numpy scipy

cd ~/Programmes
git clone https://github.com/facebookresearch/sam2.git
cd sam2 && pip install -e .

cd ~/Programmes/SMART
mkdir -p models
wget https://dl.fbaipublicfiles.com/segment_anything_2/sam2_model_zoo/sam2.1_hiera_base_plus.pt -O models/sam2.1_hiera_base_plus.pt

mkdir -p ~/.config/ART/SMART/models
cp ~/Programmes/sam2/sam2/configs/sam2.1/*.yaml ~/.config/ART/SMART/models/
```

## nind-denoise

```bash
cd ~/Programmes
git clone https://github.com/agriggio/nind-denoise.git
cd nind-denoise
python3 -m venv nind-env
source nind-env/bin/activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu pillow numpy scipy scikit-image
```

## ARTcompagnon

```bash
cd ~
git clone https://github.com/carafife/ARTcompagnon.git art-compagnon
cd art-compagnon && chmod +x install.sh && ./install.sh
```

## Vérification finale

```bash
# ART + CTL
ART --version | grep -i ctl

# SMART
source ~/Programmes/SMART/SMART-env/bin/activate
python3 -c "import torch, sam2; print('SMART OK')"
deactivate

# nind-denoise
source ~/Programmes/nind-denoise/nind-env/bin/activate
python3 -c "import torch; print('nind OK')"
deactivate
```

---

## 🎯 UTILISER DEPUIS ARTCOMPAGNON

### SMART Masking

1. Ouvrir une image RAW dans ART
2. Exporter en JPG/TIF/PNG (SMART ne lit pas RAW!)
3. Dans ART: **Color/Tone Correction** → **External Editor** → **Le ARTherapee Compagnon**
4. Dans AC: sélectionner **SMART** → charger image → créer masque IA
5. Exporter le masque
6. Utiliser dans ART

### nind-denoise (Débruitage)

1. Ouvrir image RAW dans ART
2. Clic-droit ou menu → **AI denoise (nind-denoise)**
3. Le script s'exécute → créé `image-denoised.tif`
4. Importer le résultat dans ART

### CTL Scripts

1. Ouvrir image dans ART
2. **Color/Tone Correction** → mode **LUT**
3. Sélectionner script CTL (shadowboost, bwmix, etc.)
4. Ajuster paramètres si disponibles
5. Exporter

