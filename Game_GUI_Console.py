import tkinter as tk
import customtkinter as ctk
import math

EMPTY_CELL = '-'
HUMAN_PLAYER = 'B'
COMPUTER_PLAYER = 'W'
AVAILABLE_MOVE_CELL = '@'
COMPLEXITY_LEVEL = 1
MAX, MIN = math.inf, -math.inf


class OthelloAppConsole:
    def __init__(self):
        self.game_controller = GameController()

    def run_console_game(self):
        self.take_complexity_level()
        while True:
            # Human Turn
            self.print_board_for_human()
            human_player_move = self.get_human_player_move()
            if (human_player_move != False):
                self.game_controller.make_human_move(human_player_move)
                self.print_board_for_human()
            if self.game_controller.check_end_game():
                break
            # Computer Turn
            while True:
                print("Computer Moves")
                print(self.format_printed_board(
                    self.game_controller.create_board_with_available_moves(COMPUTER_PLAYER)))
                self.game_controller.make_computer_move()
                if (not self.game_controller.check_computer_takes_human_turn()):
                    break
                if self.game_controller.check_end_game():
                    break
        self.print_end_game()

    def print_end_game(self):
        print("Game Over")
        human_player_score, computer_player_score = self.game_controller.get_score(
            self.board)
        print(
            f"Human Player: {human_player_score} Computer Player: {computer_player_score}")
        if human_player_score > computer_player_score:
            print("Human Player Wins")
        elif human_player_score < computer_player_score:
            print("Computer Player Wins")
        else:
            print("Draw")

    def take_complexity_level(self):
        print("Enter the complexity level")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        level = int(input())
        self.game_controller.set_complexity_level(level)

    def print_board_for_human(self):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(self.format_printed_board(self.game_controller.board))
        human_player_score, computer_player_score = self.game_controller.get_score(
            self.game_controller.board)
        print(
            f"Human Player: {human_player_score} Computer Player: {computer_player_score}")

    def get_human_player_move(self):
        board_with_available_moves = self.game_controller.create_board_with_available_moves(
            HUMAN_PLAYER)
        print(self.format_printed_board(board_with_available_moves))
        available_moves = self.game_controller.get_available_moves(
            self.game_controller.board, HUMAN_PLAYER)
        if (available_moves == []):
            print("No available moves for Human Player")
            return False
        while True:
            print("Enter the row and column of your move")
            row, col = map(int, input().split())
            if [row, col] in available_moves:
                return [row, col]
            print("Invalid Move")

    def format_printed_board(self, board):
        return '\n'.join([' '.join(row) for row in board])


