import pygame
import sys
import os
from pygame.sprite import Sprite

os.chdir(sys.path[0])

class Block(Sprite):
    """滑块类"""
    def __init__(self, ai_settings, screen, image_cut, num):
        '''初始化图块并设置其初始值'''
        super().__init__()
        self.screen = screen
        #加载图片并获取其外接矩形
        self.image = pygame.image.load('images_cut/'+image_cut)
        self.image = pygame.transform.smoothscale(self.image, (ai_settings.block_width, ai_settings.block_height))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #num属性表示相对位置
        self.num = num
        self.ai_settings = ai_settings

        #在图片的x属性中存储小数值
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.x = (self.screen_rect.width - 3 * self.rect.width)/2
        self.y = (self.screen_rect.height - 3 * self.rect.height)/2

    def blitme(self):
        """在指定位置绘制图片"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """调整滑块位置"""
        #根据self.x更新rect对象
        self.rect.x = self.x
        self.rect.y = self.y

