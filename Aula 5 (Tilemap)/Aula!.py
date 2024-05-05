import pygame

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura)) #cria a janela com o tamanho especificado
pygame.display.set_caption('projeto pygame') ##define o nome da janela

gravidade = 0.5

colisaos = []

class Jogador:
    def __init__(self, usaSetas):
        self.largura = 50
        self.altura = 100

        self.xInicial = 100
        self.yInicial = 100

        self.sprite = pygame.image.load("Aula 4 (Colisão & Gravidade & Sprite)/sanic.png")
        self.sprite = pygame.transform.scale(self.sprite, (96, 96))
        self.correcao = [self.largura/2 - 48, self.altura - 96]
        self.olhandoParaDireita = True

        self.rect = pygame.Rect(self.xInicial, self.yInicial, self.largura, self.altura)
        self.cor = (135, 206, 235)

        self.movimento = [0 ,0]
        self.velocidade = 10
        self.forcaPulo = 10
        self.estaNoChao = False
        self.pulos = 2

        self.usaSetas = usaSetas

        self.rect.x += self.velocidade

    def Desenhar(self):
        tela.blit(self.sprite, (self.rect.x + self.correcao[0], self.rect.y + self.correcao[1]))

    def DesenharColisor(self):
        pygame.draw.rect(tela, self.cor, self.rect, 5)

    def Movimento(self, colisores = []):

        teclas = pygame.key.get_pressed()

        '''if teclas[pygame.K_w] == True:
            self.movimento[1] = -self.velocidade

        elif teclas[pygame.K_s] == True:
            self.movimento[1] = self.velocidade

        else:
            self.movimento[1] = 0'''

        print(self.movimento)
        #aplica o movimento Y no jogador
        self.rect.y += self.movimento[1]

        self.movimento[1] += gravidade

        for colisor in colisores:
            if self.rect.colliderect(colisor):
                print("colidiu")

                if self.movimento[1] > 0:
                    self.rect.bottom = colisor.top
                    self.movimento[1] = 0
                    self.estaNoChao = True
                    self.pulos = 2

                if self.movimento[1] < 0:
                    self.rect.top = colisor.bottom
                    self.movimento[1] = 0

        if teclas[pygame.K_a] == True:
            self.movimento[0] = -self.velocidade

            if self.olhandoParaDireita == True:
                self.sprite = pygame.transform.flip(self.sprite, True, False)
                self.olhandoParaDireita = False

        elif teclas[pygame.K_d] == True:
            self.movimento[0] = self.velocidade

            if self.olhandoParaDireita == False:
                self.sprite = pygame.transform.flip(self.sprite, True, False)
                self.olhandoParaDireita = True

        else:
            self.movimento[0] = 0

        #aplica o movimento X no jogador
        self.rect.x += self.movimento[0]

        for colisor in colisores:
            if self.rect.colliderect(colisor):
                if self.movimento[0] > 0:
                    self.rect.right = colisor.left
                    self.movimento[0] = 0

                elif self.movimento[0] < 0:
                    self.rect.left = colisor.right
                    self.movimento[0] = 0

    def Pulo(self):
        if self.pulos > 0:
            self.movimento[1] = -self.forcaPulo
            self.estaNoChao = False
            self.pulos -= 1

class Tilemap:
    def __init__(self):
        self.tamanhoTile = 64

        self.texturas = [
            '',
            pygame.transform.scale(pygame.image.load('Aula 5 (Tilemap)/grama.png'), (self.tamanhoTile, self.tamanhoTile)),
            pygame.transform.scale(pygame.image.load("Aula 5 (Tilemap)/terra.png"), (self.tamanhoTile, self.tamanhoTile))
        ]

        self.mapa = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0],
            [0,0,0,0,0,0,1,2,2,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,2,2,2,2,0,0,0,0,0,0,0,0],
            [1,1,1,1,2,2,2,2,2,2,1,1,1,1,0,0,1,1],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        ]

        self.superficieTilemap = pygame.Surface((len(self.mapa[0]) * self.tamanhoTile, len(self.mapa) * self.tamanhoTile))
        self.superficieTilemap.set_colorkey((0, 0, 0))

    def Construir(self):
        for linha in range(len(self.mapa)):
            for coluna in range(len(self.mapa[0])):
                if self.mapa[linha][coluna] != 0:
                    self.superficieTilemap.blit(self.texturas[self.mapa[linha][coluna]], (coluna * self.tamanhoTile, linha * self.tamanhoTile))
                    colisaos.append(pygame.Rect(coluna * self.tamanhoTile, linha * self.tamanhoTile, self.tamanhoTile, self.tamanhoTile))

    def Desenhar(self):
        tela.blit(self.superficieTilemap, (0, 0))

jogadorClaudio = Jogador(False)



chao = pygame.Rect(0, 500, 500, 100)

tilemap = Tilemap()

tilemap.Construir()

rodando = True
clock = pygame.time.Clock()

while rodando:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jogadorClaudio.Pulo()

    jogadorClaudio.Movimento(colisaos)

    tela.fill((255, 255, 255))

    #desenha o chao provisório 
    #pygame.draw.rect(tela, (0, 255, 0), chao) 

    tilemap.Desenhar()
    jogadorClaudio.DesenharColisor()
    jogadorClaudio.Desenhar() 

    pygame.display.update() #atualiza a tela