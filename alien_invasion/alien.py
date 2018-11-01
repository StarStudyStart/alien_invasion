import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self,ai_settings,screen):
        """初始化外星人并设置其初始位置"""
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载外形图像并获取外接矩形
        self.image = pygame.image.load(r"images/alien.bmp")
        self.rect = self.image.get_rect()
        
        #设置外星人初始位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #存储外星人的准确位置
        self.x = float(self.rect.x)
        
    def blitme(self):
        #重写父类blitme方法
        """在指定位置绘制外星人"""
        self.screen.blit(self.image,self.rect)
    
    def check_edge(self):
        """检查外星人是否达到了屏幕边缘"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
            
    def update(self):
        '''向左或向右移动外星人'''
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
            
        
        
        
    
