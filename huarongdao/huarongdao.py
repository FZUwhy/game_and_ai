import sys
import os
import pygame
import game_function as gf
import random
from PIL import Image
from pygame.sprite import Group
from settings import Settings
from block import Block
from stepboard import Stepboard
from game_stat import GameStats
from button import Button
from logo import Logo
from background import Background

os.chdir(sys.path[0])


def run_game():
    # 初始化背景设置
    image_list = gf.init_images()
    pygame.init()
    ai_settings = Settings()
    
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    background = Background(ai_settings, screen)
    stats = GameStats(ai_settings)
    sb = Stepboard(ai_settings, screen, stats)
    pygame.display.set_caption("图片华容道")
    logo = Logo(ai_settings, screen)

    # 创建开始游戏按钮
    play_button = Button(ai_settings, screen, stats, "", "images_material/play_button.png")
    replay_button = Button(ai_settings, screen, stats, "", "images_material/again.png")
    exit_button = Button(ai_settings, screen, stats, "", "images_material/exit_button.png")
    back_button = Button(ai_settings, screen, stats, "", "images_material/back.png")
    reset_button = Button(ai_settings, screen, stats, "", "images_material/reset.png")
    
    # 创建滑块列表
    blocks = list()
    
    # 填充滑块列表
    gf.create_all_blocks(ai_settings, screen, blocks, image_list)  # 把切割好的图像列表传进来
    BLOCKS_ORI = list(blocks)
    reset_blocks = list()
    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, blocks, BLOCKS_ORI, reset_blocks, stats, sb, play_button, replay_button, reset_button, exit_button, back_button, image_list)
        if stats.game_menu:
            gf.update_screen_menu(ai_settings, screen, blocks, stats, sb, play_button, exit_button, logo, background)
        else:
            gf.update_screen_playing(ai_settings, screen, blocks, stats, sb, replay_button, back_button, reset_button, background)


run_game()
