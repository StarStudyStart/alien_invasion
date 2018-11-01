#coding:utf-8
import json

from ship import Ship

class GameStats():
    """跟踪游戏的统计信息"""
    
    def __init__(self,ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.read_high_score()
        self.reset_stats()
              
        #游戏刚启动时处于活动状态
        self.game_active = False
        
    def read_high_score(self):
        """读取历史最高分数"""
        try:
            with open("./high_socre.txt",'r') as f:
                self.high_score = json.load(f)['best_score']               
        except FileNotFoundError:
            self.high_score = 0
            
        
    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
