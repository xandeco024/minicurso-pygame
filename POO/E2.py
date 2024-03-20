class Pessoa: #Classe pessoa que recebe nome, idade e profissão
    def __init__(self, nome, idade, profissao):
        self.nome = nome
        self.idade = idade
        self.profissao = profissao

    def Apresentar(self):
        print("Olá, meu nome é", self.nome,", tenho", self.idade, "anos e sou ", self.profissao)

    def Trabalhar(self):
        print("Estou trabalhando")

    def Envelhecer(self):
        self.idade += 1

pessoa1 = Pessoa("João", 25, "Programador") 

pessoa1.Apresentar()
pessoa1.Trabalhar()
pessoa1.Envelhecer()
pessoa1.Apresentar()