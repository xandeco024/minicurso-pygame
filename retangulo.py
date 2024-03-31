class Retangulo:
    def __init__(self, alturaRecebida, larguraRecebida):
        self.altura = alturaRecebida
        self.largura = larguraRecebida

    def Apresentar(self):
        print("A altura do retangulo é: ", self.altura)
        print("A largura do retangulo é: ", self.largura)

    def CalcularArea(self):
        area = self.altura * self.largura
        print("A area do retangulo é: ", area)

    def calcularPerimetro(self):
        print("O perimetro do retangulo é: ", 2 * (self.altura + self.largura))

altura = int(input("Digite a altura do retangulo: "))
largura = int(input("Digite a largura do retangulo: "))

retangulo1 = Retangulo(altura, largura)

retangulo1.Apresentar()
retangulo1.CalcularArea()