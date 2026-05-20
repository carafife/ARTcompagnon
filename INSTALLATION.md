# 📖 Guide d'Installation - Le ARTherapee Compagnon v1.5.4

## 🚀 Installation automatisée (recommandée)

### Étape 1 : Cloner le dépôt
```bash
cd ~
git clone https://github.com/votre-username/ARTcompagnon.git
cd art-compagnon
```

### Étape 2 : Lancer l'installation
```bash
./install.sh
```

C'est tout ! Le script crée automatiquement :
- ✅ Le fichier de configuration dans `~/.config/ART/usercommands/`
- ✅ Les dossiers pour les scripts (`bash/`, `python/`, `lua/`)

---

## 📦 Prérequis

### ⚠️ Important
**Le ARTherapee Compagnon fonctionne GARANTIE avec ART compilé uniquement.**

ARTcompagnon ne fonctionne pas avec:
- ❌ Flatpak (ART sandboxé)
- ❌ AppImage (ART portable)

**Vous devez compiler ART depuis les sources.**

### Système
- **Linux** (Fedora, Ubuntu, Debian, etc.)
- **ART compilé** (https://github.com/agriggio/art)

### Logiciels
```bash
# Fedora
sudo dnf install python3 python3-pyqt5 git gnome-terminal

# Ubuntu/Debian
sudo apt install python3 python3-pyqt5 git gnome-terminal
```

### Python
- Python 3.6+
- PyQt5 5.15+

---

## 🔧 Vérification de l'installation

Après l'installation, vérifiez les dossiers créés :

```bash
# Dossier de configuration
ls -la ~/.config/ART/usercommands/select-editor.txt

# Dossiers des scripts (créés automatiquement au 1er lancement)
ls -la ~/.config/ART/usercommands/bash/
ls -la ~/.config/ART/usercommands/python/
ls -la ~/.config/ART/usercommands/lua/
```

---

## 🎯 Premier lancement

1. Lancez **ART**
2. Ouvrez une image RAW
3. Cliquez sur **"External Editor"** dans le menu (ou Ctrl+E)
4. **Le ARTherapee Compagnon** s'ouvre ! 🎉

---

## 📝 Ajouter vos scripts personnalisés

### Méthode 1 : Depuis l'interface (recommandée)
1. Ouvrez ARTcompagnon
2. Cliquez sur **"📥 Charger un script"**
3. Sélectionnez votre fichier (`.sh`, `.py`, `.lua`)
4. ✅ Le script est automatiquement copié au bon endroit!

### Méthode 2 : Copier manuellement

**Scripts Bash :**
```bash
cp mon-script.sh ~/.config/ART/usercommands/bash/
chmod +x ~/.config/ART/usercommands/bash/mon-script.sh
```

**Scripts Python :**
```bash
cp mon-script.py ~/.config/ART/usercommands/python/
chmod +x ~/.config/ART/usercommands/python/mon-script.py
```

**Scripts Lua :**
```bash
cp mon-script.lua ~/.config/ART/usercommands/lua/
```

---

## 📋 Exemple de script Bash

Créez `~/.config/ART/usercommands/bash/exemple.sh` :

```bash
#!/bin/bash
# Script exemple : traiter une image
IMAGE="$1"
echo "Traitement de : $IMAGE"
echo "✅ Terminé!"
```

Rendez-le exécutable :
```bash
chmod +x ~/.config/ART/usercommands/bash/exemple.sh
```

---

## 🔌 Configuration des éditeurs

Le fichier `select-editor-config.json` contient vos éditeurs préférés :

```json
{
  "editors": [
    {
      "name": "GIMP",
      "description": "GNU Image Manipulation Program",
      "command": "gimp"
    },
    {
      "name": "Krita",
      "description": "Digital Painting Application",
      "command": "krita"
    }
  ]
}
```

Vous pouvez :
- ➕ **Ajouter** des éditeurs via l'interface (onglet "Éditeurs")
- ➖ **Supprimer** des éditeurs via l'interface

---

## 🐛 Dépannage

### Le programme ne démarre pas
```bash
# Vérifiez PyQt5
python3 -c "import PyQt5; print('PyQt5 OK')"

# Vérifiez les droits
chmod +x ~/art-compagnon/select-editor.py
```

### Les scripts ne s'exécutent pas
```bash
# Vérifiez les droits (Bash et Python)
chmod +x ~/.config/ART/usercommands/bash/*.sh
chmod +x ~/.config/ART/usercommands/python/*.py

# Vérifiez le shebang (Bash)
head -1 ~/.config/ART/usercommands/bash/mon-script.sh
# Doit commencer par: #!/bin/bash
```

### ART ne reconnaît pas le programme
```bash
# Vérifiez le fichier de config
cat ~/.config/ART/usercommands/select-editor.txt

# Relancez ART
pkill ART
ART &
```

---

## 📞 Support

- Problèmes ? Ouvrez une issue sur GitHub
- Questions ? Consultez la documentation ART : https://github.com/agriggio/art

---

**Bon traitement d'images ! 🎨**
