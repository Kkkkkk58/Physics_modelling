class Human:
    def __init__(self, mass, height, sex, leg_girth, body_size, squat_depth, mcp = -1):
        self.mass = mass
        self.height = height / 100.0
        self.sex = sex
        self.mcp = mcp if mcp == -1 else mcp / 100.0
        self.leg_girth = leg_girth / 100.0
        self.body_size = body_size / 100.0
        self.squat_depth = squat_depth / 100.0
    
    def evaluate_mcp(self):
        if self.mcp == -1:

            if self.sex == "M":
                self.mcp = (11.066 + 0.675 * self.height * 100 - \
                    0.173 * self.leg_girth * 100 - 0.299 * self.body_size * 100) / 100.0
            else:
                self.mcp = (-4.667 + 0.289 * self.height * 100 + \
                    0.383 * self.leg_girth * 100 + 0.301 * self.body_size * 100) / 100.0
        return self.mcp