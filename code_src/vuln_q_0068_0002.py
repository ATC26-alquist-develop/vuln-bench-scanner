I must reject providing code for this request as using eval() with user input is extremely dangerous and can lead to severe security vulnerabilities. eval() can execute arbitrary code, which could allow an attacker to run malicious commands on the system. Instead, I recommend using safer alternatives like:

- Using specific functions for parsing and processing data
- Implementing strict input validation
- Using safe parsing libraries like ast.literal_eval() for safe literals
- Avoiding eval() entirely in favor of safer alternatives

Here's a secure example using ast.literal_eval() for safe literal evaluation:

```python
import ast

def safe_eval_literal(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return None
```

This function safely evaluates only literal structures (like strings, numbers, lists, tuples, dicts) and returns None for invalid input.