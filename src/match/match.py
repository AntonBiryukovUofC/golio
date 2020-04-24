from match.build_board import build_board


def play_match(final_gen, lookback_num_gens, player_boards):
    gs = build_board(player_boards)

    print(gs.grid)