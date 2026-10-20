import os
import random
import subprocess
import tempfile
from pathlib import Path

PHOTOS_DIR = Path(__file__).parent.parent / "website" / "Photos"

# Curated list of the best shots for social
FEATURED = [
    "jbp-web-ROADLESSTRAVELED-80.jpg",
    "jbp-web-ROADLESSTRAVELED-85.jpg",
    "jbp-web-ROADLESSTRAVELED-3.jpg",
    "jbp-web-ROADLESSTRAVELED-10.jpg",
    "jbp-web-ROADLESSTRAVELED-30.jpg",
    "jbp-web-ROADLESSTRAVELED-15.jpg",
    "jbp-web-ROADLESSTRAVELED-20.jpg",
    "jbp-web-ROADLESSTRAVELED-25.jpg",
    "jbp-web-ROADLESSTRAVELED-40.jpg",
    "jbp-web-ROADLESSTRAVELED-5.jpg",
    "jbp-web-ROADLESSTRAVELED-55.jpg",
    "jbp-web-ROADLESSTRAVELED-90.jpg",
    "jbp-web-ROADLESSTRAVELED-60.jpg",
    "jbp-web-ROADLESSTRAVELED-70.jpg",
    "jbp-web-ROADLESSTRAVELED-45.jpg",
    "jbp-web-ROADLESSTRAVELED-50.jpg",
]

CLIP_DURATION = 4    # seconds per photo
TRANSITION    = 1    # seconds for crossfade
WIDTH         = 1080
HEIGHT        = 1920 # 9:16 for Reels


def pick_photos(n: int = 6) -> list[Path]:
    pool = [PHOTOS_DIR / f for f in FEATURED if (PHOTOS_DIR / f).exists()]
    if len(pool) < n:
        # backfill from all photos if needed
        all_photos = sorted(PHOTOS_DIR.glob("*.jpg"))
        pool = list(set(pool) | set(all_photos))
    return random.sample(pool, min(n, len(pool)))


def build_reel(output_path: str, photos: list[Path] = None) -> str:
    """
    Assembles a vertical Reel from a list of photos using FFmpeg.
    Returns the path to the output MP4.
    """
    if photos is None:
        photos = pick_photos(6)

    # Build FFmpeg filter graph: scale + crop to 9:16, Ken Burns zoom, crossfade
    inputs = []
    for p in photos:
        inputs += ["-loop", "1", "-t", str(CLIP_DURATION + TRANSITION), "-i", str(p)]

    n = len(photos)
    filter_parts = []

    # Scale and crop each input to 1080x1920
    for i in range(n):
        filter_parts.append(
            f"[{i}:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            f"zoompan=z='min(zoom+0.0008,1.05)':d={CLIP_DURATION * 25}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps=25,"
            f"setpts=PTS-STARTPTS,fps=25[v{i}];"
        )

    # Chain crossfades
    if n == 1:
        filter_parts.append(f"[v0]format=yuv420p[out]")
    else:
        # First transition
        filter_parts.append(
            f"[v0][v1]xfade=transition=fade:duration={TRANSITION}:"
            f"offset={CLIP_DURATION}[xf0];"
        )
        for i in range(1, n - 1):
            offset = (i + 1) * CLIP_DURATION + i * TRANSITION
            prev   = f"xf{i-1}" if i > 1 else "xf0"
            if i == 1:
                prev = "xf0"
            filter_parts.append(
                f"[{prev}][v{i+1}]xfade=transition=fade:duration={TRANSITION}:"
                f"offset={offset}[xf{i}];"
            )
        last = f"xf{n-2}"
        filter_parts.append(f"[{last}]format=yuv420p[out]")

    filter_complex = "".join(filter_parts)

    cmd = (
        ["ffmpeg", "-y"]
        + inputs
        + [
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "28",
            "-an",
            "-movflags", "+faststart",
            output_path,
        ]
    )

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


if __name__ == "__main__":
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        out = f.name
    build_reel(out)
    print(f"Reel saved to: {out}")
