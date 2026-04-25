from utils.utils import direction_entity

class AxisPair:
    
    def __init__(
        self,
        dy: int = 0,
        dx: int = 0,
    ):
        self.dy = dy
        self.dx = dx
        
    def copy(self):
        return AxisPair(self.dy, self.dx)
    
class Cell:
    
    def __init__(
        self,
        offset: AxisPair,
        value: str | None = None,
    ):
        self.offset = offset
        self.value = value
        
    def copy(self):
        return Cell(self.offset.copy(), self.value)

class Item:
    
    def __init__(
        self,
        rows: list[list[Cell]] = [],
        direction: direction_entity = "",
        index: int = 0,
    ):
        self.rows = rows
        self.direction = direction
        self.previous_direction = direction
        self.index = index
        
    def set_direction(
        self,
        direction: direction_entity,
    ):
        self.previous_direction = self.direction
        self.direction = direction
        
    def copy(self):
        
        copy_rows: list[list[Cell]] = []
        
        for row in self.rows:
            
            copy_current_row: list[Cell] = []
            
            for cell in row:
                copy_current_row.append(cell.copy())
            
            if copy_current_row:
                copy_rows.append(copy_current_row)
                
        return Item(copy_rows, self.direction, self.index)

class Neighbor:
    def __init__(
        self,
        base: AxisPair,
        movement_range: AxisPair,
        step: AxisPair,
    ):
                
        dy_up = base.dy - step.dy
        dy_down = base.dy + step.dy
        
        dx_right = base.dx + step.dx
        dx_left = base.dx - step.dx
        
        self.upper = (dy_up if dy_up >= 0 else movement_range.dy - abs(base.dy - step.dy), base.dx)
        self.right = (base.dy, dx_right if dx_right <= (movement_range.dx - 1) else abs(movement_range.dx - base.dx - step.dx))
        self.below = (dy_down if dy_down <= (movement_range.dy - 1) else abs(movement_range.dy - base.dy - step.dy), base.dx)
        self.left = (base.dy, dx_left if dx_left >= 0 else movement_range.dx - abs(base.dx - step.dx))
        
        self.all = [
            self.upper,
            self.right,
            self.below,
            self.left
        ]
