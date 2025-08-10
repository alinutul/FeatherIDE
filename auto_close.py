import sys
from PySide6.QtWidgets import QTextEdit, QApplication, QCompleter
from PySide6.QtGui import QKeyEvent, QTextCursor
from PySide6.QtCore import Qt, QStringListModel, QRect

class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' ')) 

        self.completer = None
        self.setup_completer()

    def setup_completer(self):
        self.cpp_keywords = [
            "alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor",
            "bool", "break", "case", "catch", "char", "char8_t", "char16_t",
            "char32_t", "class", "compl", "const", "consteval", "constexpr",
            "constinit", "const_cast", "continue", "co_await", "co_defines",
            "co_return", "decltype", "default", "delete", "do", "double", "dynamic_cast",
            "else", "enum", "explicit", "export", "extern", "false", "float",
            "for", "friend", "goto", "if", "inline", "int", "long", "mutable",
            "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator",
            "or", "or_eq", "private", "protected", "public", "register",
            "reinterpret_cast", "requires", "return", "short", "signed", "sizeof",
            "static", "static_assert", "static_cast", "struct", "switch", "template",
            "this", "thread_local", "throw", "true", "try", "typedef", "typeid",
            "typename", "union", "unsigned", "using", "virtual", "void", "volatile",
            "wchar_t", "while", "xor", "xor_eq",


            "include", "iostream", "vector", "string", "algorithm", "cmath",
            "using namespace std;", "main", "cout", "cin", "printf", "scanf",
            "std::", "if () {}", "for () {}", "while () {}", "class {}",
            "struct {}", "template <typename T>", "enum class", "nullptr",

            "cin.clear()", "cin.ignore()", "getline(cin, )", "for (int i = 0; i < N; ++i)"
        ]

        self.completer = QCompleter(self)
        model = QStringListModel(self.cpp_keywords)
        self.completer.setModel(model)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)

    def insert_completion(self, completion):
        if self.completer.widget() != self:
            return

        tc = self.textCursor()
        
        # Calculate the start of the word under the cursor
        current_pos = tc.position()
        start_of_word = current_pos
        while start_of_word > 0:
            char_before = self.document().characterAt(start_of_word - 1)
            # Use Python's built-in isalnum() for string checks
            if isinstance(char_before, str) and char_before.isalnum():
                start_of_word -= 1
            else:
                break
        
        tc.setPosition(start_of_word)
        tc.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
        tc.removeSelectedText()
        
        tc.insertText(completion)
        self.setTextCursor(tc)

    def text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def keyPressEvent(self, event: QKeyEvent):
        if self.completer and self.completer.popup().isVisible():
            # Allow Tab, Enter, Return to accept completion
            if event.key() in (Qt.Key_Enter, Qt.Key_Return):
                event.ignore() # Let insert_completion handle it
                return
            # Allow Escape to hide completer
            elif event.key() == Qt.Key_Escape:
                self.completer.popup().hide()
                event.ignore()
                return

        # Auto-closing for brackets and quotes
        cursor = self.textCursor()
        if event.text() == '(':
            self.insertPlainText('()')
            cursor.movePosition(QTextCursor.PreviousCharacter)
            self.setTextCursor(cursor)
            return
        elif event.text() == '[':
            self.insertPlainText('[]')
            cursor.movePosition(QTextCursor.PreviousCharacter)
            self.setTextCursor(cursor)
            return
        elif event.text() == '{':
            self.insertPlainText('{}')
            cursor.movePosition(QTextCursor.PreviousCharacter)
            self.setTextCursor(cursor)
            return

        elif event.text() == '"':
            self.insertPlainText('""')
            cursor.movePosition(QTextCursor.PreviousCharacter)
            self.setTextCursor(cursor)
            return
        elif event.text() == "'":
            self.insertPlainText("''")
            cursor.movePosition(QTextCursor.PreviousCharacter)
            self.setTextCursor(cursor)
            return
        
        # Tab key inserts 4 spaces (override default completer behavior if active)
        elif event.key() == Qt.Key_Tab:
            if self.completer and self.completer.popup().isVisible():
                self.completer.popup().hide() # Hide completer if Tab is pressed and it's visible
            self.insertPlainText("    ") # 4 spaces
            return
        
        super().keyPressEvent(event)

        if event.text().isalnum() or event.key() == Qt.Key_Backspace: # Check for alphanumeric or backspace
            prefix = self.text_under_cursor()
            if self.completer and prefix:
                self.completer.setCompletionPrefix(prefix)
                # If there are completions available for the prefix and popup not visible
                if self.completer.completionModel().rowCount() > 0:
                    if not self.completer.popup().isVisible():
                        self.completer.popup().show()
                    # Position the completer popup
                    cr = self.cursorRect()
                    cr.setWidth(self.completer.popup().sizeHint().width())
                    self.completer.complete(cr) # popup it
                elif self.completer.popup().isVisible():
                    # If no completions or prefix is empty, hide popup
                    self.completer.popup().hide()
            elif self.completer and self.completer.popup().isVisible():
                # If there's no prefix (e.g., deleted character), hide completer
                self.completer.popup().hide()
        elif self.completer and self.completer.popup().isVisible():
            self.completer.popup().hide()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = CustomTextEdit()
    editor.setWindowTitle("Custom C++ Editor with Autocomplete")
    editor.resize(800, 600)
    editor.show()
    sys.exit(app.exec())