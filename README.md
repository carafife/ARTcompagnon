<div align="center">
  <img src="assets/artcompagnon-logo.png" width="300" alt="ARTcompagnon Logo">
</div>

# 🎨 Le ARTherapee Compagnon

Un gestionnaire d'éditeurs et de scripts pour ART (ART Raw Editor).

**Version:** v1.5 | **Status:** Stable ✅

## 🌟 Caractéristiques

- 📋 Gérez vos éditeurs externes (GIMP, Krita, RawTherapee, Hugin, etc.)
- 🔧 **Scripts multi-langages:** Bash, Python, Lua
- 📂 **Arborescence intelligente** - Organisation auto des scripts par type
- 📸 **Support de plusieurs fichiers** - Sélectionnez 3+ photos et lancez Hugin ou HDR Merge !
- 🌙 Interface moderne avec thème sombre
- 🚀 Installation automatisée
- 🇫🇷 Entièrement en français

## 📦 Installation rapide

```bash
git clone https://github.com/carafife/ARTcompagnon.git
cd ARTcompagnon
./install.sh
```

Puis relancez ART et cliquez sur "External Editor" !

## 🎯 Utilisation

### Lancer un éditeur sur vos photos
1. Sélectionnez **1 ou plusieurs images RAW** dans ART
2. Clic droit → **Le ARTherapee Compagnon**
3. Choisissez votre éditeur (GIMP, Hugin, etc.)
4. **Toutes les photos sélectionnées** sont envoyées ! ✅

### Créer et exécuter des scripts

#### Scripts Bash 🔧
```bash
# ~/.config/ART/usercommands/bash/mon_script.sh
#!/bin/bash
echo "Photo reçue: $1"
```

#### Scripts Python 🐍
```python
# ~/.config/ART/usercommands/python/mon_script.py
import sys
print(f"Photo reçue: {sys.argv[1]}")
```

#### Scripts Lua 🌙
```lua
-- ~/.config/ART/usercommands/lua/mon_script.lua
print("Photo reçue: " .. arg[1])
```

### Exemple : Fusionner 3 photos avec Hugin
ART → Sélectionnez 3 photos RAW d'expositions différentes → Clic droit → Le ARTherapee Compagnon → Cliquez "Hugin" → Hugin reçoit les 3 fichiers → Fusion HDR ! 🎉

## 📚 Documentation

- [INSTALLATION.md](INSTALLATION.md) - Guide détaillé
- [GUIDE_1.2.md](GUIDE_1.2.md) - Guide complet des scripts (bash/python/lua)
- [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) - Architecture technique

## 📁 Structure

- `select-editor.py` - Application principale (support bash/python/lua + multi-fichiers)
- `select-editor-config.json` - Configuration des éditeurs
- `~/.config/ART/usercommands/bash/` - Scripts bash personnalisés
- `~/.config/ART/usercommands/python/` - Scripts Python personnalisés
- `~/.config/ART/usercommands/lua/` - Scripts Lua personnalisés

## 🔗 Liens

- GitHub: https://github.com/carafife/ARTcompagnon
- ART Raw Editor: https://github.com/agriggio/art

## 📝 Licence

MIT - **Créé avec ❤️ par carafife**