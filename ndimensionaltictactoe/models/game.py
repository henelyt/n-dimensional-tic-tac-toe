from ndimensionaltictactoe.exceptions.cell_in_use_exception import CellInUseException
from ndimensionaltictactoe.exceptions.grid_too_large_exception import GridTooLargeException
from ndimensionaltictactoe.exceptions.grid_too_small_exception import GridTooSmallException
from ndimensionaltictactoe.exceptions.no_name_exception import NoNameException
from ndimensionaltictactoe.exceptions.out_of_bounds_exception import OutOfBoundsException
from ndimensionaltictactoe.exceptions.winning_length_too_long_exception import WinningLengthTooLongException
from ndimensionaltictactoe.exceptions.winning_length_too_short import WinningLengthTooShortException
from ndimensionaltictactoe.models.mark import Mark

GAME_CREATED_WAITING = 0
GAME_INPROGRESS = 1
GAME_COMPLETED = 4


class Game(object):
    def __init__(self,
                 name,
                 key,
                 player_x,
                 player_o,
                 size_x=3,
                 size_y=3,
                 winning_length=3,
                 dimensions=2):
        if not name:
            raise NoNameException
        if dimensions < 2:
            raise GridTooSmallException
        if dimensions > 2:
            raise GridTooLargeException
        if winning_length < 1:
            raise WinningLengthTooShortException
        if winning_length > min([size_x, size_y]):
            raise WinningLengthTooLongException

        self.name = name
        self.key = key
        self.size_x = size_x
        self.size_y = size_y
        self.max_moves = size_x * size_y
        self.dimensions = dimensions
        self.player_x = player_x
        self.player_o = player_o
        self.cells = []
        self.winning_length = winning_length
        self.state = GAME_CREATED_WAITING
        self.player_x_turn = True

    def get_cell_by_coordinates(self, x, y):
        self._validate_coordinates(x, y)
        return next((mark for mark in self.cells
                     if mark.x == x and mark.y == y), None)

    def mark_cell_by_coordinates(self, x, y, mark):
        if not self.get_cell_by_coordinates(x, y):
            mark_obj = Mark(x, y, mark)
            self.cells.append(mark_obj)
            if self.mark_causes_win(mark_obj):
                self.state = GAME_COMPLETED
                return True
            return False
        else:
            raise CellInUseException

    def _validate_coordinates(self, x, y):
        if x < 0 or y < 0:
            raise OutOfBoundsException()

        if x > self.size_x - 1 or y > self.size_y - 1:
            raise OutOfBoundsException()

    def mark_causes_win(self, mark):
        return self._mark_causes_horizontal_win(mark) or \
               self._mark_causes_vertical_win(mark) or \
               self._mark_causes_negative_slope_diagonal_win(mark) or \
               self._mark_causes_positive_slope_diagonal_win(mark)

    def _mark_causes_horizontal_win(self, mark):
        horizontal_length = 0

        # count left
        for x in range(mark.x - 1, -1, -1):
            cell = self.get_cell_by_coordinates(x, mark.y)
            if cell and (cell.value == mark.value):
                horizontal_length = horizontal_length + 1
            else:
                break

        # count right
        for x in range(mark.x + 1, self.size_x, 1):
            cell = self.get_cell_by_coordinates(x, mark.y)
            if cell and (cell.value == mark.value):
                horizontal_length = horizontal_length + 1
            else:
                break

        return horizontal_length + 1 >= self.winning_length

    def _mark_causes_vertical_win(self, mark):
        vertical_length = 0

        # count up
        for y in range(mark.y - 1, -1, -1):
            cell = self.get_cell_by_coordinates(mark.x, y)
            if cell and (cell.value == mark.value):
                vertical_length = vertical_length + 1
            else:
                break

        # count down
        for y in range(mark.y + 1, self.size_y, 1):
            cell = self.get_cell_by_coordinates(mark.x, y)
            if cell and (cell.value == mark.value):
                vertical_length = vertical_length + 1
            else:
                break

        return vertical_length + 1 >= self.winning_length

    def _mark_causes_negative_slope_diagonal_win(self, mark):
        diagonal_length = 0

        # count left and up
        for pos_mod in range(-1, -1 * max([self.size_x, self.size_y]), -1):
            check_x = mark.x + pos_mod
            check_y = mark.y + pos_mod
            if check_x < 0 or check_y < 0:
                break
            cell = self.get_cell_by_coordinates(check_x, check_y)
            if cell and (cell.value == mark.value):
                diagonal_length = diagonal_length + 1
            else:
                break

        # count right and down
        for pos_mod in range(1, max([self.size_x, self.size_y]), 1):
            check_x = mark.x + pos_mod
            check_y = mark.y + pos_mod
            if check_x > self.size_x - 1 or check_y > self.size_y - 1:
                break
            cell = self.get_cell_by_coordinates(check_x, check_y)
            if cell and (cell.value == mark.value):
                diagonal_length = diagonal_length + 1
            else:
                break

        return diagonal_length + 1 >= self.winning_length

    def _mark_causes_positive_slope_diagonal_win(self, mark):
        diagonal_length = 0

        # count left and down
        for pos_mod in range(1, max([self.size_x, self.size_y]), 1):
            check_x = mark.x - pos_mod
            check_y = mark.y + pos_mod
            if check_x < 0 or check_y > self.size_y - 1:
                break
            cell = self.get_cell_by_coordinates(check_x, check_y)
            if cell and (cell.value == mark.value):
                diagonal_length = diagonal_length + 1
            else:
                break

        # count right and up
        for pos_mod in range(1, max([self.size_x, self.size_y]), 1):
            check_x = mark.x + pos_mod
            check_y = mark.y - pos_mod
            if check_x > self.size_x - 1 or check_y < 0:
                break
            cell = self.get_cell_by_coordinates(check_x, check_y)
            if cell and (cell.value == mark.value):
                diagonal_length = diagonal_length + 1
            else:
                break

        return diagonal_length + 1 >= self.winning_length

    def is_a_draw(self):
        return not self.player_x.winner and not self.player_o.winner
