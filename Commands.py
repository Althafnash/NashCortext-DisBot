import re
import math

def calculate_expression(user_message):
    expression = re.findall(r"[-+*/().\d\s]+", user_message)
    if not expression:
        return "I couldn't find a valid expression to calculate."

    try:
        result = eval(expression[0], {"__builtins__": None}, {
            "sqrt": math.sqrt,
            "pow": pow
        })
        return f" The result is: {result}"
    except Exception as e:
        return f" Error in calculation: {str(e)}"

def handle_math_commands(message):
    parts = message.strip().lower().split()
    if len(parts) != 3:
        return None

    try:
        a = float(parts[1])
        b = float(parts[2])

        if parts[0] == "/add":
            return f"Result: {a + b}"
        elif parts[0] == "/sub":
            return f"Result: {a - b}"
        elif parts[0] == "/mu":
            return f"Result: {a * b}"
        elif parts[0] == "/div":
            if b == 0:
                return "Cannot divide by zero."
            return f"Result: {a / b}"
    except ValueError:
        return "Invalid number format."

    return None
