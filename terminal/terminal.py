from typing import ClassVar, Callable

class Terminal:
    
    started: ClassVar[bool] = False
    
    hide_cursor = "\033[?25l"
    show_cursor = "\033[?25h"
    
    def manage(
        content: str,
        func: Callable[[str], str],
    ) -> str:
        if Terminal.started:
            return func(content)
        else:
            Terminal.started = True
            return content
    
    def move_cursor(
        n: int | None = None,
        content: str | None = None,
    ) -> str:
        if n is None and content is not None:
            n = len(content.split("\n"))
            
        return f"\033[{n}A\033[F\n"

    def clean_line(
        n: int,
    ) -> str:
        return "\033[K"
    
    def clean_lines():
        return "\033[J"
    
    def overwrite_line(
        n: int,
        content: str,
    ) -> str:
        return Terminal.manage(
            content,
            lambda cntnt: Terminal.move_cursor(n) + "\r" + cntnt + "\r",
        )

    def overwrite_content(
        content: str,
    ) -> str:
        return Terminal.manage(
            content,
            lambda cntnt: Terminal.move_cursor(content=cntnt) + Terminal.clean_lines() + cntnt,
        )

    def print_content(
        content: str,
    ) -> str:
        return Terminal.manage(
            content,
            lambda cntnt: Terminal.move_cursor(content=cntnt) + cntnt,
        )
        
    def clean_content(
        content: str,
    ) -> str:
        return Terminal.manage(
            content,
            lambda cntnt: Terminal.move_cursor(content=cntnt) + Terminal.clean_lines(),
        )


def test_terminal():
    
    import time
    
    print(Terminal.hide_cursor, end="")
    
    x = True
    
    while True:
        
        if x:
            print(Terminal.overwrite_content(" O" * 20))
            x = not x
        else:
            print(Terminal.overwrite_content(" X" * 10))
            x = not x
        
        time.sleep(1)
        
if __name__ == '__main__':
    test_terminal()

# def print_content(content: str):
#     sys.stdout.write(content)
#     sys.stdout.flush()

# def clean_content(
#     content: str,
# ):
#     length = len(content.split("\n"))
#     sys.stdout.write(f"\033[{length-1}A")