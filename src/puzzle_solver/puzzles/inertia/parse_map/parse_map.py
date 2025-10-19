"""
    This file is a simple helper that parses the images from https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html and converts them to a json file. 
    Look at the ./input_output/ directory for examples of input images and output json files.
    The output json is used in the test_solve.py file to test the solver.
"""
from pathlib import Path
import numpy as np
import numpy as np
cv = None
Image = None

def load_cell_templates(p: Path) -> dict[str, dict]:
    img = Image.open(p)
    src = cv.imread(p, cv.IMREAD_COLOR)
    rgb = np.asarray(img).astype(np.float32) / 255.0
    if len(src.shape) != 2:
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    else:
        gray = src
    gray = cv.bitwise_not(gray)
    bw = cv.adaptiveThreshold(gray.copy(), 255, cv.ADAPTIVE_THRESH_MEAN_C, \
                                cv.THRESH_BINARY, 15, -2)
    return {"gray": gray}



def _grad_mag(img: np.ndarray) -> np.ndarray:
    """Fast gradient magnitude (no dependencies)."""
    img = img.astype(np.float32)
    # forward diffs with clamped prepend to keep shape
    gx = np.diff(img, axis=1, prepend=img[:, :1])
    gy = np.diff(img, axis=0, prepend=img[:1, :])
    return np.hypot(gx, gy)

def get_distance_robust(cell: np.ndarray, template: np.ndarray, max_shift: int = 2, use_edges: bool = True) -> float:
    """
    Distance robust to small translations & brightness/contrast changes.
    - Compares gradient magnitude images (toggle with use_edges).
    - Z-score normalizes each overlap region.
    - Returns the minimum mean squared error across integer shifts
      in [-max_shift, max_shift] for both axes.
    """
    A = cell.astype(np.float32)
    B = template.astype(np.float32)

    if use_edges:
        A = _grad_mag(A)
        B = _grad_mag(B)

    H, W = A.shape
    best = np.inf

    for dy in range(-max_shift, max_shift + 1):
        for dx in range(-max_shift, max_shift + 1):
            # compute overlapping slices for this shift
            y0a = max(0,  dy); y1a = H + min(0,  dy)
            x0a = max(0,  dx); x1a = W + min(0,  dx)
            y0b = max(0, -dy); y1b = H + min(0, -dy)
            x0b = max(0, -dx); x1b = W + min(0, -dx)

            if y1a <= y0a or x1a <= x0a:  # no overlap
                continue

            Aa = A[y0a:y1a, x0a:x1a]
            Bb = B[y0b:y1b, x0b:x1b]

            # per-overlap z-score to remove brightness/contrast bias
            Aa = (Aa - Aa.mean()) / (Aa.std() + 1e-6)
            Bb = (Bb - Bb.mean()) / (Bb.std() + 1e-6)

            mse = np.mean((Aa - Bb) ** 2)
            if mse < best:
                best = mse
    return float(best)

def distance_to_cell_templates(cell_rgb_image, templates: dict[str, dict]) -> dict[str, float]:
    W, H = 100, 100
    cell = cv.resize(cell_rgb_image, (W, H), interpolation=cv.INTER_LINEAR)
    distances = {}
    for name, rec in templates.items():
        if rec["gray"].shape != (W, H):
            rec["gray"] = cv.resize(rec["gray"], (W, H), interpolation=cv.INTER_LINEAR)
        distances[name] = get_distance_robust(cell, rec["gray"])
    return distances

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

    return (width, height), (horizontal_idx, vertical_idx)

def show_wait_destroy(winname, img):
    cv.imshow(winname, img)
    cv.moveWindow(winname, 500, 0)
    cv.waitKey(0)
    cv.destroyWindow(winname)



def main(image):
    global Image
    global cv
    from PIL import Image as Image_module
    import cv2 as cv_module
    Image = Image_module
    cv = cv_module
    CELL_BLANK = load_cell_templates(Path(__file__).parent / 'cells' / 'cell_blank.png')
    CELL_WALL = load_cell_templates(Path(__file__).parent / 'cells' / 'cell_wall.png')
    CELL_GEM = load_cell_templates(Path(__file__).parent / 'cells' / 'cell_gem.png')
    CELL_MINE = load_cell_templates(Path(__file__).parent / 'cells' / 'cell_mine.png')
    CELL_STOP = load_cell_templates(Path(__file__).parent / 'cells' / 'cell_stop.png')
    CELL_START = load_cell_templates(Path(__file__).parent / 'cells' / 'cell_start.png')
    TEMPLATES = {
        "blank": CELL_BLANK,
        "gem": CELL_GEM,
        "mine": CELL_MINE,
        "stop": CELL_STOP,
        "start": CELL_START,
        "wall": CELL_WALL,
    }


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
    (width, height), (horizontal_idx, vertical_idx) = extract_lines(bw)
    print(f"width: {width}, height: {height}")
    print(f"horizontal_idx: {horizontal_idx}")
    print(f"vertical_idx: {vertical_idx}")
    output = np.zeros((height - 1, width - 1), dtype=object)
    output_map = {'blank': ' ', 'gem': 'G', 'mine': 'M', 'stop': 'O', 'start': 'B', 'wall': 'W'}
    for j in range(height - 1):
        for i in range(width - 1):
            hidx1, hidx2 = horizontal_idx[j], horizontal_idx[j+1]
            vidx1, vidx2 = vertical_idx[i], vertical_idx[i+1]
            cell = gray[hidx1:hidx2, vidx1:vidx2]
            # show_wait_destroy(f"cell_{i}_{j}", cell)
            distances = distance_to_cell_templates(cell, TEMPLATES)
            # print(f"distances: {distances}")
            best_match = min(distances, key=distances.get)
            # print(f"best_match: {best_match}")
            # cv.imwrite(f"i_{i}_j_{j}.png", cell)
            output[j, i] = output_map[best_match]

    with open(output_path, 'w') as f:
        f.write('[\n')
        for i, row in enumerate(output):
            f.write('  ' + str(row.tolist()).replace("'", '"'))
            if i != len(output) - 1:
                f.write(',')
            f.write('\n')
        f.write(']')

if __name__ == '__main__':
    main(Path(__file__).parent / 'input_output' / 'inertia.html#15x12%23919933974949365.png')
    main(Path(__file__).parent / 'input_output' / 'inertia.html#15x12%23518193627142459.png')
    main(Path(__file__).parent / 'input_output' / 'inertia.html#20x16%23200992952951435.png')
