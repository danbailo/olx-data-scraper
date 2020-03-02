from core import Olx, Database
from tqdm import tqdm
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from utils import get_config, download_imgs
from datetime import datetime
from datetime import timedelta
from termcolor import colored
import urllib.request
import json
import time
import os

if __name__ == "__main__":

    first_exec = True
    count_exec = 1

    database = Database()
    olx = Olx()  

    if not os.path.isdir(os.path.join("imgs")):
        os.mkdir(os.path.join("imgs"))

    try:
        while True:
            input_file = os.path.join(".","input.txt")

            config = get_config()
            days = config[0]
            download_opt = config[1].upper()
            
            db_config = database.get_config()
            db = db_config[0]
            user = db_config[1]
            password = db_config[2]
            host = db_config[3]

            print("\n# Pressione ctrl+c para finalizar o programa!\n")
            print("Execução nº {n_exec}".format(n_exec=colored(str(count_exec), "yellow")))
            if download_opt == "ON":
                download_color = "green"
                download = True
            else:
                download_color = "red"
                download = False

            print("Download de imagens: {download}".format(download=colored(download_opt, download_color)))

            if not first_exec:                
                next_exec = datetime.now() + timedelta(days=int(days))

                print("\nPróxima execução {next_exec}.".format(next_exec=colored(next_exec.strftime("%d/%m/%Y"), "blue")))
                while datetime.now() < next_exec:
                    pass

            all_urn = olx.get_urn(input_file)

            print("\nColetando as páginas dos anúncios...")
            pages = olx.get_pages(all_urn)
            print("{len_pages} Páginas coletadas!".format(len_pages=len(pages)))

            print("\nColetando os links de cada anúncio nas páginas coletadas...")
            links_pool = Pool(8)
            links = {}
            for link in links_pool.map(olx.get_links, pages):
                links.update(link)

            links_pool.close()
            links_pool.join()        
            del links_pool   
            print("{len_links} Links coletados!".format(len_links=len(links)))

            data_pool = Pool(32)
            print("\nExtraindo os dados dos anúncios...")
            data = data_pool.map(olx.get_json, tqdm(links.values(), desc="Anúncios"))
            data_pool.close()
            data_pool.join()
            del data_pool
            print("Dados extraidos!")

            connect = database.connect(db, user, password, host)
            cursor = connect.cursor()

            if first_exec:
                database.create_table(cursor)

            print("\nInserindo dados no banco...")
            database.insert_data(cursor, data)
            connect.commit()
            print("Dados inseridos!")

            database.close(connect, cursor)

            print("\nForam inseridos {unique_data} tuplas na base dados!".format(unique_data=len(data)))

            total_imgs = 0
            if download:
                print("\nRealizando download das imagens...")
                total_imgs = download_imgs(data)
                print("Download concluído!")
                print("\nNo total, foi realizado o download de {total_imgs} imagens!".format(total_imgs=total_imgs))

            print(colored("SUCESSO!", "green"))

            count_exec += 1
            first_exec = False
    except KeyboardInterrupt:
        print("\n\nPrograma finalizado!")    
    
