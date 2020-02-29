import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import random


class Terrain:

    def __init__(self, width=5, height=10):
        self.area = np.empty([height, width], dtype="<U10")
        for terrain_x in range(width):
            for terrain_y in range(height):
                block = Block("empty")
                self.area[terrain_y, terrain_x] = block.short_property()
        self.setup_walls(width, height)
        print(self.area)

    def setup_walls(self, width, height, amount=None):
        if amount is None:
            amount = random.choice(list(range(5)))
        for wall in range(amount):
            if random.choice(["vertical", "horizontal"]) == "vertical":
                start_y = random.randint(1, height)
                end_y = random.randint(start_y, height)
                x = random.randint(1, width - 1)
                for y in range(start_y, end_y):
                    self.area[y, x] = "X"
            else:
                pass

    def pit(self, tribe, opponent):
        # todo implement
        pass


class Block:

    def __init__(self, property=None):
        self.property = property or random.choice(["empty", "wall", "pit"])

    def short_property(self):
        return {"empty": " ",
                "wall": "X",
                "pit": "U"}[self.property]

    def __str__(self):
        return self.property