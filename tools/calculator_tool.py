

from __future__ import annotations

import math


class CalculatorTool:
    """Safe calculator utility."""

    name = "calculator"

    _ALLOWED_NAMES = {
        "abs": abs,
        "round": round,
        "pow": pow,
        "min": min,
        "max": max,
        "sum": sum,

        "sqrt": math.sqrt,
        "ceil": math.ceil,
        "floor": math.floor,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "factorial": math.factorial,

        "pi": math.pi,
        "e": math.e,
    }

    def execute(self, expression: str):
        """
        Evaluate a mathematical expression safely.

        Example:
            25 * 4
            sqrt(144)
            sin(pi / 2)
            factorial(5)
        """

        expression = expression.strip()

        if not expression:
            return "Empty expression."

        try:
            result = eval(
                expression,
                {"__builtins__": {}},
                self._ALLOWED_NAMES,
            )

            return result

        except Exception as exc:
            return f"Calculation Error: {exc}"