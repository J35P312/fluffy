import argparse
import json
from slurmpy import Slurm
import os
import glob
import sys

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

def check_config(config,args):
	if not os.path.isfile(config["reference"]):
		print("error: cannot find reference genome fasta, check your config file")
		print(config["reference"])
		quit()

	if not os.path.isfile(config["wisecondorx"]["blacklist"]):
		print("error: cannot find the blacklist bed file, check your config file")
		print(config["wisecondorx"]["blacklist"])
		quit()

	if not os.path.isfile(config["singularity"]):
		print("error: cannot find the singularity collection, check your config file")
		print(config["singularity"])
		quit()

	if not os.path.isfile(config["wisecondorx"]["refpreface"]) and (not args.mkref and not args.skip_preface):
		print("error: cannot find the preface wisecondorX reference file, check your config file or use the --skip_preface option")
		print("remember to build the wisecondorX reference using the mkref option")
		print(config["wisecondorx"]["refpreface"])
		quit()

	if not os.path.isfile(config["wisecondorx"]["reftest"]) and (not args.mkref):
		print("error: cannot find the aneuploidy test wisecondorX reference file, check your config file")
		print("remember to build the wisecondorX reference using the mkref option")
		print(config["wisecondorx"]["reftest"])
		quit()

#create a command for running bwa and wisecondorX convert
def align_and_convert(config,fastq,args,sample):

	aln="singularity exec {} bwa aln -n 0 -k 0 {} {} > {}/{}.sai".format(config["singularity"],config["reference"],fastq,args.out,sample)
	samse="singularity exec {} bwa samse -n -1 {} {}/{}.sai {} | singularity exec {} bamsormadup inputformat=sam threads=16 SO=coordinate outputformat=bam tmpfile={}/{} indexfilename={}/{}.bam.bai > {}/{}.bam".format(config["singularity"],config["reference"],args.out,sample,fastq,config["singularity"],config["align"]["tmpdir"],sample,args.out,sample,args.out,sample)
	convert="singularity exec {} WisecondorX convert {}/{}.bam {}/{}.bam.wcx.npz".format(config["singularity"],args.out,sample,args.out,sample)
	run_bwa="\n".join([aln,samse,convert])

	return(run_bwa)

#generate wisecondorX reference files
def mkref(config,args):
	wcx_mkref="singularity exec {} WisecondorX newref {}/*.npz {}.test.npz --nipt --binsize {}".format(config["singularity"],args.out,args.out.rstrip("/"),config["wisecondorx"]["testbinsize"] )
	wcx_mkrefpreface="singularity exec {} WisecondorX newref {}/*.npz {}.preface.npz --nipt --binsize {}".format(config["singularity"],args.out,args.out.rstrip("/"),config["wisecondorx"]["prefacebinsize"])
	return("\n".join([wcx_mkref,wcx_mkrefpreface]))

#perform the wisecondorx test
def wisecondorx_test(config,args,sample):
	wcx_test="singularity exec {} WisecondorX --loglevel info predict {}/{}.bam.wcx.npz {} {}/{}.WCXpredict --plot --bed --blacklist {} --zscore {}".format(config["singularity"],args.out,sample,config["wisecondorx"]["reftest"],args.out,sample,config["wisecondorx"]["blacklist"],config["wisecondorx"]["zscore"])
	wcx_preface="singularity exec {} WisecondorX --loglevel info predict {}/{}.bam.wcx.npz {} {}/{}.WCXpredict.preface --plot --bed --blacklist {}".format(config["singularity"],args.out,sample,config["wisecondorx"]["refpreface"],args.out,sample,config["wisecondorx"]["blacklist"])
	gender="singularity exec {} WisecondorX gender {}/{}.bam.wcx.npz {} > {}/{}.wcx.npz.gender.txt".format(config["singularity"],args.out,sample,config["wisecondorx"]["reftest"],args.out,sample)
	return("\n".join([wcx_test,gender,wcx_preface]))

#fetal fraction estimation using tiddit and AMYCNE
def amycne_ffy(config,args,sample):
	path_gc_tab="{}/{}.gc.tab".format(args.out,sample)
	tiddit="singularity exec {} python /bin/TIDDIT.py --cov --bam {}/{}.bam -z {} -o {}/{}.tiddit".format(config["singularity"],args.out,sample,config["tiddit"]["binsize"],args.out,sample)
	gc_tab="singularity exec FluFFyPipe_0.0.sif python /bin/AMYCNE/Generate_GC_tab.py --fa {} --size {} --n_mask > {}".format(config["reference"],config["tiddit"]["binsize"],path_gc_tab)
	amycne="singularity exec {} python /bin/AMYCNE/AMYCNE.py --ff --coverage {}/{}.tiddit.tab --gc {} --Q {} > {}/{}.tiddit.AMYCNE.tab".format(config["singularity"],args.out,sample,path_gc_tab,config["amycne"]["minq"],args.out,sample)
	return("\n".join([tiddit,gc_tab,amycne]))

