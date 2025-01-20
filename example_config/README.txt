{
	#Alignment settings
	"align":{
		#Temporary files are written here
		"tmpdir":"$TMPDIR/",
                #number of cpu for alignment
                "ntasks":16,
		#amount of memory (set to 0 in order to use all memory available to the cores)
                "mem":0

	},

	#AMYCNE FFY estimation settings
	"amycne":{
		#Minimum per bin mapping quality
		"minq":13,
                #Coefficient that is multiplied with the median coverage of Y (FFY=(coefficient*(median Y coverage) ))
                "coefficient":2
	},

	#WisecondorX settings
	"wisecondorx":{
		#reference for the aneuoplody wisecondorX analysis (produced through reference)
		"ref500kbp":"/proj/sens2019010/nobackup/wisecondor_X_bwa_ref.npz",
		#reference for the Preface analysis (produced through reference)
		"ref100kbp":"/proj/sens2019010/nobackup/wisecondor_X_bwa_ref.100kbp.npz",
		#a blacklist (bed file)
		"blacklist":"/proj/sens2019010/nobackup/blacklist.bed"
	},

	#Tiddit settings
	"tiddit":{
		#bin size, this will be used in the ffy prediction 
		"binsize":50000
	},

	#preface settings
	"preface":{
		#directory containing the model file
		"model_dir":"/proj/sens2019010/nobackup/PREFACE/AMYCNE_15g_2500_100kbp.conf.model.olm",
		#custom preface model settigns
		"modelsettings":"--olm"
	},

	#Picard settings
	"picard":{
		#java settings, such as controling memory limits
		"javasettings":"-Xms4G -Xmx4G"
	},

	#reference fasta
	"reference":"/proj/sens2019010/reference/human_g1k_v37.fasta",

	#singularity files
	"singularity":"/proj/sens2019010/nobackup/wharf/jesperei/jesperei-sens2019010/Clevervulture2.sif",
        "wcx_singularity":"/proj/sens2017106/nobackup/denise/thesis/wcx2cytosure_latest.sif",

	#paths mounted (singularity bind) by singularity, you may need to add reference directory etc
        "singularity_bind":[],

	#slurm settings
	"slurm": {
		#account
		"account":"sens2019010",
		#time, usualy these processes will finnish within 1 hour
		"time":"5:00:00",
		#other flags to be written to the slurm header
		"flags":""
	},

	#summary settings
        "summary":{
		#minimum segmental call size
                "mincnv":10000000,
		#minmum zscore of segmental calls
                "zscore":3
        }

}
