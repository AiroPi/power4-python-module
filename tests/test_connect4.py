from pprint import pprint
from sqlite3 import connect

import connect4
import pytest


def test_init():
    c4 = connect4.Connect4(dimensions=(4, 4))
    assert c4.board == [[connect4.Players.NONE] * 4 for i in range(4)]
    assert c4.strboard() == ((' ' * 4 + '\n') * 4)[:-1]


def _test_victories(plays: tuple[int, ...], win_points: set[tuple[int, int]], winner: connect4.Players):
    c4 = connect4.Connect4()
    for play in plays[:-1]:
        assert c4.play(play) == set()

    assert c4.play(plays[-1]) == win_points

    with pytest.raises(connect4.GameOver) as exception:
        c4.play(0)

    assert exception.value.winner == winner


def test_vertical_victory():
    _test_victories(
        (0, 1, 0, 1, 0, 1, 0),
        {(5, 0), (4, 0), (3, 0), (2, 0)},
        connect4.Players.ONE
    )


def test_horizontal_victory():
    _test_victories(
        (0, 0, 1, 1, 2, 2, 3),
        {(5, 0), (5, 1), (5, 2), (5, 3)},
        connect4.Players.ONE
    )


def test_diagonal1_victory():
    _test_victories(
        (0, 1, 1, 2, 2, 6, 2, 3, 3, 3, 3),
        {(2, 3), (3, 2), (4, 1), (5, 0)},
        connect4.Players.ONE
    )


def test_diagonal2_victory():
    _test_victories(
        (5, 6, 4, 5, 4, 4, 3, 3, 3, 3),
        {(5, 6), (4, 5), (3, 4), (2, 3)},
        connect4.Players.TWO
    )


def test_multiple_victory():
    _test_victories(
        (0, 0, 0, 0, 1, 1, 1, 1, 2, 5, 2, 5, 2, 2, 6, 3, 6, 3, 6, 3, 5, 3),
        {(2, 0), (2, 1), (2, 2), (2, 3), (5, 3), (4, 3), (3, 3), (2, 3)},
        connect4.Players.TWO
    )
