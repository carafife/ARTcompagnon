# 🎨 Le ARTherapee Compagnon

Un gestionnaire d'éditeurs et de scripts pour ART (ART Raw Editor).

## 🌟 Caractéristiques

- 📋 Gérez vos éditeurs externes (GIMP, Krita, RawTherapee, Hugin, etc.)
- 🔧 Créez et exécutez des scripts bash personnalisés
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

### Exemple : Fusionner 3 photos avec Hugin
ART → Sélectionnez 3 photos RAW d'expositions différentes → Clic droit → Le ARTherapee Compagnon → Cliquez "Hugin" → Hugin reçoit les 3 fichiers → Fusion HDR ! 🎉

## 📚 Documentation

- [INSTALLATION.md](INSTALLATION.md) - Guide détaillé
- [GUIDE_UTILISATEUR.pdf](GUIDE_UTILISATEUR.pdf) - Manuel complet

## 📁 Structure

- `select-editor.py` - Application principale (support multi-fichiers)
- `select-editor-config.json` - Configuration des éditeurs
- `custom-tasks/` - Vos scripts bash personnalisés

## 📝 Licence

MIT - **Créé avec ❤️ par carafife**
