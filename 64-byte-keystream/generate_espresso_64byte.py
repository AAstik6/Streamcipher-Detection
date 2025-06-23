import csv
import random

# Convert integer to binary list
def int_to_bitlist(value, length):
    return [int(b) for b in bin(value)[2:].zfill(length)]

# Convert bit list to bytes
def bitlist_to_bytes(bits):
    return [int("".join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8)]

# Initialize ESPRESSO cipher
def espresso_init(key, iv):
    state = [0] * 289
    for i in range(128):
        state[i] = key[i]
    for i in range(128):
        state[i + 128] = iv[i]
    state[256:] = [0] * 33
    return state

# One round of ESPRESSO
def espresso_round(state):
    t = state[286] ^ state[287] ^ state[288]
    feedback = state[235] ^ state[273] ^ (state[230] & state[256])
    state.pop()
    state.insert(0, feedback)
    return t

# Generate one 64-byte keystream
def generate_espresso_keystream():
    key = int_to_bitlist(random.getrandbits(128), 128)
    iv = int_to_bitlist(random.getrandbits(128), 128)
    state = espresso_init(key, iv)

    # Warm-up
    for _ in range(576):
        espresso_round(state)

    # Generate 64 * 8 = 512 bits
    bits = [espresso_round(state) for _ in range(64 * 8)]
    return bitlist_to_bytes(bits)

# Generate and save samples
def generate_espresso_samples():
    total_samples = 131072
    bytes_per_sample = 64
    filename = "espresso_64byte.csv"

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        header = [f"b{i}" for i in range(bytes_per_sample)] + ["label"]
        writer.writerow(header)

        for _ in range(total_samples):
            keystream = generate_espresso_keystream()
            writer.writerow(keystream + ["ESPRESSO"])

    print(f"Saved {total_samples} ESPRESSO samples to '{filename}'")

# Run it
generate_espresso_samples()