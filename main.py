# Builing the game Othello (Without the diagonal outflanking) using Alpha-Beta Pruning
import math
EMPTY_CELL = '-'
HUMAN_PLAYER = 'B'
COMPUTER_PLAYER = 'W'
AVAILABLE_MOVE_CELL = '@'
COMPLEXITY_LEVEL = 1
MAX, MIN = math.inf, -math.inf


def game_controller():
    board = create_board(8, 8)
    human_player_remaining_disks = 30
    computer_player_remaining_disks = 30
    take_complexity_level()
    while True:
        if check_no_available_moves_for_both_palyers(board):
            break
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(format_printed_board(board))
        human_player_score, computer_player_score = get_score(board)
        print(
            f"Human Player: {human_player_score} Computer Player: {computer_player_score}")

        # Human Turn
        if check_board_unique_color(board) or check_no_empty_cells(board) or check_out_of_disks(human_player_score, computer_player_score):
            break
        human_player_move = get_human_player_move(board)
        if(human_player_move != False):
            board = making_outflanking(board, human_player_move, HUMAN_PLAYER)
            # board = make_move(board, human_player_move, HUMAN_PLAYER)
            human_player_remaining_disks -= 1
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(format_printed_board(board))

        # Computer Turn
        if check_board_unique_color(board) or check_no_empty_cells(board) or check_out_of_disks(human_player_score, computer_player_score):
            break
        print("Computer Moves")
        print(format_printed_board(create_board_with_available_moves(board, COMPUTER_PLAYER)))
        computer_player_move = get_computer_player_move(board)
        computer_player_remaining_disks -= 1
        board = making_outflanking(
            board, computer_player_move, COMPUTER_PLAYER)
        # board = make_move(board, computer_player_move, COMPUTER_PLAYER)

    print("Game Over")
    human_player_score, computer_player_score = get_score(board)
    print(
        f"Human Player: {human_player_score} Computer Player: {computer_player_score}")
    if human_player_score > computer_player_score:
        print("Human Player Wins")
    elif human_player_score < computer_player_score:
        print("Computer Player Wins")
    else:
        print("Draw")


def making_outflanking(board, move, player_color):
    new_board = [row.copy() for row in board]
    cell_from_up = can_get_outflanking_from_up(board, move, player_color)
    cell_from_down = can_get_outflanking_from_down(board, move, player_color)
    cell_from_right = can_get_outflanking_from_right(board, move, player_color)
    cell_from_left = can_get_outflanking_from_left(board, move, player_color)
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


def take_complexity_level():
    print("Enter the complexity level (1 => Easy, 2 => Medium, 3 => Hard)")
    level = int(input())
    global COMPLEXITY_LEVEL
    if (level == 1):
        COMPLEXITY_LEVEL = 2
    elif (level == 2):
        COMPLEXITY_LEVEL = 5
    else:
        COMPLEXITY_LEVEL = 10


def get_human_player_move(board):
    print(format_printed_board(
        create_board_with_available_moves(board, HUMAN_PLAYER)))
    available_moves = get_available_moves(board, HUMAN_PLAYER)
    if(available_moves == []):
        print("No available moves for Human Player")
        return False
    while True:
        print("Enter the row and column of your move")
        row, col = map(int, input().split()) 
        if [row, col] in available_moves:
            return [row, col]
        print("Invalid Move")


def make_move(board, move, player):
    board = [row.copy() for row in board]
    board[move[0]][move[1]] = player
    return board


def get_computer_player_move(board):
    available_moves = get_available_moves(board, COMPUTER_PLAYER)
    best_move = [0, 0]
    best_score = MIN
    for move in available_moves:
        new_board = make_move(board, move, COMPUTER_PLAYER)
        score = minimax(new_board, 0, False, MIN, MAX)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def format_printed_board(board):
    return '\n'.join([' '.join(row) for row in board])


def create_board(rows, cols):
    board = [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]
    board[3][3] = board[4][4] = COMPUTER_PLAYER
    board[3][4] = board[4][3] = HUMAN_PLAYER
    return board


def get_score(board):
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

def check_no_available_moves_for_both_palyers(board):
    return get_available_moves(board, HUMAN_PLAYER) == [] and get_available_moves(board, COMPUTER_PLAYER) == []

def check_board_unique_color(board):
    scores = get_score(board)
    return scores[0] == 0 or scores[1] == 0


def check_no_empty_cells(board):
    scores = get_score(board)
    return scores[0] + scores[1] == 64


def check_out_of_disks(human_player_remaining_disks, computer_player_remaining_disks):
    return human_player_remaining_disks == 0 or computer_player_remaining_disks == 0


# Available Moves
def create_board_with_available_moves(board, player):
    available_moves = get_available_moves(board, player)
    board_with_available_moves = [row.copy() for row in board]
    for move in available_moves:
        board_with_available_moves[move[0]][move[1]] = AVAILABLE_MOVE_CELL
    return board_with_available_moves


def get_available_moves(board, player):
    available_moves = []
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    for i in range(8):
        for j in range(8):
            if board[i][j] != EMPTY_CELL and board[i][j] != player:
                for direction in directions:
                    new_i, new_j = i + direction[0], j + direction[1]
                    if can_create_outflanking(board, [new_i, new_j], player):
                        available_moves.append([new_i, new_j])
    return available_moves


def can_create_outflanking(board, move, player_color):
    return (move[0] >= 0 and move[0] < 8 and move[1] >= 0 and move[1] < 8) and (board[move[0]][move[1]] == EMPTY_CELL) and (can_get_outflanking_from_up(board, move, player_color) or can_get_outflanking_from_down(board, move, player_color) or can_get_outflanking_from_right(board, move, player_color) or can_get_outflanking_from_left(board, move, player_color))


def can_get_outflanking_from_up(board, move, player_color):
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


def can_get_outflanking_from_down(board, move, player_color):
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


def can_get_outflanking_from_right(board, move, player_color):
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


def can_get_outflanking_from_left(board, move, player_color):
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


# print(format_printed_board(create_board(8, 8)))
# print("-------------------------")

arr = [
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', 'W', '-', 'W', 'B', '-', '-', '-'],
    ['-', '-', 'W', 'B', 'B', '-', '-', '-'],
    ['-', '-', '-', 'W', 'B', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-']
]
# print(format_printed_board(create_board_with_available_moves(arr, HUMAN_PLAYER)))


def minimax(board, depth, maximizing_player, alpha, beta):
    # Terminated node is reached
    # print("##########################################")
    # print("Board\n", format_printed_board(board))
    # print("##########################################")

    if (depth == COMPLEXITY_LEVEL or 
            check_no_empty_cells(board) or 
            get_available_moves(board, HUMAN_PLAYER) == [] or 
            get_available_moves(board, COMPUTER_PLAYER) == []):
        return utility_function(board)

    if maximizing_player:

        best = MIN

        available_moves = get_available_moves(board, COMPUTER_PLAYER)

        for move in available_moves:
            # new_board = make_move(board, move, COMPUTER_PLAYER)
            new_board = making_outflanking(board, move, COMPUTER_PLAYER)
            val = minimax(new_board, depth + 1, False, alpha, beta)

            best = max(best, val)
            alpha = max(alpha, best)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        return best

    else:
        best = MAX

        available_moves = get_available_moves(board, HUMAN_PLAYER)

        for move in available_moves:
            new_board = making_outflanking(board, move, HUMAN_PLAYER)
            # new_board = make_move(board, move, HUMAN_PLAYER)
            val = minimax(new_board, depth + 1, True, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        return best


def utility_function(board):
    scores = get_score(board)
    return scores[1] - scores[0]


game_controller()
