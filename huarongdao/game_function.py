import sys
import os
import pygame
import random
import cut
from pygame import event
from time import sleep
from block import Block
"""创建游戏使用的各种函数"""
def init_images():
    #返回切割图片路径
    ori_image_list = get_ori_images_path('images')
    #随机取图
    ranint = random.randint(0, 35)
    image_list = get_images_path(ori_image_list[ranint] , 'images', 'images_cut')
    return image_list

def get_ori_images_path(filepack_name):
    os.getcwd()#获取当前路径
    return os.listdir(filepack_name)#获取原图文件夹下所有文件名

def get_images_path(file_path , ori_filepack_name, filepack_name):
    """获取切割图片的路径"""
    cut.get_image_list(ori_filepack_name+'/'+file_path)
    os.getcwd()#获取当前路径
    return os.listdir(filepack_name)#获取文件夹下所有文件名

def update_screen_menu(ai_settings, screen, blocks, stats, sb, play_button, exit_button, logo, background):
    """更新菜单界面屏幕上的图像并切换到新屏幕"""
    #每次循环时都重绘屏幕
    screen.blit(background.bg_menu, (0, 0))
    #绘制Play按钮
    play_button.prep_play_button()
    play_button.draw_image_button()
    exit_button.prep_exit_button()
    exit_button.draw_image_button()
    logo.blitme()
    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_screen_playing(ai_settings, screen, blocks, stats, sb, replay_button, back_button, reset_button, background):
    """更新游戏界面屏幕上的图像并切换到新屏幕"""
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    screen.blit(background.bg_playing, (0, 0))
    #绘制游戏框
    background.blitme(background.border, background.border_rect)
    #更新滑块
    update_blocks(ai_settings, screen, blocks)
    sb.show_step()
    #是否产生了最高分？
    if stats.get_best:
        sb.show_best_score()
    #绘制返回和重置按钮
    back_button.prep_back_button()
    back_button.draw_image_button()
    reset_button.prep_reset_button()
    reset_button.draw_image_button()

    #如果游戏处于非活动状态，就绘制rePlay按钮
    if not stats.game_active:
        replay_button.prep_replay_button()
        replay_button.draw_image_button()
        if stats.game_win:
            sb.prep_win()
            sb.show_win()

    #让最近绘制的屏幕可见
    pygame.display.flip()

