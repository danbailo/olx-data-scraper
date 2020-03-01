import urllib.request
import os
import re

def get_config(config = os.path.join(".", "config.txt")):
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
    for i in range(len(data[9])):
        if not os.path.isdir(os.path.join(".", "imgs", str(data[0]))):
            os.mkdir(os.path.join(".", "imgs", str(data[0])))
        urllib.request.urlretrieve(data[9][i], os.path.join(".", "imgs", str(data[0]), str(data[0])+"_"+str(i)+".jpg"))
    return len(data[9])