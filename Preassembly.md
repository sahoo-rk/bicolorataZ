# Preassembly
Raw read quality assessment and filter

We have generated sequence data from whole body DNA extract of one female beetle from the laboratory stock. Our data constitutes about 30 GB long read nanopore sequence and 250 GB short read pair end illumina sequence. Raw sequence data was quality assessed using [FastQC](https://github.com/s-andrews/FastQC) for short reads and [NanoPlot](https://github.com/wdecoster/NanoPlot) for long read data.

```bash
# Running FastQC
fastqc -o ~/path/to/dir ~/path/to/dir/*.fastq.gz*
cd ~/path/to/dir
multiqc .
```
```bash
# Running NanoPlot
NanoPlot --summary ~/path/to/dir/sequencing_summary_1.txt ~/path/to/dir/sequencing_summary_2.txt \
 -t 40 -o ~/path/to/dir/nanoplot --N50 --minqual 9 -p $prefix
```
> The resulting <.html> files from FastQC and NanoPlot were manually inspected for sequence metadata and read quality assessment.

Because, in Nanopore sequencing platform, the DNA sequences are read through the changes in voltage, the base errors are randomly distributed in the entire length of reads. Hence, we do not usually do end trimming for Nanopore reads. However, quality control is done by default during the Guppy base calling, which is mostly carried out by the NGS facility or the service provider, that filters out the entire reads with average Phred quality less than 9.

However, we quality trimmed the short read illumina data as follows using [FastP](https://github.com/OpenGene/fastp).
```bash
# Running FastP
fastp -i ~/path/to/dir/in/R1.fastq.gz -o ~/path/to/dir/out/R1.fastq.gz \
 -I ~/path/to/dir/in/R2.fastq.gz -O ~/path/to/dir/out/R2.fastq.gz \
 --detect_adapter_for_pe --trim_poly_g -5 -3 -l 51 -j ~/path/to/dir/out/$prefix.json \ 
 -h ~/path/to/dir/out/$prefix.html -w 40
```

Our genome assembly pipeline aimed at long read based assembly where the short reads were primarily utilised to polish the long reads and the assembly files during the process. Therefore, we first
