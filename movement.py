import heapq
import pyautogui
import numpy as np

# A* node class
class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y)
        self.parent = parent
        self.g = 0  # Cost from start node
        self.h = 0  # Heuristic cost to end node
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    """Calculate the Manhattan distance as the heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, obstacles, grid_size):
    """Find the path from start to goal avoiding obstacles."""
    open_list = []
    closed_list = set()
    start_node = Node(start)
    goal_node = Node(goal)

    # Initialize the open list with the start node
    heapq.heappush(open_list, start_node)

    # Possible movements (8 directions)
    movements = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),         (0, 1),
                 (1, -1),  (1, 0),  (1, 1)]

    while open_list:
        # Get the node with the lowest f value
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)

        # If we reach the goal, reconstruct the path
        if current_node.position == goal_node.position:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        # Generate children (neighbor nodes)
        children = []
        for move in movements:
            node_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

            # Check if the node is within grid bounds
            if 0 <= node_position[0] < grid_size[0] and 0 <= node_position[1] < grid_size[1]:
                # Check if the node is not an obstacle
                if obstacles[node_position[1], node_position[0]] == 0:
                    new_node = Node(node_position, current_node)
                    children.append(new_node)

        # Loop through children
        for child in children:
            if child.position in closed_list:
                continue

            # Calculate g, h, and f values
            child.g = current_node.g + 1
            child.h = heuristic(child.position, goal_node.position)
            child.f = child.g + child.h

            # Check if child is already in open_list and has a higher g cost
            in_open = False
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    in_open = True
                    break

            if not in_open:
                heapq.heappush(open_list, child)

    return None  # Return None if no path is found

def move_mouse_along_path(path):
    """Move the mouse along the calculated path using pyautogui."""
    for point in path:
        pyautogui.moveTo(point[0], point[1], duration=0.01)  # Move the mouse to the given point
        # print(f"Moving to {point}")  # Optional: print the movement

def process_bounding_boxes(bboxes):
    """Process YOLO format bounding boxes and return integer coordinates."""
    processed_boxes = []
    for bbox in bboxes:
        x_min, y_min, x_max, y_max = map(int, bbox)
        processed_boxes.append((x_min, y_min, x_max, y_max))
    return processed_boxes

# Example usage
if __name__ == '__main__':
    # Define the grid size (e.g., screen resolution)
    screen_width, screen_height = pyautogui.size()
    grid_size = (screen_width, screen_height)

    # Create an obstacle grid (2D numpy array)
    obstacle_grid = np.zeros((screen_height, screen_width), dtype=np.uint8)

    # Example target bounding boxes in YOLO format: [x_min, y_min, x_max, y_max]
    target_bboxes = [
        [100, 200, 150, 250],
        [300, 400, 350, 450],
        [600, 500, 650, 550],
        [800, 600, 850, 650]
    ]

    # Example obstacle bounding boxes in YOLO format
    obstacle_bboxes = [
        [150, 200, 200, 250],
        [350, 400, 400, 450],
        [650, 500, 700, 550]
    ]

    # Process bounding boxes to get integer coordinates
    target_bboxes = process_bounding_boxes(target_bboxes)
    obstacle_bboxes = process_bounding_boxes(obstacle_bboxes)

    # Mark obstacles on the grid
    for bbox in obstacle_bboxes:
        x_min, y_min, x_max, y_max = bbox
        obstacle_grid[y_min:y_max+1, x_min:x_max+1] = 1  # Mark obstacle area

    # Extract center points of target bounding boxes
    target_points = []
    for bbox in target_bboxes:
        x_min, y_min, x_max, y_max = bbox
        x_center = int((x_min + x_max) / 2)
        y_center = int((y_min + y_max) / 2)
        target_points.append((x_center, y_center))

    # Define the starting position for the mouse
    current_position = pyautogui.position()

    # Move to each target point using A* and avoid obstacles
    for target in target_points:
        path = a_star(current_position, target, obstacle_grid, grid_size)
        if path:
            move_mouse_along_path(path)
            current_position = target  # Update the current position
        else:
            print(f"No valid path to {target}")
