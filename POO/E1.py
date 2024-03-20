class Retangulo:
    def __init__(self):
        self.altura = 10
        self.largura = 20

    def calcularArea(self):
        print("A area do triangulo é: ", self.altura * self.largura)

    def calcularPerimetro(self):
        print("O perimetro do triangulo é: ", 2 * (self.altura + self.largura))

    def apresentar(self):
        print("A altura do retangulo é: ", self.altura)
        print("A largura do retangulo é: ", self.largura)

retangulo1 = Retangulo()

retangulo1.apresentar()
retangulo1.calcularArea()
retangulo1.calcularPerimetro()