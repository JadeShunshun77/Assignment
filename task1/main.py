"""
main.py
运行文字版花店模拟（Step 1 最小版本）：
- 只考虑雇佣花匠（不解雇）
- 按库存和需求限制销售数量（暂不考虑工时）
- 支付工资、温室费用、租金
- 折旧、补货到满仓（使用简单固定进货价格）
"""

from models.inventory import Inventory
from models.shop import FlowerShop
from models.bouquet import Bouquet
from ioutils.prompts import ask_positive_int
import config as C


def build_bouquets() -> dict[str, Bouquet]:
    """根据 config 构造三种 Bouquet 对象。"""
    return {
        "fern_tastic": Bouquet(
            code="fern_tastic",
            greenery=C.RECIPES["fern_tastic"]["greenery"],
            roses=C.RECIPES["fern_tastic"]["roses"],
            daisies=C.RECIPES["fern_tastic"]["daisies"],
            minutes=C.RECIPES["fern_tastic"]["minutes"],
            price=C.PRICE["fern_tastic"],
        ),
        "be_leaf": Bouquet(
            code="be_leaf",
            greenery=C.RECIPES["be_leaf"]["greenery"],
            roses=C.RECIPES["be_leaf"]["roses"],
            daisies=C.RECIPES["be_leaf"]["daisies"],
            minutes=C.RECIPES["be_leaf"]["minutes"],
            price=C.PRICE["be_leaf"],
        ),
        "you_rose": Bouquet(
            code="you_rose",
            greenery=C.RECIPES["you_rose"]["greenery"],
            roses=C.RECIPES["you_rose"]["roses"],
            daisies=C.RECIPES["you_rose"]["daisies"],
            minutes=C.RECIPES["you_rose"]["minutes"],
            price=C.PRICE["you_rose"],
        ),
    }


def simple_unit_price(material: str) -> float:
    """
    Step 1 的简单进货价格函数：
    为了先打通流程，这里你可以：
    - 暂时写死一套价格（例如全用 Evergreen Essentials）
    后面再改成用户交互选择供应商。
    """
    evergreen_prices = {
        "roses": 2.80,
        "daisies": 1.50,
        "greenery": 0.95,
    }
    return evergreen_prices[material]


def main() -> None:
    # 1. 询问模拟月份数
    months = ask_positive_int("How many months to run the simulation? ", allow_zero=False)

    # 2. 初始库存：满仓
    inventory = Inventory(
        quantities=dict(C.GREENHOUSE_CAPACITY),  # 拷贝一份
        capacity=C.GREENHOUSE_CAPACITY,
        depreciation_rate=C.DEPRECIATION,
        greenhouse_cost_per_bunch=C.GREENHOUSE_COST_PER_BUNCH,
    )

    # 3. 创建花店对象
    shop = FlowerShop(
        cash=C.STARTING_CASH,
        inventory=inventory,
        rent_per_month=C.RENT_PER_MONTH,
        wage_per_hour=C.WAGE_PER_HOUR,
    )

    bouquets = build_bouquets()

    # 4. 确保至少一名花匠
    print("You must hire at least one florist to start.")
    while len(shop.florists) < C.MIN_FLORISTS:
        name = input("Enter florist name: ").strip()
        try:
            shop.add_florist(name=name, max_florists=C.MAX_FLORISTS)
        except ValueError as e:
            print("Error:", e)

    # 5. 月度循环
    for month in range(1, months + 1):
        print("\n" + "=" * 50)
        print(f"Month {month}")
        print("=" * 50)
        print(f"Cash at start of month: £{shop.cash:.2f}")
        print("Current florists:", [f.name for f in shop.florists])
        print("Current inventory:", shop.inventory.quantities)

        # （可选）Step 1 先不实现“增减花匠”，之后你可以自己加

        # 6. 决定每种花束的销售数量
        total_revenue = 0.0
        for code, bouquet in bouquets.items():
            demand = C.DEMAND_PER_MONTH[code]
            max_by_inv = shop.max_producible_by_inventory(bouquet)
            max_allowed = min(demand, max_by_inv)
            print(f"\nBouquet: {code}")
            print(f"Demand: {demand}, Max producible by inventory: {max_by_inv}")
            if max_allowed <= 0:
                print("You cannot produce any of this bouquet this month.")
                continue

            qty = ask_positive_int(
                f"How many '{code}' bouquets would you like to sell? (0–{max_allowed}) ",
                allow_zero=True,
            )
            if qty > max_allowed:
                print("That exceeds demand or inventory. Capping to max.")
                qty = max_allowed

            if qty > 0:
                try:
                    revenue = shop.sell(bouquet, qty)
                    total_revenue += revenue
                    print(f"Sold {qty} x {code}, revenue: £{revenue:.2f}")
                except ValueError as e:
                    print("Error during selling:", e)

        print(f"\nTotal revenue this month: £{total_revenue:.2f}")

        # 7. 支付工资、温室费用、租金
        wage_cost = shop.pay_wages(C.HOURS_PER_FLORIST)
        greenhouse_cost = shop.pay_greenhouse_costs()
        rent_cost = shop.pay_rent()
        print(f"Wage cost: £{wage_cost:.2f}")
        print(f"Greenhouse cost: £{greenhouse_cost:.2f}")
        print(f"Rent: £{rent_cost:.2f}")

        # 8. 折旧
        shop.apply_depreciation()
        print("Inventory after depreciation:", shop.inventory.quantities)

        # 9. 检查是否破产
        if shop.is_bankrupt():
            print(f"\nBankrupt at end of month {month}! Final cash: £{shop.cash:.2f}")
            break

        # 10. 补货到满仓
        restock_cost = shop.inventory.restock_to_full(simple_unit_price)
        shop.cash -= restock_cost
        print(f"Restock cost: £{restock_cost:.2f}")
        print("Inventory after restock:", shop.inventory.quantities)
        print(f"Cash at end of month {month}: £{shop.cash:.2f}")

    print("\nSimulation ended.")
    print(f"Final cash balance: £{shop.cash:.2f}")


if __name__ == "__main__":
    main()
