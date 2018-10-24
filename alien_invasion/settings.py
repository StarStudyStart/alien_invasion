class Settings():
    """存储外星人入侵的所有设置类"""
    def __init__(self):
        """初始化屏幕设置"""
        #游戏设置
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230,230,230)
        
        #飞船速度
        self.ship_speed_factor = 1.5
        
        #子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 5
        self.bullet_height = 12
        self.bullet_color = 60,60,60
        self.bullet_allowed = 3
        
        #外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        #1 表示右移 -1 表示左移
        self.fleet_direction = 1
        
        
