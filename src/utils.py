import PIL
from PIL import Image
import requests
import warnings
import io
import os
import re
import time
from tqdm import tqdm

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
    for imgs in tqdm(data, desc="Anúncios"):
        for i in range(len(imgs[9])):
            if not os.path.isdir(os.path.join(".", "imgs", str(imgs[0]))):
                os.mkdir(os.path.join(".", "imgs", str(imgs[0])))            
            if imgs[9][i][-4:] == ".jpg":
                request_error = 0
                while True:
                    try:
                        response = requests.get(imgs[9][i])
                        break
                    except Exception:
                        request_error += 1
                        time.sleep(10)
                        if request_error > 5:
                            print("Request error")
                            exit()
                try:
                    img = Image.open(io.BytesIO(response.content))
                    #img = Image.open(io.BytesIO(response.content)).convert('RGB')#
                    img.save(os.path.join(".", "imgs", str(imgs[0]), str(imgs[0])+"_"+str(i))+".jpeg", "JPEG")
                except Exception:
                    print("img error")
        len_total += len(imgs[9])
    return len_total             

# def download_imgs(data):
#     for i in range(len(data[9])):
#         if not os.path.isdir(os.path.join(".", "imgs", str(data[0]))):
#             os.mkdir(os.path.join(".", "imgs", str(data[0])))
#         response = requests.get(data[9][i])
#         try:
#             img = Image.open(io.BytesIO(response.content)).convert('RGB')
#             img.save(os.path.join(".", "imgs", str(data[0]), str(data[0])+"_"+str(i)), "JPEG")
#         except Exception:
#             print("img error")
#     return len(data[9])    
