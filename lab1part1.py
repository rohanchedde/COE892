import requests
import time

# Constants
MAP_FILE = 'map1.txt'
API_URL = 'https://coe892.reev.dev/lab1/rover/'  # Replace with the actual URL
MINE = 1  # Mine is represented by 1 in the grid
PATH = '*'  # Symbol for the robot's path

# Function to read the map from the file
def read_map(file_path):
    with open(file_path, 'r') as file:
        dimensions = file.readline().strip()
        rows, cols = map(int, dimensions.split())
        grid = []
        for _ in range(rows):
            line = file.readline().strip()
            if line:  # Ensure the line is not empty
                grid.append(list(map(int, line.split())))
    return grid, rows, cols

# Function to fetch moves from the API
def fetch_moves(rover_id):
    response = requests.get(f'{API_URL}/{rover_id}')
    json_data = response.json()
    return json_data['data']['moves']

# Function to simulate the robot's movements
def simulate_robot(rover_id, grid, rows, cols, moves):
    position = (0, 0)
    x, y = position
    direction = 's'

    for move in moves:
        if grid[x][y] == MINE:
            print(f"Rover {rover_id} hit a mine at ({x}, {y})! Stopping further commands.")
            break  # Stop executing further commands

        if move == 'M':
            new_x, new_y = move_robot(x, y, direction, rows, cols)
            if (new_x, new_y) != (x, y):  # Check if the move was valid
                x, y = new_x, new_y
                grid[x][y] = PATH  # Mark the new position
        elif move in ['R', 'L']:
            direction = turn(direction, move)
        elif move == 'D':
            pass  # Dig command (ignored for now)

    print(f"Rover {rover_id} final grid:")
    for row in grid:
        print(" ".join(str(cell) if cell != PATH else PATH for cell in row))

# Function for turning
def turn(direction, move):
    if move == 'R':
        if direction == 'n':
            return 'e'
        elif direction == 'e':
            return 's'
        elif direction == 's':
            return 'w'
        elif direction == 'w':
            return 'n'
    elif move == 'L':
        if direction == 'n':
            return 'w'
        elif direction == 'w':
            return 's'
        elif direction == 's':
            return 'e'
        elif direction == 'e':
            return 'n'
    return direction

# Function for moving
def move_robot(x, y, direction, rows, cols):
    if direction == 'n':
        new_x, new_y = x - 1, y
    elif direction == 's':
        new_x, new_y = x + 1, y
    elif direction == 'e':
        new_x, new_y = x, y + 1
    elif direction == 'w':
        new_x, new_y = x, y - 1
    else:
        new_x, new_y = x, y
    if 0 <= new_x < rows and 0 <= new_y < cols:
        return new_x, new_y
    else:
        return x, y

# Main function
def main():
    # Read the map
    grid, rows, cols = read_map(MAP_FILE)

    # Fetch moves for multiple rovers (example: 3 rovers)
    rover_ids = [1, 2, 3]  # Example rover IDs
    moves_list = [fetch_moves(rover_id) for rover_id in rover_ids]

    # Start timing
    start_time = time.time()

    # Simulate each rover sequentially
    for i, moves in enumerate(moves_list):
        # Create a copy of the grid for each rover
        rover_grid = [row[:] for row in grid]
        simulate_robot(rover_ids[i], rover_grid, rows, cols, moves)

    # End timing
    end_time = time.time()
    print(f"Total processing time (sequential): {end_time - start_time:.4f} seconds")

# Run the program
if __name__ == "__main__":
    main()