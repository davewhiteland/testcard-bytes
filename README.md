# testcard-bytes

Accepts any image (the "source") and produces a ".jonty" file containing
greyscale bytes (0=black, 127=50% grey, 255=white) for a given height
and width (the "target" size).

The bytes are written in order row by row, and may be interlaced (odd rows
first, then even rows). The _only_ bytes in the file are the greyscale data:
no other markers or data.

Used as a testcard for a simple TV :-)

## Suggested installation

```bash
# make a virtual environment
python -m venv venv

# activate it
source venv/bin/activate

# install pillow
pip install pillow

# run the script
python create-bytefile.py
```
