from typing import Literal
from utils.utils import Color, remove_tag, colorize_text

divider_char = "│"
vertical_divider_margin = 1
vertical_divider_padding = 2

# Vertical dividers
left_divider = (" " * vertical_divider_margin) + divider_char
right_divider = divider_char + (" " * vertical_divider_margin)

def create_horizontal_divider(
    margin: str,
    length: int,
    position: Literal["top", "bottom"],
) -> str:
    """Create horizontal top/bottom dividers."""
    if position == "top":
        return margin + "┌" + ("─" * length) + "┐"
    if position == "bottom":
        return margin + "└" + ("─" * length) + "┘"

def create_horizontal_indicator(
    index: int,
    padding_size: int,
    position: Literal["left", "right"],
) -> str:
    if position == "left":
        return str(index).rjust(padding_size) + left_divider + (" " * vertical_divider_padding)
    if position == "right":
        return (" " * vertical_divider_padding) + right_divider + str(index).ljust(padding_size)

def create_vertical_indicator(
    offset: int,
    dx_range: int,
) -> list:
    indicator = []
    for i in range(dx_range):
        
        if i == 0:
            indicator.extend(" " for _ in range(vertical_divider_padding + 1))
        
        indicator.append(str(i))
        
        if i < 10:
            indicator.extend(" " for _ in range(offset))
        else:
            if i == dx_range - 1:
                ...
            else:
                indicator.extend(" " for _ in range(offset - 1))
    
    return indicator

def show(
    scale: tuple[int, int],
    data: list[list[str]],
    footer: str,
    footer_color: Color,
    offset: int = 1,
) -> str:
    """
    Render a table-like structure with row/column indicators and dividers.
    """
    # ─── Configurations ────────────────────────────────────────────────
    y_range, x_range = scale
    
    y_max_digits = len(str(y_range))
    
    margin = " " * (y_max_digits + vertical_divider_margin)
    
    # ─── Build Content ────────────────────────────────────────────────
    content = "\n"
                
    for row_index, row in enumerate(data):
                     
        row_list: list[str] = []
                
        for val in row:
            text, tag_name = remove_tag(tagged_text=val, with_tag_name=True)
            row_list.append(colorize_text(text, tag=tag_name))
                
        content += (
            create_horizontal_indicator(row_index, y_max_digits, "left")
            + "".join(row_list)
            + create_horizontal_indicator(row_index, y_max_digits, "right")
            + "\n"
        )
        
    # ─── Axis Indicators ─────────────────────────────────────────────
    x_indicator = create_vertical_indicator(offset, x_range)
    horizontal_indicator = margin + "".join(x_indicator)

    top_horizontal_divider = create_horizontal_divider(
        margin,
        len("".join(x_indicator)),
        "top",
    )
    bottom_horizontal_divider = create_horizontal_divider(
        margin,
        len("".join(x_indicator)),
        "bottom",
    )

    # ─── Final Assembly ──────────────────────────────────────────────
    content = (
        "\n"
        + horizontal_indicator
        + "\n"
        + top_horizontal_divider
        + content
        + bottom_horizontal_divider
        + "\n"
        + horizontal_indicator
        + "\n"
    )
    
    if footer:
        
        content += (
            "\n\n"
            + margin
            + colorize_text(footer, code=footer_color)
            + "\n"
        )
                
    return content + "\n"