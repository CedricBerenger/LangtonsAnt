#! usr/bin
# -*- coding: utf8 -*-

'''
Created on 9 janv. 2016

Copyright (C) 2016 BERENGER Cédric

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

@author: cedric
'''

import pygame
import sys
import getopt

import numpy as np
from PIL import Image

#Classe modélisant une fourmis ( coordonnées, état (orientation de la flèche), etc..)
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
    
#Classe modélisant la grille. Ici, la grille est un tore, (les côtés de la grille sont connectés).
class LangtonsAntSimulator():
    
    def __init__(self,grid_shape):
        self.grid = np.zeros(grid_shape,dtype = np.int32)
        self.ants = []
        self.niter = 0
        self.olditer = 0
    
    def resizeGrid(self,grid_shape):
        self.grid = np.zeros(grid_shape,dtype = np.int32)
    
    #Itérer vers le futur (Go forward).
    def iterate(self):
        self.olditer = self.niter
        self.niter+=1
        for ant in self.ants:
            ant.go()
            
    #Itérer vers le passer (Go backward).
    def uniterate(self):
        self.olditer = self.niter
        self.niter-=1
        for ant in self.ants:
            ant.ungo()
            
    #Chargement d'une configuration initiale (au format png ou autre, c'est la lib PIL que s'occupe de tout).
    def loadPic(self,filename="init_config.png"):
        im = Image.open(filename)
        pix = im.load()
        self.grid = np.zeros(im.size,dtype = np.int32)
        for y in xrange(0,im.size[1]):
            for x in xrange(0,im.size[0]):
                if pix[x,y] == (255,0,0): self.ants.append(Ant(self,initial_state=0,initial_coords=(x,im.size[1]-y-1)))
                if pix[x,y] == (255,255,0): self.ants.append(Ant(self,initial_state=1,initial_coords=(x,im.size[1]-y-1)))
                if pix[x,y] == (0,0,255): self.ants.append(Ant(self,initial_state=2,initial_coords=(x,im.size[1]-y-1)))
                if pix[x,y] == (0,255,0): self.ants.append(Ant(self,initial_state=3,initial_coords=(x,im.size[1]-y-1)))
                if pix[x,y] == (0,0,0): self.grid[x,im.size[1]-y-1] = 1
                if pix[x,y] == (255,255,255): self.grid[x,im.size[1]-y-1] = 0

#J'aime bien les thèmes couleurs des anciens ordinateurs personnels des années 80, particulièrement celui du amstrad:
amstradLightBlue = (0,128,255)
amstradGreen = (0,255,0)
amstradYellow = (255,255,0)
amstradRed = (255,0,0)
amstradDarkPurple = (128,0,128)
amstradDarkBlue = (0,0,128)
amstradPurple = (128,0,255)

stateColor = [amstradRed,amstradYellow,amstradLightBlue,amstradGreen]

#Partie Graphique (basée sur la librarie graphique pygame).
class Graphics:
    
    def __init__(self,simulator,cellsize = 4,padding = 2):
        pygame.init()
        self.displayOverlay = False
        self.antColorCode=pygame.image.load("Others/ColorCodeBig.png")
	self.screen = pygame.display.set_mode((800,600))        
	#self.screen = pygame.display.set_mode((800,600))
        self.amstradFont = pygame.font.Font("amstrad_cpc464.ttf",12)
        self.simulator = simulator
        self.cellSize = cellsize
        self.padding = padding

    #Affiche l'overlay rappel des couleurs.
    def paintColorOverlay(self):
        if self.displayOverlay:
            self.screen.blit(self.antColorCode,(800-150-10,600-150-10))

    #(Ré)Affiche tout.
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
                
        self.paintColorOverlay()
        
        self.paint()

    #Ne paint que les modifications (peu produire des artéfacts, mais augmente considérablement les performances).
    def paint(self):
        
        w = self.cellSize
        h = w
        
        ny = self.simulator.grid.shape[1]
        l= self.cellSize+self.padding
            
        ymax = l*(ny-1)
        
        #Effacement de l'ancien label
        label = self.amstradFont.render("Langton's Ant! (Cedric Berenger) Step="+str(self.simulator.olditer),1,amstradPurple)
        self.screen.blit(label,(10,10))
        
        #Effacement de l'ancienne position
        for ant in self.simulator.ants:
            state = self.simulator.grid[ant.old_coords]           
            color = amstradDarkBlue if state else amstradPurple    
            xold = ant.old_coords[0]*l
            yold = ymax-ant.old_coords[1]*l
            pygame.draw.rect(self.screen,color,(xold,yold,w,h),0)
        
        #Affichage de la nouvelle position
        for ant in self.simulator.ants:
            color = stateColor[ant.state]
            x = ant.coords[0]*l
            y = ymax-ant.coords[1]*l
            pygame.draw.rect(self.screen,color,(x,y,w,h),0)
            
        #Affichage du nouveau label
        
        label = self.amstradFont.render("Langton's Ant! (Cedric Berenger) Step="+str(self.simulator.niter),1,amstradYellow)
        self.screen.blit(label,(10,10))
      
    #Applique le tampon (flush).  
    def update(self):
        pygame.display.update()
    
