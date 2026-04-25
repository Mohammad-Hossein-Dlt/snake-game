from utils.utils import tag_text, Color, is_shape
from game.snake import Snake
import random

def colorize_grid(
    grid: list[list[str]],
) -> list[list[str]]:
    
    for dy, row in enumerate(grid):
        for dx, cell in enumerate(row):
            if not is_shape(cell):
                if cell == "·":
                    cell = tag_text(cell, Color.GRAY)
                elif cell == "★":
                    cell = tag_text(cell, Color.GOLD)
            
            grid[dy][dx] = cell

    return grid

def create_target(
    y_range: int,
    x_range: int,
    snake: Snake,
    target: tuple[int, int] | None = None,
    offset: int = 1,
):
    
    if not target:
        shape = snake.get_all_coordinates()
        while True:
            dy = random.randint(0, y_range - 1)
            dx = random.randint(0, x_range - 1)
            target = (dy, dx + (dx*offset))
            if target not in shape:
                break
        
    return target  

def setup_board(
    y_range: int,
    x_range: int,
    snake: Snake,
    target: tuple[int, int] | None = None,
    offset: int = 1,
) -> tuple[
    list[list[str]],
    tuple[int, int],
]:

    grid = [ [ "·" for _ in range(x_range) ] for _ in range(y_range)]
    grid = [ list((" "*offset).join(row)) for row in grid]
        
    for item_index, item in enumerate(snake.body):
        for row in item.rows:
            for cell in row:
                
                check_dy = 0 <= cell.offset.dy < y_range
                check_dx = 0 <= cell.offset.dx < x_range + (x_range * offset) - offset
                check_value = cell.value and is_shape(cell.value)
                
                if check_dy and check_dx and check_value:
                    
                    value = cell.value
                    if item_index == 0:
                        value = tag_text(value, Color.BLUE)
                    else:
                        value = tag_text(value, Color.GREEN)
                    
                    grid[cell.offset.dy][cell.offset.dx] = value
    
    target = create_target(y_range, x_range, snake, target, offset)
    grid[target[0]][target[1]] = "★"
    
    grid = colorize_grid(grid)
    
    return grid, target