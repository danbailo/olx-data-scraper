from termcolor import colored
import os

"""
	Configura o arquivo de entrada do programa principal.
"""

print("\n# Pressione ctrl+c para finalizar o programa!")


print("\n{msg}".format(msg=colored("Módulo de configuração do arquivo de entrada.", "blue")))

print("\nObs: Links duplicados serão ignorados.")

old_links = set()

while True:
	method = input("\nDeseja sobrescrever o arquivo de entrada ou adicionar os novos links abaixo? [1]sobrescrever ou [2]abaixo >")
	if method not in ["1", "2"]:
		print("Por favor, entre com 1 ou 2!")
		continue
	else: break

if method == "1": method = "w"
elif method == "2":
	method = "a"
	with open(os.path.join(".", "input.txt")) as file:
		for line in file:
			if line == "\n": continue
			if line[-1] == "\n":
				old_links.add(line[:-1])

new_links = set()

try:
	while True:
		while True:
			link = input("\nDigite o link de coleta da OLX> ")
			new_links.add(link)
			option_link = " "
			while option_link[0].lower() not in ["s", "n"]:
				option_link = input("\nDeseja adicionar mais algum link? [s]im ou [n]ão/Enter?>")
				if option_link == "":
					option_link = "n"
			if option_link[0].lower() == "n" or option_link=="": break
			else: continue

		option = " "
		while option[0].lower() not in ["s", "n"]:
			option = input("\nDeseja alterar alguma informação inserida, [s]im ou [n]ão/Enter?>")
			if option == "":
				option = "n"
		if option[0].lower() == "n" or option=="": break

except KeyboardInterrupt:
	print("\n\nPrograma finalizado!")
	exit()

except EOFError:
	print("\n\nPrograma finalizado!")
	exit()

with open(os.path.join(".", "input.txt"), method) as file:
	for link in new_links - old_links:
		file.write(link + "\n")

print("\nArquivo de configuração gravado com {success}!\n".format(success=colored("SUCESSO", "green")))