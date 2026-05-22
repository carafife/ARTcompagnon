#!/usr/bin/env python3
import sys, json, subprocess, os, shutil, threading, urllib.request, zipfile, tempfile, time
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QTreeWidget, QTreeWidgetItem, 
                              QListWidgetItem, QPushButton, QLabel, QTabWidget, QWidget, 
                              QLineEdit, QComboBox, QMessageBox, QFileDialog, QTextEdit)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QPixmap, QTextCursor
from themes_data import THEMES

# =====================================
# Gestion des traductions
# =====================================TRANSLATIONS = {}

def load_translations():
    """Charge les traductions depuis translations.json"""
    global TRANSLATIONS
    config_path = os.path.join(os.path.dirname(__file__), "translations.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            TRANSLATIONS = json.load(f)
    except:
        print("⚠️  Erreur chargement translations.json")
        TRANSLATIONS = {"fr": {}, "en": {}}

def get_text(key, lang="fr"):
    """Retourne le texte traduit pour une clé"""
    if not TRANSLATIONS:
        load_translations()
    return TRANSLATIONS.get(lang, {}).get(key, key)

def load_language_config():
    """Charge la langue sauvegardée"""
    config_path = os.path.expanduser("~/.config/ARTcompagnon/artcompagnon-config.json")
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('language', 'fr')
    except:
        return 'fr'

def save_language_config(language):
    """Sauvegarde la langue choisie"""
    config_path = os.path.expanduser("~/.config/ARTcompagnon/artcompagnon-config.json")
    try:
        config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
        config['language'] = language
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    except:
        pass

# Charger les traductions au démarrage
load_translations()

# =====================================
# Gestion des thèmes
# =====================================
def load_theme_config():
    """Charge la config du thème"""
    config_path = os.path.expanduser("~/.config/ARTcompagnon/artcompagnon-config.json")
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('theme', 'defaut')
    except:
        return 'defaut'

def save_theme_config(theme_name):
    """Sauvegarde la config du thème"""
    config_path = os.path.expanduser("~/.config/ARTcompagnon/artcompagnon-config.json")
    try:
        config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
        config['theme'] = theme_name
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    except:
        pass

def apply_theme_to_app(parent_widget, theme_name):
    """Applique le thème au widget parent"""
    if theme_name in THEMES:
        stylesheet = THEMES[theme_name]
        parent_widget.setStyleSheet(stylesheet)

# =====================================
# Splash Screen
# =====================================class SplashScreen(QDialog):
    def __init__(self, logo_path):
        super().__init__()
        self.logo_path = logo_path
        self.init_ui()
        self.center_window()
        self.fade_in()
    
    def init_ui(self):
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 800, 500)
        self.setStyleSheet("background-color: #454545; border-radius: 10px;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo
        logo_container = QWidget()
        logo_layout = QVBoxLayout()
        logo_layout.setContentsMargins(0, 30, 0, 20)
        logo_label = QLabel()
        if os.path.exists(self.logo_path):
            pixmap = QPixmap(self.logo_path).scaledToWidth(380, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)
        logo_container.setLayout(logo_layout)
        layout.addWidget(logo_container)
        
        # Texte - sera animé
        self.text_label = QLabel("v3.1 Beta - Powered by Carafife")
        text_font = QFont("Sans", 14)
        text_font.setBold(True)
        self.text_label.setFont(text_font)
        self.text_label.setStyleSheet("color: #C97D3A; background-color: transparent;")
        self.text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.text_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def center_window(self):
        """Centre la splash au centre de l'écran"""
        screen_geometry = QApplication.desktop().screenGeometry()
        window_geometry = self.frameGeometry()
        center_x = (screen_geometry.width() - window_geometry.width()) // 2
        center_y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(center_x, max(0, center_y))
    
    def fade_in(self):
        """Animation fade in rapide du logo, puis du texte avec effet zoom"""
        self.setWindowOpacity(0)
        self.show()
        
        # Fade in du splash - RAPIDE (6 étapes au lieu de 11)
        for i in range(0, 6):
            self.setWindowOpacity(i / 5.0)
            QApplication.processEvents()
            threading.Event().wait(0.03)
        
        # Animation du texte: zoom in/out (pulse) centré - PLUS LONG (10 étapes)
        for i in range(0, 10):
            if i <= 5:
                size = 8 + (i / 5.0) * 16
            else:
                size = 24 - ((i - 5) / 5.0) * 10
            
            text_font = QFont("Sans", int(size))
            text_font.setBold(True)
            self.text_label.setFont(text_font)
            QApplication.processEvents()
            threading.Event().wait(0.07)
        
        # Pause réduite à 0.3s
        time.sleep(0.3)
    
    def fade_out(self):
        """Animation fade out RAPIDE"""
        for i in range(5, -1, -1):
            self.setWindowOpacity(i / 5.0)
            QApplication.processEvents()
            threading.Event().wait(0.02)
        self.close()

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
        
        # Langue et thème
        self.current_language = load_language_config()
        self.current_theme = load_theme_config()
        
        # Créer les dossiers de scripts s'ils n'existent pas
        for folder in ['bash', 'python', 'lua']:
            folder_path = os.path.join(self.scripts_dir, folder)
            os.makedirs(folder_path, exist_ok=True)
        self.load_config()
        self.init_ui()
        self.center_window()
        apply_theme_to_app(self, self.current_theme)
        # Initialiser langue au démarrage SEULEMENT si pas français (ui créée en fr par défaut)
        if self.current_language != 'fr':
            self.update_ui_language()
    
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
    
    def center_window(self):
        """Centre la fenêtre au centre de l'écran"""
        screen_geometry = QApplication.desktop().screenGeometry()
        window_geometry = self.frameGeometry()
        center_x = (screen_geometry.width() - window_geometry.width()) // 2
        center_y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(center_x, max(0, center_y))
    
    def init_ui(self):
        self.setWindowTitle("Le ARTherapee Compagnon 🇫🇷 v3.1 Beta")
        self.setGeometry(100, 100, 700, 580)
        self.setMinimumSize(700, 580)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)
        
        header_layout = QHBoxLayout()
        
        logo_label = QLabel()
        if os.path.exists(self.logo_path):
            pixmap = QPixmap(self.logo_path).scaledToWidth(150, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        header_layout.addWidget(logo_label)
        header_layout.addStretch()
        
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
        footer_font = QFont("Sans", 12)
        footer.setFont(footer_font)
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)
    
    def create_editors_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Thème et Langue - côte à côte, petits
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(10)
        
        # Thème
        theme_label = QLabel(get_text('theme_label', self.current_language))
        theme_label.setMaximumWidth(50)
        self.theme_combo = QComboBox()
        self.theme_combo.setMaximumWidth(120)
        # Affiche les noms traduits, stocke les clés en UserRole
        self.theme_keys = list(THEMES.keys())
        for key in self.theme_keys:
            self.theme_combo.addItem(get_text(f'theme_{key}', self.current_language), key)
        current_theme = load_theme_config()
        if current_theme in self.theme_keys:
            theme_index = self.theme_keys.index(current_theme)
            self.theme_combo.setCurrentIndex(theme_index)
        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)
        
        # Langue
        language_label = QLabel(get_text('language_label', self.current_language))
        language_label.setMaximumWidth(60)
        self.language_combo = QComboBox()
        self.language_combo.setMaximumWidth(100)
        self.language_combo.addItems(['Français', 'English'])
        lang_index = 1 if self.current_language == 'en' else 0
        self.language_combo.setCurrentIndex(lang_index)
        self.language_combo.currentIndexChanged.connect(self.on_language_changed)
        
        settings_layout.addWidget(theme_label)
        settings_layout.addWidget(self.theme_combo)
        settings_layout.addWidget(language_label)
        settings_layout.addWidget(self.language_combo)
        settings_layout.addStretch()
        
        layout.addLayout(settings_layout)
        
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
        
        install_pack_btn = QPushButton("📦 Installer Pack")
        install_pack_btn.setMaximumWidth(160)
        install_pack_btn.setMinimumHeight(32)
        install_pack_btn.setToolTip("Télécharger et installer un pack de scripts")
        install_pack_btn.clicked.connect(self.install_pack_from_github)
        btn_layout.addWidget(install_pack_btn)
        
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
    
    def on_theme_changed(self, index):
        # Récupère la clé du thème stockée en UserRole
        theme_key = self.theme_combo.currentData()
        if theme_key:
            apply_theme_to_app(self, theme_key)
            save_theme_config(theme_key)
    
    def on_language_changed(self, index):
        """Change la langue et met à jour l'interface"""
        lang = 'en' if index == 1 else 'fr'
        self.current_language = lang
        save_language_config(lang)
        self.update_ui_language()
    
    def update_ui_language(self):
        """Met à jour TOUS les textes de l'UI selon la langue"""
        lang = self.current_language
        
        # Fenêtre
        self.setWindowTitle(get_text('window_title', lang))
        
        # Tabs
        tabs = self.findChild(QTabWidget)
        if tabs:
            tabs.setTabText(0, get_text('tab_editors', lang))
            tabs.setTabText(1, get_text('tab_manage', lang))
            tabs.setTabText(2, get_text('tab_scripts', lang))
        
        # Mettre à jour les noms des thèmes dans le combobox
        if hasattr(self, 'theme_combo') and hasattr(self, 'theme_keys'):
            current_key = self.theme_combo.currentData()
            self.theme_combo.clear()
            for key in self.theme_keys:
                self.theme_combo.addItem(get_text(f'theme_{key}', lang), key)
            # Restaure le thème sélectionné
            if current_key and current_key in self.theme_keys:
                idx = self.theme_keys.index(current_key)
                self.theme_combo.setCurrentIndex(idx)
        
        # Traduire TOUS les QLabel
        label_mapping = {
            'Thème:': 'theme_label',
            'Theme:': 'theme_label',
            'Langue:': 'language_label',
            'Language:': 'language_label',
            'Éditeurs disponibles:': 'available_editors',
            'Available editors:': 'available_editors',
            'Scripts disponibles:': 'available_scripts',
            'Available scripts:': 'available_scripts',
            'Ajouter un nouvel éditeur:': 'add_editor_section',
            'Add a new editor:': 'add_editor_section',
            'Nom:': 'name_label',
            'Name:': 'name_label',
            'Description:': 'description_label',
            'Commande:': 'command_label',
            'Command:': 'command_label',
            'Supprimer un éditeur:': 'remove_editor_section',
            'Remove an editor:': 'remove_editor_section'
        }
        
        for label in self.findChildren(QLabel):
            text = label.text()
            if text in label_mapping:
                label.setText(get_text(label_mapping[text], lang))
        
        # Traduire TOUS les QPushButton
        button_mapping = {
            'Ouvrir': 'open_btn',
            'Open': 'open_btn',
            'Fermer': 'close_btn',
            'Close': 'close_btn',
            '▶️ Exécuter': 'execute_btn',
            '▶️ Execute': 'execute_btn',
            '➖ Supprimer': 'remove_script_btn',
            '➖ Remove': 'remove_script_btn',
            'Ajouter': 'add_btn',
            'Add': 'add_btn',
            'Supprimer': 'remove_editor_btn',
            'Remove': 'remove_editor_btn',
            '📤 Charger un script': 'upload_script_btn',
            '📥 Charger un script': 'upload_script_btn',
            '📤 Upload script': 'upload_script_btn',
            '🔄 Rafraîchir': 'refresh_scripts_btn',
            '🔄 Refresh': 'refresh_scripts_btn',
            '🗑️ Nettoyer cache': 'clear_cache_btn',
            '🗑️ Clear cache': 'clear_cache_btn',
            '📁 Config cache': 'config_cache_btn',
            '⚙️ Config cache': 'config_cache_btn',
            '⚙️ Configure cache': 'config_cache_btn',
            '📦 Installer Pack': 'install_pack_btn',
            '📦 Install Pack': 'install_pack_btn',
            '➕ Ajouter': 'add_btn',
            '➕ Add': 'add_btn',
            '➖ Supprimer': 'remove_editor_btn',
            '➖ Remove': 'remove_editor_btn'
        }
        
        for button in self.findChildren(QPushButton):
            text = button.text()
            if text in button_mapping:
                button.setText(get_text(button_mapping[text], lang))
        
        # Traduire les placeholders des QLineEdit
        for line_edit in self.findChildren(QLineEdit):
            placeholder = line_edit.placeholderText()
            if placeholder in ['ex: MonEditeur', 'ex: MyEditor']:
                line_edit.setPlaceholderText(get_text('name_placeholder', lang))
            elif placeholder in ['ex: Mon éditeur préféré', 'ex: My favorite editor']:
                line_edit.setPlaceholderText(get_text('desc_placeholder', lang))
            elif placeholder in ['ex: /usr/bin/monapp', 'ex: /usr/bin/myapp']:
                line_edit.setPlaceholderText(get_text('cmd_placeholder', lang))

    def launch_selected_editor(self):
        item = self.editors_list.currentItem()
        if item:
            editor = item.data(Qt.UserRole)
            try:
                cmd = editor['command']
                cmd = os.path.expandvars(os.path.expanduser(cmd))
                subprocess.Popen(cmd + ' ' + ' '.join(self.image_files), shell=True)
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
    
    def load_script(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un script", os.path.expanduser("~"), "Scripts (*.sh *.py *.lua *.txt);;Tous les fichiers (*)")
        if file_path:
            filename = os.path.basename(file_path)
            
            # Détecter le type
            if filename.endswith('.sh'):
                dest_folder = 'bash'
            elif filename.endswith('.py'):
                dest_folder = 'python'
            elif filename.endswith('.lua'):
                dest_folder = 'lua'
            else:
                dest_folder = 'bash'
            
            # Demander la catégorie (photo ou utilitaire)
            msg = QMessageBox()
            msg.setWindowTitle("Choisir la catégorie")
            msg.setText(f"Où placer ce script {dest_folder}?")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            
            btn_photo = msg.addButton("📷 photo", QMessageBox.AcceptRole)
            btn_utilitaire = msg.addButton("🛠️ utilitaire", QMessageBox.RejectRole)
            msg.setDefaultButton(btn_photo)
            
            msg.exec_()
            
            if msg.clickedButton() == btn_photo:
                subcategory = 'photo'
            elif msg.clickedButton() == btn_utilitaire:
                subcategory = 'utilitaire'
            else:
                return
            
            # Créer les dossiers s'ils n'existent pas
            dest_dir = os.path.join(self.scripts_dir, dest_folder, subcategory)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)
            
            try:
                shutil.copy2(file_path, dest_path)
                os.chmod(dest_path, 0o755)
                self.refresh_scripts_list()
                QMessageBox.information(self, "Succès", f"Script '{filename}' importé dans {dest_folder}/{subcategory}/!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible d'importer le script: {e}")

    def refresh_scripts_list(self):
        self.scripts_tree.clear()
        if not os.path.exists(self.scripts_dir):
            os.makedirs(self.scripts_dir, exist_ok=True)
        
        # 1. D'ABORD les 3 scripts LEGACY au premier niveau
        bash_dir = os.path.join(self.scripts_dir, 'bash')
        legacy_scripts = {
            'nind_denoise_raw.sh': '🚀 Synde Noise',
            'smart_masking.sh': '🤖 Smart Masking',
            'ctl-launcher.sh': '🎨 CT Launcher'
        }
        
        for script_name, label in legacy_scripts.items():
            script_path = os.path.join(bash_dir, script_name)
            if os.path.isfile(script_path):
                item = QTreeWidgetItem([label])
                item.setData(0, Qt.UserRole, os.path.join('bash', script_name))
                self.scripts_tree.addTopLevelItem(item)
        
        # 2. PUIS les 3 langages avec photo/utilitaire
        folders = {'bash': '🔧', 'python': '🐍', 'lua': '🌙'}
        subfolder_icons = {'photo': '📷', 'utilitaire': '🛠️'}
        
        for folder_name, icon in folders.items():
            folder_path = os.path.join(self.scripts_dir, folder_name)
            if os.path.isdir(folder_path):
                folder_item = QTreeWidgetItem([f'{icon} {folder_name.upper()}'])
                has_content = False
                
                # Sous-dossiers photo/utilitaire UNIQUEMENT
                for subfolder_name in ['photo', 'utilitaire']:
                    subfolder_path = os.path.join(folder_path, subfolder_name)
                    if os.path.isdir(subfolder_path):
                        scripts = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
                        if scripts:
                            subfolder_item = QTreeWidgetItem([f'{subfolder_icons.get(subfolder_name, "📁")} {subfolder_name.capitalize()}'])
                            folder_item.addChild(subfolder_item)
                            has_content = True
                            for script in sorted(scripts):
                                child = QTreeWidgetItem([script])
                                child.setData(0, Qt.UserRole, os.path.join(folder_name, subfolder_name, script))
                                subfolder_item.addChild(child)
                            subfolder_item.setExpanded(True)
                
                if has_content:
                    self.scripts_tree.addTopLevelItem(folder_item)
                    folder_item.setExpanded(True)

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
    

    def install_pack_from_github(self):
        """Télécharger et installer un pack depuis GitHub ARTcompagnon-Scripts"""
        def download_and_install():
            try:
                import json as json_module
                
                # URL du dernier release
                release_url = "https://api.github.com/repos/carafife/ARTcompagnon-Scripts/releases/latest"
                
                # Télécharger les infos du release
                with urllib.request.urlopen(release_url, timeout=10) as response:
                    release_data = json_module.loads(response.read().decode())
                
                # Trouver l'asset pack-basic.zip
                assets = release_data.get('assets', [])
                pack_url = None
                for asset in assets:
                    if asset['name'] == 'pack-basic.zip':
                        pack_url = asset['browser_download_url']
                        break
                
                if not pack_url:
                    QMessageBox.warning(self, "Erreur", "Pack pack-basic.zip non trouvé dans les releases!")
                    return
                
                # Télécharger le pack
                temp_dir = tempfile.mkdtemp()
                pack_path = os.path.join(temp_dir, 'pack-basic.zip')
                
                # Télécharger avec timeout
                urllib.request.urlretrieve(pack_url, pack_path)
                
                # Lancer le script d'installation
                script_dir = os.path.dirname(os.path.abspath(__file__))
                install_script = os.path.join(script_dir, "install-scripts", "install-pack.sh")
                result = subprocess.run(['bash', install_script, pack_path], capture_output=True, text=True)
                
                # Nettoyer
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
                
                if result.returncode == 0:
                    # Rafraîchir la liste
                    self.refresh_scripts_list()
                    QMessageBox.information(self, "Succès", "✅ Pack installé avec succès!")
                else:
                    QMessageBox.critical(self, "Erreur", f"❌ Erreur lors de l'installation:\n{result.stderr}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"❌ Erreur lors de l'installation: {str(e)}")
        
        # Lancer le téléchargement dans un thread séparé
        thread = threading.Thread(target=download_and_install, daemon=True)
        thread.start()
        
        # Afficher un message pendant le téléchargement
        QMessageBox.information(self, "Info", "⏳ Téléchargement et installation en cours...\nCela peut prendre quelques secondes.")



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
    
    # Afficher le splash screen IMMÉDIATEMENT
    splash = SplashScreen(logo)
    
    # Forcer le rendu du splash tout de suite
    app.processEvents()
    app.processEvents()
    
    # ⏱️ Mesurer le temps de création d'ARTcompagnon
    import time as time_module
    start_time = time_module.time()
    
    # Créer ARTcompagnon
    companion = ARTCompanion(config, sys.argv[1:], logo)
    
    end_time = time_module.time()
    load_time = end_time - start_time
    
    print(f"⏱️  ARTcompagnon chargé en {load_time:.2f}s")
    
    # Attendre minimum 0.8s (timing parfait)
    time.sleep(max(0.8, load_time * 0.8))
    
    # Fade out du splash RAPIDE
    splash.fade_out()
    
    # Afficher ARTcompagnon IMMÉDIATEMENT
    companion.show()
    companion.exec_()
