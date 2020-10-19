import pygame.font
from pygame.sprite import Group
from block import Block
class Stepboard():
    """显示步数和通关信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        #显示信息时使用的字体设置
        self.win_text_color = (255, 215, 0)
        self.step_text_color = (64, 224, 208)
        #准备通关信息
        self.prep_win()

    def prep_win(self):
        """通关信息图像"""
        self.win_image = pygame.image.load('images_material/win.png')
        self.win_image = pygame.transform.smoothscale(self.win_image, (450, 350))
        """将通关信息放在屏幕中央"""
        self.win_rect = self.win_image.get_rect()
        
        self.win_rect.centerx = self.screen_rect.centerx
        self.win_rect.centery = self.screen_rect.centery
        #在logo的center属性中存储小数值


    def prep_step(self):
        """准备步数"""
        self.step_image_bottom = pygame.image.load("images_material/step.png")
        self.step_image_bottom = pygame.transform.smoothscale(self.step_image_bottom,(300, 80))
        self.step_image_rect = self.step_image_bottom.get_rect()
        self.step_image_rect.centerx = self.screen_rect.centerx - 10
        self.step_image_rect.top = 0
        """将步数信息转换为一副渲染的图像"""
        self.font = pygame.font.SysFont(None, 60)
        step_str = str(self.stats.step)
        self.step_image = self.font.render(step_str, True, self.step_text_color)
        """将步数信息放在屏幕正上方"""
        self.step_rect = self.step_image.get_rect()
        self.step_rect.centerx = self.screen_rect.centerx + 70
        self.step_rect.top = 26

    def prep_best_score(self):
        """准备最好成绩"""
        self.stats.best_score = self.stats.step
        self.step_image_best = pygame.image.load("images_material/best_score.png")
        self.step_image_best = pygame.transform.smoothscale(self.step_image_best,(400, 130))
        self.step_image_best_rect = self.step_image_best.get_rect()
        self.step_image_best_rect.left = self.screen_rect.left
        self.step_image_best_rect.bottom = self.screen_rect.bottom
        """将步数信息转换为一副渲染的图像"""
        self.font = pygame.font.SysFont(None, 68)
        step_str = str(self.stats.best_score)
        self.step_best_font = self.font.render(step_str, True, (255, 0, 0))
        """将步数信息放在屏幕左下方"""
        self.step_best_rect = self.step_best_font.get_rect()
        self.step_best_rect.left = self.screen_rect.left + 320
        self.step_best_rect.bottom = self.screen_rect.bottom - 30

    def show_win(self):
        """在屏幕上显示通关信息"""
        self.screen.blit(self.win_image, self.win_rect)
        
    def show_step(self):
        """在屏幕上显示步数"""
        self.prep_step()
        self.screen.blit(self.step_image_bottom, self.step_image_rect)
        self.screen.blit(self.step_image, self.step_rect)

    def show_best_score(self):
        """在屏幕上显示最佳步数"""
        self.screen.blit(self.step_image_best, self.step_image_best_rect)
        self.screen.blit(self.step_best_font, self.step_best_rect)
 