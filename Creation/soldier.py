import numpy as np
import matplotlib.pyplot as plt
import random


class BranchBlock(object):

    valid_targets = {
        "Ally": [""],
        "Ally side wall": [""],
        "Enemy": [""],
        "Enemy side wall": [""],
        "Me": [""]
    }

    valid_actions_with_target = {
        "Ally side wall": ["Move to", "Flee from"],
        "Ally": ["Move to", "Flee from"],
        "Enemy": ["Move to", "Flee from", "Attack"],
        "Enemy side wall": ["Move to", "Flee from"]
    }

    valid_condition_variables_for_target = {
        "Ally side wall": [""],
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
        "Enemy side wall": [""]
    }

    valid_values_for_variables = {
        "": [""],
        "Attacking me": [True, False],
        "Attacking ally": [True, False],
        "Attacking enemy": [True, False],
        "Health higher than": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "Health lower than": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "Shield higher than": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "Shield lower than": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
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
        "Ally side wall": ["Me"],
        "Enemy": ["Me", "Ally", "Ally side wall", "Enemy side wall"],
        "Enemy side wall": ["Me"]
    }

    def __init__(self, block_type):
        self.block_type = block_type
        if self.block_type == "Action":
            self.valid_targets = {"Ally": [""],
                                  "Ally side wall": [""],
                                  "Enemy": [""],
                                  "Enemy side wall": [""]}
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


class Action(BranchBlock):

    def __init__(self, params: dict, random=True):
        super().__init__("Action")
        self.params = params
        self.target = self.try_or_random("target",
                                         self.valid_targets)
        self.action = self.try_or_random("action",
                                         self.valid_actions_with_target,
                                         self.target)
        self.conditions = self.try_or_random_conditions()
        self.selection_direction = self.try_or_random(
            "selection_direction",
            self.valid_directions_for_selection_target
        )
        self.selection_target = self.try_or_random(
            "selection_target",
            self.valid_selection_targets_for_target,
            self.target)

    def try_or_random_conditions(self):
        if "conditions" in self.params.keys():
            return self.params["conditions"]

        # create conditions equal to a random amount between 0 and 3
        amount = int(1/random.random()-1) % 4
        return [Condition({"target": self.target}) for _ in range(amount)]

    def __str__(self):
        return f"Action: {self.action} {self.target} " \
               f"that is {self.selection_direction} {self.selection_target}. "\
               f"With conditions: {[str(c) for c in self.conditions]}"


class Condition(BranchBlock):

    def __init__(self, params: dict, random=True):
        super().__init__("Condition")
        self.params = params
        self.target = self.try_or_random("target",
                                         self.valid_targets)
        self.condition_variable = self.try_or_random(
            "condition_variable",
            self.valid_condition_variables_for_target,
            self.target)
        self.condition_value = self.try_or_random(
            "condition_value",
            self.valid_values_for_variables,
            self.condition_variable)

    def __str__(self):
        return f"If target {self.target} has variable: " \
               f"{self.condition_variable} " \
               f"value: {self.condition_value}"


