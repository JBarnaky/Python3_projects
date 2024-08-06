import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setWindowTitle('Simple Calc')

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
                result = self.calculate(self.input_field.text())
                self.input_field.setText(str(result))
            except Exception as e:
                self.input_field.setText("Error")
                print(f"Error: {e}")
        else:
            self.input_field.setText(self.input_field.text() + text)

    def clear_input_field(self):
        self.input_field.setText("")

    def calculate(self, expression):
        # This method uses a simple recursive descent parser
        # to evaluate basic arithmetic expressions
        def apply_operator():
            op = operators.pop()
            v2 = values.pop()
            v1 = values.pop()
            if op == "+":
                values.append(v1 + v2)
            elif op == "-":
                values.append(v1 - v2)
            elif op == "*":
                values.append(v1 * v2)
            elif op == "/":
                values.append(v1 / v2)

        values = []
        operators = []
        i = 0
        while i < len(expression):
            if expression[i].isdigit() or expression[i] == ".":
                j = i
                while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                    i += 1
                values.append(float(expression[j:i]))
            elif expression[i] in "+-*/":
                while operators and operators[-1]!= "(" and self.get_precedence(operators[-1]) >= self.get_precedence(expression[i]):
                    apply_operator()
                operators.append(expression[i])
                i += 1
            elif expression[i] == "(":
                operators.append(expression[i])
                i += 1
            elif expression[i] == ")":
                while operators[-1]!= "(":
                    apply_operator()
                operators.pop()
                i += 1
            else:
                i += 1
        while operators:
            apply_operator()
        return values[0]

    def get_precedence(self, op):
        if op == "+" or op == "-":
            return 1
        elif op == "*" or op == "/":
            return 2
        return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)

    calculator = Calculator()
    calculator.show()

    sys.exit(app.exec())
