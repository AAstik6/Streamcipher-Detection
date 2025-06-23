import pandas as pd

# Load each CSV
rc4_df = pd.read_csv("rc4_24byte.csv")
trivium_df = pd.read_csv("trivium_24byte.csv")
espresso_df = pd.read_csv("espresso_24byte.csv")

# Combine them into one DataFrame
combined_df = pd.concat([rc4_df, trivium_df, espresso_df], ignore_index=True)

# Shuffle the combined dataset
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to final CSV
combined_df.to_csv("all_ciphers_24byte.csv", index=False)

print("✅ Merged and saved to 'all_ciphers_24byte.csv'")