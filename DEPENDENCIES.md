# 📦 Dépendances des Scripts ARTcompagnon

## 🔍 exif_viewer.py
**Lecteur de métadonnées EXIF**

Dépendance requise: `exiftool`

### Installation

**Fedora:**
```bash
dnf install exiftool
```

**Ubuntu/Debian:**
```bash
apt install exiftool
```

**Arch Linux:**
```bash
pacman -S perl-image-exiftool
```

---

## 🖼️ watermark_batch.py
**Ajout de filigrane en batch**

Dépendance requise: `Pillow` (PIL)

### Installation

**Fedora:**
```bash
pip install Pillow
```

**Ubuntu/Debian:**
```bash
pip install Pillow
```

**Arch Linux:**
```bash
pacman -S python-pillow
```

---

## 🔎 cherche_appli.py
**Recherche d'applications installées**

Dépendance requise: `xclip`

### Installation

**Fedora:**
```bash
dnf install xclip
```

**Ubuntu/Debian:**
```bash
apt install xclip
```

**Arch Linux:**
```bash
pacman -S xclip
```

---

## ⚠️ Messages d'erreur
Si une dépendance manque, chaque script affichera un message d'erreur clair avec les commandes d'installation!
