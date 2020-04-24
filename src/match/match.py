from match.build_board import build_board

from collections import deque, defaultdict


def play_match(final_gen, lookback_num_gens, player_boards):
    gs = build_board(player_boards)

    player_index_to_id = dict(zip(range(1, len(player_boards)+1), [item[0] for item in player_boards]))

    counts = deque([], maxlen=lookback_num_gens)
    for ii in range(0, final_gen):
        cell_counts = gs.cell_counts()
        counts.append({
            player_index_to_id[idx]: value for idx, value in cell_counts.items()
        })
        gs = gs.step()

    print(f"Counts are: {counts}")
    if len(counts[-1]) == 1:
        # only one player standing at the end, they're the winner
        winner = list(counts[-1].keys())[0]
        print(f"Winner was {winner}")
        return winner
    else:
        # Take average of the last runs
        total_counts = defaultdict(lambda: 0)
        for gen in counts:
            for player_id in gen:
                total_counts[player_id] += gen[player_id]

        totals = list(total_counts.items())
        totals.sort(key=lambda item: item[1], reverse=True)
        print(f"Totals are: {totals}")
        winner = totals[0][0]
        print(f"Winner is {winner}")

        return winner