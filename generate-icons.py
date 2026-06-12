"""
Generate PNG icons for the Iskandal PWA.
Run: python3 generate-icons.py
"""
import struct
import zlib
import os

def create_png(size, bg_rgb, fg_rgb):
    w, h = size, size
    br, bg_c, bb = bg_rgb
    fr, fg_c, fb = fg_rgb

    raw = bytearray()
    for y in range(h):
        raw.append(0)  # filter: none
        for x in range(w):
            cx, cy = w // 2, h // 2
            vbar_w = max(2, w // 10)
            vbar_h = max(4, h * 3 // 5)
            hbar_w = max(4, w // 4)
            hbar_h = max(2, h // 12)

            in_vbar = (abs(x - cx) <= vbar_w and abs(y - cy) <= vbar_h // 2)
            in_top  = (abs(x - cx) <= hbar_w and abs(y - (cy - vbar_h // 2)) <= hbar_h)
            in_bot  = (abs(x - cx) <= hbar_w and abs(y - (cy + vbar_h // 2)) <= hbar_h)

            if in_vbar or in_top or in_bot:
                raw.extend([fr, fg_c, fb])
            else:
                raw.extend([br, bg_c, bb])

    def chunk(name, data):
        crc = zlib.crc32(name + data) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', crc)

    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    idat = zlib.compress(bytes(raw), 9)

    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')

os.makedirs('icons', exist_ok=True)

bg = (26, 26, 46)    # #1a1a2e
fg = (79, 195, 247)  # #4fc3f7

for size in [192, 512]:
    data = create_png(size, bg, fg)
    path = f'icons/icon-{size}.png'
    with open(path, 'wb') as f:
        f.write(data)
    print(f'Created {path} ({len(data)} bytes)')
