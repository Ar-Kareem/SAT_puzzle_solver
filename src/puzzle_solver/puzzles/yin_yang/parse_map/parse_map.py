
def extract_lines(bw):
    horizontal = np.copy(bw)
    vertical = np.copy(bw)

    cols = horizontal.shape[1]
    horizontal_size = max(5, cols // 20)
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    horizontal = cv2.erode(horizontal, h_kernel)
    horizontal = cv2.dilate(horizontal, h_kernel)
    h_means = np.mean(horizontal, axis=1)
    h_idx = np.where(h_means > np.percentile(h_means, 70))[0]

    rows = vertical.shape[0]
    verticalsize = max(5, rows // 20)
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
    vertical = cv2.erode(vertical, v_kernel)
    vertical = cv2.dilate(vertical, v_kernel)
    v_means = np.mean(vertical, axis=0)
    v_idx = np.where(v_means > np.percentile(v_means, 70))[0]
    return h_idx, v_idx


def _cluster_line_indices(indices, min_run=3):
    """Group consecutive indices into line positions (take the mean of each run)."""
    if len(indices) == 0:
        return []
    indices = np.sort(indices)
    runs = []
    run = [indices[0]]
    for k in indices[1:]:
        if k == run[-1] + 1:
            run.append(k)
        else:
            if len(run) >= min_run:
                runs.append(int(np.mean(run)))
            run = [k]
    if len(run) >= min_run:
        runs.append(int(np.mean(run)))
    # De-duplicate lines that are too close (rare)
    dedup = []
    for x in runs:
        if not dedup or x - dedup[-1] > 2:
            dedup.append(x)
    return dedup


def extract_yinyang_board(image_path, debug=False):
    # Load and pre-process
    img = cv2.imread(str(image_path))
    assert img is not None, f"Failed to read image: {image_path}"
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Light grid lines → enhance lines using adaptive threshold
    # (binary inverted so lines/dots become white)
    bw = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 35, 5
    )

    # Detect grid line indices (no guessing)
    h_idx, v_idx = extract_lines(bw)
    print(f"h_idx: {h_idx}")
    print(f"v_idx: {v_idx}")
    h_lines = h_idx
    v_lines = v_idx
    # h_lines = _cluster_line_indices(h_idx)
    # v_lines = _cluster_line_indices(v_idx)
    assert len(h_lines) >= 2 and len(v_lines) >= 2, "Could not detect grid lines"

    # Cells are spans between successive grid lines
    N_rows = len(h_lines) - 1
    N_cols = len(v_lines) - 1
    board = np.full((N_rows, N_cols), ' ', dtype='<U1')

    # For robust per-cell analysis, also create a "dots" image with grid erased
    # Remove thickened grid from bw
    # Build masks for horizontal/vertical lines (reusing kernels sized by image dims)
    cols = bw.shape[1]
    rows = bw.shape[0]
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (max(5, cols // 20), 1))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(5, rows // 20)))
    horiz = cv2.morphologyEx(bw, cv2.MORPH_OPEN, h_kernel)
    vert = cv2.morphologyEx(bw, cv2.MORPH_OPEN, v_kernel)
    grid = cv2.bitwise_or(horiz, vert)
    dots = cv2.bitwise_and(bw, cv2.bitwise_not(grid))  # mostly circles remain

    # Iterate cells
    print(f"N_rows: {N_rows}, N_cols: {N_cols}")
    print(f"h_lines: {h_lines}")
    print(f"v_lines: {v_lines}")
    for r in range(N_rows):
        y0, y1 = h_lines[r], h_lines[r + 1]
        # shrink ROI to avoid line bleed
        y0i = max(y0 + 2, 0)
        y1i = max(min(y1 - 2, dots.shape[0]), y0i + 1)
        for c in range(N_cols):
            x0, x1 = v_lines[c], v_lines[c + 1]
            x0i = max(x0 + 2, 0)
            x1i = max(min(x1 - 2, dots.shape[1]), x0i + 1)

            roi_gray = gray[y0i:y1i, x0i:x1i]
            roi_dots = dots[y0i:y1i, x0i:x1i]
            area = roi_dots.shape[0] * roi_dots.shape[1]
            if area == 0:
                continue

            # If no meaningful foreground, it's empty
            fg_area = int(np.count_nonzero(roi_dots))
            if fg_area < 0.03 * area:
                board[r, c] = ' '
                continue

            # Segment the largest blob (circle) inside the cell
            contours, _ = cv2.findContours(roi_dots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                board[r, c] = ' '
                continue

            cnt = max(contours, key=cv2.contourArea)
            if cv2.contourArea(cnt) < 0.02 * area:
                board[r, c] = ' '
                continue

            mask = np.zeros_like(roi_dots)
            cv2.drawContours(mask, [cnt], -1, 255, thickness=-1)

            mean_inside = float(cv2.mean(roi_gray, mask=mask)[0])

            # Heuristic: black stones have dark interior; white stones bright interior
            # (grid background is white; outlines contribute little to mean)
            board[r, c] = 'B' if mean_inside < 150 else 'W'
    non_empty_rows = []
    non_empty_cols = []
    for r in range(N_rows):
        if not all(board[r, :] == ' '):
            non_empty_rows.append(r)
    for c in range(N_cols):
        if not all(board[:, c] == ' '):
            non_empty_cols.append(c)
    board = board[non_empty_rows, :][:, non_empty_cols]

    if debug:
        for row in board:
            print(row.tolist())
    output_path = Path(__file__).parent / "input_output" / (image_path.stem + ".json")
    with open(output_path, 'w') as f:
        f.write('[\n')
        for i, row in enumerate(board):
            f.write('  ' + str(row.tolist()).replace("'", '"'))
            if i != len(board) - 1:
                f.write(',')
            f.write('\n')
        f.write(']')
    print('output json: ', output_path)

    return board

if __name__ == "__main__":
    #  python .\src\puzzle_solver\puzzles\yin_yang\parse_map\parse_map.py | python .\src\puzzle_solver\utils\visualizer.py --read_stdin
    import cv2
    import numpy as np
    from pathlib import Path
    image_path = Path(__file__).parent / "input_output" / "MzoyLDcwMSw2NTY=.png"
    # image_path = Path(__file__).parent / "input_output" / "Njo5MDcsNDk4.png"
    # image_path = Path(__file__).parent / "input_output" / "MTE6Niw0NjEsMTIx.png"
    assert image_path.exists(), f"Image file does not exist: {image_path}"
    board = extract_yinyang_board(image_path, debug=True)
    print(board)
