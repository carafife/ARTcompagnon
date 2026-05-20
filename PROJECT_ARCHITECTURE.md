# 🎨 ARTcompagnon - Architecture

**Dernière mise à jour:** 20 mai 2026  
**Statut:** v2.0 Stable  
**Créateur:** carafife

---

## 📋 Table des Matières
1. [Architecture](#architecture)
2. [Structure des répertoires](#structure)
3. [Configuration ART](#configuration-art)
4. [Workflow Git](#workflow-git)

---

## 🏗️ Architecture

ARTcompagnon est un **lanceur d'applications** pour ART (ARTherapee).

Il se lance de 2 façons:
1. **Bouton "Editeur externe"** dans ART Preferences
2. **Clic droit** (usercommand) dans navigateur fichiers ART

Quand lancé, ARTcompagnon:
- Affiche une arborescence des scripts
- Permet de lancer des scripts bash/python/lua
- Passe l'image actuelle au script

---

## 📁 Structure des répertoires

```
~/art-compagnon/                    ← REPO LOCAL (GitHub)
├── select-editor.py                ← App principale
├── themes_data.py                  ← Thèmes dynamiques
├── translations.json               ← FR/EN translations
├── README.md
├── INSTALLATION.md
└── [autres fichiers]

~/.config/ART/usercommands/         ← Config ART
├── select-editor.txt               ← ARTcompagnon usercommand
└── bash/
    └── [vos scripts bash]
```

---

## ⚙️ Configuration ART

### File: `~/.config/ART/options`

Section `[External Editor]` DOIT avoir:
```
EditorKind=1
CustomEditor=
OutputDir=0
CustomOutputDir=
Float32=false
BypassOutputProfile=false
```

### File: `~/.config/ART/usercommands/select-editor.txt`

```
[ART UserCommand]
Label=Le ARTherapee Compagnon
Command=/home/carafife/art-compagnon/select-editor.py
FileType=raw|jpg|jpeg|tif|tiff|png
NumArgs=1
```

---

## 🔄 Workflow Git

- **`main`** = Versions STABLES (production)
- **`test`** = Branche de DÉVELOPPEMENT

Processus:
1. Développer sur `test`
2. Tester complètement
3. Merger vers `main` quand validé

---

## ⚠️ Prérequis

✅ **ART COMPILÉ OBLIGATOIRE** (pas Flatpak/AppImage)

ARTcompagnon ne fonctionne que si ART est compilé depuis source.
