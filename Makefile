.PHONY: help prepare-dev test lint run doc
PYTHON=/usr/bin/python3

.DEFAULT: help
help:
	@echo "make prepare-dev"
	@echo "       Prepara ambiente de desenvolvimento, use apenas uma vez.\n"
	@echo "make config"
	@echo "       Executa o módulo de configuração do programa principal.\n"	
	@echo "make config-db"
	@echo "       Executa o módulo de configuração do banco de dados.\n"		
	@echo "make run"
	@echo "       Executa o programa principal\n"

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