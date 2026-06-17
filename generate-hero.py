"""
Generate top page hero image for Iskandal PWA (v3).
600x600 square: hot tofu vs cold tofu rivals on Planet Iscandar.
Requires: ImageMagick (convert command)
Run: python3 generate-hero.py
Output: images/hero.png
"""
import math
import random
import subprocess
import os


def rot(cx, cy, deg):
    """SVG matrix() for rotation around (cx,cy). Avoids ImageMagick rotate() bug."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    e = cx * (1 - c) + cy * s
    f = cy * (1 - c) - cx * s
    return f'matrix({c:.5f},{s:.5f},{-s:.5f},{c:.5f},{e:.3f},{f:.3f})'


def coin(cx, cy, rx=21, ry=10, gold=True):
    if gold:
        c1, c2, c3, c4 = '#7a5800', '#c88818', '#f0c020', '#7a5800'
    else:
        c1, c2, c3, c4 = '#484858', '#8090a0', '#c0c8d4', '#484858'
    return (
        f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx}" ry="{ry}" fill="{c1}"/>'
        f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx-2}" ry="{ry-1}" fill="{c2}"/>'
        f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx-6}" ry="{ry-2}" fill="{c3}"/>'
        f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="3" fill="{c4}"/>'
    )


def coin_pile(cx, cy, rx_e=112, ry_e=62, seed=42):
    """Grid+jitter coin pile for dense, even coverage. Centre coins lifted (mound shape)."""
    rng = random.Random(seed)
    # Grid: 22px x-step, 11px y-step — matches large coin size (rx=21, ry=10)
    step_x = 22.0
    step_y = 11.0
    nx = int(rx_e * 2 / step_x) + 2
    ny = int(ry_e * 2 / step_y) + 2
    items = []
    for gi in range(-nx // 2, nx // 2 + 1):
        for gj in range(-ny // 2, ny // 2 + 1):
            dx = gi * step_x + rng.uniform(-step_x * 0.52, step_x * 0.52)
            dy = gj * step_y + rng.uniform(-step_y * 0.52, step_y * 0.52)
            if (dx / rx_e) ** 2 + (dy / ry_e) ** 2 > 1.0:
                continue
            dist = math.sqrt((dx / rx_e) ** 2 + (dy / ry_e) ** 2)
            lift = (1.0 - dist ** 1.8) * 30   # centre lifted up to 30px
            px = cx + dx
            py = cy + dy - lift
            sz = 0.75 + 0.25 * dist            # slight size gradient
            gold = rng.random() > 0.22
            items.append((py, px, py, sz, gold))
    items.sort(key=lambda t: t[0])             # painter's algorithm back-to-front
    parts = []
    for _, px, py, sz, gold in items:
        rxi = max(14, round(21 * sz))
        ryi = max(7, round(10 * sz))
        parts.append(coin(px, py, rx=rxi, ry=ryi, gold=gold))
    return '\n  '.join(parts)


COINS = coin_pile(cx=300, cy=445)

SVG = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <defs>
    <radialGradient id="bg" cx="50%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#101828"/>
      <stop offset="100%" stop-color="#04040c"/>
    </radialGradient>
  </defs>

  <!-- SPACE BACKGROUND -->
  <rect width="600" height="600" fill="url(#bg)"/>

  <!-- Stars -->
  <circle cx="22"  cy="18"  r="1.5" fill="white" opacity="0.85"/>
  <circle cx="65"  cy="42"  r="1"   fill="white" opacity="0.65"/>
  <circle cx="108" cy="22"  r="2"   fill="white" opacity="0.7"/>
  <circle cx="150" cy="50"  r="1"   fill="white" opacity="0.9"/>
  <circle cx="195" cy="12"  r="1.5" fill="white" opacity="0.8"/>
  <circle cx="242" cy="38"  r="1"   fill="white" opacity="0.55"/>
  <circle cx="290" cy="22"  r="1.5" fill="white" opacity="0.9"/>
  <circle cx="338" cy="47"  r="1"   fill="white" opacity="0.7"/>
  <circle cx="382" cy="16"  r="2"   fill="white" opacity="0.6"/>
  <circle cx="432" cy="40"  r="1"   fill="white" opacity="0.8"/>
  <circle cx="540" cy="28"  r="1.5" fill="white" opacity="0.75"/>
  <circle cx="572" cy="55"  r="1"   fill="white" opacity="0.6"/>
  <circle cx="38"  cy="88"  r="1"   fill="white" opacity="0.7"/>
  <circle cx="82"  cy="108" r="1.5" fill="white" opacity="0.8"/>
  <circle cx="128" cy="90"  r="1"   fill="white" opacity="0.6"/>
  <circle cx="172" cy="118" r="1.5" fill="white" opacity="0.75"/>
  <circle cx="220" cy="98"  r="1"   fill="white" opacity="0.9"/>
  <circle cx="262" cy="132" r="2"   fill="white" opacity="0.5"/>
  <circle cx="315" cy="85"  r="1"   fill="white" opacity="0.8"/>
  <circle cx="358" cy="115" r="1.5" fill="white" opacity="0.7"/>
  <circle cx="402" cy="92"  r="1"   fill="white" opacity="0.65"/>
  <circle cx="558" cy="108" r="1.5" fill="white" opacity="0.8"/>
  <circle cx="585" cy="88"  r="1"   fill="white" opacity="0.7"/>
  <circle cx="45"  cy="162" r="1"   fill="white" opacity="0.6"/>
  <circle cx="95"  cy="182" r="1.5" fill="white" opacity="0.7"/>
  <circle cx="145" cy="162" r="1"   fill="white" opacity="0.8"/>
  <circle cx="192" cy="195" r="1.5" fill="white" opacity="0.6"/>
  <circle cx="242" cy="170" r="1"   fill="white" opacity="0.9"/>
  <circle cx="345" cy="188" r="1"   fill="white" opacity="0.7"/>
  <circle cx="395" cy="165" r="1.5" fill="white" opacity="0.8"/>
  <circle cx="562" cy="170" r="1"   fill="white" opacity="0.6"/>
  <circle cx="588" cy="195" r="1.5" fill="white" opacity="0.7"/>
  <circle cx="55"  cy="215" r="0.8" fill="white" opacity="0.45"/>
  <circle cx="115" cy="230" r="0.8" fill="white" opacity="0.4"/>
  <circle cx="285" cy="218" r="0.8" fill="white" opacity="0.4"/>
  <circle cx="412" cy="228" r="0.8" fill="white" opacity="0.45"/>
  <circle cx="490" cy="210" r="0.8" fill="white" opacity="0.4"/>
  <circle cx="535" cy="238" r="0.8" fill="white" opacity="0.4"/>

  <!-- Earth (upper right) — blue ocean, brown land, white clouds, thin and spread -->
  <circle cx="508" cy="78" r="40" fill="#1254a0"/>
  <!-- Deep ocean shading (瑠璃色: vivid lapis blue) -->
  <ellipse cx="496" cy="94" rx="22" ry="22" fill="#1540c8" opacity="0.32"/>
  <!-- Americas — brown, wide ellipses, thin -->
  <ellipse cx="486" cy="65" rx="13" ry="18" fill="#9a7244" opacity="0.55"/>
  <ellipse cx="483" cy="93" rx="11" ry="20" fill="#8a6232" opacity="0.48"/>
  <!-- Greenland ice cap -->
  <ellipse cx="494" cy="50" rx="9"  ry="6"  fill="#d8eef8" opacity="0.60"/>
  <!-- Eurasia — wide brown mass -->
  <ellipse cx="516" cy="57" rx="22" ry="16" fill="#9a7244" opacity="0.52"/>
  <ellipse cx="530" cy="68" rx="16" ry="12" fill="#8a6232" opacity="0.46"/>
  <!-- Africa — tall brown ellipse -->
  <ellipse cx="512" cy="90" rx="13" ry="20" fill="#9a7244" opacity="0.50"/>
  <!-- Australia -->
  <ellipse cx="527" cy="101" rx="10" ry="9"  fill="#9a7244" opacity="0.44"/>
  <!-- Antarctica -->
  <ellipse cx="508" cy="113" rx="20" ry="5"  fill="#ddeeff" opacity="0.52"/>
  <!-- Clouds — white, wide, very thin -->
  <ellipse cx="494" cy="54" rx="16" ry="8"  fill="white" opacity="0.40"/>
  <ellipse cx="516" cy="50" rx="17" ry="7"  fill="white" opacity="0.36"/>
  <ellipse cx="500" cy="98" rx="22" ry="8"  fill="white" opacity="0.34"/>
  <ellipse cx="532" cy="76" rx="14" ry="6"  fill="white" opacity="0.32"/>
  <ellipse cx="484" cy="84" rx="12" ry="6"  fill="white" opacity="0.30"/>
  <ellipse cx="500" cy="68" rx="18" ry="6"  fill="white" opacity="0.28"/>
  <!-- Night-side terminator (瑠璃色: deep lapis lazuli) -->
  <ellipse cx="530" cy="78" rx="17" ry="29" fill="#1830d0" opacity="0.55"/>
  <!-- Edge clean-up stroke -->
  <circle cx="508" cy="78" r="40" fill="none" stroke="#1254a0" stroke-width="1"/>
  <!-- Atmospheric glow -->
  <circle cx="508" cy="78" r="43" fill="none" stroke="#60c0ff" stroke-width="5" opacity="0.28"/>
  <circle cx="508" cy="78" r="40" fill="none" stroke="#a8d8ff" stroke-width="1.5" opacity="0.45"/>

  <!-- PLANET GROUND (horizon raised to character feet level) -->
  <path d="M0,600 L0,420 Q300,408 600,420 L600,600 Z" fill="#2e1848"/>
  <path d="M0,420 Q300,408 600,420" stroke="#48288a" stroke-width="2.5" fill="none" opacity="0.8"/>
  <!-- Subtle horizon glow -->
  <path d="M0,420 Q300,408 600,420" stroke="#8060c8" stroke-width="6" fill="none" opacity="0.18"/>

  <!-- Craters -->
  <ellipse cx="72"  cy="535" rx="58" ry="20" fill="#1c0e30" stroke="#2e1848" stroke-width="2"/>
  <ellipse cx="72"  cy="530" rx="46" ry="15" fill="#150a24"/>
  <path d="M25 530 Q72 514 119 530" stroke="#362055" stroke-width="1.5" fill="none" opacity="0.7"/>
  <ellipse cx="528" cy="548" rx="52" ry="17" fill="#1c0e30" stroke="#2e1848" stroke-width="2"/>
  <ellipse cx="528" cy="543" rx="42" ry="13" fill="#150a24"/>
  <path d="M484 543 Q528 529 572 543" stroke="#362055" stroke-width="1.5" fill="none" opacity="0.7"/>
  <ellipse cx="420" cy="510" rx="30" ry="10" fill="#1c0e30" stroke="#2e1848" stroke-width="1.5"/>
  <ellipse cx="420" cy="507" rx="24" ry="7"  fill="#150a24"/>
  <!-- Rocks -->
  <ellipse cx="168" cy="505" rx="11" ry="5" fill="#241535" transform="{rot(168,505,-5)}"/>
  <ellipse cx="375" cy="498" rx="8"  ry="4" fill="#241535"/>
  <ellipse cx="200" cy="528" rx="14" ry="6" fill="#1e1030" transform="{rot(200,528,8)}"/>
  <ellipse cx="460" cy="490" rx="10" ry="4" fill="#241535" transform="{rot(460,490,-8)}"/>

  <!-- Shadows (at ground surface = horizon level) -->
  <ellipse cx="125" cy="418" rx="55" ry="8"  fill="#0a061a" opacity="0.7"/>
  <ellipse cx="475" cy="418" rx="55" ry="8"  fill="#0a061a" opacity="0.7"/>
  <ellipse cx="300" cy="416" rx="80" ry="10" fill="#0a061a" opacity="0.65"/>

  <!-- ======== COIN PILE ======== -->
  {COINS}

  <!-- ======== 湯豆腐 (hot tofu, left) BANZAI POSE ======== -->
  <!-- Bowl -->
  <ellipse cx="125" cy="400" rx="60" ry="11" fill="#7b4f2e"/>
  <rect x="70" y="392" width="110" height="13" rx="6" fill="#6b3f1e"/>
  <ellipse cx="125" cy="392" rx="52" ry="8" fill="#c8901a" opacity="0.35"/>

  <!-- BANZAI arms — attachment point lowered to cheek level -->
  <!-- Left arm up-left -->
  <path d="M70 310 C52 278 40 244 36 208"
        stroke="#d8c8a8" stroke-width="16" fill="none" stroke-linecap="round"/>
  <path d="M70 310 C52 278 40 244 36 208"
        stroke="#f0e8d8" stroke-width="10" fill="none" stroke-linecap="round"/>
  <!-- Right arm up-right -->
  <path d="M180 310 C198 278 210 244 214 208"
        stroke="#d8c8a8" stroke-width="16" fill="none" stroke-linecap="round"/>
  <path d="M180 310 C198 278 210 244 214 208"
        stroke="#f0e8d8" stroke-width="10" fill="none" stroke-linecap="round"/>

  <!-- Body -->
  <rect x="70" y="220" width="110" height="172" rx="12" fill="#f8f3e8"/>
  <rect x="70" y="220" width="110" height="18"  rx="8"  fill="#ede5d0"/>
  <!-- Texture grid -->
  <line x1="76"  y1="258" x2="174" y2="258" stroke="#e5dcca" stroke-width="1.5"/>
  <line x1="76"  y1="292" x2="174" y2="292" stroke="#e5dcca" stroke-width="1.5"/>
  <line x1="76"  y1="326" x2="174" y2="326" stroke="#e5dcca" stroke-width="1.5"/>
  <line x1="76"  y1="360" x2="174" y2="360" stroke="#e5dcca" stroke-width="1.5"/>
  <line x1="103" y1="226" x2="103" y2="388" stroke="#e5dcca" stroke-width="1.5"/>
  <line x1="137" y1="226" x2="137" y2="388" stroke="#e5dcca" stroke-width="1.5"/>

  <!-- Headband (ねじり鉢巻) -->
  <rect x="70" y="238" width="110" height="16" rx="3" fill="#cc2233"/>
  <!-- Diagonal twist stripes -->
  <line x1="72"  y1="254" x2="88"  y2="238" stroke="white" stroke-width="2.5" opacity="0.4"/>
  <line x1="88"  y1="254" x2="104" y2="238" stroke="white" stroke-width="2.5" opacity="0.4"/>
  <line x1="104" y1="254" x2="120" y2="238" stroke="white" stroke-width="2.5" opacity="0.4"/>
  <line x1="120" y1="254" x2="136" y2="238" stroke="white" stroke-width="2.5" opacity="0.4"/>
  <line x1="136" y1="254" x2="152" y2="238" stroke="white" stroke-width="2.5" opacity="0.4"/>
  <line x1="152" y1="254" x2="168" y2="238" stroke="white" stroke-width="2.5" opacity="0.4"/>
  <line x1="168" y1="254" x2="180" y2="241" stroke="white" stroke-width="2.5" opacity="0.4"/>
  <!-- Knot (結び目) — improved 3D with highlight/shadow -->
  <!-- Tail up — wide red band with white diagonal stripes -->
  <path d="M77 234 C71 226 65 218 61 208" stroke="#661018" stroke-width="13" fill="none" stroke-linecap="round"/>
  <path d="M77 234 C71 226 65 218 61 208" stroke="#cc2233" stroke-width="9"  fill="none" stroke-linecap="round"/>
  <line x1="68" y1="231" x2="79" y2="225" stroke="white" stroke-width="2.5" opacity="0.45"/>
  <line x1="63" y1="225" x2="74" y2="219" stroke="white" stroke-width="2.5" opacity="0.45"/>
  <line x1="59" y1="218" x2="70" y2="212" stroke="white" stroke-width="2.5" opacity="0.45"/>
  <!-- Tail down — wide red band with white diagonal stripes (mirror of upper) -->
  <path d="M77 258 C71 266 66 275 63 285" stroke="#661018" stroke-width="13" fill="none" stroke-linecap="round"/>
  <path d="M77 258 C71 266 66 275 63 285" stroke="#cc2233" stroke-width="9"  fill="none" stroke-linecap="round"/>
  <line x1="67" y1="261" x2="79" y2="267" stroke="white" stroke-width="2.5" opacity="0.45"/>
  <line x1="63" y1="268" x2="75" y2="274" stroke="white" stroke-width="2.5" opacity="0.45"/>
  <line x1="60" y1="275" x2="72" y2="281" stroke="white" stroke-width="2.5" opacity="0.45"/>
  <!-- Upper loop shadow -->
  <ellipse cx="84" cy="240" rx="13" ry="10" fill="#5e0010" opacity="0.45" transform="{rot(84,240,-22)}"/>
  <!-- Upper loop -->
  <ellipse cx="82" cy="237" rx="13" ry="10" fill="#aa1525" transform="{rot(82,237,-22)}"/>
  <!-- Upper loop inner dark (3D depth) -->
  <ellipse cx="82" cy="238" rx="8"  ry="6"  fill="#7a0c18" opacity="0.7" transform="{rot(82,238,-22)}"/>
  <!-- Upper loop highlight -->
  <ellipse cx="80" cy="234" rx="5"  ry="3"  fill="#e03040" opacity="0.65" transform="{rot(80,234,-22)}"/>
  <!-- Lower loop shadow -->
  <ellipse cx="82" cy="258" rx="12" ry="9" fill="#5e0010" opacity="0.45" transform="{rot(82,258,18)}"/>
  <!-- Lower loop -->
  <ellipse cx="80" cy="255" rx="12" ry="9" fill="#bb1e2c" transform="{rot(80,255,18)}"/>
  <!-- Lower loop inner dark -->
  <ellipse cx="80" cy="256" rx="7"  ry="5" fill="#7a0c18" opacity="0.7" transform="{rot(80,256,18)}"/>
  <!-- Lower loop highlight -->
  <ellipse cx="78" cy="252" rx="4"  ry="2.5" fill="#e03040" opacity="0.65" transform="{rot(78,252,18)}"/>
  <!-- Centre knot body -->
  <circle cx="81" cy="246" r="10" fill="#6a0a14"/>
  <circle cx="81" cy="246" r="8"  fill="#981420"/>
  <!-- Centre highlight -->
  <ellipse cx="79" cy="243" rx="5" ry="3" fill="#e03045" opacity="0.6"/>
  <!-- Centre cross-weave texture -->
  <line x1="72" y1="246" x2="90" y2="246" stroke="#5a0810" stroke-width="1.5" opacity="0.55"/>
  <line x1="81" y1="237" x2="81" y2="255" stroke="#5a0810" stroke-width="1.5" opacity="0.55"/>

  <!-- Eyes (happy, wide open) -->
  <ellipse cx="107" cy="290" rx="13" ry="14" fill="#2d2016"/>
  <ellipse cx="143" cy="290" rx="13" ry="14" fill="#2d2016"/>
  <ellipse cx="111" cy="283" rx="6" ry="6" fill="white"/>
  <ellipse cx="147" cy="283" rx="6" ry="6" fill="white"/>

  <!-- Eyebrows (happy, raised) -->
  <path d="M97 270 Q107 260 119 265"
        stroke="#6b4c2a" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <path d="M131 265 Q143 260 155 269"
        stroke="#6b4c2a" stroke-width="3.5" fill="none" stroke-linecap="round"/>

  <!-- Big smile (ニッコリ) -->
  <path d="M86 336 Q125 376 164 336"
        stroke="#2d2016" stroke-width="5" fill="none" stroke-linecap="round"/>

  <!-- Warm cheeks -->
  <ellipse cx="88"  cy="314" rx="16" ry="10" fill="#ff8c6b" opacity="0.55"/>
  <ellipse cx="162" cy="314" rx="16" ry="10" fill="#ff8c6b" opacity="0.55"/>

  <!-- Steam wisps (5 wisps, dramatic) -->
  <path d="M82  220 C74  196 86  172 78  148 C70  124 82  100 74  76"
        stroke="#d8d0c0" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.6"/>
  <path d="M101 220 C91  198 105 172 97  148 C89  124 103 100 95  76"
        stroke="#d8d0c0" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.65"/>
  <path d="M125 220 C113 195 139 168 127 142 C115 116 141 92  129 66"
        stroke="#d8d0c0" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.75"/>
  <path d="M149 220 C159 198 145 172 155 148 C165 124 151 100 161 76"
        stroke="#d8d0c0" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.65"/>
  <path d="M168 220 C178 196 164 172 174 148 C184 124 170 100 180 76"
        stroke="#d8d0c0" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.6"/>

  <!-- ======== 冷奴 (cold tofu, right) GRUMPY ARMS-FOLDED ======== -->
  <!-- Plate -->
  <ellipse cx="475" cy="400" rx="60" ry="11" fill="#4a5568"/>
  <rect x="420" y="392" width="110" height="13" rx="6" fill="#3d4555"/>

  <!-- Body -->
  <rect x="420" y="220" width="110" height="172" rx="12" fill="#edf3ff"/>
  <rect x="420" y="220" width="110" height="18"  rx="8"  fill="#ddeaff"/>
  <!-- Texture grid -->
  <line x1="426" y1="258" x2="524" y2="258" stroke="#d5e5f8" stroke-width="1.5"/>
  <line x1="426" y1="292" x2="524" y2="292" stroke="#d5e5f8" stroke-width="1.5"/>
  <line x1="426" y1="326" x2="524" y2="326" stroke="#d5e5f8" stroke-width="1.5"/>
  <line x1="426" y1="360" x2="524" y2="360" stroke="#d5e5f8" stroke-width="1.5"/>
  <line x1="453" y1="226" x2="453" y2="388" stroke="#d5e5f8" stroke-width="1.5"/>
  <line x1="487" y1="226" x2="487" y2="388" stroke="#d5e5f8" stroke-width="1.5"/>

  <!-- ネギ (green onion) -->
  <ellipse cx="448" cy="206" rx="8" ry="22" fill="#4ab030" opacity="0.9" transform="{rot(448,206,-18)}"/>
  <ellipse cx="466" cy="200" rx="8" ry="26" fill="#5abf40" opacity="0.95"/>
  <ellipse cx="484" cy="206" rx="8" ry="22" fill="#4ab030" opacity="0.9" transform="{rot(484,206,18)}"/>
  <!-- ネギ white base -->
  <ellipse cx="449" cy="218" rx="6" ry="8"  fill="#d8f0c0" opacity="0.7" transform="{rot(449,218,-18)}"/>
  <ellipse cx="466" cy="220" rx="6" ry="8"  fill="#d8f0c0" opacity="0.7"/>
  <ellipse cx="483" cy="218" rx="6" ry="8"  fill="#d8f0c0" opacity="0.7" transform="{rot(483,218,18)}"/>

  <!-- Angry eyebrows -->
  <path d="M424 250 Q437 258 447 253"
        stroke="#1a1a2a" stroke-width="4.5" fill="none" stroke-linecap="round"/>
  <path d="M503 253 Q513 258 526 250"
        stroke="#1a1a2a" stroke-width="4.5" fill="none" stroke-linecap="round"/>

  <!-- Sunglasses -->
  <rect x="428" y="258" width="40" height="25" rx="9" fill="#162040"/>
  <rect x="428" y="258" width="40" height="25" rx="9" fill="none" stroke="#0a1428" stroke-width="2"/>
  <ellipse cx="444" cy="268" rx="9" ry="4.5" fill="white" opacity="0.18"/>
  <line x1="468" y1="271" x2="482" y2="271" stroke="#0a1428" stroke-width="5"/>
  <rect x="482" y="258" width="40" height="25" rx="9" fill="#162040"/>
  <rect x="482" y="258" width="40" height="25" rx="9" fill="none" stroke="#0a1428" stroke-width="2"/>
  <ellipse cx="498" cy="268" rx="9" ry="4.5" fill="white" opacity="0.18"/>
  <line x1="428" y1="271" x2="420" y2="267" stroke="#0a1428" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="522" y1="271" x2="530" y2="267" stroke="#0a1428" stroke-width="3.5" stroke-linecap="round"/>

  <!-- Grumpy frown — moved up, above the folded arms -->
  <path d="M447 310 Q475 296 503 310"
        stroke="#2d2d3d" stroke-width="5" fill="none" stroke-linecap="round"/>

  <!-- Cheeks (cool, subtle) -->
  <ellipse cx="432" cy="300" rx="13" ry="8" fill="#7dd3fc" opacity="0.28"/>
  <ellipse cx="518" cy="300" rx="13" ry="8" fill="#7dd3fc" opacity="0.28"/>

  <!-- Folded arms (腕組み) — redesigned for clearer X crossing at stomach level -->
  <!-- Right forearm (behind): from right, going lower-left -->
  <path d="M528,348 C514,352 496,362 464,372"
        stroke="#a8bcd8" stroke-width="24" fill="none" stroke-linecap="round"/>
  <path d="M528,348 C514,352 496,362 464,372"
        stroke="#ccdaee" stroke-width="16" fill="none" stroke-linecap="round"/>
  <!-- Right fist end -->
  <ellipse cx="460" cy="373" rx="11" ry="9" fill="#b8cce0"/>
  <ellipse cx="460" cy="373" rx="7"  ry="6" fill="#ccdaee"/>
  <!-- Left forearm (on top): from left, going upper-right, clearly crossing over -->
  <path d="M422,368 C438,358 458,350 488,342"
        stroke="#a8bcd8" stroke-width="24" fill="none" stroke-linecap="round"/>
  <path d="M422,368 C438,358 458,350 488,342"
        stroke="#ddeaff" stroke-width="16" fill="none" stroke-linecap="round"/>
  <!-- Left fist end -->
  <ellipse cx="492" cy="341" rx="11" ry="9" fill="#b8cce0"/>
  <ellipse cx="492" cy="341" rx="7"  ry="6" fill="#ddeaff"/>

  <!-- Ice crystals (dramatic) -->
  <g transform="translate(368,148)">
    <line x1="16" y1="0"  x2="16" y2="32" stroke="#a8eeff" stroke-width="3.5" stroke-linecap="round" opacity="0.9"/>
    <line x1="0"  y1="16" x2="32" y2="16" stroke="#a8eeff" stroke-width="3.5" stroke-linecap="round" opacity="0.9"/>
    <line x1="4"  y1="4"  x2="28" y2="28" stroke="#a8eeff" stroke-width="3.5" stroke-linecap="round" opacity="0.9"/>
    <line x1="28" y1="4"  x2="4"  y2="28" stroke="#a8eeff" stroke-width="3.5" stroke-linecap="round" opacity="0.9"/>
    <circle cx="16" cy="16" r="4" fill="#c8f4ff" opacity="0.85"/>
  </g>
  <g transform="translate(528,138)">
    <line x1="16" y1="0"  x2="16" y2="32" stroke="#a8eeff" stroke-width="3.5" stroke-linecap="round" opacity="0.9"/>
    <line x1="0"  y1="16" x2="32" y2="16" stroke="#a8eeff" stroke-width="3.5" stroke-linecap="round" opacity="0.9"/>
    <line x1="4"  y1="4"  x2="28" y2="28" stroke="#a8eeff" stroke-width="3.5" stroke-linecap="round" opacity="0.9"/>
    <line x1="28" y1="4"  x2="4"  y2="28" stroke="#a8eeff" stroke-width="3.5" stroke-linecap="round" opacity="0.9"/>
    <circle cx="16" cy="16" r="4" fill="#c8f4ff" opacity="0.85"/>
  </g>
  <g transform="translate(374,198)">
    <line x1="13" y1="0"  x2="13" y2="26" stroke="#7dd3fc" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
    <line x1="0"  y1="13" x2="26" y2="13" stroke="#7dd3fc" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
    <line x1="3"  y1="3"  x2="23" y2="23" stroke="#7dd3fc" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
    <line x1="23" y1="3"  x2="3"  y2="23" stroke="#7dd3fc" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
    <circle cx="13" cy="13" r="3" fill="#c8f4ff" opacity="0.75"/>
  </g>
  <g transform="translate(534,190)">
    <line x1="13" y1="0"  x2="13" y2="26" stroke="#7dd3fc" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
    <line x1="0"  y1="13" x2="26" y2="13" stroke="#7dd3fc" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
    <line x1="3"  y1="3"  x2="23" y2="23" stroke="#7dd3fc" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
    <line x1="23" y1="3"  x2="3"  y2="23" stroke="#7dd3fc" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
    <circle cx="13" cy="13" r="3" fill="#c8f4ff" opacity="0.75"/>
  </g>
  <g transform="translate(382,238)">
    <line x1="10" y1="0"  x2="10" y2="20" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>
    <line x1="0"  y1="10" x2="20" y2="10" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>
    <line x1="2"  y1="2"  x2="18" y2="18" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>
    <line x1="18" y1="2"  x2="2"  y2="18" stroke="#7dd3fc" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>
  </g>
  <!-- Ice sparkle dots -->
  <circle cx="360" cy="172" r="3"   fill="#c8f4ff" opacity="0.85"/>
  <circle cx="562" cy="165" r="3"   fill="#c8f4ff" opacity="0.85"/>
  <circle cx="366" cy="232" r="2"   fill="#a8eeff" opacity="0.75"/>
  <circle cx="555" cy="228" r="2"   fill="#a8eeff" opacity="0.75"/>
  <circle cx="392" cy="148" r="1.5" fill="#e8fcff" opacity="0.65"/>
  <circle cx="552" cy="245" r="1.5" fill="#e8fcff" opacity="0.65"/>
  <circle cx="348" cy="195" r="1.5" fill="#a8eeff" opacity="0.6"/>
  <circle cx="574" cy="212" r="1.5" fill="#a8eeff" opacity="0.6"/>

</svg>'''


def main():
    os.makedirs('images', exist_ok=True)
    import sys
    plain = '--plain' in sys.argv

    svg_path = '/tmp/iskandal_hero.svg'
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(SVG)

    out = 'images/hero-plain.png' if plain else 'images/hero.png'
    result = subprocess.run(
        ['convert', '-background', 'none', '-resize', '600x600', svg_path, out],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f'Error: {result.stderr}')
        return

    if not plain:
        # Add kanji labels via annotate (SVG text is ignored by ImageMagick renderer)
        result2 = subprocess.run([
            'convert', out,
            '-font', 'IPAゴシック',
            '-pointsize', '26', '-fill', '#b04010', '-draw', 'text 112,324 "湯"',
            '-pointsize', '20', '-fill', '#1844a0', '-draw', 'text 465,298 "冷"',
            out,
        ], capture_output=True, text=True)
        if result2.returncode != 0:
            print(f'Annotate error: {result2.stderr}')
            return

    print(f'Created {out} ({os.path.getsize(out):,} bytes)')


if __name__ == '__main__':
    main()
