"""
Generate PNG icons for the Iskandal PWA.
Characters: 湯豆腐 (left, warm) and 冷奴 (right, cool) with arms around shoulders.
Requires: ImageMagick (convert command)
Run: python3 generate-icons.py
"""
import subprocess
import os

SVG = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <!-- Background -->
  <rect width="512" height="512" fill="#1a1a2e"/>

  <!-- Ground shadows -->
  <ellipse cx="145" cy="392" rx="75" ry="12" fill="#0d0d1a" opacity="0.7"/>
  <ellipse cx="367" cy="392" rx="75" ry="12" fill="#0d0d1a" opacity="0.7"/>

  <!-- ======== 湯豆腐 (hot tofu) LEFT ======== -->
  <!-- Bowl -->
  <ellipse cx="145" cy="383" rx="68" ry="14" fill="#7b4f2e"/>
  <rect x="85" y="372" width="120" height="16" rx="8" fill="#6b3f1e"/>
  <!-- Broth surface -->
  <ellipse cx="145" cy="372" rx="60" ry="10" fill="#c8901a" opacity="0.4"/>

  <!-- Body (tofu block, slight warm tint) -->
  <rect x="85" y="222" width="120" height="152" rx="12" fill="#f8f3e8"/>
  <!-- Top face -->
  <rect x="85" y="222" width="120" height="20" rx="8" fill="#ede5d0"/>
  <!-- Texture grid -->
  <line x1="91" y1="260" x2="199" y2="260" stroke="#e5dcca" stroke-width="1.5"/>
  <line x1="91" y1="295" x2="199" y2="295" stroke="#e5dcca" stroke-width="1.5"/>
  <line x1="91" y1="330" x2="199" y2="330" stroke="#e5dcca" stroke-width="1.5"/>
  <line x1="127" y1="228" x2="127" y2="370" stroke="#e5dcca" stroke-width="1.5"/>
  <line x1="163" y1="228" x2="163" y2="370" stroke="#e5dcca" stroke-width="1.5"/>

  <!-- Eyes (happy, round) -->
  <ellipse cx="127" cy="275" rx="13" ry="14" fill="#2d2016"/>
  <ellipse cx="163" cy="275" rx="13" ry="14" fill="#2d2016"/>
  <ellipse cx="131" cy="269" rx="5" ry="5" fill="white"/>
  <ellipse cx="167" cy="269" rx="5" ry="5" fill="white"/>
  <!-- Eyebrows (raised, happy) -->
  <path d="M115 258 Q127 249 139 258" stroke="#6b4c2a" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <path d="M151 258 Q163 249 175 258" stroke="#6b4c2a" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <!-- Big smile -->
  <path d="M118 308 Q145 335 172 308" stroke="#2d2016" stroke-width="5" fill="none" stroke-linecap="round"/>
  <!-- Warm cheeks -->
  <ellipse cx="108" cy="296" rx="16" ry="10" fill="#ff8c6b" opacity="0.55"/>
  <ellipse cx="182" cy="296" rx="16" ry="10" fill="#ff8c6b" opacity="0.55"/>

  <!-- Steam wisps -->
  <path d="M116 220 C112 202 120 186 114 166 C108 146 116 128 110 108"
        stroke="#c8c0b0" stroke-width="4.5" fill="none" stroke-linecap="round" opacity="0.65"/>
  <path d="M145 220 C141 200 149 182 143 160 C137 138 145 120 139 100"
        stroke="#c8c0b0" stroke-width="4.5" fill="none" stroke-linecap="round" opacity="0.65"/>
  <path d="M174 220 C170 202 178 186 172 166 C166 146 174 128 168 108"
        stroke="#c8c0b0" stroke-width="4.5" fill="none" stroke-linecap="round" opacity="0.65"/>

  <!-- ======== 冷奴 (cold tofu) RIGHT ======== -->
  <!-- Plate -->
  <ellipse cx="367" cy="383" rx="68" ry="14" fill="#4a5568"/>
  <rect x="307" y="372" width="120" height="16" rx="8" fill="#3d4555"/>

  <!-- Body (tofu block, cool blue-white) -->
  <rect x="307" y="222" width="120" height="152" rx="12" fill="#edf3ff"/>
  <!-- Top face -->
  <rect x="307" y="222" width="120" height="20" rx="8" fill="#ddeaff"/>
  <!-- Texture grid -->
  <line x1="313" y1="260" x2="421" y2="260" stroke="#d5e5f8" stroke-width="1.5"/>
  <line x1="313" y1="295" x2="421" y2="295" stroke="#d5e5f8" stroke-width="1.5"/>
  <line x1="313" y1="330" x2="421" y2="330" stroke="#d5e5f8" stroke-width="1.5"/>
  <line x1="349" y1="228" x2="349" y2="370" stroke="#d5e5f8" stroke-width="1.5"/>
  <line x1="385" y1="228" x2="385" y2="370" stroke="#d5e5f8" stroke-width="1.5"/>

  <!-- Sunglasses (left lens) -->
  <rect x="318" y="267" width="42" height="26" rx="10" fill="#162040"/>
  <rect x="318" y="267" width="42" height="26" rx="10" fill="none" stroke="#0a1428" stroke-width="2.5"/>
  <ellipse cx="334" cy="276" rx="9" ry="5" fill="white" opacity="0.2"/>
  <!-- Sunglasses (bridge) -->
  <line x1="360" y1="280" x2="376" y2="280" stroke="#0a1428" stroke-width="5"/>
  <!-- Sunglasses (right lens) -->
  <rect x="376" y="267" width="42" height="26" rx="10" fill="#162040"/>
  <rect x="376" y="267" width="42" height="26" rx="10" fill="none" stroke="#0a1428" stroke-width="2.5"/>
  <ellipse cx="392" cy="276" rx="9" ry="5" fill="white" opacity="0.2"/>
  <!-- Sunglasses arms -->
  <line x1="318" y1="280" x2="307" y2="276" stroke="#0a1428" stroke-width="4" stroke-linecap="round"/>
  <line x1="418" y1="280" x2="427" y2="276" stroke="#0a1428" stroke-width="4" stroke-linecap="round"/>

  <!-- Cool smirk -->
  <path d="M340 320 Q360 332 382 322" stroke="#2d2d3d" stroke-width="5" fill="none" stroke-linecap="round"/>
  <!-- Cool cheeks (subtle blue) -->
  <ellipse cx="318" cy="305" rx="13" ry="8" fill="#7dd3fc" opacity="0.3"/>
  <ellipse cx="414" cy="305" rx="13" ry="8" fill="#7dd3fc" opacity="0.3"/>

  <!-- Toppings: green onion slivers -->
  <ellipse cx="345" cy="227" rx="9" ry="4" fill="#5a9e3a" opacity="0.85" transform="rotate(-20 345 227)"/>
  <ellipse cx="367" cy="223" rx="9" ry="4" fill="#4a8e2a" opacity="0.85" transform="rotate(10 367 223)"/>
  <ellipse cx="388" cy="227" rx="9" ry="4" fill="#5a9e3a" opacity="0.85" transform="rotate(25 388 227)"/>

  <!-- Ice crystals (left of body) -->
  <g transform="translate(290,155)" opacity="0.75">
    <line x1="10" y1="0" x2="10" y2="20" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="0" y1="10" x2="20" y2="10" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="2" y1="2" x2="18" y2="18" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="18" y1="2" x2="2" y2="18" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <!-- Ice crystals (right of body) -->
  <g transform="translate(403,148)" opacity="0.75">
    <line x1="10" y1="0" x2="10" y2="20" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="0" y1="10" x2="20" y2="10" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="2" y1="2" x2="18" y2="18" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="18" y1="2" x2="2" y2="18" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round"/>
  </g>

  <!-- ======== Coin pyramid at feet ======== -->
  <!-- Row 4 bottom: 7 coins (y=432, r=13) gold/copper alternating -->
  <circle cx="182" cy="432" r="13" fill="#b89010"/><circle cx="182" cy="432" r="10" fill="#f0c030"/><circle cx="182" cy="432" r="5" fill="#12122a"/><circle cx="182" cy="432" r="3" fill="#c8b030"/>
  <circle cx="207" cy="432" r="13" fill="#8a4810"/><circle cx="207" cy="432" r="10" fill="#c86828"/><circle cx="207" cy="432" r="5" fill="#12122a"/><circle cx="207" cy="432" r="3" fill="#a05820"/>
  <circle cx="232" cy="432" r="13" fill="#b89010"/><circle cx="232" cy="432" r="10" fill="#f0c030"/><circle cx="232" cy="432" r="5" fill="#12122a"/><circle cx="232" cy="432" r="3" fill="#c8b030"/>
  <circle cx="256" cy="432" r="13" fill="#8a4810"/><circle cx="256" cy="432" r="10" fill="#c86828"/><circle cx="256" cy="432" r="5" fill="#12122a"/><circle cx="256" cy="432" r="3" fill="#a05820"/>
  <circle cx="280" cy="432" r="13" fill="#b89010"/><circle cx="280" cy="432" r="10" fill="#f0c030"/><circle cx="280" cy="432" r="5" fill="#12122a"/><circle cx="280" cy="432" r="3" fill="#c8b030"/>
  <circle cx="305" cy="432" r="13" fill="#8a4810"/><circle cx="305" cy="432" r="10" fill="#c86828"/><circle cx="305" cy="432" r="5" fill="#12122a"/><circle cx="305" cy="432" r="3" fill="#a05820"/>
  <circle cx="330" cy="432" r="13" fill="#b89010"/><circle cx="330" cy="432" r="10" fill="#f0c030"/><circle cx="330" cy="432" r="5" fill="#12122a"/><circle cx="330" cy="432" r="3" fill="#c8b030"/>
  <!-- Row 3: 5 coins (y=417, r=12) -->
  <circle cx="207" cy="417" r="12" fill="#8a4810"/><circle cx="207" cy="417" r="9" fill="#c86828"/><circle cx="207" cy="417" r="4" fill="#12122a"/><circle cx="207" cy="417" r="2" fill="#a05820"/>
  <circle cx="232" cy="417" r="12" fill="#b89010"/><circle cx="232" cy="417" r="9" fill="#f0c030"/><circle cx="232" cy="417" r="4" fill="#12122a"/><circle cx="232" cy="417" r="2" fill="#c8b030"/>
  <circle cx="256" cy="417" r="12" fill="#8a4810"/><circle cx="256" cy="417" r="9" fill="#c86828"/><circle cx="256" cy="417" r="4" fill="#12122a"/><circle cx="256" cy="417" r="2" fill="#a05820"/>
  <circle cx="280" cy="417" r="12" fill="#b89010"/><circle cx="280" cy="417" r="9" fill="#f0c030"/><circle cx="280" cy="417" r="4" fill="#12122a"/><circle cx="280" cy="417" r="2" fill="#c8b030"/>
  <circle cx="305" cy="417" r="12" fill="#8a4810"/><circle cx="305" cy="417" r="9" fill="#c86828"/><circle cx="305" cy="417" r="4" fill="#12122a"/><circle cx="305" cy="417" r="2" fill="#a05820"/>
  <!-- Row 2: 3 coins (y=403, r=11) -->
  <circle cx="232" cy="403" r="11" fill="#b89010"/><circle cx="232" cy="403" r="8" fill="#f0c030"/><circle cx="232" cy="403" r="4" fill="#12122a"/><circle cx="232" cy="403" r="2" fill="#c8b030"/>
  <circle cx="256" cy="403" r="11" fill="#8a4810"/><circle cx="256" cy="403" r="8" fill="#c86828"/><circle cx="256" cy="403" r="4" fill="#12122a"/><circle cx="256" cy="403" r="2" fill="#a05820"/>
  <circle cx="280" cy="403" r="11" fill="#b89010"/><circle cx="280" cy="403" r="8" fill="#f0c030"/><circle cx="280" cy="403" r="4" fill="#12122a"/><circle cx="280" cy="403" r="2" fill="#c8b030"/>
  <!-- Row 1 top: 1 coin (y=391, r=10) -->
  <circle cx="256" cy="391" r="10" fill="#b89010"/><circle cx="256" cy="391" r="7" fill="#f0c030"/><circle cx="256" cy="391" r="3" fill="#12122a"/>

  <!-- ======== Arms (shoulder embrace) ======== -->
  <!-- Cold tofu LEFT arm → over hot tofu right shoulder (drawn first = behind) -->
  <path d="M307 262 C280 238 240 228 205 242"
        stroke="#c8d8f0" stroke-width="22" fill="none" stroke-linecap="round"/>
  <path d="M307 262 C280 238 240 228 205 242"
        stroke="#ddeaff" stroke-width="16" fill="none" stroke-linecap="round"/>

  <!-- Hot tofu RIGHT arm → over cold tofu left shoulder (drawn after = in front) -->
  <path d="M205 262 C232 238 272 228 307 242"
        stroke="#c8b090" stroke-width="22" fill="none" stroke-linecap="round"/>
  <path d="M205 262 C232 238 272 228 307 242"
        stroke="#f0e8d8" stroke-width="16" fill="none" stroke-linecap="round"/>

  <!-- Title at bottom -->
  <text x="256" y="464"
        text-anchor="middle"
        font-family="Arial Black, Impact, sans-serif"
        font-size="44" font-weight="900"
        textLength="370" lengthAdjust="spacingAndGlyphs"
        fill="#4fc3f7">ISKANDAL</text>
</svg>'''


def main():
    os.makedirs('icons', exist_ok=True)
    svg_path = '/tmp/iskandal_icon.svg'
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(SVG)

    for size in [192, 512]:
        out = f'icons/icon-{size}.png'
        result = subprocess.run(
            ['convert', '-background', 'none',
             '-resize', f'{size}x{size}',
             svg_path, out],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f'Created {out} ({os.path.getsize(out):,} bytes)')
        else:
            print(f'Error: {result.stderr}')


if __name__ == '__main__':
    main()
