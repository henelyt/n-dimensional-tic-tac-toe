from ndimensionaltictactoe.exceptions.cell_in_use_exception import CellInUseException
from ndimensionaltictactoe.exceptions.grid_too_large_exception import GridTooLargeException
from ndimensionaltictactoe.exceptions.grid_too_small_exception import GridTooSmallException
from ndimensionaltictactoe.exceptions.out_of_bounds_exception import OutOfBoundsException
from ndimensionaltictactoe.exceptions.winning_length_too_long_exception import WinningLengthTooLongException
from ndimensionaltictactoe.exceptions.winning_length_too_short import WinningLengthTooShortException
from ndimensionaltictactoe.models.mark import Mark


class Game(object):
    def __init__(self,
                 key,
                 player_x_key,
                 player_o_key,
                 size_x=3,
                 size_y=3,
                 dimensions=2,
                 winning_length=3):
        if dimensions < 2:
            raise GridTooSmallException
        if dimensions > 2:
            raise GridTooLargeException
        if winning_length < 1:
            raise WinningLengthTooShortException
        if winning_length > min([size_x, size_y]):
            raise WinningLengthTooLongException

        self.key = key
        self.size_x = size_x
        self.size_y = size_y
        self.dimensions = dimensions
        self.player_x_key = player_x_key
        self.player_o_key = player_o_key
        self.cells = []

    def get_cell_by_coordinates(self, coordinates):
        self._validate_coordinates(coordinates)
        return next((mark for mark in self.cells if mark.coordinates == coordinates), None)

    def mark_cell_by_coordinates(self, coordinates, mark):
        if not self.get_cell_by_coordinates(coordinates):
            self.cells.append(Mark(coordinates, mark))
        else:
            raise CellInUseException

    def _validate_coordinates(self, coordinates):
        if coordinates[0] < 0 or coordinates[1] < 0:
            raise OutOfBoundsException()

        if coordinates[0] > self.size_x - 1 or coordinates[1] > self.size_y - 1:
            raise OutOfBoundsException()
