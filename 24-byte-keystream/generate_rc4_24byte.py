import csv
import random

# RC4 Key Scheduling Algorithm
def KSA(key):
    key = [ord(char) for char in key]
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

# RC4 Pseudo-Random Generation Algorithm
def PRGA(S, num_bytes):
    i = j = 0
    stream = []
    while len(stream) < num_bytes:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        stream.append(K)
    return stream

# Main generator function
def generate_rc4_keystreams():
    total_samples = 131072
    bytes_per_sample = 24
    filename = "rc4_24byte.csv"

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write header row: b0, b1, ..., b23, label
        header = [f"b{i}" for i in range(bytes_per_sample)] + ["label"]
        writer.writerow(header)

        # Write 2^17 rows of 24-byte keystream + label
        for _ in range(total_samples):
            key = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8))
            S = KSA(key)
            keystream = PRGA(S, bytes_per_sample)
            writer.writerow(keystream + ["RC4"])

    print(f"✅ Done! Saved {total_samples} samples to '{filename}' with header.")

# Run the generator
generate_rc4_keystreams()