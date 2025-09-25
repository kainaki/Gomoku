import json
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.stats_file = 'stats.json'
        self._init_stats()
        
    def _init_stats(self):
        if not os.path.exists(self.stats_file):
            default_stats = {
                "total_games": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "win_streak": 0,
                "max_win_streak": 0,
                "games": []
            }
            self._save_stats(default_stats)
    
    def _load_stats(self):
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            self._init_stats()
            return self._load_stats()
    
    def _save_stats(self, stats):
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving stats: {e}")
    
    def add_game_result(self, result, difficulty, board_size):
        """Result: 'win', 'loss', 'draw'"""
        stats = self._load_stats()
        
        stats["total_games"] += 1
        
        if result == "win":
            stats["wins"] += 1
            stats["win_streak"] += 1
            stats["max_win_streak"] = max(stats["max_win_streak"], stats["win_streak"])
        elif result == "loss":
            stats["losses"] += 1
            stats["win_streak"] = 0
        elif result == "draw":
            stats["draws"] += 1
            stats["win_streak"] = 0
        
        game_record = {
            "date": datetime.now().isoformat(),
            "result": result,
            "difficulty": difficulty,
            "board_size": board_size
        }
        stats["games"].append(game_record)
        
        if len(stats["games"]) > 100:
            stats["games"] = stats["games"][-100:]
        
        self._save_stats(stats)
    
    def get_stats(self):
        stats = self._load_stats()
        if stats["total_games"] > 0:
            win_rate = (stats["wins"] / stats["total_games"]) * 100
        else:
            win_rate = 0
            
        return {
            "total_games": stats["total_games"],
            "wins": stats["wins"],
            "losses": stats["losses"],
            "draws": stats["draws"],
            "win_rate": round(win_rate, 1),
            "win_streak": stats["win_streak"],
            "max_win_streak": stats["max_win_streak"]
        }

database = Database()