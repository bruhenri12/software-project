from rsoccer_gym.Entities import Robot
from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)
        self.target = None
        self.teammates_agents: dict[int, 'ExampleAgent'] = dict()

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

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.target)
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass

    def closest_target(self) -> Point:
        return min(self.targets, key=lambda target: self.pos.dist_to(target))

    def set_target(self, target) -> Point:
        """
        Set the target for this agent. 
        If there is another teammate closer to the target, this agent will focus on another target.
        If no other target is available, this agent will focus on the next closest target.
        Returns:
            Point: The closest possible target to this agent
        """

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
            if (len(self.targets) == 1):
                return self.pos
            # If there is no other target, this agent will focus on the next closest target
            self.targets.remove(target)
            return self.set_target(self.closest_target())
        
        return target
