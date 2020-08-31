import pygame
import sys
import Engine

sys.path.append('Images')
pygame.init()

Width = Height = 512
Dimension = 8
sq_size = Height // Dimension
max_FPS = 15
Images = {}


def load_images():
    pieces = ["wK", "bK", "wQ", "bQ", "wR", "bR", "wB", "bB", "wN", "bN", "wP", "bP"]
    for piece in pieces:
        Images[piece] = pygame.transform.scale(pygame.image.load("Images/" + piece + ".png"), (sq_size, sq_size))


def main():
    screen = pygame.display.set_mode((Width, Height))
    screen.fill(pygame.Color("black"))
    clock = pygame.time.Clock()
    gs = Engine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    animate = False
    print(gs.board)
    load_images()
    sq_selected = ()
    player_clicks = []
    game_over = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()
                    col = location[0] // sq_size
                    row = location[1] // sq_size
                    if sq_selected == (row, col):
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                        if len(player_clicks) == 1:
                            if sq_selected in gs.invalid_moves():
                                sq_selected = ()
                                player_clicks = []
                        # print(player_clicks)
                    if len(player_clicks) == 2:
                        move = Engine.Move(player_clicks[0], player_clicks[1], gs.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(move)
                                move_made = True
                                animate = True
                                print(move.get_chess_notation())
                                sq_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undo_move()
                    move_made = True
                    animate = False
                    game_over = False
                if event.key == pygame.K_r:
                    game_over = False
                    gs = Engine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                if event.key == pygame.K_ESCAPE:
                    running = False

        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, gs, valid_moves, sq_selected)
        if gs.check_mate:
            game_over = True
            if gs.white_to_move:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")
        elif gs.stale_mate:
            game_over = True
            draw_text(screen, "Lmao stalemate")
        clock.tick(max_FPS)
        pygame.display.flip()
    pygame.quit()


def highlight_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):
            s = pygame.Surface((sq_size, sq_size))
            s.set_alpha(100)
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c * sq_size, r * sq_size))
            s.fill(pygame.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * sq_size, move.end_row * sq_size))


def draw_game_state(screen, gs, valid_moves, sq_selected):
    draw_board(screen)
    highlight_squares(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)


# noinspection PyGlobalUndefined
def draw_board(screen):
    global colors
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for r in range(Dimension):
        for c in range(Dimension):
            colour = ((r + c) % 2)
            if colour == 0:
                color = pygame.Color("white")
            else:
                color = pygame.Color("gray")
            pygame.draw.rect(screen, color, pygame.Rect(c * sq_size, r * sq_size, sq_size, sq_size))


def draw_pieces(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(Images[piece], pygame.Rect(c * sq_size, r * sq_size, sq_size, sq_size))


# noinspection PyGlobalUndefined
def animate_move(move, screen, board, clock):
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 2
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        r, c = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = pygame.Rect(move.end_col * sq_size, move.end_row * sq_size, sq_size, sq_size)
        pygame.draw.rect(screen, color, end_square)
        if move.piece_captured != '--':
            screen.blit(Images[move.piece_captured], end_square)
        screen.blit(Images[move.piece_moved], pygame.Rect(c * sq_size, r * sq_size, sq_size, sq_size))
        pygame.display.flip()
        clock.tick(60)


def draw_text(screen, text):
    font = pygame.font.SysFont('Helvetica', 32, True, False)
    text_object = font.render(text, 5, pygame.Color('white'))
    text_location = pygame.Rect(0, 0, Width, Height).move(Width / 2 - text_object.get_width() / 2,
                                                          Height / 2 - text_object.get_height() / 2)
    b = pygame.Surface((Width, Height))
    b.set_alpha(150)
    b.fill(pygame.Color('black'))
    screen.blit(b, (0, 0))
    screen.blit(text_object, text_location)


#def draw_piece_selection:
 #   pass


if __name__ == "__main__":
    main()
