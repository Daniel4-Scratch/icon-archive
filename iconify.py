import os
import glob
import math
import subprocess

# Configuration
ICON_DIR = "./icons"
ICON_SIZE = 16
SPRITE_NAME = "sprite.png"
CSS_NAME = "sprite.css"

# Get all .png files
icons = sorted(glob.glob(os.path.join(ICON_DIR, "*.png")))
total_icons = len(icons)
if total_icons == 0:
    raise SystemExit("❌ No PNG files found in ./icons/")

# Calculate closest square grid
cols = rows = math.ceil(math.sqrt(total_icons))
sprite_width = cols * ICON_SIZE
sprite_height = rows * ICON_SIZE

print(f"📦 Found {total_icons} icons. Grid: {cols} x {rows}")

# Step 1: Generate sprite sheet using ImageMagick
print("🧱 Building sprite sheet with ImageMagick...")
cmd = [
    "magick", "montage",
    "-tile", f"{cols}x{rows}",
    "-geometry", "+0+0",
    "-background", "none",
    *icons,
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

for i, path in enumerate(icons):
    name = os.path.splitext(os.path.basename(path))[0]
    x = (i % cols) * ICON_SIZE
    y = (i // cols) * ICON_SIZE
    css.append(f".sprite.{name} {{ background-position: -{x}px -{y}px; }}")

with open(CSS_NAME, "w") as f:
    f.write("\n".join(css))

print(f"✅ Done! Generated {SPRITE_NAME} and {CSS_NAME}")
