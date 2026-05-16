# 🎨 ARTcompagnon - Architecture & Documentation

**Dernière mise à jour:** 16 mai 2026  
**Statut:** v1.1-beta  
**Créateur:** carafife (tutoriels photo libres)

---

## 📋 Table des Matières
1. [Architecture du Projet](#architecture)
2. [Environnement](#environnement)
3. [Outils Intégrés](#outils-intégrés)
4. [Chemins Critiques](#chemins-critiques)
5. [Limitations Connues](#limitations-connues)
6. [Dépendances](#dépendances)
7. [Workflow Utilisateur](#workflow-utilisateur)
8. [Points d'Attention](#points-d-attention)
9. [Références](#références)

---

## 🏗️ Architecture du Projet

### Structure des Répertoires

```
~/art-compagnon/                    ← REPO LOCAL (connecté GitHub)
├── .git/                           ← Contrôle de version
├── select-editor.py                ← App principale Qt/Python
├── select-editor-config.json       ← Config des éditeurs
├── custom-tasks/                   ← Scripts bash pour AC
│   ├── ctl-launcher.sh            ← Lance les scripts CTL
│   ├── smart_masking.sh           ← Lance SMART
│   └── lightzone-wrapper.sh       ← Wrapper LightZone
├── PROJECT_ARCHITECTURE.md        ← CETTE DOC
├── SMART_NIND-DENOISE_DOCUMENTATION.md
├── README.md
└── VERSION

~/Programmes/                        ← Outils externes
├── ART/                            ← Image processor (compilé GitHub)
├── SMART/                          ← AI mask builder (SAM2)
├── sam2/                           ← Segmentation model (Meta)
├── nind-denoise/                   ← AI denoiser
└── ART-ctlscripts/                 ← Scripts CTL collection

~/.config/ART/                       ← Config ART
├── usercommands/
│   ├── select-editor.txt          ← AC command
│   └── nind_denoise.txt           ← nind-denoise command
├── ctlscripts/                     ← CTL scripts folder
└── SMART.json                      ← SMART config
```

### Points Critiques de l'Architecture

⚠️ **IMPORTANT:** 
- **Repo local = `~/art-compagnon/`** (minuscule, connecté GitHub)
- **ANCIEN dossier `~/Programmes/ARTcompagnon/` = SUPPRIMÉ** (était une copie)
- AC utilise `select-editor.py` depuis `~/art-compagnon/`

---

## 💻 Environnement

**Système:** Fedora 44 (NOT Ubuntu/Debian)
- Package manager: `dnf` (pas `apt`)
- Shell: `bash`
- GPU: AMD Radeon (pas CUDA → utiliser `device=cpu`)

**Python:** 
- Venv pour SMART: `~/Programmes/SMART/SMART-env/`
- Venv pour nind-denoise: `~/Programmes/nind-denoise-env/`
- Venv pour SAM2: dans SMART-env

---

## 🛠️ Outils Intégrés

### 1. SMART (SAM2 Mask Builder)

**Fonction:** Créer des masques intelligents basés sur segmentation d'images

**Installation:** `~/Programmes/SMART/`

**Limitations:**
- ❌ Ne lit que **JPG/TIF/PNG** (pas RAW - limitation Pillow)
- 📌 Utilisateurs doivent exporter RAW en JPG d'abord
- FileType dans `select-editor.txt`: `jpg|jpeg|tif|tiff|png`

**Configuration:**
- Config file: `~/.config/ART/SMART.json`
- Device: `cpu` (AMD Radeon)
- Modèle actif: `sam2.1_hiera_base_plus.pt` (309 MB)

---

### 2. nind-denoise (AI Denoiser)

**Fonction:** Réduire le bruit des images haute sensibilité

**Installation:** `~/Programmes/nind-denoise/`

**Limitations:**
- ❌ Ne lit que **RAW**
- ⏱️ Très lent sur CPU (AMD Radeon)
- 📁 Crée fichier `-denoised.tif` en sortie

---

### 3. ART-ctlscripts (CTL Collection)

**Fonction:** Scripts CTL pour transformations couleur avancées

**Installation:** `~/Programmes/ART-ctlscripts/`

**Contient:** `_artlib.ctl`, `shadowboost.ctl`, `bwmix.ctl`, etc.

---

## 📍 Chemins Critiques

```
SMART:              ~/Programmes/SMART/
nind-denoise:       ~/Programmes/nind-denoise/
ART:                ~/Programmes/ART/
ART-ctlscripts:     ~/Programmes/ART-ctlscripts/

Config ART:         ~/.config/ART/
  - usercommands:   ~/.config/ART/usercommands/
  - ctlscripts:     ~/.config/ART/ctlscripts/
  - SMART config:   ~/.config/ART/SMART.json

AC repo:            ~/art-compagnon/ ← CELUI-CI!
custom-tasks:       ~/art-compagnon/custom-tasks/
```

---

## ⚠️ Limitations Connues

| Outil | Formats | Limitations |
|-------|---------|-------------|
| SMART | JPG/TIF/PNG | Pas RAW (Pillow) |
| nind-denoise | RAW | Lent CPU, crée TIF |
| CTL Scripts | - | Nécessite ENABLE_CTL=ON |
| AC | bash scripts | Pas Python/CTL natif (évolution prévue) |

---

## 🎯 Workflow Utilisateur

### SMART
1. RAW dans ART → Exporter JPG
2. Clic droit → ARTcompagnon → SMART
3. Shift+clic = point, Shift+clic droit = retrait

### nind-denoise
1. RAW dans ART
2. Clic droit → "AI denoise"
3. Attendre traitement

### CTL Scripts
1. Image dans ART
2. Clic droit → ARTcompagnon → ctl-launcher.sh
3. Choisir script → Relancer ART
4. Color/Tone Correction → LUT

---

## 🚨 Points d'Attention

### 1. Dossiers
❌ `~/Programmes/ARTcompagnon/` (supprimé)
✅ `~/art-compagnon/` (repo git)

### 2. SMART et RAW
❌ SMART ne lit JAMAIS RAW
✅ Exporter RAW → JPG d'abord

### 3. ART et CTL
❌ CTL absent = ART sans ENABLE_CTL
✅ Recompiler avec dépendances CTL

### 4. GPU
⚠️ AMD Radeon n'a pas CUDA
✅ Utiliser `device=cpu`

### 5. AC vs usercommands
- AC = depuis éditeur ART
- usercommands = depuis navigateur fichiers

---

## 📚 Références

- ARTcompagnon: https://github.com/carafife/ARTcompagnon
- ART: https://github.com/agriggio/art
- SMART: https://github.com/artraweditor/SMART
- SAM2: https://github.com/facebookresearch/sam2
- nind-denoise: https://github.com/agriggio/nind-denoise
- ART-ctlscripts: https://github.com/artraweditor/ART-ctlscripts
- Forum ART FR: https://forum.artherapee.fr/

---

## 🔄 Workflow Git

### Branches

- **`main`** = Versions STABLES (prod)
- **`test`** = Branche de TEST (développement)

### Processus de validation

```
1. Commit sur test
   git checkout test
   git add .
   git commit -m "..."
   git push origin test

2. TESTER les modifs

3. Merger vers main (une fois validé)
   git checkout main
   git merge test
   git push origin main
```

⚠️ **IMPORTANT:** Ne JAMAIS pousser directement sur `main`!

---

## 🚀 Évolutions Prévues

- ✋ AC supporte bash scripts → Évolution vers **Python + CTL natif**
- ✋ SMART RAW limitation → Solution: workflow RAW→JPG (OK pour MVP)
- ✋ Plugin system pour AC → Architecture modulaire future

---

**Pour relancer la machine:** Dis `@ARTCOMPAGNON-CONTEXT` à Claude!
