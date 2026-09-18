#!/usr/bin/env python3
"""Draw a project cover card in the same language as the ones in the handoff.

The covers that came with the design (uploads/covers/P-01..P-12.png) were
produced by the design tool, which is not part of this repo. A project added
afterwards still needs one, so this redraws the same card: 1280x720, steel
accent rule across the top, the ruled blueprint field, the kicker, the title,
and the method x field line over the team.

Every measurement here was read back off uploads/covers/P-12.png rather than
guessed — the band positions, the 40px rule pitch, the fade down the rules and
the exact palette. Only the motif differs per project, as it does in the
originals, and this one is deliberately abstract.

    python3 tools/make_cover.py P-13 "Title" "Method" "Field" "Team" out.png
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
MARGIN = 64

BG = (44, 69, 93)
ACCENT = (89, 128, 166)
LIGHT = (181, 217, 253)          # kicker, meta, and the ruled field
TITLE = (242, 242, 243)
TEAM = (183, 191, 199)

BAR_H = 6
RULE_TOP, RULE_PITCH, RULE_H, RULE_LAST = 99, 40, 2, 619
RULE_ALPHA_TOP, RULE_ALPHA_BOTTOM = 0.350, 0.131   # linear between y=99 and y=579

FONT_DIR = pathlib.Path("/usr/share/fonts/truetype/liberation")
BOLD = FONT_DIR / "LiberationSans-Bold.ttf"
REGULAR = FONT_DIR / "LiberationSans-Regular.ttf"


def blend(colour, alpha, over=BG):
    return tuple(round(o + alpha * (c - o)) for c, o in zip(colour, over))


def cap_y(top, font, sample="H"):
    """PIL positions text by its ascender box; the originals line up on cap height."""
    return top - font.getbbox(sample)[1]

def tracked(draw, xy, text, font, fill, tracking=0.0):
    """Draw text with letter spacing, which PIL has no setting for."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def wrap(text, font, draw, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def motif(draw):
    """Many candidates, a few selected: the shape of a feature-selection result.

    The originals carry a figure hinting at the project's subject. This is the
    same idea at the same weight, drawn from primitives rather than pretending
    to be a domain illustration.
    """
    cols, rows = 26, 5
    gap_x, gap_y, size = 22, 22, 9
    x0 = W - MARGIN - (cols * gap_x - (gap_x - size))
    y0 = 306
    picked = {(0, 3), (1, 17), (2, 8), (3, 21), (4, 12), (1, 4), (3, 9)}
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * gap_x, y0 + r * gap_y
            if (r, c) in picked:
                draw.rectangle([x, y, x + size, y + size], fill=blend(LIGHT, 0.85))
            else:
                draw.rectangle([x, y, x + size, y + size], fill=blend(LIGHT, 0.16))


def build(pid, title, method, field, team, dest):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W - 1, BAR_H - 1], fill=ACCENT)

    span = 579 - RULE_TOP
    for y in range(RULE_TOP, RULE_LAST + 1, RULE_PITCH):
        t = (y - RULE_TOP) / span
        alpha = RULE_ALPHA_TOP + t * (RULE_ALPHA_BOTTOM - RULE_ALPHA_TOP)
        draw.rectangle([0, y, W - 3, y + RULE_H - 1], fill=blend(LIGHT, max(alpha, 0.0)))

    motif(draw)

    kicker = ImageFont.truetype(str(BOLD), 20)
    tracked(draw, (MARGIN, cap_y(61, kicker)), f"PAIRS · SUMMER 2026 · {pid}",
            kicker, LIGHT, tracking=0.3)

    title_font = ImageFont.truetype(str(BOLD), 46)
    lines = wrap(title, title_font, draw, W - 2 * MARGIN - 40)
    top = 429 if len(lines) <= 2 else 429 - 61 * (len(lines) - 2)
    for i, line in enumerate(lines):
        draw.text((MARGIN, cap_y(top + i * 61, title_font)), line,
                  font=title_font, fill=TITLE)

    meta_font = ImageFont.truetype(str(BOLD), 20)
    end = tracked(draw, (MARGIN, cap_y(604, meta_font)),
                  f"{method.upper()}  ×  {field.upper()}", meta_font, LIGHT, tracking=1.2)
    draw.rectangle([MARGIN, 623, max(int(end) + 20, W - MARGIN), 624],
                   fill=blend((255, 255, 255), 0.204))

    team_font = ImageFont.truetype(str(REGULAR), 22)
    draw.text((MARGIN, cap_y(648, team_font)), team, font=team_font, fill=TEAM)

    img.save(dest, "PNG")
    return dest


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print(__doc__, file=sys.stderr)
        raise SystemExit(2)
    print(build(*sys.argv[1:6], pathlib.Path(sys.argv[6])))
