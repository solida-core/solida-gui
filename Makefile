DEFAULT_SOLIDA_CORE_ROOT=~/solida-core
USERID=$(shell id -u)
GROUPID=$(shell id -g)

ifndef SOLIDA_CORE_ROOT
override SOLIDA_CORE_ROOT = ${DEFAULT_SOLIDA_CORE_ROOT}
endif

help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "  start                   bring up the solida-gui app"
	@echo "  stop                    bring down the solida-gui app"
	@echo "  clean                   remove solida-gui from your computer"
	@echo "  "
	@echo "  Solida-gui will be deployed into ${DEFAULT_SOLIDA_CORE_ROOT}"
	@echo "  To set a different path, digit: "
	@echo "  make SOLIDA_CORE_ROOT=/your/path <target>"
	@echo "  "


init:
	mkdir -p ${SOLIDA_CORE_ROOT}/config
	mkdir -p ${SOLIDA_CORE_ROOT}/projects
	mkdir -p ${SOLIDA_CORE_ROOT}/profiles
	mkdir -p ${SOLIDA_CORE_ROOT}/.tmp
	mkdir -p ${SOLIDA_CORE_ROOT}/.miniconda
	mkdir -p ${SOLIDA_CORE_ROOT}/.cache

	sed -i 's|${DEFAULT_SOLIDA_CORE_ROOT}|${SOLIDA_CORE_ROOT}|g' docker-compose.yml 

start: init
	docker-compose build --build-arg USER_ID=${USERID} --build-arg GROUP_ID=${GROUPID}
	docker-compose up -d
	echo "Point your browser to: http://0.0.0.0:8000"

stop:
	docker-compose down

clean: stop
	docker rmi solida-gui_web:latest
	rm -rf 	${SOLIDA_CORE_ROOT}
