from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "platform-terminal.gif"

WIDTH = 1120
HEIGHT = 620
PADDING = 26
LINE_HEIGHT = 26

COLORS = {
    "bg": "#0b0f14",
    "panel": "#111820",
    "border": "#223241",
    "text": "#d6deeb",
    "muted": "#617487",
    "red": "#ff6b7a",
    "green": "#8bd5a1",
    "cyan": "#77dbe8",
    "yellow": "#f8c878",
}


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/Library/Fonts/JetBrainsMono-Regular.ttf",
        "/Library/Fonts/FiraCode-Regular.ttf",
    ]
    for font_path in candidates:
        if Path(font_path).exists():
            return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()


FONT = load_font(20)
FONT_SMALL = load_font(18)
FONT_BOLD = load_font(20)


def draw_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, color: str, font=FONT) -> None:
    draw.text(xy, text, fill=color, font=font)


def base_frame() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        (10, 10, WIDTH - 10, HEIGHT - 10),
        radius=22,
        fill=COLORS["panel"],
        outline=COLORS["border"],
        width=2,
    )
    draw.ellipse((34, 32, 48, 46), fill="#ff5f57")
    draw.ellipse((58, 32, 72, 46), fill="#ffbd2e")
    draw.ellipse((82, 32, 96, 46), fill="#28c840")
    draw_text(draw, (124, 29), "babim@platform:~", COLORS["muted"], FONT_SMALL)
    return image


def draw_prompt(draw: ImageDraw.ImageDraw, command: str, cursor: bool = False) -> None:
    y = 72
    x = PADDING
    draw_text(draw, (x, y), "babim", COLORS["red"])
    draw_text(draw, (x + 58, y), "@", COLORS["text"])
    draw_text(draw, (x + 74, y), "platform", COLORS["cyan"])
    draw_text(draw, (x + 160, y), ":~$ ", COLORS["text"])
    draw_text(draw, (x + 212, y), command, COLORS["green"])
    if cursor:
        cursor_x = x + 212 + int(draw.textlength(command, font=FONT)) + 5
        draw_text(draw, (cursor_x, y), "_", COLORS["text"])


def draw_neofetch(draw: ImageDraw.ImageDraw) -> None:
    ascii_art = [
        "          _..._",
        "        .'     '.",
        "       /  .- -.  \\",
        "       | (  _  ) |",
        "       \\  `---'  /",
        "        '._____.'",
        "",
        "     /\\          /\\",
        "    /  \\  /\\    /  \\",
        "   /____\\/  \\__/____\\",
        "      calm systems",
    ]

    info = [
        ("babim-negev@GitHub", COLORS["red"]),
        ("-------------------", COLORS["muted"]),
        ("OS:      macOS, Windows, Rocky Linux", COLORS["text"]),
        ("Host:    Russia", COLORS["text"]),
        ("Kernel:  Software Engineer", COLORS["text"]),
        ("Uptime:  24 years", COLORS["text"]),
        ("IDE:     VSCode", COLORS["text"]),
        ("Work:    SRE / Platform Engineer", COLORS["text"]),
        ("Owner:   bash-forces.ru", COLORS["text"]),
        ("Focus:   homelab, reliability, automation", COLORS["text"]),
        ("", COLORS["text"]),
        ("Contact:", COLORS["red"]),
        ("---------", COLORS["muted"]),
        ("TG:      babim-negev", COLORS["text"]),
        ("Email:   captainprice1356@gmail.com", COLORS["text"]),
        ("", COLORS["text"]),
        ("Building calm systems and useful tools.", COLORS["green"]),
    ]

    header_y = 128
    art_x = 78
    art_y = header_y + 32
    info_x = 500

    for idx, line in enumerate(ascii_art):
        draw_text(draw, (art_x, art_y + idx * LINE_HEIGHT), line, COLORS["cyan"], FONT)

    for idx, (line, color) in enumerate(info):
        if line.startswith(("OS:", "Host:", "Kernel:", "Uptime:", "IDE:", "Work:", "Owner:", "Focus:", "TG:", "Email:")):
            label, value = line.split(":", 1)
            y = header_y + idx * LINE_HEIGHT
            draw_text(draw, (info_x, y), f"{label}:", COLORS["cyan"], FONT)
            draw_text(draw, (info_x + 92, y), value.strip(), color, FONT)
        else:
            draw_text(draw, (info_x, header_y + idx * LINE_HEIGHT), line, color, FONT)


def main() -> None:
    frames: list[Image.Image] = []
    durations: list[int] = []

    command = "neofetch"
    for index in range(len(command) + 1):
        frame = base_frame()
        draw = ImageDraw.Draw(frame)
        draw_prompt(draw, command[:index], cursor=True)
        frames.append(frame)
        durations.append(55)

    final_frame = base_frame()
    final_draw = ImageDraw.Draw(final_frame)
    draw_prompt(final_draw, command)
    draw_neofetch(final_draw)
    frames.append(final_frame)
    durations.append(10_000)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
    )
    print(f"Generated {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
