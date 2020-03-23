Bootstrap: docker
From: ubuntu:16.04

%environment
SHELL=/bin/bash
PATH=/opt/anaconda/bin:${PATH}
LC_ALL=C.UTF-8

%runscript
    echo "This is what happens when you run the container..."
    export PATH=/opt/anaconda/bin:${PATH}    

%post
    echo "Hello from inside the container"
    apt-get update
    apt-get -y install wget git bzip2 build-essential gcc zlib1g-dev language-pack-en-base apt-transport-https make cmake unzip python3 sudo python2.7 python-numpy python-matplotlib python-biopython samtools
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

    cd /root/ && wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
    cd /root/ && chmod 700 ./Miniconda2-latest-Linux-x86_64.sh
    cd /root/ && bash ./Miniconda2-latest-Linux-x86_64.sh -b -p /opt/anaconda/

    export PATH=/opt/anaconda/bin:${PATH}

    conda config --add channels defaults
    conda config --add channels conda-forge
    conda config --add channels bioconda
    conda config --add channels r

    conda install -f -c conda-forge -c bioconda wisecondorx
    pip install -U git+https://github.com/CenterForMedicalGeneticsGhent/WisecondorX
    conda install r-ichorcna
    conda install -c bioconda samtools bwa sambamba minimap2 picard
    conda install -c bioconda biobambam
    
    conda install -c conda-forge r-base
    conda install -c r r-doparallel r-foreach r-neuralnet r-glmnet r-data.table r-mass

    pip install sklearn numpy scipy matplotlib pysam futures bottleneck cython
    cd /bin/ &&  git clone https://github.com/VUmcCGP/wisecondor.git    
    
    cd /bin/ && wget https://github.com/CenterForMedicalGeneticsGhent/PREFACE/archive/v0.1.1.zip && unzip v0.1.1.zip
    cd /

    cd /bin/ && git clone https://github.com/J35P312/AMYCNE.git && cd AMYCNE && python setup.py build_ext --inplace    
    
    git clone https://github.com/SciLifeLab/TIDDIT.git
    mv TIDDIT/* /bin/
    cd /bin/ && ./INSTALL.sh
    chmod +x /bin/TIDDIT.py

    cd /bin/ && git clone https://github.com/J35P312/FluFFyPipe.git
