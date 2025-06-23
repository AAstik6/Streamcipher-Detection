import csv
import random

# Convert integer to list of bits
def int_to_bitlist(value, length):
    return [int(b) for b in bin(value)[2:].zfill(length)]

# Convert bit list to list of bytes (8 bits per byte)
def bitlist_to_bytes(bits):
    return [int("".join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)]

# Initialize TRIVIUM cipher with key and IV
def trivium_init(key, iv):
    state = [0]*288

    # Load key (80 bits)
    for i in range(80):
        state[i] = key[i]
    # Load IV (80 bits)
    for i in range(80):
        state[i + 93] = iv[i]
    # Set last 3 bits to 1
    state[285], state[286], state[287] = 1, 1, 1

    # Warm-up: discard first 4*288 outputs
    for _ in range(4 * 288):
        trivium_round(state)

    return state

# One round of TRIVIUM update
def trivium_round(state):
    t1 = state[65] ^ state[92]
    t2 = state[161] ^ state[176]
    t3 = state[242] ^ state[287]

    z = t1 ^ t2 ^ t3

    t1 = t1 ^ (state[90] & state[91]) ^ state[170]
    t2 = t2 ^ (state[174] & state[175]) ^ state[263]
    t3 = t3 ^ (state[285] & state[286]) ^ state[68]

    # Shift state
    state.pop()
    state.insert(0, t3)
    state[93] = t1
    state[177] = t2

    return z

# Generate one 32-byte keystream sample
def generate_trivium_keystream():
    key = int_to_bitlist(random.getrandbits(80), 80)
    iv = int_to_bitlist(random.getrandbits(80), 80)
    state = trivium_init(key, iv)

    bits = [trivium_round(state) for _ in range(32 * 8)]  # 32 bytes = 256 bits
    return bitlist_to_bytes(bits)

# Write all samples to CSV
def generate_trivium_samples():
    total_samples = 131072
    bytes_per_sample = 32
    filename = "trivium_32byte.csv"

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        # Header row
        header = [f"b{i}" for i in range(bytes_per_sample)] + ["label"]
        writer.writerow(header)

        for _ in range(total_samples):
            keystream = generate_trivium_keystream()
            writer.writerow(keystream + ["TRIVIUM"])

    print(f"Saved {total_samples} TRIVIUM samples to '{filename}'")

# Run it
generate_trivium_samples()