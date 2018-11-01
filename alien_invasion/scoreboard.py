# coing:utf-8
import pygame
from pygame.sprite import Group

from ship import Ship

class ScoreBoard():
    """显示得分信息的类"""
    
    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        
        #显示得分时用到的信息
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        
        #准备初始化当前的分图像、最高分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        
    def prep_score(self):
        """将文字转化为图像对象，初始化记分板位置"""
        round_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(round_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                self.ai_settings.bg_color)
            
        #初始化记分板位置
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 
        self.score_rect.top = 20
        
    def prep_high_score(self):
        """将最高分转化为渲染图象"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
                self.ai_settings.bg_color)
        
        #初始化最高分位置
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20
        
    def prep_level(self):
        """显示玩家等级"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                self.text_color, self.ai_settings.bg_color)
         
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20   
        self.level_rect.top = self.score_rect.bottom + 10
        
    def prep_ships(self):
        """显示还剩余多少飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
         
    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #绘制飞船
        self.ships.draw(self.screen)
        

        
            
        
