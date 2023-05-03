# Preassembly
Raw read quality assessment and filter

We have generated sequence data from whole body DNA extract of one female beetle from the laboratory stock. Our data constitutes about 30 GB long read nanopore sequence and 250 GB short read pair end illumina sequence. Raw sequence data was quality assessed using [FastQC](https://github.com/s-andrews/FastQC) for short reads and [NanoPlot](https://github.com/wdecoster/NanoPlot) for long read data.

```bash
# Running FastQC
fastqc -o ~/path/to/dir/out ~/path/to/dir/in/*.fastq.gz*
cd ~/path/to/dir/out
multiqc .
```
```bash
# Running NanoPlot
NanoPlot --summary ~/path/to/dir/in/lr_summary_1.txt ~/path/to/dir/in/lr_summary_2.txt \
 -t 40 -o ~/path/to/dir/out/nanoplot --N50 --minqual 9 -p $prefix
```
> The resulting <.html> files from FastQC and NanoPlot were manually inspected for sequence metadata and read quality assessment.

Because, in Nanopore sequencing platform, the DNA sequences are read through the changes in voltage, the base errors are randomly distributed in the entire length of reads. Hence, we do not usually do end trimming for Nanopore reads. However, quality control is done by default during the Guppy base calling, which is mostly carried out by the NGS facility or the service provider, that filters out the entire reads with average Phred quality less than 9.

However, we quality trimmed the short read illumina data as follows using [FastP](https://github.com/OpenGene/fastp).
```bash
# Running FastP
fastp -i ~/path/to/dir/in/sr_R1.fastq.gz -o ~/path/to/dir/out/sr.corrected.R1.fq.gz \
 -I ~/path/to/dir/in/sr_r2.fastq.gz -O ~/path/to/dir/out/sr.corrected.R2.fq.gz \
 --detect_adapter_for_pe --trim_poly_g -5 -3 -l 51 -j ~/path/to/dir/out/$prefix.json \ 
 -h ~/path/to/dir/out/$prefix.html -w 40
```

Our genome assembly pipeline aimed at long read based assembly where the short reads were primarily utilised to polish the long reads and the assembly files during the process. Therefore, we first ploished the nanopore long reads with the error corrected illumina short reads from FastP using [fmlrc2](https://github.com/HudsonAlpha/fmlrc2).
```bash
# Building BWT using error corrected short reads from FastP
gunzip -c ~/path/to/dir/in/sr.corrected.R1.fq.gz ~/path/to/dir/in/sr.corrected.R2.fq.gz \
| awk 'NR % 4 == 2' | tr NT TN | ropebwt2 -LR | tr NT TN | fmlrc2-convert ~/path/to/dir/out/comp_msbwt.npy
# Error correcting the long read file
fmlrc2 -C 10 -t 40 ~/path/to/dir/in/comp_msbwt.npy ~/path/to/dir/in/lr.fastq.gz ~/path/to/dir/out/lr.corrected.fa
# Compressing the error corrected long read for downstream processes
bgzip -@ 40 ~/path/to/dir/in/lr.corrected.fa
```
> The resulting ```lr.corrected.fa``` will be the input for downstream genome analysis with the ```sr.corrected.R1.fq.gz``` and ```sr.corrected.R2.fq.gz``` files being used for polishing the assembly. Check Assembly page for next steps.

We further used a k-mer based read assessment to understand the sequencing coverage and genome size estimation. For the purpose, we used [meryl](https://github.com/marbl/meryl) and [Genomescope](https://github.com/schatzlab/genomescope).
```bash
# Estimating the k-mer size
$MERQURY/best_k.sh $genomesize
```
> For the genome sizes of 700 MB and 1200 MB, the estimated k-mer size was 19.67 and 20.06, respectively. We, therefore, used 20 as the k-mer size for our downstream analyses.

```bash
# Assessing error corrected short reads for k-mer distribution graph
meryl count threads=$threads k=20 ~/path/to/dir/in/*.fq.gz output sr.meryl
meryl histogram ~/path/to/dir/in/sr.meryl > sr.hist
Rscript ~/path/to/dir/genomescope.R -i ~/path/to/dir/in/sr.hist -o ~/path/to/dir/out -n $prefix -p 2 -k 20
```
Careful assessment of this output is essential to understand the distribution of sequence reads in the genome space. rrrrr
