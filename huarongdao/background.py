import pygame
import sys
import os
from pygame.sprite import Sprite

os.chdir(sys.path[0])

class Background():
    def __init__(self, ai_settings, screen):
        '''初始化背景图片并设置其初始值'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        #开始界面
        self.bg_menu = pygame.image.load(r"images_material\bg_menu.jpg")
        self.bg_menu = pygame.transform.smoothscale(self.bg_menu, (self.screen_rect.width, self.screen_rect.height))
        #游玩界面
        self.bg_playing = pygame.image.load(r"images_material\bg_playing.jpg")
        self.bg_playing = pygame.transform.smoothscale(self.bg_playing, (self.screen_rect.width, self.screen_rect.height))
        #滑块背景
        self.border = pygame.image.load(r"images_material\border.png")
        self.border = pygame.transform.smoothscale(self.border, (540, 565))
        self.border_rect = self.border.get_rect()
        self.border_rect.centerx = self.screen_rect.centerx
        self.border_rect.centery = self.screen_rect.centery -3

    def blitme(self, image, rect):
        """在指定位置绘制图片"""
        self.screen.blit(image, rect)