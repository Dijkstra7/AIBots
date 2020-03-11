import random
from action import Action
from condition import Condition, HealthAmount, AttackingCondition, \
    ShieldAmount, DistanceCondition


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
        self.enemy_wall = None
        self.allied_wall = None

        self.action_tree = []
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
            if isinstance(sub_branch, Action):
                self.executed = self.try_execute(sub_branch)
            if isinstance(sub_branch, Condition):
                # print("Checking " + str(sub_branch))
                if not self.condition_passed(sub_branch):
                    break
            if type(sub_branch) == list:
                self.execute_branch(sub_branch)

    def build_random_action_tree(self):
        while random.random() < 1./(len(self.action_tree)+1):
            self.action_tree.append(self.random_branch())
        # self.action_tree = self.random_branch()

    def random_branch(self, depth=1.):
        width = 1.
        branch = []
        while random.random() < 1/width:
            width += 1
            if random.random() < 1/depth:
                branch.append([Condition.generate_condition(self, {}),
                               self.random_branch(depth+1)])
            else:
                branch.append(Action({}))
        return branch

    def try_execute(self, action: Action):
        # Try to execute the action
        for condition in action.conditions:
            print(">Checking condition to execute this action:\n>",
                  condition, "\n>",
                  f"This condition has"
                  f" {['', 'not '][condition.passed(self)]}"
                  f"passed")

        randomly_passed = random.choice([False])
        if randomly_passed:
            print(f"Executed {action}")
        else:
            print(f"Failed executing {action}")
        return randomly_passed

    def condition_passed(self, condition: Condition):
        if condition.condition_variable == "":
            passed = True
        else:
            passed = condition.passed(self)

        if passed:
            print(f"Satisfied Condition {condition}")
            return True
        print(f"Not Satisfied Condition {condition}")
        return False

    def get_soldiers_from_target(self, target):
        if target in ["Ally", "ally"]:
            return self.allies
        if target in ["Enemy", "enemy"]:
            return self.enemies
        if target in ["Me", "me"]:
            return [self]
        if target in ["Enemy wall", "enemy wall"]:
            return [self.enemy_wall]
        if target in ["Allied wall", "allied wall"]:
            return [self.allied_wall]

        print(target)

    def get_distance(self, target_1, target_2):
        if "wall" in target_1.name or "wall" in target_2.name:
            return abs(target_1.y - target_2.y)
        return max(abs(target_1.x-target_2.x), abs(target_1.y-target_2.y))


def print_sub_branch(root, branch):
    for sub_branch_id in range(len(branch)):
        sub_branch = branch[sub_branch_id]
        if type(sub_branch) == list:
            if isinstance(sub_branch[0], Condition):
                print_sub_branch(f"{root}.{sub_branch_id+1}", sub_branch)
            else:
                print_sub_branch(f"{root}", sub_branch)
        else:
            if isinstance(sub_branch, Condition):
                print(f"Branch {root}: {sub_branch}")
            else:
                print(f"Branch {root}.{sub_branch_id+1}: {sub_branch}")


def test():
    soldier = Soldier("A")
    soldier.x = 1
    soldier.y = 1
    ally = Soldier("B")
    ally.x = 2
    ally.y = 1
    allied_wall = Soldier("Allied wall")
    enemy_wall = Soldier("Enemy wall")
    enemy_wall.y = 6
    enemy = Soldier("E")
    enemy.x = 5
    enemy.y = 5
    soldier.enemies = [enemy]
    soldier.allies = [ally]
    ally.enemies = [enemy]
    ally.allies = [soldier]
    enemy.enemies = [soldier, ally]
    for soldier in ally.enemies:
        soldier.enemy_wall = allied_wall
        soldier.allied_wall = enemy_wall
    for soldier in enemy.enemies:
        soldier.allied_wall = allied_wall
        soldier.enemy_wall = enemy_wall
    enemy.action_tree = [[Action({"target": "Enemy",
                                  "action": "Attack",
                                  "conditions": [],
                                  "selection_direction": "Closest from",
                                  "selection_target": "Me"})]]
    print(f"This soldier has {len(soldier.action_tree)} branches")
    print_sub_branch("1", soldier.action_tree)
    # for i in range(10):
    soldier.execute_tree()
    enemy.execute_tree()


if __name__ == "__main__":
    test()
