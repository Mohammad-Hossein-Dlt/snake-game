from core.core import AxisPair, Cell, Item, Neighbor
from shape.shape_engine import GridEngine, ShapeEngine
from utils.utils import direction_entity, is_shape


class Snake:
    
    def __init__(
        self,
        start_point: tuple[int, int],
        movement_range: tuple[int, int],
        shape: list[list[int]],
        offset: int = 1,
    ):
        self.start_point = (start_point[0], start_point[1] + (start_point[1]*offset))
        self.movement_range = (movement_range[0], movement_range[1] + (movement_range[1] * offset) - offset)
        
        grid_engine = GridEngine(shape)
        grid = grid_engine.convert(width=5, height=3)
        self.shape: ShapeEngine = ShapeEngine(grid)
        self.shape_lines = self.shape.create_shape()
                
        self.body: list[Item] = []
        self.append(self.start_point)
    
    def append(
        self,
        new_cell: tuple[int, int],
    ) -> list[list[list[tuple[int, int]]]]:
        
        new_item: Item = Item()
        
        for dy, row in enumerate(self.shape_lines):
            new_row: list[Cell] = []
            for dx, cell in enumerate(row, 1):
                relative = self.get_relative_coordinates(
                    (new_cell[0], new_cell[1]),
                    (dy, dx),
                )
                value = cell
                new_row.append(
                    Cell(
                        AxisPair(*relative),
                        value if is_shape(value) else None,
                    ),
                )
                
            new_item.rows.append(new_row)
                    
        self.body.append(new_item)
                
    def get_relative_coordinates(
        self,
        origin: tuple[int, int],
        offset: tuple[int, int],
    ) -> tuple[int, int]:
        
        origin_dy, origin_dx = origin
        offset_dy, offset_dx = offset
        
        central_dy = self.shape.central_dy
        central_dx = self.shape.central_dx
        
        dy = 0
        if offset_dy < central_dy:
            dy = origin_dy - (central_dy - offset_dy)
        elif offset_dy > central_dy:
            dy = origin_dy + (offset_dy - central_dy)
        elif offset_dy == central_dy:
            dy = origin_dy                    
        
        dx = 0
        if offset_dx < central_dx:
            dx = origin_dx - (central_dx - offset_dx)
        elif offset_dx > central_dx:
            dx = origin_dx + (offset_dx - central_dx)
        elif offset_dx == central_dx:
            dx = origin_dx
            
        return [dy, dx]
        
        
    def check_collide_self(
        self,
        other_item: Item,
    ) -> bool:
        
        for item in self.body:
            for dy, row in enumerate(item.rows):
                for dx, cell in enumerate(row):
                    
                    if item.index != other_item.index:
                        for other_dy, other_row in enumerate(other_item.rows):
                            for other_dx, other_cell in enumerate(other_row):
                                
                                check_dy = cell.offset.dy == other_cell.offset.dy
                                check_dx = cell.offset.dx == other_cell.offset.dx
                                check_both_is_shape = is_shape(self.shape_lines[dy][dx]) and is_shape(self.shape_lines[other_dy][other_dx])
                                
                                if check_dy and check_dx and check_both_is_shape:
                                    return True
                
        return False        
        
    def check_collide_target(
        self,
        item: Item,
        target: tuple[int, int],
    ) -> bool:
        
        for row in item.rows:
            
            first = next(cell for cell in row if cell.value)
            last = next(row[i] for i in reversed(range(len(row))) if row[i].value)
            
            if first.offset.dy == last.offset.dy == target[0]:
                
                # if target is in the middle of the grid row
                if first.offset.dx <= target[1] <= last.offset.dx:
                    return True

                # if target is in the end of the grid row
                elif last.offset.dx <= first.offset.dx <= target[1]:
                    return True

                # if target is in the start of the grid row
                elif target[1] <= last.offset.dx <= first.offset.dx:
                    return True

        return False
    
    def get_all_coordinates(
        self,
    ) -> list[tuple[int, int]]:
        
        coordinates = []
        
        for chunk in self.body:
            for row in chunk.rows:
                for cell in row:
                    coordinates.append((cell.offset.dy, cell.offset.dx))
                
        return coordinates
    
    def move_action(
        self,
        cell: Cell,
        direction: direction_entity,
    ) -> AxisPair:
        
        neighbor = Neighbor(
            base=AxisPair(cell.offset.dy, cell.offset.dx),
            movement_range=AxisPair(*self.movement_range),
            step=AxisPair(self.shape.shape_height, self.shape.shape_width),
        )
        
        if direction == "up":
            next_cell = neighbor.upper
            
        elif direction == "right":
            next_cell = neighbor.right
        
        elif direction == "down":
            next_cell = neighbor.below
        
        elif direction == "left":
            next_cell = neighbor.left
        
        else:
            next_cell = (cell.offset.dy, cell.offset.dx)
        
        return AxisPair(*next_cell)
    
    def move(
        self,
        direction: direction_entity,
        target: tuple[int, int] | None = None,
    ) -> tuple[tuple[int, int] | None, bool]:
        
        collide_target: Item = None
        collide_self: bool = False
        
        for index, item in enumerate(self.body):            
            
            previous_direction = self.find_previous_direction(item)
            
            if index == 0:
                item.set_direction(direction)   
            else:
                item.set_direction(previous_direction)
                
            for row in item.rows:
                for cell in row:
                    new_cell = self.move_action(cell, item.direction)
                    cell.offset.dy = new_cell.dy
                    cell.offset.dx = new_cell.dx
                    
            if not collide_self and self.check_collide_self(item):
                collide_self = True
                
            if target and self.check_collide_target(item, target):
                collide_target = item
                target = None
                        
        if collide_target:
            self.add()
                                
        return target, collide_self
    
    def find_previous_direction(
        self,
        item: Item,
    ) -> direction_entity:

        front: Item | None = None

        if item.index == 0:
            front = self.body[0]
        if item.index != 0:
            front = self.body[item.index-1]
            
        return front.previous_direction
    
    def add(
        self,
    ):
        
        last = self.body[-1]
        base = last.copy()
        
        direction = base.direction
            
        for row in base.rows:
            for cell in row:
                if direction == "up":
                    cell.offset.dy += self.shape.shape_height
                if direction == "down":
                    cell.offset.dy -= self.shape.shape_height
                if direction == "left":
                    cell.offset.dx += self.shape.shape_width
                if direction == "right":
                    cell.offset.dx -= self.shape.shape_width

        base.index += 1
        self.body.append(base)

    
if __name__ == '__main__':
    n = Neighbor(10, 10, 20, 20)
    print(n.all)
    
