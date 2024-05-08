import math
from helper import valid_number_plate


class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

        self.plates_map= {}


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h, veh_number = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            area = w*h

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 3000:
                    self.center_points[id] = (cx, cy)
                    # print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id, veh_number])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count, veh_number])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, w, h, object_id, veh_number = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center
            if(valid_number_plate(veh_number)):
                if object_id in self.plates_map:
                    # Key exists, append to the existing list
                    self.plates_map[object_id].append((w*h, veh_number))
                else:
                    # Key doesn't exist, create a new list with the value
                    self.plates_map[object_id] = [(w*h, veh_number)]
        
        ids_to_update = set(self.center_points.keys()) - set(new_center_points.keys())

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return  ids_to_update
