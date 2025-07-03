import os
import glob
import math
import subprocess
import sys
from PIL import Image

# Configuration
ICON_DIR = sys.argv[1] if len(sys.argv) > 1 else "./icons"
ICON_SIZE = sys.argv[2] if len(sys.argv) > 2 else 16
SPRITE_NAME = "sprite.png"
CSS_NAME = "sprite.css"

# Get all .png files
all_icons = sorted(glob.glob(os.path.join(ICON_DIR, "*.png")))
valid_icons = []
invalid_icons = []

# Validate image sizes
print("🔍 Validating icon sizes...")
for path in all_icons:
    try:
        with Image.open(path) as img:
            if img.size == (ICON_SIZE, ICON_SIZE):
                valid_icons.append(path)
            else:
                invalid_icons.append(path)
    except Exception as e:
        invalid_icons.append(path)

total_icons = len(valid_icons)
if total_icons == 0:
    raise SystemExit("❌ No valid icons with correct size found.")

# Report skipped files
if invalid_icons:
    print(f"⚠️ Skipped {len(invalid_icons)} invalid icons (not {ICON_SIZE}x{ICON_SIZE}):")
    for path in invalid_icons:
        print("   -", os.path.basename(path))

# Calculate closest square grid
cols = rows = math.ceil(math.sqrt(total_icons))
sprite_width = cols * ICON_SIZE
sprite_height = rows * ICON_SIZE

print(f"📦 Using {total_icons} icons. Grid: {cols} x {rows}")

# Step 1: Generate sprite sheet
print("🧱 Building sprite sheet with ImageMagick...")
cmd = [
    "magick", "montage",
    "-tile", f"{cols}x{rows}",
    "-geometry", "+0+0",
    "-background", "none",
    *valid_icons,
    SPRITE_NAME
]
subprocess.run(cmd, check=True)

# Step 2: Generate CSS
print("🧾 Generating CSS...")
css = [
    f""".sprite {{
    background: url('{SPRITE_NAME}') no-repeat;
    width: {ICON_SIZE}px;
    height: {ICON_SIZE}px;
    display: inline-block;
    background-size: {sprite_width}px {sprite_height}px;
}}"""
]

for i, path in enumerate(valid_icons):
    name = os.path.splitext(os.path.basename(path))[0]
    x = (i % cols) * ICON_SIZE
    y = (i // cols) * ICON_SIZE
    css.append(f".sprite.{name} {{ background-position: -{x}px -{y}px; }}")

with open(CSS_NAME, "w") as f:
    f.write("\n".join(css))

print(f"✅ Done! Generated {SPRITE_NAME} and {CSS_NAME}")
# run robloxify.py to convert the CSS to Lua
if os.path.exists("robloxify.py"):
    print("🔄 Running robloxify.py to convert CSS to Lua...")
    subprocess.run(["python", "robloxify.py", CSS_NAME], check=True)
else:
    print("⚠️ Warning: robloxify.py not found. Skipping Lua conversion.")
# End of script
