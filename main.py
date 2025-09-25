import os
import sys
import json
import msvcrt
from game import GomokuGame
from bot import GomokuBot
from config import config
from database import database

class GomokuApp:
    def __init__(self):
        config.load_config()
        self.lang = self.load_language()
        self.game = None
        self.bot = None
        self.current_screen = "menu"
        self.selected_cell = None
        
    def load_language(self):
        try:
            lang_file = f'lang/{config.language}.json'
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading language: {e}")
        
        # Fallback to English
        return {
            "game_title": "Gomoku",
            "menu_play": "Play",
            "menu_settings": "Settings",
            "menu_stats": "Statistics",
            "menu_exit": "Exit",
            "settings_title": "Settings",
            "stats_title": "Statistics",
            "settings_language": "Language",
            "settings_board_size": "Board size",
            "settings_difficulty": "Difficulty",
            "settings_player_color": "Your color",
            "settings_black_color": "Black stone color",
            "settings_white_color": "White stone color",
            "stats_games_played": "Games played",
            "stats_wins": "Wins",
            "stats_losses": "Losses",
            "stats_draws": "Draws",
            "stats_win_rate": "Win rate",
            "stats_win_streak": "Current streak",
            "stats_max_streak": "Max streak",
            "difficulty_easy": "Easy",
            "difficulty_medium": "Medium",
            "difficulty_hard": "Hard",
            "color_black": "Black",
            "color_white": "White",
            "game_restart": "New game",
            "game_main_menu": "Main menu",
            "game_turn": "Move",
            "game_winner_black": "Black wins!",
            "game_winner_white": "White wins!",
            "game_draw": "Draw!",
            "game_bot_thinking": "Bot thinking...",
            "press_enter": "Press Enter to continue...",
            "invalid_choice": "Invalid choice.",
            "select_option": "Select option",
            "select_cell": "Selected cell",
            "invalid_move": "Invalid move!",
            "cell_occupied": "Cell is already occupied.",
            "game_interrupted": "Game interrupted.",
            "available_commands": "Commands: ←→↑↓ - navigate, SPACE - place stone, Q - quit, R - restart, M - menu",
            "color_red": "Red",
            "color_blue": "Blue",
            "color_green": "Green",
            "color_yellow": "Yellow",
            "color_magenta": "Magenta",
            "color_cyan": "Cyan",
            "color_white": "White",
            "color_black": "Black",
            "back_to_menu": "Back to menu",
            "player_move": "Player move at",
            "bot_move": "Bot move at"
        }
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def wait_for_enter(self):
        input(f"\n{self.lang.get('press_enter', 'Press Enter to continue...')}")
    
    def get_key(self):
        """Получает нажатую клавишу без ожидания Enter"""
        if os.name == 'nt':
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                return key
            return key
        else:

            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
    
    def display_menu(self):
        self.clear_screen()
        title = self.lang.get("game_title", "Gomoku")
        
        if config.language == 'ru_ru':
            print("╔══════════════════════════════════════════════════╗")
            print(f"║{title:^50}║")
            print("╠══════════════════════════════════════════════════╣")
            
            menu_items = [
                f"1. {self.lang.get('menu_play', 'Играть')}",
                f"2. {self.lang.get('menu_settings', 'Настройки')}",
                f"3. {self.lang.get('menu_stats', 'Статистика')}",
                f"4. {self.lang.get('menu_exit', 'Выход')}"
            ]
            
            for item in menu_items:
                print(f"║ {item:<48} ║")
            
            print("╚══════════════════════════════════════════════════╝")
        else:
            print("╔══════════════════════════════════════════╗")
            print(f"║{title:^42}║")
            print("╠══════════════════════════════════════════╣")
            
            menu_items = [
                f"1. {self.lang.get('menu_play', 'Play')}",
                f"2. {self.lang.get('menu_settings', 'Settings')}",
                f"3. {self.lang.get('menu_stats', 'Statistics')}",
                f"4. {self.lang.get('menu_exit', 'Exit')}"
            ]
            
            for item in menu_items:
                print(f"║ {item:<40} ║")
            
            print("╚══════════════════════════════════════════╝")

    def display_settings(self):
        self.clear_screen()
        title = self.lang.get("settings_title", "Settings")
        
        if config.language == 'ru_ru':
            print("╔══════════════════════════════════════════════════╗")
            print(f"║{title:^50}║")
            print("╠══════════════════════════════════════════════════╣")
            print(f"║ 1. {self.lang.get('settings_language', 'Язык')}: {config.language:<36}    ║")
            print(f"║ 2. {self.lang.get('settings_board_size', 'Размер доски')}: {config.board_size:<32}║")
            print(f"║ 3. {self.lang.get('settings_difficulty', 'Сложность')}: {config.difficulty:<33}  ║")
            print(f"║ 4. {self.lang.get('settings_player_color', 'Ваш цвет')}: {config.player_color:<30}      ║")
            print(f"║ 5. {self.lang.get('settings_black_color', 'Цвет черных камней')}: {config.black_color:<20}      ║")
            print(f"║ 6. {self.lang.get('settings_white_color', 'Цвет белых камней')}: {config.white_color:<20}       ║")
            print(f"║ 7. {self.lang.get('back_to_menu', 'Вернуться в меню'):<36}          ║")
            print("╚══════════════════════════════════════════════════╝")
        else:
            print("╔══════════════════════════════════════════╗")
            print(f"║{title:^42}║")
            print("╠══════════════════════════════════════════╣")
            print(f"║ 1. {self.lang.get('settings_language', 'Language')}: {config.language:<26}  ║")
            print(f"║ 2. {self.lang.get('settings_board_size', 'Board size')}: {config.board_size:<16}          ║")
            print(f"║ 3. {self.lang.get('settings_difficulty', 'Difficulty')}: {config.difficulty:<24}  ║")
            print(f"║ 4. {self.lang.get('settings_player_color', 'Your color')}: {config.player_color:<16}          ║")
            print(f"║ 5. {self.lang.get('settings_black_color', 'Black stone color')}: {config.black_color:<10}         ║")
            print(f"║ 6. {self.lang.get('settings_white_color', 'White stone color')}: {config.white_color:<10}         ║")
            print(f"║ 7. {self.lang.get('back_to_menu', 'Back to menu'):<30}        ║")
            print("╚══════════════════════════════════════════╝")

    def display_stats(self):
        self.clear_screen()
        stats = database.get_stats()
        title = self.lang.get("stats_title", "Statistics")
        
        if config.language == 'ru_ru':
            print("╔════════════════════════════════════════════════════╗")
            print(f"║{title:^52}║")
            print("╠════════════════════════════════════════════════════╣")
            
            print(f"║ {self.lang.get('stats_games_played', 'Сыграно игр')}: {stats['total_games']:<29}         ║")
            print(f"║ {self.lang.get('stats_wins', 'Победы')}: {stats['wins']:<42} ║")
            print(f"║ {self.lang.get('stats_losses', 'Поражения')}: {stats['losses']:<38}  ║")
            print(f"║ {self.lang.get('stats_draws', 'Ничьи')}: {stats['draws']:<41}   ║")
            print(f"║ {self.lang.get('stats_win_rate', 'Процент побед')}: {stats['win_rate']}%{'':<26}        ║")
            print(f"║ {self.lang.get('stats_win_streak', 'Текущая серия')}: {stats['win_streak']:<25}           ║")
            print(f"║ {self.lang.get('stats_max_streak', 'Макс. серия')}: {stats['max_win_streak']:<32}      ║")
            
            print("╚════════════════════════════════════════════════════╝")
        else:
            print("╔══════════════════════════════════════════════╗")
            print(f"║{title:^46}║")
            print("╠══════════════════════════════════════════════╣")
            
            print(f"║ {self.lang.get('stats_games_played', 'Games played')}: {stats['total_games']:<21}          ║")
            print(f"║ {self.lang.get('stats_wins', 'Wins')}: {stats['wins']:<36}   ║")
            print(f"║ {self.lang.get('stats_losses', 'Losses')}: {stats['losses']:<34}   ║")
            print(f"║ {self.lang.get('stats_draws', 'Draws')}: {stats['draws']:<35}   ║")
            print(f"║ {self.lang.get('stats_win_rate', 'Win rate')}: {stats['win_rate']}%{'':<26}       ║")
            print(f"║ {self.lang.get('stats_win_streak', 'Current streak')}: {stats['win_streak']:<17}            ║")
            print(f"║ {self.lang.get('stats_max_streak', 'Max streak')}: {stats['max_win_streak']:<23}          ║")
            
            print("╚══════════════════════════════════════════════╝")
    
    def run(self):
        while True:
            if self.current_screen == "menu":
                self.show_menu()
            elif self.current_screen == "game":
                self.run_game()
            elif self.current_screen == "settings":
                self.show_settings()
            elif self.current_screen == "stats":
                self.show_stats()
    
    def show_menu(self):
        while True:
            self.display_menu()
            choice = input(f"\n{self.lang.get('select_option', 'Select option')} (1-4): ").strip()
            
            if choice == "1":
                self.start_game()
                break
            elif choice == "2":
                self.current_screen = "settings"
                break
            elif choice == "3":
                self.current_screen = "stats"
                break
            elif choice == "4":
                if config.language == 'ru_ru':
                    print("До свидания!")
                else:
                    print("Goodbye!")
                sys.exit()
            else:
                print(self.lang.get('invalid_choice', 'Invalid choice.'))
                self.wait_for_enter()
    
    def show_settings(self):
        while True:
            self.display_settings()
            choice = input(f"\n{self.lang.get('select_option', 'Select option')} (1-7): ").strip()
            
            if choice == "1":
                self.change_language()
            elif choice == "2":
                self.change_board_size()
            elif choice == "3":
                self.change_difficulty()
            elif choice == "4":
                self.change_player_color()
            elif choice == "5":
                self.change_black_color()
            elif choice == "6":
                self.change_white_color()
            elif choice == "7":
                self.current_screen = "menu"
                break
            else:
                print(self.lang.get('invalid_choice', 'Invalid choice.'))
                self.wait_for_enter()
    
    def show_stats(self):
        self.display_stats()
        self.wait_for_enter()
        self.current_screen = "menu"
    
    def change_language(self):
        print(f"\n{self.lang.get('settings_language', 'Language')}:")
        print("1. Русский (ru_ru)")
        print("2. English (en_us)")
        
        choice = input(f"{self.lang.get('select_option', 'Select option')} (1-2): ").strip()
        
        if choice == "1":
            config.language = "ru_ru"
        elif choice == "2":
            config.language = "en_us"
        else:
            print(self.lang.get('invalid_choice', 'Invalid choice.'))
            self.wait_for_enter()
            return
        
        config.save_config()
        self.lang = self.load_language()
        if config.language == 'ru_ru':
            print("✓ Язык изменен успешно!")
        else:
            print("✓ Language changed successfully!")
        self.wait_for_enter()
    
    def change_board_size(self):
        try:
            size = int(input(f"{self.lang.get('settings_board_size', 'Board size')} (5-15): "))
            if 5 <= size <= 15:
                config.board_size = size
                config.save_config()
                if config.language == 'ru_ru':
                    print("✓ Размер доски изменен успешно!")
                else:
                    print("✓ Board size changed successfully!")
            else:
                if config.language == 'ru_ru':
                    print("Размер доски должен быть от 5 до 15.")
                else:
                    print("Board size must be between 5 and 15.")
        except ValueError:
            if config.language == 'ru_ru':
                print("Пожалуйста, введите число.")
            else:
                print("Please enter a valid number.")
        self.wait_for_enter()
    
    def change_difficulty(self):
        print(f"\n{self.lang.get('settings_difficulty', 'Difficulty')}:")
        print(f"1. {self.lang.get('difficulty_easy', 'Easy')}")
        print(f"2. {self.lang.get('difficulty_medium', 'Medium')}")
        print(f"3. {self.lang.get('difficulty_hard', 'Hard')}")
        
        choice = input(f"{self.lang.get('select_option', 'Select option')} (1-3): ").strip()
        
        difficulties = {"1": "easy", "2": "medium", "3": "hard"}
        if choice in difficulties:
            config.difficulty = difficulties[choice]
            config.save_config()
            if config.language == 'ru_ru':
                print("✓ Сложность изменена успешно!")
            else:
                print("✓ Difficulty changed successfully!")
        else:
            print(self.lang.get('invalid_choice', 'Invalid choice.'))
        self.wait_for_enter()
    
    def change_player_color(self):
        print(f"\n{self.lang.get('settings_player_color', 'Your color')}:")
        print(f"1. {self.lang.get('color_black', 'Black')} ({self.lang.get('game_restart', 'first move')})")
        print(f"2. {self.lang.get('color_white', 'White')} ({self.lang.get('game_main_menu', 'second move')})")
        
        choice = input(f"{self.lang.get('select_option', 'Select option')} (1-2): ").strip()
        
        if choice == "1":
            config.player_color = "black"
        elif choice == "2":
            config.player_color = "white"
        else:
            print(self.lang.get('invalid_choice', 'Invalid choice.'))
            self.wait_for_enter()
            return
        
        config.save_config()
        if config.language == 'ru_ru':
            print("✓ Цвет игрока изменен успешно!")
        else:
            print("✓ Player color changed successfully!")
        self.wait_for_enter()
    
    def change_black_color(self):
        print(f"\n{self.lang.get('settings_black_color', 'Black stone color')}:")
        colors = ["red", "blue", "green", "yellow", "magenta", "cyan", "black", "white"]
        for i, color in enumerate(colors, 1):
            print(f"{i}. {self.lang.get(f'color_{color}', color.capitalize())}")
        
        try:
            choice = int(input(f"{self.lang.get('select_option', 'Select option')} (1-{len(colors)}): ").strip())
            if 1 <= choice <= len(colors):
                config.black_color = colors[choice - 1]
                config.save_config()
                if config.language == 'ru_ru':
                    print("✓ Цвет черных камней изменен успешно!")
                else:
                    print("✓ Black stone color changed successfully!")
            else:
                print(self.lang.get('invalid_choice', 'Invalid choice.'))
        except ValueError:
            print(self.lang.get('invalid_choice', 'Invalid choice.'))
        self.wait_for_enter()
    
    def change_white_color(self):
        print(f"\n{self.lang.get('settings_white_color', 'White stone color')}:")
        colors = ["red", "blue", "green", "yellow", "magenta", "cyan", "black", "white"]
        for i, color in enumerate(colors, 1):
            print(f"{i}. {self.lang.get(f'color_{color}', color.capitalize())}")
        
        try:
            choice = int(input(f"{self.lang.get('select_option', 'Select option')} (1-{len(colors)}): ").strip())
            if 1 <= choice <= len(colors):
                config.white_color = colors[choice - 1]
                config.save_config()
                if config.language == 'ru_ru':
                    print("✓ Цвет белых камней изменен успешно!")
                else:
                    print("✓ White stone color changed successfully!")
            else:
                print(self.lang.get('invalid_choice', 'Invalid choice.'))
        except ValueError:
            print(self.lang.get('invalid_choice', 'Invalid choice.'))
        self.wait_for_enter()
    
    def start_game(self):
        self.game = GomokuGame(self.lang)
        self.bot = GomokuBot(self.game)
        self.current_screen = "game"
        self.selected_cell = (self.game.board_size // 2, self.game.board_size // 2)
        
        # Bot makes first move if player is white
        if config.player_color == 'white':
            print(f"\n{self.lang.get('game_bot_thinking', 'Bot thinking...')}")
            bot_move = self.bot.make_move()
            if bot_move:
                self.game.make_move(*bot_move)
                print(f"{self.lang.get('bot_move', 'Bot move at')} ({bot_move[0]}, {bot_move[1]})")
    
    def run_game(self):
        game_running = True
        
        while game_running and not self.game.game_over:
            self.clear_screen()
            self.game.display_board(self.selected_cell)
            
            current_player_name = self.lang.get('color_black', 'Black') if self.game.current_player == "black" else self.lang.get('color_white', 'White')
            print(f"\n{self.lang.get('game_turn', 'Move')}: {current_player_name}")
            
            if self.selected_cell:
                row, col = self.selected_cell
                cell_status = self.lang.get('color_white', 'Empty') if self.game.board[row][col] is None else self.lang.get('color_black', 'Occupied')
                print(f"{self.lang.get('select_cell', 'Selected cell')}: ({row}, {col})")
            
            if self.game.current_player == config.player_color:
                print(f"{self.lang.get('available_commands', 'Commands:')}")
                
                while True:
                    key = self.get_key()
                    
                    if key == b'H':  # Up
                        self.selected_cell = (max(0, self.selected_cell[0] - 1), self.selected_cell[1])
                        break
                    elif key == b'P':  # Down
                        self.selected_cell = (min(self.game.board_size - 1, self.selected_cell[0] + 1), self.selected_cell[1])
                        break
                    elif key == b'K':  # Left
                        self.selected_cell = (self.selected_cell[0], max(0, self.selected_cell[1] - 1))
                        break
                    elif key == b'M':  # Right
                        self.selected_cell = (self.selected_cell[0], min(self.game.board_size - 1, self.selected_cell[1] + 1))
                        break

                    elif key == b' ':
                        row, col = self.selected_cell
                        if self.game.make_move(row, col):
                            print(f"{self.lang.get('player_move', 'Player move at')} ({row}, {col})")
                            
                            if not self.game.game_over:
                                print(f"\n{self.lang.get('game_bot_thinking', 'Bot thinking...')}")
                                bot_move = self.bot.make_move()
                                if bot_move:
                                    self.game.make_move(*bot_move)
                                    print(f"{self.lang.get('bot_move', 'Bot move at')} ({bot_move[0]}, {bot_move[1]})")
                        else:
                            print(f"{self.lang.get('invalid_move', 'Invalid move!')} {self.lang.get('cell_occupied', 'Cell is already occupied.')}")
                        break
                        
                    elif key in [b'q', b'Q']:
                        print(f"\n{self.lang.get('game_interrupted', 'Game interrupted.')}")
                        game_running = False
                        self.current_screen = "menu"
                        break

                    elif key in [b'r', b'R']:
                        self.start_game()
                        return

                    elif key in [b'm', b'M']:
                        game_running = False
                        self.current_screen = "menu"
                        break
            
            else:
                print(f"\n{self.lang.get('game_bot_thinking', 'Bot thinking...')}")
                bot_move = self.bot.make_move()
                if bot_move:
                    self.game.make_move(*bot_move)
                    print(f"{self.lang.get('bot_move', 'Bot move at')} ({bot_move[0]}, {bot_move[1]})")
        
        if self.game.game_over:
            self.clear_screen()
            self.game.display_board()
            
            if self.game.winner:
                winner_name = self.lang.get('color_black', 'Black') if self.game.winner == "black" else self.lang.get('color_white', 'White')
                if config.language == 'ru_ru':
                    print(f"\n🎉 {winner_name} побеждают!")
                else:
                    print(f"\n🎉 {winner_name} wins!")
            else:
                print(f"\n🤝 {self.lang.get('game_draw', 'Draw!')}")
            
            if self.game.winner:
                if self.game.winner == config.player_color:
                    result = 'win'
                else:
                    result = 'loss'
            else:
                result = 'draw'
            
            database.add_game_result(result, config.difficulty, config.board_size)
            
            print(f"\n1. {self.lang.get('game_restart', 'New game')}")
            print(f"2. {self.lang.get('game_main_menu', 'Main menu')}")
            
            choice = input(f"\n{self.lang.get('select_option', 'Select option')} (1-2): ").strip()
            
            if choice == "1":
                self.start_game()
            else:
                self.current_screen = "menu"

if __name__ == "__main__":
    app = GomokuApp()
    app.run()