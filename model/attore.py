from dataclasses import dataclass

@dataclass
class Attore:
    id: str
    name: str
    eta: int

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.name}"