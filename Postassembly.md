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
We used [merqury](https://github.com/marbl/merqury) to check k-mer distribution in the assembly with respect to that in the sequence reads.
```bash
$MERQURY/merqury.sh ../illumina.meryl /home/sahoork/beetle/analysis/assembly/HYD23.draft.assembly.fasta illumina.merqury
```
As our results from BUSCO and MERQURY indicate for the presence significant levels of duplicatin in the draft assembly, we aimed at purging those duplicate regions with the help of [purge.dups](https://github.com/dfguan/purge_dups).
```bash
# Indexing, splitting & self-mapping the draft assembly
minimap2 -t $threads -k 20 -d ./draft.mm2.index ~/path/to/dir/in/draft.assembly.fa
split_fa ~/path/to/dir/in/draft.assembly.fa > draft.assembly.fa.split
minimap2 -x asm5 -DP -t $threads draft.assembly.fa.split draft.assembly.fa.split | gzip -c - > draft.split.self.paf.gz
```
> The resulting ```draft.split.self.paf.gz``` will be used to prepare the ```.bed``` file at the purging step.
```bash
# Mapping nanopore long reads to the draft assembly & checking the base coverage
minimap2 -t $threads -x map-ont ./draft.mm2.index ~/path/to/dir/in/lr.corrected.fa.gz | gzip -c - > draft.lr.map.paf.gz
pbcstat draft.lr.map.paf.gz        # outputs are PB.base.cov & PB.stat files
calcuts PB.stat > cutoffs.default 2> calcults.log
scripts/hist_plot.py -c cutoffs.default PB.stat PB.coverage.default.png
```
We can now check how the determined cutoff values are positioned across the base coverage graph. This step is essential as the cutoff values assigned at this step will be used to purge the duplications from the draft assembly. To make sure that we are using the right cutoffs, we manually 
```bash
# Manually setting the cutoffs
for i in {1,2,3,4,5}
do
 calcuts -l {a} -m {b} -u {c} PB.stat > cutoffs.m$i
 (m1: a=2, b=21, c=220; m2: a=1, b=21, c=220; m3: a=1, b=17, c=220; m4: a=1, b=21, c=500; m5: a=1, b=21, c=501)
 scripts/hist_plot.py -c cutoffs.m$i PB.stat PB.coverage.m$i.png
done
```

```bash
# Purging the assembly
purge_dups -2 -T cutoffs.m$i -c PB.base.cov ./draft.split.self.paf.gz > dups.m$i.bed 2> purge_dups.m$i.log
get_seqs -l 500 -e dups.m$i.bed ./draft.assembly.fa -p draft.m$i.endpurged
```

```bash
# Using MERQURY
$MERQURY/merqury.sh ../illumina.meryl ~/path/to/dir/in/draft.m$i.endpurged.purged.fa \
 ~/path/to/dir/in/draft.m$i.endpurged.hap.fa purge.m$i.merqury
# Using BUSCO
busco -i ~/path/to/dir/in/draft.m$i.endpurged.purged.fa -o draft.m$i.endpurged -m genome -l ./endopterygota_odb10 \
 --download_path ./busco_downloads --offline -c $threads
```

```bash
# Using BlobTools
blobtools create --fasta ~/path/to/dir/in/draft.m$i.endpurged.purged.fa ~/path/to/dir/out/assembly-blob
blobtools add --busco  ~/path/to/dir/in/full_table.tsv ~/path/to/dir/out/assembly-blob
blobtools view --remote ~/path/to/dir/out/assembly-blob
blobtools host `pwd`
```

