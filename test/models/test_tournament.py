import unittest
from uuid import uuid4

from mock import patch, MagicMock

from ndimensionaltictactoe.models.player import Player
from ndimensionaltictactoe.models.round import Round
from ndimensionaltictactoe.models.tournament import Tournament


class TestTournament(unittest.TestCase):
    def test__play_round__calls_game_thread_once_when_two_players_in_lobby(self):
        player_1 = Player(uuid4(), "player 1", "update_url1")
        player_2 = Player(uuid4(), "player 2", "update_url2")
        lobby = {player_1.key: player_1,
                 player_2.key: player_2}

        tournament = Tournament(uuid4(), "Test Tournament", lobby)

        round = Round(1, 3, 3, 3)

        mock_scheduler = MagicMock(autospec=True)
        tournament.play_round(mock_scheduler, round)

        self.assertEqual(1, mock_scheduler.add_job.call_count)

