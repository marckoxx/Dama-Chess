# keeps track of the game's logic
class GameState:
    def __init__(self):  # this means it's the function of the class GameState itself.
        # so when calling stuff from here just say Game.State.something.
        # the board is read row, column, character/s inside.
        # example: self.board[0][0][0] = 'b' [first row][first column][first character]
        # if the third parameter is not set, it returns both characters.
        # min_max of the rows and columns are (0, 7), while for the characters it's obviously (0, 1)
        self.board = [
            ["--", "bR", "--", "bN", "--", "bN", "--", "bR"],
            ["bP", "--", "bP", "--", "bP", "--", "bP", "--"],
            ["--", "bP", "--", "bP", "--", "bP", "--", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "--", "wP", "--", "wP", "--", "wP", "--"],
            ["--", "wP", "--", "wP", "--", "wP", "--", "wP"],
            ["wR", "--", "wN", "--", "wN", "--", "wR", "--"]]
        # the move_functions is a dictionary and it removes clutter in get_all_possible_moves
        self.move_functions = {"P": self.get_pawn_moves, "N": self.get_knight_moves, "B": self.get_bishop_moves,
                               "R": self.get_rook_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}
        # it's set to True since white always goes first.
        # To make it black's turn, make it False or write not self.white_to_move
        self.white_to_move = True
        # the list that contain the moves in [start file][start rank][end file][end rank] format. e.g. a2a4
        self.move_log = []
        # start locations of the kings. The values will be changed to keep track of the king.
        # the king is tracked so that a possible pin/check is checked all the time.
        self.white_king_location = (-12, -11)
        self.black_king_location = (-12, -11)
        # I don't need to explain these.
        self.check_mate = False
        self.stale_mate = False
        self.in_check = False
        # lists the values of where is the pinned piece and the piece that checks the king
        self.pins = []
        self.checks = []
        # the square where you can move then backstab the hell out of that idiot
        self.en_passant_possible = ()
        # the square of the eaten enemy piece
        self.dama_take_possible = []
        self.white_dama_count = []
        self.black_dama_count = []
        self.first_white_dama = False
        self.first_black_dama = False
        self.white_king_start = []
        self.black_king_start = []
        self.white_pawn_conv = []
        self.black_pawn_conv = []
        self.enemy_pawns = []
        self.pos = ['0', '1', '2', '3', '4', '5', '6', '7']

    # handles the main info when you make a move
    def make_move(self, move):
        # makes the piece move and leave the former square empty
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.board[move.start_row][move.start_col] = "--"
        # adds the made move to the move log
        self.move_log.append(move)
        # ends the turn of the current color
        self.white_to_move = not self.white_to_move
        # to keep track of the king's location
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)
        # to do the en passant
        # need to put this first else the en passant is possible but will not remove the taken pawn
        if (move.end_row, move.end_col) == self.en_passant_possible:
            move.is_en_passant_move = True
            self.board[move.start_row][move.end_col] = "--"
            move.piece_captured = self.board[move.start_row][move.end_col]
        # to check what square an en passant take is possible
        if move.piece_moved[1] == "P" and \
                abs(move.start_row - move.end_row) == 2 and \
                abs(move.start_col - move.end_col) == 0:
            # shows where the attacking pawn can move to backstab
            self.en_passant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.en_passant_possible = ()
        # to do the dama take
        if (move.end_row, move.end_col) in self.dama_take_possible:
            move.is_dama_take = True
            self.dama_take_possible = []
            self.board[((move.start_row + move.end_row) // 2)][((move.start_col + move.end_col) // 2)] = "--"

        # to create pawn promotion prompt
        if move.is_pawn_promotion:
            white_dama_type = len(self.white_dama_count) % 2
            black_dama_type = len(self.black_dama_count) % 2
            possible_promotions = ['K', 'Q', 'R', 'N']
            if not self.white_to_move:
                # to make the dama a bishop
                if len(self.white_dama_count) != 0 and white_dama_type == 0:
                    self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'B'
                    self.white_dama_count.append((move.end_row, move.end_col))
                # to summon any piece except a bishop
                if len(self.white_dama_count) != 0 and white_dama_type == 1:
                    while True:
                        promoted_piece = input("Select a piece except a Bishop and a Pawn [K, Q, R, N]:")
                        if promoted_piece != 'B':
                            self.board[move.end_row][move.end_col] = move.piece_moved[0] + promoted_piece
                            self.white_dama_count.append((move.end_row, move.end_col))
                            if promoted_piece in possible_promotions:
                                break
                # the first dama of white
                if len(self.white_dama_count) == 0:
                    self.first_white_dama = True
                    self.get_enemy_pawns()
                    self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'
                    self.white_dama_count.append((move.end_row, move.end_col))
                    while True:
                        print(self.enemy_pawns)
                        selected_king_row = input('Please select the row of the pawn:')
                        if selected_king_row in self.pos:
                            selected_king_col = input('Please select the column of the pawn:')
                            if selected_king_col in self.pos:
                                selected_king = (int(selected_king_row), int(selected_king_col))
                                print(selected_king)
                                if selected_king in self.enemy_pawns:
                                    self.board[selected_king[0]][selected_king[1]] = 'bK'
                                    self.black_king_location = (selected_king[0], selected_king[1])
                                    self.enemy_pawns = []
                                    self.black_pawn_conv.append((selected_king[0], selected_king[1]))
                                    self.black_king_start.append(len(self.move_log))
                                    break

            else:
                # to make the dama a bishop
                if len(self.black_dama_count) != 0 and black_dama_type == 0:
                    self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'B'
                    self.black_dama_count.append((move.end_row, move.end_col))
                # to summon any piece except a bishop
                if len(self.black_dama_count) != 0 and black_dama_type == 1:
                    while True:
                        promoted_piece = input("Select a piece except a Bishop and a Pawn [K, Q, R, N]:")
                        if promoted_piece != 'B':
                            self.board[move.end_row][move.end_col] = move.piece_moved[0] + promoted_piece
                            self.black_dama_count.append((move.end_row, move.end_col))
                            if promoted_piece in possible_promotions:
                                break
                # the first dama of black
                if len(self.black_dama_count) == 0:
                    self.get_enemy_pawns()
                    self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'
                    self.black_dama_count.append((move.end_row, move.end_col))
                    while True:
                        print(self.enemy_pawns)
                        selected_king_row = input('Please select the row of the pawn:')
                        if selected_king_row in self.pos:
                            selected_king_col = input('Please select the column of the pawn:')
                            if selected_king_col in self.pos:
                                selected_king = (int(selected_king_row), int(selected_king_col))
                                print(selected_king)
                                if selected_king in self.enemy_pawns:
                                    self.board[selected_king[0]][selected_king[1]] = 'wK'
                                    self.white_king_location = (selected_king[0], selected_king[1])
                                    self.enemy_pawns = []
                                    self.white_pawn_conv.append((selected_king[0], selected_king[1]))
                                    self.white_king_start.append(len(self.move_log))
                                    break

    # well, to undo moves. duh.
    def undo_move(self):
        # makes sure you don't undo yourself to nothingness
        if len(self.move_log) != 0:
            # thanks pop ctrl + z
            move = self.move_log.pop()
            # reverts the move made and turn
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            # to keep track of the kings(again)
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)
            # well it's to undo the en passant huh
            if move.is_en_passant_move:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = 'bP' if self.white_to_move else 'wP'
                self.en_passant_possible = (move.end_row, move.end_col)
                move.piece_captured = self.board[((move.start_row + move.end_row) // 2)][
                    ((move.start_col + move.end_col) // 2)]
            if move.piece_moved[1] == 'P' and \
                    abs(move.start_row - move.end_row) == 2 and \
                    abs(move.start_col - move.end_col) == 0:
                self.en_passant_possible = ()
            if move.is_dama_take:
                move.is_dama_take = False
                self.board[move.end_row][move.end_col] = "--"
                self.dama_take_possible.append((move.end_row, move.end_col))
                self.board[((move.start_row + move.end_row) // 2)][
                    ((move.start_col + move.end_col) // 2)] = move.dama_piece_taken
            # to undo a dama
            if move.is_pawn_promotion:
                if self.white_to_move:
                    move.is_pawn_promotion = False
                    if len(self.white_dama_count) != 0:
                        self.white_dama_count.pop()
                else:
                    move.is_pawn_promotion = False
                    if len(self.black_dama_count) != 0:
                        self.black_dama_count.pop()
            # to undo a first pawn promotion
            if self.first_white_dama:
                if self.black_king_start[0] - 1 == (len(self.move_log)):
                    self.board[(self.black_pawn_conv[0][0])][(self.black_pawn_conv[0][1])] = 'bP'
            if self.first_black_dama:
                if self.white_king_start[0] - 1 == (len(self.move_log)):
                    self.board[(self.white_pawn_conv[0][0])][(self.white_pawn_conv[0][1])] = 'bP'
            # literally mario 1 up. Don't mess up this time.
            if self.check_mate:
                self.check_mate = False
            if self.stale_mate:
                self.stale_mate = False

    # To make sure you don't do anything stupid. (Hopefully)
    def get_valid_moves(self):
        # well it's the list of valid moves.
        moves = []
        # steals stuff from another function to make it's own life easier
        self.in_check, self.pins, self.checks = self.see_checks_and_pins()
        # to keep track of the king, yes we already know that
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        # oh no
        if self.in_check:
            # if there's one piece that's aiming a gun at you
            if len(self.checks) == 1:
                moves = self.get_all_possible_moves()
                # converts the assailant square to its own variable
                check = self.checks[0]
                # converts the square into coordinates
                check_row = check[0]
                check_col = check[1]
                # he's the baaaaaad guy
                piece_checking = self.board[check_row][check_col]
                # duh
                valid_squares = []
                # if the attacker is a knight
                if piece_checking[1] == 'N':
                    # the king will check using the knight moves.
                    # if no knight is in the 8 moves, all moves are valid squares.
                    # wait I'm not sure yet
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != 'K':
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_possible_moves()
        if len(moves) == 0:
            if self.see_checks_and_pins():
                if self.in_check:
                    self.check_mate = True
                    if self.white_to_move:
                        print('Checkmate, Black Wins')
                    else:
                        print('Checkmate, White Wins')
                else:
                    self.stale_mate = True
                    print('Stalemate')
        return moves

    def see_checks_and_pins(self):
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            enemy_color = 'b'
            ally_color = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_row = self.black_king_location[0]
            start_col = self.white_king_location[1]
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        piece_kind = end_piece[1]
                        if (0 <= j <= 3 and piece_kind == 'R') or \
                                (4 <= j <= 7 and piece_kind == 'B') or \
                                (i == 1 and piece_kind == 'P' and ((enemy_color == 'w' and 6 <= j <= 7) or (
                                        enemy_color == 'b' and 4 <= j <= 5))) or \
                                (piece_kind == 'Q') or (i == 1 and piece_kind == 'K'):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            if end_piece[1] != 'K':
                                if possible_pin == ():
                                    possible_pin = (end_row, end_col, d[0], d[1])
                                    pins.append(possible_pin)
                                    break
                            else:
                                break

        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for a in knight_moves:
            end_row = start_row + a[0]
            end_col = start_col + a[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N":
                    in_check = True
                    checks.append((end_row, end_col, a[0], a[1]))

        return in_check, pins, checks

    def invalid_moves(self):
        empty = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == "--":
                    empty.append((r, c))
        return empty

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    # noinspection PyArgumentList
                    self.move_functions[piece](r, c, moves)

        return moves

    def get_enemy_pawns(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                pawn = self.board[r][c]
                if (pawn == 'wP' and self.white_to_move) or (pawn == 'bP' and not self.white_to_move):
                    self.enemy_pawns.append((r, c))

    def get_pawn_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        self.get_dama_moves(r, c, moves)
        if self.white_to_move:
            if r - 1 >= 0:
                if self.board[r - 1][c] == "--":  # 1 move forward
                    if not piece_pinned or pin_direction == (-1, 0):
                        moves.append(Move((r, c), (r - 1, c), self.board))
                        if r == 6 and self.board[r - 2][c] == "--":  # 2 moves forward
                            moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # capture to the left
                if self.board[r - 1][c - 1][0] == 'b':
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                if self.board[r][c - 1][0] != 'w':
                    if (r - 1, c - 1) == self.en_passant_possible:
                        moves.append(Move((r, c), (r - 1, c - 1), self.board, (r - 1, c - 1)))
            if c + 1 <= 7:  # capture to the right
                if self.board[r - 1][c + 1][0] == 'b':
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
                if self.board[r][c + 1][0] != 'w':
                    if (r - 1, c + 1) == self.en_passant_possible:
                        moves.append(Move((r, c), (r - 1, c + 1), self.board, (r - 1, c + 1)))

        else:  # black pawn moves
            if r + 1 <= 7:
                if self.board[r + 1][c] == "--":  # 1 move forward
                    if not piece_pinned or pin_direction == (1, 0):
                        moves.append(Move((r, c), (r + 1, c), self.board))
                        if r == 1 and self.board[r + 2][c] == "--":  # 2 moves forward
                            moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # capture to the left
                if self.board[r + 1][c - 1][0] == 'w':
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if self.board[r][c - 1][0] != 'b':
                    if (r + 1, c - 1) == self.en_passant_possible:
                        moves.append(Move((r, c), (r + 1, c - 1), self.board, (r + 1, c - 1)))
            if c + 1 <= 7:  # capture to the right
                if self.board[r + 1][c + 1][0] == 'w':
                    if not piece_pinned or pin_direction == (1, 1):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
                if self.board[r][c + 1][0] != 'b':
                    if (r + 1, c + 1) == self.en_passant_possible:
                        moves.append(Move((r, c), (r + 1, c + 1), self.board, (r + 1, c + 1)))

    def get_knight_moves(self, r, c, moves):
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                if self.board[r][c][1] == 'Q':
                    self.pins.remove(self.pins[i])
                break

        self.get_dama_moves(r, c, moves)
        horse_jumps = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for m in horse_jumps:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] == 'Q':
                    self.pins.remove(self.pins[i])
                break

        self.get_dama_moves(r, c, moves)
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + (d[0] * i)
                end_col = c + (d[1] * i)
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_rook_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] == 'Q':
                    self.pins.remove(self.pins[i])
                break

        self.get_dama_moves(r, c, moves)
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + (d[0] * i)
                end_col = c + (d[1] * i)
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_queen_moves(self, r, c, moves):
        self.get_dama_moves(r, c, moves)
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        self.get_dama_moves(r, c, moves)
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = r + row_moves[i]
            end_col = c + col_moves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    if ally_color == 'w':
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)

                    in_check, pins, checks = self.see_checks_and_pins()
                    if not in_check:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    if ally_color == 'w':
                        self.white_king_location = (r, c)
                    else:
                        self.black_king_location = (r, c)

    def get_dama_moves(self, r, c, moves):

        if self.white_to_move:
            if r >= 1 and c - 1 >= 0:  # dama move to the left
                if self.board[r - 1][c - 1] == "--":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))

            if r >= 1 and c + 1 <= 7:  # dama move to the right
                if self.board[r - 1][c + 1] == "--":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

            if r >= 2 and c - 2 >= 0:  # dama move/capture to the left
                if self.board[r - 2][c - 2] == "--":
                    if self.board[r - 1][c - 1][0] == "b":
                        moves.append(Move((r, c), (r - 2, c - 2), self.board))
                        self.dama_take_possible.append((r - 2, c - 2))

            if r >= 2 and c + 2 <= 7:  # dama move/capture to the right
                if self.board[r - 2][c + 2] == "--":
                    if self.board[r - 1][c + 1][0] == "b":
                        moves.append(Move((r, c), (r - 2, c + 2), self.board))
                        self.dama_take_possible.append((r - 2, c + 2))
        else:
            if r <= 6 and c - 1 >= 0:  # dama move to the left
                if self.board[r + 1][c - 1] == "--":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))

            if r <= 6 and c + 1 <= 7:  # dama move/capture to the right
                if self.board[r + 1][c + 1] == "--":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

            if r <= 5 and c - 2 >= 0:  # dama move/capture to the left
                if self.board[r + 2][c - 2] == "--":
                    if self.board[r + 1][c - 1][0] == "w":
                        moves.append(Move((r, c), (r + 2, c - 2), self.board))
                        self.dama_take_possible.append((r + 2, c - 2))

            if r <= 5 and c + 2 <= 7:  # dama move/capture to the right
                if self.board[r + 2][c + 2] == "--":
                    if self.board[r + 1][c + 1][0] == "w":
                        moves.append(Move((r, c), (r + 2, c + 2), self.board))
                        self.dama_take_possible.append((r + 2, c + 2))


class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, en_passant_possible=(), dama_take_possible=()):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # en passant stuff
        self.is_en_passant_move = False
        if self.piece_moved[1] == 'P' and (self.end_row, self.end_col) == en_passant_possible:
            self.is_en_passant_move = True
        # dama takes stuff
        self.dama_piece_taken = board[((self.start_row + self.end_row) // 2)][((self.start_col + self.end_col) // 2)]
        self.is_dama_take = False
        if (self.end_row, self.end_col) in dama_take_possible:
            self.is_dama_take = True
        # pawn promotion stuff
        self.is_pawn_promotion = False
        self.possible_promotion = (self.piece_moved == 'wP' and self.end_row == 0) or \
                                  (self.piece_moved == 'bP' and self.end_row == 7)
        if self.possible_promotion:
            self.is_pawn_promotion = True

        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        # print(self.move_id)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
