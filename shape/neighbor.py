
class Neighbor:
    def __init__(
        self,
        dy: int,
        dx: int,
        table: dict[tuple[int, int], int],
    ):
        
        self.dy = dy
        self.dx = dx
        
        top = (dy-1, dx)        
        right = (dy, dx+1)
        bottom = (dy+1, dx)
        left = (dy, dx-1)
        
        self.top = table[top] if top in table else None
        self.bottom = table[bottom] if bottom in table else None
        self.right = table[right] if right in table else None
        self.left = table[left] if left in table else None
  