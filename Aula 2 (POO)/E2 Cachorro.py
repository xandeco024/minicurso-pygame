#Exercicio de classes e objetos, que recebem agrumentos (nome, raça, pelagem, porte) (metodo morder)

class Cachorro: #Criação da classe cachorro
    def __init__(self, nome, raca, pelagem, porte): #ao criar um objeto com a classe cachorro, ele PRECISA receber nome, raça, pelagem e porte
        self.nome = nome
        self.raca = raca
        self.pelagem = pelagem
        self.porte = porte

    def Apresentar(self): #metodo para apresentar as caracteristicas do cachorro
        print("auau, meu nome é :", self.nome)
        print("auau, minha raça é :", self.raca)
        print("auau, minha pelagem é :", self.pelagem)
        print("auau, meu porte é :", self.porte)
    
    def Latir(self): #metodo para o cachorro latir
        print("auau,", self.nome, " está latindo intensamente")

    def Morder(self, cachorroAlvo): #metodo para o cachorro morder outro cachorro (recebendo o outro cachorro como argumento)
        print("auau,", self.nome, " mordeu ", cachorroAlvo.nome)


#criando os cachorros
cachorro1 = Cachorro("Roberto", "Vira-lata", "curta", "médio")
cachorro2 = Cachorro("Rex", "Pastor Alemão", "longa", "grande")

#chamando os metodos
#rinha de cachorro...
cachorro1.Latir()
cachorro2.Morder(cachorro1)
cachorro1.Morder(cachorro2)