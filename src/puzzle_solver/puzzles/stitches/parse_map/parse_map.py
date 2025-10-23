"""
    This file is a simple helper that parses the images from https://www.puzzle-stitches.com/ and converts them to a json file. 
    Look at the ./input_output/ directory for examples of input images and output json files.
    The output json is used in the test_solve.py file to test the solver.
"""
# import json
from pathlib import Path
import numpy as np
cv = None
Image = None


def extract_lines(bw):
    # Create the images that will use to extract the horizontal and vertical lines
    horizontal = np.copy(bw)
    vertical = np.copy(bw)

    cols = horizontal.shape[1]
    horizontal_size = cols // 5
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
    horizontal = cv.erode(horizontal, horizontalStructure)
    horizontal = cv.dilate(horizontal, horizontalStructure)
    horizontal_means = np.mean(horizontal, axis=1)
    horizontal_cutoff = np.percentile(horizontal_means, 50)
    # location where the horizontal lines are
    horizontal_idx = np.where(horizontal_means > horizontal_cutoff)[0]
    # print(f"horizontal_idx: {horizontal_idx}")
    height = len(horizontal_idx)
    # show_wait_destroy("horizontal", horizontal)  # this has the horizontal lines

    rows = vertical.shape[0]
    verticalsize = rows // 5
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, verticalsize))
    vertical = cv.erode(vertical, verticalStructure)
    vertical = cv.dilate(vertical, verticalStructure)
    vertical_means = np.mean(vertical, axis=0)
    vertical_cutoff = np.percentile(vertical_means, 50)
    vertical_idx = np.where(vertical_means > vertical_cutoff)[0]
    # print(f"vertical_idx: {vertical_idx}")
    width = len(vertical_idx)
    # print(f"height: {height}, width: {width}")
    # print(f"vertical_means: {vertical_means}")
    # show_wait_destroy("vertical", vertical)  # this has the vertical lines

    vertical = cv.bitwise_not(vertical)
    # show_wait_destroy("vertical_bit", vertical)

    return horizontal_idx, vertical_idx

def show_wait_destroy(winname, img):
    cv.imshow(winname, img)
    cv.moveWindow(winname, 500, 0)
    cv.waitKey(0)
    cv.destroyWindow(winname)


def mean_consecutives(arr: np.ndarray) -> np.ndarray:
    """if a sequence of values is consecutive, then average the values"""
    sums = []
    counts = []
    for i in range(len(arr)):
        if i == 0:
            sums.append(arr[i])
            counts.append(1)
        elif arr[i] == arr[i-1] + 1:
            sums[-1] += arr[i]
            counts[-1] += 1
        else:
            sums.append(arr[i])
            counts.append(1)
    return np.array(sums) // np.array(counts)

def dfs(x, y, out, output, current_num):
    # if current_num == '48':
    #     print('dfs', x, y, current_num)
    if x < 0 or x >= out.shape[1] or y < 0 or y >= out.shape[0]:
        return
    if out[y, x] != '  ':
        return
    out[y, x] = current_num
    if output['top'][y, x] == 0:
        dfs(x, y-1, out, output, current_num)
    if output['left'][y, x] == 0:
        dfs(x-1, y, out, output, current_num)
    if output['right'][y, x] == 0:
        dfs(x+1, y, out, output, current_num)
    if output['bottom'][y, x] == 0:
        dfs(x, y+1, out, output, current_num)

