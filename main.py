import sys
import os
import cv2
import json

INPUT_FILE = "input.mp4"
OUTPUT_FILE = "output.mcfunction"
WIDTH = 32
HEIGHT = 18

if not os.path.isfile(INPUT_FILE):
    print(f"{INPUT_FILE} is missing!")
    sys.exit(1)

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)


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

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = resize(frame)
        lines = frame_to_compressed_lines(frame)
        f.write(f"# Frame {frame_index}\n")
        for i, line in enumerate(lines):
            json_text = json_line(line)
            cmd = (
                f"data modify entity @e[type=armor_stand,limit=1,sort=nearest] "
                f'CustomName set value {json_text}'
            )

            f.write(cmd + "\n")

        frame_index += 1

cap.release()
print(f"Done! {frame_index} frames -> {OUTPUT_FILE}")
