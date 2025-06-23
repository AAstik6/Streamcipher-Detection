def int_to_bitlist(value, length):
    return [int(b) for b in bin(value)[2:].zfill(length)]

def bitlist_to_bytes(bits):
    # Convert bits to list of 8-bit integers (bytes)
    return [int("".join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)] # This groups the bits into 8s and converts each group back into a number.

def trivium_init(key, iv):
    # Convert key and iv to 80-bit binary list
    key_bits = int_to_bitlist(int(key, 16), 80)
    iv_bits = int_to_bitlist(int(iv, 16), 80)

    state = [0] * 288

    # Load key
    for i in range(80):
        state[i] = key_bits[i]

    # Load IV
    for i in range(80):
        state[i + 93] = iv_bits[i]

    # Final bits as per TRIVIUM spec
    state[285] = 1
    state[286] = 1
    state[287] = 1

    # Warm-up: 4 × 288 = 1152 cycles
    for _ in range(4 * 288):
        t1 = state[65] ^ (state[90] & state[91]) ^ state[92] ^ state[170]
        t2 = state[161] ^ (state[174] & state[175]) ^ state[176] ^ state[263]
        t3 = state[242] ^ (state[285] & state[286]) ^ state[287] ^ state[68]

        state = [t3] + state[:92] + [t1] + state[93:176] + [t2] + state[177:287]

    return state

def trivium_generate_keystream(state, num_bits=64):
    output = []

    for _ in range(num_bits):
        t1 = state[65] ^ state[92]
        t2 = state[161] ^ state[176]
        t3 = state[242] ^ state[287]

        z = t1 ^ t2 ^ t3
        output.append(z)

        t1 = t1 ^ (state[90] & state[91]) ^ state[170]
        t2 = t2 ^ (state[174] & state[175]) ^ state[263]
        t3 = t3 ^ (state[285] & state[286]) ^ state[68]

        state = [t3] + state[:92] + [t1] + state[93:176] + [t2] + state[177:287]

    return output

def generate_trivium_keystream_sample(key_hex, iv_hex, byte_length=8):
    bit_length = byte_length * 8  # e.g., 8 bytes = 64 bits
    state = trivium_init(key_hex, iv_hex)
    keystream_bits = trivium_generate_keystream(state, num_bits=bit_length)
    return bitlist_to_bytes(keystream_bits)

import csv
import random

samples = []

for i in range(131072):
    key = "%020x" % random.getrandbits(80)
    iv = "%020x" % random.getrandbits(80)
    keystream = generate_trivium_keystream_sample(key, iv, byte_length=8)
    samples.append((keystream, "TRIVIUM"))

    if i % 10000 == 0:
        print(f"Generated {i} samples...")

# Save to CSV
with open("trivium_8byte_samples.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["byte1", "byte2", "byte3", "byte4", "byte5", "byte6", "byte7", "byte8", "label"])
    for sample, label in samples:
        writer.writerow(sample + [label])

print("✅ TRIVIUM samples saved to 'trivium_8byte_samples.csv'")