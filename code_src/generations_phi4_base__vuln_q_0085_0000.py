def evaluate_expression(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return str(e)

expression = input("Enter a mathematical expression: ")
result = evaluate_expression(expression)
print("Result:", result)