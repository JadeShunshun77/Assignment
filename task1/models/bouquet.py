class Bouquet:
    def __init__(self, name, greenery, roses, daisies, time_minutes, price, demand):
        self.name = name
        self.greenery = greenery
        self.roses = roses
        self.daisies = daisies
        self.time_minutes = time_minutes
        self.price = price
        self.demand = demand

    def supplies_needed(self, quantity):
        return {
            "greenery": self.greenery * quantity,
            "roses": self.roses * quantity,
            "daisies": self.daisies * quantity,
        }

    def revenue(self, quantity):
        return self.price * quantity
