"""Code to build commands"""

import pathlib


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
