#Importando a biblioteca pygame
import pygame

#Inicializando os módulos do pygame (como se você estivesse ligando os interruptores da sua casa, os eletrodomesticos e etc... antes de começar a utiliza-la)
pygame.init()

#Definindo a largura e altura da tela
largura = 800
altura = 600

#Criando a tela e definindo o titulo.
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('projeto pygame')

#criando jogador
class Jogador():
    def __init__(self):
        self.xInicial = 100
        self.yInicial = 100

        self.largura = 50
        self.altura = 100

        self.rect = pygame.Rect(self.xInicial, self.xInicial, self.largura, self.altura) #cria um retangulo que representa o jogador
        self.cor = (200, 105, 19)
 
        self.velocidade = 10

    def Desenhar(self):
        pygame.draw.rect(tela, self.cor, self.rect)

    def Movimento(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] == True:
            self.rect.x -= self.velocidade

        if teclas[pygame.K_RIGHT] == True:
            self.rect.x += self.velocidade
        
        if teclas[pygame.K_UP] == True:
            self.rect.y -= self.velocidade

        if teclas[pygame.K_DOWN] == True:
            self.rect.y += self.velocidade

#Criando o loop principal e o objetos
            
jogadorClaudio = Jogador()

rodando = True

clock = pygame.time.Clock()
fps = 60

while rodando: #enquanto rodando for verdadeiro, o jogo continuará rodando.

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False #se clicou no botão de fechar a janela, rodando se torna falso e o jogo para de rodar.

    #primeiro vc mexe os pauzinhos por trás das cortinas, e depois mostra o resultado para o publico.

    jogadorClaudio.Movimento()

    #Preenchendo a tela com a cor branca, como apagando uma lousa.
    tela.fill((255, 255, 255))

    #Desenhando o jogador
    jogadorClaudio.Desenhar()

    #Atualizando a tela (como se você estivesse virando a pagina de um caderno)
    pygame.display.update()