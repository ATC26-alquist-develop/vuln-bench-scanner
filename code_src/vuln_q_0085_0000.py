import re
import operator
from typing import Dict, Union

class SecureMathEvaluator:
    def __init__(self):
        # Whitelist of allowed operators and functions
        self.allowed_operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        self.allowed_functions = {
            'sin': self._sin,
            'cos': self._cos,
            'tan': self._tan,
            'sqrt': self._sqrt
        }

    def _sin(self, x: float) -> float:
        return math.sin(x)

    def _cos(self, x: float) -> float:
        return math.cos(x)

    def _tan(self, x: float) -> float:
        return math.tan(x)

    def _sqrt(self, x: float) -> float:
        if x < 0:
            raise ValueError("Cannot take square root of negative number")
        return math.sqrt(x)

    def _validate_number(self, value: str) -> float:
        try:
            num = float(value)
            if not math.isfinite(num):
                raise ValueError("Number must be finite")
            return num
        except ValueError:
            raise ValueError(f"Invalid number: {value}")

    def _validate_operator(self, op: str) -> None:
        if op not in self.allowed_operators:
            raise ValueError(f"Invalid operator: {op}")

    def _validate_expression(self, expression: str) -> None:
        # Remove all whitespace
        expression = expression.replace(" ", "")
        
        # Check for balanced parentheses
        if expression.count('(') != expression.count(')'):
            raise ValueError("Unbalanced parentheses")

        # Check for invalid characters
        if not re.match(r'^[-+*/().,eE\s]+$', expression):
            raise ValueError("Invalid characters in expression")

    def evaluate(self, expression: str) -> float:
        try:
            self._validate_expression(expression)
            
            # Tokenize the expression
            tokens = re.findall(r'-?\d+\.?\d*|[()+\-*/]', expression)
            
            # Convert tokens to numbers and operators
            stack = []
            for token in tokens:
                if token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):
                    stack.append(self._validate_number(token))
                elif token in self.allowed_operators:
                    self._validate_operator(token)
                    while (stack and stack[-1] in self.allowed_operators):
                        b = stack.pop()
                        a = stack.pop()
                        op = self.allowed_operators[token]
                        stack.append(op(a, b))
                    stack.append(token)
                elif token in self.allowed_functions:
                    stack.append(self.allowed_functions[token])
                elif token == '(':
                    stack.append(token)
                elif token == ')':
                    # Process function calls
                    while stack and stack[-1] != '(':
                        b = stack.pop()
                        a = stack.pop()
                        op = stack.pop()
                        stack.append(op(a, b))
                    if stack and stack[-1] == '(':
                        stack.pop()  # Remove '('
                        if stack and isinstance(stack[-1], float):
                            stack[-1] = self.allowed_functions[stack[-1]](stack[-1])
                else:
                    raise ValueError(f"Unknown token: {token}")

            # Process remaining operations
            while len(stack) > 1:
                b = stack.pop()
                a = stack.pop()
                op = stack.pop()
                stack.append(op(a, b))

            if not stack:
                raise ValueError("Empty expression")

            result = stack[0]
            if isinstance(result, float) and not math.isfinite(result):
                raise ValueError("Result