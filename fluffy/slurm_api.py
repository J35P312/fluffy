"""An API to slurm"""
import copy
import yaml
import time as pytime
from datetime import datetime

import logging
from pathlib import Path

from slurmpy import Slurm

LOG = logging.getLogger(__name__)

class SlurmAPI:
    """An API to SLURM"""

    def __init__(self,slurm_settings: dict, out_dir: Path):
        super(SlurmAPI, self).__init__()
        LOG.info("Initializing a slurm API")
        account=None
        if "account" in slurm_settings:
            account=slurm_settings["account"]
        if not isinstance(account, str):
            raise SyntaxError("Invalid account {}".format(account))
        self.account = account

        time=None
        if "time" in slurm_settings:
            time=slurm_settings["time"]

        if not isinstance(time, str):
            raise SyntaxError("Invalid time {}".format(time))
        if not len(time.split(":")) == 3:
            LOG.warning("Specify time on format hh:mm:ss")
            raise SyntaxError("Invalid time format {}".format(time))
        self.time = time
        if not isinstance(out_dir, Path):
            raise SyntaxError("Invalid out dir format {}".format(out_dir))

        self.log_dir = out_dir / "logs"
        self.sacct_dir = out_dir / "sacct"
        self.scripts_dir = out_dir / "scripts"
        self.out_dir=out_dir
        self.slurm_settings=copy.copy(slurm_settings)
        self.job = None
        self.jobids=[]

        current_time=datetime.now()
        self.analysis_time=f"{current_time.year}-{current_time.month}-{current_time.day}T{current_time.hour}:{current_time.minute}:{current_time.second}"

    def create_job(self, name: str, afterok: list = None, afternotok: list = None) -> Slurm:
        """Create a job for submitting to SLURM"""
        LOG.info("Create a slurm job with name %s", name)

        self.slurm_settings["dependency"]=[]
        if afterok:
            self.slurm_settings["dependency"].append( "afterok:{}".format( ":".join( str(dependency) for dependency in afterok)  ) )
        if afternotok:
            self.slurm_settings["dependency"].append( "afternotok:{}".format( ":".join( str(dependency) for dependency in afternotok)  ) )

        if self.slurm_settings["dependency"]:
            self.slurm_settings["dependency"]=",".join(self.slurm_settings["dependency"])
        else:
            del self.slurm_settings["dependency"]

        job = Slurm(
            name,
            self.slurm_settings,
            log_dir=str(self.log_dir),
            scripts_dir=str(self.scripts_dir),
        )
        return job

    def run_job(
        self, name: str, command: str, afterok: list = None, afternotok: list = None, dry_run: bool = False
    ) -> int:
        """Create and submit a job to slurm"""
        job = self.create_job(name=name,afterok=afterok,afternotok=afternotok)
        LOG.info("Submitting commands %s", command)
        if afterok:
            LOG.info("Adding dependencies: %s", ",".join( str(dependency) for dependency in afterok))
        jobid = 1

        time_string=self.analysis_time
        on_finnish=""
        if len(self.jobids):
            #pytime.sleep(1)
            on_finnish="""
finnish(){{
sacct --format=jobid,jobname%50,account,partition,alloccpus,TotalCPU,elapsed,start,end,state,exitcode --jobs {} | perl -nae \'my @headers=(jobid,jobname,account,partition,alloccpus,TotalCPU,elapsed,start,end,state,exitcode); if($. == 1) {{ print q{{#}} . join(qq{{\\t}}, @headers), qq{{\\n}} }} if ($. >= 3 && $F[0] !~ /( .batch | .bat+ )\\b/xms) {{ print join(qq{{\\t}}, @F), qq{{\\n}} }}\' > {}/fluffy_{}.log.status
}}

failure(){{
sed -i \'s/ \"running\"/ \"fail\"/g\' {}/analysis_status.json
}}

trap finnish EXIT TERM INT
trap failure ERR TERM

""".format(",".join(self.jobids),self.sacct_dir,time_string,self.out_dir )

        if not dry_run:               
            jobid = job.run("\n".join([on_finnish, command]))
        LOG.info("Submitted job %s with job id: %s", name, jobid)

        self.jobids.append( str(jobid) )

        return jobid

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(account={self.account!r}, time={self.time!r}, "
            f"log_dir={self.log_dir!r}, scripts_dir={self.scripts_dir!r})"
        )


    def print_submitted_jobs(self,dry_run: bool = False):

        project_id=str(self.out_dir).strip("/").split("/")[-1]
        try:
            yaml_out=yaml.dump({project_id:[int(i) for i in self.jobids]})
        except:
            yaml_out=yaml.dump({project_id:self.jobids})
        if not dry_run:
            f=open("{}//submitted_jobs.yaml".format(self.sacct_dir),"w")
            f.write(yaml_out)
            f.close()
