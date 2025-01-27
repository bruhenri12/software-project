from rsoccer_gym.Entities import Robot
from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.PathPlanning import PathPlanning
from utils.Point import Point

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)
        self.target = None
        self.teammates_agents: dict[int, 'ExampleAgent'] = dict()
        self.obstacles: list[Point] = []
        self.path_samples: list[Point] = []
        self.sample_target = None

    def step(self, self_robot : Robot, 
             opponents: dict[int, Robot] = dict(), 
             teammates: dict[int, Robot] = dict(), 
             teammates_agents: dict[int, 'ExampleAgent'] = dict(),
             targets: list[Point] = [], 
             keep_targets=False) -> Robot:
        self.teammates_agents = teammates_agents
        return super().step(self_robot, opponents, teammates, targets, keep_targets)

    def decision(self):
        if len(self.targets) == 0:
            return

        # Define the closest target to this agent
        self.target = self.set_target(self.closest_target())

        # Check all obstacles in the field of view
        field_obstacles = [Point(rob.x,rob.y) for rob in self.opponents.values()]
        field_obstacles += [rob.pos for rob in self.teammates_agents.values() if rob != self]
        self.obstacles: list[Point] = PathPlanning.check_obstacles(field_obstacles, self.pos, self.target, Navigation.degrees_to_radians(40))

        #TO-DO: Sample based path finding

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.target)
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass

    def closest_target(self) -> Point:
        return min(self.targets, key=lambda target: self.pos.dist_to(target))

    def set_target(self, target) -> Point:
        """ Set the target for this agent. """

        # Check if another teammate is focusing the same target
        teammates_with_same_target = [
            teammate_agent for teammate_agent in self.teammates_agents.values()
            if teammate_agent.target != None and teammate_agent.target == target
        ]

        if len(teammates_with_same_target) == 0:
            return target
        
        closer_teammate = min(teammates_with_same_target, key=lambda teammate: teammate.pos.dist_to(target))

        # If there is a teammate closer to the target, this agent will focus on another target
        if closer_teammate.pos.dist_to(target) < self.pos.dist_to(target):
            # If the teammate is closer to the last available target, this agent will stop
            if (len(self.targets) == 1):
                return self.pos
            
            self.targets.remove(target)
            return self.set_target(self.closest_target())
        
        # If this agent is closer to the target, it will focus on it
        return target
