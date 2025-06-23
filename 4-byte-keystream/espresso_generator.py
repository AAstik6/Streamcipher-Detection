import random

def rotate_left(x, shift, width=128):
    return ((x << shift) & ((1 << width) - 1)) | (x >> (width - shift))

def espresso_keystream(key, iv, num_bytes=8):
    # Key and IV are integers
    state = key ^ iv
    keystream = []

    for _ in range(num_bytes):
        # Simulate transformation (very simplified)
        state = rotate_left(state, 7)
        state ^= (state >> 3) ^ (state >> 17)
        keystream.append(state & 0xFF)  # Take the lowest 8 bits as a byte

    return keystream

import csv

samples = []

for _ in range(131072):
    key = random.getrandbits(128)  # ESPRESSO uses 128-bit key
    iv = random.getrandbits(128)   # 128-bit IV
    keystream = espresso_keystream(key, iv, num_bytes=8)
    samples.append((keystream, "ESPRESSO"))

# Save to CSV
with open("espresso_8byte_samples.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["byte1", "byte2", "byte3", "byte4", "byte5", "byte6", "byte7", "byte8", "label"])
    for sample, label in samples:
        writer.writerow(sample + [label])

print("✅ ESPRESSO samples saved to 'espresso_8byte_samples.csv'")