#fetal fraction estimation using Preface
def preface(config,args,sample):
	preface="singularity exec {} Rscript /bin/PREFACE-0.1.1/PREFACE.R predict --infile {}/{}.WCXpredict.preface_bins.bed --model {}/model.RData > {}/{}_bins.bed.PREFACE.txt".format(config["singularity"],args.out,sample,config["preface"]["model_dir"],args.out,sample)
	return(preface)

#collect QC stats using picard tools
def picard_qc(config,args,sample):
	out_prefix="{}/{}".format(args.out,sample)
	picard_gc="singularity exec {} picard CollectGcBiasMetrics I={}.bam O={}_gc_bias_metrics.txt CHART={}_gc_bias_metrics.pdf S={}.gc.summary.tab R={} {}".format(config["singularity"],out_prefix,out_prefix,out_prefix,out_prefix,config["reference"],config["picard"]["javasettings"])
	picard_insert="singularity exec {} picard CollectInsertSizeMetrics I={}.bam O={}_insert_size_metrics.txt H={}_insert_size_histogram.pdf M=0.5 {}".format(config["singularity"],out_prefix,out_prefix,out_prefix,config["picard"]["javasettings"])
	picard_complexity="singularity exec {} picard EstimateLibraryComplexity I={}.bam O={}_complex_metrics.txt {}".format(config["singularity"],out_prefix,out_prefix,config["picard"]["javasettings"])
	return("\n".join([picard_gc,picard_insert,picard_complexity]))

#construct Preface model
def preface_model(config,args):
	preface="singularity exec {} Rscript /bin/PREFACE-0.1.1/PREFACE.R train --config {}.PREFACE.config.tab --outdir {} {}".format(config["singularity"],args.out.rstrip("/"),config["preface"]["model_dir"],config["preface"]["modelsettings"])
	return(preface)

#generate a csv summary
def summarise(config,args):
	summary="singularity exec {} python /bin/FluFFyPipe/scripts/generate_csv.py --folder {} --samplesheet {} --Zscore {} --minCNV {} > {}/{}.summary.csv".format(config["singularity"],args.out,args.sample,config["summary"]["zscore"],config["summary"]["mincnv"],args.out,args.out.strip("/").split("/")[-1])
	return(summary)	

parser = argparse.ArgumentParser("""fluffypipe.py --sample <samplesheet>  --project <input_folder> --out <output_folder>  --config config.json""")
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

#copy config to output directory
os.system("cp {} {}".format(args.config,args.out))
#write version and command line to output directory
f=open("{}/cmd.txt".format(args.out),"w")
f.write("fluffypipe-{}\n".format(version))
f.write(" ".join(sys.argv))
f.close()


with open(args.config) as f:
	config = json.load(f)

check_config(config,args)

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
				ff=float(content[-2])*100

			out.append("{}\t{}/{}.WCXpredict.preface_bins.bed\t{}\t".format(sample,args.out,sample,gender,ff))

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

		run_picard=picard_qc(config,args,sample)
		picard = Slurm("picard_qc-{}".format(sample),{"account": config["slurm"]["account"], "partition": "core","time":config["slurm"]["time"] },log_dir="{}/logs".format(args.out),scripts_dir="{}/scripts".format(args.out))
		jobids.append(picard.run( run_picard,depends_on=[align_jobid] ))

		run_wcx=wisecondorx_test(config,args,sample)
		wcx_test = Slurm("wcx-{}".format(sample),{"account": config["slurm"]["account"], "partition": "core","time":config["slurm"]["time"] },log_dir="{}/logs".format(args.out),scripts_dir="{}/scripts".format(args.out))
		jobids.append(wcx_test.run( run_wcx,depends_on=[align_jobid] ))
		wcx_test_jobid=jobids[-1]

		if not args.skip_preface:
			run_preface=preface(config,args,sample)
			preface_predict = Slurm("preface_predict-{}".format(sample),{"account": config["slurm"]["account"], "partition": "core","time":config["slurm"]["time"] },log_dir="{}/logs".format(args.out),scripts_dir="{}/scripts".format(args.out))
			jobids.append(preface_predict.run(run_preface,depends_on=[wcx_test_jobid]))

	run_summarise=summarise(config,args)
	summarise_batch = Slurm("summarise_batch-{}".format( args.project.strip("/").split("/")[-1] ),{"account": config["slurm"]["account"], "partition": "core","time":config["slurm"]["time"] },log_dir="{}/logs".format(args.out),scripts_dir="{}/scripts".format(args.out))
	summarise_batch.run(run_summarise,depends_on=jobids )