class GameController:
    def __init__(self):
        self.board = self.create_board(8, 8)
        self.board_with_available_cells = self.create_board(8, 8)
        self.human_player_remaining_disks = 30
        self.computer_player_remaining_disks = 30

    def get_board(self):
        self.board_with_available_cells = self.create_board_with_available_moves(
            HUMAN_PLAYER)
        return self.board_with_available_cells

    def make_human_move(self, move):
        if move in self.get_available_moves(self.board, HUMAN_PLAYER):
            self.board = self.making_outflanking(
                self.board, move, HUMAN_PLAYER)
            self.human_player_remaining_disks -= 1
            return True
        return False

    def make_computer_move(self):
        best_move = self.get_computer_player_move()
        self.board = self.making_outflanking(
            self.board, best_move, COMPUTER_PLAYER)
        self.computer_player_remaining_disks -= 1

    def check_end_game(self):
        if (self.check_board_unique_color()
                or self.check_no_empty_cells(self.board)
            or self.check_out_of_disks()
                or self.check_no_available_moves_for_both_players()):
            return True
        return False

    def check_computer_takes_human_turn(self):
        return self.get_available_moves(self.board, HUMAN_PLAYER) == []

    def making_outflanking(self, board, move, player_color):
        new_board = [row.copy() for row in self.board]
        cell_from_up = self.can_get_outflanking_from_up(
            board, move, player_color)
        cell_from_down = self.can_get_outflanking_from_down(
            board, move, player_color)
        cell_from_right = self.can_get_outflanking_from_right(
            board, move, player_color)
        cell_from_left = self.can_get_outflanking_from_left(
            board, move, player_color)
        if cell_from_up:
            for i in range(cell_from_up[0], move[0] + 1):
                new_board[i][move[1]] = player_color
        if cell_from_down:
            for i in range(move[0], cell_from_down[0] + 1):
                new_board[i][move[1]] = player_color
        if cell_from_right:
            for i in range(move[1], cell_from_right[1] + 1):
                new_board[move[0]][i] = player_color
        if cell_from_left:
            for i in range(cell_from_left[1], move[1] + 1):
                new_board[move[0]][i] = player_color
        return new_board

    def set_complexity_level(self, level):
        global COMPLEXITY_LEVEL
        if (level == 1):
            COMPLEXITY_LEVEL = 1
        elif (level == 2):
            COMPLEXITY_LEVEL = 3
        else:
            COMPLEXITY_LEVEL = 5

    def make_move(self, move, player):
        board = [row.copy() for row in self.board]
        board[move[0]][move[1]] = player
        return board

    def get_computer_player_move(self):
        available_moves = self.get_available_moves(self.board, COMPUTER_PLAYER)
        best_move = [0, 0]
        best_score = MIN
        for move in available_moves:
            new_board = self.make_move(move, COMPUTER_PLAYER)
            score = self.minimax(new_board, 0, False, MIN, MAX)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def create_board(self, rows, cols):
        board = [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]
        board[3][3] = board[4][4] = COMPUTER_PLAYER
        board[3][4] = board[4][3] = HUMAN_PLAYER
        return board

    def get_score(self, board):
        human_player_score = 0
        computer_player_score = 0
        for row in board:
            for cell in row:
                if cell == HUMAN_PLAYER:
                    human_player_score += 1
                elif cell == COMPUTER_PLAYER:
                    computer_player_score += 1
        return human_player_score, computer_player_score

    # Check Legal Moves

    def check_no_available_moves_for_both_players(self):
        return (self.get_available_moves(self.board, HUMAN_PLAYER) == [] and
                self.get_available_moves(self.board, COMPUTER_PLAYER) == [])

    def check_board_unique_color(self):
        scores = self.get_score(self.board)
        return scores[0] == 0 or scores[1] == 0

    def check_no_empty_cells(self, board):
        scores = self.get_score(board)
        return scores[0] + scores[1] == 64

    def check_out_of_disks(self):
        return self.human_player_remaining_disks == 0 or self.computer_player_remaining_disks == 0

    # Available Moves

    def create_board_with_available_moves(self, player):
        available_moves = self.get_available_moves(self.board, player)
        board_with_available_moves = [row.copy() for row in self.board]
        for move in available_moves:
            board_with_available_moves[move[0]][move[1]] = AVAILABLE_MOVE_CELL
        return board_with_available_moves

    def get_available_moves(self, board, player):
        available_moves = []
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for i in range(8):
            for j in range(8):
                if board[i][j] != EMPTY_CELL and board[i][j] != player:
                    for direction in directions:
                        new_i, new_j = i + direction[0], j + direction[1]
                        if self.can_create_outflanking(board, [new_i, new_j], player):
                            available_moves.append([new_i, new_j])
        return available_moves

    def can_create_outflanking(self, board, move, player_color):
        return ((move[0] >= 0 and move[0] < 8 and move[1] >= 0 and move[1] < 8)
                and (board[move[0]][move[1]] == EMPTY_CELL)
                and (self.can_get_outflanking_from_up(board, move, player_color)
                     or self.can_get_outflanking_from_down(board, move, player_color)
                     or self.can_get_outflanking_from_right(board, move, player_color)
                     or self.can_get_outflanking_from_left(board, move, player_color)))

    def can_get_outflanking_from_up(self, board, move, player_color):
        current_cell = [move[0] - 1, move[1]]
        counter = 0
        while (current_cell[0] >= 0 and board[current_cell[0]][current_cell[1]] != EMPTY_CELL):
            if board[current_cell[0]][current_cell[1]] == player_color:
                if (counter == 0):
                    return False
                return [current_cell[0], current_cell[1]]
            current_cell[0] -= 1
            counter += 1
        return False

    def can_get_outflanking_from_down(self, board, move, player_color):
        current_cell = [move[0] + 1, move[1]]
        counter = 0
        while (current_cell[0] < 8 and board[current_cell[0]][current_cell[1]] != EMPTY_CELL):
            if board[current_cell[0]][current_cell[1]] == player_color:
                if (counter == 0):
                    return False
                return [current_cell[0], current_cell[1]]
            current_cell[0] += 1
            counter += 1
        return False

    def can_get_outflanking_from_right(self, board, move, player_color):
        current_cell = [move[0], move[1] + 1]
        counter = 0
        while (current_cell[1] < 8 and board[current_cell[0]][current_cell[1]] != EMPTY_CELL):
            if board[current_cell[0]][current_cell[1]] == player_color:
                if (counter == 0):
                    return False
                return [current_cell[0], current_cell[1]]
            current_cell[1] += 1
            counter += 1
        return False

    def can_get_outflanking_from_left(self, board, move, player_color):
        current_cell = [move[0], move[1] - 1]
        counter = 0
        while (current_cell[1] >= 0 and board[current_cell[0]][current_cell[1]] != EMPTY_CELL):
            if board[current_cell[0]][current_cell[1]] == player_color:
                if (counter == 0):
                    return False
                return [current_cell[0], current_cell[1]]
            current_cell[1] -= 1
            counter += 1
        return False

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        if (depth == COMPLEXITY_LEVEL or
                self.check_no_empty_cells(board) or
                self.get_available_moves(board, HUMAN_PLAYER) == [] or
                self.get_available_moves(board, COMPUTER_PLAYER) == []):
            return self.utility_function(board)
        if maximizing_player:
            best = MIN
            available_moves = self.get_available_moves(board, COMPUTER_PLAYER)
            for move in available_moves:
                new_board = self.making_outflanking(
                    board, move, COMPUTER_PLAYER)
                val = self.minimax(new_board, depth + 1, False, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                # Alpha Beta Pruning
                if beta <= alpha:
                    break
            return best
        else:
            best = MAX
            available_moves = self.get_available_moves(board, HUMAN_PLAYER)
            for move in available_moves:
                new_board = self.making_outflanking(board, move, HUMAN_PLAYER)
                val = self.minimax(new_board, depth + 1, True, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                # Alpha Beta Pruning
                if beta <= alpha:
                    break
            return best

    def utility_function(self, board):
        scores = self.get_score(board)
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        edges = [(0, i) for i in range(8)] + [(7, i) for i in range(8)] + \
            [(i, 0) for i in range(8)] + [(i, 7) for i in range(8)]

        ai_corners = sum(
            1 for corner in corners if board[corner[0]][corner[1]] == COMPUTER_PLAYER)
        player_corners = sum(
            1 for corner in corners if board[corner[0]][corner[1]] == HUMAN_PLAYER)

        ai_edges = sum(
            1 for edge in edges if board[edge[0]][edge[1]] == COMPUTER_PLAYER)
        player_edges = sum(
            1 for edge in edges if board[edge[0]][edge[1]] == HUMAN_PLAYER)

        return 5 * (scores[1] - scores[0]) + 50 * (ai_corners - player_corners) + 20 * (ai_edges - player_edges)


class InitialWindow(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Othello Game - Select Complexity Level")
        self.geometry("300x200")

        self.complexity_level = ctk.StringVar(value="easy")

        self.easy_radio = ctk.CTkRadioButton(
            self, text="Easy", variable=self.complexity_level, value="easy")
        self.easy_radio.pack(pady=10)

        self.medium_radio = ctk.CTkRadioButton(
            self, text="Medium", variable=self.complexity_level, value="medium")
        self.medium_radio.pack(pady=10)

        self.hard_radio = ctk.CTkRadioButton(
            self, text="Hard", variable=self.complexity_level, value="hard")
        self.hard_radio.pack(pady=10)

        self.start_button = ctk.CTkButton(
            self, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=20)

    def start_game(self):
        complexity_level = self.complexity_level.get()
        self.app.set_complexity_level(complexity_level)
        self.destroy()
        self.app.create_board_window()


class OthelloAppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        # Assuming GameController is your console app logic
        self.game_controller = GameController()
        self.initial_window = InitialWindow(self)

    def create_board_window(self):
        self.deiconify()  # Show the main window
        self.title("Othello Game")
        self.geometry("600x400")

        self.board_frame = ctk.CTkFrame(self)
        self.board_frame.pack(padx=20, pady=20)
        self.GUI_create_board()
        self.GUI_create_score()
        # Scores
        self.human_player_score = 4
        self.computer_player_score = 4

    def set_complexity_level(self, level):
        if level == "easy":
            self.game_controller.set_complexity_level(1)
        elif level == "medium":
            self.game_controller.set_complexity_level(2)
        elif level == "hard":
            self.game_controller.set_complexity_level(3)

    def GUI_create_board(self):
        self.buttons = []
        for i in range(8):
            row = []
            for j in range(8):
                cell = ctk.CTkButton(self.board_frame, text="", width=50, height=50,
                                     command=lambda i=i, j=j: self.GUI_make_move(i, j))
                cell.grid(row=i, column=j)
                row.append(cell)
            self.buttons.append(row)
        self.GUI_update_board()

    def GUI_update_board(self):
        board = self.game_controller.get_board()
        for i in range(8):
            for j in range(8):
                if board[i][j] == HUMAN_PLAYER:
                    self.buttons[i][j].configure(
                        text="B", fg_color="black", hover_color="gray")
                elif board[i][j] == COMPUTER_PLAYER:
                    self.buttons[i][j].configure(
                        text="W", fg_color="white", hover_color="gray")
                elif board[i][j] == AVAILABLE_MOVE_CELL:
                    self.buttons[i][j].configure(
                        text="", fg_color="red", hover_color="gray")
                else:
                    self.buttons[i][j].configure(
                        text="", fg_color="green", hover_color="gray")

    def GUI_make_move(self, i, j):
        # Human Turn: Human makes a move if possible
        success = self.game_controller.make_human_move([i, j])
        if success:
            self.GUI_update_board()
            self.GUI_update_scores()
            if self.game_controller.check_end_game():
                self.GUI_show_winner()
                return
            while True:
                # Computer Turn: Computer makes a move if possible
                self.game_controller.make_computer_move()
                self.GUI_update_board()
                self.GUI_update_scores()
                if self.game_controller.check_end_game():
                    self.GUI_show_winner()
                    return
                if (not self.game_controller.check_computer_takes_human_turn()):
                    break

    def GUI_show_winner(self):
        human_player_score, computer_player_score = self.game_controller.get_score(
            self.game_controller.get_board())
        if human_player_score > computer_player_score:
            winner = "Human Player"
        elif human_player_score < computer_player_score:
            winner = "Computer Player"
        else:
            winner = "Draw"
        self.winner_label = ctk.CTkLabel(
            self.score_frame, text=f"Winner: {winner}")
        self.winner_label.grid(row=2, column=0)

    def GUI_create_score(self):
        self.score_frame = ctk.CTkFrame(self)
        self.score_frame.pack(padx=20, pady=20)
        self.human_player_score_label = ctk.CTkLabel(
            self.score_frame, text="Human Player Score: 4")
        self.human_player_score_label.grid(row=0, column=0)
        self.computer_player_score_label = ctk.CTkLabel(
            self.score_frame, text="Computer Player Score: 4")
        self.computer_player_score_label.grid(row=1, column=0)
        self.GUI_update_scores()

    def GUI_update_scores(self):
        human_player_score, computer_player_score = self.game_controller.get_score(
            self.game_controller.get_board())
        self.human_player_score = human_player_score
        self.computer_player_score = computer_player_score
        self.human_player_score_label.configure(
            text=f"Human Player Score: {self.human_player_score}")
        self.computer_player_score_label.configure(
            text=f"Computer Player Score: {self.computer_player_score}")


class GameType:
    def choose_game_type(self):
        print("Choose the game type")
        print("1. Console Game")
        print("2. GUI Game")
        game_type = int(input())
        if game_type == 1:
            game_console = OthelloAppConsole()
            game_console.run_console_game()
        elif game_type == 2:
            app = OthelloAppGUI()
            app.mainloop()


if __name__ == "__main__":
    game_type = GameType()
    game_type.choose_game_type()
