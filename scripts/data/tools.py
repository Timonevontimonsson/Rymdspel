import os
import pygame
from scripts.data import constant as c
from scripts import player
import pickle

keybinding = {
        'left':pygame.K_a,
        'right':pygame.K_d,
        'up':pygame.K_w,
        'down':pygame.K_s,
        'skill':pygame.K_SPACE,
        'dash':pygame.K_LSHIFT,
        'pause': pygame.K_p,
        'enter':pygame.K_RETURN
    }

keyPressed = []
keyReleased = []
keyEvent = []
class Control(object):
    """kontroll klass för hela projektet. Den innehåller game 
    loopen och eventloopen och lite logik med"""
    
    def __init__(self, caption):
        self.screen = pygame.display.get_surface()
        self.done = False
        self.clock = pygame.time.Clock()
        self.caption = caption
        self.fps = 60
        self.show_fps = False
        self.current_time = 0.0
        self.keys = pygame.key.get_pressed()
        self.state_dict = {}
        self.state_name = None
        self.state = None
        self.pressed_timer = 0
        
        

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        
    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        player = self.state.cleanup_player()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist, player)
        self.state.previous = previous

#keys[tools.keybinding['down']] or keys[tools.keybinding['up']] or keys[tools.keybinding['left']] or keys[tools.keybinding['right']]

    def event_loop(self):
        global keyPressed
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                keyEvent.append(event.type)
               
            elif event.type == pygame.KEYDOWN:
                self.keys = pygame.key.get_pressed()
                keyPressed.append(event.key)
                print(keyPressed)
            elif event.type == pygame.KEYUP:
                if event.key != pygame.K_LSHIFT:

                    keyReleased.append(event.key)
                if event.key == pygame.K_LSHIFT:
                    keyPressed.remove(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    keyPressed.append("mouse")
                if event.button == 3:
                    keyPressed.append("mouse2")
                    
                
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and "mouse" in keyPressed:
                    keyPressed.remove("mouse")
                    keyReleased.append("mouse")
                if event.button == 3:
                    if "mouse2" in keyPressed:
                        keyPressed.remove("mouse2")
                    
            
            self.state.get_event(event)


    def main(self):
        """Main loop for entire program"""
        
        while not self.done:
            
            self.event_loop()
            self.update()
            pygame.display.update()
            self.clock.tick(self.fps)
            
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pygame.display.set_caption(with_fps)
        




class _State(object):
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def get_event(self, event):
        pass

    def startup(self, current_time, persistant):
        self.persist = persistant
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.persist
    def cleanup_player(self):
        self.done = False
        return self.player

    def update(self, surface, keys):
        pass





def load_all_gfx(directory, colorkey=(255,0,255), accept=('.png', 'jpg', 'bmp')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics


def load_all_music(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
    songs = {}
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_fonts(directory, accept=('.ttf')):
    return load_all_music(directory, accept)


def load_all_sfx(directory, accept=('.wav','.mpe','.ogg','.mdi')):
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pygame.mixer.Sound(os.path.join(directory, fx))
    return effects