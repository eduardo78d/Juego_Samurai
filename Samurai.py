# -*- coding: utf-8 -*-
#Nombre 

import pygame
from pygame.locals import*
import os
import sys
from random import randint


width = 1190
height = 635
Nivel = 0
ListaEnemigos=[]


class Menu:
    def __init__(self, opciones):
        self.opciones = opciones
        self.font = pygame.font.Font('dejavu.ttf', 20)
        self.seleccionado = 0
        self.total = len(self.opciones)
        self.mantiene_pulsado = False

    def actualizar(self):
        """Altera el valor de 'self.seleccionado' con los direccionales."""

        k = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if k[K_UP]:
                self.seleccionado -= 1
            elif k[K_DOWN]:
                self.seleccionado += 1
            elif k[K_RETURN]:

                # Invoca a la función asociada a la opción.
                titulo, funcion = self.opciones[self.seleccionado]
                print "Selecciona la opción '%s'." %(titulo)
                funcion()

        # procura que el cursor esté entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > self.total - 1:
            self.seleccionado = self.total - 1

        # indica si el usuario mantiene pulsada alguna tecla.
        self.mantiene_pulsado = k[K_UP] or k[K_DOWN] or k[K_RETURN]


    def imprimir(self, screen):
        """Imprime sobre 'screen' el texto de cada opción del menú."""

        total = self.total
        indice = 0
        altura_de_opcion = 30
        x = 105
        y = 105
        
        for (titulo, funcion) in self.opciones:
            if indice == self.seleccionado:
                color = (200, 0, 0)
            else:
                color = (0, 0, 0)

            imagen = self.font.render(titulo, 1, color)
            posicion = (x, y + altura_de_opcion * indice)
            indice += 1
            screen.blit(imagen, posicion)

		
class Fondo(pygame.sprite.Sprite):
	def __init__(self):
		self.imagenFondo = pygame.image.load("imagenes/fondo.png")
		self.rect = self.imagenFondo.get_rect()

	def update(self,Pantalla,x,y):
		#self.rect.move_ip(-x,-y)
		Pantalla.blit(self.imagenFondo, self.rect)

class Jugador(pygame.sprite.Sprite):
	"Cargando a Jugador"
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.img1 = pygame.image.load("imagenes/samurai1.png")
		self.img2  = pygame.image.load("imagenes/samurai2.png")
		self.img3  = pygame.image.load("imagenes/samurai1_1.png")
		self.img4  = pygame.image.load("imagenes/samurai2_1.png")
		self.imgAtque = pygame.image.load("imagenes/samurai3.png")
		self.imgAtque2 = pygame.image.load("imagenes/samurai3_1.png")
		self.imgAtque3 = pygame.image.load("imagenes/samurai4.png")
		self.imgAtque4 = pygame.image.load("imagenes/samurai4_1.png")

		self.ListaImagenes = [[self.img1, self.img2,self.imgAtque, self.imgAtque3],[self.img3, self.img4,self.imgAtque2,self.imgAtque4]]
		self.imagenActual = 0
		self.imagenSamurai= self.ListaImagenes[self.imagenActual][0]
		self.rect = self.imagenSamurai.get_rect()
		#self.rect.top,self.rect.left = 100,150
		self.mask=pygame.mask.from_surface(self.imagenSamurai)
		self.Orientacion = 0

		self.Movimiento = False
		self.Ataque = False
		self.ListaEstrellas= []
		self.vida= 100
		self.proyectil = False

	def mover(self,x,y):
		self.rect.move_ip(x,y)

	def Dibujo(self,superficie, Orientacion, actual):
		if self.vida >0:
			self.imagen = self.ListaImagenes[Orientacion][actual]
			superficie.blit(self.imagen,self.rect)

	def update(self, superficie, x,y, contador):
		if x == 0 and y == 0:self.Movimiento= False
		else: self.Movimiento = True

		if contador== 1 and self.Movimiento== True:
			self.NextImage()
		
		if x>0: self.Orientacion= 0
		elif x<0: self.Orientacion= 1

		if self.Ataque== True:
			aux,auy = self.rect.top, self.rect.left
			self.rect = self.imagenSamurai.get_rect()
			self.rect.top , self.rect.left = aux,auy
			self.Dibujo(superficie, self.Orientacion, 2)
			self.Ataque= False

		elif self.proyectil== True:
			self.imagenActual= 3
			self.Dibujo(superficie, self.Orientacion, self.imagenActual)
			self.NextImage()
			self.proyectil=False


		self.Dibujo(superficie, self.Orientacion, self.imagenActual)

		#x=0
		#y=0
		self.mover(x,y)
	
	def NextImage(self):	
		self.imagenActual +=1
		if self.imagenActual > len(self.ListaImagenes)-1:
			self.imagenActual=0

	def Disparos(self,x,y, Orientacion):
		EstrellaSamuari = Arma()
		EstrellaSamuari.coordenadas(x,y, Orientacion)
		self.ListaEstrellas.append(EstrellaSamuari)


	def ColisioneEnemigo(self, Enemigo):
		self.rectAux = self.imagenSamurai.get_rect()
		if self.rectAux.colliderect(Enemigo):
			return True

