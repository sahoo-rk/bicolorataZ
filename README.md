# bicolorataZnome
Genome assembly and annotation pipeline of *Zygogramma bicolorata*, commonly known as the 'Parthenium beetle' or 'Mexican beetle'.

> This repository has two primary agenda: one, a supplementary material to the research publication [Sahoo et al 2023](https://doi.org/10.1093/gbe/evad188) on the beetle genome assembly; two, a guide to the non-bioinformaticians to get acquainted with the genome assembly pipeline.

To make sure that all the syntax used in the analysis pipeline are clear to the reader, few key notations need to be clarified:  
`~/path/to/dir` denotes path to the directory of interest.  
`~/path/to/dir/in` denotes path to the directory where the input file resides.  
`~/path/to/dir/out` denotes path to the directory where the output file will be placed.  
`./` indicates current directory from where the program of interest in executing.  

The pipeline has a simplified route. [Preassembly.md](../main/1.%20Preassembly.md) records the quality assessment steps to check and filter low quality reads and biological/methodological contaminants of minor interest from the raw sequence data. Once the raw data is cleaned, a series of methods in the [Assembly.md](../main/2.%20Assembly.md) stage is followed to establish the most probable connections among the reads forming contigs or scaffolds or chromosomes, if possible. Then, the assembled fragments are checked for quality and completeness using certain measurable parameters in the [Postassembly.md](../main/3.%20Postassembly.md) stage.

Wish the best!

> Note: This pipeline is not exhaustive in nature. Training programs at the [Galaxy Project](https://training.galaxyproject.org) are comprehensive and resourceful. Readers may gain further insight into the pipeline by following those tutorials.
