import json, math
from PIL import Image, ImageDraw
cert = json.load(open("sycro_salida/certificado.json"))
freqs = cert["frecuencias_cymatic"]
W = H = 800
img = Image.new("RGB", (W, H), "black")
draw = ImageDraw.Draw(img)
cx, cy = W//2, H//2
colors = [(0,240,255), (255,0,229), (255,215,0)]
for k, col in enumerate(colors):
    pts = []
    for i in range(701):
        th = i/700*2*math.pi
        r = 90
        for f in freqs:
            r += 16*math.sin(f/60*th + k)
        x = cx + math.cos(th)*r*1.5
        y = cy + math.sin(th)*r*1.5
        pts.append((x, y))
    draw.line(pts, fill=col, width=2)
img.save("sycro_salida/sello_cymatic.png")
print("Sello PNG creado sin matplotlib")
print(f"Frecuencias: {freqs}")
