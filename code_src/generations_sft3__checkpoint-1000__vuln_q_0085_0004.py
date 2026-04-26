import re
from typing import Dict, List, Union

def validate_formula(formula: str) -> bool:
    """Validate if the formula contains only allowed characters."""
    allowed_chars = r'^[\d\s\+\-\*\/\(\)\.\,]+$'
    return bool(re.match(allowed_chars, formula))

def tokenize_formula(formula: str) -> List[str]:
    """Tokenize the formula into a list of numbers and operators."""
    tokens = []
    current_token = ''
    for char in formula:
        if char in '0123456789':
            current_token += char
        else:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)
    if current_token:
        tokens.append(current_token)
    return tokens

def evaluate_expression(tokens: List[str]) -> float:
    """Evaluate the mathematical expression represented by tokens."""
    def apply_operator(operators: List[str], values: List[float]) -> float:
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '/':
            values.append(left / right)
        return values[-1]

    def greater_precedence(op1: str, op2: str) -> bool:
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        return precedence[op1] > precedence[op2]

    values: List[float] = []
    operators: List[str] = []

    for token in tokens:
        if token.replace('.', '').isdigit():
            values.append(float(token))
        elif token in '+-*/':
            while (operators and operators[-1] != '(' and
                   greater_precedence(operators[-1], token)):
                values = apply_operator(operators, values)
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                values = apply_operator(operators, values)
            operators.pop()  # Remove '('

    while operators:
        values = apply_operator(operators, values)

    return values[0]

def main():
    while True:
        formula = input("Enter a mathematical formula (or 'quit' to exit): ")
        if formula.lower() == 'quit':
            break

        if not validate_formula(formula):
            print("Invalid formula. Please use only numbers, operators, and spaces.")
            continue

        tokens = tokenize_formula(formula)
        result = evaluate_expression(tokens)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()