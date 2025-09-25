import json
import os

class Config:
    def __init__(self):
        self.language = "en_us"
        self.board_size = 9
        self.difficulty = "medium"
        self.player_color = "black"
        self.black_color = "blue"
        self.white_color = "red"
        self.search_depth = {"easy": 1, "medium": 2, "hard": 4}
        
    def load_config(self):
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.language = data.get('language', self.language)
                    self.board_size = data.get('board_size', self.board_size)
                    self.difficulty = data.get('difficulty', self.difficulty)
                    self.player_color = data.get('player_color', self.player_color)
                    self.black_color = data.get('black_color', self.black_color)
                    self.white_color = data.get('white_color', self.white_color)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.save_config()
            
    def save_config(self):
        data = {
            'language': self.language,
            'board_size': self.board_size,
            'difficulty': self.difficulty,
            'player_color': self.player_color,
            'black_color': self.black_color,
            'white_color': self.white_color
        }
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

config = Config()