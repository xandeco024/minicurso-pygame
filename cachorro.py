class Cachorro:
    def __init__(self, nome, raca, pelagem, porte):
        self.nome = nome
        self.raca = raca
        self.pelagem = pelagem
        self.porte = porte

    def Apresentar(self):
        print("auau, meu nome é :", self.nome)
        print("auau, minha raça é :", self.raca)
        print("auau, minha pelagem é :", self.pelagem)
        print("auau, meu porte é :", self.porte)
    
    def Latir(self):
        print("auau,", self.nome, " está latindo intensamente")

    def Morder(self, cachorroAlvo):
        print("auau,", self.nome, " mordeu ", cachorroAlvo.nome)

cachorro1 = Cachorro("Roberto", "Vira-lata", "curta", "médio")
cachorro2 = Cachorro("Rex", "Pastor Alemão", "longa", "grande")


cachorro1.Latir()
cachorro2.Morder(cachorro1)
cachorro1.Morder(cachorro2)