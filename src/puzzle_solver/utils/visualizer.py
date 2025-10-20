from __future__ import annotations
import argparse
from typing import Any, Mapping, Tuple
import json
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

RGB = Tuple[int, int, int]

def render_board_image(
    board: np.ndarray,
    colors: Mapping[Any, RGB],
    cell_size: int = 64,
    grid: bool = True,
    bg_default: RGB = (240, 240, 240),
    text_color: RGB = (0, 0, 0),
    padding: int = 20,
    ) -> None:
    """
    Render a 2D numpy array as a colored grid image with centered text labels.

    Args:
        board: 2D numpy array (dtype can be object/str/int/etc.). Each cell's value
               is looked up in `colors` for its fill color.
        colors: Dict-like mapping from cell values to RGB tuples (0-255).
        cell_size: Square side length (pixels) for each cell.
        grid: Whether to draw grid lines around cells.
        bg_default: Fill color when a cell's value is not in `colors`.
        text_color: Color for text labels.
        padding: Extra pixels around the entire grid on each side.
    """
    if board.ndim != 2:
        raise ValueError("`board` must be a 2D numpy array.")

    rows, cols = board.shape
    width  = cols * cell_size + padding * 2
    height = rows * cell_size + padding * 2

    img = Image.new("RGB", (width, height), color=bg_default)
    draw = ImageDraw.Draw(img)

    # font size
    desired_pt = max(10, int(cell_size * 0.4))
    font = ImageFont.truetype("DejaVuSans.ttf", desired_pt)

    missing_values = set()
    for r in range(rows):
        for c in range(cols):
            val = board[r, c]
            if isinstance(val, np.generic):
                val = val.item()
            if val not in colors:
                print(f'missing value: {val} of type {type(val)} at position {r}, {c}')
                missing_values.add(val)
            fill = colors.get(val, bg_default)

            x0 = padding + c * cell_size
            y0 = padding + r * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            draw.rectangle([x0, y0, x1, y1], fill=fill)

            if grid:
                draw.rectangle([x0, y0, x1, y1], outline=(0, 0, 0), width=1)

            # Center the text
            text = "" if val is None else str(val)
            if text:
                # textbbox gives more accurate sizing than textsize
                bbox = draw.textbbox((0, 0), text, font=font)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
                tx = x0 + (cell_size - tw) / 2
                ty = y0 + (cell_size - th) / 2
                draw.text((tx, ty), text, fill=text_color, font=font)

    img.show()





def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('--read_stdin', action='store_true')
    args = parser.parse_args()
    if args.read_stdin:
        # read from stdin until the line starts with "output json: "
        print('reading board from stdin until the line starts with "output json: "')
        json_path = None
        while True:
            line = sys.stdin.readline()
            if line.startswith('output json: '):
                json_path = line.split('output json: ')[1].strip()
                break
        with open(json_path, 'r') as f:
            board = np.array(json.load(f))
        print(f'read board from {json_path}')
    else:
        # with open('src/puzzle_solver/puzzles/stitches/parse_map/input_output/MTM6OSw4MjEsNDAx.json', 'r') as f:
        #     board = np.array(json.load(f))
        board = np.array([
            ['01', '123', '01', '01', '02', '02', '02', '03', '03', '03', '03', '04', '05', '05', '05'],
            ['01', '02', '02', '02', '02', '06', '07', '07', '03', '08', '03', '04', '04', '05', '09'],
            ['01', '01', '02', '11', '06', '06', '06', '12', '12', '08', '13', '13', '13', '09', '09'],
            ['01', '11', '11', '11', '14', '06', '06', '12', '12', '15', '15', '13', '09', '09', '09'],
            ['01', '01', '11', '11', '14', '12', '12', '12', '16', '16', '15', '13', '13', '17', '09'],
            ['01', '11', '11', '14', '14', '12', '42', '42', '42', '15', '15', '13', '13', '17', '18'],
            ['01', '11', '11', '14', '14', '12', '12', '43', '15', '15', '20', '13', '13', '17', '18'],
            ['01', '01', '11', '19', '19', '19', '43', '43', '44', '20', '20', '20', '13', '17', '18'],
            ['01', '22', '23', '23', '23', '19', '43', '21', '21', '24', '24', '24', '25', '17', '17'],
            ['22', '22', '22', '23', '19', '19', '26', '24', '24', '24', '28', '28', '25', '17', '33'],
            ['22', '22', '23', '23', '27', '27', '26', '26', '24', '24', '29', '29', '25', '25', '33'],
            ['22', '22', '35', '27', '27', '26', '26', '26', '26', '30', '30', '30', '25', '34', '34'],
            ['37', '22', '35', '35', '35', '35', '35', '26', '26', '30', '31', '31', '32', '32', '40'],
            ['37', '37', '37', '36', '36', '35', '26', '26', '26', '40', '40', '40', '40', '40', '40'],
            ['37', '37', '37', '37', '35', '35', '38', '38', '39', '39', '40', '40', '40', '41', '41'],
        ])
    return board

if __name__ == '__main__':
    board = get_input()
    # rcolors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255), (128, 128, 128)]
    vs =[0, 128, 255]
    rcolors = [(v1, v2, v3) for v1 in vs for v2 in vs for v3 in vs if (v1, v2, v3) != (0, 0, 0)]
    nums = set([c.item() for c in np.nditer(board)])
    colors = {c: rcolors[i % len(rcolors)] for i, c in enumerate(nums)}
    print(nums)
    print('max i:', max(nums))
    print('skipped:', set(range(int(max(nums)) + 1)) - set(int(i) for i in nums))
    render_board_image(board, colors)