if [ ! -d "/home/appuser/miniconda/bin" ]
then
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /home/appuser/miniconda.sh
    sh /home/appuser/miniconda.sh -b -u -p /home/appuser/miniconda
    rm /home/appuser/miniconda.sh
fi

/home/appuser/miniconda/bin/conda update conda -y
