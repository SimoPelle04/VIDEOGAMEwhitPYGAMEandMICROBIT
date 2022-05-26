import random
from turtle import delay
from matplotlib import transforms
import numpy as np
import sys
import serial, time
import pygame as pg
import threading, queue
import time
from pygame.math import Vector2

#var globali
pg.init()
accellerazioni = queue.Queue()
bussola = queue.Queue()
spari= queue.Queue()
listaMostri = []
listaColpi = []

class Read_Microbit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
      
    def terminate(self):
        self._running = False
        
    def run(self):
        #serial config
        port = "COM16"
        s = serial.Serial(port)
        s.baudrate = 115200
        while self._running:
            data = s.readline().decode() 
            dati = data.split(" ")
            #print(dati)
            acc = float(dati[0]) 
            comp = float(dati[1])
            sparo = dati[2][0:5]
            accellerazioni.put(acc)
            bussola.put(comp)
            spari.put(sparo)
            time.sleep(0.01)

class proiettile:
    def __init__(self,x,y,rotazione):
        self.posizione = Vector2([x,y])
        self.velocita = 15
        self.angle = rotazione
        self.rotazione = Vector2([0,-1])
        self.rotazione = self.rotazione.rotate(rotazione)
        self.proiettile = self
        self.proiettilerect = self
    def create(self,screen):
        self.proiettile = pg.image.load("./proiettile.gif")
        self.proiettile = pg.transform.scale(self.proiettile,(25,50))
        self.proiettile = pg.transform.rotate(self.proiettile,self.angle)
        self.proiettilerect = self.proiettile.get_rect()
        self.proiettilerect.center= self.posizione
        screen.blit(self.proiettile,self.proiettilerect)
        pg.display.flip()

class mostro:
    def __init__(self, tipo,x):
        self.tipo = tipo
        self.x = x
        self.y = -10
        self.velocita = 0
        self.mostro = self
        self.mostrorect = self

    def create(self,screen):
        if(self.tipo == 1):
            self.mostro = pg.image.load("./mostro1.gif")
            self.velocita = 1
            
        elif(self.tipo == 2):
            self.mostro = pg.image.load("./mostro2.gif") 
            self.velocita = 2
        else:
            self.mostro = pg.image.load("./mostro3.gif") 
            self.velocita = 3
        
        self.mostro = pg.transform.scale(self.mostro,(100,150))
        self.mostrorect = self.mostro.get_rect()
        self.mostrorect.centerx = self.x
        self.mostrorect.centery = self.y
        screen.blit(self.mostro,self.mostrorect)

def menu():
    width = 1200
    height = 800
    screen = pg.display.set_mode((width, height))

    menu = pg.image.load("./menu.gif")
    menu = pg.transform.scale(menu,(1200,800))
    menurect = menu.get_rect()
    menurect.centerx = width//2
    menurect.centery = height//2
    screen.blit(menu,menurect)
    pg.display.update()
    start = spari.get()
    spari.task_done()
    while (start == "False"):
        start = spari.get()
        spari.task_done()
    return start

