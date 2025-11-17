import math
from dataclasses import dataclass
from typing import Dict


@dataclass
class Inventory:
    """
    管理温室库存、折旧和温室成本。
    quantities: 当前库存数量（bunch）
    capacity: 每种原料最大容量
    depreciation_rate: 每月折旧比例
    greenhouse_cost_per_bunch: 每 bunch 的温室费用
    """
    quantities: Dict[str, int]
    capacity: Dict[str, int]
    depreciation_rate: Dict[str, float]
    greenhouse_cost_per_bunch: Dict[str, float]

    def can_consume(self, needs: Dict[str, int], qty: int) -> bool:
        """
        判断库存是否足够制作 qty 束这种花束。
        needs: 制作一束花所需各原料数量
        """
        for material, per_bouquet in needs.items():
            required = per_bouquet * qty
            if self.quantities.get(material, 0) < required:
                return False
        return True

    def consume(self, needs: Dict[str, int], qty: int) -> None:
        """
        从库存中扣减制作 qty 束花所需的原料。
        假定调用前已经用 can_consume 检查过。
        """
        for material, per_bouquet in needs.items():
            required = per_bouquet * qty
            self.quantities[material] -= required
            if self.quantities[material] < 0:
                # 防御性检查
                raise ValueError(f"Inventory for {material} became negative.")

    def month_cost(self) -> float:
        """
        根据当前库存数量计算本月温室成本：
        每 bunch 收 greenhouse_cost_per_bunch。
        """
        total = 0.0
        for material, qty in self.quantities.items():
            unit_cost = self.greenhouse_cost_per_bunch[material]
            total += qty * unit_cost
        return total

    def depreciate(self) -> None:
        """
        应用每月折旧：
        每种原料按比例损耗，向上取整。
        """
        for material, rate in self.depreciation_rate.items():
            current = self.quantities.get(material, 0)
            loss = math.ceil(current * rate)
            self.quantities[material] = max(0, current - loss)

    def restock_to_full(self, unit_price_lookup) -> float:
        """
        把库存补回满仓。
        unit_price_lookup(material: str) -> float
            一个函数，返回该原料的进货单价（Step 1 可以简单写死）。
        返回：总补货成本。
        """
        total_cost = 0.0
        for material, cap in self.capacity.items():
            current = self.quantities.get(material, 0)
            need = cap - current
            if need <= 0:
                continue
            unit_price = unit_price_lookup(material)  # TODO: Step 1 里你可用简单策略
            total_cost += unit_price * need
            self.quantities[material] = cap
        return total_cost
