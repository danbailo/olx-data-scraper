from termcolor import colored
import os

print("\n# Pressione ctrl+c para finalizar o programa!")

print("\n{msg}".format(msg=colored("Módulo de configuração do banco de dados.", "blue")))

try:
	while True:
			db = input("\nDigite o nome do banco de dados> ")
			user = input("\nDigite o nome do usuário banco de dados> ")
			password = input("\nDigite a senha deste usuário do banco de dados> ")
			host = input("\nDigite o nome do banco de dados (padrão: localhost)> ")
			if host == "":
				host = "localhost"

			option = " "
			while option[0].lower() not in ["s", "n"]:
				option = input("\nDeseja alterar alguma informação inserida, [s]im ou [n]ão/Enter?>")
				if option == "":
					option = "n"
			if option[0].lower() == "n" or option=="": break
except KeyboardInterrupt:
	print("\n\nPrograma finalizado!")
	exit()

with open(os.path.join("config", "db_config.txt"), "w") as file:
	file.write("Banco de dados: {db}\n".format(db=db))
	file.write("Usuário: {user}\n".format(user=user))
	file.write("Senha: {password}\n".format(password=password))
	file.write("Host: {host}\n".format(host=host))

print("\nArquivo de configuração gravado com {success}!\n".format(success=colored("SUCESSO", "green")))