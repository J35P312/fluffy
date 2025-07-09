![Build](https://github.com/Clinical-Genomics/fluffy/workflows/Build/badge.svg)
[![codecov](https://codecov.io/gh/Clinical-Genomics/fluffy/branch/master/graph/badge.svg)](https://codecov.io/gh/Clinical-Genomics/fluffy)
# FluFFyPipe
NIPT analysis pipeline, using WisecondorX for detecting aneuplodies and large CNVs, AMYCNE for FFY and PREFACE for FF prediction (optional). wcx2cytosure is used to convert WisecondorX output into CytoSure Interpret Software (by OGT) format (.cgh file). FluFFYPipe produces a variety of output files, as well as a per batch csv summary.

![fluffythesnail](https://github.com/user-attachments/assets/57680a01-68b4-4c63-97b3-93e871cf6082)


# Run FluFFyPipe
Run NIPT analysis, using a previously comnputed reference:

    fluffy --sample <samplesheet>  --project <input_folder> --out <output_folder> --analyse
    
Run NIPT analysis, using an internally computed reference (i.e the reference is built using all samples listed in samplesheet):

    fluffy --sample <samplesheet>  --project <input_folder> --out <output_folder> --analyse --batch-ref

optionally, skip preface:

    fluffy --sample <samplesheet>  --project <input_folder> --out <output_folder> --skip_preface --analyse

All output will be written to the output folder, this output includes:

```
bam files
wisecondorX output
tiddit coverage summary
Fetal fraction estimation
cgh file with probes for coverage per bin and aberrations for visualization in CytoSure Interpret Software (by OGT).
```

as well as a summary csv and multiqc html (per batch)

the input folder is a project folder containing one folder per sample, each of these subfolders contain the fastq file(s).
The samplesheet contains at least a "sampleID" column, the sampleID should match the subfolders in the input folder. The samplesheet may contain other columns, such as flowcell and index folder: such columns will be printed to the summary csv.
If the samplesheet contains a SampleName column, fluffy will name the output according to SampleName

Create a WisecondorX reference

    fluffy --sample <samplesheet>  --project <input_folder> --out <output_folder> --reference
    
samplesheet should contain atleast a "sampleID" column. All samples in the samplesheet will be used to construct the reference, visit the WisecondorX manual for more information.
# Optional fluffy parameters:
	Analysis mode:
		--dry_run - run the pipeline without generating files
		-l	-	add paramters to the slurm header of the script, should be given on the following format parameter:value
				example: qos:high 
	
	Reference mode:
		--dry_run - run the pipeline without generating files
		
	Rerun mode:
		--dry_run - run the pipeline without generating files
		
# Troubleshooting and rerun
There are three statuses of the fluffy pipeline:
running, complete, and failed

The status of a fluffy run is found in the

	<output_folder>/analysis_status.json
	
The status of all jobs are listed in

	<output_folder>/sacct/fluffy_<date>.log.status
	
Where <date> is the timepoint when the jobs were submitted
Use grep to find the failed jobs:
	
	grep -v COMPLETE <output_folder>/sacct/fluffy_<date>.log.status
	
The output logs are stored in:

	 <output_folder>/logs

Before continuing, you may want to generate the summary csv for all completed cases:

	bash <output_folder>/scripts/summarizebatch-<hash>

where <hash> is a randomly generated string.
	
use the rerun module to rerun failed fluffy analyses:

	fluffy --sample <samplesheet>  --project <input_folder> --out <output_folder> --skip_preface rerun
	
 
# Install FluFFyPipe
FluFFyPipe requires python 3, slurm, slurmpy, and singularity, python-coloredlogs.

fluffy may be installed using pip:

	pip install fluffy-cg

alternatively, fluffy is cloned and installed from github:
	git clone https://github.com/Clinical-Genomics/fluffy
	cd fluffy
	pip install -e .
	
Next download the FluFFyPipe singularity container and the wcx2cytosure singularity container:

     singularity pull library://jeisfeldt/default/fluffy:sha256.dbef92cd5eab8558c2729f73a191d73a7576a24e9bb44dde7372c0cd405c4ef6 
     singularity pull --arch amd64 library://ravinale/wcx2cytosure/wcx2cytosure:latest


copy the example config (found in example_config), and edit the variables.
You will need to download/create the following files:

	Reference fasta (indexed using bwa)

	WisecondorX reference files (created using the reference mode)

	PREFACE model file (optional)

	blacklist bed file (used by wisecondorX)

	FluFFyPipe singularity collection (singularity pull --name FluFFyPipe.sif shub://J35P312/FluFFyPipe)
	
	wcx2cytosure singularity container


