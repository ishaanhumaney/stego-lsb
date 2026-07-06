import os
from PIL import Image

def text_to_bin(text):
    # Convert text to a string of binary bits, adding a null byte at the end as a delimiter
    return ''.join(format(ord(c), '08b') for c in text) + '00000000'

def bin_to_text(bin_str):
    # Read 8 bits at a time and convert back to characters until we hit the null byte
    chars = []
    for i in range(0, len(bin_str), 8):
        byte = bin_str[i:i+8]
        if byte == '00000000' or len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def encode_image(img_path, secret_text, output_path):
    if not os.path.exists(img_path):
        print(f"Error: Image not found at {img_path}")
        return

    img = Image.open(img_path).convert('RGB')
    pixels = img.load()
    width, height = img.size
    
    bin_msg = text_to_bin(secret_text)
    msg_idx = 0
    msg_len = len(bin_msg)

    for y in range(height):
        for x in range(width):
            if msg_idx >= msg_len:
                img.save(output_path)
                print(f"Success: Message hidden in {output_path}")
                return
            
            r, g, b = pixels[x, y]
            
            # Modify the LSB of each color channel if we still have bits to hidepng
            if msg_idx < msg_len:
                r = (r & ~1) | int(bin_msg[msg_idx])
                msg_idx += 1
            if msg_idx < msg_len:
                g = (g & ~1) | int(bin_msg[msg_idx])
                msg_idx += 1
            if msg_idx < msg_len:
                b = (b & ~1) | int(bin_msg[msg_idx])
                msg_idx += 1
                
            pixels[x, y] = (r, g, b)

    print("Error: Image is too small to hold the entire message.")

def decode_image(img_path):
    if not os.path.exists(img_path):
        print(f"Error: Image not found at {img_path}")
        return

    img = Image.open(img_path).convert('RGB')
    pixels = img.load()
    width, height = img.size
    
    bin_str = ""
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            bin_str += str(r & 1)
            bin_str += str(g & 1)
            bin_str += str(b & 1)
            
            # Check if we've found our null byte delimiter to stop early
            if len(bin_str) >= 8 and bin_str[-8:] == '00000000':
                return bin_to_text(bin_str)
                
    return bin_to_text(bin_str)

if __name__ == '__main__':
    # Quick test run
    original_img = "Assets/input.png"  # Drop a real png here to test
    encoded_img = "Assets/hidden.png"
    secret = "Meet me at the coffee shop at 0900. Passcode: BlueFalcon."
    
    # Create a dummy image for testing if you don't have one handy
    if not os.path.exists(original_img):
        Image.new('RGB', (300, 300), color='blue').save(original_img)
        print(f"Created a temporary {original_img} for testing.")

    encode_image(original_img, secret, encoded_img)
    
    decoded_message = decode_image(encoded_img)
    print(f"Decoded Message: {decoded_message}")
