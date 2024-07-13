import math
from typing import Tuple

class Delta3DPrinterBalance:
    def __init__(self, tower_radius: float, arm_length: float):
        self.tower_radius = tower_radius
        self.arm_length = arm_length

    def calculate_arm_heights(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        # Calculate the distance from the center for each tower
        tower_positions = [
            (-self.tower_radius * math.sqrt(3) / 2, -self.tower_radius / 2),
            (self.tower_radius * math.sqrt(3) / 2, -self.tower_radius / 2),
            (0, self.tower_radius)
        ]

        arm_heights = []
        for tower_x, tower_y in tower_positions:
            # Calculate the horizontal distance from the tower to the target point
            dx = x - tower_x
            dy = y - tower_y
            horizontal_distance = math.sqrt(dx**2 + dy**2)

            # Use Pythagorean theorem to calculate the required arm height
            arm_height = z + math.sqrt(self.arm_length**2 - horizontal_distance**2)
            arm_heights.append(arm_height)

        return tuple(arm_heights)

    def optimize_print_area(self, max_height: float, step: float = 1.0):
        best_volume = 0
        best_radius = 0

        for test_radius in range(1, int(self.tower_radius), int(step)):
            volume = 0
            for x in range(-test_radius, test_radius + 1, int(step)):
                for y in range(-test_radius, test_radius + 1, int(step)):
                    if x**2 + y**2 <= test_radius**2:
                        try:
                            heights = self.calculate_arm_heights(x, y, 0)
                            if all(0 <= h <= max_height for h in heights):
                                volume += step**2 * max_height
                        except ValueError:
                            pass  # Skip invalid points

            if volume > best_volume:
                best_volume = volume
                best_radius = test_radius

        return best_radius, best_volume

# Example usage
if __name__ == "__main__":
    # Initialize with tower radius and arm length (in mm)
    printer = Delta3DPrinterBalance(tower_radius=150, arm_length=300)

    # Calculate arm heights for a specific XYZ coordinate
    x, y, z = 50, 50, 100
    arm_heights = printer.calculate_arm_heights(x, y, z)
    print(f"Arm heights for point ({x}, {y}, {z}):")
    print(f"A: {arm_heights[0]:.2f} mm")
    print(f"B: {arm_heights[1]:.2f} mm")
    print(f"C: {arm_heights[2]:.2f} mm")

    # Optimize print area
    max_height = 200  # mm
    best_radius, best_volume = printer.optimize_print_area(max_height)
    print(f"\nOptimal print radius: {best_radius} mm")
    print(f"Maximum print volume: {best_volume/1000000:.2f} liters")