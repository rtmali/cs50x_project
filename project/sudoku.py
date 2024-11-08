import pygame
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500  # Adjusted height for 9x9 grid
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH / GRID_SIZE
FPS = 60

# Difficulty levels
DIFFICULTY_EASY = 36
DIFFICULTY_MEDIUM = 27
DIFFICULTY_HARD = 18

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_LIGHT_RED = (255, 200, 200)
COLOR_MENU_BACKGROUND = (240, 240, 240)

# Initialize Pygame
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SUDOKU")

# Key constants for easier reference
KEY_RESET = pygame.K_r
KEY_NEW = pygame.K_n
KEY_QUIT = pygame.K_q
KEY_CLEAR = pygame.K_c  # Key to clear inputs
KEY_MENU = pygame.K_ESCAPE  # Key to invoke submenu
KEY_EASY = pygame.K_1
KEY_MEDIUM = pygame.K_2
KEY_HARD = pygame.K_3

# Fonts
font_user_input = pygame.font.SysFont("arial", 25)
font_instructions = pygame.font.SysFont("arial", 20)
font_congratulations = pygame.font.SysFont("arial", 40)
font_menu = pygame.font.SysFont("arial", 30)

# Game state variables
sudoku_grid = [[(0, False) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
initial_sudoku_grid = []
x_coordinate, y_coordinate = 0, 0
user_input_value = ''
invalid_cells = []  # List to keep track of invalid cells
puzzle_solved = False
difficulty_level = DIFFICULTY_EASY  # Default difficulty

def get_coordinate(pos):
    """Get the grid coordinates from mouse position."""
    global x_coordinate, y_coordinate
    x_coordinate = int(pos[0] // CELL_SIZE)
    y_coordinate = int(pos[1] // CELL_SIZE)

def draw_selection_box():
    """Draw a selection box around the current cell."""
    for i in range(2):
        pygame.draw.line(screen, COLOR_RED, (x_coordinate * CELL_SIZE - 3, (y_coordinate + i) * CELL_SIZE),
                         (x_coordinate * CELL_SIZE + CELL_SIZE + 3, (y_coordinate + i) * CELL_SIZE), 7)
        pygame.draw.line(screen, COLOR_RED, ((x_coordinate + i) * CELL_SIZE, y_coordinate * CELL_SIZE),
                         ((x_coordinate + i) * CELL_SIZE, y_coordinate * CELL_SIZE + CELL_SIZE), 7)

def draw_sudoku_grid():
    """Draw the Sudoku grid and numbers, highlighting invalid cells."""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            num, is_initial = sudoku_grid[j][i]
            cell_color = COLOR_WHITE
            text_color = COLOR_BLACK  # Default text color

            if (j, i) in invalid_cells:
                cell_color = COLOR_LIGHT_RED  # Light red for invalid cells
                if num != 0:  # If there's an invalid input
                    text_color = (169, 169, 169)  # Grey color for invalid inputs

            pygame.draw.rect(screen, cell_color, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if num != 0:
                text_value = font_user_input.render(str(num), True, text_color)
                screen.blit(text_value, (i * CELL_SIZE + 15, j * CELL_SIZE + 15))

    for i in range(GRID_SIZE + 1):
        thick = 7 if i % 3 == 0 else 1
        pygame.draw.line(screen, COLOR_BLACK, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), thick)
        pygame.draw.line(screen, COLOR_BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_WIDTH), thick)

def is_valid_move(grid, i, j, val):
    """Check if a move is valid."""
    val = int(val)
    for it in range(GRID_SIZE):
        if grid[i][it][0] == val or grid[it][j][0] == val:
            return False
    subgrid_x, subgrid_y = 3 * (i // 3), 3 * (j // 3)
    for x in range(subgrid_x, subgrid_x + 3):
        for y in range(subgrid_y, subgrid_y + 3):
            if grid[x][y][0] == val:
                return False
    return True

def check_puzzle_solved(grid):
    """Check if the puzzle is solved."""
    for row in grid:
        if sorted(num for num, _ in row) != list(range(1, GRID_SIZE + 1)):
            return False
    for col in range(GRID_SIZE):
        if sorted(grid[row][col][0] for row in range(GRID_SIZE)) != list(range(1, GRID_SIZE + 1)):
            return False
    for x in range(0, GRID_SIZE, 3):
        for y in range(0, GRID_SIZE, 3):
            subgrid = [grid[y + i][x + j][0] for i in range(3) for j in range(3)]
            if sorted(subgrid) != list(range(1, GRID_SIZE + 1)):
                return False
    return True

def draw_submenu():
    """Draw the submenu for options."""
    screen.fill(COLOR_MENU_BACKGROUND)
    pygame.draw.rect(screen, COLOR_BLACK, (50, 110, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200), 5)

    # Define submenu options
    options = [
        "New Game",
        "Restart",
        "Back to Game",
        "Exit",
    ]

    FRAME_WIDTH = 300  # Set a fixed width for the frames

    # Draw red inner frames around the submenu options
    for index, option_text in enumerate(options):
        position_y = 150 + index * 60  # Adjust y position based on index
        text_surface = font_menu.render(option_text, True, COLOR_BLACK)
        text_width = text_surface.get_width()
        x_position = SCREEN_WIDTH // 2 - FRAME_WIDTH // 2  # Center the frame

        option_rect = pygame.Rect(x_position, position_y, FRAME_WIDTH, 50)  # Use fixed frame width
        pygame.draw.rect(screen, COLOR_RED, option_rect, 2)
        screen.blit(text_surface, (x_position + (FRAME_WIDTH - text_width) // 2, position_y + 10))  # Center text within frame

    pygame.display.update()

def generate_sudoku_puzzle():
    """Generate a random Sudoku puzzle based on difficulty."""
    global sudoku_grid, initial_sudoku_grid
    sudoku_grid = [[(0, False) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Randomly fill cells based on difficulty
    filled_cells = 0
    while filled_cells < difficulty_level:
        i, j = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        if is_valid_move(sudoku_grid, i, j, num):
            sudoku_grid[i][j] = (num, True)
            filled_cells += 1

    initial_sudoku_grid = [row[:] for row in sudoku_grid]

def reset_sudoku_puzzle():
    """Reset the Sudoku grid to its initial state."""
    global sudoku_grid, initial_sudoku_grid, puzzle_solved, invalid_cells
    sudoku_grid = [row[:] for row in initial_sudoku_grid]
    puzzle_solved = False
    invalid_cells = []  # Reset invalid cells

def clear_user_inputs():
    """Clear all user inputs on the Sudoku grid and reset invalid cells."""
    global sudoku_grid, invalid_cells
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            num, is_initial = sudoku_grid[i][j]
            if not is_initial:
                sudoku_grid[i][j] = (0, False)  # Reset user input to 0
    invalid_cells.clear()  # Clear the list of invalid cells

def clear_invalid_inputs():
    """Clear invalid user inputs from the Sudoku grid."""
    global sudoku_grid, invalid_cells
    for i, j in invalid_cells:
        sudoku_grid[i][j] = (0, False)  # Reset the user input to 0
    invalid_cells.clear()  # Clear the list of invalid cells

def display_difficulty_menu():
    """Display the difficulty menu for the game."""
    screen.fill(COLOR_WHITE)
    pygame.draw.rect(screen, COLOR_BLACK, (50, 110, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200), 5)

    # Define difficulty options
    options = [
        "Easy",
        "Medium",
        "Hard",
        "Exit",
    ]

    FRAME_WIDTH = 300  # Set a fixed width for the frames

    # Draw red inner frames around the difficulty options
    for index, option_text in enumerate(options):
        position_y = 150 + index * 60  # Adjust y position based on index
        text_surface = font_menu.render(option_text, True, COLOR_BLACK)
        text_width = text_surface.get_width()
        x_position = SCREEN_WIDTH // 2 - FRAME_WIDTH // 2  # Center the frame

        option_rect = pygame.Rect(x_position, position_y, FRAME_WIDTH, 50)  # Use fixed frame width
        pygame.draw.rect(screen, COLOR_RED, option_rect, 2)
        screen.blit(text_surface, (x_position + (FRAME_WIDTH - text_width) // 2, position_y + 10))  # Center text within frame

    pygame.display.update()

# Initialize the game
display_difficulty_menu()
run = True
menu_active = True
submenu_active = False

while run:
    if menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check for difficulty options
                if 150 <= pos[1] <= 200:  # Easy
                    difficulty_level = DIFFICULTY_EASY
                    generate_sudoku_puzzle()
                    menu_active = False
                elif 210 <= pos[1] <= 260:  # Medium
                    difficulty_level = DIFFICULTY_MEDIUM
                    generate_sudoku_puzzle()
                    menu_active = False
                elif 270 <= pos[1] <= 320:  # Hard
                    difficulty_level = DIFFICULTY_HARD
                    generate_sudoku_puzzle()
                    menu_active = False
                elif 330 <= pos[1] <= 380:  # Exit
                    run = False
    elif submenu_active:
        draw_submenu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check for submenu options
                if 150 <= pos[1] <= 200:  # New Game option
                    display_difficulty_menu()  # Go back to difficulty menu
                    menu_active = True  # Activate the menu
                    submenu_active = False
                elif 210 <= pos[1] <= 260:  # Restart option
                    clear_user_inputs()  # Clear user inputs
                    submenu_active = False
                elif 270 <= pos[1] <= 320:  # Back to Game option
                    submenu_active = False  # Close the submenu
                elif 330 <= pos[1] <= 380:  # Exit option
                    run = False
    else:
        screen.fill(COLOR_WHITE)
        draw_sudoku_grid()
        draw_selection_box()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_MENU:
                    submenu_active = True  # Activate the submenu
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                get_coordinate(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == KEY_RESET:
                    clear_user_inputs()  # Clear user inputs
                elif event.key == KEY_NEW:
                    clear_invalid_inputs()  # Clear invalid cells before starting a new game
                    generate_sudoku_puzzle()
                elif event.key == KEY_CLEAR:
                    if (y_coordinate, x_coordinate) in invalid_cells:
                        invalid_cells.remove((y_coordinate, x_coordinate))  # Remove from invalid list
                    sudoku_grid[y_coordinate][x_coordinate] = (0, False)  # Clear the selected cell input
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    user_input_value = str(event.key - pygame.K_0)  # Convert pygame key to string representation
                elif event.key == KEY_QUIT:
                    run = False
                elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    if event.key == pygame.K_UP:
                        y_coordinate = (y_coordinate - 1) % GRID_SIZE
                    elif event.key == pygame.K_DOWN:
                        y_coordinate = (y_coordinate + 1) % GRID_SIZE
                    elif event.key == pygame.K_LEFT:
                        x_coordinate = (x_coordinate - 1) % GRID_SIZE
                    elif event.key == pygame.K_RIGHT:
                        x_coordinate = (x_coordinate + 1) % GRID_SIZE

        if user_input_value:
            num, is_initial = sudoku_grid[y_coordinate][x_coordinate]
            if not is_initial:
                if is_valid_move(sudoku_grid, y_coordinate, x_coordinate, user_input_value):
                    sudoku_grid[y_coordinate][x_coordinate] = (int(user_input_value), False)
                    if check_puzzle_solved(sudoku_grid):
                        puzzle_solved = True
                else:
                    invalid_cells.append((y_coordinate, x_coordinate))  # Add invalid cell to list
                    sudoku_grid[y_coordinate][x_coordinate] = (int(user_input_value), False)  # Store user input
            user_input_value = ''

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

pygame.quit()

