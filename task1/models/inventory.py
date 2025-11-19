import math
import config


class Inventory:
    def __init__(self):
        self.capacity = config.SUPPLY_CAPACITY.copy()#max amount they could hold

        self.stock = self.capacity.copy()#start with full

    def enough_supplies(self, supplies_needed):
        for item, amount in supplies_needed.items():
            if amount > self.stock.get(item, 0):
                return False
        return True

    def use_supplies(self, supplies_needed):
        for item, amount in supplies_needed.items():
            self.stock[item] -= amount

    def monthly_storage_cost(self):#Monthly storage cost
        total = 0
        for item, qty in self.stock.items():
            cost = config.SUPPLY_STORAGE_COST[item]
            total += qty * cost
        return total

    def apply_depreciation(self):#Monthly Depreciation
        for item, qty in self.stock.items():
            rate = config.SUPPLY_DEPRECIATION[item]
            lost = math.ceil(qty * rate)
            new_amount = qty - lost
            if new_amount < 0:
                new_amount = 0
            self.stock[item] = new_amount

    def restock_to_full(self, prices):#Restock
        total_cost = 0
        for item, cap in self.capacity.items():
            current = self.stock[item]
            need = cap - current
            if need > 0:
                total_cost += need * prices[item]
                self.stock[item] += need
        return total_cost

    def status_string(self):
        return (
            f" Roses: {self.stock['roses']}\n"
            f" Daisy: {self.stock['daisies']}\n"
            f" Greenery: {self.stock['greenery']}"
        )

