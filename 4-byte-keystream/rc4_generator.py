import random

def KSA(key):
    key = [ord(c) for c in key]  # Convert each letter to its ASCII value
    S = list(range(256))         # Create list [0, 1, 2, ..., 255]
    j = 0

    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]  # Swap

    return S

def PRGA(S, n=8):
    i = 0
    j = 0
    keystream = []

    for _ in range(n):  # Generate 'n' keystream bytes
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]

        t = (S[i] + S[j]) % 256
        keystream.append(S[t])  # Add one byte to keystream

    return keystream

def generate_rc4_keystream_sample(key, n=8):
    S = KSA(key)
    return PRGA(S, n)

if __name__ == "__main__":
    samples = []

    for i in range(131072):
        # Make the key slightly different each time
        key = f"mysecret{i}"
        keystream = generate_rc4_keystream_sample(key, n=8)
        samples.append((keystream, "RC4"))

    # Print first 5 samples to check
    for i in range(5):
        print(f"Sample {i+1}: {samples[i][0]} Label: {samples[i][1]}")


import csv
#save samples to the csv fil
with open("rc4_8byte_samples.csv",mode="w",newline="") as file:
    writer = csv.writer(file)
    # write header
    writer.writerow(["byte1", "byte2", "byte3", "byte4", "byte5", "byte6", "byte7", "byte8", "label"])

    # write each sample
    for sample, label in samples:
        writer.writerow(sample + [label])

print("✅ RC4 samples saved to 'rc4_8byte_samples.csv'")