def GameOver(punteggio): 
    width = 1200
    height = 800
    screen = pg.display.set_mode((width, height))
    
    menu = pg.image.load("./gameover.gif")
    menu = pg.transform.scale(menu,(1200,800))
    menurect = menu.get_rect()
    menurect.centerx = width//2
    menurect.centery = height//2
    
    testoHaiPerso = "HAI PERSO"
    testoPunteggio = "PUNTEGGIO:" + str(punteggio)

    screen.blit(menu,menurect)
    testoHaiPerso = scriviTesto(testoHaiPerso, 'freesansbold.ttf', 70, (255, 255, 0),[width//2,height//2],screen)
    testoPunteggio = scriviTesto(testoPunteggio, 'freesansbold.ttf', 45, (255, 255, 0),[width//2,650],screen)
    pg.display.update()
    time.sleep(10)

def stampaVite(nVite,screen):
    vita = pg.image.load("./vite.gif")
    vita = pg.transform.scale(vita,[30,45])
    vita1rect = vita.get_rect()
    vita2rect = vita.get_rect()
    vita3rect = vita.get_rect()
    vita1rect.centerx = 25
    vita1rect.centery = 25
    vita2rect.centerx = 50
    vita2rect.centery = 25
    vita3rect.centerx = 75
    vita3rect.centery = 25
    if(nVite == 3):
        screen.blit(vita,vita1rect)
        screen.blit(vita,vita2rect)
        screen.blit(vita,vita3rect)
    elif(nVite == 2):
        screen.blit(vita,vita1rect)
        screen.blit(vita,vita2rect)
    else:
        screen.blit(vita,vita1rect)

def  scriviTesto(testo,font,dim,color,pos,screen):
    caratteristiche = pg.font.Font(font, dim)
    testo = caratteristiche.render(testo, True, color)
    testorect =  testo.get_rect()
    testorect.center = pos
    screen.blit(testo,testorect)

def pygameConfig(dimFucile):
    width = 1200
    height = 800
    screen = pg.display.set_mode((width, height))

    sfondo = pg.image.load("./sfondo.gif")
    sfondo = pg.transform.scale(sfondo,(1200,800))
    sfondorect = sfondo.get_rect()
    sfondorect.centerx = width//2
    sfondorect.centery = height//2
    screen.blit(sfondo,sfondorect)


    clock = pg.time.Clock()
    fucile = pg.image.load("./fucile.gif")
    fucile = pg.transform.scale(fucile,(dimFucile[0],dimFucile[1]))
    fucilerect = fucile.get_rect()
    fucilerect.centerx = width//2
    fucilerect.centery = 725
    screen.blit(fucile,fucilerect)

    pg.display.flip()
    return fucile,fucilerect,screen,width,height,clock,sfondo,sfondorect

def gestisciMostro(casuale,listaMostri,width,height,numVite,screen,speed):
    if(casuale < 3 and casuale != 0):
        m = mostro(casuale,random.randint(0,width))
        m.create(screen)
        listaMostri.append(m)
    for m in listaMostri:
        speed[1] = m.velocita
        m.mostrorect = m.mostrorect.move(speed)
        screen.blit(m.mostro,m.mostrorect)
        pg.display.flip()
        
        if(m.mostrorect.y > height):
            listaMostri.remove(m)
            numVite -= 1
    return numVite

def ruotare(fucile,rotazione,screen,width):
    fucile = pg.transform.rotate(fucile,rotazione)
    fucilerect = fucile.get_rect(center=(width//2,725))
    screen.blit(fucile,( fucilerect.x,fucilerect.y))
    pg.display.flip()
    return fucilerect

def sparare(fucilerect,screen,rotazione):
    p = proiettile(fucilerect.centerx,fucilerect.centery,rotazione)
    p.create(screen)
    listaColpi.append(p)

def gestioneProiettili(listaColpi,screen,height,width):
    for proiettile in listaColpi:
        proiettile.posizione += [-proiettile.rotazione.x*proiettile.velocita,proiettile.rotazione.y*proiettile.velocita]
        proiettile.proiettilerect.center = proiettile.posizione
        screen.blit(proiettile.proiettile,proiettile.proiettilerect)
        pg.display.flip()
        
        if(proiettile.proiettilerect.y > height or proiettile.proiettilerect.y < 0 or proiettile.proiettilerect.x > width or proiettile.proiettilerect.x < 0  ):
            listaColpi.remove(proiettile)

def punteggioDifficolta(punteggio,b):
    for m in listaMostri:
        for p in listaColpi:
            point = p.posizione
            collide = m.mostrorect.collidepoint(point)
            if(collide == True):
                listaMostri.remove(m)
                listaColpi.remove(p)
                punteggio += 1;
    if(punteggio/5 == 0 and b > 50):
        b-= 10
    return punteggio,b

def main():
    running = True
    numVite = 3
    a,b=1,500
    speed = [0,0]
    dimFucile= [100,150]
    rotazione = 0
    punteggio = 0
    sparo = False

    rm = Read_Microbit()
    rm.start()
    pg.init()
    

    partire = menu()
    if partire:
        rotIniziale = bussola.get()
        bussola.task_done()
        fucile,fucilerect,screen,width,height,clock,sfondo,sfondorect = pygameConfig(dimFucile)
        while running: 
           
            screen.blit(sfondo,sfondorect)
            stampaVite(numVite,screen)

            rotazione = rotIniziale - bussola.get()
            bussola.task_done()
            fucilerect = ruotare(fucile,rotazione,screen,width)
            numVite = gestisciMostro(random.randint(a,b),listaMostri,width,height,numVite,screen,speed)
            gestioneProiettili(listaColpi,screen,height,width)
            
            #volevo fare il caricatore e muovendo il microbit ricricavo solo che da casa non riuscivo senza microbit
            #acc = accellerazioni.get()
            #accellerazioni.task_done()

            sparo = spari.get()
            spari.task_done()
    
            if (sparo != "False"):
                #fatto per non poter tenere pemuto il tasto quindi bisogna schiacciare e rilasciare per sparare
                sparo = spari.get()
                spari.task_done()
                if (sparo == "False"):
                    sparare(fucilerect,screen,rotazione)
                
            punteggio,b = punteggioDifficolta(punteggio,b)
            
            if(numVite == 0):
                GameOver(punteggio)
                running = False
            pg.display.flip()
            clock.tick(10)

    rm.terminate()
    rm.join()
    pg.quit
    

if __name__== "__main__":
    main()