import pygame, sys

pygame.init()

largura = 1280
altura = 720

tela = pygame.display.set_mode((largura, altura)) #cria a janela com o tamanho especificado
pygame.display.set_caption('Cenourinha Adventure Pygame Edition') ##define o nome da janela

#removeu o pygame.display.update da camera e criou a hud

class Jogador:
    def __init__(self, gravidade, colisores, mundo, objetos):
        self.largura = 64
        self.altura = 64

        self.colisores = colisores
        self.mundo = mundo
        self.gravidade = gravidade
        self.objetos = objetos

        self.xInicial = 128
        self.yInicial = 64*14

        self.sprite = pygame.image.load("Assets/Sprites/Cenourinha/parado1.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        self.animacoes = {
            'andando': {
                'nome': 'andando',
                'sprites': [
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Cenourinha/andando1.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Cenourinha/andando2.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Cenourinha/andando3.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Cenourinha/andando4.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Cenourinha/andando5.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Cenourinha/andando6.png"), (self.largura, self.altura)),
                ],
                'velocidade': 0.15
            },

            'parado': {
                'nome': 'parado',
                'sprites': [
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Cenourinha/parado1.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Cenourinha/parado2.png"), (self.largura, self.altura)),
                ],
                'velocidade': 0.075
            },

            'pulando': {
                'nome': 'pulando',
                'sprites': [
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Cenourinha/pulando.png"), (self.largura, self.altura)),
                ],
                'velocidade': 0.1
            },

            'dano': {
                'nome': 'dano',
                'sprites': [
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Cenourinha/dano.png"), (self.largura, self.altura)),
                ],
                'velocidade': 0.1
            }
        }

        self.animador = Animador(self.animacoes)

        self.animador.DefinirAnimacao('parado')

        self.correcao = [0,0]
        self.olhandoParaDireita = True

        self.rect = pygame.Rect(self.xInicial, self.yInicial, self.largura, self.altura)
        self.cor = (135, 206, 235)

        self.gatilhoDisparo = True
        self.gatilhoPulo = True

        self.movimento = [0 ,0]
        self.velocidade = 8
        self.forcaPulo = 15
        self.estaNoChao = False
        self.pulos = 2
        self.podeSerControlado = True

        self.puloSFX = pygame.mixer.Sound("Assets/SFX/pulo.wav")
        self.puloSFX.set_volume(0.1)
        self.tiroSFX = pygame.mixer.Sound("Assets/SFX/tiro.wav")
        self.tiroSFX.set_volume(0.1)
        self.danoSFX = pygame.mixer.Sound("Assets/SFX/dano.wav")
        self.danoSFX.set_volume(0.1)

        self.dano = 1
        self.temporizadorknockback = 0
        self.levandoDano = False
        self.vidaMaxima = 3
        self.vidaAtual = self.vidaMaxima

        self.pontos = 0

    def Desenhar(self, superficie):
        self.sprite = self.animador.SpriteAtual()
        if self.olhandoParaDireita == False:
            self.sprite = pygame.transform.flip(self.sprite, True, False)
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
                    #self.sprite = pygame.transform.flip(self.sprite, True, False)
                    self.olhandoParaDireita = False

            elif teclas[pygame.K_d] == True:
                self.movimento[0] = self.velocidade

                if self.olhandoParaDireita == False:
                    #self.sprite = pygame.transform.flip(self.sprite, True, False)
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
        #remover self.sprite = self.sprite
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

    def Animar(self):
        if self.movimento[0] != 0 and self.animador.AnimacaoAtual() != 'andando':
            self.animador.DefinirAnimacao('andando')

        elif self.movimento[0] == 0 and self.animador.AnimacaoAtual() != 'parado':
            self.animador.DefinirAnimacao('parado')

        if self.estaNoChao == False and self.animador.AnimacaoAtual() != 'pulando':
            self.animador.DefinirAnimacao('pulando')

        if self.levandoDano == True and self.animador.AnimacaoAtual() != 'dano':
            self.animador.DefinirAnimacao('dano')

    def Atualizar(self):
        self.Movimento()
        self.RestringirAoMundo()
        self.Animar()
        self.animador.Atualizar()

        teclas = pygame.key.get_pressed()
        botoes = pygame.mouse.get_pressed()

        if teclas[pygame.K_SPACE] == True:
            if self.gatilhoPulo == False:
                self.Pulo()
                self.gatilhoPulo = True

        else:
            self.gatilhoPulo = False

        #if teclas[pygame.K_q] == True:
        #    if self.gatilhoDisparo == False:
        #        self.Disparar(self.objetos)
        #        self.gatilhoDisparo = True
        #
        #else:
        #    self.gatilhoDisparo = False
            
        if botoes[0] == True:
            if self.gatilhoDisparo == False:
                self.Disparar(self.objetos)
                self.gatilhoDisparo = True
        else:
            self.gatilhoDisparo = False

        if self.vidaAtual <= 0:
            self.Morrer()
        
        if self.levandoDano == True:
            self.temporizadorknockback += 1
            ##remover self.sprite = self.spriteDano

            if self.temporizadorknockback > 10:
                self.levandoDano = False
                self.podeSerControlado = True
                self.temporizadorknockback = 0
                ##remover self.sprite = self.sprite

