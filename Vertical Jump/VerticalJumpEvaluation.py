import Human

class VerticalJumpEvaluation:
    def __init__(self, human):
        self.human = human
        self.human.evaluate_mcp()
