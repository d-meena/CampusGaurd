import math
from helper import valid_number_plate

class IdTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

    def getId(self, cx, cy, thrld_dis):
        for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < thrld_dis:
                      return id

        self.id_count += 1
        return self.id_count - 1
