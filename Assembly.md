# Assembly
Stitching error corrected reads to prepare continuous long stretches of sequence

As we have aimed at assembling the genome using long reads, we prefer to use [flye](https://github.com/fenderglass/Flye) assembler for contig preparation from the read files. Alternatively Canu can also be used for nanopore reads assembly.
```
# Running flye assembler
flye --nano-raw ~/path/to/dir/in/lr.corrected.fa.gz -o ~/path/to/dir/out -t $threads
```

```
### Scaffolding FLYE contigs with error-corrected long-reads
contigs=$(~/path/to/dir/in/contigs.fa)
reads=$(~/path/to/dir/in/lr.corrected.fa.gz)
longstitch ntLink-arks draft=contigs.fa reads=$reads out_prefix=$prefix t=$threads G=1e9
```
