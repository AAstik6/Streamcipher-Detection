import csv
import random

# Convert integer to binary list (bit list)
def int_to_bitlist(value, length):
    return [int(b) for b in bin(value)[2:].zfill(length)]

# Convert bit list to byte list
def bitlist_to_bytes(bits):
    return [int("".join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)]

# ESPRESSO cipher initialization
def espresso_init(key, iv):
    state = [0] * 289
    for i in range(128):
        state[i] = key[i]
    for i in range(128):
        state[i + 128] = iv[i]
    state[256:] = [0] * 33
    return state

# ESPRESSO update function (one round)
def espresso_round(state):
    t = state[286] ^ state[287] ^ state[288]
    feedback = state[235] ^ state[273] ^ (state[230] & state[256])
    state.pop()
    state.insert(0, feedback)
    return t

# Generate 32-byte ESPRESSO keystream (256 bits)
def generate_espresso_keystream():
    key = int_to_bitlist(random.getrandbits(128), 128)
    iv = int_to_bitlist(random.getrandbits(128), 128)
    state = espresso_init(key, iv)

    bits = []
    # Warm-up (discard initial bits)
    for _ in range(576):
        espresso_round(state)
    for _ in range(256):  # 32 bytes = 256 bits
        bits.append(espresso_round(state))
    return bitlist_to_bytes(bits)

# Generate and save all samples
def generate_espresso_samples():
    total_samples = 131072
    bytes_per_sample = 32
    filename = "espresso_32byte.csv"

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write header: b0 to b31 + label
        header = [f"b{i}" for i in range(bytes_per_sample)] + ["label"]
        writer.writerow(header)

        for _ in range(total_samples):
            keystream = generate_espresso_keystream()
            writer.writerow(keystream + ["ESPRESSO"])

    print(f"✅ Done! Saved {total_samples} ESPRESSO samples to '{filename}'")

# Run it
generate_espresso_samples()