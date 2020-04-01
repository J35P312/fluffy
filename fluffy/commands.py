"""Code to build commands"""

import pathlib


# perform the wisecondorx test
def wisecondorx_test(config, args, sample):

    out_prefix = "{}/{}/{}".format(args.out, sample, sample)
    wcx_test = "singularity exec {} WisecondorX --loglevel info predict {}.bam.wcx.npz {} {}.WCXpredict --plot --bed --blacklist {} --zscore {}".format(
        config["singularity"],
        out_prefix,
        config["wisecondorx"]["reftest"],
        out_prefix,
        config["wisecondorx"]["blacklist"],
        config["wisecondorx"]["zscore"],
    )
    wcx_preface = "singularity exec {} WisecondorX --loglevel info predict {}.bam.wcx.npz {} {}.WCXpredict.preface --plot --bed --blacklist {}".format(
        config["singularity"],
        out_prefix,
        config["wisecondorx"]["refpreface"],
        out_prefix,
        config["wisecondorx"]["blacklist"],
    )
    gender = "singularity exec {} WisecondorX gender {}.bam.wcx.npz {} > {}.wcx.npz.gender.txt".format(
        config["singularity"], out_prefix, config["wisecondorx"]["reftest"], out_prefix
    )
    return "\n".join([wcx_test, gender, wcx_preface])


# fetal fraction estimation using tiddit and AMYCNE
def amycne_ffy(config, args, sample):
    out_prefix = "{}/{}/{}".format(args.out, sample, sample)
    path_gc_tab = "{}/{}/{}.gc.tab".format(args.out, sample, sample)
    tiddit = "singularity exec {} python /bin/TIDDIT.py --cov --bam {}.bam -z {} -o {}.tiddit".format(
        config["singularity"], out_prefix, config["tiddit"]["binsize"], out_prefix
    )
    gc_tab = "singularity exec FluFFyPipe_0.0.sif python /bin/AMYCNE/Generate_GC_tab.py --fa {} --size {} --n_mask > {}".format(
        config["reference"], config["tiddit"]["binsize"], path_gc_tab
    )
    amycne = "singularity exec {} python /bin/AMYCNE/AMYCNE.py --ff --coverage {}.tiddit.tab --gc {} --Q {} > {}.tiddit.AMYCNE.tab".format(
        config["singularity"],
        out_prefix,
        path_gc_tab,
        config["amycne"]["minq"],
        out_prefix,
    )
    return "\n".join([tiddit, gc_tab, amycne])


# collect QC stats using picard tools
def picard_qc(config, args, sample):
    out_prefix = "{}/{}/{}".format(args.out, sample, sample)
    picard_gc = "singularity exec {} picard CollectGcBiasMetrics I={}.bam O={}_gc_bias_metrics.txt CHART={}_gc_bias_metrics.pdf S={}.gc.summary.tab R={} {}".format(
        config["singularity"],
        out_prefix,
        out_prefix,
        out_prefix,
        out_prefix,
        config["reference"],
        config["picard"]["javasettings"],
    )
    picard_insert = "singularity exec {} picard CollectInsertSizeMetrics I={}.bam O={}_insert_size_metrics.txt H={}_insert_size_histogram.pdf M=0.5 {}".format(
        config["singularity"],
        out_prefix,
        out_prefix,
        out_prefix,
        config["picard"]["javasettings"],
    )
    picard_complexity = "singularity exec {} picard EstimateLibraryComplexity I={}.bam O={}_complex_metrics.txt {}".format(
        config["singularity"], out_prefix, out_prefix, config["picard"]["javasettings"]
    )
    return "\n".join([picard_gc, picard_insert, picard_complexity])


# construct Preface model
def preface_model(config, args):
    preface = "singularity exec {} Rscript /bin/PREFACE-0.1.1/PREFACE.R train --config {}.PREFACE.config.tab --outdir {} {}".format(
        config["singularity"],
        args.out.rstrip("/"),
        config["preface"]["model_dir"],
        config["preface"]["modelsettings"],
    )
    return preface


# generate a csv summary
def summarise(config, args):
    summary = "singularity exec {} python /bin/FluFFyPipe/scripts/generate_csv.py --folder {} --samplesheet {} --Zscore {} --minCNV {} > {}/{}.summary.csv".format(
        config["singularity"],
        args.out,
        args.sample,
        config["summary"]["zscore"],
        config["summary"]["mincnv"],
        args.out,
        args.out.strip("/").split("/")[-1],
    )
    return summary
