# FluFFyPipe
NIPT analysis pipeline, using WisecondorX for detecting aneuplodies and large CNVs, AMYCNE for FFY and PREFACE for FF prediction (optional). FluFFYPipe produces a variety of output files, as well as a per batch csv summary.

FluFFyPipe is still in early development, use at your own risk!

<p align="center">
<img src="https://github.com/J35P312/FluFFyPipe/blob/master/logo/IMG_20200320_132001.jpg" width="400" height="400" >
</p>

# Run FluFFyPipe
Run NIPT analysis:

  fluffypipe.py --sample <samplesheet>  --in <input_folder> --out <output_folder>
  
optionally, skip preface:

  fluffypipe.py --sample <samplesheet>  --in <input_folder> --out <output_folder> --skip_preface

All output will be written to the output folder, this output includes:

  bam files
  wisecondorX output
  tiddit coverage summary
  Fetal fraction estimation

as well as a summary csv (per batch)

the input folder is a project folder containing one folder per sample, each of these subfolders contain the fastq file(s).
The samplesheet contains at least a "sampleID" column, the sampleID should match the subfolders in the input folder. The samplesheet may contain other columns, such as flowcell and index folder: such columns will be printed to the summary csv.

Create a WisecondorX reference 

  fluffypipe.py --sample <samplesheet>  --in <input_folder> --out <output_folder> --mkref
  
samplesheet should contain atleast a "sampleID" column. All samples in the samplesheet will be used to construct the reference, visit the WisecondorX manual for more information.

Create a PREFACE reference:

  fluffypipe.py --sample <samplesheet>  --in <input_folder> --out <output_folder> --mkmodel
  
samplesheet should contain atleast a "sampleID" column. All samples in the samplesheet will be used to construct the reference, visit the PREFACE manual for more information. Note, you need to first run the FluFFYPipe with "--skip_preface" option, next you may run mkmodel - this is necessary as the AMYCNE FFY estimations are used for training the model.

# Install FluFFyPipe

