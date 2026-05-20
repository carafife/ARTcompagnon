# 📚 Installing Optional Dependencies

**For: ART (ArtrawEditor) + The ARTherapee Companion**
**Version:** v2.0 | **Date:** May 2026 | **Language:** English

---

## ⚠️ Important

**The ARTherapee Companion is GUARANTEED to work with ART compiled only.**

The dependencies below are **optional**:
- **SMART Masking** - Create intelligent masks with AI
- **nind-denoise** - Denoise RAW images with AI
- **CTL Scripts** - Apply advanced color scripts

---

## 🎯 1. SMART Masking

### What is it?
SMART uses AI (SAM2) to create intelligent masks on your images.

**Input format:** JPG, TIF, PNG (export RAW as JPG first)

### General Installation

#### Step 1: Clone SMART
```bash
cd ~/Programmes
git clone https://github.com/artraweditor/SMART.git
cd SMART
```

#### Step 2: Virtual Environment
```bash
python3 -m venv SMART-env
source SMART-env/bin/activate
```

#### Step 3: Install Python Dependencies
```bash
pip install PyQt5 opencv-python Pillow
```

#### Step 4: Clone SAM2 (AI model)
```bash
cd ~/Programmes
git clone https://github.com/facebookresearch/sam2.git
cd sam2
source ~/Programmes/SMART/SMART-env/bin/activate
pip install -e .
```

#### Step 5: Download Models
```bash
cd ~/Programmes/sam2/checkpoints
bash download_ckpts.sh
```

#### Step 6: Configure Paths
```bash
mkdir -p ~/Programmes/SMART/models
mkdir -p ~/Programmes/SMART/data

# Copy configs and models
cp ~/Programmes/sam2/sam2/configs/sam2.1_hiera_*.yaml ~/Programmes/SMART/data/
cp ~/Programmes/sam2/checkpoints/sam2.1_hiera_*.pt ~/Programmes/SMART/models/
```

#### Step 7: Verify Installation
```bash
cd ~/Programmes/SMART
source SMART-env/bin/activate
python src/main.py --help
```

### Usage with ARTcompagnon

1. **Select a RAW image** in ART
2. **Export as JPG** (ART → File → Export as JPEG)
3. **Open ARTcompagnon** (right-click → "The ARTherapee Companion")
4. **Click SMART Masking**
5. **Create your masks:**
   - `Shift + Left click` = add point
   - `Shift + Right click` = remove point
6. **Save** your mask

---

## 🎯 2. nind-denoise

### What is it?
nind-denoise uses AI (Deep Learning) to denoise RAW images.

**Input format:** RAW only

⚠️ **Warning:** Very slow on CPU (AMD/Intel without GPU CUDA)

### General Installation

#### Step 1: Clone nind-denoise
```bash
cd ~/Programmes
git clone --depth 1 https://github.com/agriggio/nind-denoise
cd nind-denoise
```

#### Step 2: Virtual Environment
```bash
python3 -m venv nind-denoise-env
source nind-denoise-env/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install torch torchvision ConfigArgParse opencv-python pyyaml
```

#### Step 4: Configure for CPU
Edit `nind_denoise_raw.sh` and ensure:
```bash
DEVICE=cpu
PYTHON=$HOME/Programmes/nind-denoise-env/bin/python
NIND_DENOISE_DIR=$HOME/Programmes/nind-denoise
```

#### Step 5: Configure ART usercommand
```bash
mkdir -p ~/.config/ART/usercommands/bash
cp ~/Programmes/nind-denoise/nind_denoise_raw.sh ~/.config/ART/usercommands/bash/
chmod +x ~/.config/ART/usercommands/bash/nind_denoise_raw.sh
```

### Usage with ARTcompagnon

1. **Select a RAW image** in ART
2. **Open ARTcompagnon** (right-click → "The ARTherapee Companion")
3. **Click nind-denoise**
4. **Wait for processing** (can be long on CPU)
5. **Denoised image is created** with `-denoised.tif` suffix

