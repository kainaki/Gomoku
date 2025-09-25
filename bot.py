import random
from config import config

class GomokuBot:
    def __init__(self, game):
        self.game = game
        self.difficulty = config.difficulty
        
    def make_move(self):
        if self.difficulty == 'easy':
            return self.easy_move()
        elif self.difficulty == 'medium':
            return self.medium_move()
        elif self.difficulty == 'hard':
            return self.hard_move()
        else:
            return self.easy_move()  # fallback
    
    def easy_move(self):
        empty_cells = []
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.board[i][j] is None:
                    empty_cells.append((i, j))
        
        if empty_cells:
            return random.choice(empty_cells)
        return None
    
    def medium_move(self):
        winning_move = self.find_winning_move(self.game.current_player)
        if winning_move:
            return winning_move

        opponent = 'black' if self.game.current_player == 'white' else 'white'
        blocking_move = self.find_winning_move(opponent)
        if blocking_move:
            return blocking_move

        threat_move = self.find_threat_move(opponent)
        if threat_move:
            return threat_move

        own_threat = self.find_threat_move(self.game.current_player)
        if own_threat:
            return own_threat

        return self.strategic_move()
    
    def hard_move(self):
        winning_move = self.find_winning_move(self.game.current_player)
        if winning_move:
            return winning_move
        
        opponent = 'black' if self.game.current_player == 'white' else 'white'
        blocking_move = self.find_winning_move(opponent)
        if blocking_move:
            return blocking_move

        fork_move = self.find_fork_move()
        if fork_move:
            return fork_move

        opponent_fork_block = self.block_opponent_fork()
        if opponent_fork_block:
            return opponent_fork_block
        
        return self.advanced_evaluate_board()
    
    def find_winning_move(self, player):
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.board[i][j] is None:
                    self.game.board[i][j] = player
                    if self.game.check_win(i, j):
                        self.game.board[i][j] = None
                        return (i, j)
                    self.game.board[i][j] = None
        return None
    
    def find_threat_move(self, player, length=4):
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.board[i][j] is None:
                    if self.check_potential_line(player, i, j, length):
                        return (i, j)
        return None
    
    def check_potential_line(self, player, row, col, target_length):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = 0
            gaps = 0
            
            for direction in [1, -1]:
                consecutive = True
                for step in range(1, target_length):
                    r = row + dx * step * direction
                    c = col + dy * step * direction
                    
                    if not (0 <= r < self.game.board_size and 0 <= c < self.game.board_size):
                        consecutive = False
                        break
                    
                    if self.game.board[r][c] == player:
                        count += 1
                    elif self.game.board[r][c] is None:
                        gaps += 1
                        if gaps > 1:
                            consecutive = False
                            break
                    else:
                        consecutive = False
                        break
                
                if not consecutive:
                    break
            
            if count >= target_length - 1 and gaps <= 2:
                return True
        
        return False
    
    def strategic_move(self):
        empty_cells = []
        center = self.game.board_size // 2
        
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.board[i][j] is None:
                    # Базовый вес на основе позиции
                    weight = 0
                    
                    distance_to_center = abs(i - center) + abs(j - center)
                    weight += (self.game.board_size - distance_to_center) * 2                    
                    weight += self.evaluate_position(i, j, self.game.current_player) * 3                    
                    opponent = 'black' if self.game.current_player == 'white' else 'white'
                    weight += self.evaluate_position(i, j, opponent) * 2                    
                    empty_cells.append(((i, j), weight))
        
        if not empty_cells:
            return None
            
        empty_cells.sort(key=lambda x: x[1], reverse=True)
        return empty_cells[0][0]
    
    def evaluate_position(self, row, col, player):
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            line_score = 0
            for direction in [1, -1]:
                consecutive = 0
                for step in range(1, 5):
                    r = row + dx * step * direction
                    c = col + dy * step * direction
                    
                    if not (0 <= r < self.game.board_size and 0 <= c < self.game.board_size):
                        break
                    
                    if self.game.board[r][c] == player:
                        consecutive += 1
                    elif self.game.board[r][c] is None:
                        continue
                    else:
                        break
                
                line_score += consecutive
            
            if line_score >= 2:
                score += line_score * line_score
        
        return score
    
    def find_fork_move(self):
        opponent = 'black' if self.game.current_player == 'white' else 'white'
        best_fork = None
        best_fork_score = 0
        
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.board[i][j] is None:
                    fork_score = self.calculate_fork_potential(i, j)
                    
                    if fork_score > best_fork_score:
                        best_fork_score = fork_score
                        best_fork = (i, j)
        
        return best_fork if best_fork_score >= 2 else None
    
    def calculate_fork_potential(self, row, col):
        threats = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        self.game.board[row][col] = self.game.current_player

        for dx, dy in directions:
            for direction in [1, -1]:
                if self.check_direction_potential(row, col, dx, dy, direction, 4):
                    threats += 1
                    if threats >= 2:
                        self.game.board[row][col] = None
                        return threats
        
        self.game.board[row][col] = None
        return threats
    
    def check_direction_potential(self, row, col, dx, dy, direction, length):
        count = 1
        
        for step in range(1, length):
            r = row + dx * step * direction
            c = col + dy * step * direction
            
            if not (0 <= r < self.game.board_size and 0 <= c < self.game.board_size):
                return False
            
            if self.game.board[r][c] == self.game.current_player:
                count += 1
            elif self.game.board[r][c] is not None:
                return False
        
        return count >= length - 1
    
    def block_opponent_fork(self):
        opponent = 'black' if self.game.current_player == 'white' else 'white'
        fork_blocks = []
        
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.board[i][j] is None:
                    self.game.board[i][j] = opponent
                    fork_score = self.calculate_fork_potential(i, j)
                    self.game.board[i][j] = None
                    
                    if fork_score >= 2:
                        fork_blocks.append((i, j))
        
        return random.choice(fork_blocks) if fork_blocks else None
    
    def advanced_evaluate_board(self):
        empty_cells = []
        
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.board[i][j] is None:
                    score = self.cell_score(i, j)
                    empty_cells.append(((i, j), score))
        
        if not empty_cells:
            return None
            
        empty_cells.sort(key=lambda x: x[1], reverse=True)
        if len(empty_cells) > 3 and random.random() < 0.1:
            return empty_cells[random.randint(1, 3)][0]
        
        return empty_cells[0][0]
    
    def cell_score(self, row, col):
        score = 0
        center = self.game.board_size // 2
        distance = abs(row - center) + abs(col - center)
        score += (self.game.board_size * 2 - distance) * 10
        score += self.evaluate_patterns(row, col, self.game.current_player) * 100
        opponent = 'black' if self.game.current_player == 'white' else 'white'
        score += self.evaluate_patterns(row, col, opponent) * 80
        score += self.evaluate_line_potential(row, col) * 50
        
        return score
    
    def evaluate_patterns(self, row, col, player):
        patterns = {
            'five': 100000,      
            'open_four': 10000,  
            'four': 1000,        
            'open_three': 500,   
            'three': 200,        
            'open_two': 50,      
            'two': 10           
        }
        
        total_score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            for direction in [1, -1]:
                pattern_score = self.analyze_direction(row, col, dx, dy, direction, player, patterns)
                total_score += pattern_score
        
        return total_score
    
    def analyze_direction(self, row, col, dx, dy, direction, player, patterns):
        self.game.board[row][col] = player
        
        count = 1
        open_ends = 0

        for step in range(1, 6):
            r = row + dx * step * direction
            c = col + dy * step * direction
            
            if not (0 <= r < self.game.board_size and 0 <= c < self.game.board_size):
                break
            
            if self.game.board[r][c] == player:
                count += 1
            elif self.game.board[r][c] is None:
                open_ends += 1
                break
            else:
                break
        
        for step in range(1, 6):
            r = row - dx * step * direction
            c = col - dy * step * direction
            
            if not (0 <= r < self.game.board_size and 0 <= c < self.game.board_size):
                break
            
            if self.game.board[r][c] == player:
                count += 1
            elif self.game.board[r][c] is None:
                open_ends += 1
                break
            else:
                break
        
        self.game.board[row][col] = None
        if count >= 5:
            return patterns['five']
        elif count == 4:
            return patterns['open_four'] if open_ends >= 2 else patterns['four']
        elif count == 3:
            return patterns['open_three'] if open_ends >= 2 else patterns['three']
        elif count == 2:
            return patterns['open_two'] if open_ends >= 2 else patterns['two']
        
        return 0
    
    def evaluate_line_potential(self, row, col):
        potential = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            space = self.check_available_space(row, col, dx, dy)
            potential += space * 5
        
        return potential
    
    def check_available_space(self, row, col, dx, dy):
        space = 0
        
        for direction in [1, -1]:
            for step in range(1, 6):
                r = row + dx * step * direction
                c = col + dy * step * direction
                
                if not (0 <= r < self.game.board_size and 0 <= c < self.game.board_size):
                    break
                
                if self.game.board[r][c] is None:
                    space += 1
                else:
                    break
        
        return space