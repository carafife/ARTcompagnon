#!/usr/bin/env python3
import sys, json, subprocess, os, shutil, threading
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QTreeWidget, QTreeWidgetItem, 
                              QListWidgetItem, QPushButton, QLabel, QTabWidget, QWidget, 
                              QLineEdit, QComboBox, QMessageBox, QFileDialog, QTextEdit)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QPixmap, QTextCursor

class OutputEmitter(QObject):
    output_signal = pyqtSignal(str)

class TerminalWindow(QDialog):
    def __init__(self, script_path, image_files):
        super().__init__()
        self.script_path = script_path
        self.image_files = image_files if isinstance(image_files, list) else [image_files]
        self.init_ui()
        self.run_script()
    
    def init_ui(self):
        self.setWindowTitle("Exécution du script")
        self.setGeometry(100, 100, 700, 500)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Exécution: {os.path.basename(self.script_path)}"))
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #1a1a1a; color: #00ff00; font-family: monospace;")
        layout.addWidget(self.output)
        close_btn = QPushButton("Fermer")
        close_btn.setToolTip("Fermer cette fenêtre")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.setLayout(layout)
        self.emitter = OutputEmitter()
        self.emitter.output_signal.connect(self.append_output)
    
    def run_script(self):
        def execute():
            try:
                process = subprocess.Popen(['bash', self.script_path] + self.image_files,
                                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                         text=True, bufsize=1)
                for line in process.stdout:
                    self.emitter.output_signal.emit(line.rstrip())
                process.wait()
                if process.returncode == 0:
                    self.emitter.output_signal.emit("\n✅ Script terminé avec succès!")
                else:
                    self.emitter.output_signal.emit(f"\n❌ Erreur: code {process.returncode}")
            except Exception as e:
                self.emitter.output_signal.emit(f"❌ Erreur: {str(e)}")
        
        thread = threading.Thread(target=execute, daemon=True)
        thread.start()
    
    def append_output(self, text):
        self.output.append(text)
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.output.setTextCursor(cursor)

