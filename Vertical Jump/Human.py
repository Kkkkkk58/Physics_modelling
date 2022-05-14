class Human:
    def __init__(self, mass, height, sex, leg_girth, body_size, squat_depth, mcp = -1):
        self.mass = mass
        self.height = height
        self.sex = sex
        self.mcp = mcp
        self.leg_girth = leg_girth
        self.body_size = body_size
        self.squat_depth = squat_depth
    
    def evaluate_mcp(self): # обхват голени, размер туловища
        if self.human.mcp == -1:

            if self.human.sex == "M":
                self.human.mcp = 11.066 + 0.675 * self.human.height - \
                    0.173 * self.human.leg_girth - 0.299 * self.human.body_size
            else:
                self.mcp = -4.667 + 0.289 * self.height + \
                    0.383 * self.human.leg_girth + 0.301 * self.human.body_size

        return self.mcp