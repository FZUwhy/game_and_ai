import pygame.font

class Button():

    def __init__(self, ai_settings, screen, stats, msg = "", img = ""):
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = ai_settings

        #设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (225,225,225)
        self.text_color = (100, 100, 100)
        self.font = pygame.font.SysFont(None, 80)
        #创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        if img == "":
            self.prep_msg(msg)
        else:
            self.prep_img(img)

    def prep_play_button(self):
        self.image = pygame.transform.smoothscale(self.image, (self.settings.block_width + 20, self.settings.block_height-10))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

    def prep_exit_button(self):
        self.image = pygame.transform.smoothscale(self.image, (self.settings.block_width + 20, self.settings.block_height-10))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery + 130

    def prep_replay_button(self):
        self.image = pygame.transform.smoothscale(self.image, (250, 120))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx + 420
        self.rect.centery = self.screen_rect.centery + 300

    def prep_back_button(self):
        self.image = pygame.transform.smoothscale(self.image, (self.settings.block_width, self.settings.block_height))
        self.rect = self.image.get_rect()
        self.rect.top = self.screen_rect.top
        self.rect.left = self.screen_rect.left

    def prep_reset_button(self):
        self.image = pygame.transform.smoothscale(self.image, (self.settings.block_width, self.settings.block_height))
        self.rect = self.image.get_rect()
        self.rect.top = self.screen_rect.top
        self.rect.right = self.screen_rect.right

    def prep_msg(self, msg):
        """将msg渲染成图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = self.rect.centerx
        self.rect.centery = self.screen_rect.centery + 130

    def prep_img(self, img):
        """加载img,创建图片按钮"""
        self.image = pygame.image.load(img)
        
    def draw_button(self):
        """绘制一个用颜色填充的按钮,再绘制文本 """   
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_image_button(self):
        """在指定位置绘制图片按钮"""
        self.screen.blit(self.image, self.rect)