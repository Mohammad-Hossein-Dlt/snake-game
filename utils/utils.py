from typing import TypeAlias, Literal
from enum import Enum
import re

direction_entity: TypeAlias = Literal["up", "right", "down", "left"]

chars = [
    "╯",
    "╰",
    "╮",
    "╭",
    # 
    "┘",
    "└",
    "┐",
    "┌",
    # 
    "─",
    "│",
    # 
    "┴",
    "┬",
    # 
    "├",
    "┤",
    # 
    "┼",
]

def is_shape(shape: str) -> bool:
    for i in chars:
        if i in shape:
            return True

class Color(str, Enum):
    BLACK = "1;30"
    RED = "1;31"
    GREEN = "1;32"
    YELLOW = "1;33"
    BLUE = "1;34"
    PURPLE = "1;35"
    TURQUOISE = "1;36"
    WHITE = "1;37"
    GOLD = "38;2;255;215;0"
    GRAY = "90"

def tag_text(
    text: str,
    color: Color,
):
    text = text
    text_lines = text.splitlines()
    
    tagged_text = ""
    for line in text_lines:
        tagged_text += f"<{color.name}>" + line + f"</{color.name}>"
        tagged_text += "\n"    
    
    return tagged_text.strip()

def remove_tag(
    tagged_text: str,
    with_tag_name: bool = False,
) -> tuple[str, str] | str:
        
    tag_name, content = "", ""
    
    pattern = r"<(\w+)>(.*?)</\1>"
    matches = re.findall(pattern, tagged_text)
    if matches:
        for index, (t_name, cntnt) in enumerate(matches):
            tag_name = t_name
            content += cntnt + ("\n" if index != len(matches) - 1 else "") 
    
    tag_name = tag_name.strip()
    content = content or tagged_text
        
    return [content, tag_name] if with_tag_name else content

def colorize_text(
    text: str,
    code: Color | None = None,
    tag: str | None = None,
):
    color_code = ""
    
    if code:
        color_code = code.value
    elif tag:
        try:
            color_code = Color[tag].value
        except Exception:
            color_code = Color.WHITE.value
    
    return f"\033[{color_code}m" + text + "\033[0m" if color_code else text