class ProjetilJogador:
    def __init__(self, jogador, objetos):
        self.jogador = jogador
        self.objetos = objetos

        self.largura = 32
        self.altura = 32

        self.sprite = pygame.image.load("Assets/Sprites/Cenourinha/cenoura.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        if self.jogador.olhandoParaDireita == True:
            self.direcao = 1
        else:
            self.direcao = -1
            self.sprite = pygame.transform.flip(self.sprite, True, False)

        self.rect = pygame.Rect(self.jogador.rect.x + self.direcao, self.jogador.rect.y + 16, self.largura, self.altura)

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
    def __init__(self, colisores = [], mapa = []):
        self.tamanhoTile = 64 #define a altura e largura de cada tile (porque é um quadrado)

        self.texturas = [
            '',
            pygame.transform.scale(pygame.image.load("Assets/Sprites/Mundo/grama.png"), (self.tamanhoTile, self.tamanhoTile)),
            pygame.transform.scale(pygame.image.load("Assets/Sprites/Mundo/terra.png"), (self.tamanhoTile, self.tamanhoTile)),
        ]

        self.colisores = colisores
        self.mapa = mapa

        self.superficieTilemap = pygame.Surface((len(self.mapa[0]) * self.tamanhoTile, len(self.mapa) * self.tamanhoTile))
        self.superficieTilemap.set_colorkey((0, 0, 0))

        for linha in range(len(self.mapa)):
            for coluna in range(len(self.mapa[0])):
                if self.mapa[linha][coluna] != 0:
                    self.superficieTilemap.blit(self.texturas[self.mapa[linha][coluna]], (coluna * self.tamanhoTile, linha * self.tamanhoTile))
                    self.colisores.append(pygame.Rect(coluna * self.tamanhoTile, linha * self.tamanhoTile, self.tamanhoTile, self.tamanhoTile))

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

        self.sprite = pygame.image.load("Assets/Sprites/Mundo/espinho.png")
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

        self.largura = 128
        self.altura = 128

        self.sprite = pygame.image.load("Assets/Sprites/Inimigo/andando1.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        #self.spriteDano = pygame.image.load("Aula 7 (Combate 2)/zombie dano.png")
        #self.spriteDano = pygame.transform.scale(self.spriteDano, (self.largura, self.altura))

        self.animacoes = {
            'andando': {
                'nome': 'andando',
                'sprites': [
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Inimigo/andando1.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Inimigo/andando2.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Inimigo/andando3.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Inimigo/andando4.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Inimigo/andando5.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Inimigo/andando6.png"), (self.largura, self.altura)),
                    ],
                'velocidade': 0.11
            },
            'dano': {
                'nome': 'dano',
                'sprites': [
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Inimigo/dano.png"), (self.largura, self.altura)),
                ],
                'velocidade': 0.1
            }
        }

        self.animador = Animador(self.animacoes)

        self.animador.DefinirAnimacao('andando')

        self.sprite = self.sprite

        self.indo = True
        self.amplitude = amplitude
        self.xInicial = x
        self.rect = pygame.Rect(x, y, self.largura, self.altura)

        self.levandoDano = True
        self.temporizadorDano = 0
        self.vidaMaxima = 3
        self.vidaAtual = self.vidaMaxima
        self.dano = 2

        self.morteSFX = pygame.mixer.Sound("Assets/SFX/inimigoMorte.wav")
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
        self.levandoDano = True

    def Desenhar(self, superficie):
        self.sprite = self.animador.SpriteAtual()
        if self.indo == False:
            self.sprite = pygame.transform.flip(self.sprite, True, False)
        superficie.blit(self.sprite, (self.rect.x, self.rect.y))

    def Animar(self):
        if self.levandoDano ==  True and self.animador.AnimacaoAtual() != 'dano':
            self.animador.DefinirAnimacao('dano')

        elif self.animador.AnimacaoAtual() != 'andando':
            self.animador.DefinirAnimacao('andando')

    def Atualizar(self):
        self.Movimento()
        self.Animar()
        self.animador.Atualizar()

        for objeto in self.objetos.lista:
            if isinstance(objeto, Jogador):
                if self.rect.colliderect(objeto.rect):
                    objeto.LevarDano(self.dano)

        if self.levandoDano == True:
            self.temporizadorDano += 1

            if self.temporizadorDano > 10:
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

        self.sprite = pygame.image.load("Assets/Sprites/Moeda/cenoura1.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        self.animacoes = {
            'rodando': {
                'nome': 'rodando',
                'sprites': [
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Moeda/cenoura1.png"), (self.largura, self.altura)),
                    pygame.transform.scale(pygame.image.load("Assets/Sprites/Moeda/cenoura2.png"), (self.largura, self.altura)),
                ],
                'velocidade': 0.1
            }
        }

        self.animador = Animador(self.animacoes)

        self.animador.DefinirAnimacao('rodando')

        self.yInicial = y
        self.indo = True
        self.rect = pygame.Rect(x, y, self.largura, self.altura)
        self.velocidade = 1

        self.moedaSFX = pygame.mixer.Sound("Assets/SFX/moeda.wav")
        self.moedaSFX.set_volume(0.1)

    def Desenhar(self, superficie):
        self.sprite = self.animador.SpriteAtual()
        superficie.blit(self.sprite, (self.rect.x, self.rect.y))

    def Atualizar(self):
        self.animador.Atualizar()

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

        self.coracao = pygame.image.load("Assets/Sprites/UI/coracao.png")
        self.coracao = pygame.transform.scale(self.coracao, (48, 48))

        self.moeda = pygame.image.load("Assets/Sprites/UI/cenoura1.png")
        self.moeda = pygame.transform.scale(self.moeda, (48, 48))

    def Mostrar(self, superficie):
        fonte = pygame.font.Font("Assets/Kenney Pixel Square.ttf", 32)

        for i in range(self.jogador.vidaAtual):
            superficie.blit(self.coracao, (48 + 48 * i * 1.25, 48))

        superficie.blit(self.moeda, (48, 48*3))

        textoPontos = fonte.render(str(self.jogador.pontos), True, (255, 255, 255))
        superficie.blit(textoPontos, (48*2 + 10, 48*3 - 2))

class Portal:
    def __init__(self, jogador, faseDestino, gerenciadorDeFases, x, y):
        self.jogador = jogador
        self.faseDestino = faseDestino
        self.gerenciadorDeFases = gerenciadorDeFases

        self.largura = 256
        self.altura = 64*5

        self.sprite = pygame.image.load("Assets/Sprites/Mundo/portal.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        self.rect = pygame.Rect(x, y, self.largura, self.altura)

    def Desenhar(self, superficie):
        superficie.blit(self.sprite, (self.rect.x, self.rect.y))

    def Atualizar(self):
        if self.rect.colliderect(self.jogador.rect):
            self.gerenciadorDeFases.CarregarFase(self.faseDestino)

class Fase1:
    def __init__(self, gerenciadorDeFases):
        self.mundo = pygame.surface.Surface((64*100, 64*50))
        self.mixer = pygame.mixer

        self.gerenciadorDeFases = gerenciadorDeFases

        self.mixer.music.load("Assets/BGM/musica1.mp3")
        self.mixer.music.set_volume(0.1)
        self.mixer.music.play(-1)

        self.gravidade = 0.9
        self.colisores = []
        self.objetos = Grupo()

        self.jogador = Jogador(self.gravidade, self.colisores, self.mundo, self.objetos)
        self.objetos.Adicionar(self.jogador)

        mapa = [
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

        self.tilemap = Tilemap(self.colisores, mapa)
        self.objetos.Adicionar(self.tilemap)

        self.espinhos = [
            Espinho(self.jogador, 512, 64*14),
            Espinho(self.jogador, 576, 64*14),
            Espinho(self.jogador, 64*19, 64*14),
            Espinho(self.jogador, 64*20, 64*14),
            Espinho(self.jogador, 64*21, 64*14),
            Espinho(self.jogador, 64*26, 64*14),
            Espinho(self.jogador, 64*27, 64*14),
            Espinho(self.jogador, 64*28, 64*14),
        ]

        for espinho in self.espinhos:
            self.objetos.Adicionar(espinho)

        self.inimigo1 = InimigoPatrulhador(256, self.objetos, 64*8, 64*13)
        self.objetos.Adicionar(self.inimigo1)

        self.moeda1 = Moeda(self.objetos, 64*20, 64*8)
        self.objetos.Adicionar(self.moeda1)

        self.moeda2 = Moeda(self.objetos, 64*27, 64*8)
        self.objetos.Adicionar(self.moeda2)

        self.camera = CameraQueSegue(self.jogador, self.mundo)
        self.objetos.Adicionar(self.camera)

        self.hud = HUD(self.jogador)
        self.objetos.Adicionar(self.hud)

        self.portal = Portal(self.jogador, "fase2", self.gerenciadorDeFases, 64*35, 64*7)
        self.objetos.Adicionar(self.portal)

    def Atualizar(self):
        self.objetos.Atualizar()

    def Desenhar(self, tela):
        tela.fill((0, 0, 0))
        self.mundo.fill((135, 206, 250))

        self.objetos.Desenhar(self.mundo)

        self.camera.Mostrar(tela)
        self.hud.Mostrar(tela)

class Fase2:
    def __init__(self, gerenciadorDeFases):
        self.mundo = pygame.surface.Surface((64*100, 64*50))
        self.mixer = pygame.mixer

        self.gerenciadorDeFases = gerenciadorDeFases

        self.mixer.music.load("Assets/BGM/musica1.mp3")
        self.mixer.music.set_volume(0.1)
        self.mixer.music.play(-1)

        self.gravidade = 0.9
        self.colisores = []
        self.objetos = Grupo()

        self.jogador = Jogador(self.gravidade, self.colisores, self.mundo, self.objetos)
        self.objetos.Adicionar(self.jogador)

        mapa = [
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
            [2,2,2,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1],
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

        self.tilemap = Tilemap(self.colisores, mapa)
        self.objetos.Adicionar(self.tilemap)

        self.espinhos = [
            Espinho(self.jogador, 512, 64*14),
            Espinho(self.jogador, 576, 64*14),
            Espinho(self.jogador, 64*19, 64*14),
            Espinho(self.jogador, 64*20, 64*14),
            Espinho(self.jogador, 64*21, 64*14),
            Espinho(self.jogador, 64*26, 64*14),
            Espinho(self.jogador, 64*27, 64*14),
            Espinho(self.jogador, 64*28, 64*14),
        ]

        for espinho in self.espinhos:
            self.objetos.Adicionar(espinho)

        self.inimigo1 = InimigoPatrulhador(256, self.objetos, 64*8, 64*13)
        self.objetos.Adicionar(self.inimigo1)

        self.moeda1 = Moeda(self.objetos, 64*20, 64*8)
        self.objetos.Adicionar(self.moeda1)

        self.moeda2 = Moeda(self.objetos, 64*27, 64*8)
        self.objetos.Adicionar(self.moeda2)

        self.camera = CameraQueSegue(self.jogador, self.mundo)
        self.objetos.Adicionar(self.camera)

        self.hud = HUD(self.jogador)
        self.objetos.Adicionar(self.hud)

        self.portal = Portal(self.jogador, "menu", self.gerenciadorDeFases, 64*35, 64*7)
        self.objetos.Adicionar(self.portal)

    def Atualizar(self):
        self.objetos.Atualizar()

    def Desenhar(self, tela):
        tela.fill((0, 0, 0))
        self.mundo.fill((135, 206, 250))

        self.objetos.Desenhar(self.mundo)

        self.camera.Mostrar(tela)
        self.hud.Mostrar(tela)

class MenuInicial:
    def __init__(self, gerenciadorDeFases):
        self.gerenciadorDeFases = gerenciadorDeFases

        self.fundo = pygame.image.load("Assets/Sprites/UI/background.png")
        self.fundo = pygame.transform.scale(self.fundo, (1280, 720))

        self.titulo = pygame.image.load("Assets/Sprites/UI/title.png")
        self.titulo = pygame.transform.scale(self.titulo, (512+256+128, 256+128+64))

        self.grupoObjetos = Grupo()

        self.fonte = pygame.font.Font("Assets/Kenney Pixel Square.ttf", 32)
        self.texto = self.fonte.render("Pressione ESPAÇO para começar", True, (255, 255, 255))

        #self.botaoIniciar = BotaoUI(640-128, 360, 256, 64, (0, 255, 0), "Iniciar")
        self.botaoIniciar = BotaoUI(640-128, 360, 256, 64, (100, 255, 100), (0, 255, 0), "Iniciar", (255, 255, 255), self.Iniciar)
        self.grupoObjetos.Adicionar(self.botaoIniciar)
        
        #self.botaoSair = BotaoUI(640-128, 360+64+32, 256, 64, (0, 255, 0), "Sair")
        self.botaoSair = BotaoUI(640-128, 360+64+32, 256, 64, (100, 255, 100), (0, 255, 0), "Sair", (255, 255, 255), self.Sair)
        self.grupoObjetos.Adicionar(self.botaoSair)

    def Iniciar(self):
        self.gerenciadorDeFases.CarregarFase("fase1")

    def Sair(self):
        #global rodando
        #rodando = False
        pygame.quit()
        sys.exit()

    def Atualizar(self):
        self.grupoObjetos.Atualizar()

    def Desenhar(self, tela):
        tela.fill((0, 0, 0))
        
        tela.blit(self.fundo, (0, 0))
        tela.blit(self.titulo, (640-256-128-64, 0))

        self.grupoObjetos.Desenhar(tela)

class BotaoUI:
    def __init__(self, x, y, largura, altura, corNormal, corSelecionado, texto, corTexto, acao):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = corNormal
        self.corNormal = corNormal
        self.corSelecionado = corSelecionado
        self.texto = texto
        self.corTexto = corTexto
        self.acao = acao

    def Clicar(self):
        self.acao()
        pass

    def Desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)
        fonte = pygame.font.Font("Assets/Kenney Pixel Square.ttf", 32)
        texto = fonte.render(self.texto, True, (255, 255, 255))
        tela.blit(texto, (self.rect.x + self.rect.width/2 - texto.get_width()/2, self.rect.y + self.rect.height/2 - texto.get_height()/2))

    def Atualizar(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.x < mouse[0] < self.rect.x + self.rect.width and self.rect.y < mouse[1] < self.rect.y + self.rect.height:
            self.cor = self.corSelecionado

            if click[0] == 1:
                self.Clicar()

        else:
            self.cor = self.corNormal

class GerenciadorDeFases:
    def __init__(self, faseInicial):
        self.faseAtual = self.CarregarFase(faseInicial)

    def CarregarFase(self, fase):
        
        if fase == "menu":
            self.faseAtual = MenuInicial(self)

        elif fase == "fase1":
            self.faseAtual = Fase1(self)

        elif fase == "fase2":
            self.faseAtual = Fase2(self)

        return self.faseAtual

class Animador:
    def __init__(self, animacoes):
        self.animacoes = animacoes
        self.animacaoAtual = None
        self.velocidadeAtual = 0
        self.spritesAtuais = []
        self.indice = 0

    def DefinirAnimacao(self, nome):
        self.animacaoAtual = self.animacoes[nome]
        self.spritesAtuais = self.animacaoAtual['sprites']
        self.velocidadeAtual = self.animacaoAtual['velocidade']
        self.indice = 0

    def Atualizar(self):
        self.indice += self.velocidadeAtual

        if self.indice >= len(self.spritesAtuais):
            self.indice = 0
            
    def SpriteAtual(self):
        return self.spritesAtuais[int(self.indice)]
    
    def AnimacaoAtual(self):
        return self.animacaoAtual['nome']

rodando = True
clock = pygame.time.Clock()

gerenciadorDeFases = GerenciadorDeFases("menu")

while rodando:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    gerenciadorDeFases.faseAtual.Atualizar()
    gerenciadorDeFases.faseAtual.Desenhar(tela)

    pygame.display.update()