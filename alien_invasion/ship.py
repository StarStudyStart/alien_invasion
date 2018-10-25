import pygame
class Ship():
    """飞船的位置"""
    def __init__(self,ai_settings,screen):
        """初始化飞船的位置"""
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载飞船图像，获取其外界矩形
        self.image = pygame.image.load(r"images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #每艘飞船的初始位置放置在屏幕底部正中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        #移动标志
        self.moving_right = False
        self.moving_left = False
        
        #飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)
        
    def update(self):
        """根据移动标志，调整飞船位置"""
        #更新飞船的center值，而不是centerx
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        
        #根据self.centerg更新rect对象
        self.rect.centerx = self.center
            
    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)
        
    def center_ship(self):
        """将飞船放置到正中央"""
        self.rect.centerx = self.screen_rect.centerx
    
