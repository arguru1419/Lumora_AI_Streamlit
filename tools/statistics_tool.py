
from __future__ import annotations

import statistics


class StatisticsTool:

    name = "statistics"

    def execute(self, values):

        if not values:

            return {
                "count": 0,
                "mean": 0,
                "median": 0,
                "minimum": 0,
                "maximum": 0,
                "stdev": 0,
            }

        return {

            "count": len(values),

            "mean": statistics.mean(values),

            "median": statistics.median(values),

            "minimum": min(values),

            "maximum": max(values),

            "stdev": (
                statistics.stdev(values)
                if len(values) > 1
                else 0
            ),
        }