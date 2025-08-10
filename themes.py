from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase


def apply_custom_theme1(app: QApplication):
    """
    Applies 'Classic Dark' theme.
    Dark background with light text.
    """
    stylesheet = """
    QMainWindow {
        background-color: #2b2b2b; /* Dark grey */
        color: #f0f0f0; /* Light grey text */
    }
    QMenuBar {
        background-color: #3c3f41; /* Slightly lighter dark grey */
        color: #f0f0f0;
        border-bottom: 1px solid #1e1e1e;
    }
    QMenuBar::item {
        background-color: transparent;
        padding: 5px 10px;
    }
    QMenuBar::item:selected {
        background-color: #555555;
    }
    QMenu {
        background-color: #3c3f41;
        border: 1px solid #1e1e1e;
        color: #f0f0f0;
    }
    QMenu::item {
        padding: 5px 20px;
    }
    QMenu::item:selected {
        background-color: #555555;
    }
    QStatusBar {
        background-color: #2b2b2b;
        color: #f0f0f0;
        border-top: 1px solid #1e1e1e;
    }
    QTreeView {
        background-color: #3c3c3c; /* Darker grey for tree view content */
        color: #cccccc; /* Lighter grey text for items */
        border: 1px solid #444444;
        alternate-background-color: #373737;
        selection-background-color: #555555;
        selection-color: #f0f0f0;
        padding: 5px;
        font-size: 10pt;
    }
    QTreeView::branch:selected {
        background-color: #555555;
    }
    /* --- QHeaderView (for Name, Size columns) Styling --- */
    QHeaderView::section {
        background-color: #3c3c3c; /* Match tree view background */
        color: #f0f0f0; /* Light text for headers */
        padding: 5px;
        border: 1px solid #444444;
        border-right: none; /* Optional: remove right border for cleaner look */
        border-top: none; /* Optional: remove top border */
    }
    QHeaderView::section:hover {
        background-color: #4a4a4a;
    }
    QHeaderView::section:pressed {
        background-color: #555555;
    }
    /* --- End QHeaderView Styling --- */

    QTextEdit {
        background-color: #222222; /* Even darker for editor */
        color: #f0f0f0;
        border: 1px solid #444444;
        selection-background-color: #007acc; /* VS Code blue for selection */
        selection-color: #ffffff;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 10pt;
        
    }
    QSplitter::handle {
        background-color: #444444;
        width: 3px;
        height: 3px;
    }
    QTabWidget::pane {
        border: 1px solid #444444;
        background-color: #3c3c3c;
    }
    QTabBar::tab {
        background: #3c3c3c;
        color: #cccccc;
        padding: 8px 15px;
        border: 1px solid #444444;
        border-bottom-left-radius: 4px;
        border-bottom-right-radius: 4px;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background: #2b2b2b;
        color: #f0f0f0;
        border-bottom-color: #2b2b2b;
    }
    QTabBar::tab:hover {
        background: #4a4a4a;
    }
    QLineEdit {
        background-color: #444444;
        color: #f0f0f0;
        border: 1px solid #555555;
        padding: 5px;
        border-radius: 3px;
    }
    QPushButton {
        background-color: #007acc;
        color: #ffffff;
        border: none;
        padding: 8px 15px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #005f99;
    }
    QPushButton:pressed {
        background-color: #004c7a;
    }
    QMessageBox {
        background-color: #3c3c3c;
        color: #f0f0f0;
    }
    QMessageBox QPushButton {
        background-color: #007acc;
        color: #ffffff;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
    }
    
    /* --- QCompleter (Popup) Styling --- */
    /* Target QListView directly as the completer popup is often just a QListView */
    QListView {
        background-color: #3c3c3c; /* Match tree view background or slightly darker */
        color: #cccccc; /* Lighter grey text */
        border: 1px solid #444444;
        selection-background-color: #007acc; /* VS Code blue for selection */
        selection-color: #ffffff;
        outline: 0; /* Remove dotted border on selection */
        font-family: "Consolas", "Courier New", monospace; /* Match editor font */
        font-size: 10pt; /* Match editor font size */
    }
    QListView::item {
        padding: 4px 8px; /* Padding for each item */
    }
    QListView::item:selected {
        background-color: #007acc; /* Match selection */
        color: #ffffff;
    }
    /* --- End QCompleter Styling --- */
    """
    app.setStyleSheet(stylesheet)


