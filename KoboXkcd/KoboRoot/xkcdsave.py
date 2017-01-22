import urllib2
import pygame, os
from subprocess import call
import xkcd
import io
from time import sleep
import textwrap
os.environ['SDL_NOMOUSE'] = '1'
def to_hex(color):
    hex_chars = "0123456789ABCDEF"
    return hex_chars[color / 16] + hex_chars[color % 16]
    
def convert_to_raw(surface,num):
    print("Converting image . . .")
    raw_img = ""
    for row in range(surface.get_height()):
        for col in range(surface.get_width()):
            color = surface.get_at((col, row))[0]
            raw_img += ('\\x' + to_hex(color)).decode('string_escape')
    f = open("./xkcd/"+str(num)+'.raw', "wb")
    f.write(raw_img)
    f.close()
    print(num)

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


def display(i):
    print(i)
    print("Downloading latest comic")
    pygame.font.init()
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (125, 125, 125)
    screen = pygame.Surface((600, 800))
    screen.fill(white)
    comic=xkcd.Comic(i)
    link = comic.getImageLink()
    image_raw = urllib2.urlopen(link).read()
    image_raw2 = io.BytesIO(image_raw)
    image = pygame.image.load(image_raw2)
    myfont = pygame.font.Font('./xkcd-Regular.otf', 20)
    myfont2 = pygame.font.Font('./xkcd-Regular.otf', 13)
    label = myfont.render('xkcd '+ str(i)+'; '+comic.getTitle(), 1, black)
    if(image.get_width() > image.get_height()):
        label = pygame.transform.rotate(label,90)
        label_rect = label.get_rect()
        label_rect.center = (7, 400)
        image = pygame.transform.rotate(image,90)
        image = aspect_scale(image,(460,750))
        image.set_colorkey((255, 255, 255))
        img_rect = image.get_rect()
        img_rect.center = (275, 400)
        position = 290+int(image.get_width()/2)+10
    else:
        label_rect = label.get_rect()
        label_rect.center = (300, 7)
        image = aspect_scale(image,(460,750))
        image.set_colorkey((255, 255, 255))
        img_rect = image.get_rect()
        img_rect.center = (300, 400)
        position = 300+int(image.get_width()/2)+10
    screen.blit(label, label_rect)
    print(position)
    for l in textwrap.wrap(comic.getAltText(),80):
        alttext = myfont2.render(l, 1, black)
        alttext = pygame.transform.rotate(alttext,90)
        alttext_rect = alttext.get_rect()
        alttext_rect.center = (position, 400)
        screen.blit(alttext, alttext_rect)
        position+=20
        if(position > 600):
            print('aah!')
            break
    screen.blit(image,img_rect)
    convert_to_raw(screen,i)

for m in range(405,xkcd.getLatestComicNum()):
    try:
        display(m)
    except:
        pass
    sleep(0.5)
