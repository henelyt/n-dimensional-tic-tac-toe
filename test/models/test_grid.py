import uuid

import pytest

from ndimensionaltictactoe.models.mark import X_MARK, O_MARK
from ndimensionaltictactoe.exceptions.grid_too_large_exception import GridTooLargeException
from ndimensionaltictactoe.exceptions.grid_too_small_exception import GridTooSmallException
from ndimensionaltictactoe.models.game import Game
from ndimensionaltictactoe.models.mark import Mark

PLAYER_X_KEY = uuid.uuid4()
PLAYER_O_KEY = uuid.uuid4()


def test__init__should_raise_exception_when_dimensions_less_than_two():
    with pytest.raises(GridTooSmallException):
        Game('test-grid', PLAYER_X_KEY, PLAYER_O_KEY, 3, 1)


def test__init__should_raise_exception_when_dimensions_greater_than_two():
    with pytest.raises(GridTooLargeException):
        Game('test-grid', PLAYER_X_KEY, PLAYER_O_KEY, 3, 3)


def test__get_cell_by_coordinates__returns_mark_at_coordinates():
    existing_mark_1 = Mark(X_MARK, (0, 0))
    existing_mark_2 = Mark(O_MARK, (1, 1))
    grid = Game('test-grid', PLAYER_X_KEY, PLAYER_O_KEY)
    grid.cells.append(existing_mark_1)
    grid.cells.append(existing_mark_2)

    actual_mark = grid.get_cell_by_coordinates((1, 1))

    assert actual_mark == existing_mark_2


def test__get_cell_by_coordinates__returns_none_if_coordinates_are_empty():
    existing_mark_1 = Mark(X_MARK, (0, 0))
    grid = Game('test-grid', PLAYER_X_KEY, PLAYER_O_KEY)
    grid.cells.append(existing_mark_1)

    actual_mark = grid.get_cell_by_coordinates((1, 1))

    assert not actual_mark
