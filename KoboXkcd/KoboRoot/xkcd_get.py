import urllib2
import pygame, os
from subprocess import *
import xkcd
import io
import random
import json
import textwrap
random.seed()

os.environ['SDL_NOMOUSE'] = '1'
import urllib2
import struct
import time
from time import sleep
import sys
import schedule
def internet_on():
    try:
        response=urllib2.urlopen('http://www.google.com',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

is_internet_on = internet_on()

def to_hex(color):
    hex_chars = "0123456789ABCDEF"
    return hex_chars[color / 16] + hex_chars[color % 16]
    
def convert_to_raw(surface,number):
    f = open("/mnt/sd/xkcd/"+str(number)+'.raw', "wb")               



    f.write(pygame.image.tostring(surface,"RGB")[::3])

    f.close()
    print("Converting image . . .")
#    raw_img = ""
#    for row in range(surface.get_height()):
#        for col in range(surface.get_width()):
#            color = surface.get_at((col, row))[0]
#            raw_img += ('\\x' + to_hex(color)).decode('string_escape')
#    f = open("/mnt/sd/xkcd/"+str(number)+'.raw', "wb")
#    f.write(raw_img)
#    f.close()

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

def update():
    latest_num = os.listdir("/mnt/sd/xkcd/")
    latest_num = [int(x.strip('.raw')) for x in latest_num]
    latest_num.sort()
    latest_num = latest_num[-1]



    if(latest_num == xkcd.getLatestComicNum()):
	return True

 
    for i in range(latest_num,xkcd.getLatestComicNum()+1):
	
        print("Downloading comic" + str(i))
        pygame.font.init()
        white = (255, 255, 255)
        black = (0, 0, 0)
        gray = (125, 125, 125)
        screen = pygame.Surface((600, 800))

        screen.fill(white)
        comic=xkcd.Comic(i)
	print(comic)
        link = comic.getImageLink()
        image_raw = urllib2.urlopen(link).read()
        image_raw2 = io.BytesIO(image_raw)
        image = pygame.image.load(image_raw2)
        myfont = pygame.font.Font('/KoboXkcd/KoboRoot/xkcd-Regular.otf', 20)
        myfont2 = pygame.font.Font('/KoboXkcd/KoboRoot/xkcd-Regular.otf', 13)
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
def display(number):
    print(number)
    call(["/display_raw.sh","/mnt/sd/xkcd/"+str(number)+".raw"])

if(is_internet_on):
    update()

latest_num = os.listdir("/mnt/sd/xkcd/")                           
latest_num = [int(x.strip('.raw')) for x in latest_num]            
latest_num.sort()                                                  
latest_num = latest_num[-1] 

#call(['pkill','nickel']) 
call(['/rw.sh']) 
display(latest_num)
in_file = open('/dev/input/event0','rb')
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)
in_file = open('/dev/input/event0','rb')
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)
while True:
    (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
    if code != 0 and value != 0:
        print("Event type %u, code %u, value %u at %d.%d" % \
        (type, code, value, tv_sec, tv_usec))

	call(["/usr/local/Kobo/pickel","blinkoff"])
	if(code == 60):
	    try:
	        call(["/display_raw.sh","/mnt/sd/dc/"+str(random.randint(1,2800))+".raw"]) 
	    except:
	        pass
	if(code == 59):
	    update()
	    display(latest_num) 
	if(code == 62):
            display(random.randint(1,latest_num))

    else:
     # Events with code, type and value == 0 are "separator" events
	pass
    event=in_file.read(EVENT_SIZE)

while True:
	display(random.randint(1,latest_num))

