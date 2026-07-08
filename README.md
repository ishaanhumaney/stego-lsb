# StegoLSB

A lightweight, zero-configuration Python utility that hides text data within raw image pixels using Least Significant Bit (LSB) steganography. It injects binary strings directly into the color channels of an image, leaving the visual output completely unchanged to the naked eye.

## How It Works

Every pixel in a standard RGB image consists of three color channels: Red, Green, and Blue. Each channel is represented by an 8-bit integer (0–255). 

StegoLSB alters only the lowest bit—the Least Significant Bit—of these integers to match the bitstream of your secret message. Because modifying this bit changes the color value by a maximum of 1 out of 255, the difference is visually imperceptible. The script appends a hidden null byte delimiter (`00000000`) to mark the end of the text payload, allowing the decoder to extract the exact message and stop reading before scanning extraneous pixel data.

## Key Features

* **Lossless Color Injection:** Modifies LSB values directly across individual RGB channels.
* **Early Stop Detection:** Embedded null-byte delimiter ensures swift message decoding without reading the entire canvas.
* **Self-Contained Pipeline:** Automatically creates temporary testing canvas assets if no seed image is specified.
* **Minimalist Footprint:** Written purely using standard Python loops paired with the `Pillow` library.

## Tech Stack

* **Language:** Python 3.x
* **Core Libraries:** `PIL` (Pillow) for fast, uncompressed pixel-buffer arrays.
* **Environment:** Cross-platform (runs anywhere Python can run).

## Project Structure
```bash
stego-lsb/
├── .github/workflows/
│   └── ci.yml             # Automatic validation and self-test suite
├── Assets/
│   └── .gitkeep           # Target space for input/output images
├── .gitignore             # Filters cache blocks and local test canvases
├── README.md              # Documentation
└── main.py                # Core encoder/decoder runtime engine
```
## Quick Start

-> Option A: Web-Based via GitHub Codespaces (No Local Installation)
  Click the green Code button at the top of this repository.

  Select the Codespaces tab, then click Create codespace on main.

  Once the environment spins up, run the execution script directly in the terminal panel:
    pip install Pillow && python main.py

-> Option B: Local Machine Set Up
-> Install the image processing dependency
pip install Pillow

-> Run the built-in demo execution loop
python main.py

## Usage API
To integrate this directly into your own automation apps, import the encoding and decoding components:
from main import encode_image, decode_image

-> Embed text inside an image
encode_image("my_source.png", "Secret Payload Here", "secured_output.png")

-> Extract text from an image
secret_message = decode_image("secured_output.png")
print(secret_message)

## Roadmap
[ ] Add automated payload compression before embedding to maximize character limits.

[ ] Implement an optional AES-256 encryption layer prior to LSB parsing.

[ ] Introduce support for RGBA alpha-channel bit manipulation.
