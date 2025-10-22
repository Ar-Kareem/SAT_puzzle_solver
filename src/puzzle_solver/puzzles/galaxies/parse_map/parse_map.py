"""
    This file is a simple helper that parses the images from https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/galaxies.html and converts them to a json file. 
    Look at the ./input_output/ directory for examples of input images and output json files.
    The output json is used in the test_solve.py file to test the solver.
"""
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
    output = {(dx, dy): arr.copy() for dx in [-1, 0, 1] for dy in [-1, 0, 1]}
    hists = {(dx, dy): {} for dx in [-1, 0, 1] for dy in [-1, 0, 1]}
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
            cell = cv.bitwise_not(cell)  # invert colors
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    mx = mid_x + dx*mid_x
                    my = mid_y + dy*mid_y
                    mx0 = max(0, mx - 5)
                    mx1 = min(cell.shape[1], mx + 5)
                    my0 = max(0, my - 5)
                    my1 = min(cell.shape[0], my + 5)
                    cell_part = cell[my0:my1, mx0:mx1]
                    hists[(dx, dy)][j, i] = np.sum(cell_part)
            # top = cell[0:10, mid_y-5:mid_y+5]
            # hists['top'][j, i] = np.sum(top)
            # left = cell[mid_x-5:mid_x+5, 0:10]
            # hists['left'][j, i] = np.sum(left)
            # right = cell[mid_x-5:mid_x+5, -10:]
            # hists['right'][j, i] = np.sum(right)
            # bottom = cell[-10:, mid_y-5:mid_y+5]
            # hists['bottom'][j, i] = np.sum(bottom)
            # print(f"cell_{i}_{j}, ", [hists[(dx, dy)][j, i] for dx in [-1, 0, 1] for dy in [-1, 0, 1]])
            # show_wait_destroy(f"cell_{i}_{j}", cell)

    fig, axs = plt.subplots(3, 3)
    target = 100
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            axs[dx+1, dy+1].hist(list(hists[(dx, dy)].values()), bins=100)
            axs[dx+1, dy+1].set_title(f'{dx},{dy}')
            # target = np.mean(list(hists[(dx, dy)].values()))
            axs[dx+1, dy+1].axvline(target, color='red')
    # plt.show()
    # 1/0
    for j in range(height - 1):
        for i in range(width - 1):
            sums_str = ''
            out_str = ''
            for dx in [-1, 0, 1]:
                out_xpart = 'L' if dx == -1 else 'C' if dx == 0 else 'R'
                for dy in [-1, 0, 1]:
                    out_ypart = 'T' if dy == -1 else 'C' if dy == 0 else 'B'
                    sums_str += str(hists[(dx, dy)][j, i]) + ' '
                    if hists[(dx, dy)][j, i] < target:
                        out_str += (out_xpart + out_ypart + ' ')
                        output[(dx, dy)][j, i] = 1
            print(f"cell_{j}_{i}", end=': ')
            print(out_str)
            print('   Sums: ', sums_str)

    out = np.full_like(output[(0, 0)], '  ', dtype='U2')
    counter = 0
    for j in range(out.shape[0]):
        for i in range(out.shape[1]):
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if output[(dx, dy)][j, i] == 1:
                        # out[j, i] = dxdy_to_char[(dx, dy)]
                        if dx == 0 and dy == 0:  # single point
                            out[j, i] = str(counter).zfill(2)
                            counter += 1
                        elif dx == 0 and dy == 1:  # vertical
                            out[j, i] = str(counter).zfill(2)
                            out[j+1, i] = str(counter).zfill(2)
                            counter += 1
                        elif dx == 1 and dy == 0:  # horizontal
                            out[j, i] = str(counter).zfill(2)
                            out[j, i+1] = str(counter).zfill(2)
                            counter += 1
                        elif dx == 1 and dy == 1:  # 2 by 2
                            out[j, i] = str(counter).zfill(2)
                            out[j+1, i] = str(counter).zfill(2)
                            out[j, i+1] = str(counter).zfill(2)
                            out[j+1, i+1] = str(counter).zfill(2)
                            counter += 1

    # print(out)
    with open(output_path, 'w') as f:
        f.write('[\n')
        for i, row in enumerate(out):
            f.write('  ' + str(row.tolist()).replace("'", '"'))
            if i != len(out) - 1:
                f.write(',')
            f.write('\n')
        f.write(']')
    print('output json: ', output_path)

if __name__ == '__main__':
    # to run this script and visualize the output, in the root run:
    #  python .\src\puzzle_solver\puzzles\galaxies\parse_map\parse_map.py | python .\src\puzzle_solver\utils\visualizer.py --read_stdin
    # main(Path(__file__).parent / 'input_output' / 'MTM6OSw4MjEsNDAx.png')
    # main(Path(__file__).parent / 'input_output' / 'weekly_oct_3rd_2025.png')
    # main(Path(__file__).parent / 'input_output' / 'star_battle_67f73ff90cd8cdb4b3e30f56f5261f4968f5dac940bc6.png')
    # main(Path(__file__).parent / 'input_output' / 'LITS_MDoxNzksNzY3.png')
    # main(Path(__file__).parent / 'input_output' / 'lits_OTo3LDMwNiwwMTU=.png')
    main(Path(__file__).parent / 'input_output' / 'eofodowmumgzzdkopzlpzkzaezrhefoezejvdtxrzmpgozzemxjdcigcqzrk.png')