def apply_custom_theme2(app: QApplication):
    """
    Applies 'Subtle Light' theme.
    Light background with dark text, muted tones.
    """
    stylesheet = """
    QMainWindow {
        background-color: #f5f5f5; /* Very light grey */
        color: #333333; /* Dark grey text */
    }
    QMenuBar {
        background-color: #e0e0e0; /* Light grey */
        color: #333333;
        border-bottom: 1px solid #cccccc;
    }
    QMenuBar::item {
        background-color: transparent;
        padding: 5px 10px;
    }
    QMenuBar::item:selected {
        background-color: #d0d0d0;
    }
    QMenu {
        background-color: #e0e0e0;
        border: 1px solid #cccccc;
        color: #333333;
    }
    QMenu::item {
        padding: 5px 20px;
    }
    QMenu::item:selected {
        background-color: #d0d0d0;
    }
    QStatusBar {
        background-color: #f5f5f5;
        color: #333333;
        border-top: 1px solid #cccccc;
    }
    QTreeView {
        background-color: #ffffff; /* White background for tree view content */
        color: #333333; /* Dark text for items */
        border: 1px solid #e0e0e0;
        alternate-background-color: #f8f8f8;
        selection-background-color: #e0eaf4; /* Light blue selection */
        selection-color: #111111;
        padding: 5px;
        font-size: 10pt;
    }
    QTreeView::branch:selected {
        background-color: #e0eaf4;
    }
    /* --- QHeaderView (for Name, Size columns) Styling --- */
    QHeaderView::section {
        background-color: #e0e0e0; /* Match tree view background */
        color: #333333; /* Dark text for headers */
        padding: 5px;
        border: 1px solid #cccccc;
        border-right: none;
        border-top: none;
    }
    QHeaderView::section:hover {
        background-color: #d0d0d0;
    }
    QHeaderView::section:pressed {
        background-color: #cccccc;
    }
    /* --- End QHeaderView Styling --- */

    QTextEdit {
        background-color: #ffffff; /* White for editor */
        color: #222222;
        border: 1px solid #e0e0e0;
        selection-background-color: #cceeff; /* Light blue selection */
        selection-color: #000000;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 10pt;
    }
    QSplitter::handle {
        background-color: #e0e0e0;
        width: 3px;
        height: 3px;
    }
    QTabWidget::pane {
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
    }
    QTabBar::tab {
        background: #e0e0e0;
        color: #555555;
        padding: 8px 15px;
        border: 1px solid #e0e0e0;
        border-bottom-left-radius: 4px;
        border-bottom-right-radius: 4px;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background: #ffffff;
        color: #333333;
        border-bottom-color: #ffffff;
    }
    QTabBar::tab:hover {
        background: #d0d0d0;
    }
    QLineEdit {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #cccccc;
        padding: 5px;
        border-radius: 3px;
    }
    QPushButton {
        background-color: #5cb85c;
        color: #ffffff;
        border: none;
        padding: 8px 15px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #4cae4c;
    }
    QPushButton:pressed {
        background-color: #449d44;
    }
    QMessageBox {
        background-color: #ffffff;
        color: #333333;
    }
    QMessageBox QPushButton {
        background-color: #5cb85c;
        color: #ffffff;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
    }
    /* --- QCompleter (Popup) Styling --- */
    QListView {
        background-color: #ffffff; /* White background */
        color: #333333; /* Dark text */
        border: 1px solid #e0e0e0;
        selection-background-color: #cceeff; /* Light blue selection */
        selection-color: #000000;
        outline: 0;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 10pt;
    }
    QListView::item {
        padding: 4px 8px;
    }
    QListView::item:selected {
        background-color: #cceeff;
        color: #000000;
    }
    /* --- End QCompleter Styling --- */
    """
    app.setStyleSheet(stylesheet)

