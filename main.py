import queue
from multiprocessing import Process, Queue
from core.board import setup_board
from get_input.get_input import get_direction
from core.show import Color, show
from game.snake import Snake, direction_entity
from terminal.terminal import Terminal

speed: float = 0.5
scale: tuple[int, int] = (20, 30)
offset: int = 3

def run_game():
        
    start_point: tuple[int, int] =(
        # random.randint(0, scale[0] - 1),
        # random.randint(0, scale[1] - 1),
        10 , 10
    )

    shape = [
        
        [1],
        
        # [1, 1, 1, 1],
        # [1, 0, 0, 1],
        # [1, 0, 0, 1],
        # [1, 1, 1, 1],
        
        # [1, 1, 0],
        # [0, 1, 1],
    
        # [1, 0, 1],
        # [1, 1, 1],
        # [0, 1, 0],    
        
        # [1, 0, 0, 1],
        # [1, 1, 1, 1],
        # [0, 1, 1, 0],
        
        # [1, 0, 1],
        # [1, 1, 1],
        # [1, 1, 1],
        # [0, 1, 0],    

        # [1, 0, 0, 1],
        # [1, 1, 1, 1],
        # [1, 1, 1, 1],
        # [0, 1, 1, 0],    

    ]

    snake = Snake(start_point=start_point, movement_range=scale, shape=shape, offset=offset)

    target: tuple[int, int] = None
    
    grid, target = setup_board(*scale, snake=snake, target=target, offset=offset)
    
    queue_data = Queue()
    
    get_key_process = Process(target=get_direction, args=(queue_data,), daemon=True)
    get_key_process.start()
    
    direction: direction_entity = "right"
    
    print(Terminal.hide_cursor, end="")
    
    while True:
        
        grid, target = setup_board(*scale, snake=snake, target=target, offset=offset)
        content = show(scale, grid, f"Score: {len(snake.body) - 1}", Color.GREEN, offset=offset)
        
        print(Terminal.overwrite_content(content))
        
        try:
            direction = queue_data.get(timeout=speed)
        except queue.Empty:
            pass
        
        target, collide = snake.move(direction, target)
                
        if not direction:
            content = show(scale, grid, f"Game closed", Color.TURQUOISE, offset=offset)
            print(Terminal.overwrite_content(content))
            queue_data.close()
            get_key_process.terminate()
            get_key_process.join()
            break
                
        if collide:
            content = show(scale, grid, "You lose", Color.RED, offset=offset)
            print(Terminal.overwrite_content(content))
            queue_data.close()
            get_key_process.terminate()
            get_key_process.join()
            break                 
        
def test_rich():

    from rich.console import Console
    from rich.syntax import Syntax
    from rich.panel import Panel
    
    console = Console()
    
    python = """
    def hello_world():
        print("Hello, World!")
    """
    
    java = """
    void main():
        system.out.printls("Hello, World!");
    """

    syntax = Syntax(python, "python", theme="monokai", line_numbers=True)
    console.print(syntax)    
    console.print("Tui", style="yellow bold underline")
    

    console.print(Panel("Text in the panel", title="title", subtitle="subtitle"))

if __name__ == '__main__':
    run_game()
    # test_rich()
   
 
'''

      0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29     
   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐   
 0 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 0 
 1 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 1 
 2 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 2 
 3 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 3 
 4 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 4 
 5 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 5 
 6 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 6 
 7 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 7 
 8 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 8 
 9 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ┌───┐   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 9 
10 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   │   │   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 10
11 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   └───┘   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 11
12 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 12
13 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 13
14 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 14
15 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 15
16 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 16
17 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 17
18 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 18
19 │  ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·   ·  │ 19
   └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘   
      0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29     
                                                                                                                                 
                                                                                                                                 
   Game closed                                                                                                                   
                                                                                                                                 
                                                                                                                                 
'''