#!/usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
https://github.com/xamox/pygame/tree/master/examples
"""


#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror
import random

from pygame import mixer

pygame.mixer.init()
if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'C:/Users/santi/Desktop/TE2003 python/Videogame/Act_game')


#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

#classes for our game objects
class Fist(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('bat_sprite.png', -1)
        self.punching = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        "returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "called to pull the fist back"
        self.punching = 0


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    ancho, largo = 480, 320


    def __init__(self):
        self.speed = 5               #velocidad de movimiento
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('rat_sprite.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 100, 100
        self.move1, self.move2 = self.speed, self.speed
        self.dizzy = 0

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        newpos = self.rect.move((self.move1, self.move2))

        if self.rect.left < self.area.left or self.rect.right > self.area.right:
            self.move1 = -self.move1
            self.image = pygame.transform.flip(self.image, 1, 0)
        if self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
            self.move2 = -self.move2

        newpos = self.rect.move((self.move1, self.move2))

        self.rect = newpos

    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image



def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((468, 320))
    pygame.display.set_caption('TE2003')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("TE2003 Embebidos avanzados", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    whiff_sound = pygame.mixer.Sound('whiff.wav')
    punch_sound = pygame.mixer.Sound('punch.wav')
    #
    # whiff_sound = pygame.mixer.music.play((r'C:\Users\L03038590\Documents\TE2003\mod4_linux_embebido\whiff.wav'))
    # punch_sound = pygame.mixer.music.play((r'C:\Users\L03038590\Documents\TE2003\mod4_linux_embebido\punch.wav'))
    chimp = Chimp()
    fist = Fist()
    allsprites = pygame.sprite.RenderPlain((fist, chimp))

    clock = pygame.time.Clock()
    counter, clktxt = 120, '120'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT,1000)
    clkfont = pygame.font.SysFont('Consolas', 25)
    k=0

    score, sctxt = 0, '0'.rjust(3)
    scfont = pygame.font.SysFont('Consolas', 30)

#Main Loop
    going = True
    while going:


        #Handle Input Events
        for event in pygame.event.get():

            if event.type == pygame.USEREVENT :
                counter -= 1
                k += 1
                clktxt = str(counter).rjust(3) if counter > 0 else 'TIME OUT!'
                if counter == 0:
                    going = False
                if k == 20:
                    chimp.move1 -= 5
                    chimp.move2 -= 5
                    k = 0

            elif event.type == QUIT:
                going = False

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False

            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play() #punch
                    chimp.punched()
                    score += 10
                    sctxt = str(score).rjust(3)
                else:
                    whiff_sound.play() #miss
                    score -= 20
                    sctxt = str(score).rjust(3)
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        screen.blit(clkfont.render(clktxt, True, (0,0,0)), (22,38))
        screen.blit(scfont.render(sctxt, True, (0,0,0)), (400,38))
        allsprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
