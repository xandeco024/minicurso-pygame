import pygame

pygame.init()

largura = 1280
altura = 720

tela = pygame.display.set_mode((largura, altura)) #cria a janela com o tamanho especificado
pygame.display.set_caption('projeto pygame') ##define o nome da janela

#removeu o pygame.display.update da camera e criou a hud

class Jogador:
    def __init__(self, gravidade, colisores, mundo):
        self.largura = 64
        self.altura = 128

        self.colisores = colisores
        self.mundo = mundo
        self.gravidade = gravidade

        self.xInicial = 128
        self.yInicial = 64*14

        self.spriteOriginal = pygame.image.load("Aula 7 (Combate 2)/steve.png")
        self.spriteOriginal = pygame.transform.scale(self.spriteOriginal, (self.largura, self.altura))

        self.spriteDano = pygame.image.load("Aula 7 (Combate 2)/steve dano.png")
        self.spriteDano = pygame.transform.scale(self.spriteDano, (self.largura, self.altura))

        self.sprite = self.spriteOriginal

        self.correcao = [0,0]
        self.olhandoParaDireita = True

        self.rect = pygame.Rect(self.xInicial, self.yInicial, self.largura, self.altura)
        self.cor = (135, 206, 235)

        self.movimento = [0 ,0]
        self.velocidade = 10
        self.forcaPulo = 15
        self.estaNoChao = False
        self.pulos = 2
        self.podeSerControlado = True

        self.puloSFX = pygame.mixer.Sound("Aula 9 (SOM)/SFX/pulo.wav")
        self.puloSFX.set_volume(0.1)
        self.tiroSFX = pygame.mixer.Sound("Aula 9 (SOM)/SFX/tiro.wav")
        self.tiroSFX.set_volume(0.1)
        self.danoSFX = pygame.mixer.Sound("Aula 9 (SOM)/SFX/dano.wav")
        self.danoSFX.set_volume(0.1)

        self.dano = 1
        self.temporizadorknockback = 0
        self.levandoDano = False
        self.vidaMaxima = 3
        self.vidaAtual = self.vidaMaxima

        self.pontos = 0

    def Desenhar(self, superficie):
        superficie.blit(self.sprite, (self.rect.x + self.correcao[0], self.rect.y + self.correcao[1]))

    def DesenharColisor(self, superficie):
        pygame.draw.rect(superficie, self.cor, self.rect, 5)

    def Movimento(self):

        teclas = pygame.key.get_pressed()

        '''if teclas[pygame.K_w] == True:
            self.movimento[1] = -self.velocidade

        elif teclas[pygame.K_s] == True:
            self.movimento[1] = self.velocidade

        else:
            self.movimento[1] = 0'''
        
        #aplica o movimento Y no jogador
        self.rect.y += self.movimento[1]
        self.movimento[1] += self.gravidade

        for colisor in self.colisores:
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

        for colisor in self.colisores:
            if self.rect.colliderect(colisor):
                if self.movimento[0] > 0:
                    self.rect.right = colisor.left
                    self.movimento[0] = 0

                elif self.movimento[0] < 0:
                    self.rect.left = colisor.right
                    self.movimento[0] = 0

    def Pulo(self):
        if self.pulos > 0 and self.podeSerControlado:
            self.puloSFX.play()
            self.movimento[1] = -self.forcaPulo
            self.estaNoChao = False
            self.pulos -= 1

    def RestringirAoMundo(self):
        larguraMundo = self.mundo.get_width()
        alturaMundo = self.mundo.get_height()

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > larguraMundo:
            self.rect.right = larguraMundo

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > alturaMundo:
            self.rect.bottom = alturaMundo

    def Morrer(self):
        self.rect.x = self.xInicial
        self.rect.y = self.yInicial

        self.vidaAtual = self.vidaMaxima
        self.sprite = self.spriteOriginal
        self.podeSerControlado = True
        self.levandoDano = False
        self.temporizadorknockback = 0

    def LevarDano(self, dano):
        self.danoSFX.play()
        self.vidaAtual -= dano
        self.levandoDano = True
        self.podeSerControlado = False

        self.movimento[1] = -10

        if self.olhandoParaDireita == True:
            self.movimento[0] = -10
        else:
            self.movimento[0] = 10

    def Disparar(self, objetos):
        self.tiroSFX.play()
        projetil = ProjetilJogador(self, objetos)
        objetos.Adicionar(projetil)

    def Atualizar(self):
        self.Movimento()
        self.RestringirAoMundo()

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

