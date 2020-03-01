.PHONY: help prepare-dev test lint run doc
PYTHON=/usr/bin/python3

.DEFAULT: help
help:
	@echo "make prepare-dev"
	@echo "       Prepara ambiente de desenvolvimento, use apenas uma vez."
	@echo "make config"
	@echo "       Executa o módulo de configuração do programa principal."	
	@echo "make run"
	@echo "       run project"

prepare-dev:
	sudo apt install python3 python3-pip -y
	${PYTHON} -m pip install -U pip --user
	${PYTHON} -m pip install -r requirements.txt --user

config:
	${PYTHON} src/config.py

config-db:
	${PYTHON} src/db_config.py	

run: src
	${PYTHON} src/main.py