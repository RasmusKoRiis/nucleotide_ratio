import pandas as pd
import sys

depth_file = sys.argv[1]
output_file = sys.argv[2]
sample_name = sys.argv[3]


# Load the tab-separated file
df = pd.read_csv(depth_file , sep='\t')

# Define the header
header = ['Ref_Name', 'base_position', 'a', 'depth', 'b', 'adenine', 'cytosine', 'guanine', 'thymine', 'none']

# Read the TSV file into a Pandas DataFrame with the specified header
df = pd.read_csv(depth_file, delimiter='\t', header=None, names=header)

# Select specific columns
df = df.iloc[:, [0, 1, 3, 5, 6, 7, 8, 9]]

for col in range(3, 8):
    df.iloc[:, col] = df.iloc[:, col].str.split(':').str[1]

cols_to_convert = ["adenine", "thymine", "cytosine", "guanine"]
df[cols_to_convert] = df[cols_to_convert].astype(float)

df[['adenine', 'thymine', 'cytosine', 'guanine']] = df[['adenine', 'thymine', 'cytosine', 'guanine']].div(df['depth'], axis=0)

# Add a new column filled with a variable name
df['sample'] = sample_name

# Save the updated DataFrame as a CSV file
df.to_csv(output_file, index=False)

