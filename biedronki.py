#!/usr/bin/python3
# Copyrights (C) 2020 Mateusz Bondarczuk
# Napisane przy pomocy podręcznika "PYTHON Kurs Programowania Na Prostych Przykładach" Biblioteczka Komputer Świat

import pygame
import os
import random
import threading

pygame.init()

#rozmiar okna gry
szer = 600
wys = 600
#lista wartości kierunku ruchu biedronek
#wektory = [-10, 0, 10]
coPokazuje = "menu"
punkty = 0.0
vx, vy = 0, 0
iloscBiedronek = 10



screen = pygame.display.set_mode((szer,wys))

def napisz(tekst, x, y, rozmiar) :
    cz = pygame.font.SysFont("Conacry", rozmiar)
    rend = cz.render(tekst, 1, (255,100,100))
    x = (szer - rend.get_rect().width)/2
#   y = (wys - rend.get_rect().height)/2
    screen.blit(rend, (x,y))

def dodPunkt():
    global punkty
    if coPokazuje == "gramy" :
        punkty += 0.1
def zerPunkty():
    global punkty
    punkty = 0

class Biedronka() :
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.szerB = 32
        self.wysB = 32
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerB, self.wysB)
        self.grafika = pygame.image.load(os.path.join('bied.png'))
    def rysuj(self):
        screen.blit(self.grafika, (self.x, self.y))
    def ruch(self):
        self.x += self.vx
        self.y += self.vy
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerB, self.wysB)
    def czyZezarla(self, robal):
        if self.ksztalt.colliderect(robal):
            return True
        else:
            return False
        

class Mszyca():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.szerM = 32
        self.wysM = 32
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerM, self.wysM)
        self.grafika = pygame.image.load(os.path.join('mszyca.png'))
    def rysuj(self):
        screen.blit(self.grafika, (self.x, self.y))
    def ruch(self, vx, vy):
        self.x += vx
        self.y += vy
        self.ksztalt = pygame.Rect(self.x, self.y, self.szerM, self.wysM)


#stworzmy biedry
biedry = []
def stworzBiedry():
    global biedry
    for i in range(iloscBiedronek):
        #bx = random.randint(0, 568)
        #by = random.randint(0, 568)
        # tworzy biedronki w danej pozycji na ekranie(bx,by) i poruszające się w jednym z 8 kierunków(np. 10,10 lub 10,0)
        #biedra = Biedronka(bx, by, random.choice(wektory), random.choice(wektory))
        biedra = Biedronka(random.randint(0, 568), random.randint(0, 568), random.randint(-10, 10), random.randint(-10, 10))
        # eliminacja biedronek, które stoja w miejscu
        while biedra.vx == 0 and biedra.vy == 0 :
            #biedra = Biedronka(bx, by, random.choice(wektory), random.choice(wektory))
            #biedra = Biedronka(bx, by, random.randint(-10, 10), random.randint(-10, 10))
            biedra = Biedronka(random.randint(0, 568), random.randint(0, 568), random.randint(-10, 10), random.randint(-10, 10))
        biedry.append(biedra)

stworzBiedry()

while True:
    dodPunkt()
    #reakcje na naciśnięcie klawiszy i ikon w oknie gry
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()
        #ruch mszycy
        if event.type == pygame.KEYDOWN :
            #ruch w górę
            if event.key == pygame.K_UP :
                vx = 0
                vy = -10
            #ruch w dół
            elif event.key == pygame.K_DOWN :
                vx = 0
                vy = 10
            #ruch w lewo
            elif event.key == pygame.K_LEFT :
                vx = -10
                vy = 0
            #ruch w prawo
            elif event.key == pygame.K_RIGHT :
                vx = 10
                vy = 0
            elif event.key == pygame.K_ESCAPE :
                pygame.quit()
                quit()
            elif event.key == pygame.K_SPACE :
                if coPokazuje != "gramy" :
                    # tworzymy nieruchomą mszyce w losowym miejscu na planszy
                    mx = random.randint(0, 568)
                    my = random.randint(0, 568)
                    m = Mszyca(mx, my)
                    vx, vy = 0, 0

                    coPokazuje = "gramy"
                    zerPunkty()
                    #usun stare biedry
                    biedry = []
                    #utwórz nowe biedry
                    stworzBiedry()



    screen.fill((0,128,0))
    if coPokazuje == "menu" :
        napisz("Naciśnij spację aby rozpocząć.", 20, 300, 36)
        grafika = pygame.image.load(os.path.join("bied.png"))
        for i in range(5):
            x = random.randint(100, 500)
            y = random.randint(100, 200)
            screen.blit(grafika, (x, y))
        pygame.time.wait(500)
    elif coPokazuje == "gramy":
        
        #narysuj biedry na planszy i wpraw je w ruch
        for b in biedry:
            b.rysuj()
            b.ruch()
            
        #spraw aby odbiły się od krawędzi planszy
        for b in biedry:
            #odbicie od lewej i prawej ściany
            if b.x <= 0 or (b.x + b.szerB) >= szer :
                b.vx = b.vx * -1
            #odbicie od górnej i dolnej ściany
            elif b.y <= 0 or (b.y + b.wysB) >= wys :
                b.vy = b.vy * -1

        # wpraw ją w ruch
        m.ruch(vx, vy)
        #narysuj mszyce na ekranie
        m.rysuj()

        #odbicie mszycy od lewej i prawej ściany
        if m.x <= 0 or (m.x + m.szerM) >= szer :
            vx = vx * -1
        #odbicie mszycy od górnej i dolnej ściany
        elif m.y <= 0 or (m.y + m.wysM) >= wys :
            vy = vy * -1

        # jak biedra zdeży się z mszycą
        for b in biedry :
            if b.czyZezarla(m.ksztalt) :
                coPokazuje = "koniec"

        napisz("PUNKTY: " + str(round(punkty)), 100, 50, 32)
        #szybkosc poruszania sie obiektów
        pygame.time.wait(80)

    elif coPokazuje == "koniec" :
        napisz("KONIEC GRY!!!", 100, 150, 56)
        napisz("PUNKTY: "+str(round(punkty)), 100, 350, 32)
        napisz("naciśnij spację aby zagrać jeszcze raz ", 100, 400, 28)
        napisz("lub ESC aby zakończyć grę ", 100, 430, 28)

    #odświeżenie ekranu
    pygame.display.update()