def apply_custom_theme3(app: QApplication):
    """
    Applies 'Blue Midnight' theme.
    Dark blue tones for a professional look.
    """
    stylesheet = """
    QMainWindow {
        background-color: #1e1e2d; /* Deep blue-grey */
        color: #e0e0f0; /* Light blue-white text */
    }
    QMenuBar {
        background-color: #2a2a3e;
        color: #e0e0f0;
        border-bottom: 1px solid #151520;
    }
    QMenuBar::item {
        background-color: transparent;
        padding: 5px 10px;
    }
    QMenuBar::item:selected {
        background-color: #3a3a5e;
    }
    QMenu {
        background-color: #2a2a3e;
        border: 1px solid #151520;
        color: #e0e0f0;
    }
    QMenu::item {
        padding: 5px 20px;
    }
    QMenu::item:selected {
        background-color: #3a3a5e;
    }
    QStatusBar {
        background-color: #1e1e2d;
        color: #e0e0f0;
        border-top: 1px solid #151520;
    }
    QTreeView {
        background-color: #2a2a3e; /* Dark blue-grey for tree view content */
        color: #c0c0d0; /* Lighter blue-grey text for items */
        border: 1px solid #3a3a5e;
        alternate-background-color: #252538;
        selection-background-color: #4a4a7e; /* Medium blue selection */
        selection-color: #ffffff;
        padding: 5px;
        font-size: 10pt;
    }
    QTreeView::branch:selected {
        background-color: #4a4a7e;
    }
    /* --- QHeaderView (for Name, Size columns) Styling --- */
    QHeaderView::section {
        background-color: #2a2a3e; /* Match tree view background */
        color: #e0e0f0; /* Light text for headers */
        padding: 5px;
        border: 1px solid #3a3a5e;
        border-right: none;
        border-top: none;
    }
    QHeaderView::section:hover {
        background-color: #3a3a5e;
    }
    QHeaderView::section:pressed {
        background-color: #4a4a7e;
    }
    /* --- End QHeaderView Styling --- */

    QTextEdit {
        background-color: #1a1a2a; /* Darker blue for editor */
        color: #e0e0f0;
        border: 1px solid #3a3a5e;
        selection-background-color: #0055aa; /* Strong blue selection */
        selection-color: #ffffff;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 10pt;
    }
    QSplitter::handle {
        background-color: #3a3a5e;
        width: 3px;
        height: 3px;
    }
    QTabWidget::pane {
        border: 1px solid #3a3a5e;
        background-color: #2a2a3e;
    }
    QTabBar::tab {
        background: #2a2a3e;
        color: #c0c0d0;
        padding: 8px 15px;
        border: 1px solid #3a3a5e;
        border-bottom-left-radius: 4px;
        border-bottom-right-radius: 4px;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background: #1e1e2d;
        color: #e0e0f0;
        border-bottom-color: #1e1e2d;
    }
    QTabBar::tab:hover {
        background: #3e3e60;
    }
    QLineEdit {
        background-color: #3a3a5e;
        color: #e0e0f0;
        border: 1px solid #4a4a7e;
        padding: 5px;
        border-radius: 3px;
    }
    QPushButton {
        background-color: #4682b4;
        color: #ffffff;
        border: none;
        padding: 8px 15px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #366d9c;
    }
    QPushButton:pressed {
        background-color: #2a5a80;
    }
    QMessageBox {
        background-color: #2a2a3e;
        color: #e0e0f0;
    }
    QMessageBox QPushButton {
        background-color: #4682b4;
        color: #ffffff;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
    }
    /* --- QCompleter (Popup) Styling --- */
    QListView {
        background-color: #2a2a3e; /* Dark blue-grey */
        color: #c0c0d0; /* Lighter blue-grey text */
        border: 1px solid #3a3a5e;
        selection-background-color: #0055aa; /* Strong blue selection */
        selection-color: #ffffff;
        outline: 0;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 10pt;
    }
    QListView::item {
        padding: 4px 8px;
    }
    QListView::item:selected {
        background-color: #0055aa;
        color: #ffffff;
    }
    /* --- End QCompleter Styling --- */
    """
    app.setStyleSheet(stylesheet)

