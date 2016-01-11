#! usr/bin
# -*- coding: utf8 -*-

'''
Created on 9 janv. 2016

@author: cedric
'''


import pygame
import sys
import getopt

import numpy as np
from PIL import Image

class Ant:
    def __init__(self,simulator,initial_coords,initial_state=0):
        self.simulator = simulator
        self.state = initial_state
        self.coords = initial_coords
        self.old_coords = initial_coords
    
    def go(self):
        #Mise à jour des coordonnées
        self.old_coords = self.coords
        x = self.coords[0]
        y = self.coords[1]
        if(self.state == 0): y+=1 #Haut
        if(self.state == 1): x+=1 #Droite
        if(self.state == 2): y-=1 #Bas
        if(self.state == 3): x-=1 #Gauche
        
        x%=self.simulator.grid.shape[0]
        y%=self.simulator.grid.shape[1]
        self.coords = (x,y)
        #Mise à jour de l'état (rotation de l'état courant):
        state = self.simulator.grid[self.coords]
        
        self.simulator.grid[self.coords] = 1-state
        
        self.state += 1 if state else -1
        self.state %= 4

    def ungo(self):
        
        #Mise à jour de l'état (rotation de l'état courant):
        
        state = self.simulator.grid[self.coords]
        
        self.state += 1 if state else -1
        self.state %= 4
        
        self.simulator.grid[self.coords] = 1-state
        
        #Mise à jour des coordonnées
        self.old_coords = self.coords
        x = self.coords[0]
        y = self.coords[1]
        if(self.state == 0): y-=1 #Haut
        if(self.state == 1): x-=1 #Droite
        if(self.state == 2): y+=1 #Bas
        if(self.state == 3): x+=1 #Gauche
        
        x%=self.simulator.grid.shape[0]
        y%=self.simulator.grid.shape[1]
        self.coords = (x,y)
    
class LangtonsAntSimulator():
    
    def __init__(self,grid_shape):
        self.grid = np.zeros(grid_shape,dtype = np.int32)
        self.ants = []
        self.niter = 0
    
    def resizeGrid(self,grid_shape):
        self.grid = np.zeros(grid_shape,dtype = np.int32)
    
    def iterate(self):
        self.niter+=1
        for ant in self.ants:
            ant.go()
            
    def uniterate(self):
        self.niter-=1
        for ant in self.ants:
            ant.ungo()
            
    def loadPic(self,filename="init_config.png"):
        im = Image.open(filename)
        pix = im.load()
        print im.size
        self.grid = np.zeros(im.size,dtype = np.int32)
        for y in xrange(0,im.size[1]):
            for x in xrange(0,im.size[0]):
                if pix[x,y] == (255,0,0): self.ants.append(Ant(self,initial_state=0,initial_coords=(x,im.size[1]-y-1)))
                if pix[x,y] == (255,255,0): self.ants.append(Ant(self,initial_state=1,initial_coords=(x,im.size[1]-y-1)))
                if pix[x,y] == (0,0,255): self.ants.append(Ant(self,initial_state=2,initial_coords=(x,im.size[1]-y-1)))
                if pix[x,y] == (0,255,0): self.ants.append(Ant(self,initial_state=3,initial_coords=(x,im.size[1]-y-1)))
                if pix[x,y] == (0,0,0): self.grid[x,im.size[1]-y-1] = 1
                if pix[x,y] == (255,255,255): self.grid[x,im.size[1]-y-1] = 0

amstradLightBlue = (0,128,255)
amstradGreen = (0,255,0)
amstradYellow = (255,255,0)
amstradRed = (255,0,0)
amstradDarkPurple = (128,0,128)
amstradDarkBlue = (0,0,128)
amstradPurple = (128,0,255)

stateColor = [amstradRed,amstradYellow,amstradLightBlue,amstradGreen]

class Graphics:
    
    def __init__(self,simulator,screen,cellsize = 4,padding = 2):
        self.simulator = simulator
        self.screen = screen
        self.cellSize = cellsize
        self.padding = padding

    def paintAll(self):
        self.screen.fill(amstradDarkPurple)
        
        w = self.cellSize
        h = w
        
        nx = self.simulator.grid.shape[0]
        ny = self.simulator.grid.shape[1]
        
        l= self.cellSize+self.padding
        ymax = l*(ny-1)
        
        for j in xrange(0,ny):
            for i in xrange(0,nx):        
                state = self.simulator.grid[i,j]         
                color = amstradDarkBlue if state else amstradPurple
                x = i*l
                y = ymax - j*l
                pygame.draw.rect(self.screen,color,(x,y,w,h),0)
                
        self.paint()

    def paint(self):
        
        w = self.cellSize
        h = w
        
        ny = self.simulator.grid.shape[1]
        l= self.cellSize+self.padding
            
        ymax = l*(ny-1)
        
        for ant in self.simulator.ants:
            state = self.simulator.grid[ant.old_coords]           
            color = amstradDarkBlue if state else amstradPurple    
            xold = ant.old_coords[0]*l
            yold = ymax-ant.old_coords[1]*l
            pygame.draw.rect(self.screen,color,(xold,yold,w,h),0)
        
        for ant in self.simulator.ants:
            color = stateColor[ant.state]
            x = ant.coords[0]*l
            y = ymax-ant.coords[1]*l
            pygame.draw.rect(self.screen,color,(x,y,w,h),0)
          
def main(argv):
                 
    #Lecture des arguments
    
    delay = 80
    image = "init_config.png"
    size = 10
                    
    try:
        opts, args = getopt.getopt(argv,"hi:d:s:",["ifile=","delay=","size="])
    except getopt.GetoptError:
        print 'LangtonsAnt.py -i <image> -d <delay (ms)> -s <size>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'LangtonsAnt.py -i <image> -d <delay (ms)> -s <size>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            image = arg
        elif opt in ("-d", "--delay"):
            delay = int(arg)
        elif opt in ("-s", "--size"):
            size = int(arg)
    
    #Main program
                    
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Langton's Ant Simulator, Cédric Bérenger 2015")
    
    amstradFont = pygame.font.Font("amstrad_cpc464.ttf",12)
    
    pygame.display.update()
    
    simulator = LangtonsAntSimulator((100,100))
    
    simulator.loadPic(filename=image)
    
    #simulator.ants.append(Ant(simulator,(50,50)))
    g = Graphics(simulator,screen,cellsize=size)
    
    g.paintAll()
    
    
    label = amstradFont.render("Langton's Ant! (Cedric Berenger) Step=0",1,amstradYellow)
    screen.blit(label,(10,10))
    
    pygame.display.update()
    
    pause = 1
    
    while 1:
        
            pygame.display.update()
            label = amstradFont.render("Langton's Ant! (Cedric Berenger) Step="+str(simulator.niter),1,amstradPurple)
            screen.blit(label,(10,10))
        
            for i in xrange(0,delay+1):
                pygame.time.delay(1)
            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            exit()
                        if event.key == pygame.K_RIGHT:
                            simulator.iterate()
                        if event.key == pygame.K_LEFT:
                            simulator.uniterate()
                        if event.key == pygame.K_SPACE:
                            pause = 1 - pause
                        if event.key == pygame.K_UP:
                            delay -=10
                            if delay < 0:
                                delay = 0
                        if event.key == pygame.K_DOWN:
                            delay += 10
                            
                            
            if not pause:
                simulator.iterate()
                
            label = amstradFont.render("Langton's Ant! (Cedric Berenger) Step="+str(simulator.niter),1,amstradYellow)
            screen.blit(label,(10,10))
            g.paint()
            
if __name__ == "__main__":
    main(sys.argv[1:])