class ProjetilJogador:
    def __init__(self, jogador, objetos):
        self.jogador = jogador
        self.objetos = objetos

        self.largura = 32
        self.altura = 32

        self.sprite = pygame.image.load("Aula 7 (Combate 2)/projetil.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        if self.jogador.olhandoParaDireita == True:
            self.direcao = 1
        else:
            self.direcao = -1

        self.rect = pygame.Rect(self.jogador.rect.x + self.direcao, self.jogador.rect.y, self.largura, self.altura)

        self.velocidade = 20

        self.tempoDeVida = 120

    def Desenhar(self, superficie):
        superficie.blit(self.sprite, (self.rect.x, self.rect.y))

    def Atualizar(self):

        self.tempoDeVida -= 1
        if self.tempoDeVida <= 0:
            self.objetos.Remover(self)

        self.rect.x += self.velocidade * self.direcao

        for objeto in self.objetos.lista:
            if isinstance(objeto, InimigoPatrulhador):
                if self.rect.colliderect(objeto.rect):
                    objeto.LevarDano(self.jogador.dano)
                    self.objetos.Remover(self)

class Tilemap:
    def __init__(self):
        self.tamanhoTile = 64 #define a altura e largura de cada tile (porque é um quadrado)

        self.texturas = [
            '',
            pygame.transform.scale(pygame.image.load("Aula 7 (Combate 2)/grama.png"), (self.tamanhoTile, self.tamanhoTile)),
            pygame.transform.scale(pygame.image.load("Aula 7 (Combate 2)/terra.png"), (self.tamanhoTile, self.tamanhoTile))
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
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,1,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,2,2,1,0,0,0,2,2,2,2,2,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,0,0,0,0,0,2,2,2,0,0,0,2,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,2,2,0,0,0,2,2,2,2,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1],
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

    def Desenhar(self, superficie):
        superficie.blit(self.superficieTilemap, (0, 0))

class CameraQueSegue:
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

    def Mostrar(self, superficie):
        superficieCamera = pygame.Surface.subsurface(self.superficieMundo, self.rect)
        superficie.blit(superficieCamera, (0, 0))

class Espinho:
    def __init__(self, jogador, x, y):
        self.jogador = jogador

        self.largura = 64
        self.altura = 64

        self.sprite = pygame.image.load("Aula 7 (Combate 2)/espinho.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        self.rect = pygame.Rect(x, y, self.largura, self.altura)

        self.dano = 1

    def Desenhar(self, superficie):
        superficie.blit(self.sprite, (self.rect.x, self.rect.y))
    
    def DesenharColisor(self, superficie):
        pygame.draw.rect(superficie, (255, 0, 0), self.rect, 5)

    def Atualizar(self):
        if self.jogador.rect.colliderect(self.rect):
            self.jogador.LevarDano(self.dano)

class InimigoPatrulhador:
    def __init__(self, amplitude, objetos, x, y):
        self.objetos = objetos

        self.largura = 64
        self.altura = 128

        self.spriteOriginal = pygame.image.load("Aula 7 (Combate 2)/zombie.png")
        self.spriteOriginal = pygame.transform.scale(self.spriteOriginal, (self.largura, self.altura))

        self.spriteDano = pygame.image.load("Aula 7 (Combate 2)/zombie dano.png")
        self.spriteDano = pygame.transform.scale(self.spriteDano, (self.largura, self.altura))

        self.sprite = self.spriteOriginal

        self.indo = True
        self.amplitude = amplitude
        self.xInicial = x
        self.rect = pygame.Rect(x, y, self.largura, self.altura)

        self.levandoDano = True
        self.temporizadorDano = 0
        self.vidaMaxima = 3
        self.vidaAtual = self.vidaMaxima
        self.dano = 2

        self.morteSFX = pygame.mixer.Sound("Aula 9 (SOM)/SFX/inimigoMorte.wav")
        self.morteSFX.set_volume(0.1)

        self.velocidade = 3

    def Movimento(self):
        if self.indo == True:
            self.rect.x += self.velocidade

            if self.rect.x > self.xInicial + self.amplitude:
                self.indo = False
                self.sprite = pygame.transform.flip(self.sprite, True, False)
        
        else:
            self.rect.x -= self.velocidade

            if self.rect.x < self.xInicial:
                self.indo = True
                self.sprite = pygame.transform.flip(self.sprite, True, False)

    def LevarDano(self, dano):
        self.vidaAtual -= dano
        self.sprite = self.spriteDano
        self.levandoDano = True

    def Desenhar(self, superficie):
        superficie.blit(self.sprite, (self.rect.x, self.rect.y))

    def Atualizar(self):
        self.Movimento()

        for objeto in self.objetos.lista:
            if isinstance(objeto, Jogador):
                if self.rect.colliderect(objeto.rect):
                    objeto.LevarDano(self.dano)

        if self.levandoDano == True:
            self.temporizadorDano += 1

            if self.temporizadorDano > 10:
                self.sprite = self.spriteOriginal
                self.levandoDano = False
                self.temporizadorDano = 0

        if self.vidaAtual <= 0:
            print("i morreu")
            self.morteSFX.play()
            self.objetos.Remover(self)

class Moeda:
    def __init__(self, objetos, x, y):
        self.largura = 64
        self.altura = 64

        self.objetos = objetos

        for objeto in self.objetos.lista:
            if isinstance(objeto, Jogador):
                self.jogador = objeto

        self.sprite = pygame.image.load("Aula 7 (Combate 2)/moeda.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        self.yInicial = y
        self.indo = True
        self.rect = pygame.Rect(x, y, self.largura, self.altura)
        self.velocidade = 1

        self.moedaSFX = pygame.mixer.Sound("Aula 9 (SOM)/SFX/moeda.wav")
        self.moedaSFX.set_volume(0.1)

    def Desenhar(self, superficie):
        superficie.blit(self.sprite, (self.rect.x, self.rect.y))

    def Movimento(self):
        if self.indo == True:
            self.rect.y += self.velocidade

            if self.rect.y >= self.yInicial + 10:
                self.indo = False
        
        else:
            self.rect.y -= self.velocidade

            if self.rect.y <= self.yInicial:
                self.indo = True

    def Atualizar(self):
        self.Movimento()

        if self.jogador.rect.colliderect(self.rect):
            self.jogador.pontos += 1
            self.moedaSFX.play()
            self.objetos.Remover(self)

class Grupo:
    def __init__(self):
        self.lista = []

    def Adicionar(self, objeto):
        self.lista.append(objeto)

    def Remover(self, objeto):
        self.lista.remove(objeto)

    def Atualizar(self):
        for objeto in self.lista:
            if hasattr(objeto, "Atualizar"):
                objeto.Atualizar()

    def Desenhar(self, superficie):
        for objeto in self.lista:
            if hasattr(objeto, "Desenhar"):
                objeto.Desenhar(superficie)

class HUD:
    def __init__(self, jogador):
        self.jogador = jogador

        self.coracao = pygame.image.load("Aula 8 (HUD)/coracao.png")
        self.coracao = pygame.transform.scale(self.coracao, (48, 48))

        self.moeda = pygame.image.load("Aula 8 (HUD)/moeda.png")
        self.moeda = pygame.transform.scale(self.moeda, (48, 48))

    def Mostrar(self, superficie):
        fonte = pygame.font.Font("Aula 8 (HUD)/Kenney Pixel Square.ttf", 32)

        for i in range(self.jogador.vidaAtual):
            superficie.blit(self.coracao, (48 + 48 * i * 1.25, 48))

        superficie.blit(self.moeda, (48, 48*3))

        textoPontos = fonte.render(str(self.jogador.pontos), True, (255, 255, 255))
        superficie.blit(textoPontos, (48*2 + 10, 48*3 - 2))


mundo = pygame.surface.Surface((64*100, 64*50))

mixer = pygame.mixer

mixer.music.load("Aula 9 (SOM)/BGM/musica1.mp3")
mixer.music.set_volume(0.1)
mixer.music.play(-1)

gravidade = 0.9
colisores = []
objetos = Grupo()

jogador = Jogador(gravidade, colisores, mundo)
objetos.Adicionar(jogador)

tilemap = Tilemap()
tilemap.CriarTilemap()
objetos.Adicionar(tilemap)

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

for espinho in espinhos:
    objetos.Adicionar(espinho)

inimigo1 = InimigoPatrulhador(256, objetos, 64*8, 64*13)
objetos.Adicionar(inimigo1)

moeda1 = Moeda(objetos, 64*20, 64*8)
objetos.Adicionar(moeda1)

moeda2 = Moeda(objetos, 64*27, 64*8)
objetos.Adicionar(moeda2)

camera = CameraQueSegue(jogador, mundo)
objetos.Adicionar(camera)

hud = HUD(jogador)
objetos.Adicionar(hud)

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                jogador.Disparar(objetos)

    objetos.Atualizar()

    tela.fill((0, 0, 0))
    mundo.fill((135, 206, 250))

    objetos.Desenhar(mundo)

    camera.Mostrar(tela)
    hud.Mostrar(tela)

    pygame.display.update()