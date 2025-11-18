import math
from typing import Dict

import config


class Inventory:
    def __init__(self):
        # Max capacity for each material (copied from config)
        self.capacity: Dict[str, int] = config.SUPPLY_CAPACITY.copy()
        # Start fully stocked
        self.stock: Dict[str, float] = self.capacity.copy()

    # Supply check & deduction

    def enough_supplies(self, supplies_needed: Dict[str, int]) -> bool:
        for item, amount in supplies_needed.items():
            if amount > self.stock.get(item, 0):
                return False
        return True

    def use_supplies(self, supplies_needed: Dict[str, int]) -> None:
        for item, amount in supplies_needed.items():
            self.stock[item] -= amount

    # Storage cost & depreciation

    def monthly_storage_cost(self) -> float:
        total = 0.0
        for item, qty in self.stock.items():
            cost_per_unit = config.SUPPLY_STORAGE_COST[item]
            total += qty * cost_per_unit
        return total

    def apply_depreciation(self) -> None:
        for item, qty in self.stock.items():
            rate = config.SUPPLY_DEPRECIATION[item]
            lost = math.ceil(qty * rate)
            new_qty = max(qty - lost, 0)
            self.stock[item] = new_qty

    # Restocking

    def restock_to_full(self, prices: Dict[str, float]) -> float:
        total_cost = 0.0
        for item, cap in self.capacity.items():
            current = self.stock[item]
            need = cap - current
            if need > 0:
                unit_price = prices[item]
                total_cost += need * unit_price
                self.stock[item] += need
        return total_cost

    # Helper for display

    def status_string(self) -> str:
        return (
            f" Roses: {self.stock['roses']}\n"
            f" Daisy: {self.stock['daisies']}\n"
            f" Greenery: {self.stock['greenery']}"
        )
