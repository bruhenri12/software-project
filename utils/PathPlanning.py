from utils.Point import Point
import math
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

            # If the target vector magnitude is zero, the origin is at the target
            if target_vector_magnitude == 0:
                return False
            
            # If the obstacle vector magnitude is zero, the obstacle is at the target
            if obstacle_vector_magnitude == 0:
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
