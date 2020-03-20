{
  #Alignment settings
	"align":{
    #Temporary files are written here
		"tmpdir":"$TMPDIR/"
	},
  #AMYCNE FFY estimation settings
	"amycne":{
    #Minimum per bin mapping quality
		"minq":13,
    #GC content file
		"gc":"/proj/sens2019010/nobackup/wharf/jesperei/jesperei-sens2019010/AMYCNE/human_g1k_v37.50kbp.gc.bed"
	},
  #WisecondorX settings
	"wisecondorx":{
    #reference for the aneuoplody wisecondorX analysis (produced through mkref)
		"ref500kbp":"/proj/sens2019010/nobackup/wisecondor_X_bwa_ref.npz",
    #reference for the Preface analysis (produced through mkref)
		"ref100kbp":"/proj/sens2019010/nobackup/wisecondor_X_bwa_ref.100kbp.npz",
    #a blacklist (bed file)
		"blacklist":"/proj/sens2019010/nobackup/blacklist.bed"
	},
  #Tiddit settings
	"tiddit":{
    #bin size, this will be used in the ffy prediction 
		"binsize":50000
	},
	"preface":{
    #directory containing the model file
		"model_dir":"/proj/sens2019010/nobackup/PREFACE/AMYCNE_15g_2500_100kbp.conf.model.olm",
    #use olm (otherwise set to 0)
		"olm":1
	},
  #reference fasta
	"reference":"/proj/sens2019010/reference/human_g1k_v37.fasta",
  #singularity file
	"singularity":"/proj/sens2019010/nobackup/wharf/jesperei/jesperei-sens2019010/Clevervulture2.sif",
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
