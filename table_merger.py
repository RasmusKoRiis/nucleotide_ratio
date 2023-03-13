import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import *

sample01 = sys.argv[1]
sample02 = sys.argv[2]
sample03 = sys.argv[3]
output_file = sys.argv[4]

# load the three CSV files into DataFrames
df1 = pd.read_csv(sample01)
df2 = pd.read_csv(sample02)
df3 = pd.read_csv(sample03)

# merge the three DataFrames on the 'base_position' column
merged_df = pd.merge(df1, df2, on='base_position')
merged_df = pd.merge(merged_df, df3, on='base_position')

# calculate absolute difference between nucleotides
merged_df['adenine_diff'] = abs(merged_df['adenine_x'] - merged_df['adenine_y'])
merged_df['guanine_diff'] = abs(merged_df['guanine_x'] - merged_df['guanine_y'])
merged_df['thymine_diff'] = abs(merged_df['thymine_x'] - merged_df['thymine_y'])
merged_df['cytosine_diff'] = abs(merged_df['cytosine_x'] - merged_df['cytosine_y'])

# filter rows where the difference is greater than 0.1
merged_df = merged_df[(merged_df[['adenine_diff', 'cytosine_diff', 'guanine_diff', 'thymine_diff']] > 0.09).any(axis=1)]

# reshape the data so each sample's adenine, cytosine, guanine, and thymine values are in separate columns
melted_df = pd.melt(merged_df, id_vars=['base_position', 'sample_x', 'sample_y', 'sample'], value_vars=['adenine_x', 'cytosine_x', 'guanine_x', 'thymine_x', 'adenine_y', 'cytosine_y', 'guanine_y', 'thymine_y', 'adenine', 'cytosine', 'guanine', 'thymine'], var_name='value_vars', value_name='nucleotide')

# add a new column called sample2 based on the value in the value_vars column
melted_df['sample2'] = melted_df.apply(lambda x: x['sample_x'] if x['value_vars'].endswith('_x') else (x['sample_y'] if x['value_vars'].endswith('_y') else x['sample']), axis=1)

# drop the sample_x, sample_y, and sample columns
melted_df.drop(columns=['sample_x', 'sample_y', 'sample'], inplace=True)

melted_df["value_vars"] = melted_df["value_vars"].str.replace("_x", "").str.replace("_y", "")

print(melted_df)

base_positions = melted_df['base_position'].unique()

import math

# Calculate the number of rows and columns needed for the mosaic
num_charts = len(base_positions)
num_cols = int(math.sqrt(num_charts))
num_rows = math.ceil(num_charts / num_cols)

# Create a figure with a grid of subplots for the mosaic
fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(12, 12))

# Flatten the grid of subplots into a 1D array
axes = axes.flatten()

# Create an empty list for the legend handles and labels
legend_handles = []
legend_labels = []

# Loop through each base position and create a stacked bar chart in a subplot
for i, base_pos in enumerate(base_positions):
    # Get data for current base position
    df_bp = melted_df[melted_df['base_position'] == base_pos]
    
    # Pivot data for stacked bar chart
    df_pivot = df_bp.pivot(index='sample2', columns='value_vars', values='nucleotide')
    
    # Create stacked bar chart in a subplot
    ax = df_pivot.plot(kind='bar', stacked=True, figsize=(8,6), ax=axes[i])
    ax.set_title(f"Base Position {base_pos}")
    ax.set_xlabel('Sample ID')
    ax.set_ylabel('Nucleotide Ratio')
    
    # Remove the legend from the subplot
    ax.get_legend().remove()
    
   

# Adjust the spacing between subplots
plt.tight_layout()
plt.legend(["adenine" , "thymine","cytosine", "guanine" ], loc= 'lower left')



# Save the mosaic in a file
plt.savefig('mosaic.png')

