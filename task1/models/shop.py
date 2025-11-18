from typing import Dict, List

from config import (
     BOUQUET_CONFIGS,
     VENDORS,
     STARTING_CASH,
     RENT_PER_MONTH,
     WAGE_PER_HOUR,
     HOURS_PER_FLORIST_PER_MONTH,
     MIN_FLORISTS,
     MAX_FLORISTS,
)
from models.bouquet import Bouquet
from models.florist import Florist
from models.inventory import Inventory
from ioutils.prompts import ask_int, ask_yes_no


class FlowerShop:

    def __init__(self):
        self.cash: float = STARTING_CASH
        self.inventory = Inventory()
        # Convert config BouquetConfig objects into actual Bouquet instances
        self.bouquets: Dict[str, Bouquet] = {
            name: Bouquet(
                name=cfg.name,
                greenery=cfg.greenery,
                roses=cfg.roses,
                daisies=cfg.daisies,
                time_minutes=cfg.time_minutes,
                price=cfg.price,
                demand=cfg.demand,
            )
            for name, cfg in BOUQUET_CONFIGS.items()
        }
        self.florists: List[Florist] = []

    def _florist_names(self) -> List[str]:
        return [f.name for f in self.florists]

    # Hiring and firing

    def hire_florists_interactive(self) -> None:
        current = len(self.florists)
        remaining_slots = MAX_FLORISTS - current
        if remaining_slots <= 0:
            print(f"You already have the maximum number of florists ({MAX_FLORISTS}).")
            return

        min_to_hire = 0
        if current == 0:
            min_to_hire = MIN_FLORISTS
            print(f"You currently have 0 florists, you must hire at least {MIN_FLORISTS}.")

        to_hire = ask_int(
            f" How many florists would you like to hire? (min {min_to_hire}, max {remaining_slots}): ",
            min_val=min_to_hire,
            max_val=remaining_slots,
        )

        bouquet_names = list(self.bouquets.keys())

        for _ in range(to_hire):
            while True:
                name = input("Please input florist name (one at a time): ").strip()
                if not name:
                    print("Error: name cannot be empty.")
                    continue
                if name in self._florist_names():
                    print("Error: a florist with that name already exists.")
                    continue
                break

            speciality = None
            if ask_yes_no("Does this florist have a speciality? (y/n): "):
                print("Choose speciality bouquet type:")
                for i, b_name in enumerate(bouquet_names, start=1):
                    print(f"  {i}. {b_name}")
                idx = ask_int("Enter number: ", min_val=1, max_val=len(bouquet_names))
                speciality = bouquet_names[idx - 1]

            florist = Florist(name=name, speciality=speciality)
            self.florists.append(florist)
            print(f"Hired florist: {florist}")

        print("Current staff: ")
        print(" ", self.florists)

    def fire_florists_interactive(self) -> None:
        current = len(self.florists)
        if current <= MIN_FLORISTS:
            print(f"You must employ at least {MIN_FLORISTS} florist(s).")
            return

        max_can_fire = current - MIN_FLORISTS
        to_fire = ask_int(
            f" How many florists would you like to remove? (0 to {max_can_fire}): ",
            min_val=0,
            max_val=max_can_fire,
        )

        for _ in range(to_fire):
            # Show numbered staff list
            print("Current staff:")
            for idx, f in enumerate(self.florists, start=1):
                print(f"  {idx}. {f}")

            # Choose one to remove
            choice = ask_int(
                "Enter the number of the florist you want to remove: ",
                min_val=1,
                max_val=len(self.florists),
            )
            removed = self.florists.pop(choice - 1)
            print(f"Removed florist: {removed}")


    # Labour & supply calculations

    def _available_labour_minutes(self) -> int:
        return sum(f.monthly_capacity_minutes() for f in self.florists)

    def _supplies_needed_for_plan(self, bouquet_plan: Dict[str, int]) -> Dict[str, int]:
        needed = {"roses": 0, "daisies": 0, "greenery": 0}
        for b_name, qty in bouquet_plan.items():
            bouquet = self.bouquets[b_name]
            s = bouquet.supplies_needed(qty)
            for item, amount in s.items():
                needed[item] += amount
        return needed

    def _revenue_for_plan(self, bouquet_plan: Dict[str, int]) -> float:
        revenue = 0.0
        for b_name, qty in bouquet_plan.items():
            bouquet = self.bouquets[b_name]
            revenue += bouquet.revenue(qty)
        return revenue

    def _required_labour_minutes(self, bouquet_plan: Dict[str, int]) -> int:
        # 1. Base time (no specialities applied yet)
        base_minutes = 0
        for b_name, qty in bouquet_plan.items():
            bouquet = self.bouquets[b_name]
            base_minutes += qty * bouquet.time_minutes

        # 2. Time saved thanks to speciality workers
        total_saving = 0.0
        if self.florists:
            for b_name, qty in bouquet_plan.items():
                if qty <= 0:
                    continue

                specialists = [f for f in self.florists if f.speciality == b_name]
                if not specialists:
                    continue

                bouquet = self.bouquets[b_name]
                t = bouquet.time_minutes

                # Total time capacity for specialists
                total_spec_capacity = sum(f.monthly_capacity_minutes() for f in specialists)

                # Number of bouquets they could make at half-time
                max_discount_bouquets = total_spec_capacity / (t / 2.0)
                discounted_bouquets = min(qty, int(max_discount_bouquets))

                # Each discounted bouquet saves t/2 minutes
                saving = discounted_bouquets * (t / 2.0)
                total_saving += saving

        effective_minutes = int(base_minutes - total_saving)
        if effective_minutes < 0:
            effective_minutes = 0
        return effective_minutes

    def _validate_bouquet_plan(self, bouquet_plan: Dict[str, int]) -> bool:
        # Demand limits
        for b_name, qty in bouquet_plan.items():
            if qty < 0:
                print("Error: bouquet quantities cannot be negative.")
                return False
            demand = self.bouquets[b_name].demand
            if qty > demand:
                print(f"Error: {b_name} exceeds demand ({qty} > {demand}).")
                return False

        # Supply limits
        needed = self._supplies_needed_for_plan(bouquet_plan)
        if not self.inventory.enough_supplies(needed):
            print("Error: Not enough supplies in the greenhouse to make this plan.")
            print("Supplies needed:", needed)
            print("Supplies available:", self.inventory.stock)
            return False

        # Labour limits
        required_minutes = self._required_labour_minutes(bouquet_plan)
        available_minutes = self._available_labour_minutes()
        if required_minutes > available_minutes:
            print("Error: Not enough labour to make this many bouquets.")
            print(f" Required minutes: {required_minutes}, Available: {available_minutes}")
            return False

        return True

    # Vendor info

    def _print_vendor_info(self) -> None:
        print("Supplier price information:")
        for idx, v in VENDORS.items():
            print(
                f"({idx}) {v.name}: "
                f"Roses £{v.roses}/bunch, "
                f"Daisies £{v.daisies}/bunch, "
                f"Greenery £{v.greenery}/bunch"
            )


    def _estimate_restock_cost_for_vendor(self, vendor_idx: int) -> float:
        vendor = VENDORS[vendor_idx]
        total = 0.0
        for item, cap in self.inventory.capacity.items():
            current = self.inventory.stock[item]
            need = cap - current
            if need > 0:
                unit_price = getattr(vendor, item)
                total += need * unit_price
        return total

    # Main monthly simulation

    def run_month(self, month_number: int) -> bool:
        print(f"Month: {month_number}")
        print("Before the month starts, there are some owner actions for you to carry out.")
        print("First, review the number of staff, then decide how many bouquets to sell.")
        print(f"Current number of florists: {len(self.florists)}")

        # Staff management option
        change_staff = ask_yes_no("Do you want to change your florists this month? (y/n): ")

        if change_staff:
            self.hire_florists_interactive()
            self.fire_florists_interactive()
        else:
            print("Skipping staff changes for this month.")

        # Bouquet production planning
        print("How much of each bouquet would you like to sell?")
        bouquet_plan: Dict[str, int] = {}
        bouquet_names = list(self.bouquets.keys())
        # Keep looping until the entire plan is valid
        while True:
            bouquet_plan.clear()
            for b_name in bouquet_names:
                bouquet = self.bouquets[b_name]
                demand = bouquet.demand
                while True:
                    prompt = f"{b_name} (0–{demand}): "
                    qty = ask_int(prompt, min_val=0, max_val=demand)
                    bouquet_plan[b_name] = qty

                    need_this = bouquet.supplies_needed(qty)

                    total_need = self._supplies_needed_for_plan(bouquet_plan)

                    remaining = {
                        item: self.inventory.stock[item] - total_need[item]
                        for item in self.inventory.stock.keys()
                    }

                    print(f"For {b_name} (qty = {qty}):")
                    print("  This bouquet will use:")
                    print(f"    Roses: {need_this['roses']}")
                    print(f"    Daisies: {need_this['daisies']}")
                    print(f"    Greenery: {need_this['greenery']}")
                    print("  After all bouquets chosen so far, greenhouse remaining:")
                    print(f"    Roses: {remaining['roses']}")
                    print(f"    Daisies: {remaining['daisies']}")
                    print(f"    Greenery: {remaining['greenery']}")
                    print()

                    if any(val < 0 for val in remaining.values()):
                        print("Error: this plan exceeds current greenhouse supplies.")
                        print("Please enter a smaller quantity for this bouquet.")

                        continue

                    break

            if self._validate_bouquet_plan(bouquet_plan):
                total_minutes = self._available_labour_minutes()
                required_minutes = self._required_labour_minutes(bouquet_plan)
                remaining_minutes = total_minutes - required_minutes

                print("Labour usage for this month:")
                print(f"  Total available labour: {total_minutes} minutes")
                print(f"  Required by bouquet plan: {required_minutes} minutes")
                print(f"  Remaining (unused) labour: {remaining_minutes} minutes")
                print()
                # --------------------------------
                break
            else:
                print("The chosen quantities violate inventory or labour constraints.")
                print("Please re-enter your bouquet plan.")

        # Beginning-of-month cash
        start_cash = self.cash

        # Revenue + supply deduction
        income = self._revenue_for_plan(bouquet_plan)
        self.cash += income

        supplies_needed = self._supplies_needed_for_plan(bouquet_plan)
        self.inventory.use_supplies(supplies_needed)

        # Wages
        employee_costs = (
            len(self.florists)
            * HOURS_PER_FLORIST_PER_MONTH
            * WAGE_PER_HOUR
        )
        self.cash -= employee_costs

        # Storage
        greenhouse_costs = self.inventory.monthly_storage_cost()
        self.cash -= greenhouse_costs

        # Rent
        rent_cost = RENT_PER_MONTH
        self.cash -= rent_cost

        # Check bankruptcy
        if self.cash < 0:
            print("The shop does not have enough cash to pay expenses.")
            print(f"End of month Cash Balance: £{self.cash:.2f}")
            print("The shop is bankrupt. Simulation ends.")
            return False

        # Depreciation
        self.inventory.apply_depreciation()

        #  Status summary
        print("End of month calculations: ")
        print(f"Cash Balance, Month Start: £{start_cash}")
        print(f" Income: £ {income}")
        print(" Outgoings:")
        print(f" Employee costs: £ {employee_costs}")
        print(f" Greenhouse costs: £ {greenhouse_costs}")
        print(f" Rent: £ {rent_cost}")
        print("Current shop status:")
        print(" Current staff:", self.florists)
        print(" Greenhouse quantity: ")
        print(self.inventory.status_string())

        # Restocked
        print("The greenhouse has spare capacity and needs to be restocked...")

        # 1) Estimate cost under each vendor
        cost_by_vendor = []
        for idx, vendor in VENDORS.items():
            est_cost = self._estimate_restock_cost_for_vendor(idx)
            cost_by_vendor.append(est_cost)
            print(f"  Option {idx}: {vendor.name}  → estimated restock cost £{est_cost:.2f}")

        # 2) Choose vendor
        choice = ask_int(
            f"Choose a vendor for all supplies this month (0–{len(VENDORS) - 1}): ",
            min_val=0,
            max_val=len(VENDORS) - 1,
        )

        chosen_vendor = VENDORS[choice]
        prices = {
            "roses": chosen_vendor.roses,
            "daisies": chosen_vendor.daisies,
            "greenery": chosen_vendor.greenery,
        }

        # 3) Apply restock
        restock_cost = self.inventory.restock_to_full(prices)
        self.cash -= restock_cost

        print(f" + Flower restock costs: £{restock_cost:.2f}")
        print(f" End of month Cash Balance: £{self.cash:.2f}")

        if self.cash < 0:
            print("The shop went bankrupt after restocking. Simulation ends.")
            return False

        print("***********************************************************************")
        return True

