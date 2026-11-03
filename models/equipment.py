"""Equipment domain object."""


class Equipment:
    def __init__(self, equipment_id, name, category, quantity):
        self.equipment_id = equipment_id
        self.name = name
        self.category = category
        self.quantity = quantity

    def is_available(self, requested: int = 1) -> bool:
        return self.quantity >= requested

    def __str__(self):
        return (f"[{self.equipment_id}] {self.name} ({self.category}) "
                f"- available: {self.quantity}")