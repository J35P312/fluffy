import argparse
import json
from slurmpy import Slurm
import os
import glob

#read the samplesheet
def read_samplesheet(samplesheet,project_dir):
	samples={}
	first=True
	sample_col=0
	for line in open(samplesheet):
		if " " in line:
			content=line.strip().split()
		elif "," in line:
			content=line.strip().split(",")
		else:
			content=[line.strip()]

		if first:
			first=False
			for i in range(0,len(content)):
				if content[i] == "SampleID":
					sample_col=i
			continue

		sample_name=content[ sample_col ]


		if sample_name in samples:
			continue

		fastq=[]
		R1=[]
		R2=[]
		for file in glob.glob("{}/*{}*/*.fastq.gz".format(project_dir,sample_name)):
			print(file)
			if not "R1" in file and not "R2" in file:
				continue
			if "R1" in file:
				R1.append(file)
			elif "R2" in file:
				R2.append(file)
			fastq.append(file)
		print(fastq)
		if len(R1) < 2:
			fastq=" ".join(fastq)
		else:
			if len(R2) == 0:
				fastq="<( zcat {}/*{}*/*R1*fastq.gz )".format(project_dir,sample_name)
			else:
				fastq="<( zcat {}/*{}*/*R1*fastq.gz ) <( zcat {}/{}/*R2*fastq.gz )".format(project_dir,sample_name,project_dir,sample_name)
		samples[sample_name]=fastq

	return(samples)

#create a command for running bwa and wisecondorX convert
def align_and_convert(config,fastq,args,sample):

	aln="singularity exec {} bwa aln -n 0 -k 0 {} {} > {}/{}.sai".format(config["singularity"],config["reference"],fastq,args.out,sample)
	samse="singularity exec {} bwa samse -n -1 {} {}/{}.sai {} | singularity exec {} bamsormadup inputformat=sam threads=16 SO=coordinate outputformat=bam tmpfile={}/{} indexfilename={}/{}.bam.bai > {}/{}.bam".format(config["singularity"],config["reference"],args.out,sample,fastq,config["singularity"],config["align"]["tmpdir"],sample,args.out,sample,args.out,sample)
	convert="singularity exec {} WisecondorX convert {}/{}.bam {}/{}.bam.wcx.npz".format(config["singularity"],args.out,sample,args.out,sample)
	run_bwa="\n".join([aln,samse,convert])

	return(run_bwa)

#generate wisecondorX reference files
def mkref(config,args):
	wcx_mkref="singularity exec {} WisecondorX newref {}/*.npz {}.npz --nipt --binsize 500000".format(config["singularity"],args.out,args.out.rstrip("/") )
	wcx_mkref100kbp="singularity exec {} WisecondorX newref {}/*.npz {}.npz --nipt --binsize 100000".format(config["singularity"],args.out,args.out.rstrip("/"))
	return("\n".join([wcx_mkref,wcx_mkref100kbp]))

#perform the wisecondorx test
def wisecondorx_test(config,args,sample):
	wcx_test500="singularity exec {} WisecondorX --loglevel info predict {}/{}.bam.wcx.npz {} {}/{}.WCXpredict --plot --bed --blacklist {}".format(config["singularity"],args.out,sample,config["wisecondorx"]["ref500kbp"],args.out,sample,config["wisecondorx"]["blacklist"])
	wcx_test100="singularity exec {} WisecondorX --loglevel info predict {}/{}.bam.wcx.npz {} {}/{}.WCXpredict.100kbp --plot --bed --blacklist {}".format(config["singularity"],args.out,sample,config["wisecondorx"]["ref100kbp"],args.out,sample,config["wisecondorx"]["blacklist"])
	gender="singularity exec {} WisecondorX gender {}/{}.bam.wcx.npz {} > {}/{}.wcx.npz.gender.txt".format(config["singularity"],args.out,sample,config["wisecondorx"]["ref500kbp"],args.out,sample)
	return("\n".join([wcx_test500,gender,wcx_test100]))

#fetal fraction estimation using tiddit and AMYCNE
def amycne_ffy(config,args,sample):
	tiddit="singularity exec {} python /bin/TIDDIT.py --cov --bam {}/{}.bam -z {} -o {}/{}.tiddit".format(config["singularity"],args.out,sample,config["tiddit"]["binsize"],args.out,sample)
	amycne="singularity exec {} python /bin/AMYCNE/AMYCNE.py --ff --coverage {}/{}.tiddit.tab --gc {} --Q {} > {}/{}.tiddit.AMYCNE.tab".format(config["singularity"],args.out,sample,config["amycne"]["gc"],config["amycne"]["minq"],args.out,sample)
	return("\n".join([tiddit,amycne]))

