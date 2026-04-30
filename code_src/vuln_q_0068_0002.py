import ast

def safe_eval_literal(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return None