---

## 🎯 3. CTL Scripts

### What is it?
CTL (Color Transformation Language) allows advanced color correction scripts.

**Format:** `.ctl` scripts (already integrated in ART)

### Installation on Fedora

#### Step 1: Install System Dependencies
```bash
sudo dnf install ctl CTL-devel openexr openexr-devel
```

#### Step 2: Compile ART with CTL
```bash
cd ~/Programmes/ART
mkdir build
cd build
cmake .. -DENABLE_CTL=ON -DCTL_INCLUDE_DIR=/usr/include/CTL
make -j4
sudo make install
```

#### Step 3: Clone CTL Scripts
```bash
cd ~/Programmes
git clone https://github.com/artraweditor/ART-ctlscripts.git
```

#### Step 4: Configure ART
1. Open ART
2. Edit → Preferences
3. Color Management → CLUT / CTL folder
4. Select: `~/Programmes/ART-ctlscripts`

### Installation on Arch Linux/Manjaro

#### Step 1: Install System Dependencies
```bash
sudo pacman -S ctl openexr
```

#### Step 2: Compile ART with CTL
```bash
cd ~/Programmes/ART
mkdir build
cd build
cmake .. -DENABLE_CTL=ON -DCTL_INCLUDE_DIR=/usr/include/CTL
make -j4
sudo make install
```

#### Step 3: Clone CTL Scripts
```bash
cd ~/Programmes
git clone https://github.com/artraweditor/ART-ctlscripts.git
```

#### Step 4: Configure ART
1. Open ART
2. Edit → Preferences
3. Color Management → CLUT / CTL folder
4. Select: `~/Programmes/ART-ctlscripts`

### Installation on Ubuntu/Debian

#### Step 1: Install System Dependencies
```bash
sudo apt update
sudo apt install libctl-dev libopenexr-dev
```

#### Step 2: Compile ART with CTL
```bash
cd ~/Programmes/ART
mkdir build
cd build
cmake .. -DENABLE_CTL=ON -DCTL_INCLUDE_DIR=/usr/include/CTL
make -j4
sudo make install
```

#### Step 3: Clone CTL Scripts
```bash
cd ~/Programmes
git clone https://github.com/artraweditor/ART-ctlscripts.git
```

#### Step 4: Configure ART
1. Open ART
2. Edit → Preferences
3. Color Management → CLUT / CTL folder
4. Select: `~/Programmes/ART-ctlscripts`

### Usage

1. **Open a RAW image** in ART
2. **Tools → Color Management → CTL Scripts**
3. **Select a script** (ex: color_harmonizer.ctl)
4. **Apply** the changes

---

## 🔧 ARTcompagnon Configuration

Scripts must be integrated into ARTcompagnon via **usercommands**:

### SMART
- Path: `~/.config/ART/usercommands/bash/smart_masking.sh`
- Format: JPG|JPEG|TIF|TIFF|PNG

### nind-denoise
- Path: `~/.config/ART/usercommands/bash/nind_denoise_raw.sh`
- Format: RAW

### CTL
- Integrated directly in ART (no usercommand needed)

---

## 🐛 Troubleshooting

### SMART won't start
```bash
# Check installation
cd ~/Programmes/SMART
source SMART-env/bin/activate
python src/main.py
```

### nind-denoise is very slow
- Normal on CPU! Consider an NVIDIA GPU with CUDA for acceleration

### CTL Scripts don't appear
```bash
# Check path in ART
# Preferences → Color Management → CLUT/CTL folder
# Must point to: ~/Programmes/ART-ctlscripts
```

---

## 📞 Support

- **ART:** https://github.com/agriggio/art
- **SMART:** https://github.com/artraweditor/SMART
- **SAM2:** https://github.com/facebookresearch/sam2
- **nind-denoise:** https://github.com/agriggio/nind-denoise
- **CTL Scripts:** https://github.com/artraweditor/ART-ctlscripts

---

**Happy image processing! 🎨**
