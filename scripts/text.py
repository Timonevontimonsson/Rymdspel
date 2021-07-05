import pygame
class Text():


    def textToScreen(win, text, x, y, size = 50,
            color = (200, 000, 000), font_type = 'Comic Sans MS'):
    

        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        win.blit(text, (x, y))
