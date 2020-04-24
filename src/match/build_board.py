from math import ceil, sqrt

from common.gamestate import GameState


def build_board(player_boards):
    num_players = len(player_boards)
    needed_board_size_x = ceil(sqrt(num_players))
    needed_board_size_y = ceil(num_players/needed_board_size_x)

    single_board_y = player_boards[0][1].shape[0]
    single_board_x = player_boards[0][1].shape[1]

    for ii, board in player_boards:
        if (board.shape[0] != single_board_y or
                board.shape[1] != single_board_x):
            raise Exception(f"Player id {ii} has a board that does not match other board size, unable to build"
                            f"a game board.")

    y = single_board_y * needed_board_size_y
    x = single_board_x * needed_board_size_x

    gs = GameState(y, x)

    y_counter = 0
    for ii in range(0, num_players):
        sub_board = GameState.from_numpy_array(player_boards[ii][1] * (ii+1))
        gs = gs.apply_subboard(y_counter * single_board_y, (ii - y_counter * needed_board_size_x) * single_board_x,
                               sub_board)
        if ii - y_counter*needed_board_size_x >= needed_board_size_x - 1:
            y_counter += 1

    return gs
