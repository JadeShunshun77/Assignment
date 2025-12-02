from typing import Dict

# Bouquets

class BouquetConfig:
    def __init__(
        self,
        name: str,
        greenery: int,
        roses: int,
        daisies: int,
        time_minutes: int,
        price: float,
        demand: int,
    ):
        self.name = name
        self.greenery = greenery
        self.roses = roses
        self.daisies = daisies
        self.time_minutes = time_minutes
        self.price = price
        self.demand = demand


BOUQUET_CONFIGS: Dict[str, BouquetConfig] = {
    "Fern-tastic": BouquetConfig(
        name="Fern-tastic",
        greenery=4,
        roses=0,
        daisies=2,
        time_minutes=20,
        price=18.50,
        demand=175,
    ),
    "Be-Leaf in Yourself": BouquetConfig(
        name="Be-Leaf in Yourself",
        greenery=2,
        roses=1,
        daisies=3,
        time_minutes=30,
        price=17.75,
        demand=100,
    ),
    "You Rose to the Occasion": BouquetConfig(
        name="You Rose to the Occasion",
        greenery=2,
        roses=4,
        daisies=2,
        time_minutes=45,
        price=32.50,
        demand=250,
    ),
}


#Greenhouses

SUPPLY_CAPACITY = {
    "roses": 200,
    "daisies": 250,
    "greenery": 400,
}

SUPPLY_DEPRECIATION = {
    "roses": 0.40,
    "daisies": 0.15,
    "greenery": 0.05,
}

SUPPLY_STORAGE_COST = {
    "roses": 1.50,
    "daisies": 0.80,
    "greenery": 0.20,
}


# Vendors

class VendorConfig:
    def __init__(self, name: str, roses: float, daisies: float, greenery: float):
        self.name = name
        self.roses = roses
        self.daisies = daisies
        self.greenery = greenery


VENDORS = {
    0: VendorConfig(
        name="Evergreen Essentials",
        roses=2.80,
        daisies=1.50,
        greenery=0.95,
    ),
    1: VendorConfig(
        name="FloraGrow Distributors",
        roses=1.60,
        daisies=1.20,
        greenery=1.80,
    ),
}


# Financial / Florists configuration

STARTING_CASH = 7500.0
RENT_PER_MONTH = 800.0
WAGE_PER_HOUR = 15.50
HOURS_PER_FLORIST_PER_MONTH = 80

MIN_FLORISTS = 1
MAX_FLORISTS = 4
