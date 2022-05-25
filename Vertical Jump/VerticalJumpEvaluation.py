from Constants import GRAVITATIONAL_ACCELERATION
from Human import *
from math import *
from functools import lru_cache

class VerticalJumpEvaluation:
    def __init__(self, human, takeoff_velocity):
        self.human = human
        self.human.evaluate_mcp()
        self.takeoff_velocity = takeoff_velocity

    # t_0 = 2 * d / V_0
    def takeoff_time(self):
        return 2.0 * self.human.squat_depth / self.takeoff_velocity
    
    # a = V_0 / t_0
    def takeoff_acceleration(self):
        return self.takeoff_velocity / self.takeoff_time()

    # Y = Y_0 + V_0 * t - 1/2 * g * t^2
    def coordinate(self, time):
        return self.human.mcp + self.takeoff_velocity * time - (GRAVITATIONAL_ACCELERATION * time**2) / 2.0\
            if time >= 0 else (self.human.mcp - self.human.squat_depth) + self.takeoff_velocity * (self.takeoff_time() + time) - (self.takeoff_acceleration() * (self.takeoff_time() + time)**2) / 2.0

    # S = s_0 + V_0 * t + 1/2 * g * t^2
    def distance(self, time):
        return self.human.squat_depth + self.takeoff_velocity * time + (GRAVITATIONAL_ACCELERATION * time**2) / 2.0\
            if time >= 0 else self.coordinate(time) - (self.human.mcp - self.human.squat_depth)
   
    
    def angle_sin(self, time):
       return 1 if time >= 0 \
           else (self.human.hip_size - (self.human.mcp - self.coordinate(time))) / self.human.hip_size

    # V = V_0 - g * t
    def velocity(self, time):
        return self.takeoff_velocity - GRAVITATIONAL_ACCELERATION * time\
            if time >= 0 else self.takeoff_acceleration() * (self.takeoff_time() + time)

    # F = m * g * (h + d) / h
    def push_force(self):
        return self.human.mass * GRAVITATIONAL_ACCELERATION * (self.max_height() - self.human.mcp + self.human.squat_depth) / self.human.squat_depth
    
    def push_force_projection(self, time):
        return self.push_force() * self.angle_sin(time)
    
    # t = 2 * V_0 / g
    def flight_time(self):
        return 2.0 * self.takeoff_velocity / GRAVITATIONAL_ACCELERATION

    # H = H_0 + V_0 ^ 2 / (2 * g)
    def max_height(self):
        return self.human.mcp +  self.takeoff_velocity**2 / (2.0 * GRAVITATIONAL_ACCELERATION)

    # E + E_к + E_п
    def full_energy(self, time):
        return self.potential_energy(time) + self.kinetic_energy(time)
    
    # E_к = m * V^2 / 2
    def kinetic_energy(self, time):
        return self.human.mass * self.velocity(time)**2 / 2.0
    
    # E_п = m * g * h
    def potential_energy(self, time):
        return self.human.mass * GRAVITATIONAL_ACCELERATION * self.coordinate(time)

    # IDK
    def support_reaction_force(self, time):
        return self.human.mass * GRAVITATIONAL_ACCELERATION + self.push_force_projection(time) if time < 0 \
            else 0

    # A = F * r * cos{a}
    @lru_cache(None)
    def support_reaction_work(self, time):
        return self.support_reaction_force(time) * (self.distance(time) - self.distance(-self.takeoff_time())) * sqrt(1 - self.angle_sin(time)**2)\
            + self.support_reaction_work(time - 0.01) if time >= -(self.takeoff_time()) else 0

    # N = A / t
    def support_reaction_power(self, time):
        return self.support_reaction_work(time) * 1.0 / (self.takeoff_time() + time) if time != 0\
            else self.support_reaction_power(time - 0.01)

    # def optimal_jump(self):
    #     muscle_force = 3 * self.human.mass * GRAVITATIONAL_ACCELERATION


    
    
    

