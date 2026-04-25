from shape.neighbor import Neighbor
from shape.grid_engine import GridEngine
from shape.shape_examples import shapes
import math
  
class ShapeEngine:
    
    def __init__(
        self,
        grid: list[list[int]],
    ):  
        
        self.init_shape(grid)
        
    def init_shape(
        self,
        grid: list[list[int]],
    ) -> None:
        
        self.grid = grid
        
        self.shape_width = max(len(row) for row in self.grid)
        self.shape_height = len(self.grid)

        self.central_dy = math.floor(self.shape_height / 2)
        self.central_dx = math.ceil(self.shape_width / 2)
        
        self.table = {
            (dy, dx): cell
            for dy, row in enumerate(self.grid)
                for dx, cell in enumerate(row)
        }

    def adapt(
        self,
        dy: int,
        dx: int,
        vaule: int,
    ) -> str:
        
        neighbor = Neighbor(dy, dx, self.table)
        
        line = " "
        
        if not vaule:
            return " "
                
        if neighbor.top and neighbor.right and neighbor.bottom and neighbor.left:
            line = "┼"
        elif neighbor.top and neighbor.right and neighbor.bottom:
            line = "├"
        elif neighbor.top and neighbor.right and neighbor.left:
            line = "┴"
        elif neighbor.top and neighbor.bottom and neighbor.left:
            line = "┤"
        elif neighbor.right and neighbor.bottom and neighbor.left:
            line = "┬"
        elif neighbor.top and neighbor.right:
            line = "└"
        elif neighbor.top and neighbor.left:
            line = "┘"
        elif neighbor.right and neighbor.bottom:
            line = "┌"
        elif neighbor.bottom and neighbor.left:
            line = "┐"
        elif neighbor.top and neighbor.bottom:
            line = "│"
        elif neighbor.right and neighbor.left:
            line = "─"
        
        return line
            
    def create_shape(
        self,
        grid: list[list[int]] | None = None,
    ) -> list[list[str]]:
        
        if not grid:
            grid = self.grid
        
        shape: list[list[str]] = []
        
        for dy, row in enumerate(grid):
            row_c: list[str] = []
            for dx, cell in enumerate(row):
                row_c.append(self.adapt(dy, dx, cell))
            
            shape.append(row_c)

        return shape
        
if __name__ == "__main__":

    for index, shape in enumerate(shapes):
        
        grid_engine = GridEngine(shape)
        
        grid_engine.rotate("left")
        grid = grid_engine.convert(width=5, height=3)
        
        shape_engine = ShapeEngine(grid)
        shape_rows = shape_engine.create_shape()
            
        # for row in grid:
        #     print(row)
        
        for row in shape_rows:
            print("".join(row))
        
        if index < len(shapes) - 1:
            print("-"*100)