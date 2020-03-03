import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import random

from terrain import Terrain
from soldier import Soldier

class Tribe:
    def __init__(self):
        pass


""" Initialize tribes

Params
------
amount (int): the amount of tribes to be initialized.
"""


def initialize_tribes(amount=4):
    tribes = []
    for tribe in range(amount):
        tribes.append(Tribe())
    return tribes


""" Fight amongst all tribes
 *
 * Let every tribe fight against a random other tribe (including itself).
 * 
 * Params
 * ------
 * tribes: The tribes that will be fighting
 * terrain: The terrain the tribes will fight on. Will be randomized when None.
 *
 * Returns
 * -------
 * results: list of Result from the fights
 */"""


def fight(tribes, terrain=None):
    results = []
    for tribe in tribes:
        opponent = random.choice(tribes)
        terrain = terrain or Terrain()
        results.append(terrain.pit(tribe, opponent))
    return results


def store_best(RESULTS):
    # todo implement
    pass


def visualize_best(tribes, results, terrain):
    # todo implement
    pass


def reinforce(tribes, results):
    # todo implement
    return tribes


def main():
    tribes = initialize_tribes(amount=4)
    for i in range(100):
        results = []
        terrain = Terrain()
        for j in range(10):
            results.append(fight(tribes, terrain))
        store_best(results)
        visualize_best(tribes, results, terrain)  # Going to be on other thread
        tribes = reinforce(tribes, results)


if __name__ == "__main__":
    main()