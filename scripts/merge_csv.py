import sys
import copy

first=True
data={}
sample_order=[]
for line in open(sys.argv[1]):
	if first:
		print(line.strip())
		first=False
		continue

	content=line.strip().split("\",\"")
	data[content[0]] = copy.copy(content)
	sample_order.append(content[0])



#print(data)
first =True
for line in open(sys.argv[2]):
	if first:
		first=False
		continue

	content=line.strip().split("\",\"")

	#Update QCflag
	if "Excluded_from_ref" in content[8]:
		if data[content[0]][8] == "":
			data[content[0]][8]="Excluded_from_ref"
		else:
			data[content[0]][8]=";".join([ "Excluded_from_ref",data[content[0]][8] ])

	#Update Zscore
	data[content[0]][9]=content[9]
	data[content[0]][10]=content[10]
	data[content[0]][11]=content[11]

	#update ratio
	data[content[0]][13]=content[13]
	data[content[0]][14]=content[14]
	data[content[0]][15]=content[15]
	#print(data[content[0]])
	print('","'.join(data[content[0]]))
