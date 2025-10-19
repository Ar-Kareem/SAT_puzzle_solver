import coverage
import time
import sys
from pathlib import Path

# Add src directory to path so imports work when running tests directly
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


cov = coverage.Coverage(
    source=["puzzle_solver"],
    branch=True
)
cov.start()

tic = time.time()
import puzzle_solver
# import numpy as np
# from ortools.sat.python import cp_model
toc = time.time()
print(f"Time taken: {toc - tic} seconds")

cov.stop()
cov.save()
cov.report()                        # text report
cov.html_report(directory="htmlcov")



data = cov.get_data()
prefixes = ("#", "def ", "from ", "import ")
results = []
import_results = []

for filename in sorted(data.measured_files()):
    executed = data.lines(filename) or []
    if not executed:
        continue

    try:
        text = Path(filename).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = Path(filename).read_text(encoding="utf-8", errors="ignore")

    lines = text.splitlines()
    for ln in sorted(executed):
        if 1 <= ln <= len(lines):
            s = lines[ln - 1].lstrip()
            if s and not s.startswith(prefixes):
                results.append((filename, ln, s))
            if 'import ' in s:
                import_results.append((filename, ln, s))

for fname, ln, code in results:
    print(f"{fname}:{ln}: {code}")

for fname, ln, code in import_results:
    print(f"{fname}:{ln}: {code}")

out = Path("import_covered_lines.txt")
out.write_text("\n".join(f"{f}:{n}: {c}" for f, n, c in results) + '\n\n' + "\n".join(f"{f}:{n}: {c}" for f, n, c in import_results), encoding="utf-8")
print(f"\nWrote filtered list to {out}")