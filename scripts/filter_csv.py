import argparse
import copy
import os
from os import listdir
from os.path import isfile, join

import numpy

parser = argparse.ArgumentParser(
    """filter_csv.py --csv input_csv --Zscore zscore_limit --max_exclude maximum_excluded"""
)

parser.add_argument("--csv",required=True,type=str,help="folder containing wisecondorX output files")
parser.add_argument("--Zscore", default=2, type=float, help="Z score limit (13,18,21)")
parser.add_argument("--binsize",nargs="+", default=100000, type=int, help="bin size of the output reference")
parser.add_argument("--project",required=True, type=str, help="Fluffy project directory")
parser.add_argument("--singularity", type=str, help="singularity base command")

args = parser.parse_args()

first=True

files=[]
excluded=0
for line in open(args.csv):
	if first:
		first=False
		continue
	content=line.strip().split("\",\"")

	sample=content[0]
	zscore13=abs(float(content[9]))	
	zscore18=abs(float(content[10]))	
	zscore21=abs(float(content[11]))

	if max([zscore13,zscore18,zscore21]) > args.Zscore:
		excluded+=1
	else:
		files.append("{}/{}/{}.bam.wcx.npz".format(args.project,sample,sample))	

print("excluded: {}".format(excluded))
print("reference: {}".format(len(files)) )
for binsize in args.binsize:
	os.system("{} WisecondorX newref {} {}.wcxref.{}.npz --nipt --binsize {}".format(args.singularity," ".join(files),args.project,binsize,binsize))

f=open("{}/internal_ref_samples.txt".format(args.project) ,"w")
for sample in files:
	f.write(sample.split("/")[-1].split(".")[0].strip("\"")+"\n")

f.close()
