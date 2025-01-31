import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog, QMessageBox,
    QTabWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox
)
from PyQt6.QtGui import (
    QAction, QIcon, QKeySequence, QTextCursor, QPalette, QColor, QTextDocument
)
from PyQt6.QtCore import Qt

class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find and Replace")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Find
        find_layout = QHBoxLayout()
        self.find_label = QLabel("Find:")
        self.find_field = QLineEdit()
        find_layout.addWidget(self.find_label)
        find_layout.addWidget(self.find_field)

        # Replace
        replace_layout = QHBoxLayout()
        self.replace_label = QLabel("Replace:")
        self.replace_field = QLineEdit()
        replace_layout.addWidget(self.replace_label)
        replace_layout.addWidget(self.replace_field)

        # Options
        self.case_check = QCheckBox("Case sensitive")
        self.whole_word_check = QCheckBox("Whole words")

        # Buttons
        button_layout = QHBoxLayout()
        self.find_button = QPushButton("Find Next")
        self.replace_button = QPushButton("Replace")
        self.replace_all_button = QPushButton("Replace All")
        self.close_button = QPushButton("Close")

        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.replace_button)
        button_layout.addWidget(self.replace_all_button)
        button_layout.addWidget(self.close_button)

        layout.addLayout(find_layout)
        layout.addLayout(replace_layout)
        layout.addWidget(self.case_check)
        layout.addWidget(self.whole_word_check)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Connect buttons
        self.find_button.clicked.connect(lambda: self.parent().find_text())
        self.replace_button.clicked.connect(lambda: self.parent().replace_text())
        self.replace_all_button.clicked.connect(lambda: self.parent().replace_all())
        self.close_button.clicked.connect(self.close)

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dark_theme = False
        self.find_dialog = None

    def initUI(self):
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_title)
        self.setCentralWidget(self.tabs)

        # Create menu bar
        self.create_actions()
        self.create_menus()

        # Set window properties
        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)
        self.statusBar().showMessage("Ready")

        # Add initial tab
        self.new_file()

    def create_actions(self):
        # File actions
        self.new_action = QAction("&New", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction("&Open...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction("&Save", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction("Save &As...", self)
        self.save_as_action.triggered.connect(self.save_as_file)

        self.exit_action = QAction("&Exit", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.exit_action.triggered.connect(self.close)

        # Edit actions
        self.undo_action = QAction("&Undo", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.triggered.connect(self.undo)

        self.redo_action = QAction("&Redo", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.triggered.connect(self.redo)

        self.cut_action = QAction("&Cut", self)
        self.cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        self.cut_action.triggered.connect(self.cut)

        self.copy_action = QAction("&Copy", self)
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.copy_action.triggered.connect(self.copy)

        self.paste_action = QAction("&Paste", self)
        self.paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        self.paste_action.triggered.connect(self.paste)

        self.select_all_action = QAction("Select &All", self)
        self.select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        self.select_all_action.triggered.connect(self.select_all)

        self.find_action = QAction("&Find/Replace...", self)
        self.find_action.setShortcut(QKeySequence.StandardKey.Find)
        self.find_action.triggered.connect(self.show_find_replace)

        # View actions
        self.theme_action = QAction("Toggle &Theme", self)
        self.theme_action.triggered.connect(self.toggle_theme)

    def create_menus(self):
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Edit menu
        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.select_all_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.find_action)

        # View menu
        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction(self.theme_action)

    def get_current_editor(self):
        return self.tabs.currentWidget()

    def new_file(self):
        text_edit = QTextEdit()
        text_edit.textChanged.connect(self.update_title)
        self.tabs.addTab(text_edit, "Untitled")
        self.tabs.setCurrentIndex(self.tabs.count()-1)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File")
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                text_edit = QTextEdit()
                text_edit.setText(content)
                text_edit.textChanged.connect(self.update_title)
                self.tabs.addTab(text_edit, filename.split('/')[-1])
                self.tabs.setCurrentIndex(self.tabs.count()-1)
                self.tabs.setTabToolTip(self.tabs.currentIndex(), filename)
                self.statusBar().showMessage(f"Opened {filename}", 3000)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to open file:\n{str(e)}")

    def save_file(self):
        current_editor = self.get_current_editor()
        filename = self.tabs.tabToolTip(self.tabs.currentIndex())
        if filename:
            try:
                with open(filename, 'w') as f:
                    # Fix variable name from current_edit to current_editor
                    f.write(current_editor.toPlainText())
                self.statusBar().showMessage(f"Saved {filename}", 3000)
                self.tabs.setTabText(self.tabs.currentIndex(), filename.split('/')[-1])
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save file:\n{str(e)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        current_editor = self.get_current_editor()
        filename, _ = QFileDialog.getSaveFileName(self, "Save As")
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(current_editor.toPlainText())
                self.tabs.setTabText(self.tabs.currentIndex(), filename.split('/')[-1])
                self.tabs.setTabToolTip(self.tabs.currentIndex(), filename)
                self.statusBar().showMessage(f"Saved as {filename}", 3000)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save file:\n{str(e)}")

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def update_title(self):
        filename = self.tabs.tabToolTip(self.tabs.currentIndex())
        if filename:
            self.setWindowTitle(f"Text Editor - {filename}")
        else:
            self.setWindowTitle("Text Editor - Untitled")

    def undo(self):
        current_editor = self.get_current_editor()
        if current_editor:
            current_editor.undo()

    def redo(self):
        current_editor = self.get_current_editor()
        if current_editor:
            current_editor.redo()

    def cut(self):
        current_editor = self.get_current_editor()
        if current_editor:
            current_editor.cut()

    def copy(self):
        current_editor = self.get_current_editor()
        if current_editor:
            current_editor.copy()

    def paste(self):
        current_editor = self.get_current_editor()
        if current_editor:
            current_editor.paste()

    def select_all(self):
        current_editor = self.get_current_editor()
        if current_editor:
            current_editor.selectAll()

    def show_find_replace(self):
        if not self.find_dialog:
            self.find_dialog = FindReplaceDialog(self)
        self.find_dialog.show()

    def find_text(self):
        current_editor = self.get_current_editor()
        if not current_editor:
            return

        flags = QTextDocument.FindFlag(0)
        if self.find_dialog.case_check.isChecked():
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if self.find_dialog.whole_word_check.isChecked():
            flags |= QTextDocument.FindFlag.FindWholeWords

        text = self.find_dialog.find_field.text()
        if text:
            found = current_editor.find(text, flags)
            if not found:
                QMessageBox.information(self, "Not Found", "Text not found.")
        else:
            QMessageBox.warning(self, "Warning", "Please enter text to find.")

    def replace_text(self):
        current_editor = self.get_current_editor()
        if not current_editor:
            return

        cursor = current_editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.find_dialog.replace_field.text())
        self.find_text()

    def replace_all(self):
        current_editor = self.get_current_editor()
        if not current_editor:
            return

        text = current_editor.toPlainText()
        find_text = self.find_dialog.find_field.text()
        replace_text = self.find_dialog.replace_field.text()

        flags = 0
        if self.find_dialog.case_check.isChecked():
            flags |= QTextCursor.FindFlag.FindCaseSensitively
        if self.find_dialog.whole_word_check.isChecked():
            flags |= QTextCursor.FindFlag.FindWholeWords

        new_text = text.replace(find_text, replace_text, flags)
        current_editor.setPlainText(new_text)

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        if self.dark_theme:
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197).lighter())
            dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            QApplication.instance().setPalette(dark_palette)
        else:
            QApplication.instance().setPalette(QApplication.style().standardPalette())

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()