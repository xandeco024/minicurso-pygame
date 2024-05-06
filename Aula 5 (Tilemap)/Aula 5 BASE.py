#Aula 2: Criando o objeto jogador
#Compreendendo como funcionam as classes em python e suas funções.

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

gravidade = 1

#criando jogador

class Jogador(pygame.sprite.Sprite):
    def __init__(self, xInicial, yInicial):
        super().__init__()

        self.largura = 64
        self.altura = 64

        self.image = pygame.image.load('Arquivos/Artes/mini qyron.png') #carrega a imagem do jogador
        self.image = pygame.transform.scale(self.image, (self.largura, self.altura))  #estica a imagem do jogador para o tamanho desejado
        self.olhandoParaDireita = True

        self.rect = pygame.Rect(xInicial, yInicial, self.largura, self.altura) #cria um retangulo que representa o jogador

        self.velocidade = 10 #define a velocidade que o jogador terá
        self.velocidadeXY = [0, 0] #define os eixos x e y, que serão utilizados para movimentar o jogador, colisão e animação

        self.forcaPulo = 10 #define a força do pulo

    def Desenhar(self):
        tela.blit(self.image, self.rect) #desenha a imagem do jogador na tela, na posição do rect do jogador

    def DesenharColisor(self):
        pygame.draw.rect(tela, (255, 0, 0), self.rect, 2) #desenha o rect do jogador na tela

    def Movimento(self, rectsColisao):

        teclas = pygame.key.get_pressed() #pega todas as teclas, que estão sendo pressionadas ou não

        if teclas[pygame.K_RIGHT] == True: #se a tecla direita estiver sendo pressionada
            self.velocidadeXY[0] = self.velocidade

            if self.olhandoParaDireita == False: #se o jogador estiver olhando para a esquerda
                self.image = pygame.transform.flip(self.image, True, False) #gire a imagem do jogador
                self.olhandoParaDireita = True #o jogador agora está olhando para a direita

        elif teclas[pygame.K_LEFT] == True: #se a tecla esquerda estiver sendo pressionada
            self.velocidadeXY[0] = -self.velocidade #mova o jogador para a esquerda

            if self.olhandoParaDireita == True: #se o jogador estiver olhando para a direita
                self.image = pygame.transform.flip(self.image, True, False) #gire a imagem do jogador
                self.olhandoParaDireita = False #o jogador agora está olhando para a esquerda

        else:
            self.velocidadeXY[0] = 0 #se nem tecla para direita, nem a para esquerda estiver sendo pressionada, a velocidade no eixo x é 0

        if teclas[pygame.K_UP] == True: #se a tecla cima estiver sendo pressionada
            self.velocidadeXY[1] = -self.velocidade

        elif teclas[pygame.K_DOWN] == True: #se a tecla baixo estiver sendo pressionada
            self.velocidadeXY[1] = self.velocidade

        else:
            self.velocidadeXY[1] = 0 #se nem tecla para cima, nem a para baixo estiver sendo pressionada, a velocidade no eixo y é 0

        print(self.velocidadeXY)

        #aplica o movimento no jogador
        self.rect.x += self.velocidadeXY[0] 

        for rect in rectsColisao: #loop para verificar se o jogador está colidindo horizontalmente com cada um dos tiles que tem colisão.
            if self.rect.colliderect(rect) == True:
                if self.velocidadeXY[0] > 0: #colisão com a direita
                    self.rect.right = rect.left
                    self.velocidadeXY[0] = 0

                elif self.velocidadeXY[0] < 0: #colisão com a esquerda
                    self.rect.left = rect.right
                    self.velocidadeXY[0] = 0

        self.rect.y += self.velocidadeXY[1]

        for rect in rectsColisao: #loop para verificar se o jogador está colidindo verticalmente com cada um dos tiles que tem colisão.
            if self.rect.colliderect(rect) == True:
                if self.velocidadeXY[1] > 0: #colisão com o chão
                    self.rect.bottom = rect.top
                    self.velocidadeXY[1] = 0

                elif self.velocidadeXY[1] < 0: #colisão com o teto
                    self.rect.top = rect.bottom
                    self.velocidadeXY[1] = 0

        #fazer gracinha ver se conseguem coocar pra movimentar no wasd e nas setas.

class Tilemap(): #classe que representa um tilemap, que é utilizado para construir as fases.
    def __init__(self):
        self.tamanhoTile = 64 #define a altura e largura de cada tile (porque é um quadrado)

        self.texturas = [
            "",
            pygame.transform.scale(pygame.image.load("Arquivos/Artes/grama.png"), (self.tamanhoTile, self.tamanhoTile)),
            pygame.transform.scale(pygame.image.load("Arquivos/Artes/terra.png"), (self.tamanhoTile, self.tamanhoTile))
        ]

        self.mapa = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0],
            [0,0,0,0,0,0,1,2,2,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,2,2,2,2,0,0,0,0,0,0,0,0],
            [1,1,1,1,2,2,2,2,2,2,1,1,1,1,0,0,1,1],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        ]

        self.tilesColisao = []

        self.superficieTilemap = pygame.Surface((len(self.mapa[0] * self.tamanhoTile), len(self.mapa * self.tamanhoTile)))
        self.superficieTilemap.set_colorkey((0, 0, 0))

    def CriarTilemap(self):
        for linha in range(len(self.mapa)):
            for coluna in range(len(self.mapa[linha])):
                if self.mapa[linha][coluna] != 0:
                    self.superficieTilemap.blit(self.texturas[self.mapa[linha][coluna]], (coluna * self.tamanhoTile, linha * self.tamanhoTile))
                    self.tilesColisao.append(pygame.Rect(coluna * self.tamanhoTile, linha * self.tamanhoTile, self.tamanhoTile, self.tamanhoTile))

    def DesenharTilemap(self):
        tela.blit(self.superficieTilemap, (0, 0))

#criando objetos do jogo

tilemap = Tilemap()
tilemap.CriarTilemap()

jogador = Jogador(100, 100)

#Criando o loop principal
rodando = True

clock = pygame.time.Clock()
fps = 60

while rodando: #enquanto rodando for verdadeiro, o jogo continuará rodando.

    clock.tick(fps)

    #Verificando se o usuário clicou no botão de fechar a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False #se clicou no botão de fechar a janela, rodando se torna falso e o jogo para de rodar

    #Preenchendo a tela com a cor branca, como apagando uma lousa.
    tela.fill((20, 20, 50))

    #Desenhando um retangulo na tela
    #pygame.draw.rect(tela, jogadorCor, jogadorRect) #desenha na TELA, com a COR DO JOGADOR, um RETANGULO na POSIÇÃO DO JOGADOR, com sua ALTURA E LARGURA.

    tilemap.DesenharTilemap()

    jogador.Movimento(tilemap.tilesColisao)
    jogador.DesenharColisor()
    jogador.Desenhar()

    #Atualizando a tela (como se você estivesse virando a pagina de um caderno)
    pygame.display.update() 