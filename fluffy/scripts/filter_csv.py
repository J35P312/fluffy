import argparse
import copy
import sys
import subprocess
import os
import numpy
from os import listdir
from os.path import isfile, join

def mad(arr):
    #copied from:https://stackoverflow.com/questions/8930370/where-can-i-find-mad-mean-absolute-deviation-in-scipy
    arr = numpy.ma.array(arr).compressed() # should be faster to not use masked arrays.
    med = numpy.median(arr)
    return numpy.median(numpy.abs(arr - med))


parser = argparse.ArgumentParser(
    """filter_csv.py --csv input_csv --Zscore zscore_limit --max_exclude maximum_excluded"""
)

parser.add_argument("--csv",required=True,type=str,help="folder containing wisecondorX output files")
parser.add_argument("--Zscore", default=2, type=float, help="Z score limit (13,18,21)")
parser.add_argument("--ratio", default=1.01, type=float, help="Z score limit (13,18,21)")
parser.add_argument("--binsize",nargs="+", default=100000, type=int, help="bin size of the output reference")
parser.add_argument("--project",required=True, type=str, help="Fluffy project directory")
parser.add_argument("--singularity", type=str, help="singularity base command")

args = parser.parse_args()

first=True

files=[]
excluded=0
Zscores={"13":[],"18":[],"21":[]}

exclude=set([])

for line in open(args.csv):
	if first:
		first=False
		continue
	content=line.strip().split("\",\"")

	sample=content[0].replace("\"","")
	zscore13=abs(float(content[9]))	
	zscore18=abs(float(content[10]))	
	zscore21=abs(float(content[11]))

	ratio13=abs(float(content[13]))	
	ratio18=abs(float(content[14]))	
	ratio21=abs(float(content[15]))	

	if max([ratio13,ratio18,ratio21]) > args.ratio or max([zscore13,zscore18,zscore21]) > args.Zscore or "Excluded_from_ref(In_Samplesheet)" in line:
		excluded+=1
	else:
		Zscores["13"].append(ratio13)
		Zscores["18"].append(ratio18)
		Zscores["21"].append(ratio21)

		files.append("{}/{}/{}.bam.wcx.npz".format(args.project,sample,sample))	

tries=30
n=0
for binsize in args.binsize:

	try:
		os.remove("{}.wcxref.{}.npz".format(args.project,binsize))
	except:
		pass

	cmd_str=args.singularity.split()+["WisecondorX","newref"]+files+["{}.wcxref.{}.npz".format(args.project,binsize),"--nipt","--binsize", str(binsize)]
	print (cmd_str)

	while True:
		
		cmd = subprocess.Popen(cmd_str,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		output, error = cmd.communicate()
		rc=cmd.returncode
		print(rc)
		print(error)
		n+=1
		if n > tries:
			sys.exit(1)

		if not rc:
			break

		
print("excluded: {}".format(excluded))
print("reference: {}".format(len(files)) )

f=open("{}/internal_ref_samples.txt".format(args.project) ,"w")
for sample in files:
	f.write(sample.split("/")[-1].split(".")[0].strip("\"")+"\n")

f.close()
