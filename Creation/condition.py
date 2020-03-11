import random
from branchBlock import BranchBlock
# from soldier import Soldier


class Condition(BranchBlock):

    @staticmethod
    def generate_condition(entity, params, _random=True):
        if "condition_variable" not in params.keys():
            if _random is True:
                condition_class = random.choice([HealthAmount,
                                                 ShieldAmount,
                                                 AttackingCondition,
                                                 DistanceCondition])
            else:
                condition_class = HealthAmount
        else:
            condition_class = params["condition_variable"]
        return condition_class(entity, params, _random)

    def __init__(self, params: dict, _random=True):
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
        self.comparison = ""
        self.opponent = ""

    def __str__(self):
        return f"If {self.target} has " \
               f"{self.condition_variable} " \
               f"{self.opponent}{[' ', ''][self.opponent == '']}"\
               f"{self.comparison}{[' ', ''][self.comparison == '']}" \
               f"value: {self.condition_value}"

    def passed(self, entity):
        return True


class ConditionAmount(Condition):

    def __init__(self, entity, params: dict, _random=True):
        super().__init__(params, _random)
        self.entity = entity
        self.comparison = self.try_or_random(
            "comparison", self.valid_comparisons, "comparisons")

    def passed_amount(self, targets_state):
        if "equal" in self.comparison and any(
                [state == self.condition_value for state in targets_state]
        ):
            return True
        if "higher" in self.comparison and any(
                [state > self.condition_value for state in targets_state]
        ):
            return True
        return "lower" in self.comparison and any(
            [state < self.condition_value for state in targets_state]
        )


class HealthAmount(ConditionAmount):

    def __init__(self, entity, params: dict, _random=True):
        params["condition_variable"] = "Health"
        super().__init__(entity, params, _random)

    def passed(self, entity):
        targets = entity.get_soldiers_from_target(self.target)
        targets_state = [target.health for target in targets]
        return self.passed_amount(targets_state)


class ShieldAmount(ConditionAmount):

    def __init__(self, entity, params: dict, _random=True):
        params["condition_variable"] = "Shield"
        super().__init__(entity, params, _random)

    def passed(self, entity):
        targets = entity.get_soldiers_from_target(self.target)
        targets_state = [target.shield for target in targets]
        return self.passed_amount(targets_state)


class AttackingCondition(Condition):

    def __init__(self, entity, params: dict, _random=True):
        self.params = params
        self.params["condition_variable"] = "Attacking"
        self.params["target"], self.params["opponent"] = self.try_or_random(
            "attack_pair", self.valid_attack_pairs, "attack_pair"
        )
        super().__init__(self.params, _random)
        self.entity = entity
        self.opponent = self.params["opponent"]

    def passed(self, entity):
        targets = entity.get_soldiers_from_target(self.target)
        opponents = entity.get_soldiers_from_target(self.opponent)
        # print(self)
        return any([
            any([
                    (target.is_attacking is not None) and
                    ((target.is_attacking.name == opponent.name) ==
                     self.condition_value)
                    for opponent in opponents
                ])
            for target in targets
            ])


class DistanceCondition(Condition):

    def __init__(self, entity, params: dict, _random=True):
        self.entity = entity
        self.params = params
        self.params["condition_variable"] = "Distance from"
        self.params["target"], self.params["opponent"] = self.try_or_random(
            "distance_pair", self.valid_distance_pairs, "distance_pairs"
        )
        self.params["comparison"] = self.try_or_random(
            "comparison", self.valid_comparisons, "comparisons")
        super().__init__(params)
        self.opponent = self.params["opponent"]
        self.comparison = self.params["comparison"]

    def passed(self, entity):
        distances = []
        for target in entity.get_soldiers_from_target(self.target):
            for opponent in entity.get_soldiers_from_target(self.opponent):
                distances.append(self.get_distance(target, opponent))
        if "equal" in self.comparison and any(
                [self.condition_value == distance for distance in distances]
        ):
            return True
        if "lower" in self.comparison and any(
            [self.condition_value < distance for distance in distances]
        ):
            return True
        if "higher" in self.comparison and any(
            [self.condition_value > distance for distance in distances]
        ):
            return True
        return False

    @staticmethod
    def get_distance(target, opponent):
        if 'wall' in opponent.name:
            return abs(target.y - opponent.y)
        return max(abs(target.x - opponent.x), abs(target.y - opponent.y))

