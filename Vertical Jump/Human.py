class Human:
    def __init__(self, mass, height, sex, leg_girth, body_size, squat_depth, mcp = -1):
        self.mass = mass
        self.height = height
        self.sex = sex
        self.mcp = mcp
        self.leg_girth = leg_girth
        self.body_size = body_size
        self.squat_depth = squat_depth
    
    def evaluate_mcp(self):
        if self.mcp == -1:

            if self.sex == "M":
                self.mcp = 11.066 + 0.675 * self.height - \
                    0.173 * self.leg_girth - 0.299 * self.body_size
            else:
                self.mcp = -4.667 + 0.289 * self.height + \
                    0.383 * self.leg_girth + 0.301 * self.body_size
        print(self.mcp)
        return self.mcp