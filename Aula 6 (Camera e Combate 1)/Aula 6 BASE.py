import pygame

pygame.init()

largura = 1280
altura = 720

tela = pygame.display.set_mode((largura, altura)) #cria a janela com o tamanho especificado
pygame.display.set_caption('projeto pygame') ##define o nome da janela
mundo = pygame.surface.Surface((64*100, 64*50))

gravidade = 0.9
colisores = []

class Jogador:
    def __init__(self):
        self.largura = 50
        self.altura = 100

        self.xInicial = 128
        self.yInicial = 576+64

        self.spriteOriginal = pygame.image.load("Aula 6 (Camera e Combate 1)/steve.png")
        self.spriteOriginal = pygame.transform.scale(self.spriteOriginal, (48, 96))

        self.spriteDano = pygame.image.load("Aula 6 (Camera e Combate 1)/steve dano.png")
        self.spriteDano = pygame.transform.scale(self.spriteDano, (48, 96))

        self.sprite = self.spriteOriginal

        self.correcao = [self.largura/2 - 24, self.altura - 96]
        self.olhandoParaDireita = True

        self.rect = pygame.Rect(self.xInicial, self.yInicial, self.largura, self.altura)
        self.cor = (135, 206, 235)

        self.movimento = [0 ,0]
        self.velocidade = 10
        self.forcaPulo = 15
        self.estaNoChao = False
        self.pulos = 2
        self.podeSerControlado = True

        self.temporizadorknockback = 0
        self.levandoDano = False
        self.vidaMaxima = 3
        self.vidaAtual = self.vidaMaxima

    def Desenhar(self):
        mundo.blit(self.sprite, (self.rect.x + self.correcao[0], self.rect.y + self.correcao[1]))

    def DesenharColisor(self):
        pygame.draw.rect(mundo, self.cor, self.rect, 5)

    def Movimento(self, colisores = []):

        teclas = pygame.key.get_pressed()

        '''if teclas[pygame.K_w] == True:
            self.movimento[1] = -self.velocidade

        elif teclas[pygame.K_s] == True:
            self.movimento[1] = self.velocidade

        else:
            self.movimento[1] = 0'''
        
        #aplica o movimento Y no jogador
        self.rect.y += self.movimento[1]
        self.movimento[1] += gravidade

        for colisor in colisores:
            if self.rect.colliderect(colisor):

                if self.movimento[1] > 0:
                    self.rect.bottom = colisor.top
                    self.movimento[1] = 0
                    self.estaNoChao = True
                    self.pulos = 2

                if self.movimento[1] < 0:
                    self.rect.top = colisor.bottom
                    self.movimento[1] = 0

        if self.podeSerControlado == True:
            if teclas[pygame.K_a] == True:
                self.movimento[0] = -self.velocidade

                if self.olhandoParaDireita == True:
                    self.spriteOriginal = pygame.transform.flip(self.spriteOriginal, True, False)
                    self.olhandoParaDireita = False

            elif teclas[pygame.K_d] == True:
                self.movimento[0] = self.velocidade

                if self.olhandoParaDireita == False:
                    self.spriteOriginal = pygame.transform.flip(self.spriteOriginal, True, False)
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
        if self.pulos > 0 and self.podeSerControlado:
            self.movimento[1] = -self.forcaPulo
            self.estaNoChao = False
            self.pulos -= 1

    def RestringirAoMundo(self, mundo):
        larguraMundo = mundo.get_width()
        alturaMundo = mundo.get_height()

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > larguraMundo:
            self.rect.right = larguraMundo

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > alturaMundo:
            self.rect.bottom = alturaMundo

    def Piscar(self):
        pass

    def Morrer(self):
        self.rect.x = self.xInicial
        self.rect.y = self.yInicial

        self.vidaAtual = self.vidaMaxima
        self.sprite = self.spriteOriginal
        self.podeSerControlado = True
        self.levandoDano = False
        self.temporizadorknockback = 0

    def LevarDano(self, dano):
        self.vidaAtual -= dano
        self.levandoDano = True
        self.podeSerControlado = False

        self.movimento[1] = -10

        if self.olhandoParaDireita == True:
            self.movimento[0] = -10
        else:
            self.movimento[0] = 10

    def Atualizar(self, mundo, colisores = []):
        self.Movimento(colisores)
        self.RestringirAoMundo(mundo)

        if self.vidaAtual <= 0:
            self.Morrer()
        
        if self.levandoDano == True:
            self.temporizadorknockback += 1
            self.sprite = self.spriteDano

            if self.temporizadorknockback > 10:
                self.levandoDano = False
                self.podeSerControlado = True
                self.temporizadorknockback = 0
                self.sprite = self.spriteOriginal


