# Preassembly
Raw read quality assessment and filter

We have generated sequence data from whole body DNA extract of one female beetle from the laboratory stock. Our data constitutes about 30 GB long read nanopore sequence and 250 GB short read pair end illumina sequence. Raw sequence data was quality assessed using FastP for short reads and NanoPlot for long read data.

```
fastqc -o ~/path/to/dir *.fastq.gz*
cd ~/path/to/dir
multiqc .
```
