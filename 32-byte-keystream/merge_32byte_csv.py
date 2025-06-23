import pandas as pd

# Load the individual cipher CSVs
rc4_df = pd.read_csv("rc4_32byte.csv")
trivium_df = pd.read_csv("trivium_32byte.csv")
espresso_df = pd.read_csv("espresso_32byte.csv")

# Combine them all into one DataFrame
combined_df = pd.concat([rc4_df, trivium_df, espresso_df], ignore_index=True)

# Shuffle the dataset for randomness
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the combined file
combined_df.to_csv("all_ciphers_32byte.csv", index=False)

print("Merged all into 'all_ciphers_32byte.csv'")