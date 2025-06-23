import pandas as pd

# Load each CSV file
rc4_df = pd.read_csv("rc4_8byte_samples.csv")
trivium_df = pd.read_csv("trivium_8byte_samples.csv")
espresso_df = pd.read_csv("espresso_8byte_samples.csv")

# Combine them into one DataFrame
combined_df = pd.concat([rc4_df, trivium_df, espresso_df], ignore_index=True)

# Shuffle the dataset
combined_df = combined_df.sample(frac=1).reset_index(drop=True)

# Save the combined dataset
combined_df.to_csv("all_ciphers_8byte.csv", index=False)

print("✅ Combined dataset saved as 'all_ciphers_8byte.csv'")