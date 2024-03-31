class Cachorro:
    def __init__(self, nome, raca, idade):
        self.nome = nome
        self.raca = raca
        self.idade = idade

    def Apresentar(self):
        print("auau, meu aunome é :", self.nome)
        print("auau, minha auraca é :", self.raca)
        print("auau, minha auidade é :", self.idade)

    def Latir(self):
        print("auau, latindo intensamente")

cachorro1 = Cachorro("Rex", "Vira-lata", 3)
cachorro1.Apresentar()

