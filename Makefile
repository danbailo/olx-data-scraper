.PHONY: help prepare-dev test lint run doc
PYTHON=/usr/bin/python3

.DEFAULT: help
help:
	@echo "make prepare-dev"
	@echo "       Prepara ambiente de desenvolvimento, use apenas uma vez.\n"
	@echo "make config"
	@echo "       Executa o módulo de configuração do programa principal.\n"	
	@echo "make db-config"
	@echo "       Executa o módulo de configuração do banco de dados.\n"		
	@echo "make run"
	@echo "       Executa o programa principal\n"

prepare-dev:
	sudo apt install python3 python3-pip python3-psycopg2 postgresql postgresql-contrib -y 
	${PYTHON} -m pip install -U pip --user
	${PYTHON} -m pip install -r requirements.txt --user

config:
	${PYTHON} src/config.py

db-config:
	${PYTHON} src/db_config.py

db-conn-test:
	${PYTHON} src/db_test.py	

run: src
	${PYTHON} src/main.py
