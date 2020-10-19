import pygame

class Logo():

    def __init__(self, ai_settings, screen):
        '''初始化游戏标题并设置其初始值'''
        self.screen = screen
        #加载logo图形并获取其外接矩形
        self.image = pygame.image.load('images_material/logo.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #将Logo放在屏幕中上方
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.top + 16
        self.ai_settings = ai_settings

        #在logo的center属性中存储小数值
        self.center = float(self.rect.centerx)

    def blitme(self):
        """在指定位置绘制logo"""
        self.screen.blit(self.image, self.rect)

    