#Listing des touches.
def print_keys():
    print """
Keys:
=====
Space            Launch / Pause the simulation.
Up,Down          Change the simulation speed.
Left,Right       Go Forward / Backward in time.
Q                Quit the simulator.
O                Display / Hide the Ant color code overlay.\n

Use the help option -h for further informations.

"""

#Affichage de l'aide.
def print_help():
    print """\nLangtonsAnt.py -i <image> -d <delay (ms)> -s <size (pixels)>
        
A Simple Langton's Ant Simulator, Created by Cedric Berenger,
With initial configuration loadable via simple png picture.
.
        
Options: i is the image path, d is , and s is the size of the cells in pixels.
========
-i <"my_image.png">    image to use as initial configuration (file path).
-d <42>                the delay between two frames (simulator speed).
-s <42>                the size of the cells of the grid in pixels.
-p <4>                 the padding between cells.

Image format:
=============
A pixel without color represents a cell of the grid:

White pixel    is a white cell.
Black pixel    is a black cell.

A colored pixel represents an ant and the color codes the direction of the arrow of the ant, according to the ant color code in the overlay:

Red            Up
Blue           Bottom
Green          Left
Yellow         Right

Note: In my implementation, An ant always start on a white cell and do not write it on the first iteration. Why ? Why not ! (It was just too boring to code it right ^^).
\n"""
    
#Fonction principale.      
def main(argv):
                 
    #Lecture des arguments
    
    #Valeurs par défaut: 
    
    delay = 80                  #Delay entre l'affichage de deux trames (plus le delai est cours, plus la simulation est rapide).
    image = "init_config.png"   #Image pour la configuration initiale.
    size = 10                   #Taille des cellules.
    padding = 2                 #Padding.
    try:
        opts, args = getopt.getopt(argv,"hi:d:s:p:",["ifile=","delay=","size=","padding="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            image = arg
        elif opt in ("-d", "--delay"):
            delay = int(arg)
        elif opt in ("-p", "--padding"):
            padding = int(arg)
        elif opt in ("-s", "--size"):
            size = int(arg)
    
    #Programme principal
    
    print_keys()    #Affichage de l'aide dans la console.
                    
    simulator = LangtonsAntSimulator((100,100)) #Création d'une grille de simulation (la taille 100x100 n'a pas d'importance)...
    simulator.loadPic(filename=image)           #...Car ici, on crée une nouvelle grille via chargement d'une configuration initiale. 
    
    g = Graphics(simulator,cellsize=size,padding=padding)       #Création de l'objet graphique (utilise pygame).
    g.paintAll()
    
    way = 1                                     #Sens temporel (1=futur/-1=passé)
    pause = 1                                   #Met en pause la simulation (1=Oui / 0=Non)
    
    while 1:                                    #Boucle principale.
        
            for i in xrange(0,delay+1):
                pygame.time.delay(1)
            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            exit()
                        if event.key == pygame.K_o:
                            g.displayOverlay = not g.displayOverlay
                            g.paintAll()
                        if event.key == pygame.K_RIGHT:
                            simulator.iterate()
                            way = 1
                        if event.key == pygame.K_LEFT:
                            simulator.uniterate()
                            way = -1
                        if event.key == pygame.K_SPACE:
                            pause = 1 - pause
                        if event.key == pygame.K_UP:
                            delay -=10
                            if delay < 0:
                                delay = 0
                        if event.key == pygame.K_DOWN:
                            delay += 10
                            
                g.paint()
                g.update()
                
            #Cette partie, c'est juste pour mettre en pause sur l'image de remerciement, à enlever pour améliorer les perfs.                
            if not pause and (not (image == "Tests/ThankYou.png" and simulator.niter == 17767)) :
                if way > 0:
                    simulator.iterate()
                else:
                    simulator.uniterate()
            
if __name__ == "__main__":
    main(sys.argv[1:])
