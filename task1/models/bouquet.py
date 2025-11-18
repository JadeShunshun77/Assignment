from dataclasses import dataclass
#

@dataclass
class Bouquet:
    name: str
    greenery: int
    roses: int
    daisies: int
    time_minutes: int
    price: float
    demand: int

    def supplies_needed(self, quantity: int) -> dict:
        return {
            "greenery": self.greenery * quantity,
            "roses": self.roses * quantity,
            "daisies": self.daisies * quantity,
        }

    def revenue(self, quantity: int) -> float:
        return self.price * quantity
