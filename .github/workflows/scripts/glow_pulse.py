#!/usr/bin/env python3
import math
import argparse
from PIL import Image, ImageEnhance, ImageFilter, ImageChops, ImageDraw

def fit_square(img, size):
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ratio = min(size / img.width, size / img.height)
    new_w = int(img.width * ratio)
    new_h = int(img.height * ratio)
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    x = (size - new_w) // 2
    y = (size - new_h) // 2
    canvas.paste(img, (x, y), img if img.mode == "RGBA" else None)
    return canvas

def circular_mask(size, feather=2):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((feather, feather, size - feather, size - feather), fill=255)
    if feather > 0:
        m = m.filter(ImageFilter.GaussianBlur(feather))
    return m

def make_frames(base, frames=40, fps=20, base_blur=3.0, pulse_blur=6.0,
                pulse_bright=0.35, max_rotate=2.0, keep_circle=False):
    W, H = base.size
    mask = circular_mask(min(W, H), feather=2) if keep_circle else None
    out_frames = []
    for i in range(frames):
        t = i / frames
        bright = 1.0 + pulse_bright * math.sin(2 * math.pi * t)
        blur_radius = base_blur + pulse_blur * (0.5 + 0.5 * math.sin(2 * math.pi * t))
        angle = max_rotate * math.sin(2 * math.pi * t)
        frame = ImageEnhance.Brightness(base).enhance(bright)
        glow = frame.filter(ImageFilter.GaussianBlur(blur_radius))
        composed = ImageChops.screen(frame.convert("RGB"), glow.convert("RGB")).convert("RGBA")
        composed = composed.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
        if mask is not None:
            alpha = composed.getchannel("A")
            alpha = ImageChops.multiply(alpha, mask)
            composed.putalpha(alpha)
        pal = composed.convert("P", palette=Image.ADAPTIVE, colors=128, dither=Image.FLOYDSTEINBERG)
        out_frames.append(pal)
    duration_ms = int(1000 / fps)
    return out_frames, duration_ms

def main():
    parser = argparse.ArgumentParser(description="Neon-Glow-Animation als Discord-Style GIF.")
    parser.add_argument("--in", dest="inp", default="assets/logo.png", help="Eingabebild (PNG empfohlen).")
    parser.add_argument("--out", dest="out", default="build/discord_logo.gif", help="Ausgabedatei (GIF).")
    parser.add_argument("--size", type=int, default=512, help="Quadratische Zielgröße (z.B. 512).")
    parser.add_argument("--frames", type=int, default=40, help="Anzahl Frames pro Loop.")
    parser.add_argument("--fps", type=int, default=20, help="Framerate.")
    parser.add_argument("--base-blur", type=float, default=3.0, help="Basis-Glow (px).")
    parser.add_argument("--pulse-blur", type=float, default=6.0, help="Zusätzlicher Glow durch Puls (px).")
    parser.add_argument("--pulse-bright", type=float, default=0.35, help="Helligkeitspuls-Amplitude (0..1).")
    parser.add_argument("--max-rotate", type=float, default=2.0, help="Max. Wipp-Rotation (Grad).")
    parser.add_argument("--keep-circle", action="store_true", help="Runder transparenter Zuschnitt (Discord-Icon Stil).")
    args = parser.parse_args()

    img = Image.open(args.inp).convert("RGBA")
    base = fit_square(img, args.size)
    frames, duration = make_frames(
        base,
        frames=args.frames,
        fps=args.fps,
        base_blur=args.base_blur,
        pulse_blur=args.pulse_blur,
        pulse_bright=args.pulse_bright,
        max_rotate=args.max_rotate,
        keep_circle=args.keep_circle,
    )
    frames[0].save(
        args.out,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        disposal=2,
        optimize=True,
    )
    print(f"Fertig -> {args.out}")

if __name__ == "__main__":
    main()
