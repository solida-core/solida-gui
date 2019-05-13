if [ ! -d "/root/miniconda" ]
then
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda.sh
    sh /root/miniconda.sh -b -u -p /root/miniconda
    rm /root/miniconda.sh
fi
ln -s /root/miniconda/bin/conda /usr/local/bin/conda
conda update conda -y
