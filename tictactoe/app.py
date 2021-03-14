import pygame
from . import constants


class App():

    def __init__(self):
        self._runnning = True
        self._display = None
        self.board_surface = None
        self.size = self.width, self.height = constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT
        self.board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        self.player_turn = 0
        self.playing = True
        self.winning_cells = None
        self.win_image = None

    def on_init(self):
        pygame.init()
        self._display = pygame.display.set_mode(self.size)
        self._runnning = True

        # Surface to actually draw on
        self.board_surface = self._display.subsurface((constants.EDGE_BORDER, constants.EDGE_BORDER,
            constants.WINDOW_WIDTH - constants.EDGE_BORDER * 2,
            constants.WINDOW_WIDTH - constants.EDGE_BORDER * 2))
        
        self.win_image = pygame.Surface((self.board_surface.get_width() / 3,
            self.board_surface.get_height() / 3))
        self.win_image.fill(constants.WIN_COLOR)

    def _start(self):
        self.on_init()
        while self._runnning:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
        self.on_destroy()

    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self._runnning = False
        elif event.type == pygame.MOUSEBUTTONDOWN and self.playing:
            pos = pygame.mouse.get_pos()

            # Check if clicked on board surface
            if not self.board_surface.get_rect().collidepoint(pos):
                return
            
            # Calculate cell address from position
            x, y = pos
            row = int((y - constants.EDGE_BORDER) // (self.board_surface.get_width() / 3))
            col = int((x - constants.EDGE_BORDER) // (self.board_surface.get_height() / 3))

            # Check if cell is occupied
            if self.board[row][col] != -1:
                return

            self.board[row][col] = self.player_turn
            self.player_turn = 0 if self.player_turn == 1 else 1
            pygame.display.update()

            self.winning_cells = self.check_winner()
            if self.winning_cells is not None:
                self.playing = False

    def fill_win_cells(self):

        cell_width = self.board_surface.get_width() / 3
        cell_height = self.board_surface.get_height() / 3

        for row_i, col_i in self.winning_cells:
            self.board_surface.blit(
                self.win_image,
                (
                    cell_width * col_i,
                    cell_height * row_i,
                    cell_width,
                    cell_height
                )
            )


    def check_winner(self):
        # Check straight row matches
        for row_i, row in enumerate(self.board):
            cmp = self.board[row_i][0]
            if cmp != -1 and all(self.board[row_i][column_i] == cmp
                                 for column_i in range(1, 3)):
                return (row_i, 0), (row_i, 1), (row_i, 2)
        
        # Check staright column matches
        for column_i in range(0, 3):
            cmp = self.board[0][column_i]
            if cmp != -1 and all(self.board[row_i][column_i] == cmp
                                 for row_i in range(0, 3)):
                return (0, column_i), (1, column_i), (2, column_i)

        # Check diagonals
        cmp = self.board[1][1]
        if cmp != -1:
            if all(self.board[i][i] == cmp for i in range(0, 3)):
                return tuple((i, i) for i in range(0, 3))

            # Check another diagonal
            if all(self.board[i][2-i] == cmp for i in range(0, 3)):
               return tuple((i, 2-i) for i in range(0, 3))
        
        # No winner yet
        return None
    
    def draw_player_sign(self, pos, player):
        cell_width = self.board_surface.get_width() / 3
        cell_height = self.board_surface.get_height() / 3

        row, col = pos

        # Surface to draw cell at
        cell_surface = self.board_surface.subsurface(
            (cell_width * col, cell_height * row, cell_width, cell_height)
        )

        if player == 0:
            pygame.draw.ellipse(
                cell_surface,
                constants.FOREGROUND_COLOR,
                (
                    constants.EDGE_BORDER,
                    constants.EDGE_BORDER,
                    cell_width - constants.EDGE_BORDER * 2,
                    cell_height - constants.EDGE_BORDER * 2
                ),
                constants.LINE_THICKNESS
            )
        elif player == 1:
            pygame.draw.line(
                cell_surface,
                constants.FOREGROUND_COLOR,
                (constants.EDGE_BORDER, constants.EDGE_BORDER),
                (cell_width - constants.EDGE_BORDER, cell_height - constants.EDGE_BORDER),
                constants.LINE_THICKNESS
            )

            pygame.draw.line(
                cell_surface,
                constants.FOREGROUND_COLOR,
                (cell_width - constants.EDGE_BORDER, constants.EDGE_BORDER),
                (constants.EDGE_BORDER, cell_height - constants.EDGE_BORDER),
                constants.LINE_THICKNESS
            )

    def on_render(self):
        self._display.fill(constants.BACKGROUND_COLOR)

        if self.winning_cells is not None:
            self.fill_win_cells()

        # Draw horizontal lines
        top_horizontal_y = (self.board_surface.get_height() / 3)
        bottom_horizontal_y = top_horizontal_y * 2

        pygame.draw.line(self.board_surface, constants.FOREGROUND_COLOR,
            (0, top_horizontal_y),
            (self.width, top_horizontal_y),
            constants.LINE_THICKNESS)
        pygame.draw.line(self.board_surface, constants.FOREGROUND_COLOR,
            (0, bottom_horizontal_y),
            (self.width, bottom_horizontal_y),
            constants.LINE_THICKNESS)

        # Draw vertical lines
        left_vertical_x = (self.board_surface.get_width() / 3)
        right_vertical_x = left_vertical_x * 2

        pygame.draw.line(self.board_surface, constants.FOREGROUND_COLOR,
            (left_vertical_x, 0),
            (left_vertical_x, self.height),
            constants.LINE_THICKNESS)
        pygame.draw.line(self.board_surface, constants.FOREGROUND_COLOR,
            (right_vertical_x, 0),
            (right_vertical_x, self.height),
            constants.LINE_THICKNESS)

        # Draw signs
        for row_i, row in enumerate(self.board):
            for col_i, cell in enumerate(row):
                if cell != -1:
                    self.draw_player_sign((row_i, col_i), cell)

        pygame.display.flip()

    def on_destroy(self):
        pygame.quit()
