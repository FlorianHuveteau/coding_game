import pygame

WHITE = pygame.Color("white")

class Ui():

    def __init__(self, path_mng):
        self.font_mng = self.FontManager()
        self.font = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        self.font_size = 22
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.elapsed_time = 0

    def draw(self, surface):

        elapse_lbl = self.font_mng.create_text(text="Elapse Time", font=self.font, size=self.font_size, color=pygame.Color("white"))
        surface.blit(elapse_lbl, (20, 20))

        font = pygame.font.SysFont(self.font, self.font_size)
        elapsed = font.render("{:.2f}".format(self.elapsed_time), True, pygame.Color("white"), (0, 0, 0))
        elapsed_rect = elapsed.get_rect()
        surface.blit(elapsed, (120, 20))
        self.button(surface, "Restart", 600, 50, 80,30)


    def button(self, surface, msg, x, y, w, h, action=None):
        """
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        pygame.draw.rect(surface, WHITE, (x, y, w, h),1)
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if click[0] == 1 and action != None:
                action()

        font_surf = pygame.font.SysFont(self.font, self.font_size)
        text_surf = font_surf.render(msg, True, WHITE, (0,0,0))
        text_rect = text_surf.get_rect()
        text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        surface.blit(text_surf, text_rect)

    def update(self, dt, elapsed_time):
        self.dt = dt
        self.elapsed_time = elapsed_time





    class FontManager():

        def __init__(self):
            self.available_fonts = pygame.font.get_fonts()
            self.cached_fonts = {}
            self.cached_texts = {}

        def make_font(self, font, size):
            choice = font.lower().replace(" ", "")
            if choice in self.available_fonts:
                return pygame.font.SysFont(choice, size)

            return pygame.font.Font(None, size)

        def get_font(self, font, size):
            key = "{}|{}".format(font, size)
            img = self.cached_fonts.get(key)
            if not img:
                img = self.make_font(font, size)
                self.cached_fonts[key] = font
            return img

        def create_text(self, text, font, size, color):
            key = "{}|{}|{}|{}".format(text, font, size, color)
            img = self.cached_texts.get(key)
            if not img:
                font = self.get_font(font, size)
                img = font.render(text, True, color, (0, 0, 0))
                self.cached_texts[key] = img
            return img
