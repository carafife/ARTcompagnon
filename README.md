<div align="center">
  <img src="assets/artcompagnon-logo.png" width="300" alt="ARTcompagnon Logo">
</div>

# 🎨 Le ARTherapee Compagnon

Lanceur d'applications et de scripts pour ART (ARTherapee).

**Version:** v2.0 | **Status:** Stable ✅

Lanceur d'applications et de scripts pour ART (ARTherapee).

**Version:** v2.0 | **Status:** Stable ✅

## 🌟 Caractéristiques

- 📋 **Éditeurs externes** - GIMP, Krita, RawTherapee, Hugin, Lightzone, etc.
- 🔧 **Scripts multi-langages** - Bash, Python, Lua
- 📂 **Arborescence intelligente** - Organisation auto par type
- 📸 **Multi-fichiers** - Sélectionnez plusieurs photos et lancez Hugin/HDR!
- 🌙 **Thèmes dynamiques** - Défaut & Average
- 🇫🇷 🇬🇧 **Multilingue** - Français & Anglais
- 🚀 Installation simple

## ⚠️ Prérequis

**ART COMPILÉ OBLIGATOIRE** (pas Flatpak/AppImage)

ARTcompagnon ne fonctionne que si ART est compilé depuis source.

## 📦 Installation rapide

```bash
git clone https://github.com/carafife/ARTcompagnon.git
cd ARTcompagnon
./install.sh
```

Relancez ART!

## 🎯 Utilisation

### Lancer un éditeur

**Option 1 - Bouton "Editeur externe"** (Preferences)
- ART → Preferences → External Editor → Cliquez le bouton

**Option 2 - Clic droit** (Navigateur fichiers)
- Sélectionnez image(s) → Clic droit → Le ARTherapee Compagnon → Choisissez éditeur

### Créer vos scripts

**Bash** `~/.config/ART/usercommands/bash/mon_script.sh`
```bash
#!/bin/bash
echo "Photo: $1"
```

**Python** `~/.config/ART/usercommands/python/mon_script.py`
```python
import sys
print(f"Photo: {sys.argv[1]}")
```

**Lua** `~/.config/ART/usercommands/lua/mon_script.lua`
```lua
print("Photo: " .. arg[1])
```

## 📚 Documentation

- [INSTALLATION.md](INSTALLATION.md) - Installation ARTcompagnon
- [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) - Architecture technique
- [COMPLETE_SETUP_GUIDE_FR.md](COMPLETE_SETUP_GUIDE_FR.md) - Guide complet (ART + dépendances optionnelles)

## 📝 Licence

MIT - Créé avec ❤️ par carafife
