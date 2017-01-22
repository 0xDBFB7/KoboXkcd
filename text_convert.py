import pygame
import sys
from subprocess import *
screen = pygame.Surface((600,800))
screen.fill((255,255,255))
pygame.font.init()
myFont = pygame.font.SysFont("monospace", int(sys.argv[3]))
y = int(sys.argv[3])
with open(sys.argv[1]) as f:
    for line in f:
        screen.blit(myFont.render(line,True,(0,0,0)),(5,y))
        y+=int(sys.argv[3])
f= open(sys.argv[2], "wb")
f.write(pygame.image.tostring(screen,"RGB")[::3])
f.close()
call(["/display_raw.sh",sys.argv[2]])

