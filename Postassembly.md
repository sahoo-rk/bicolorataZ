# Postassembly

Assessing the draft assembly and correcting it, if necessary.

We first assessed assembly statistics using [Quast](https://github.com/ablab/quast) and seqstat from [genometools](https://github.com/genometools/genometools).
```bash
quast.py -t $threads --x-for-Nx 90 ~/path/to/dir/in/draft.assembly.fa --pe1 ~/path/to/dir/in/sr.corrected.R1.fastq \ 
 --pe2 ~/path/to/dir/in/sr.corrected.R2.fastq -o ~/path/to/dir/out
 
seqstat -contigs -genome 1200000000 ~/path/to/dir/in/draft.assembly.fa > assembly.stats
 ```
 We, then, checked the assembly completeness in reference to single copy orthologs databse using busco.
 ```bash
busco -i ~/path/to/dir/in/draft.assembly.fa --out_path ~/path/to/dir/out -o $prefix -l ~/path/to/dir/out/endopterygota_odb10 \
 -m genome --offline -c $threads --download_path ./busco_downloads
```
We used [merqury](https://github.com/marbl/merqury) to check k-mer distribution in the assembly with respect to that of in the sequence reads.
```bash
$MERQURY/merqury.sh ../illumina.meryl /home/sahoork/beetle/analysis/assembly/HYD23.draft.assembly.fasta illumina.merqury
```
