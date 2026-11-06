
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from map_visualizer import MapVisualizer


# ============================================================
# 1. Project directories
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "Material"

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Step 1: Project directories ready", flush=True)


# ============================================================
# 2. Locate raster data
# ============================================================

background_files = list(
    (DATA_DIR / "background").rglob(
        "raster-50k_2724246.tif"
    )
)

elevation_files = list(
    (DATA_DIR / "elevation").rglob("SZ.asc")
)

if not background_files:
    raise FileNotFoundError(
        "Background raster was not found."
    )

if not elevation_files:
    raise FileNotFoundError(
        "Elevation raster was not found."
    )

background_path = background_files[0]
elevation_path = elevation_files[0]

print("Background raster:", background_path, flush=True)
print("Elevation raster:", elevation_path, flush=True)
print("Step 2: Raster paths verified", flush=True)


# ============================================================
# 3. Mock coordinates for independent Task 5 testing
# ============================================================

# Task 1: Starting point
start = (439619, 85800)

# Task 6: Mock highest point
highest = (442000, 88000)

# Task 8: Mock route (not a real ITN-based route)
route = [
    (439619, 85800),
    (440000, 86000),
    (440500, 87000),
    (441000, 87500),
    (442000, 88000)
]

print("Step 3: Mock data prepared", flush=True)


# ============================================================
# 4. Create visualiser
# ============================================================

visualizer = MapVisualizer(
    background_path=background_path,
    elevation_path=elevation_path,
    map_size=20000
)

print("Step 4: MapVisualizer created", flush=True)


# ============================================================
# 5. Generate map
# ============================================================

print("Step 5: Generating map...", flush=True)

fig, ax = visualizer.plot_map(
    start=start,
    highest=highest,
    route=route
)

print("Step 6: Map generated successfully", flush=True)


# ============================================================
# 6. Save map
# ============================================================

output_path = OUTPUT_DIR / "task5_test_map.png"

print("Step 7: Saving PNG...", flush=True)

fig.savefig(
    output_path,
    dpi=150,
    bbox_inches="tight"
)

plt.close(fig)

if not output_path.is_file():
    raise RuntimeError("Output image was not created.")

print("Step 8: Map saved successfully!", flush=True)
print("Output:", output_path, flush=True)
print("File size:", output_path.stat().st_size, "bytes")

print("=" * 55)
print("CEGE0096 Task 5 test completed successfully!")
print("=" * 55)
