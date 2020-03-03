import requests
import warnings
import time
import os
import re

warnings.filterwarnings("ignore")

def get_config(config = os.path.join("config", "config.txt")):
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
	len_total = 0
	for i in range(len(data[9])):
		if not os.path.isdir(os.path.join(".", "imgs", str(data[0]))):
			os.mkdir(os.path.join(".", "imgs", str(data[0])))
		request_error = 0
		while True:
			try:
				response = requests.get(data[9][i])
				break
			except Exception:
				request_error += 1
				time.sleep(10)
				if request_error > 5:
					print("Request error")
					exit()
		try:
			path = os.path.join(".", "imgs", str(data[0]), str(data[0])+"_"+str(i))+".jpg"
			with open(path, "wb") as file:
				file.write(response.content)
			len_total += 1
		except Exception as err:
			print(err)
			print(err.__class__)
			print()
	return len_total