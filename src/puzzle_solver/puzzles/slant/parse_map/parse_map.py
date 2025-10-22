"""
    This file is a simple helper that parses the images from https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html and converts them to a json file. 
    Look at the ./input_output/ directory for examples of input images and output json files.
    The output json is used in the test_solve.py file to test the solver.
"""

import json, itertools
from pathlib import Path
import numpy as np
cv = None


def extract_lines(bw):
    horizontal = np.copy(bw)
    vertical = np.copy(bw)

    cols = horizontal.shape[1]
    horizontal_size = max(5, cols // 20)
    h_kernel = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
    horizontal = cv.erode(horizontal, h_kernel)
    horizontal = cv.dilate(horizontal, h_kernel)
    h_means = np.mean(horizontal, axis=1)
    h_idx = np.where(h_means > np.percentile(h_means, 70))[0]

    rows = vertical.shape[0]
    verticalsize = max(5, rows // 20)
    v_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, verticalsize))
    vertical = cv.erode(vertical, v_kernel)
    vertical = cv.dilate(vertical, v_kernel)
    v_means = np.mean(vertical, axis=0)
    v_idx = np.where(v_means > np.percentile(v_means, 70))[0]
    return h_idx, v_idx

def mean_consecutives(arr):
    if len(arr) == 0:
        return arr
    sums, counts = [arr[0]], [1]
    for k in arr[1:]:
        if k == sums[-1] + counts[-1]:
            sums[-1] += k; counts[-1] += 1
        else:
            sums.append(k); counts.append(1)
    return np.array(sums)//np.array(counts)

def main(img_path):
    global cv
    import cv2 as cv_module
    cv = cv_module
    image_path = Path(img_path)
    output_path = image_path.parent / (image_path.stem + '.json')
    src = cv.imread(img_path, cv.IMREAD_COLOR)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    inv = cv.bitwise_not(gray)
    bw = cv.adaptiveThreshold(inv, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 15, -2)
    h_idx, v_idx = extract_lines(bw)
    h_idx = mean_consecutives(h_idx)
    v_idx = mean_consecutives(v_idx)

    # Estimate grid cell and circle radii
    cell = int(np.median(np.diff(h_idx))) if len(h_idx) > 3 else 40
    r_min = max(6, int(cell*0.18))
    r_max = int(cell*0.52)

    # Global Hough detection with parameter sweep
    blur = cv.medianBlur(gray, 5)
    detected = []  # x, y, r

    for dp, p2 in itertools.product([1.2, 1.0], [20, 18, 16, 14, 12]):
        circles = cv.HoughCircles(
            blur, cv.HOUGH_GRADIENT, dp=dp, minDist=max(12, int(cell*0.75)),
            param1=120, param2=p2, minRadius=r_min, maxRadius=r_max
        )
        if circles is not None:
            for (x, y, r) in np.round(circles[0, :]).astype(int):
                detected.append((x, y, r))

    # Non-maximum suppression to remove duplicates
    def nms(circles, dist_thr=10):
        kept = []
        for x,y,r in sorted(circles, key=lambda c: -c[2]):
            if all((x-kx)**2+(y-ky)**2 > dist_thr**2 for kx,ky,kr in kept):
                kept.append((x,y,r))
        return kept

    detected = nms(detected, dist_thr=max(10,int(cell*0.4)))

    # Map circle centers to nearest intersection
    H, W = len(h_idx), len(v_idx)
    presence = np.zeros((H, W), dtype=int)

    # Build KD-like search by grid proximity
    tol = int(cell*0.5)  # max distance from an intersection to accept a circle
    for (cx, cy, r) in detected:
        # find nearest indices
        j = int(np.argmin(np.abs(h_idx - cy)))
        i = int(np.argmin(np.abs(v_idx - cx)))
        if abs(h_idx[j]-cy) <= tol and abs(v_idx[i]-cx) <= tol:
            presence[j, i] = 1

    with open(output_path, 'w') as f:
        f.write('[\n')
        for i, row in enumerate(presence):
            f.write('  ' + str(row.tolist()).replace("'", '"'))
            if i != len(presence) - 1:
                f.write(',')
            f.write('\n')
        f.write(']')
    print('output json: ', output_path)
    print('output json: ', output_path)
    print('output json: ', output_path)

    overlay = src.copy()
    for (cx, cy, r) in detected:
        cv.circle(overlay, (cx, cy), r, (255,0,0), 2)
    for j, y in enumerate(h_idx):
        for i, x in enumerate(v_idx):
            color = (0,0,255) if presence[j,i]==1 else (0,255,0)
            cv.circle(overlay, (int(x), int(y)), 4, color, 2)
    show_wait_destroy("overlay", overlay)



def show_wait_destroy(winname, img):
    cv.imshow(winname, img)
    cv.moveWindow(winname, 500, 0)
    cv.waitKey(0)
    cv.destroyWindow(winname)


if __name__ == '__main__':
    # to run this script and visualize the output, in the root run:
    #  python .\src\puzzle_solver\puzzles\slant\parse_map\parse_map.py | python .\src\puzzle_solver\utils\visualizer.py --read_stdin
    main(Path(__file__).parent / 'input_output' / '23131379850022376.png')
