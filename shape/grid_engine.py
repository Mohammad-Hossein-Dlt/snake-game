from shape.neighbor import Neighbor
from typing import Literal

class GridEngine:
    
    def __init__(
        self,
        grid: list[list[int]],

    ):  
        
        self.init_grid(grid)
    
    def init_grid(
        self,
        grid: list[list[int]],
    ):
        
        self.grid = grid

        self.grid_width = max(len(row) for row in self.grid)
        self.grid_height = len(self.grid)
        
        self.table = {
            (dy, dx): cell
            for dy, row in enumerate(self.grid)
                for dx, cell in enumerate(row)
        }
        
    def create_space(
        self,
        neighbor: Neighbor,
        width: int,
    ) -> list[int]:
        
        result: int = []
        
        if neighbor.right:
            if neighbor.left:
                result = [0 for _ in range(width - 2)]
            elif neighbor.left == 0:
                result = [0 for _ in range(width - 2)]
            elif neighbor.left is None:
                result = [0 for _ in range(width - 1)]
            
        elif neighbor.right == 0:
            if neighbor.left:
                result = [0 for _ in range(width - 1)]
            elif neighbor.left == 0:
                result = [0 for _ in range(width - 1)]
            elif neighbor.left is None:
                result = [0 for _ in range(width)]
        
        if neighbor.right is None:
            if neighbor.left:
                result = [0 for _ in range(width - 1)]
            elif neighbor.left == 0:
                result = [0 for _ in range(width - 1)]
            elif neighbor.left is None:
                result = [0 for _ in range(width)]
                
        return result
        
        
    def adapt(
        self,
        dy: int,
        dx: int,
        vaule: int,
        width: int,
        mode: Literal["top", "middle", "bottom"],
    ) -> list[int]:
        
        neighbor = Neighbor(dy, dx, self.table)
        
        result = []
        
        if mode == "top" or mode == "bottom":
            if vaule:
                if neighbor.right and neighbor.left:
                    result = [1 for _ in range(width - 1)]
                elif not neighbor.right and not neighbor.left:
                    result = [1 for _ in range(width)]
                elif neighbor.right:
                    result = [1 for _ in range(width)]
                elif neighbor.left:
                    result = [1 for _ in range(width - 1)]
            else:
                
                result = self.create_space(neighbor, width)
            
        if mode == "middle":
            if vaule:
                if neighbor.right and neighbor.left:
                    result = [0 for _ in range(width - 2)] + [1]
                elif neighbor.right:
                    result = [1] + [0 for _ in range(width - 2)] + [1]
                elif neighbor.left:
                    result = [0 for _ in range(width - 2)] + [1]
                elif not neighbor.right and not neighbor.left:
                    result = [1] + [0 for _ in range(width - 2)] + [1]
            else:
                
                result = self.create_space(neighbor, width)
        
        return result
        
    def convert(
        self,
        width: int,
        height: int,
    ) -> list[list[int]]:

        result: list[list[int]] = []
        
        for dy, row in enumerate(self.grid):
            
            top_row: list[int] = []
            for dx, cell in enumerate(row):
                top_row.extend(self.adapt(dy, dx, cell, width, "top"))
            result = self.merge(result, top_row)
            
            for _ in range(height - 2):
                middle_row: list[int] = []
                for dx, cell in enumerate(row):
                    middle_row.extend(self.adapt(dy, dx, cell, width, "middle"))
                result.append(middle_row)

            
            bottom_row: list[int] = []
            for dx, cell in enumerate(row):
                bottom_row.extend(self.adapt(dy, dx, cell, width, "bottom"))
            result.append(bottom_row)

        return result
    
    def merge(
        self,
        grid: list[list[int]],
        new_row: list[int],
    ) -> list[list[int]]:
        
        if not grid:
            grid: list[list[int]] = []
            grid.append(new_row)
            return grid
        
        if not any(new_row):
            grid.append(new_row)
            return grid
        
        for dx, cell in enumerate(grid[-1]):
            grid[-1][dx] = new_row[dx] or cell
                        
        return grid
        
    
    def rotate(
        self,
        direction: Literal["up", "right", "down", "left"]
    ) -> None:
        
        grid: list[list[str]] = [[0 for _ in range(self.grid_height)] for _ in range(self.grid_width)]
        
        dy_index = 0
        dx_index = 0
        
        dy_factor = 1
        dx_factor = 1
        
        if direction == "right":
            dy_factor = -1            
            dy_index = 1
        
        if direction == "left":
            dx_factor = -1        
            dx_index = 1
        
        for dy, row in enumerate(self.grid, dy_index):
            for dx, cell in enumerate(row, dx_index):
                grid[dx_factor*dx][dy_factor*dy] = cell
        
        self.init_grid(grid)
    