import random


class BranchBlock:

    valid_targets = {
        "Ally": [""],
        "Allied wall": [""],
        "Enemy": [""],
        "Enemy wall": [""],
        "Me": [""]
    }

    valid_actions_with_target = {
        "Allied wall": ["Move to", "Flee from"],
        "Ally": ["Move to", "Flee from"],
        "Enemy": ["Move to", "Flee from", "Attack"],
        "Enemy wall": ["Move to", "Flee from"]
    }

    valid_attack_pairs = {
        "attack_pair": [
            ["Me", "Enemy"],
            ["Ally", "Enemy"],
            ["Enemy", "Me"],
            ["Enemy", "Ally"],
        ]
    }

    valid_distance_pairs = {
        "distance_pairs": [
            ["Me", "Enemy"],
            ["Me", "Ally"],
            ["Me", "Allied wall"],
            ["Me", "Enemy wall"],
            ["Ally", "Allied wall"],
            ["Ally", "Enemy wall"],
            ["Enemy", "Allied wall"],
            ["Enemy", "Enemy wall"],
        ]
    }

    valid_condition_variables_for_target = {
        "Allied wall": [""],
        "Ally": ["Attacking enemy",
                 "Health higher than", "Health lower than",
                 "Shield higher than", "Shield lower than",
                 "Distance from me higher than",
                 "Distance from me lower than",
                 "Distance from enemy higher than",
                 "Distance from enemy lower than"],
        "Enemy": ["Attacking me", "Attacking ally",
                  "Health higher than", "Health lower than",
                  "Shield higher than", "Shield lower than",
                  "Distance from me higher than",
                  "Distance from me lower than",
                  "Distance from ally higher than",
                  "Distance from ally lower than"],
        "Me": ["Attacking enemy",
               "Health higher than", "Health lower than",
               "Shield higher than", "Shield lower than",
               "Distance from enemy higher than",
               "Distance from enemy lower than",
               "Distance from ally higher than",
               "Distance from ally lower than"],
        "Enemy wall": [""]
    }

    valid_values_for_variables = {
        "": [""],
        "Attacking": [True, False],
        "Attacking me": [True, False],
        "Attacking ally": [True, False],
        "Attacking enemy": [True, False],
        "Health": list(range(11)),
        "Health higher than": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "Health lower than": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "Shield": list(range(11)),
        "Shield higher than": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "Shield lower than": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "Distance from": list(range(4)),
        "Distance from ally lower than": [3, 2, 1],
        "Distance from ally higher than": [0, 1, 2],
        "Distance from enemy lower than": [3, 2, 1],
        "Distance from enemy higher than": [0, 1, 2],
        "Distance from me lower than": [3, 2, 1],
        "Distance from me higher than": [0, 1, 2],
    }

    valid_directions_for_selection_target = {
        "Closest to": None,
        "Furthest from": None
    }

    valid_selection_targets_for_target = {
        "Ally": ["Me", "Enemy", "Ally side wall", "Enemy side wall"],
        "Allied wall": ["Me"],
        "Enemy": ["Me", "Ally", "Ally side wall", "Enemy side wall"],
        "Enemy wall": ["Me"]
    }

    valid_comparisons = {
        "comparisons": [
            "higher than",
            "lower than",
            "higher than or equal to",
            "lower than or equal to",
            "equal to",
        ]
    }

    def __init__(self, block_type):
        self.params = {}
        self.block_type = block_type
        if self.block_type == "Action":
            self.valid_targets = {"Ally": [""],
                                  "Allied wall": [""],
                                  "Enemy": [""],
                                  "Enemy wall": [""]}
        else:
            self.valid_targets = {"Ally": [""],
                                  "Enemy": [""],
                                  "Me": [""]}

    def try_or_random(self, key, choices: list or dict, choice_key=None):
        if key in self.params.keys():
            return self.params[key]
        if choice_key is None:
            return random.choice(list(choices.keys()))
        return random.choice(choices[choice_key])


