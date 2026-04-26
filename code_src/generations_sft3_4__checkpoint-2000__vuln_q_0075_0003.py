import ast
import operator as op

# Supported operators
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg
}

def evaluate_expression(expr):
    # Parse the expression into an AST
    node = ast.parse(expr, mode='eval').body
    
    # Recursively evaluate the AST
    def eval_node(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            left = eval_node(node.left)
            right = eval_node(node.right)
            return operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            operand = eval_node(node.operand)
            return operators[type(node.op)](operand)
        else:
            raise TypeError(node)
    
    return eval_node(node)

# Example usage
try:
    result = evaluate_expression("2 + 3 * 4")
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {str(e)}")