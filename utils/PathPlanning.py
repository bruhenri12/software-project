from utils.Point import Point
import math
import random

class PathPlanning:

    @staticmethod
    def check_obstacles(obstacles: list[Point], origin: Point, target: Point, theta: float) -> list[Point]:
        """
        Checks if any points in the obstacles list are within the field of view (FOV) defined by the origin, target, and theta (in radians).
        """
        def is_within_fov(obstacle: Point, origin: Point, target: Point, theta: float) -> bool:
            target_direction = origin.direction_to(target)
            obstacle_direction = origin.direction_to(obstacle)
            
            target_vector_magnitude = target_direction.magnitude()
            obstacle_vector_magnitude = obstacle_direction.magnitude()

            if target_vector_magnitude == 0: # The origin is at the target
                return False
            
            if obstacle_vector_magnitude == 0: # The obstacle is at the target
                return True

            # Calculate the angle between the two direction vectors using the cosine rule
            vectors_angle_cos = target_direction.dot(obstacle_direction) / (target_vector_magnitude * obstacle_vector_magnitude)
            angle_to_obstacle = math.acos(vectors_angle_cos)
            
            return angle_to_obstacle <= theta / 2

        obstacles_in_fov = [
            obstacle for obstacle in obstacles 
            if is_within_fov(obstacle, origin, target, theta) and obstacle.dist_to(origin) < target.dist_to(origin)
        ]
        return obstacles_in_fov

    @staticmethod
    def generate_samples(obstacles: list[Point], offset: float, num_samples: int) -> list[Point]:
        """
        Generates a list of random samples around each obstacle with an offset. The number of samples and the maximum distance from the obstacle are specified.
        """
        if len(obstacles) == 0:
            return []
        
        def generate_offset(offset: float):
            return random.uniform(-offset, offset)
        
        samples = []

        for obstacle in obstacles:
            for _ in range(num_samples):
                while True:
                    sample = Point(obstacle.x + generate_offset(offset), obstacle.y + generate_offset(offset))
            
                    # Check if the sample is not within the obstacle
                    if all(sample.dist_to(obs_check) > offset for obs_check in obstacles):
                        samples.append(sample)
                        break

        return samples
