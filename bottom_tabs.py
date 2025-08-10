from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTextEdit, QLineEdit, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt


class BottomTabsWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # === Build Output Tab ===
        self.build_output = QTextEdit()
        self.build_output.setReadOnly(True)
        self.build_output.setPlaceholderText("Build messages will appear here...")
        self.addTab(self.build_output, "Build Output")

        # === AI Chat Tab ===
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("AI chat history will appear here...")

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your message to the AI...")
        self.send_chat_button = QPushButton("Send")

        chat_input_layout = QHBoxLayout()
        chat_input_layout.addWidget(self.chat_input)
        chat_input_layout.addWidget(self.send_chat_button)

        self.chat_layout.addWidget(self.chat_display)
        self.chat_layout.addLayout(chat_input_layout)

        self.addTab(self.chat_widget, "AI Chat")

        # === Notes Tab (Temporary) ===
        self.notes_widget = QWidget()
        self.notes_layout = QVBoxLayout(self.notes_widget)

        self.notes_text_edit = QTextEdit()
        self.notes_text_edit.setPlaceholderText("Write your notes here...")

        self.notes_layout.addWidget(self.notes_text_edit)
        self.notes_widget.setLayout(self.notes_layout)

        self.addTab(self.notes_widget, "Notes")
