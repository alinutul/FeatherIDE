from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PySide6.QtCore import QRegularExpression

class CppSyntaxHighlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)
        self._setup_formats()
        self._setup_rules()
        
    def _setup_formats(self):
        """Initialize all text formats with their styles"""
        self.formats = {
            'keyword': self._create_format("#569cd6", bold=True),
            'type': self._create_format("#4EC9B0"),  # Teal for types
            'preprocessor': self._create_format("#9b703f"),
            'string': self._create_format("#d69d85"),
            'char': self._create_format("#d69d85"),
            'number': self._create_format("#b5cea8"),
            'comment': self._create_format("#6A9955"),
            'function': self._create_format("#DCDCAA"),
            'class': self._create_format("#4EC9B0", bold=True),
        }
        
        # Special format for multi-line comments
        self.multi_line_comment_format = self._create_format("#6A9955")
        
    def _create_format(self, color, bold=False):
        """Helper to create a text format"""
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Bold)
        return fmt
    
    def _setup_rules(self):
        """Initialize all syntax highlighting rules"""
        self.highlighting_rules = []
        
        # Keywords (C++11 through C++20)
        keywords = [
            # Core language keywords
            'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor',
            'bool', 'break', 'case', 'catch', 'char', 'char8_t', 'char16_t', 'char32_t',
            'class', 'concept', 'const', 'consteval', 'constexpr', 'constinit', 'const_cast',
            'continue', 'co_await', 'co_return', 'co_yield', 'decltype', 'default', 'delete',
            'do', 'double', 'dynamic_cast', 'else', 'enum', 'explicit', 'export',
            'extern', 'false', 'float', 'for', 'friend', 'goto', 'if', 'inline',
            'int', 'long', 'mutable', 'namespace', 'new', 'noexcept', 'not', 'not_eq',
            'nullptr', 'operator', 'or', 'or_eq', 'private', 'protected', 'public',
            'reflexpr', 'register', 'reinterpret_cast', 'requires', 'return', 'short',
            'signed', 'sizeof', 'static', 'static_assert', 'static_cast', 'struct',
            'switch', 'template', 'this', 'thread_local', 'throw', 'true', 'try',
            'typedef', 'typeid', 'typename', 'union', 'unsigned', 'using', 'virtual',
            'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq',
            
            # Common macros/aliases
            'NULL', 'override', 'final', 'noexcept'
        ]
        self._add_rule(r'\b(?:' + '|'.join(keywords) + r')\b', 'keyword')
        
        # Standard types
        types = [
            'int8_t', 'int16_t', 'int32_t', 'int64_t',
            'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t',
            'size_t', 'ssize_t', 'ptrdiff_t', 'intptr_t', 'uintptr_t',
            'string', 'wstring', 'u16string', 'u32string',
            'vector', 'map', 'unordered_map', 'set', 'unordered_set',
            'shared_ptr', 'unique_ptr', 'weak_ptr', 'function'
        ]
        self._add_rule(r'\b(?:' + '|'.join(types) + r')\b', 'type')
        
        # Preprocessor directives
        self._add_rule(r'#\s*\w+', 'preprocessor')
        self._add_rule(r'#include\s*<[^>]*>', 'preprocessor')
        self._add_rule(r'#include\s*"[^"]*"', 'preprocessor')
        self._add_rule(r'#(if|elif|else|endif|define|undef|pragma|error|warning)\b', 'preprocessor')
        
        # Strings and characters (with escape sequence support)
        self._add_rule(r'"(?:\\.|[^"\\])*"', 'string')  # Double quotes
        self._add_rule(r"'(?:\\.|[^'\\])'", 'char')     # Single quotes
        
        # Numbers (decimal, hex, binary, octal, floats)
        self._add_rule(r'\b\d+(?:\.\d*)?(?:[eE][+-]?\d+)?[fFlL]?\b', 'number')  # Decimal
        self._add_rule(r'\b0[xX][0-9a-fA-F]+(?:[uU]?[lL]{0,2}|[lL]{0,2}[uU]?)\b', 'number')  # Hex
        self._add_rule(r'\b0[bB][01]+(?:[uU]?[lL]{0,2}|[lL]{0,2}[uU]?)\b', 'number')  # Binary
        self._add_rule(r'\b0[oO]?[0-7]+(?:[uU]?[lL]{0,2}|[lL]{0,2}[uU]?)\b', 'number')  # Octal
        
        # Single-line comments
        self._add_rule(r'//.*$', 'comment')
        
        # Functions (identifier followed by parenthesis)
        self._add_rule(r'\b[a-zA-Z_]\w*(?=\s*\()', 'function')
        
        # Class names (PascalCase convention)
        self._add_rule(r'\b[A-Z][a-zA-Z0-9_]*\b', 'class')
        
        # Setup multi-line comment patterns
        self.comment_start = QRegularExpression(r'/\*')
        self.comment_end = QRegularExpression(r'\*/')
    
    def _add_rule(self, pattern, format_name):
        """Add a highlighting rule"""
        regex = QRegularExpression(pattern)
        self.highlighting_rules.append((regex, self.formats[format_name]))
    
    def highlightBlock(self, text):
        """Apply syntax highlighting to the current text block"""
        # Apply simple rules first
        for pattern, fmt in self.highlighting_rules:
            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
        
        # Handle multi-line comments
        self._highlight_multiline_comments(text)
    
    def _highlight_multiline_comments(self, text):
        """Special handling for multi-line comments"""
        # Initialize block state
        self.setCurrentBlockState(0)
        
        # Check if previous block was in a comment
        prev_state = self.previousBlockState()
        
        # Find the start index
        start_idx = 0
        if prev_state != 1:
            start_match = self.comment_start.match(text)
            start_idx = start_match.capturedStart() if start_match.hasMatch() else -1
        
        # While we have comment starts in this block
        while start_idx >= 0:
            # Look for the end of the comment
            end_match = self.comment_end.match(text, start_idx + 2)
            
            if end_match.hasMatch():
                # Comment ends in this block
                comment_length = end_match.capturedEnd() - start_idx
                self.setCurrentBlockState(0)
            else:
                # Comment continues to next block
                comment_length = len(text) - start_idx
                self.setCurrentBlockState(1)
            
            # Apply the comment format
            self.setFormat(start_idx, comment_length, self.multi_line_comment_format)
            
            # Look for next comment start
            next_match = self.comment_start.match(text, start_idx + comment_length)
            start_idx = next_match.capturedStart() if next_match.hasMatch() else -1