from typing import List
from numba import njit
from numba.core import types
from numba.typed import Dict
import numpy as np


class Cell:
    @staticmethod
    @njit
    def birth_from_parents(parents: List['Cell']):
        counter = Dict.empty(
            key_type=types.int32,
            value_type=types.int32,
        )
        for parent in parents:
            if parent.team_id in counter:
                counter[parent.team_id] += 1
            else:
                counter[parent.team_id] = 1

        if len(counter) == 1:
            new_id = list(counter.keys())[0]
        else:
            max_count = max(counter.values())
            possible_parents = [key for key in counter if counter[key] == max_count]
            new_id = np.random.choice(possible_parents)

        return Cell(team_id=new_id)

        # parent_id_count = Counter([cell.team_id for cell in parents])
        # if len(parent_id_count) == 1:
        #     new_id = parent_id_count.most_common(1)[0][0]
        # else:
        #     highest_count = parent_id_count.most_common(1)[0][1]
        #     possible_parents = [key for key in parent_id_count if parent_id_count[key] == highest_count]
        #     new_id = random.choice(possible_parents)
        #
        # return Cell(team_id=new_id)

    def __init__(self, team_id: int):
        self.team_id = team_id
