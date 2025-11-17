from dataclasses import dataclass, field
from typing import List, Dict

from .florist import Florist
from .bouquet import Bouquet
from .inventory import Inventory


@dataclass
class FlowerShop:
    """
    管理花店整体状态：现金、库存、花匠、固定成本等。
    """
    cash: float
    inventory: Inventory
    florists: List[Florist] = field(default_factory=list)
    rent_per_month: float = 0.0
    wage_per_hour: float = 0.0

    def add_florist(self, name: str, max_florists: int) -> None:
        """雇佣一名新花匠。Step 1 不考虑专长。"""
        if len(self.florists) >= max_florists:
            raise ValueError("Cannot hire more florists: reached maximum.")
        if any(f.name == name for f in self.florists):
            raise ValueError("A florist with this name already exists.")
        self.florists.append(Florist(name=name))

    def remove_florist(self, name: str, min_florists: int) -> None:
        """
        解雇一名花匠。
        Step 1：你可以先不在 main.py 里调用这个方法，
        只在扩展时实现“解雇逻辑”。
        """
        if len(self.florists) <= min_florists:
            raise ValueError("Cannot go below minimum number of florists.")
        self.florists = [f for f in self.florists if f.name != name]

    def total_labor_minutes(self) -> int:
        """
        计算当前所有花匠每月总工时（分钟）。
        Step 1 版本：不区分花束类型，只给你一个总劳动力上限。
        更精细的“不同花束占用不同时间”你可以在扩展时自己加。
        """
        return sum(f.monthly_capacity_minutes() for f in self.florists)

    def max_producible_by_inventory(self, bouquet: Bouquet) -> int:
        """
        仅根据库存，最多能做多少束该花束。
        （不考虑工时与需求）
        """
        max_qty = float("inf")
        for material, per_bouquet in bouquet.ingredients.items():
            if per_bouquet == 0:
                continue
            available = self.inventory.quantities.get(material, 0)
            max_qty = min(max_qty, available // per_bouquet)
        return 0 if max_qty == float("inf") else int(max_qty)

    def sell(self, bouquet: Bouquet, qty: int) -> float:
        """
        销售 bouquet 的 qty 束：
        - 检查库存
        - 扣减库存
        - 增加现金
        返回收入金额
        """
        if not self.inventory.can_consume(bouquet.ingredients, qty):
            raise ValueError("Not enough inventory to make requested bouquets.")
        self.inventory.consume(bouquet.ingredients, qty)
        revenue = bouquet.price * qty
        self.cash += revenue
        return revenue

    def pay_wages(self, hours_per_florist: int) -> float:
        """支付所有花匠工资，并从现金中扣除。"""
        total_hours = len(self.florists) * hours_per_florist
        total_cost = total_hours * self.wage_per_hour
        self.cash -= total_cost
        return total_cost

    def pay_rent(self) -> float:
        """支付房租。"""
        self.cash -= self.rent_per_month
        return self.rent_per_month

    def pay_greenhouse_costs(self) -> float:
        """支付温室成本（基于当前库存）。"""
        cost = self.inventory.month_cost()
        self.cash -= cost
        return cost

    def apply_depreciation(self) -> None:
        """应用库存折旧。"""
        self.inventory.depreciate()

    def is_bankrupt(self) -> bool:
        """判断是否破产（现金<0）。"""
        return self.cash < 0