def apply_custom_theme4(app: QApplication):
    """
    Applies 'Forest Green' theme.
    Earthy tones with muted greens and browns.
    """
    stylesheet = """
    QMainWindow {
        background-color: #36453b; /* Dark forest green */
        color: #e0e6db; /* Light off-white */
    }
    QMenuBar {
        background-color: #4a5d4e;
        color: #e0e6db;
        border-bottom: 1px solid #2c3830;
    }
    QMenuBar::item {
        background-color: transparent;
        padding: 5px 10px;
    }
    QMenuBar::item:selected {
        background-color: #5e7362;
    }
    QMenu {
        background-color: #4a5d4e;
        border: 1px solid #2c3830;
        color: #e0e6db;
    }
    QMenu::item {
        padding: 5px 20px;
    }
    QMenu::item:selected {
        background-color: #5e7362;
    }
    QStatusBar {
        background-color: #36453b;
        color: #e0e6db;
        border-top: 1px solid #2c3830;
    }
    QTreeView {
        background-color: #4a5d4e; /* Dark green for tree view content */
        color: #c7d1be; /* Light green-beige text for items */
        border: 1px solid #5e7362;
        alternate-background-color: #405044;
        selection-background-color: #728c69; /* Muted green selection */
        selection-color: #ffffff;
        padding: 5px;
        font-size: 10pt;
    }
    QTreeView::branch:selected {
        background-color: #728c69;
    }
    /* --- QHeaderView (for Name, Size columns) Styling --- */
    QHeaderView::section {
        background-color: #4a5d4e; /* Match tree view background */
        color: #e0e6db; /* Light text for headers */
        padding: 5px;
        border: 1px solid #5e7362;
        border-right: none;
        border-top: none;
    }
    QHeaderView::section:hover {
        background-color: #5e7362;
    }
    QHeaderView::section:pressed {
        background-color: #728c69;
    }
    /* --- End QHeaderView Styling --- */

    QTextEdit {
        background-color: #313f36; /* Darker green for editor */
        color: #e0e6db;
        border: 1px solid #5e7362;
        selection-background-color: #5f854b; /* Deeper green selection */
        selection-color: #ffffff;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 10pt;
    }
    QSplitter::handle {
        background-color: #5e7362;
        width: 3px;
        height: 3px;
    }
    QTabWidget::pane {
        border: 1px solid #5e7362;
        background-color: #4a5d4e;
    }
    QTabBar::tab {
        background: #4a5d4e;
        color: #c7d1be;
        padding: 8px 15px;
        border: 1px solid #5e7362;
        border-bottom-left-radius: 4px;
        border-bottom-right-radius: 4px;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background: #36453b;
        color: #e0e6db;
        border-bottom-color: #36453b;
    }
    QTabBar::tab:hover {
        background: #5d7462;
    }
    /* --- QCompleter (Popup) Styling --- */
    QListView {
        background-color: #4a5d4e; /* Dark green */
        color: #c7d1be; /* Light green-beige text */
        border: 1px solid #5e7362;
        selection-background-color: #5f854b; /* Deeper green selection */
        selection-color: #ffffff;
        outline: 0;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 10pt;
    }
    QListView::item {
        padding: 4px 8px;
    }
    QListView::item:selected {
        background-color: #5f854b;
        color: #ffffff;
    }
    /* --- End QCompleter Styling --- */
    """
    app.setStyleSheet(stylesheet)