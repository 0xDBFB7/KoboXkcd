import pygame
import sys
from subprocess import *
screen = pygame.Surface((600,800))

def aspect_scale(img,(bx,by)):                                         
    """ Scales 'img' to fit into box bx/by.                            
     This method will retain the original image's aspect ratio """     
    ix,iy = img.get_size()                                                  
    if ix > iy:                                                              
        # fit to width                                                        
        scale_factor = bx/float(ix)                                           
        sy = scale_factor * iy                                                
        if sy > by:                                                           
            scale_factor = by/float(iy)                                       
            sx = scale_factor * ix                                            
            sy = by                                                           
        else:                                                                 
            sx = bx                                                           
    else:                                                                     
        # fit to height                                                       
        scale_factor = by/float(iy)                                           
        sx = scale_factor * ix                                                
        if sx > bx:                                                           
            scale_factor = bx/float(ix)                                       
            sx = bx                                                           
            sy = scale_factor * iy                                            
        else:                                                                 
            sy = by                                                           
                                                                              
    return pygame.transform.scale(img, (int(sx),int(sy)))  
if(len(sys.argv) > 2):
	screen.blit(aspect_scale(pygame.image.load(sys.argv[1]),(600,800)),(0,0))
else:
        screen.blit(pygame.image.load(sys.argv[1]),(0,0))

f= open(sys.argv[2], "wb")  
f.write(pygame.image.tostring(screen,"RGB")[::3])  
f.close()
call(["/display_raw.sh",sys.argv[2]])      
