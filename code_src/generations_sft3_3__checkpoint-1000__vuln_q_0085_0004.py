import re
from typing import Dict, List, Union

def validate_formula(formula: str) -> bool:
    """Validate if the formula contains only allowed characters."""
    allowed_chars = r'^[\d\s\+\-\*\/\(\)\.\,\=]+$'
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
    def precedence(op: str) -> int:
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    def apply_operator(op: str, b: float, a: float) -> float:
        if op == '+':
            return a + b
        if op == '-':
            return a - b
        if op == '*':
            return a * b
        if op == '/':
            return a / b

    def greater_precedence(op1: str, op2: str) -> bool:
        return precedence(op1) > precedence(op2)

    def infix_to_postfix(tokens: List[str]) -> List[str]:
        output_queue = []
        operator_stack = []
        for token in tokens:
            if token.replace('.', '').isdigit():
                output_queue.append(token)
            elif token in '+-*/':
                while (operator_stack and operator_stack[-1] != '(' and
                       greater_precedence(operator_stack[-1], token)):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
        while operator_stack:
            output_queue.append(operator_stack.pop())
        return output_queue

    postfix = infix_to_postfix(tokens)
    stack = []
    for token in postfix:
        if token.replace('.', '').isdigit():
            stack.append(float(token))
        else:
            b, a = stack.pop(), stack.pop()
            stack.append(apply_operator(token, b, a))
    return stack[0]

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