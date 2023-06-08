import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setWindowTitle('Cimple calc')

        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)

        button_grid = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "+"],
            ["0", ".", "C", "-"],
            ["="]
        ]

        for row in button_grid:
            row_layout = QHBoxLayout()
            for item in row:
                button = QPushButton(item)
                if item == "C":
                    button.clicked.connect(self.clear_input_field)
                else:
                    button.clicked.connect(lambda _, text=item: self.button_clicked(text))
                row_layout.addWidget(button)
            self.layout.addLayout(row_layout)

        self.setLayout(self.layout)

    def button_clicked(self, text):
        if text == "=":
            try:
                result = eval(self.input_field.text())
                self.input_field.setText(str(result))
            except:
                self.input_field.setText("Error")
        else:
            self.input_field.setText(self.input_field.text() + text)

    def clear_input_field(self):
        self.input_field.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    calculator = Calculator()
    calculator.show()

    sys.exit(app.exec_())
