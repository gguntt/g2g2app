"""Launcher icon: calculator first, exchange rate as the detail that sets it apart."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = 1024
ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "app" / "src" / "main" / "res"
OUT = Path(__file__).resolve().parent

HANA = (0, 132, 133)
SHINHAN = (0, 70, 255)
BODY = (236, 241, 246, 255)
DISPLAY = (11, 28, 46, 255)
NUM = (255, 255, 255, 255)
OP = (214, 226, 240, 255)
EQUALS = (255, 122, 26, 255)
DOLLAR = (61, 220, 151, 255)
WON = (255, 196, 64, 255)
ARROW = (255, 255, 255, 255)


def font(size: int) -> ImageFont.FreeTypeFont:
    for name in ("segoeuib.ttf", "segoeuisb.ttf", "malgunbd.ttf", "arialbd.ttf"):
        path = Path(r"C:\Windows\Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def gradient() -> Image.Image:
    img = Image.new("RGB", (SIZE, SIZE))
    px = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            t = (x * 0.62 + y * 0.38) / (SIZE - 1)
            t = t * t * (3 - 2 * t)
            px[x, y] = tuple(int(a + (b - a) * t) for a, b in zip(HANA, SHINHAN))
    return img


def swap_arrows(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    gap = 16
    length = 54
    head = 16
    y1 = cy - gap
    draw.line((cx - length, y1, cx + length - head, y1), fill=ARROW, width=9)
    draw.polygon(
        [(cx + length - head - 2, y1 - 12), (cx + length + 6, y1), (cx + length - head - 2, y1 + 12)],
        fill=ARROW,
    )
    y2 = cy + gap
    draw.line((cx - length + head, y2, cx + length, y2), fill=ARROW, width=9)
    draw.polygon(
        [(cx - length + head + 2, y2 - 12), (cx - length - 6, y2), (cx - length + head + 2, y2 + 12)],
        fill=ARROW,
    )


def foreground() -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((228, 214, 812, 836), radius=86, fill=(0, 20, 40, 110))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16)))

    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((214, 196, 810, 828), radius=80, fill=BODY)

    disp = (250, 232, 774, 408)
    draw.rounded_rectangle(disp, radius=32, fill=DISPLAY)
    draw.rounded_rectangle((274, 392, 750, 400), radius=2, fill=WON)

    face = font(118)
    draw.text((292, 268), "$", font=face, fill=DOLLAR, anchor="lm")
    draw.text((732, 268), "₩", font=face, fill=WON, anchor="rm")
    swap_arrows(draw, 512, 300)

    left, top = 262, 436
    cols, rows = 4, 4
    gap = 14
    bw, bh = 112, 80
    for row in range(rows):
        for col in range(cols):
            x = left + col * (bw + gap)
            y = top + row * (bh + gap)
            is_eq = row == rows - 1 and col == cols - 1
            fill = EQUALS if is_eq else (OP if col == cols - 1 else NUM)
            draw.rounded_rectangle((x, y, x + bw, y + bh), radius=18, fill=fill)
            if is_eq:
                mid = y + bh // 2
                draw.rounded_rectangle((x + 34, mid - 16, x + bw - 34, mid - 8), radius=3, fill=(255, 255, 255, 255))
                draw.rounded_rectangle((x + 34, mid + 8, x + bw - 34, mid + 16), radius=3, fill=(255, 255, 255, 255))
    return img


def circle_mask(size: int) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    return mask


def save_sizes(image: Image.Image, name: str, sizes: dict[str, int]) -> None:
    for folder, size in sizes.items():
        dest = RES / folder
        dest.mkdir(parents=True, exist_ok=True)
        image.resize((size, size), Image.Resampling.LANCZOS).save(dest / name, optimize=True)


def main() -> None:
    bg = gradient()
    fg = foreground()
    full = bg.convert("RGBA")
    full.alpha_composite(fg)

    legacy = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }
    adaptive = {
        "mipmap-mdpi": 108,
        "mipmap-hdpi": 162,
        "mipmap-xhdpi": 216,
        "mipmap-xxhdpi": 324,
        "mipmap-xxxhdpi": 432,
    }
    save_sizes(bg, "ic_launcher_background.png", adaptive)
    save_sizes(fg, "ic_launcher_foreground.png", adaptive)
    save_sizes(full.convert("RGB"), "ic_launcher.png", legacy)

    for folder, size in legacy.items():
        icon = full.resize((size, size), Image.Resampling.LANCZOS)
        circled = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        circled.paste(icon, (0, 0))
        circled.putalpha(circle_mask(size))
        circled.save(RES / folder / "ic_launcher_round.png", optimize=True)

    preview = ROOT / "tools"
    preview.mkdir(parents=True, exist_ok=True)
    full.convert("RGB").resize((512, 512), Image.Resampling.LANCZOS).save(preview / "icon_preview.png")
    full.resize((192, 192), Image.Resampling.LANCZOS).save(preview / "icon_192.png")
    full.resize((48, 48), Image.Resampling.LANCZOS).save(preview / "icon_48.png")
    print("icons written")


if __name__ == "__main__":
    main()