class Soldier:

    def __init__(self, name, random_tree=True):
        self.name = name
        self.health = 10
        self.speed = 1
        self.damage = [4, 2, 1]
        self.shield = 10
        self.action_tree = []
        self.x = 0
        self.y = 0
        self.is_attacking = None
        self.is_moving_target = None
        self.is_moving_direction = None
        self.allies = []
        self.enemies = []
        self.wins = 0
        self.losses = 0
        self.win_steps = 0
        self.lose_steps = 0

        if random_tree is True:
            self.build_random_action_tree()

    def execute_tree(self):
        self.executed = False
        for branch in self.action_tree:
            if self.executed:
                continue
            self.execute_branch(branch)
        if self.executed is False:
            # No options have passed
            print("Doing nothing")

    def execute_branch(self, branch):
        for sub_branch in branch:
            if self.executed:
                continue
            if type(sub_branch) == Action:
                self.executed = self.try_execute(sub_branch)
            if type(sub_branch) == Condition:
                if not self.condition_passed(sub_branch):
                    break
            if type(sub_branch) == list:
                self.execute_branch(sub_branch)

    def build_random_action_tree(self):
        # while random.random() < 1./(len(self.action_tree)+1):
        #     self.action_tree.append(self.random_branch())
        self.action_tree = self.random_branch()

    def random_branch(self, depth=1.):
        width = 1.
        branch = []
        while random.random() < 1/width:
            width += 1
            if random.random() < 1/depth:
                branch.append([Condition({}), self.random_branch(depth+1)])
            else:
                branch.append(Action({}))
        return branch

    def try_execute(self, action: Action):
        randomly_passed = random.choice([False])
        if randomly_passed:
            print(f"Executed {action}")
        else:
            print(f"Failed executing {action}")
        return randomly_passed

    def condition_passed(self, condition: Condition):
        if condition.condition_variable == "":
            passed = True

        elif condition.condition_variable == "Health higher than":
            passed = any([x.health > condition.condition_value for x in
                          self.get_soldiers_from_target(condition.target)])

        elif condition.condition_variable == "Health lower than":
            passed = any([x.health < condition.condition_value for x in
                          self.get_soldiers_from_target(condition.target)])

        elif condition.condition_variable == "Shield higher than":
            passed = any([x.shield > condition.condition_value for x in
                          self.get_soldiers_from_target(condition.target)])

        elif condition.condition_variable == "Shield lower than":
            passed = any([x.shield > condition.condition_value for x in
                          self.get_soldiers_from_target(condition.target)])

        elif condition.condition_variable == "Attacking enemy":
            passed = any([
                any([x.is_attacking.name == y.name
                     for x in self.get_soldiers_from_target(condition.target)])
                for y in self.get_soldiers_from_target("Enemy")])

        elif condition.condition_variable == "Attacking ally":
            passed = any([
                any([
                    x.is_attacking.name == y.name
                    for x in self.get_soldiers_from_target(condition.target)
                ])
                for y in self.get_soldiers_from_target("Ally")
            ])

        elif condition.condition_variable == "Attacking me":
            passed = any([x.is_attacking.name == self.name for x in
                          self.get_soldiers_from_target(condition.target)])

        elif "Distance" in condition.condition_variable:
            distance_target = condition.condition_variable.split(" ")[2]
            if "lower" in condition.condition_variable:
                passed = any([
                    any([
                        self.get_distance(x, y) < condition.condition_value
                        for x in self.get_soldiers_from_target(distance_target)
                    ])
                    for y in self.get_soldiers_from_target(condition.target)
                ])
            else:
                passed = any([
                    any([
                        self.get_distance(x, y) > condition.condition_value
                        for x in self.get_soldiers_from_target(distance_target)
                    ])
                    for y in self.get_soldiers_from_target(condition.target)
                ])

        else:
            passed = random.choice([True])


        if passed:
            print(f"Satisfied Condition {condition}")
            return True
        print(f"Not Satisfied Condition {condition}")
        return False

    def get_soldiers_from_target(self, target):
        if target == "Ally":
            return self.allies
        if target == "Enemy":
            return self.enemies
        if target == "Me":
            return [self]

    def get_distance(self, target_1, target_2):
        if "Wall" in target_1.name or "Wall" in target_2.name:
            return abs(target_1.y - target_2.y)
        return max(abs(target_1.x-target_2.x), abs(target_1.y-target_2.y))


def print_sub_branch(root, branch):
    for sub_branch_id in range(len(branch)):
        sub_branch = branch[sub_branch_id]
        if type(sub_branch) == list:
            if type(sub_branch[0]) == Condition:
                print_sub_branch(f"{root}.{sub_branch_id+1}", sub_branch)
            else:
                print_sub_branch(f"{root}", sub_branch)
        else:
            if type(sub_branch) == Condition:
                print(f"Branch {root}: {sub_branch}")
            else:
                print(f"Branch {root}.{sub_branch_id+1}: {sub_branch}")


def test():
    soldier = Soldier("A")
    soldier.x = 1
    soldier.y = 1
    allied_wall = Soldier("Allied Wall")
    enemy_wall = Soldier("Enemy Wall")
    enemy_wall.y = 4
    enemy = Soldier("E")
    enemy.x = 3
    enemy.y = 3
    soldier.enemies = [enemy]
    enemy.enemies = [soldier]
    print(f"This soldier has {len(soldier.action_tree)} branches")
    for branch_id in range(len(soldier.action_tree)):
        print_sub_branch(f"{branch_id+1}", soldier.action_tree[branch_id])
    # print(Action({}))
    soldier.execute_tree()


if __name__ == "__main__":
    test()