#fetal fraction estimation using Preface
def preface(config,args,sample):
	preface="singularity exec {} Rscript /bin/PREFACE-0.1.1/PREFACE.R predict --infile {}/{}.WCXpredict.100kbp_bins.bed --model {}/model.RData > {}/{}_bins.bed.PREFACE.txt".format(config["singularity"],args.out,sample,config["preface"]["model_dir"],args.out,sample)
	return(preface)

#construct Preface model
def preface_model(config,args):
	preface="singularity exec {} Rscript /bin/PREFACE-0.1.1/PREFACE.R train --config {}.PREFACE.config.tab --outdir {}".format(config["singularity"],args.out.rstrip("/"),config["preface"]["model_dir"])
	return(preface)

parser = argparse.ArgumentParser("""fluffypipe.py --sample <samplesheet>  --in <input_folder> --out <output_folder>  --config config.json""")
parser.add_argument('--project'       ,type=str, help="input project folder", required=True)
parser.add_argument('--out'       ,required=True,type=str, help="output folder")
parser.add_argument('--config'       ,required=True,type=str, help="json config file")
parser.add_argument('--sample', type=str,required=True, help="path to samplesheet")
parser.add_argument('--mkref', help="generate wisecondorX reference",action="store_true")
parser.add_argument('--mkmodel', help="generate PREFACE model",action="store_true")
parser.add_argument('--version', help="print version",action="store_true")
parser.add_argument('--skip_preface', help="Skip Preface fetal fraction prediction",action="store_true")
args= parser.parse_args()

version="0.0.0"
if args.version:
	print ("FluFFYPipe version {}".format(version))
	quit()

if not os.path.isdir(args.out):
	os.system( "mkdir {}".format(args.out) )

with open(args.config) as f:
	config = json.load(f)

samples=read_samplesheet(args.sample,args.project)

if args.mkref:
	jobids=[]
	for sample in samples:
		fastq=samples[sample]
		run_bwa=align_and_convert(config,fastq,args,sample)
		bwa = Slurm("bwaAln-{}".format(sample),{"account": config["slurm"]["account"], "partition": "node","time":config["slurm"]["time"] },log_dir="{}/logs".format(args.out),scripts_dir="{}/scripts".format(args.out))
		jobids.append(bwa.run(run_bwa))

	wcxmkref = Slurm("wcxmkref",{"account": config["slurm"]["account"], "partition": "node","time":config["slurm"]["time"] },log_dir="{}/logs".format(args.out),scripts_dir="{}/scripts".format(args.out))
	wcxmkref.run( mkref(config,args),depends_on=jobids )

elif args.mkmodel:
	f=open("{}.PREFACE.config.tab".format(args.out.rstrip("/")), "w" )
	f.write("ID\tfilepath\tgender\tFF\n")
	for sample in samples:
		for line in open("{}/{}.AMYCNE.tab".format(args.out,sample) ):
			if "medA" in line:
				continue
			content=line.strip().split()
			if female in line:
				ff="NA"
				gender="F"
			else:
				gender="M"
				ff=float(content[2])*100

			out.append("{}\t{}/{}.WCXpredict.100kbp_bins.bed\t{}\t".format(sample,args.out,sample,gender,ff))

	f.write("\n".join(out))
	f.close()

	if config["preface"]["model_dir"] == "":
		print ("error: the model_dir parameter is not set, check your config file")
		quit()

	run_model=preface_model(config,args,sample)

else:
	jobids=[]
	for sample in samples:
		fastq=samples[sample]
		run_bwa=align_and_convert(config,fastq,args,sample)
		bwa = Slurm("bwaAln-{}".format(sample),{"account": config["slurm"]["account"], "partition": "node","time":config["slurm"]["time"] },log_dir="{}/logs".format(args.out),scripts_dir="{}/scripts".format(args.out))
		align_jobid=bwa.run(run_bwa)

		run_ffy=amycne_ffy(config,args,sample)
		ffy = Slurm("amycne-{}".format(sample),{"account": config["slurm"]["account"], "partition": "core","time":config["slurm"]["time"] },log_dir="{}/logs".format(args.out),scripts_dir="{}/scripts".format(args.out))
		jobids.append(ffy.run( run_ffy,depends_on=[align_jobid] ))

		run_wcx=wisecondorx_test(config,args,sample)
		wcx_test = Slurm("wcx-{}".format(sample),{"account": config["slurm"]["account"], "partition": "core","time":config["slurm"]["time"] },log_dir="{}/logs".format(args.out),scripts_dir="{}/scripts".format(args.out))
		jobids.append(wcx_test.run( run_wcx,depends_on=[align_jobid] ))
		wcx_test_jobid=jobids[-1]

		if not args.skip_preface:
			run_preface=preface(config,args,sample)
			preface_predict = Slurm("preface_predict-{}".format(sample),{"account": config["slurm"]["account"], "partition": "core","time":config["slurm"]["time"] },log_dir="{}/logs".format(args.out),scripts_dir="{}/scripts".format(args.out))
			jobids.append(preface_predict.run(run_preface,depends_on=[wcx_test_jobid]))

