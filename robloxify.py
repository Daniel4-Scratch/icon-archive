import sys
import re
import os

if len(sys.argv) < 2:
    print("Usage: python robloxify.py <file.css>")
    print("Example: python robloxify.py library/fugue16/sprite.css")
    sys.exit(1)

filename = sys.argv[1]

# Handle relative paths - if the file doesn't exist as-is, try looking in library/
if not os.path.exists(filename):
    # If it starts with /, remove it and try in library/
    if filename.startswith('/'):
        filename = filename.lstrip('/')
        filename = os.path.join('library', filename)
    elif not filename.startswith('library/'):
        filename = os.path.join('library', filename)

if not os.path.exists(filename):
    print(f"Error: File '{sys.argv[1]}' not found.")
    print("Available CSS files:")
    for root, dirs, files in os.walk('library'):
        for file in files:
            if file.endswith('.css'):
                print(f"  {os.path.join(root, file)}")
    sys.exit(1)

with open(filename, "r", encoding="utf-8") as f:
    css = f.read()

lua_table = {}

pattern = re.compile(r"\.sprite\.([a-zA-Z0-9\-_]+)\s*\{\s*background-position:\s*(-?\d+)px\s*(-?\d+)px;")

for match in pattern.finditer(css):
    name = match.group(1).replace("-", "_")
    x = abs(int(match.group(2)))
    y = abs(int(match.group(3)))
    lua_table[name] = f"Vector2.new({x}, {y})"

output = f"local icons = {{\n"
for name, value in lua_table.items():
    output += f"    {name} = {value},\n"
output += "}\n\n"
output += "return icons"
output_filename = filename.replace('.css', '.luau')
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(output)
