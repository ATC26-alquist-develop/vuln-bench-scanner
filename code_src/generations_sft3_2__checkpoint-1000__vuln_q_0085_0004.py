import re
from typing import Dict, List, Union

def validate_formula(formula: str) -> bool:
    """Validate if the formula contains only allowed characters."""
    allowed_chars = r'^[\d\s\+\-\*\/\(\)\.\,\=]+$'
    return bool(re.match(allowed_chars, formula))

def tokenize_formula(formula: str) -> List[str]:
    """Tokenize the formula into a list of tokens."""
    return re.findall(r'\d+|\+|\-|\*|\/|\(|\)|\.|\=|\s', formula)

def evaluate_expression(tokens: List[str]) -> Union[float, str]:
    """Evaluate the mathematical expression using Shunting Yard algorithm."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output_queue = []
    operator_stack = []
    
    for token in tokens:
        if token.replace('.', '').isdigit():
            output_queue.append(float(token))
        elif token in precedence:
            while (operator_stack and operator_stack[-1] != '(' and
                   precedence.get(operator_stack[-1], 0) >= precedence[token]):
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
    
    def apply_operator(op: str, b: float, a: float) -> float:
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a / b
    
    result = output_queue[0]
    for token in output_queue[1:]:
        if isinstance(token, float):
            result = apply_operator(token, result, 0)
        else:
            result = apply_operator(token, result, result)
    
    return result

def main():
    print("Enter formulas one by one. Type 'quit' to exit.")
    while True:
        formula = input("Enter formula: ").strip()
        
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