def check_events(ai_settings, screen, blocks, BLOCKS_ORI, reset_blocks, stats, sb, play_button, replay_button, reset_button, exit_button, back_button, image_list):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, blocks, BLOCKS_ORI, stats, sb)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            if stats.game_menu:
                check_play_button(ai_settings, screen, stats, sb, play_button, blocks, BLOCKS_ORI, reset_blocks, mouse_x, mouse_y, image_list)
                check_exit_button(stats, exit_button, mouse_x, mouse_y)
            else:
                check_replay_button(ai_settings, screen, stats, sb, replay_button, blocks, reset_blocks, mouse_x, mouse_y, image_list)
                check_back_button(ai_settings, stats, back_button, mouse_x, mouse_y)
                check_reset_button(ai_settings, screen, stats, sb, reset_button, mouse_x, mouse_y, blocks, reset_blocks)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, blocks, BLOCKS_ORI, reset_blocks, mouse_x, mouse_y, image_list):
    """在玩家单击Play按钮时调用start_game函数开始新游戏"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        #取消菜单界面 进入游戏界面
        stats.game_menu = False
        start_game(ai_settings, screen, stats, sb, play_button, blocks, reset_blocks, image_list)

def check_replay_button(ai_settings, screen, stats, sb, play_button, blocks, reset_blocks, mouse_x, mouse_y, image_list):
    """在玩家单击Play按钮时调用start_game函数开始新游戏"""
    if play_button.rect.collidepoint(mouse_x, mouse_y) and stats.game_win:
        stats.game_win = False
        start_game(ai_settings, screen, stats, sb, play_button, blocks, reset_blocks, image_list)

def check_exit_button(stats, exit_button, mouse_x, mouse_y):
    """在玩家单击exit按钮时退出游戏"""
    if exit_button.rect.collidepoint(mouse_x, mouse_y):
        #退出游戏
        pygame.quit()
        sys.exit()

def check_back_button(ai_settings, stats, back_button, mouse_x, mouse_y):
    """在玩家单击返回箭头时返回菜单界面"""
    if back_button.rect.collidepoint(mouse_x, mouse_y):
        #返回界面
        stats.game_menu = True
        if not stats.game_win:
            ai_settings.random_col = ai_settings.ZERO_COL
            ai_settings.random_row = ai_settings.ZERO_ROW

def check_reset_button(ai_settings, screen, stats, sb, reset_button, mouse_x, mouse_y, blocks, reset_blocks):
    """在玩家单击刷新时重置步数,同时作为代价相应增加此图的乱序程度"""
    if reset_button.rect.collidepoint(mouse_x, mouse_y):
        block_init(ai_settings, screen, blocks, stats)
        ai_settings.times += ai_settings.times_reset
        stats.step = 0

def start_game(ai_settings, screen, stats, sb, play_button, blocks, reset_blocks, image_list):
    """开始新游戏，清空列表，重置滑块"""
    stats.game_active = True
    #清空列表
    blocks.clear()
    #BLOCKS_ORI.clear()
    #创建新的滑块群
    image_list = init_images()
    create_all_blocks(ai_settings, screen, blocks, image_list)
    block_init(ai_settings, screen, blocks, stats)
    ai_settings.times += ai_settings.times_speed
    
    #重置步数图像
    stats.reset_stats()
    sb.prep_step()


def check_result(ai_settings, blocks, BLOCKS_ORI, stats, sb):
    """检测游戏胜利"""
    if not isinstance(blocks[ai_settings.ZERO_ROW * 3 + ai_settings.ZERO_COL], int):
        return
    i = 0
    for block in blocks:
        if i != (ai_settings.ZERO_ROW * 3 +ai_settings.ZERO_COL):
            if block.num != BLOCKS_ORI[i].num:
                return
        i += 1
    #修改游戏运行和胜利标志
    stats.game_active = False
    stats.game_win = True
    stats.get_best = True
    check_best_score(stats, sb)
    return

def check_keydown_events(event, ai_settings, screen, blocks, BLOCKS_ORI, stats, sb):
    """响应按键"""
    #按Q退出游戏
    if event.key == pygame.K_q:
        sys.exit()
    elif stats.game_active:
        #只有游戏状态标志为true时能移动滑块
        if event.key == pygame.K_RIGHT:
            #向右移动滑块
            block_move_right(ai_settings, screen, blocks, stats)
        elif event.key == pygame.K_LEFT:
            #向左移动滑块
            block_move_left(ai_settings, screen, blocks, stats)
        elif event.key == pygame.K_UP:
            #向上移动滑块
            block_move_up(ai_settings, screen, blocks, stats)
        elif event.key == pygame.K_DOWN:
            #向下移动滑块
            block_move_down(ai_settings, screen, blocks, stats)
        #检测游戏胜利
        check_result(ai_settings, blocks, BLOCKS_ORI, stats, sb)
            

def block_move_right(ai_settings, screen, blocks, stats):
    """向右移动滑块"""
    if ai_settings.random_col != 0:
        blocks[ai_settings.random_row * 3 + ai_settings.random_col] = blocks[ai_settings.random_row * 3 +(ai_settings.random_col-1)]
        width = blocks[ai_settings.random_row * 3 + ai_settings.random_col].rect.width
        #滑块右移一个block.rect.width
        blocks[ai_settings.random_row * 3 + ai_settings.random_col].rect.x += width
        blocks[ai_settings.random_row * 3 +(ai_settings.random_col-1)] = 0
        ai_settings.random_col -= 1
        stats.step += 1
        
def block_move_left(ai_settings, screen, blocks, stats):
    """向左移动滑块"""
    if ai_settings.random_col != 2:
        blocks[ai_settings.random_row * 3 + ai_settings.random_col] = blocks[ai_settings.random_row * 3 +(ai_settings.random_col+1)]
        width = blocks[ai_settings.random_row * 3 + ai_settings.random_col].rect.width
        #滑块左移一个block.rect.width
        blocks[ai_settings.random_row * 3 + ai_settings.random_col].rect.x -= width
        blocks[ai_settings.random_row * 3 +(ai_settings.random_col+1)] = 0
        ai_settings.random_col += 1
        stats.step += 1
        
def block_move_up(ai_settings, screen, blocks, stats):
    """向上移动滑块"""
    if ai_settings.random_row != 2:
        row = ai_settings.random_row+1
        blocks[ai_settings.random_row * 3 + ai_settings.random_col] = blocks[ row* 3 + ai_settings.random_col]
        height = blocks[ai_settings.random_row * 3 + ai_settings.random_col].rect.height
        #滑块上移一个block.rect.width
        blocks[ai_settings.random_row * 3 + ai_settings.random_col].rect.y -= height
        blocks[ row* 3 + ai_settings.random_col] = 0
        ai_settings.random_row += 1
        stats.step += 1

def block_move_down(ai_settings, screen, blocks, stats):
    """向下移动滑块"""
    if ai_settings.random_row != 0:
        blocks[ai_settings.random_row * 3 + ai_settings.random_col] = blocks[(ai_settings.random_row-1) * 3 + ai_settings.random_col]
        height = blocks[ai_settings.random_row * 3 + ai_settings.random_col].rect.height
        #滑块下移一个block.rect.width
        blocks[ai_settings.random_row * 3 + ai_settings.random_col].rect.y += height
        blocks[(ai_settings.random_row-1) * 3 + ai_settings.random_col] = 0
        ai_settings.random_row -= 1
        stats.step += 1

def block_init(ai_settings, screen, blocks, stats):
    """随机移动ai_settings.times次打乱滑块，保证一定有解"""
    for i in range(ai_settings.times):
        random_num = random.randint(0, 3)
        if random_num == 0:
            block_move_up(ai_settings, screen, blocks, stats)
        elif random_num == 1:
            block_move_down(ai_settings, screen, blocks, stats)
        elif random_num == 2:
            block_move_left(ai_settings, screen, blocks, stats)
        elif random_num == 3:
            block_move_right(ai_settings, screen, blocks, stats)

def create_all_blocks(ai_settings, screen, blocks, cut_images):
    """创建滑块群,并生成随机数用于扣去一张图"""
    print(ai_settings.ZERO_ROW, ai_settings.ZERO_COL)
    random_int = ai_settings.random_row * 3 + ai_settings.random_col
    number_blocks_x = 3
    number_rows = 3
    for row_number in range(number_rows):
        for block_number in range(number_blocks_x):
            if (row_number * 3 + block_number) != random_int:
                create_blocks(ai_settings, screen, blocks, block_number, row_number, cut_images[row_number * 3 + block_number])
            else:
                blocks.append(0)

def create_blocks(ai_settings, screen, blocks, block_number, row_number, image_cut):
    """填充滑块编组"""
    #创建一个滑块并计算滑块位置:所有滑块整体要于screen居中
    block = Block(ai_settings, screen, image_cut, row_number * 3 + block_number)
    block_width = block.rect.width
    block.x += block_width * block_number
    block.y += block.rect.height*row_number
    block.rect.x = block.x
    block.rect.y = block.y
    blocks.append(block)

def update_blocks(ai_settings, screen, blocks):
    """更新滑块群中所有滑块的位置"""
    for block in blocks:
        if isinstance(block, Block): 
            block.blitme()
    
def check_best_score(stats, sb):
    """检查是否诞生了最好成绩"""
    if stats.best_score > stats.step:
        stats.best_score = stats.step
        sb.prep_best_score()

