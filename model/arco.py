class Arco:
    def __init__(self, attore1, attore2, peso):
        self.attore1 = attore1
        self.attore2 = attore2
        self.peso = peso

    def __str__(self):
        return f"{self.attore1} - {self.attore2} - {self.peso}"