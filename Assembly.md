# Assembly
Stitching error corrected reads to prepare continuous long stretches of sequence

As we have aimed at assembling the genome using long reads, we prefer to use [flye](https://github.com/fenderglass/Flye) assembler for contig preparation from the read files. Alternatively Canu can also be used for nanopore reads assembly.
```bash
# Running flye assembler
flye --nano-raw ~/path/to/dir/in/lr.corrected.fa.gz -o ~/path/to/dir/out -t $threads
```
> The output of this assembly is <contigs.fa>.

We further stitch the resulting contigs to prepare long contigs with the help of corrected long reads. We used [LongStitch](https://github.com/bcgsc/LongStitch) for the purpose.
```bash
# Stiching the resulting contigs
contigs=$(~/path/to/dir/in/contigs.fa)
reads=$(~/path/to/dir/in/lr.corrected.fa.gz)
longstitch ntLink-arks draft=contigs.fa reads=$reads out_prefix=$prefix t=$threads G=1e9
```
> The output of this programe is <long.contigs.fa>.

Next we polished the long contigs with the help of error corrected long reads using [medaka](https://github.com/nanoporetech/medaka).
```bash
# Polishing the long contigs using error-corrected long-reads
medaka_consensus -i ~/path/to/dir/in/lr.corrected.fa.gz -d ~/path/to/dir/in/long.contigs.fa \
 -o ~/path/to/dir/out -m r104_e81_hac_g5015 -t $threads
```
> The output of this programe is <consensus.contigs.fa>.

Subsequent polishing with short reads using [Polca](https://github.com/alekseyzimin/masurca), distributed as a part of MaSuRCA genome assembly toolkit.
```bash
# Running polca
polca.sh -a ~/path/to/dir/in/consensus.contigs.fa -r '~/path/to/dir/in/sr.corrected.R1.fq.gz \
 ~/path/to/dir/in/sr.corrected_R2.fq.gz' -t $threads -m 2G
 ```
> The output of this programe is <consensus.pc.contigs.fa>.

Subsequently, the polca corrected contigs were screened for contaminants using [kraken2](https://github.com/DerrickWood/kraken2).
```bash
# Building kraken database

# Running kraken
kraken2 --db $database --threads $threads --output ~/path/to/dir/out/kraken.out --confidence 0.10 \
 --report ~/path/to/dir/out/report.kraken <(dustmasker -in ~/path/to/dir/in/consensus.pc.contigs.fa \
 -outfmt fasta | sed -e '/^>/!s/[atgc]/N/g')

# Extrcating an identified contaminant
extract_kraken_reads.py -k ~/path/to/dir/in/kraken.out -s ~/path/to/dir/in/consensus.pc.contigs.fa -t 953 -r ~/path/to/dir/in/report.kraken \
 --include-children -o ~/path/to/dir/out/wolb.contigs.fa

#Isolating the assembly using an in-house python file
python ~/path/to/dir/in/filter_assembly.py
```
