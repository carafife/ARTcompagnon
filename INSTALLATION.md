# 📖 Guide d'Installation - Le ARTherapee Compagnon

## 🚀 Installation automatisée (recommandée)

### Étape 1 : Cloner le dépôt

```bash
cd ~
git clone https://github.com/votre-username/ARTcompagnon.git
cd ARTcompagnon
```

### Étape 2 : Lancer l'installation

```bash
./install.sh
```

C'est tout ! Le script crée automatiquement :
- ✅ Le dossier de configuration ART
- ✅ Le dossier de l'application dans `/home/votre-user/Programmes/ARTcompagnon/`
- ✅ Le dossier pour les scripts personnalisés

---

## 📦 Prérequis

### Système
- **Linux** (Fedora, Ubuntu, Debian, etc.)
- **ART** installé (https://artherapee.fr/)

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
# Dossier config ART
ls -la ~/.config/ART/usercommands/select-editor.txt

# Dossier application
ls -la ~/Programmes/ARTcompagnon/

# Dossier custom-tasks
ls -la ~/Programmes/ARTcompagnon/custom-tasks/
```

---

## 🎯 Premier lancement

1. Lancez **ART**
2. Ouvrez une image RAW
3. Cliquez sur **"External Editor"** dans le menu
4. **Le ARTherapee Compagnon** s'ouvre ! 🎉

---

## 📝 Ajouter vos scripts personnalisés

### Méthode 1 : Depuis l'interface

1. Ouvrez ARTcompagnon
2. Allez dans l'onglet **"🔧 Scripts ART"**
3. Cliquez sur **"📥 Charger un script"**
4. Sélectionnez votre fichier `.sh`

### Méthode 2 : Copier manuellement

```bash
cp mon-script.sh ~/Programmes/ARTcompagnon/custom-tasks/
chmod +x ~/Programmes/ARTcompagnon/custom-tasks/mon-script.sh
```

---

## 📋 Exemple de script personnalisé

Créez `~/Programmes/ARTcompagnon/custom-tasks/traiter-image.sh` :

```bash
#!/bin/bash
# Script exemple : traiter une image

IMAGE="$1"

echo "Traitement de : $IMAGE"
echo "Conversion en sRGB..."
convert "$IMAGE" -colorspace sRGB "${IMAGE%.tif}_sRGB.tif"
echo "✅ Terminé!"
```

Rendez-le exécutable :
```bash
chmod +x ~/Programmes/ARTcompagnon/custom-tasks/traiter-image.sh
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
- ➕ **Ajouter** des éditeurs via l'interface (onglet "➕ Gérer")
- ➖ **Supprimer** des éditeurs via l'interface

---

## 🐛 Dépannage

### Le programme ne démarre pas
```bash
# Vérifiez PyQt5
python3 -c "import PyQt5; print('PyQt5 OK')"

# Vérifiez les droits
chmod +x ~/Programmes/ARTcompagnon/select-editor.py
```

### Les scripts ne s'exécutent pas
```bash
# Vérifiez les droits
chmod +x ~/Programmes/ARTcompagnon/custom-tasks/*.sh

# Vérifiez les chemins dans le script
head -1 ~/Programmes/ARTcompagnon/custom-tasks/mon-script.sh
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
- Questions ? Consultez la documentation ART : https://artherapee.fr/

---

**Bon traitement d'images ! 🎨**
