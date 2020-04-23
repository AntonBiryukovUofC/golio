from typing import List
import numpy as np


class Cell:
    @staticmethod
    def birth_from_parents(parents: List['Cell']):
        counter = {}
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

    def __init__(self, team_id: int):
        self.team_id = team_id
