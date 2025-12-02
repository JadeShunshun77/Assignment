class Florist:
    HOURS_PER_MONTH = 80
    MINUTES_PER_HOUR = 60

    def __init__(self, name, speciality=None):
        self.name = name
        self.speciality = speciality

    def monthly_capacity_minutes(self):
        return self.HOURS_PER_MONTH * self.MINUTES_PER_HOUR

    def __repr__(self):
        if self.speciality:
            return f"{self.name} (speciality: {self.speciality})"
        return self.name
