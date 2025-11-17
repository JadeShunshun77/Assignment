from dataclasses import dataclass


@dataclass
class Florist:
    """
    表示一个花匠。
    Step 1 版本：先不考虑“专长”，只考虑人数和工时。
    """
    name: str

    def monthly_capacity_minutes(self) -> int:
        """返回该花匠每月可工作的总分钟数。"""
        hours = 80
        return hours * 60
