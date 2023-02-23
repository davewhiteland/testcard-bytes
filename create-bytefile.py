from PIL import Image
import re

INPUT_IMAGE_FILENAME = "testcard.png"
OUTPUT_FILENAME = "testcard.jonty"
TEST_PNG_FILENAME = "output-test.png"
DEFAULT_MAX_X = 504
DEFAULT_MAX_Y = 377
DEFAULT_OUTPUT_FILENAME = "output"
BYTE_FILE_EXTENSION = ".jonty"
FILENAME_RE = re.compile(r"([A-Za-z_]+)")

print(f"[?] source image (testcard) filename: [{INPUT_IMAGE_FILENAME}]\n> ", end="")
source_filename = input().strip() or INPUT_IMAGE_FILENAME
testcard = Image.open(source_filename)
width, height = testcard.size
print(f"[ ] source image dimensions are {width} x {height}")

print(f"[?] target width in pixels (x)? [{DEFAULT_MAX_X}]\n> ", end="")
input_str = input().strip()
max_x = int(input_str) if input_str.isdigit() else DEFAULT_MAX_X

print(f"[?] target height in pixels (y)? [{DEFAULT_MAX_Y}]\n> ", end="")
input_str = input().strip()
max_y = int(input_str) if input_str.isdigit() else DEFAULT_MAX_Y

print(f"[?] want interlaced? [Y/n]\n> ", end="")
is_interlaced = f"{input().strip().lower()}y".startswith("y")

print(f"[?] Want 8-byte greyscale values? [Y/n]\n> ", end="")
# note: default is 8-byte, so negate that answer for 7-byte
is_7_byte = not f"{input().strip().lower()}y".startswith("y")

output_filename = ""
if match := re.match(FILENAME_RE, source_filename):
  output_filename = f"{match.group(1)}"
else:
  output_filename = DEFAULT_OUTPUT_FILENAME
output_filename += f"-{max_x}-x-{max_y}"
if is_interlaced: output_filename += "-i"
if is_7_byte: output_filename += "-7byte"
output_filename += BYTE_FILE_EXTENSION
print(f"[?] output filename? [{output_filename}]\n> ", end="")
output_filename = input().strip() or output_filename 

if width != max_x or height != max_y:
    testcard = testcard.resize((max_x, max_y), resample=Image.BICUBIC)
    print(f"[!] resized image to {max_x} x {max_y}")

y_numbers = [i for i in range(max_y)]
if is_interlaced:
    y_numbers = [i for i in y_numbers if not i%2] + \
                [i for i in y_numbers if i%2]
min = 127 if is_7_byte else 255
max = 0
qty_pixels = 0
text_filename = output_filename.rsplit(".", 1)[0]+".txt"

outfile = open(output_filename, "wb")
textfile = open(text_filename, "w")
for y in y_numbers:
    for x in range(max_x):
        pixel = testcard.getpixel((x, y))
        grey = int((pixel[0] + pixel[1] + pixel[2])/3)
        if is_7_byte: grey = int(grey/2)
        if grey > max: max = grey
        if grey < min: min = grey
        outfile.write(grey.to_bytes(1, "big"))
        textfile.write(hex(grey).replace('0x', '').zfill(2)+"\n")
outfile.close()
textfile.close()
print(
  f"[ ] wrote {output_filename} ({qty_pixels} bytes: "
  f"min={int(min)}, max={max}){'' if is_interlaced else ' not'} interlaced"
)
print(f"[ ] wrote {text_filename} text/hex file too")

# now test that by reading the bytes back and producing a PNG
greenscreen = (0, 255, 0 , 255)
img = Image.new('RGB', (max_x, max_y), greenscreen)
pixels = img.load()
with open(output_filename, "rb") as infile:
    try:
        for y in y_numbers:
            for x in range(max_x):
                if byte := infile.read(1):
                    grey = int.from_bytes(byte, "big")
                    pixels[x, y] = (grey, grey, grey)
                else:
                    raise ValueError(
                      f"No more bytes to read from {OUTPUT_FILENAME} "
                      f"(got to ({x}, {y})"
                    )
    except ValueError as e:
      print(f"[!] error: {e}")              
img.save(TEST_PNG_FILENAME)
print(f"[ ] created {TEST_PNG_FILENAME} from that, for sanity-check")
print("[ ] done\n")