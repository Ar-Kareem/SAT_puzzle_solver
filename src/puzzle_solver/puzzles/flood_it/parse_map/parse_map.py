"""
    This file is a simple helper that parses the images from https://www.chiark.greenend.org.uk and converts them to a json file.
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
    horizontal_size = cols // 20
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
    horizontal = cv.erode(horizontal, horizontalStructure)
    horizontal = cv.dilate(horizontal, horizontalStructure)
    horizontal_means = np.mean(horizontal, axis=1)
    horizontal_cutoff = np.percentile(horizontal_means, 50)
    # location where the horizontal lines are
    horizontal_idx = np.where(horizontal_means > horizontal_cutoff)[0]
    # print(f"horizontal_idx: {horizontal_idx}")
    # height = len(horizontal_idx)
    # show_wait_destroy("horizontal", horizontal)  # this has the horizontal lines

    rows = vertical.shape[0]
    verticalsize = rows // 20
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, verticalsize))
    vertical = cv.erode(vertical, verticalStructure)
    vertical = cv.dilate(vertical, verticalStructure)
    vertical_means = np.mean(vertical, axis=0)
    vertical_cutoff = np.percentile(vertical_means, 50)
    vertical_idx = np.where(vertical_means > vertical_cutoff)[0]
    # print(f"vertical_idx: {vertical_idx}")
    # width = len(vertical_idx)
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
    median_vertical_dist = np.median(np.diff(vertical_idx))
    median_horizontal_dist = np.median(np.diff(horizontal_idx))
    print(f"median_vertical_dist: {median_vertical_dist}, median_horizontal_dist: {median_horizontal_dist}")
    height = len(horizontal_idx)
    width = len(vertical_idx)
    print(f"height: {height}, width: {width}")
    print(f"horizontal_idx: {horizontal_idx}")
    print(f"vertical_idx: {vertical_idx}")
    output_rgb = {}
    j_idx = 0
    for j in range(height - 1):
        i_idx = 0
        for i in range(width - 1):
            hidx1, hidx2 = horizontal_idx[j], horizontal_idx[j+1]
            vidx1, vidx2 = vertical_idx[i], vertical_idx[i+1]
            hidx1 = max(0, hidx1 - 2)
            hidx2 = min(src.shape[0], hidx2 + 4)
            vidx1 = max(0, vidx1 - 2)
            vidx2 = min(src.shape[1], vidx2 + 4)
            if (hidx2 - hidx1) < median_horizontal_dist * 0.5 or (vidx2 - vidx1) < median_vertical_dist * 0.5:
                continue
            cell = src[hidx1:hidx2, vidx1:vidx2]
            mid_x = cell.shape[1] // 2
            mid_y = cell.shape[0] // 2
            print(f"mid_x: {mid_x}, mid_y: {mid_y}")
            cell_50_percent = cell[int(mid_y*0.5):int(mid_y*1.5), int(mid_x*0.5):int(mid_x*1.5)]
            # show_wait_destroy(f"cell_{i_idx}_{j_idx}", cell_50_percent)
            output_rgb[j_idx, i_idx] = cell_50_percent.mean(axis=(0, 1))
            print(f"output_rgb[{j_idx}, {i_idx}]: {output_rgb[j_idx, i_idx]}")
            i_idx += 1
        j_idx += 1

    colors_to_cluster = cluster_colors(output_rgb)
    width = max(pos[1] for pos in output_rgb.keys()) + 1
    height = max(pos[0] for pos in output_rgb.keys()) + 1
    out = np.zeros((height, width), dtype=object)
    print(colors_to_cluster)
    for pos, cluster_id in colors_to_cluster.items():
        out[pos[0], pos[1]] = cluster_id
    print('Shape of out:', out.shape)

    with open(output_path, 'w') as f:
        f.write('[\n')
        for i, row in enumerate(out):
            f.write('  ' + str(row.tolist()).replace("'", '"'))
            if i != len(out) - 1:
                f.write(',')
            f.write('\n')
        f.write(']')
    print('output json: ', output_path)

def euclidean_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5

KNOWN_COLORS = {
    (0, 0, 255): 'Red',
    (0, 255, 0): 'Green',
    (255, 77, 51): 'Blue',
    (0, 255, 255): 'Yellow',
    (255, 153, 255): 'Pink',
    (0, 128, 255): 'Orange',
    (255, 204, 102): 'Cyan',
    (179, 255, 179): 'Washed Green',
    (77, 77, 128): 'Brown',
    (179, 0, 128): 'Purple',
}

def cluster_colors(rgb: dict[tuple[int, int], tuple[int, int, int]]) -> dict[tuple[int, int, int], int]:
    MIN_DIST = 10  # if distance between two colors is less than this, then they are the same color
    colors_to_cluster = KNOWN_COLORS.copy()
    for pos, color in rgb.items():
        color = tuple(color)
        if color in colors_to_cluster:
            continue
        for existing_color, existing_cluster_id in colors_to_cluster.items():
            if euclidean_distance(color, existing_color) < MIN_DIST:
                colors_to_cluster[color] = existing_cluster_id
                break
        else:
            new_name = str(', '.join(str(int(c)) for c in color))
            print('WARNING: new color found:', new_name, 'at pos:', pos)
            colors_to_cluster[color] = new_name
    pos_to_cluster = {pos: colors_to_cluster[tuple(color)] for pos, color in rgb.items()}
    return pos_to_cluster


if __name__ == '__main__':
    # to run this script and visualize the output, in the root run:
    #  python .\src\puzzle_solver\puzzles\flood_it\parse_map\parse_map.py | python .\src\puzzle_solver\utils\visualizer.py --read_stdin
    # main(Path(__file__).parent / 'input_output' / 'flood.html#12x12c10m5%23637467359431429.png')
    # main(Path(__file__).parent / 'input_output' / 'flood.html#12x12c6m5%23132018455881870.png')
    # main(Path(__file__).parent / 'input_output' / 'flood.html#12x12c6m0%23668276603006993.png')
    # main(Path(__file__).parent / 'input_output' / 'flood.html#20x20c8m0%23991967486182787.png')flood.html#20x20c4m0%23690338575695152
    main(Path(__file__).parent / 'input_output' / 'flood.html#20x20c4m0%23690338575695152.png')
