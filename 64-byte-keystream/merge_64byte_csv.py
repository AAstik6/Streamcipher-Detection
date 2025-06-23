import pandas as pd

# Load individual cipher CSVs
rc4_df = pd.read_csv("rc4_64byte.csv")
trivium_df = pd.read_csv("trivium_64byte.csv")
espresso_df = pd.read_csv("espresso_64byte.csv")

# Combine them
combined_df = pd.concat([rc4_df, trivium_df, espresso_df], ignore_index=True)

# Shuffle the combined dataset
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the merged CSV
combined_df.to_csv("all_ciphers_64byte.csv", index=False)

print("Merged all into 'all_ciphers_64byte.csv'")