class Tilemap:
    def __init__(self):
        self.tamanhoTile = 64 #define a altura e largura de cada tile (porque é um quadrado)

        self.texturas = [
            '',
            pygame.transform.scale(pygame.image.load("Aula 6 (Camera e Combate 1)/grama.png"), (self.tamanhoTile, self.tamanhoTile)),
            pygame.transform.scale(pygame.image.load("Aula 6 (Camera e Combate 1)/terra.png"), (self.tamanhoTile, self.tamanhoTile))
        ]

        self.mapa = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,2,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,2,0,2,0,2,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,1,2,2,0,0,2,2,2,0,2,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,2,2,1,0,0,0,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,0,0,0,0,0,2,2,2,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,2,2,0,0,0,2,2,2,2,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        ]


        self.superficieTilemap = pygame.Surface((len(self.mapa[0]) * self.tamanhoTile, len(self.mapa) * self.tamanhoTile))
        self.superficieTilemap.set_colorkey((0, 0, 0))


    def CriarTilemap(self):
        for linha in range(len(self.mapa)):
            for coluna in range(len(self.mapa[0])):
                if self.mapa[linha][coluna] != 0:
                    self.superficieTilemap.blit(self.texturas[self.mapa[linha][coluna]], (coluna * self.tamanhoTile, linha * self.tamanhoTile))
                    colisores.append(pygame.Rect(coluna * self.tamanhoTile, linha * self.tamanhoTile, self.tamanhoTile, self.tamanhoTile))

    def DesenharTilemap(self):
        mundo.blit(self.superficieTilemap, (0, 0))

class CameraQueSegue():
    def __init__(self, alvo, mundo):
        self.alvo = alvo
        self.rect = pygame.Rect(0, 0, largura, altura)
        self.superficieMundo = mundo
        self.larguraMundo = mundo.get_width()
        self.alturaMundo = mundo.get_height()

        #superficie camera é subsfurface da superficie mundo

    def Atualizar(self):
        self.rect.center = self.alvo.rect.center

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > self.larguraMundo:
            self.rect.right = self.larguraMundo

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > self.alturaMundo:
            self.rect.bottom = self.alturaMundo

    def Mostrar(self):
        superficieCamera = pygame.Surface.subsurface(self.superficieMundo, self.rect)
        tela.blit(superficieCamera, (0, 0))
        pygame.display.update() #atualiza a tela

class Espinho():
    def __init__(self, jogador, x, y):
        self.jogador = jogador

        self.largura = 64
        self.altura = 64

        self.sprite = pygame.image.load("Aula 6 (Camera e Combate 1)/espinho.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        self.rect = pygame.Rect(x, y, self.largura, self.altura)

        self.dano = 1

    def Desenhar(self):
        mundo.blit(self.sprite, (self.rect.x, self.rect.y))
    
    def DesenharColisor(self):
        pygame.draw.rect(mundo, (255, 0, 0), self.rect, 5)

    def Atualizar(self):
        if self.jogador.rect.colliderect(self.rect):
            self.jogador.LevarDano(self.dano)

jogador = Jogador()

tilemap = Tilemap()
tilemap.CriarTilemap()

espinhos = [
    Espinho(jogador, 512, 64*14),
    Espinho(jogador, 576, 64*14),
    Espinho(jogador, 64*19, 64*14),
    Espinho(jogador, 64*20, 64*14),
    Espinho(jogador, 64*21, 64*14),
    Espinho(jogador, 64*26, 64*14),
    Espinho(jogador, 64*27, 64*14),
    Espinho(jogador, 64*28, 64*14),
]

camera = CameraQueSegue(jogador, mundo)

rodando = True
clock = pygame.time.Clock()

while rodando:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jogador.Pulo()

    jogador.Atualizar(mundo, colisores)

    for espinho in espinhos:
        espinho.Atualizar()

    camera.Atualizar()

    tela.fill((0, 0, 0))
    mundo.fill((135, 206, 250))

    tilemap.DesenharTilemap()
    jogador.DesenharColisor()
    jogador.Desenhar() 
    
    for espinho in espinhos:
        espinho.Desenhar()
        #espinho.DesenharColisor()

    camera.Mostrar()