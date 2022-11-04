import pygame
import random

# CLASSE RETANGULOS
class Recs(object):
  def __init__(self, num_inicial):
    self.list = []
    for x in range(num_inicial):
      left_random = random.randrange(2, 560)
      top_random = random.randrange(-580, -10)
      width = random.randrange(10, 30)
      height = random.randrange(15, 30)
      self.list.append(pygame.Rect(left_random, top_random, width, height))

  def mover(self):
    for retangulo in self.list:
      retangulo.move_ip(0, 2)

  def cor(self, superficie):
    for retangulo in self.list:
      pygame.draw.rect(superficie, (165, 214, 254), retangulo)

  def recriar(self):
    for x in range(len(self.list)):
      if self.list[x].top > 481:
        left_random = random.randrange(2, 560)
        top_random = random.randrange(-580, -10)
        width = random.randrange(10, 30)
        height = random.randrange(15, 30)
        self.list[x] = (pygame.Rect(left_random, top_random, width, height))

# CLASSE JOGADOR
class Player(pygame.sprite.Sprite):
  def __init__(self, imagem):
    self.imagem = imagem
    self.rect = self.imagem.get_rect()
    self.rect.top, self.rect.left = (200, 200)

  def mover(self, vx, vy):
    self.rect.move_ip(vx, vy)
    
  def update(self, superficie):
    superficie.blit(self.imagem, self.rect)

def colisao(player, recs):
  for rec in recs.list:
    if player.rect.colliderect(rec):
      return True
  return False
  
def main():
  import pygame
  
# -- DECLARAÇÃO DAS VARIAVEIS (OBJETOS) --
  pygame.init()
  tela = pygame.display.set_mode((480, 300))
  sair = False
  relogio = pygame.time.Clock()
# ----- IMAGENS -----
  img_nave = pygame.image.load("img/nave.png").convert_alpha()
  img_background = pygame.image.load("img/background.png").convert_alpha()
  img_explosao = pygame.image.load("img/explosao.png").convert_alpha()
# ----- AUDIOS -----
  pygame.mixer.music.load("audio/musica.mp3")
  pygame.mixer.music.play(3)
  som_explosao = pygame.mixer.Sound("audio/explosao2.wav")
  som_movimento = pygame.mixer.Sound("audio/som2.wav")
# ----- TEXTO -----
  texto = pygame.font.SysFont("Arial", 15, True, False)
  jogador = Player(img_nave)

  vx, vy = 0, 0
  velocidade = 10
  left_press, right_press, up_press, down_press = False, False, False, False

  ret = Recs(30)
  colidiu = False

  while sair != True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sair = True

# --- MOVIMENTAÇÃO ---
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          left_press = True
          vx = -velocidade
        if event.key == pygame.K_RIGHT:
          right_press = True
          vx = velocidade
        if event.key == pygame.K_UP:
          up_press = True
          vy = -velocidade
          som_movimento.play()
        if event.key == pygame.K_DOWN:
          down_press = True
          vy = velocidade

      if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
          left_press = False
          if right_press:
            vx = velocidade
          else:  
            vx = 0
        if event.key == pygame.K_RIGHT:
          right_press = False
          if left_press:
            vx = -velocidade
          else:  
            vx = 0
        if event.key == pygame.K_UP:
          up_press = False
          if down_press:
            vy = -velocidade
          else:  
            vy = 0
        if event.key == pygame.K_DOWN:
          down_press = False
          if up_press:
            vy = velocidade
          else:  
            vy = 0

# ----- COLISÃO -----
    if colisao(jogador, ret):
      colidiu = True
      jogador.imagem = img_explosao
      pygame.mixer.music.stop()
      som_explosao.play()
      
    if colidiu == False:
      ret.mover()
      jogador.mover(vx, vy)
      tela.blit(img_background, (0,0))
      segundos = pygame.time.get_ticks()/1000
      segundos = str(segundos)
      contador = texto.render("Pontuação: {}".format(segundos), segundos, (255, 255, 255), 0)
    
    relogio.tick(20)
    tela.blit(contador, (300, 10))
    ret.cor(tela)
    ret.recriar()
    jogador.update(tela)
    
    pygame.display.update()
    
  pygame.quit()

main()