def main(image):
    global Image
    global cv
    import matplotlib.pyplot as plt
    from PIL import Image as Image_module
    import cv2 as cv_module
    Image = Image_module
    cv = cv_module


    image_path = Path(image)
    output_path = image_path.parent / (image_path.stem + '.json')
    src = cv.imread(image, cv.IMREAD_COLOR)
    assert src is not None, f'Error opening image: {image}'
    if len(src.shape) != 2:
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    else:
        gray = src
    # now the image is in grayscale

    # Apply adaptiveThreshold at the bitwise_not of gray, notice the ~ symbol
    gray = cv.bitwise_not(gray)
    bw = cv.adaptiveThreshold(gray.copy(), 255, cv.ADAPTIVE_THRESH_MEAN_C, \
                                cv.THRESH_BINARY, 15, -2)
    # show_wait_destroy("binary", bw)

    # show_wait_destroy("src", src)
    horizontal_idx, vertical_idx = extract_lines(bw)
    horizontal_idx = mean_consecutives(horizontal_idx)
    vertical_idx = mean_consecutives(vertical_idx)
    height = len(horizontal_idx)
    width = len(vertical_idx)
    print(f"height: {height}, width: {width}")
    print(f"horizontal_idx: {horizontal_idx}")
    print(f"vertical_idx: {vertical_idx}")
    arr = np.zeros((height - 1, width - 1), dtype=object)
    output = {'top': arr.copy(), 'left': arr.copy(), 'right': arr.copy(), 'bottom': arr.copy()}
    target = 200_000
    hists = {'top': {}, 'left': {}, 'right': {}, 'bottom': {}}
    for j in range(height - 1):
        for i in range(width - 1):
            hidx1, hidx2 = horizontal_idx[j], horizontal_idx[j+1]
            vidx1, vidx2 = vertical_idx[i], vertical_idx[i+1]
            hidx1 = max(0, hidx1 - 2)
            hidx2 = min(src.shape[0], hidx2 + 4)
            vidx1 = max(0, vidx1 - 2)
            vidx2 = min(src.shape[1], vidx2 + 4)
            cell = src[hidx1:hidx2, vidx1:vidx2]
            mid_x = cell.shape[1] // 2
            mid_y = cell.shape[0] // 2
            # if j > height - 4 and i > width - 6:
            #     show_wait_destroy(f"cell_{i}_{j}", cell)
            # show_wait_destroy(f"cell_{i}_{j}", cell)
            cell = cv.bitwise_not(cell)  # invert colors
            top = cell[0:10, mid_y-5:mid_y+5]
            hists['top'][j, i] = np.sum(top)
            left = cell[mid_x-5:mid_x+5, 0:10]
            hists['left'][j, i] = np.sum(left)
            right = cell[mid_x-5:mid_x+5, -10:]
            hists['right'][j, i] = np.sum(right)
            bottom = cell[-10:, mid_y-5:mid_y+5]
            hists['bottom'][j, i] = np.sum(bottom)

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].hist(list(hists['top'].values()), bins=100)
    axs[0, 0].set_title('Top')
    axs[0, 1].hist(list(hists['left'].values()), bins=100)
    axs[0, 1].set_title('Left')
    axs[1, 0].hist(list(hists['right'].values()), bins=100)
    axs[1, 0].set_title('Right')
    axs[1, 1].hist(list(hists['bottom'].values()), bins=100)
    axs[1, 1].set_title('Bottom')
    global_target = None
    # global_target = 28_000
    target_top = np.mean(list(hists['top'].values()))
    target_left = np.mean(list(hists['left'].values()))
    target_right = np.mean(list(hists['right'].values()))
    target_bottom = np.mean(list(hists['bottom'].values()))
    if global_target is not None:
        target_top = global_target
        target_left = global_target
        target_right = global_target
        target_bottom = global_target

    axs[0, 0].axvline(target_top, color='red')
    axs[0, 1].axvline(target_left, color='red')
    axs[1, 0].axvline(target_right, color='red')
    axs[1, 1].axvline(target_bottom, color='red')
    # plt.show()
    # 1/0
    print(f"target_top: {target_top}, target_left: {target_left}, target_right: {target_right}, target_bottom: {target_bottom}")
    for j in range(height - 1):
        for i in range(width - 1):
            if hists['top'][j, i] > target_top:
                output['top'][j, i] = 1
            if hists['left'][j, i] > target_left:
                output['left'][j, i] = 1
            if hists['right'][j, i] > target_right:
                output['right'][j, i] = 1
            if hists['bottom'][j, i] > target_bottom:
                output['bottom'][j, i] = 1
            print(f"cell_{j}_{i}", end=': ')
            print('T' if output['top'][j, i] else '', end='')
            print('L' if output['left'][j, i] else '', end='')
            print('R' if output['right'][j, i] else '', end='')
            print('B' if output['bottom'][j, i] else '', end='')
            print('   Sums: ', hists['top'][j, i], hists['left'][j, i], hists['right'][j, i], hists['bottom'][j, i])

    current_count = 0
    z_fill = 2
    out = np.full_like(output['top'], '  ', dtype='U32')
    for j in range(out.shape[0]):
        if current_count > 99:
            z_fill = 3
        for i in range(out.shape[1]):
            if out[j, i] == '  ':
                if current_count == 48:
                    print(f"current_count: {current_count}, x: {i}, y: {j}")
                dfs(i, j, out, output, str(current_count).zfill(z_fill))
                current_count += 1
    print(out)

    with open(output_path, 'w') as f:
        f.write('[\n')
        for i, row in enumerate(out):
            f.write('  ' + str(row.tolist()).replace("'", '"'))
            if i != len(out) - 1:
                f.write(',')
            f.write('\n')
        f.write(']')
    print('output json: ', output_path)

    # with open(output_path.parent / 'debug.json', 'w') as f:
    #     debug_pos = {}
    #     for j in range(out.shape[0]):
    #         for i in range(out.shape[1]):
    #             out_str = ''
    #             out_str += 'T' if output['top'][j, i] else ''
    #             out_str += 'L' if output['left'][j, i] else ''
    #             out_str += 'R' if output['right'][j, i] else ''
    #             out_str += 'B' if output['bottom'][j, i] else ''
    #             debug_pos[f'{j}_{i}'] = out_str
    #     json.dump(debug_pos, f, indent=2)

if __name__ == '__main__':
    # to run this script and visualize the output, in the root run:
    #  python .\src\puzzle_solver\puzzles\stitches\parse_map\parse_map.py | python .\src\puzzle_solver\utils\visualizer.py --read_stdin
    # main(Path(__file__).parent / 'input_output' / 'MTM6OSw4MjEsNDAx.png')
    # main(Path(__file__).parent / 'input_output' / 'weekly_oct_3rd_2025.png')
    # main(Path(__file__).parent / 'input_output' / 'star_battle_67f73ff90cd8cdb4b3e30f56f5261f4968f5dac940bc6.png')
    # main(Path(__file__).parent / 'input_output' / 'LITS_MDoxNzksNzY3.png')
    # main(Path(__file__).parent / 'input_output' / 'lits_OTo3LDMwNiwwMTU=.png')
    # main(Path(__file__).parent / 'input_output' / 'norinori_501d93110d6b4b818c268378973afbf268f96cfa8d7b4.png')
    main(Path(__file__).parent / 'input_output' / 'norinori_OTo0LDc0Miw5MTU.png')
