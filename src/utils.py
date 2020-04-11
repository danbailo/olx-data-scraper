import requests
import time
import os
import re

def get_config(config = os.path.join("config", "config.txt")):
	"""
		Pega a configuração para executar o programa principal, contida no arquivo config.txt.
	"""	
	pattern_options = re.compile(r"(.*\:\s|.*\:)(.*?)((\s\#.*)|(\#.*))")
	with open(config, "r") as file:
		options = []
		for line in file:
			info = pattern_options.match(line)[2]
			options.append(info)
	if options[1].lower() not in ["on", "off"]:
		print('\nPor favor, escreva somente "on" ou "off" na configuração de download!\n')
		exit()
	return options

def download_imgs(data):
	"""
		Realiza o download das imagens, salvando em pastas separadas, onde o nome de cada pasta e o ID do anúncio.
	"""		
	len_total = 0
	for i in range(len(data[9])):
		if not os.path.isdir(os.path.join(".", "imgs", str(data[0]))):
			os.mkdir(os.path.join(".", "imgs", str(data[0])))
		request_error = 0
		while True:
			try:
				response = requests.get(data[9][i])
				format_img = "." + data[9][i].split(".")[-1]
				break
			except Exception:
				request_error += 1
				time.sleep(10)
				if request_error > 5:
					print("Request error")
					exit()
		try:
			path = os.path.join(".", "imgs", str(data[0]), str(data[0])+"_"+str(i)) + format_img
			with open(path, "wb") as file:
				file.write(response.content)
			len_total += 1
		except Exception:
			pass
	return len_total

def write_log(info):
	file = open("log.txt", "a")
	file.write("Execução nº {n_exec}\n\n".format(n_exec = info["number_exec"]))
	file.write("Data da última execução {curr_exec}\n\n".format(curr_exec = info["curr_exec"].strftime("%d/%m/%Y")))
	file.write("Próxima execução {next_exec}\n\n".format(next_exec = info["next_exec"].strftime("%d/%m/%Y")))
	file.write("{len_pages} Páginas coletadas!\n".format(len_pages = info["len_pages"]))
	file.write("{len_links} Links coletados!\n".format(len_links = info["len_links"]))
	file.write("Foram inseridos {unique_data} tuplas na base dados!\n".format(unique_data = info["len_data"]))
	file.write("No total, foi realizado o download de {total_imgs} imagens!\n".format(total_imgs = info["total_imgs"]))
	file.write("\n###\n\n")
	file.close()