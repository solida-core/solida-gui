# solida-gui
[![Travis](https://api.travis-ci.com/solida-core/solida-gui.svg?branch=master)](https://travis-ci.com/solida-core/solida-gui)

Container Docker application that facilitate the reproducibility and portability of NGS pipelines.
It can easily organize the deployment, the data management and the execution 
of a Snakemake based workflow

solida-gui container include:
- [solida](https://github.com/solida-core/solida): Python command-line tool 
- Graphical User Interface developed in Django


## Requirements

You need [docker-engine](https://docs.docker.com/engine/installation/) 
and [docker-compose](https://docs.docker.com/compose/install/)  
See [docker-compose docs](https://docs.docker.com/compose/reference/overview/)

For deploying in remote host see [ssh-keygen](https://www.ssh.com/ssh/keygen/)

## Quickstart

The first execution could require several minutes, from the second one will be faster.

### Using the Makefile

Print the help message
```bash
make help
```

Bring up the solida-gui app
```bash
make start
```

Bring down the solida-gui app
```bash
make stop
```

### Manually

Create the workdir tree:
```bash
mkdir ~/solida-core             # root path 
mkdir ~/solida-core/config      # path for configuration files
mkdir ~/solida-core/projects    # path where deploying projects in localhost
mkdir ~/solida-core/profiles    # path where storing profiles in localhost
mkdir ~/solida-core/.tmp        # path where storing temporary files
mkdir ~/solida-core/.miniconda  # path where install miniconda
mkdir ~/solida-core/.cache      # Solida cache path
```

> You can change these paths as you prefer, but remember to modify docker-compose.yaml file accordly
> ```yaml
> ...
> volumes:
>      - ~/solida-core/projects:/home/appuser/projects
>      - ~/solida-core/.tmp:/home/appuser/.tmp
>      - ~/solida-core/profiles:/home/appuser/.local/share/solida/
>      - ~/solida-core/config:/home/appuser/.config/solida
>      - ~/solida-core/.miniconda:/home/appuser/miniconda
>      - ~/solida-core/.cache:/home/appuser/.cache
> ...
> ```


Clone the repository:  
```bash
git clone https://github.com/solida-core/solida-gui.git
```

Cd into the docker directory:  
```bash
cd solida-gui
```
Bring up the containers:  
```bash
docker-compose up
```

Point your browser to: 
`http://0.0.0.0:8000` 
