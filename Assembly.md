# Assembly
Stitching error corrected reads to prepare continuous long stretches of sequence

As we have aimed at assembling the genome using long reads, we prefer to use [flye](https://github.com/fenderglass/Flye) assembler for contig preparation from the read files. Alternatively Canu can also be used for nanopore reads assembly.
```bash
# Running flye assembler
flye --nano-raw ~/path/to/dir/in/lr.corrected.fa.gz -o ~/path/to/dir/out -t $threads
# The output of this assembly is <contigs.fa>
```
We further stitch the resulting contigs to prepare long contigs with the help of corrected long reads. We used [LongStitch](https://github.com/bcgsc/LongStitch) for the purpose.
```bash
# Stiching the resulting contigs
contigs=$(~/path/to/dir/in/contigs.fa)
reads=$(~/path/to/dir/in/lr.corrected.fa.gz)
longstitch ntLink-arks draft=contigs.fa reads=$reads out_prefix=$prefix t=$threads G=1e9
# The output of this programe is <long.contigs.fa>
```
Next we polished the long contigs with the help of error corrected long reads using [medaka](https://github.com/nanoporetech/medaka).
```bash
# Polishing the long contigs using error-corrected long-reads
medaka_consensus -i ~/path/to/dir/in/lr.corrected.fa.gz -d ~/path/to/dir/in/long.contigs.fa -o ~/path/to/dir/out -m r104_e81_hac_g5015 -t $threads
# The output of this programe is <consensus.contigs.fa>
```
Subsequent polishing with short reads using [Polca](https://github.com/alekseyzimin/masurca).
```bash
polca.sh -a ~/path/to/dir/in/consensus.contigs.fa -r '~/path/to/dir/in/sr.corrected.R1.fq.gz ~/path/to/dir/in/sr.corrected_R2.fq.gz' -t $threads -m 2G
```
