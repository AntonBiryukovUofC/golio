from ..gamestate import GameState


class TestGameState:
    def test_init_of_grid(self):
        uut = GameState(10, 40)

        for ii in range(0, 10):
            assert uut.grid[ii] == [None]*40
