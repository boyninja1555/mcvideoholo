import sys
import os
import cv2
import json

INPUT_FILE = "input.mp4"
OUTPUT_DIR = "output"
WIDTH = 32
HEIGHT = 18

if not os.path.isfile(INPUT_FILE):
    print(f"{INPUT_FILE} is missing!")
    sys.exit(1)

if os.path.exists(OUTPUT_DIR):
    for root, dirs, files in os.walk(OUTPUT_DIR, topdown=False):
        for f in files:
            os.remove(os.path.join(root, f))
        for d in dirs:
            os.rmdir(os.path.join(root, d))
else:
    os.makedirs(OUTPUT_DIR)


def resize(frame):
    return cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)


def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"


def pixel_color(bgr):
    b, g, r = bgr
    return rgb_to_hex(r, g, b)


def frame_to_compressed_lines(frame):
    lines = []
    for y in range(HEIGHT):
        row = frame[y]
        components = []
        prev_color = None
        buffer = []
        for x in range(WIDTH):
            color = pixel_color(row[x])
            if color == prev_color:
                buffer.append("█")
            else:
                if buffer:
                    components.append({"text": "".join(buffer), "color": prev_color})

                buffer = ["█"]
                prev_color = color

        if buffer:
            components.append({"text": "".join(buffer), "color": prev_color})

        lines.append(components)

    return lines


def json_line(line):
    return json.dumps(line, separators=(",", ":"))


cap = cv2.VideoCapture(INPUT_FILE)
frame_index = 0
setup_path = os.path.join(OUTPUT_DIR, "setup.mcfunction")
cleanup_path = os.path.join(OUTPUT_DIR, "cleanup.mcfunction")

with (
    open(setup_path, "w", encoding="utf-8") as setup,
    open(cleanup_path, "w", encoding="utf-8") as cleanup,
):
    setup.write("# Setup\n")
    cleanup.write("# Cleanup\n")
    for i in range(HEIGHT):
        setup.write(
            f'summon armor_stand ~ ~{"" if i == 0 else i} ~ {{Tags:["mcvideo{i}"],NoGravity:true}}\n'
        )

        cleanup.write(f"kill @e[type=armor_stand,tag=mcvideo{i}]\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = resize(frame)
    lines = frame_to_compressed_lines(frame)
    frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame_index:04d}.mcfunction")
    with open(frame_path, "w", encoding="utf-8") as f:
        f.write(f"# Frame {frame_index}\n")
        for i, line in enumerate(lines):
            json_text = json_line(line)
            cmd = (
                "data modify entity "
                f"@e[type=armor_stand,tag=mcvideo{i},limit=1] "
                f"CustomName set value {json_text}"
            )

            f.write(cmd + "\n")

    frame_index += 1

cap.release()
print(f"Done! {frame_index} frames -> {OUTPUT_DIR}/")
