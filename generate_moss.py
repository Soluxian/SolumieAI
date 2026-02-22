import random
from PIL import Image, ImageDraw
from math import sin, pi

random.seed(42)

width, height = 1280, 720

# Create image
img = Image.new('RGB', (width, height))

# Base gradient: dark green at bottom to lighter at top
draw = ImageDraw.Draw(img)
for y in range(height):
    factor = y / height
    r = int(5 + 15 * factor)
    g = int(30 + 90 * factor)
    b = int(5 + 15 * factor)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Moss patches: clustered ellipses
def draw_moss_patch(draw, cx, cy, size, color_offset):
    for _ in range(random.randint(5,15)):
        x = cx + random.randint(-size, size)
        y = cy + random.randint(-size//2, size//2)
        if x >= 0 and x < width and y >= 0 and y < height:
            w = random.randint(1, size//2 + 2)
            h = random.randint(1, size//3 + 1)
            gr = int(40 + random.randint(0,40) + color_offset)
            gg = int(70 + random.randint(20,60) + color_offset)
            gb = int(30 + random.randint(0,30) + color_offset)
            draw.ellipse([x-w, y-h, x+w, y + h*2], fill=(gr, gg, gb))

num_patches = 300
for _ in range(num_patches):
    cx = random.randint(0, width)
    cy = random.randint(height//2, height)
    size = random.randint(10, 40)
    offset = random.randint(-10,20)
    draw_moss_patch(draw, cx, cy, size, offset)

# Vines
def draw_vine(draw, x1, y1, x2, y2, thickness_var=3):
    steps = random.randint(15, 30)
    points = [(x1, y1)]
    for i in range(1, steps):
        t = i / steps
        dx = (x2 - x1) * t
        dy = (y2 - y1) * t
        sway_x = 40 * sin(t * pi * 3 + random.random() * pi) * (1 - t)
        sway_y = 20 * sin(t * pi * 2 + random.random() * pi) * (1 - t)
        points.append((x1 + dx + sway_x, y1 + dy + sway_y))
    points.append((x2, y2))
    width_v = random.randint(1, thickness_var)
    draw.line(points, fill=(15, 45, 20), width=width_v)

for _ in range(15):
    x1 = random.randint(0, width // 3)
    y1 = random.randint(3*height//4, height)
    x2 = x1 + random.randint(300, 800)
    y2 = y1 - random.randint(150, 400)
    if x2 > width:
        x2 = width - random.randint(10,50)
    draw_vine(draw, x1, y1, x2, y2)

# Dew drops with simple glow
for _ in range(150):
    x = random.randint(50, width-50)
    y = random.randint(100, height-50)
    size = random.randint(2,5)
    # Outer glow
    draw.ellipse([x-size*2, y-size*2, x+size*3, y+size*3], fill=(230,250,220))
    # Drop
    draw.ellipse([x-size, y-size//2, x+size, y+size*1.5], fill=(210, 240, 200))
    # Highlight
    draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], fill=(255,255,240))

# Save main
img.save('moss-bg.png', optimize=True)

# Thumbnail 256x144 (16:9)
thumb = img.resize((256, 144), Image.Resampling.LANCZOS)
thumb.save('moss-bg-thumb.png', optimize=True)

print("Generated moss-bg.png (1280x720) and moss-bg-thumb.png (256x144)")
