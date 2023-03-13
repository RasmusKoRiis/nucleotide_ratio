#!/bin/bash

sample1="10P1"
sample2="10P2"
sample3="10P3"


for file in bam-files/*bam; do
    bam_name=$(basename $file .bam)
    /workspace/nucleotide_ratio/bam-readcount/build/bin/bam-readcount -w1 $file > results/"$bam_name"_raw.tsv
done

for depth_file in results/*raw.tsv; do  
    bam_name=$(basename $depth_file .sorted_raw.tsv)
    python3 mutation_ratio_finder.py $depth_file results/"$bam_name"_processed_raw.csv $bam_name
done

# 3 Samples
#python3 table_merger.py results/"$sample1"_processed_raw.csv results/"$sample2"_processed_raw.csv results/"$sample3"_processed_raw.csv  "results/merged_tabel.csv"

#2 Samples
python3 table_merger_2.py "results/10P1_processed_raw.csv" "results/10P2_processed_raw.csv"  "results/merged_tabel.csv"







