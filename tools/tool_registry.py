
from tools.calculator_tool import CalculatorTool
from tools.summary_tool import SummaryTool
from tools.statistics_tool import StatisticsTool


class ToolRegistry:

    def __init__(self):

        self._tools = {}

        self.register(CalculatorTool())
        self.register(SummaryTool())
        self.register(StatisticsTool())

    # ---------------------------------------

    def register(self, tool):

        self._tools[tool.name] = tool

    # ---------------------------------------

    def get(self, tool_name):

        return self._tools.get(tool_name)

    # ---------------------------------------

    def execute(
        self,
        tool_name,
        *args,
        **kwargs,
    ):

        tool = self.get(tool_name)

        if tool is None:

            raise ValueError(
                f"Tool '{tool_name}' is not registered."
            )

        return tool.execute(
            *args,
            **kwargs,
        )

    # ---------------------------------------

    def list_tools(self):

        return sorted(
            self._tools.keys()
        )