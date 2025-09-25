from config import config

class GomokuGame:
    def __init__(self, lang):
        self.board_size = config.board_size
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'black'
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.move_count = 0
        self.lang = lang

        self.win_cache = {}
        
        # Color codes
        self.colors = {
            'black': self.get_color_code(config.black_color),
            'white': self.get_color_code(config.white_color),
            'reset': '\033[0m',
            'cursor': '\033[93m',
            'grid': '\033[90m',
            'bright_black': '\033[1;30m',  
            'bright_white': '\033[1;37m',  
            'bright_red': '\033[1;31m',    
            'bright_green': '\033[1;32m',  
            'bright_yellow': '\033[1;33m', 
            'bright_blue': '\033[1;34m',   
            'bright_magenta': '\033[1;35m',
            'bright_cyan': '\033[1;36m'    
        }
        
        self.grid_lines = self._precalculate_grid()
    
    def _precalculate_grid(self):
        lines = []

        lines.append(f"{self.colors['grid']}  ┌{'───┬' * (self.board_size - 1)}───┐{self.colors['reset']}")
        
        for i in range(self.board_size):
            if i < self.board_size - 1:
                lines.append(f"{self.colors['grid']}  ├{'───┼' * (self.board_size - 1)}───┤{self.colors['reset']}")
            else:
                lines.append(f"{self.colors['grid']}  └{'───┴' * (self.board_size - 1)}───┘{self.colors['reset']}")
        
        return lines
    
    def get_color_code(self, color_name):
        colors = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m'
        }
        return colors.get(color_name, '\033[37m')
    
    def get_bright_color_code(self, color_name):
        bright_colors = {
            'black': '\033[1;30m',
            'red': '\033[1;31m',
            'green': '\033[1;32m',
            'yellow': '\033[1;33m',
            'blue': '\033[1;34m',
            'magenta': '\033[1;35m',
            'cyan': '\033[1;36m',
            'white': '\033[1;37m'
        }
        return bright_colors.get(color_name, '\033[1;37m')
    
    def display_board(self, selected_cell=None):
        print(self.grid_lines[0])
        
        for i, row in enumerate(self.board):
            line = f"{self.colors['grid']}  │{self.colors['reset']}"
            
            for j, cell in enumerate(row):
                is_selected = selected_cell and selected_cell[0] == i and selected_cell[1] == j
                is_last_move = self.last_move and self.last_move[0] == i and self.last_move[1] == j
                
                if is_last_move:
                    if cell == 'black':
                        bright_color = self.get_bright_color_code(config.black_color)
                        symbol = f"{bright_color}●{self.colors['reset']}"
                    elif cell == 'white':
                        bright_color = self.get_bright_color_code(config.white_color)
                        symbol = f"{bright_color}●{self.colors['reset']}"
                    else:
                        symbol = f"{self.colors['grid']}∙{self.colors['reset']}"
                elif is_selected:
                    if cell == 'black':
                        symbol = f"{self.colors['cursor']}◉{self.colors['reset']}"
                    elif cell == 'white':
                        symbol = f"{self.colors['cursor']}◌{self.colors['reset']}"
                    else:
                        symbol = f"{self.colors['cursor']}✧{self.colors['reset']}"
                else:
                    if cell == 'black':
                        symbol = f"{self.colors['black']}●{self.colors['reset']}"
                    elif cell == 'white':
                        symbol = f"{self.colors['white']}○{self.colors['reset']}"
                    else:
                        symbol = f"{self.colors['grid']}∙{self.colors['reset']}"
                
                line += f" {symbol} {self.colors['grid']}│{self.colors['reset']}"
            
            print(line)
            
            if i < self.board_size - 1:
                print(self.grid_lines[i + 1])
        
        print(self.grid_lines[-1])
        
        black_symbol = f"{self.colors['black']}●{self.colors['reset']}"
        white_symbol = f"{self.colors['white']}○{self.colors['reset']}"
        cursor_symbol = f"{self.colors['cursor']}✧{self.colors['reset']}"
        
        bright_black = f"{self.get_bright_color_code(config.black_color)}●{self.colors['reset']}"
        bright_white = f"{self.get_bright_color_code(config.white_color)}●{self.colors['reset']}"
        
        if self.last_move:
            row, col = self.last_move
            player = self.board[row][col]
            player_name = self.lang.get('color_black', 'Black') if player == "black" else self.lang.get('color_white', 'White')
            if config.language == 'ru_ru':
                print(f"Последний ход: {player_name} ({row}, {col})")
            else:
                print(f"Last move: {player_name} ({row}, {col})")
    
    def make_move(self, row, col):
        if self.board[row][col] is None and not self.game_over:
            self.board[row][col] = self.current_player
            self.last_move = (row, col)
            self.move_count += 1
            
            if self.fast_check_win(row, col):
                self.game_over = True
                self.winner = self.current_player
            elif self.move_count == self.board_size * self.board_size:
                self.game_over = True
            else:
                self.current_player = 'white' if self.current_player == 'black' else 'black'
            return True
        return False
    
    def fast_check_win(self, row, col):
        """Оптимизированная проверка победы"""
        player = self.board[row][col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = 1
            
            for direction in [1, -1]:
                r, c = row, col
                for _ in range(4):
                    r += dx * direction
                    c += dy * direction
                    
                    if not (0 <= r < self.board_size and 0 <= c < self.board_size):
                        break
                    
                    if self.board[r][c] == player:
                        count += 1
                    else:
                        break
                    
                    if count >= 5:
                        return True
        
        return False
    
    def check_win(self, row, col):
        """Полная проверка победы (для бота)"""
        return self.fast_check_win(row, col)
    
    def is_board_full(self):
        return self.move_count == self.board_size * self.board_size
    
    def reset_game(self):
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'black'
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.move_count = 0
        self.win_cache.clear()