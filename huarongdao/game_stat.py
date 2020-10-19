class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings,blocks = []):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #游戏刚启动时处于非活动非胜利状态
        self.game_menu = True
        self.game_active = False
        self.game_win = False
        #在任何情况下都不应该重置最短步数
        self.best_score = 9999999
        self.blocks = blocks
        self.reset_blocks = blocks
        self.get_best = False
        self.reset = False
    
    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.step = 0
        