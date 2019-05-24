# solida-gui

Container Docker application that facilitate the reproducibility and portability of NGS pipelines.
It can easily organize the deployment, the data management and the execution 
of a Snakemake based workflow

solida-gui container include:
- [solida](https://github.com/solida-core/solida): Python command-line tool 
- Graphical User Iterface developed in Django


## Requirements

You need [docker-engine](https://docs.docker.com/engine/installation/) 
and [docker-compose](https://docs.docker.com/compose/install/)  
See [docker-compose docs](https://docs.docker.com/compose/reference/overview/)

For deploying in remote host see [sss-keygen](https://www.ssh.com/ssh/keygen/)

## Quick start

Create the workdir tree:
```bash
mkdir ~/solida-core             # root path 
mkdir ~/solida-core/config      # path for configuration files
mkdir ~/solida-core/projects    # path where deploying projects in localhost
mkdir ~/solida-core/profiles    # path where storing profiles in localhost
mkdir ~/solida-core/.tmp        # path where storing temporary files 
```

> You can change these paths as you prefer, but remember to modify docker-compose.yaml file accordly
> ```yaml
> ...
> volumes:
>      - ~/solida-core/projects:/root/projects
>      - ~/solida-core/.tmp:/root/.tmp
>      - ~/solida-core/profiles:/root/.local/share/solida/
>      - ~/solida-core/config:/root/.config/solida
> ...


Clone the repository:  
```bash
git clone https://github.com/ratzeni/solida-gui.git
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
