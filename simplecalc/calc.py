import sys
import re
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLineEdit, QPushButton, QListWidget, QSizePolicy)
from PyQt6.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.memory = 0.0
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Enhanced Calculator')
        self.layout = QVBoxLayout()
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.addWidget(self.input_field)
        
        # History list
        self.history_list = QListWidget()
        self.layout.addWidget(self.history_list)
        
        # Button grid
        button_grid = [
            ["MC", "MR", "M+", "M-", "C"],
            ["7", "8", "9", "/", "←"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "+", ")"],
            ["0", ".", "=", "-", "MS"]
        ]

        for row in button_grid:
            row_layout = QHBoxLayout()
            for item in row:
                button = QPushButton(item)
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                
                if item == "C":
                    button.clicked.connect(self.clear_input)
                elif item == "←":
                    button.clicked.connect(self.backspace)
                elif item == "=":
                    button.clicked.connect(self.calculate_result)
                elif item in ["MC", "MR", "M+", "M-", "MS"]:
                    {
                        "MC": lambda: self.memory_operation('clear'),
                        "MR": lambda: self.memory_operation('recall'),
                        "M+": lambda: self.memory_operation('add'),
                        "M-": lambda: self.memory_operation('subtract'),
                        "MS": lambda: self.memory_operation('store')
                    }[item]()
                else:
                    button.clicked.connect(lambda _, text=item: self.append_text(text))
                
                row_layout.addWidget(button)
            self.layout.addLayout(row_layout)
        
        self.setLayout(self.layout)
    
    def append_text(self, text):
        current = self.input_field.text()
        if current == "Error":
            self.clear_input()
        if text == "." and not self.valid_decimal(current):
            return
        self.input_field.setText(current + text)
    
    def valid_decimal(self, current_text):
        parts = re.split(r'([+\-*/()])', current_text)
        current_number = parts[-1] if parts else ""
        return '.' not in current_number
    
    def calculate_result(self):
        expression = self.input_field.text()
        try:
            result = self.evaluate_expression(expression)
            self.input_field.setText(str(result))
            self.history_list.addItem(f"{expression} = {result}")
        except Exception as e:
            self.input_field.setText("Error")
            print(f"Calculation error: {e}")

    def evaluate_expression(self, expression):
        # Handle unary minus by adding 0 before negative numbers
        expression = re.sub(r'([+\-*/\(]|^)\s*-\s*(\d+\.?\d*)', r'\g<1>0-\2', expression)
        return self.shunting_yard(expression)
    
    def shunting_yard(self, expr):
        precedence = {'+':1, '-':1, '*':2, '/':2, '^':3}
        output = []
        operators = []
        i = 0
        
        while i < len(expr):
            if expr[i].isdigit() or expr[i] == '.':
                j = i
                while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                    j += 1
                num = expr[i:j]
                if num.count('.') > 1:
                    raise ValueError("Invalid number format")
                output.append(float(num))
                i = j
            elif expr[i] in precedence or expr[i] in '()':
                if expr[i] == '(':
                    operators.append(expr[i])
                elif expr[i] == ')':
                    while operators[-1] != '(':
                        output.append(operators.pop())
                    operators.pop()
                else:
                    while (operators and operators[-1] != '(' and
                           precedence[operators[-1]] >= precedence[expr[i]]):
                        output.append(operators.pop())
                    operators.append(expr[i])
                i += 1
            else:
                i += 1
        
        while operators:
            output.append(operators.pop())
        
        return self.evaluate_rpn(output)
    
    def evaluate_rpn(self, tokens):
        stack = []
        for token in tokens:
            if isinstance(token, float):
                stack.append(token)
            else:
                b = stack.pop()
                a = stack.pop() if stack else 0
                if token == '+': stack.append(a + b)
                elif token == '-': stack.append(a - b)
                elif token == '*': stack.append(a * b)
                elif token == '/': stack.append(a / b)
                elif token == '^': stack.append(a ** b)
        return stack[0] if stack else 0
    
    def memory_operation(self, operation):
        try:
            current = float(self.input_field.text())
            match operation:
                case 'clear': self.memory = 0.0
                case 'recall': self.input_field.setText(str(self.memory))
                case 'add': self.memory += current
                case 'subtract': self.memory -= current
                case 'store': self.memory = current
        except:
            pass
    
    def backspace(self):
        self.input_field.setText(self.input_field.text()[:-1])
    
    def clear_input(self):
        self.input_field.clear()
    
    def keyPressEvent(self, event):
        key = event.text()
        modifiers = event.modifiers()
        
        if key in '0123456789.+-*/()^':
            self.append_text(key)
        elif event.key() in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
            self.calculate_result()
        elif event.key() == Qt.Key.Key_Backspace:
            self.backspace()
        elif event.key() == Qt.Key.Key_Escape:
            self.clear_input()
        elif modifiers == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_C:
                QApplication.clipboard().setText(self.input_field.text())
            elif event.key() == Qt.Key.Key_V:
                self.input_field.setText(QApplication.clipboard().text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())
