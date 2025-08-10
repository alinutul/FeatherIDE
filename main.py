import sys
import os
import json

from PySide6.QtCore import QCoreApplication, QRect, Qt, QMetaObject
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QMenuBar, QMenu, QStatusBar,
    QTreeView, QTextEdit, QSplitter, QVBoxLayout, QFileSystemModel, QFileDialog,
    QMessageBox, QTabWidget, QLineEdit, QPushButton, QHBoxLayout
)
from file_manager import FileManager
from ui_mainwindow import Ui_MainWindow
from bottom_tabs import BottomTabsWidget
#from themes import apply_monospace_font

from UIs.Disable import Ui_FormDisable
from UIs.Enable import Ui_FormEnable

from ai_config import OllamaThread

from themes import apply_custom_theme1, apply_custom_theme2, apply_custom_theme3, apply_custom_theme4

from syntax_highlighter import CppSyntaxHighlighter

from auto_close import CustomTextEdit
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Setup UI from generated class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        appdata_path = os.getenv('APPDATA')
        folder_path = os.path.join(appdata_path, "FeatherIDE")
        os.makedirs(folder_path, exist_ok=True)
        


        self.json_file_path = os.path.join(folder_path, "comp.json")

        # Initialize data if the file doesn't exist yet
        if not os.path.exists(self.json_file_path) or os.path.getsize(self.json_file_path) == 0:
            data = {"password": "", "comp": 0}
            with open(self.json_file_path, "w") as f:
                json.dump(data, f)
            print("JSON file initialized with default data.")
        else:
            print("JSON file already exists and is not empty.")

        # === Custom layout using splitters ===
        # Vertical splitter to separate editor/tree from bottom tabs
        vertical_splitter = QSplitter(Qt.Vertical)
        # Horizontal splitter to separate file tree from code editor
        horizontal_splitter = QSplitter(Qt.Horizontal)

        # Tree view for file system navigation
        self.tree_view = QTreeView()
        self.model = QFileSystemModel()
        # Set the root path to the current working directory for initial display

        #self.model.setRootPath(os.path.abspath(os.getcwd())) 
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.path.abspath(os.getcwd())))
        horizontal_splitter.addWidget(self.tree_view)
        # Hide unnecessary columns in the tree view
        self.tree_view.hideColumn(2)  # Hide "File Type"
        self.tree_view.hideColumn(3)  # Hide "Last Modified"

        # Code editor area
        self.editor = CustomTextEdit()

        self.editor.setPlaceholderText("Start coding here...")

        
        self.highlighter = CppSyntaxHighlighter(self.editor.document())

        horizontal_splitter.addWidget(self.editor)
        # Set stretch factors for horizontal splitter: tree view takes 1 part, editor takes 3 parts
        horizontal_splitter.setStretchFactor(0, 1)
        horizontal_splitter.setStretchFactor(1, 3)

        self.bottom_tabs = BottomTabsWidget()
                # === Themes Menu ===
        theme_menu = self.menuBar().addMenu("Theme")        

        # Define theme actions
        theme1_action = QAction("Theme 1", self)
        theme2_action = QAction("Theme 2", self)
        theme3_action = QAction("Theme 3", self)
        theme4_action = QAction("Theme 4", self)
        apply_custom_theme1(QApplication.instance())
        # Connect to handler functions
        theme1_action.triggered.connect(lambda: apply_custom_theme1(QApplication.instance()))
        theme2_action.triggered.connect(lambda: apply_custom_theme2(QApplication.instance()))
        theme3_action.triggered.connect(lambda: apply_custom_theme3(QApplication.instance()))
        theme4_action.triggered.connect(lambda: apply_custom_theme4(QApplication.instance()))

        # Add actions to the menu
        theme_menu.addAction(theme1_action)
        theme_menu.addAction(theme2_action)
        theme_menu.addAction(theme3_action)
        theme_menu.addAction(theme4_action)

        #meniu help
        help_menu = self.menuBar().addMenu("Help")

        about_action = QAction("About FeatherIDE", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        help_action = QAction("Help...", self)
        help_action.triggered.connect(self.show_help_dialog)
        help_menu.addAction(help_action)

        

        # Assemble into vertical splitter: horizontal splitter (tree+editor) on top, bottom_tabs at bottom
        vertical_splitter.addWidget(horizontal_splitter)
        vertical_splitter.addWidget(self.bottom_tabs)
        # Set stretch factors for vertical splitter: top section takes 4 parts, bottom takes 1 part
        vertical_splitter.setStretchFactor(0, 4)
        vertical_splitter.setStretchFactor(1, 1)

        # Set the main layout for the central widget
        layout = QVBoxLayout(self.ui.centralwidget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.addWidget(vertical_splitter)
    
        # Set keyboard shortcuts for common actions
        self.ui.actionSave.setShortcut("Ctrl+S")
        self.ui.actionSave_As.setShortcut("Ctrl+Shift+S")
        self.ui.actionOpen.setShortcut("Ctrl+O")
        self.ui.actionNewProject.setShortcut("Ctrl+N") 
        self.ui.actionNewFile.setShortcut("Ctrl+Shift+N") 
        self.ui.actionUndo.setShortcut("Ctrl+Z")
        self.ui.actionRedo.setShortcut("Ctrl+Y")
        self.ui.actionCut.setShortcut("Ctrl+X")
        self.ui.actionCopy.setShortcut("Ctrl+C")
        self.ui.actionPaste.setShortcut("Ctrl+V")
        self.ui.actionDelete.setShortcut("Del")
        self.ui.actionBuild.setShortcut("F7") # Shortcut for Build
        self.ui.actionBuildAndRun.setShortcut("Ctrl+F5") # Shortcut for Build and Run

        # Initialize FileManager, passing necessary UI components and the update_window_title callback
        self.file_manager = FileManager(self, self.editor, self.model, self.tree_view, self.update_window_title)

        # Connect UI actions to FileManager methods
        self.ui.actionNewProject.triggered.connect(self.file_manager.new_project) 
        self.ui.actionNewFile.triggered.connect(self.file_manager.new_file) 
        self.ui.actionOpen.triggered.connect(self.file_manager.open_note)
        self.ui.actionSave.triggered.connect(self.file_manager.save_note)
        self.ui.actionSave_As.triggered.connect(self.file_manager.save_as_note)

        # Connect template actions
        self.ui.actionLoadTemplate.triggered.connect(self.file_manager.load_template) 
        self.ui.actionSaveTemplate.triggered.connect(self.file_manager.save_template) 

        # Connect build actions to new methods in MainWindow
        self.ui.actionBuild.triggered.connect(self.file_manager.build_code1)
        self.ui.actionBuildAndRun.triggered.connect(self.file_manager.build_and_run)

        # Connect competition actions (you'll need to define these methods in FileManager or MainWindow)
        self.ui.actionEnableCompetition.triggered.connect(self.enable_competition_mode)
        self.ui.actionDisableCompetition.triggered.connect(self.disable_competition_mode)

        # Connect chat actions
        self.bottom_tabs.send_chat_button.clicked.connect(self.send_ai_message)
        self.bottom_tabs.chat_input.returnPressed.connect(self.send_ai_message)

        # Connect text editor changes to mark the file as unsaved
        self.editor.textChanged.connect(self.file_manager.mark_unsaved)

        # Connect tree view item clicks to open files
        self.tree_view.clicked.connect(self.file_manager.open_file_from_tree_view)

        # Set the initial window title
        self.update_window_title()

        self.setWindowIcon(QIcon("Resources/feather.ico"))

    def wheelEvent(self, event):
        # Check if Ctrl key is pressed and user is scrolling
        if event.modifiers() == Qt.ControlModifier:
            delta = event.angleDelta().y()
            current_font = self.editor.font()
            font_size = current_font.pointSize()

            # Increase or decrease font size based on scroll direction
            if delta > 0:  # Scroll up -> Increase font size
                new_font_size = font_size + 1
            else:  # Scroll down -> Decrease font size
                new_font_size = font_size - 1

            # Set the new font size
            current_font.setPointSize(new_font_size)
            self.editor.setFont(current_font)

        # Call the default event handler to ensure the scroll works
        super().wheelEvent(event)
        
    def update_window_title(self):
        print("DEBUG: Entering update_window_title")
        file_name, is_unsaved = self.file_manager.get_filename_and_status()
        print(f"DEBUG: file_name={file_name}, is_unsaved={is_unsaved}")
        if is_unsaved:
            title = f"{file_name}* - FeatherIDE"
        else:
            title = f"{file_name} - FeatherIDE"
        print(f"DEBUG: Setting title to: {title}")
        self.setWindowTitle(title)
        print("DEBUG: Exiting update_window_title")

    def save_password_and_enable(self):
        password = self.form.textEdit.toPlainText()

        data = {
                "password": password,
                "comp": 1  # or some other flag you want to save
        }
        
        # Write to a JSON file
        with open(self.json_file_path, "w") as f:
            json.dump(data, f)
        
        self.form_widget.close()
        QMessageBox.information(self, "Competition Mode", "Competition mode is ENABLED!")


    def enter_password(self):
        try:
            with open(self.json_file_path, "r") as f:
                data = json.load(f)
        except:
            return
        password = self.form.textEdit.toPlainText()
        if password == data.get("password",0):
            data = {
                    "password": "",
                    "comp": 0  # or some other flag you want to save
            }
            with open(self.json_file_path, "w") as f:
                json.dump(data, f)

            self.form_widget.close()    
            QMessageBox.information(self, "Competition Mode", "Competition mode is DISABLED!")
        else:
            QMessageBox.warning(self, "Error", "Incorrect password.")

    def enable_competition_mode(self):
        try:
            with open(self.json_file_path, "r") as f:
                data = json.load(f)
        except:
            return
        if  data.get("comp",0) == 0:  # If competition mode is currently DISABLED
            self.form_widget = QWidget()
            self.form = Ui_FormEnable()
            self.form.setupUi(self.form_widget)
            # Connect Save button
            self.form.pushButton.clicked.connect(self.save_password_and_enable)
            self.form_widget.show()
        else:
            QMessageBox.information(self, "Competition Mode", "Competition mode is already ENABLED!")

    def disable_competition_mode(self):
        try:
            with open(self.json_file_path, "r") as f:
                data = json.load(f)
        except:
            return
        if  data.get("comp",0) == 1:
            self.form_widget = QWidget()
            self.form = Ui_FormDisable()
            self.form.setupUi(self.form_widget)
            self.form.pushButton.clicked.connect(self.enter_password)
            self.form_widget.show()
        else:
            QMessageBox.information(self, "Competition Mode", "Competition mode is already DISABLED!")


    def send_ai_message(self):
        try:
            with open(self.json_file_path, "r") as f:
                data = json.load(f)
        except:
            return
        if  data.get("comp",0) == 0:
            user_message = self.bottom_tabs.chat_input.text()
            if not user_message:
                return

            self.bottom_tabs.chat_display.append(f"<b>You:</b> {user_message}")
            self.bottom_tabs.chat_input.clear()
            

            self.bottom_tabs.send_chat_button.setEnabled(False)
            self.bottom_tabs.chat_input.setEnabled(False)
            self.bottom_tabs.chat_display.append("<i>AI is thinking...</i>")


            self.ollama_thread = OllamaThread(prompt=user_message, model_name="openchat")
            self.ollama_thread.response_ready.connect(self._handle_ai_response)
            self.ollama_thread.error_occurred.connect(self._handle_ai_error)
            self.ollama_thread.finished.connect(self._enable_chat_controls) # Re-enable controls when thread finishes
            self.ollama_thread.start() # Start the thread

    def _handle_ai_response(self, response_text):
        """Slot to receive AI response from OllamaThread."""
        self.bottom_tabs.chat_display.append(f"<b>AI:</b> {response_text}")

    def _handle_ai_error(self, error_message):
        """Slot to receive error messages from OllamaThread."""
        self.bottom_tabs.chat_display.append(f"<i style='color: red;'>AI Error: {error_message}</i>")
        QMessageBox.critical(self, "AI Chat Error", error_message)

    def _enable_chat_controls(self):
        """Re-enables chat input and send button."""
        self.bottom_tabs.send_chat_button.setEnabled(True)
        self.bottom_tabs.chat_input.setEnabled(True)
        self.bottom_tabs.chat_input.setFocus() # Put focus back to input field

    def show_about_dialog(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel

        dialog = QDialog(self)
        dialog.setWindowTitle("About FeatherIDE")
        dialog.resize(400, 200)

        layout = QVBoxLayout(dialog)
        label = QLabel("FeatherIDE v1.0\n\nLightweight IDE for C++ coding and AI integration.\n\nCreated with ❤️ using PySide6.\n\n\n\nAuthors: Ulici Alin and Ivanic Razvan")
        label.setWordWrap(True)

        layout.addWidget(label)
        dialog.exec()

    def show_help_dialog(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit

        dialog = QDialog(self)
        dialog.setWindowTitle("Help - FeatherIDE")
        dialog.resize(500, 300)

        layout = QVBoxLayout(dialog)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(
            "FeatherIDE Help:\n\n"
            "- Ctrl+N: New Project\n"
            "- Ctrl+Shift+N: New File\n"
            "- Ctrl+S: Save File\n"
            "- Ctrl+O: Open File\n"
            "- F7: Build Code\n"
            "- Ctrl+F5: Build and Run\n"
            "- Use the AI Chat tab to ask coding questions\n"
            "- Use the Notes tab to write temporary notes\n"
            "- Use Templates to save a starting code for future projects\n"
            "- Enable Competition Mode to restrict actions"
        )

        layout.addWidget(text_edit)
        dialog.setLayout(layout)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())