class ARTCompanion(QDialog):
    def __init__(self, config_file, image_files, logo_path):
        super().__init__()
        self.config_file = config_file
        self.image_files = image_files if isinstance(image_files, list) else [image_files]
        self.logo_path = logo_path
        self.scripts_dir = os.path.expanduser("~/.config/ART/usercommands")
        
        # Créer les dossiers de scripts s'ils n'existent pas
        for folder in ['bash', 'python', 'lua']:
            folder_path = os.path.join(self.scripts_dir, folder)
            os.makedirs(folder_path, exist_ok=True)
        self.load_config()
        self.init_ui()
        self.apply_theme()
    
    def find_terminal(self):
        """Trouve un terminal disponible"""
        terminals = {
            'gnome-terminal': ['gnome-terminal', '--', 'bash', '{script}', '{file}'],
            'xterm': ['xterm', '-e', 'bash {script} {file}'],
            'konsole': ['konsole', '-e', 'bash {script} {file}'],
            'xfce4-terminal': ['xfce4-terminal', '-e', 'bash {script} {file}'],
            'terminator': ['terminator', '-e', 'bash {script} {file}'],
        }
        for term_name, cmd in terminals.items():
            if shutil.which(term_name):
                return cmd
        return None
    
    def load_config(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def init_ui(self):
        self.setWindowTitle("Le ARTherapee Compagnon 🇫🇷 v1.5.3-beta")
        self.setGeometry(100, 100, 700, 580)
        self.setMinimumSize(700, 580)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)
        
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        
        logo_label = QLabel()
        if os.path.exists(self.logo_path):
            pixmap = QPixmap(self.logo_path).scaledToWidth(56, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        header_layout.addWidget(logo_label)
        
        title_section = QVBoxLayout()
        title_section.setSpacing(3)
        
        title = QLabel("Le ARTherapee Compagnon")
        title_font = QFont("Sans", 16)
        title_font.setBold(True)
        title_font.setWeight(QFont.ExtraBold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title_section.addWidget(title)
        
        subtitle = QLabel("Gérez vos outils")
        subtitle_font = QFont("Sans", 9)
        subtitle_font.setBold(True)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        title_section.addWidget(subtitle)
        
        header_layout.addLayout(title_section)
        header_layout.addStretch()
        
        flag = QLabel("🇫🇷")
        flag_font = QFont()
        flag_font.setPointSize(16)
        flag.setFont(flag_font)
        flag.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        header_layout.addWidget(flag)
        
        main_layout.addLayout(header_layout)
        
        tabs = QTabWidget()
        tabs.addTab(self.create_editors_tab(), "📋 Éditeurs")
        tabs.addTab(self.create_manage_tab(), "➕ Gérer")
        tabs.addTab(self.create_scripts_tab(), "🔧 Scripts ART")
        main_layout.addWidget(tabs)
        
        footer = QLabel('<a href="https://artherapee.fr/" style="color: #c97d3a; text-decoration: none;">🌐 artherapee.fr</a>')
        footer.setOpenExternalLinks(True)
        footer.setAlignment(Qt.AlignCenter)
        footer_font = QFont("Sans", 8)
        footer.setFont(footer_font)
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)
    
    def create_editors_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.editors_list = QListWidget()
        self.update_editors_list()
        self.editors_list.itemDoubleClicked.connect(self.launch_selected_editor)
        layout.addWidget(self.editors_list)
        btn_layout = QHBoxLayout()
        open_btn = QPushButton("Ouvrir")
        open_btn.setToolTip("Ouvrir le dossier des scripts")
        close_btn = QPushButton("Fermer")
        close_btn.setToolTip("Fermer cette fenêtre")
        open_btn.setMaximumWidth(110)
        close_btn.setMaximumWidth(110)
        open_btn.setMinimumHeight(32)
        close_btn.setMinimumHeight(32)
        open_btn.clicked.connect(self.launch_selected_editor)
        close_btn.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        widget.setLayout(layout)
        return widget
    
    def create_manage_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        add_section = QVBoxLayout()
        add_section.addWidget(QLabel("Ajouter un nouvel éditeur:"))
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nom:"))
        self.add_name_input = QLineEdit()
        self.add_name_input.setPlaceholderText("ex: MonEditeur")
        name_layout.addWidget(self.add_name_input)
        add_section.addLayout(name_layout)
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Description:"))
        self.add_desc_input = QLineEdit()
        self.add_desc_input.setPlaceholderText("ex: Mon éditeur préféré")
        desc_layout.addWidget(self.add_desc_input)
        add_section.addLayout(desc_layout)
        cmd_layout = QHBoxLayout()
        cmd_layout.addWidget(QLabel("Commande:"))
        self.add_cmd_input = QLineEdit()
        self.add_cmd_input.setPlaceholderText("ex: /usr/bin/monapp")
        cmd_layout.addWidget(self.add_cmd_input)
        add_section.addLayout(cmd_layout)
        add_btn = QPushButton("➕ Ajouter")
        add_btn.setToolTip("Ajouter un nouveau script")
        add_btn.setMaximumWidth(150)
        add_btn.clicked.connect(self.add_editor)
        add_section.addWidget(add_btn)
        layout.addLayout(add_section)
        layout.addSpacing(15)
        remove_section = QVBoxLayout()
        remove_section.addWidget(QLabel("Supprimer un éditeur:"))
        self.remove_combo = QComboBox()
        self.update_remove_combo()
        remove_section.addWidget(self.remove_combo)
        remove_btn = QPushButton("➖ Supprimer")
        remove_btn.setToolTip("Supprimer ce script")
        remove_btn.setMaximumWidth(150)
        remove_btn.clicked.connect(self.remove_editor)
        remove_section.addWidget(remove_btn)
        layout.addLayout(remove_section)
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_scripts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        load_btn = QPushButton("📥 Charger un script")
        load_btn.setMaximumWidth(180)
        load_btn.setMinimumHeight(32)
        load_btn.setToolTip("Charger un script personnalisé")
        load_btn.clicked.connect(self.load_script)
        btn_layout.addWidget(load_btn)
        refresh_btn = QPushButton("🔄 Rafraîchir")
        refresh_btn.setMaximumWidth(140)
        refresh_btn.setMinimumHeight(32)
        refresh_btn.setToolTip("Rafraîchir la liste des scripts")
        refresh_btn.clicked.connect(self.refresh_scripts_list)
        btn_layout.addWidget(refresh_btn)
        
        cache_config_btn = QPushButton("📁 Config cache")
        cache_config_btn.setMaximumWidth(140)
        cache_config_btn.setMinimumHeight(32)
        cache_config_btn.setToolTip("Sélectionner le dossier cache ART")
        cache_config_btn.clicked.connect(self.configure_cache_folder)
        btn_layout.addWidget(cache_config_btn)
        
        cache_clean_btn = QPushButton("🗑️ Nettoyer cache")
        cache_clean_btn.setMaximumWidth(140)
        cache_clean_btn.setMinimumHeight(32)
        cache_clean_btn.setToolTip("Nettoyer les fichiers temporaires TIF")
        cache_clean_btn.clicked.connect(self.clean_cache_folder)
        btn_layout.addWidget(cache_clean_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("Scripts disponibles:"))
        self.scripts_tree = QTreeWidget()
        self.scripts_tree.setHeaderLabel('Scripts disponibles')
        self.refresh_scripts_list()
        layout.addWidget(self.scripts_tree)
        exec_layout = QHBoxLayout()
        exec_layout.setSpacing(10)
        exec_btn = QPushButton("▶️ Exécuter")
        exec_btn.setToolTip("Exécuter le script sélectionné")
        exec_btn.setMaximumWidth(140)
        exec_btn.setMinimumHeight(35)
        exec_btn.clicked.connect(self.execute_selected_script)
        exec_layout.addWidget(exec_btn)
        remove_script_btn = QPushButton("➖ Supprimer")
        remove_script_btn.setToolTip("Supprimer le script sélectionné")
        remove_script_btn.setMaximumWidth(140)
        remove_script_btn.setMinimumHeight(35)
        remove_script_btn.clicked.connect(self.remove_script)
        exec_layout.addWidget(remove_script_btn)
        exec_layout.addStretch()
        layout.addLayout(exec_layout)
        widget.setLayout(layout)
        return widget
    
    def update_editors_list(self):
        self.editors_list.clear()
        for editor in self.config['editors']:
            item = QListWidgetItem(f"  {editor['name']}\n  {editor['description']}")
            item.setData(Qt.UserRole, editor)
            item.setSizeHint(QSize(650, 50))
            self.editors_list.addItem(item)
    
    def update_remove_combo(self):
        self.remove_combo.clear()
        for editor in self.config['editors']:
            self.remove_combo.addItem(editor['name'], editor)
    
    def launch_selected_editor(self):
        item = self.editors_list.currentItem()
        if item:
            editor = item.data(Qt.UserRole)
            try:
                cmd = editor['command']
                cmd = os.path.expandvars(os.path.expanduser(cmd))
                subprocess.Popen([cmd] + self.image_files)
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de lancer {editor['name']}: {e}")
    
    def add_editor(self):
        name = self.add_name_input.text().strip()
        desc = self.add_desc_input.text().strip()
        cmd = self.add_cmd_input.text().strip()
        if not all([name, desc, cmd]):
            QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires!")
            return
        self.config['editors'].append({"name": name, "description": desc, "command": cmd})
        self.save_config()
        self.update_editors_list()
        self.update_remove_combo()
        self.add_name_input.clear()
        self.add_desc_input.clear()
        self.add_cmd_input.clear()
        QMessageBox.information(self, "Succès", f"{name} ajouté!")
    
    def remove_editor(self):
        if self.remove_combo.count() == 0:
            QMessageBox.warning(self, "Erreur", "Aucun éditeur à supprimer!")
            return
        editor = self.remove_combo.currentData()
        reply = QMessageBox.question(self, "Confirmer", f"Supprimer {editor['name']}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.config['editors'].remove(editor)
            self.save_config()
            self.update_editors_list()
            self.update_remove_combo()
            QMessageBox.information(self, "Succès", "Éditeur supprimé!")
    
    def load_script(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un script", os.path.expanduser("~"), "Scripts (*.sh *.py *.lua *.txt);;Tous les fichiers (*)")
        if file_path:
            filename = os.path.basename(file_path)
            
            # Détecter le type et le dossier destination
            if filename.endswith('.sh'):
                dest_folder = 'bash'
            elif filename.endswith('.py'):
                dest_folder = 'python'
            elif filename.endswith('.lua'):
                dest_folder = 'lua'
            else:
                dest_folder = 'bash'  # défaut
            
            dest_dir = os.path.join(self.scripts_dir, dest_folder)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)
            
            try:
                shutil.copy2(file_path, dest_path)
                os.chmod(dest_path, 0o755)
                self.refresh_scripts_list()
                QMessageBox.information(self, "Succès", f"Script '{filename}' importé dans {dest_folder}/!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible d'importer le script: {e}")
    
    def refresh_scripts_list(self):
        self.scripts_tree.clear()
        if not os.path.exists(self.scripts_dir):
            os.makedirs(self.scripts_dir, exist_ok=True)
        
        folders = {'bash': '🔧', 'python': '🐍', 'lua': '🌙'}
        found = False
        
        for folder_name, icon in folders.items():
            folder_path = os.path.join(self.scripts_dir, folder_name)
            if os.path.isdir(folder_path):
                scripts = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                if scripts:
                    folder_item = QTreeWidgetItem([f'{icon} {folder_name.upper()}'])
                    self.scripts_tree.addTopLevelItem(folder_item)
                    found = True
                    for script in sorted(scripts):
                        child = QTreeWidgetItem([script])
                        child.setData(0, Qt.UserRole, os.path.join(folder_name, script))
                        folder_item.addChild(child)
                    folder_item.setExpanded(True)
        
        if not found:
            empty = QTreeWidgetItem(['📭 Aucun script trouvé'])
            self.scripts_tree.addTopLevelItem(empty)
    
    def execute_selected_script(self):
        item = self.scripts_tree.currentItem()
        if not item or item.text(0) == '📭 Aucun script trouvé':
            QMessageBox.warning(self, "Erreur", "Sélectionnez un script!")
            return
        
        script_rel = item.data(0, Qt.UserRole)
        if not script_rel:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un script (pas un dossier)!")
            return
        
        script_path = os.path.join(self.scripts_dir, script_rel)
        script_name = os.path.basename(script_rel)
        
        try:
            if script_name.endswith('.sh'):
                subprocess.Popen(['gnome-terminal', '--', 'bash', script_path] + self.image_files)
            elif script_name.endswith('.py'):
                subprocess.Popen(['gnome-terminal', '--', 'python3', script_path] + self.image_files)
            elif script_name.endswith('.lua'):
                subprocess.Popen(['gnome-terminal', '--', 'lua', script_path] + self.image_files)
            else:
                QMessageBox.warning(self, "Erreur", f"Type non supporté: {script_name}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'exécuter: {str(e)}")
    
    def remove_script(self):
        item = self.scripts_tree.currentItem()
        if not item or item.data(0, Qt.UserRole) is None:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un script!")
            return
        script_rel = item.data(0, Qt.UserRole)
        script_path = os.path.join(self.scripts_dir, script_rel)
        reply = QMessageBox.question(self, "Confirmer", f"Supprimer '{os.path.basename(script_rel)}'?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                os.remove(script_path)
                self.refresh_scripts_list()
                QMessageBox.information(self, "Succès", "Script supprimé!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de supprimer: {e}")
    
    def configure_cache_folder(self):
        """Ouvre un dialogue pour configurer le dossier cache"""
        cache_folder = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le dossier cache ART",
            os.path.expanduser("~/.cache/ART")
        )
        if cache_folder:
            import json
            config_file = os.path.join(os.path.dirname(__file__), 'cache_config.json')
            with open(config_file, 'w') as f:
                json.dump({"cache_folder": cache_folder}, f)
            QMessageBox.information(self, "Succès", f"Cache configuré: {cache_folder}")
    
    def clean_cache_folder(self):
        """Nettoie les fichiers .tif du dossier cache"""
        import json
        cache_folder = os.path.expanduser("~/.cache/ART/temp")
        
        # Essayer de charger la config si elle existe
        config_file = os.path.join(os.path.dirname(__file__), 'cache_config.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    cache_folder = config.get("cache_folder", cache_folder)
            except:
                pass
        
        if not os.path.exists(cache_folder):
            QMessageBox.warning(self, "Erreur", f"Dossier introuvable: {cache_folder}")
            return
        
        try:
            tif_files = [f for f in os.listdir(cache_folder) if f.endswith(('.tif', '.TIF'))]
            if not tif_files:
                QMessageBox.information(self, "Info", "Aucun fichier .tif à supprimer")
                return
            
            total_size = 0
            for f in tif_files:
                filepath = os.path.join(cache_folder, f)
                total_size += os.path.getsize(filepath)
                os.remove(filepath)
            
            size_mb = total_size / (1024 * 1024)
            msg = f"✅ Cache nettoyé!\n{len(tif_files)} fichier(s) supprimé(s)\n{size_mb:.1f} MB libérés"
            QMessageBox.information(self, "Succès", msg)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du nettoyage: {e}")
    
    def apply_theme(self):
        dark_stylesheet = """QDialog, QWidget { background-color: #1a1a1a; color: #e8e8e8; } QLabel { color: #e8e8e8; } QListWidget, QLineEdit, QComboBox, QTextEdit { background-color: #252525; border: 1px solid #3a3a3a; color: #e8e8e8; border-radius: 4px; padding: 5px; } QListWidget::item { padding: 8px; border-radius: 4px; } QListWidget::item:selected { background-color: #c97d3a; color: #ffffff; } QListWidget::item:hover { background-color: #2f2f2f; } QPushButton { background-color: #c97d3a; color: #ffffff; border: none; border-radius: 4px; font-weight: bold; font-size: 10px; padding: 3px; font-family: Sans; } QPushButton:hover { background-color: #d9945a; } QPushButton:pressed { background-color: #b96b2a; } QTabWidget::pane { border: 1px solid #3a3a3a; } QTabBar::tab { background-color: #252525; color: #e8e8e8; padding: 5px 15px; border: 1px solid #3a3a3a; } QTabBar::tab:selected { background-color: #c97d3a; color: #ffffff; }"""
        self.setStyleSheet(dark_stylesheet)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: select-editor.py <image_file>")
        sys.exit(1)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config = os.path.join(script_dir, "select-editor-config.json")
    logo = os.path.join(script_dir, "logo.png")
    if not os.path.exists(config):
        print(f"Config not found: {config}")
        sys.exit(1)
    app = QApplication(sys.argv)
    companion = ARTCompanion(config, sys.argv[1:], logo)
    companion.exec_()
