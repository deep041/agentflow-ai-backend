
import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def calculate(expression: str) -> float:
    if len(expression) > 100:
        raise ValueError("Expression too long")

    tree = ast.parse(expression, mode="eval")

    def evaluate(node, depth=0):
        if depth > 12:
            raise ValueError("Expression too complex")

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                value = float(node.value)
                if abs(value) > 1e12:
                    raise ValueError("Number too large")
                return value

        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -evaluate(node.operand, depth + 1)

        if isinstance(node, ast.BinOp):
            operation = OPERATORS.get(type(node.op))

            if operation:
                left = evaluate(node.left, depth + 1)
                right = evaluate(node.right, depth + 1)

                if isinstance(node.op, ast.Div) and right == 0:
                    raise ValueError("Division by zero")

                result = operation(left, right)

                if abs(result) > 1e12:
                    raise ValueError("Result too large")

                return result

        raise ValueError("Unsupported expression")

    return evaluate(tree.body)
