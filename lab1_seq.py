import requests
import time  # Import the time module


# Read the map from the file
file = open('map1.txt', 'r')
dimensions = file.readline().strip()
rows, cols = map(int, dimensions.split())

# Read the rest of the file to get the grid
grid = []
for _ in range(rows):
    line = file.readline().strip()
    if line:  # Ensure the line is not empty
        grid.append(list(map(int, line.split())))

# URL of the Rover
url = 'https://coe892.reev.dev/lab1/rover/1'  # Rover URL

# Send a GET request to the website
response = requests.get(url)

# Parse the JSON data
json_data = response.json()

# Extract the "moves" value from the nested structure
moves = json_data['data']['moves']

# Initial Variables
position = (0, 0)
x, y = position
direction = 's'
mine = 1  # Mine is represented by 1 in the grid
path = '*'  # Symbol for the robot's path
grid[x][y] = path

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
def move_robot(x, y, direction):
    if direction == 'n':
        new_x, new_y = x - 1, y
    elif direction == 's':
        new_x, new_y = x + 1, y
    elif direction == 'e':
        new_x, new_y = x, y + 1
    elif direction == 'w':
        new_x, new_y = x, y - 1
    if 0 <= new_x < rows and 0 <= new_y < cols:
        return new_x, new_y
    else:
        return x, y

# Simulate the robot's movements
for i, move in enumerate(moves):
    # Check if the next move is dig
    next_move_is_dig = i + 1 < len(moves) and moves[i + 1] != 'D'
    
    if move == 'M':
        print(x, y)
        new_x, new_y = move_robot(x, y, direction)
        if (new_x, new_y) != (x, y):  # Check if the move was valid
            x, y = new_x, new_y

            if grid[x][y] == mine and next_move_is_dig:
                print("Robot hit a mine at ({}, {})! Stopping further commands.".format(x, y))
                grid[x][y] = path
                break
            grid[x][y] = path

    elif move in ['R', 'L']:
        direction = turn(direction, move)

    elif move == 'D':
        grid[x][y] = path
        

# Print the grid
for row in grid:
    print(" ".join(str(cell) if cell != path else path for cell in row))