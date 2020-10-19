import random
import pygame
class Settings():
    """存储《图片华容道》所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        #屏幕设置
        self.screen_width = 1090
        self.screen_height = 700
        self.bg_color = (255,255,255)
        #滑块设置
        self.block_width = 130
        self.block_height = 130
        #随机数设置，用于扣去随机一张图片
        self.random_row = random.randint(0, 2)
        self.random_col = random.randint(0, 2)
        self.ZERO_ROW = self.random_row
        self.ZERO_COL = self.random_col
        self.init_row = self.random_row
        self.init_col = self.random_col
        self.game_active = True
        self.win = False
        #随机打乱次数
        self.times = 10
        #难度增加系数
        self.times_speed = 20
        #重置步数的代价
        self.times_reset = 10
        