import re
from typing import Dict, List, Union

def validate_formula(formula: str) -> bool:
    """Validate if the formula contains only allowed characters."""
    allowed_chars = set('0123456789+-*/().')
    return all(char in allowed_chars for char in formula)

def tokenize_formula(formula: str) -> List[str]:
    """Tokenize the formula into a list of numbers and operators."""
    tokens = []
    current_token = ''
    for char in formula:
        if char in '0123456789+-*/()':
            current_token += char
        else:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            if char != ' ':
                raise ValueError(f"Invalid character in formula: {char}")
    if current_token:
        tokens.append(current_token)
    return tokens

def evaluate_expression(tokens: List[str]) -> float:
    """Evaluate the mathematical expression using operator precedence."""
    def apply_operator(op: str, b: float, a: float) -> float:
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a / b
        else:
            raise ValueError(f"Invalid operator: {op}")

    def greater_precedence(op1: str, op2: str) -> bool:
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        return precedence[op1] > precedence[op2]

    def apply_operator_stack(op: str, b: float, a: float) -> float:
        if op_stack and greater_precedence(op_stack[-1], op):
            op = op_stack.pop()
            b = result_stack.pop()
            a = result_stack.pop()
            result_stack.append(apply_operator(op, b, a))
        else:
            result_stack.append(apply_operator(op, b, a))

    result_stack: List[float] = []
    op_stack: List[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.isdigit():
            result_stack.append(float(token))
        elif token in '+-*/':
            while op_stack and greater_precedence(op_stack[-1], token):
                apply_operator_stack(op_stack.pop(), result_stack.pop(), result_stack.pop())
            op_stack.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                apply_operator_stack(op_stack.pop(), result_stack.pop(), result_stack.pop())
            if op_stack and op_stack[-1] == '(':
                op_stack.pop()
        i += 1

    while op_stack:
        apply_operator_stack(op_stack.pop(), result_stack.pop(), result_stack.pop())

    return result_stack[0]

def main():
    while True:
        try:
            formula = input("Enter a mathematical formula (e.g., '2+3*4'): ")
            if not validate_formula(formula):
                raise ValueError("Invalid characters in formula")
            
            tokens = tokenize_formula(formula)
            result = evaluate_expression(tokens)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            print()

if __name__ == "__main__":
    main()