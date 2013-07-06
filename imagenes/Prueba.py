# -*- coding: cp1252 -*-
import pygame, sys
from pygame.locals import *
#defino unas variables globales para el ancho y el alto
Ancho = 1000
Alto = 500

#se crea la clase para la pokebola, no cambia para nada 
class Pokebola( pygame.sprite.Sprite ):  
    def __init__(self, pos_i_x, pos_i_y ): 
        pygame.sprite.Sprite.__init__(self) 
       
        self.image = pygame.image.load("samurai2.png")
        self.rect = self.image.get_rect() 
        self.rect.center = (pos_i_x, pos_i_y) 
        # retire lo del trainer por que no estaba definido dentro de la clase
        self.dx = 0   
        self.dy = -3 

    def update(self):
        self.rect.move_ip((self.dx, self.dy)) 
        if self.rect.y < 0 : 
            self.kill() 

#creo una clase para el personaje principal 
#que también es un sprite...
class Trainer( pygame.sprite.Sprite ):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Estrella.png")
        self.rect = self.image.get_rect()
        self.rect.center = (1000/2,500/2 ) #aquí ,lo colocamos en una posición inicial
        #la ventaja de utilizar rect, es que nos permite, como creo intentaste, colocar
        #la imagen con el centro como lo ponemos
        #además, resulta redundante preguntar el alto y el ancho si sabemos que es de 1000 X 500 
        self.dx = 10
    def update(self):
        #es mucho mejor dejar que el personaje se actualice a si mismo 
        posx, posy = self.rect.center #creamos dos variables para la posición
        for event in pygame.event.get():
            #en esta parte modificamos la posición
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    posx -= self.dx 
                if event.key == K_RIGHT:
                    posx += self.dx
        self.rect.center = (posx, posy) #y aquí lo aplicamos 

def main(): #creo una función principal
    pygame.init() #inicialzo a pygame
    pantalla = pygame.display.set_mode( (Ancho,Alto) ) #creo la pantalla
    pygame.mouse.set_visible(False) #no digo que este mal el "0", solo que así se entiende más 
    bg = pygame.image.load("fondo.png") #
    #ahora, creamos algo que te parecerá nuevo:
    # "un grupo de sprites"
    sprites = pygame.sprite.RenderClear()
    #y añadimos a nuestro personaje al grupo
    trainer = Trainer()
    sprites.add( trainer )
    jugar = True
    while jugar:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jugar = False; pygame.quit() #el punto y coma permite poner sentencias en la misma linea
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        #ahora, cuando presiones, se agregara una bala
                        x, y = trainer.rect.center #tomamos la posición inicial, que sera la misma
                        #que la del personaje
                        pokebola = Pokebola(x,y) #lo pasamos como argumento para inicializarla 
                        sprites.add(pokebola) #y la añadimos al código
            pantalla.fill((250,250,250))
            pantalla.blit(bg, (0,0) )
            sprites.draw(pantalla) #esto dibuja TODOS los sprites en el grupo
            sprites.update() #y esto actualiza TODOS los sprites en el grupo
            #esa es la gran ventaja de trabajar con esprites
            pygame.display.update()
main()