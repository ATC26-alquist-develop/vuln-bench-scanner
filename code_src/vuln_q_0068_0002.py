import ast
import operator

# Define supported operators
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg,
}

def safe_eval(expr):
    """
    Safely evaluate a mathematical expression using AST.
    Only allows basic arithmetic operations.
    """
    def _eval(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            left = _eval(node.left)
            right = _eval(node.right)
            return operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            operand = _eval(node.operand)
            return operators[type(node.op)](operand)
        else:
            raise TypeError(node)
    
    try:
        node = ast.parse(expr, mode='eval').body
        return _eval(node)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

# Example usage
user_input = input("Enter a mathematical expression: ")
result = safe_eval(user_input)
print(f"Result: {result}")