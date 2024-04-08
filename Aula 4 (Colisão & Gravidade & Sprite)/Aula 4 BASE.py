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

gravidade = 0.5

#criando jogador
class Jogador():
    def __init__(self):
        self.xInicial = 100
        self.yInicial = 100

        self.largura = 50
        self.altura = 75

        self.sprite = pygame.image.load('Arquivos/Artes/mini qyron.png')
        self.sprite = pygame.transform.scale(self.sprite, (128, 128))
        #formula para o offset, que centraliza o sprite no rect, largura do rect - largura do sprite / 2, altura do rect - altura do sprite
        self.offset = [self.largura/2 - 64, self.altura - 128]
        self.olhandoParaDireita = True


        self.rect = pygame.Rect(self.xInicial, self.xInicial, self.largura, self.altura) #cria um retangulo que representa o jogador
        self.pulos = 2
        self.forcaPulo = 12
        self.velocidade = 10
        self.movimento = [0, 0]
        self.estaNoChao = False

        self.corRect = (200, 105, 19)

    def DesenharRect(self):
        pygame.draw.rect(tela, self.corRect, self.rect, 5)

    def Desenhar(self):
        if self.movimento[0] > 0 and self.olhandoParaDireita == False:
            self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.olhandoParaDireita = True

        elif self.movimento[0] < 0 and self.olhandoParaDireita == True:
            self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.olhandoParaDireita = False

        tela.blit(self.sprite, (self.rect.x + self.offset[0], self.rect.y + self.offset[1]))

    def Movimento(self, colisores = []):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] == True or teclas[pygame.K_a] == True:
            self.movimento[0] = -self.velocidade

        elif teclas[pygame.K_RIGHT] == True or teclas[pygame.K_d] == True:
            self.movimento[0] = self.velocidade

        else:
            self.movimento[0] = 0

        self.rect.x += self.movimento[0] #movimenta o jogador no eixo x

        for colisor in colisores: #verifica se está colidindo com algum colisor no eixo x
            if self.rect.colliderect(colisor):
                if self.movimento[0] > 0:
                    self.rect.right = colisor.left
                    self.movimento[0] = 0

                elif self.movimento[0] < 0:
                    self.rect.left = colisor.right
                    self.movimento[0] = 0
        
        '''if teclas[pygame.K_UP] == True or teclas[pygame.K_w] == True:
            self.movimento[1] = -self.velocidade

        elif teclas[pygame.K_DOWN] == True or teclas[pygame.K_s] == True:
            self.movimento[1] = self.velocidade

        else:
            self.movimento[1] = 0'''

        self.rect.y += self.movimento[1] #movimenta o jogador no eixo y

        self.movimento[1] += gravidade #adiciona a gravidade ao movimento no eixo y

        for colisor in colisores: #verifica se está colidindo com algum colisor no eixo y
            if self.rect.colliderect(colisor):
                if self.movimento[1] > 0:
                    self.rect.bottom = colisor.top
                    self.movimento[1] = 0
                    self.estaNoChao = True
                    self.pulos = 2

                elif self.movimento[1] < 0:
                    self.rect.top = colisor.bottom
                    self.movimento[1] = 0
                    self.estaNoChao = False

        print(self.movimento[1], self.estaNoChao)

    def Jump(self):
        if self.pulos > 0:
            self.movimento[1] = 0
            self.movimento[1] -= self.forcaPulo
            self.estaNoChao = False
            self.pulos -= 1

#Criando o loop principal e o objetos
            
jogadorClaudio = Jogador()
chao = pygame.Rect(0, 500, 600, 100)
bloco = pygame.Rect(250, 250, 300, 100)

rodando = True

clock = pygame.time.Clock()
fps = 60

while rodando: #enquanto rodando for verdadeiro, o jogo continuará rodando.

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False #se clicou no botão de fechar a janela, rodando se torna falso e o jogo para de rodar.

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jogadorClaudio.Jump()

    #primeiro vc mexe os pauzinhos por trás das cortinas, e depois mostra o resultado para o publico.

    jogadorClaudio.Movimento([chao, bloco])

    #Preenchendo a tela com a cor branca, como apagando uma lousa.
    tela.fill((255, 255, 255))

    #Desenhando o jogador
    pygame.draw.rect(tela, (0, 0, 255), bloco)
    pygame.draw.rect(tela, (255, 0, 0), chao)
    jogadorClaudio.DesenharRect()
    jogadorClaudio.Desenhar()

    #Atualizando a tela (como se você estivesse virando a pagina de um caderno)
    pygame.display.update()