import random
from branchBlock import BranchBlock
from condition import Condition

class Action(BranchBlock):

    def __init__(self, params: dict, _random=True):
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
        # TO TEST: check if the entity should be self or target
        return [Condition.generate_condition(self.target,
                                             {"target": self.target})
                for _ in range(amount)]

    def __str__(self):
        return f"Action: {self.action} {self.target} " \
               f"that is {self.selection_direction} {self.selection_target}." \
               f" With conditions: {[str(c) for c in self.conditions]}"