class Enemigo(pygame.sprite.Sprite):
	def __init__(self,x,y,v):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenVolador = pygame.image.load("imagenes/Enemigo1.png")
		self.rect = self.ImagenVolador.get_rect()
		self.rect.top, self.rect.left = y,x
		print self.rect
		self.posy= self.rect.top
		self.posx= self.rect.left
		self.mask=pygame.mask.from_surface(self.ImagenVolador)
		self.vida = 50
		self.Orientacion = 0
		self.Arriba = True
		self.velocidad = v
		self.VIVO = True

	def update(self, superficie):
		if self.VIVO == True:
			if self.Arriba == True:
				if self.rect.top >0 :
					self.rect.top = self.rect.top -self.velocidad
				if self.rect.top < 10:
					self.Arriba= False
			elif self.Arriba == False:
				if self.rect.top >=0:
					self.rect.top = self.rect.top+self.velocidad
				if self.rect.top >550:
					self.Arriba = True
		self.posy = self.rect.top
		self.Dibujar(superficie)

	def Dibujar(self, superficie):
			superficie.blit(self.ImagenVolador,self.rect)

	def Get_Rect(self):
		self.rectAux = self.ImagenVolador.get_rect()
		return self.rectAux

class Arma(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.Estrella = pygame.image.load("imagenes/Estrella.png")
		self.rect = self.Estrella.get_rect()
		self.rect.top, self.rect.left = 30,30
		self.posy= 100
		self.posx= 100
		self.mask=pygame.mask.from_surface(self.Estrella)
		self.Orientacion= 0
		self.velocidadDisparo = 20

	def update(self, superficie):
		if self.Orientacion ==1:
			self.posx = self.posx - self.velocidadDisparo
		else:
			self.posx = self.posx + self.velocidadDisparo
		self.Dibujar(superficie)

	def Dibujar(self,superficie):

		superficie.blit(self.Estrella, (self.posx, self.posy))

	def coordenadas(self, px, py, Orientacion):
		self.posy = py
		self.posx = px
		self.Orientacion =Orientacion

def Colisiones(Jugador, Enemigo):
	if pygame.sprite.collide_rect(Jugador,Enemigo):
	#if Jugador.rect.colliderect(Enemigo.rect):
		return True



def juego():
	pygame.init()
	Pantalla= pygame.display.set_mode((width,height),0,0)
	pygame.display.set_caption("Samuarai")

	fondo = Fondo()
	Nivel = 0
	Samuarai = Jugador()


	velocidad =8
	reloj = pygame.time.Clock()
	Jugar = True
	vx, vy = 0,0
	Estrella = Arma()
	contador = 0


	ListaArmas= []
	
	siguienteNivel = Nivel
	sonidoAtaque = pygame.mixer.Sound("sonido/Nmoes1.mid")

	while Jugar:
		contador +=1
		if contador >1:
			contador=0

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					vx=-velocidad
				if event.key == pygame.K_RIGHT:
					vx= velocidad
				if event.key== pygame.K_UP:
					vy -=velocidad
				if event.key == pygame.K_DOWN:
					vy= velocidad

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					vx=0
				if event.key == pygame.K_RIGHT:
					vx= 0
				if event.key== pygame.K_UP:
					vy =0
				if event.key == pygame.K_DOWN:
					vy= 0
				if event.key == pygame.K_s:
					Samuarai.Ataque= True
					sonidoAtaque.play()
					for Enemigos in ListaEnemigos:
						if Colisiones(Samuarai, Enemigos):
							Enemigos.vida -=10
					if Samuarai.Orientacion ==1:
						Samuarai.Ataque= False

				if event.key == pygame.K_d:
					x,y  = Samuarai.rect.center
					if Samuarai.Orientacion ==0:
						Samuarai.proyectil= True
					Samuarai.Disparos(x,y, Samuarai.Orientacion)
					ListaArmas = Samuarai.ListaEstrellas

		reloj.tick(20)
		fondo.update(Pantalla,vx,vy)
		Samuarai.update(Pantalla,vx,vy, contador )
		
		#Musica de niveles y enemigos de niveles
		if siguienteNivel== Nivel:
			Sonidos()
			print "Entro "
			CreadorEnemigos()
			siguienteNivel= siguienteNivel+1

		for Enemigos in ListaEnemigos:
			if Colisiones(Samuarai, Enemigos):
				print "Dameged"

		if len(ListaEnemigos)>0:
			for x in ListaEnemigos:
				if x.vida >0:
					x.update(Pantalla)
				else:
					ListaEnemigos.remove(x)
		else:
			Nivel= Nivel+1

		if len(ListaArmas) >0:
			for x in ListaArmas:
				x.update(Pantalla)
				if(x.posx< 0 or x.posx >3000):
					ListaArmas.remove(x)	
					print "Eliminado"
				else:
					if len(ListaEnemigos)>0:
						for e in ListaEnemigos:
							if Colisiones(x,e):
								ListaArmas.remove(x)

		pygame.display.update()

	pygame.quit()

###############################################

def Sonidos():
	if Nivel==0:
		IntroGoku = os.path.join("sonido", "juan.mid")
		pygame.mixer.music.load(IntroGoku)
	elif Nivel==1:
		IntroGoku = os.path.join("sonido", "juan.mid")
		pygame.mixer.music.load(IntroGoku)

	pygame.mixer.music.play(2)

def CreadorEnemigos():
	if Nivel ==0 :
		for w in range(2):
			x = randint(400,900)
			v= randint(2,10)
			y = randint(2,800)
			EnemigoVolador = Enemigo(x,y,v)
			ListaEnemigos.append(EnemigoVolador)
	elif Nivel== 1:
			for w in range(4):
				x = randint(400,900)
				v= randint(2,10)
				y = randint(2,800)
				EnemigoVolador = Enemigo(x,y,v)
				ListaEnemigos.append(EnemigoVolador)

def comenzar_nuevo_juego():
    juego()

def mostrar_opciones():
    pass

def creditos():
    salir = False
    opciones = [
        ("Regresar", MenuPrincipal),
        ]

    pygame.font.init()
    screen = pygame.display.set_mode((320, 240))
    fondo = pygame.image.load("imagenes/fondo.png")
    menu = Menu(opciones)
    while not salir:

        for e in pygame.event.get():
            if e.type == QUIT:
                salir = True

        screen.blit(fondo, (0, 0))
        menu.actualizar()
        menu.imprimir(screen)

        pygame.display.flip()
        pygame.time.delay(10)


def salir_del_programa():
    import sys
    sys.exit(0)

def MenuPrincipal():    
    salir = False
    opciones = [
        ("Jugar", comenzar_nuevo_juego),
        ("Opciones", mostrar_opciones),
        ("Creditos", creditos),
        ("Salir", salir_del_programa)
        ]

    pygame.font.init()
    screen = pygame.display.set_mode((320, 240))
    fondo = pygame.image.load("imagenes/fondo.png")
    menu = Menu(opciones)

    while not salir:

        for e in pygame.event.get():
            if e.type == QUIT:
                salir = True

        screen.blit(fondo, (0, 0))
        menu.actualizar()
        menu.imprimir(screen)

        pygame.display.flip()
        pygame.time.delay(10)

MenuPrincipal()