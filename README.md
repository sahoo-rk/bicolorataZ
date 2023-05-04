# bicolorataZ
Genome assembly and annotation pipeline of *Zygogramma bicolorata*, commonly known as the Mexican beetle.

> This repository has two primary agenda: one, a supplementary material to our research publication XXX on the beetle genome assembly; two, a guide to the non-bioinformaticians to get acquainted to the genome assembly pipeline.

To make sure that all the syntax used in the analysis pipeline are clear to the reader, few key notations need to be clarified:  
```~/path/to/dir``` denotes path to the directory of interest.  
```~/path/to/dir/in``` denotes path to the directory where the input file resides.  
```~/path/to/dir/out``` denotes path to the directory where the output file will be placed.  
```./``` indicates current directory from where the program of interest in executing.  

The pipeline has a simplified route. ```Preassembly.md``` records the quality assessment steps that we follow to check and filter low quality reads and biological/methodological contaminants of minor interest from the raw sequence data. Once the raw data is cleaned, we follow a series of methods in the ```Assembly.md``` stage to establish the most probable connections among the reads forming contigs or scaffolds or chromosomes, if possible. We then test the assembled fragments for quality and completeness using certain measurable parameters in the ```Postassembly.md``` stage.

As an ecologist by training, I have had a steep learning curve while working with the high-throughput sequence data. However, I realise that this period has been one of the most engaging part of my current research as I learn and apply the bioinformatic fundamentals and tools to explore and understand the unknown.

Hope this pipeline will be an useful asset to the readers, particulary to the researchers from non-bioinformatics background.  
Wish the best!

