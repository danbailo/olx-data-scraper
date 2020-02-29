from core import Olx, Database
from tqdm import tqdm
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from utils import get_config
from datetime import datetime
from datetime import timedelta
import json
import time
import os

if __name__ == "__main__":

    first_exec = True
    count_exec = 1

    input_file = os.path.join("..", "input.txt")
    database = Database("mydb", "postgres", "59228922ddd")
    olx = Olx()

    try:
        while True:

            if not first_exec:
                days, download = get_config()
                next_exec = datetime.now() + timedelta(seconds=int(days))

                print("Próxima execução {next_exec}".format(next_exec=next_exec.strftime("%T")))
                while datetime.now() < next_exec:
                    pass

            all_urn = olx.get_urn(input_file)

            print("\nColetando as páginas dos anúncios...")
            pages = olx.get_pages(all_urn)
            print("{len_pages} Páginas coletadas!".format(len_pages=len(pages)))

            print("\nColetando os links de cada anúncio nas páginas coletadas...")
            links = olx.get_links(pages)

            print("{len_links} Links coletados!".format(len_links=len(links)))
            olx.unique_id = 0

            process_pool = Pool(32)
            print("\nExtraindo os dados dos anúncios...")
            data = process_pool.map(olx.get_json, tqdm(links.values()))
            process_pool.close()
            process_pool.join()
            del process_pool
            print("Dados extraidos!")

            print("\nInserindo dados no banco...")
            database.insert_data(data)
            print("Dados inseridos!")

            set_data = set()
            for row in data:
                set_data.add(row[0])

            print("\nForam inseridos {set_data} tuplas na base dados!".format(set_data=len(set_data)))
            print("{duplicate} anúncios duplicados no total!\n".format(duplicate=len(data) - len(set_data)))

            count_exec += 1
            first_exec = False
    except KeyboardInterrupt:
        print("\nPrograma finalizado!\n")
        database.close()
    
    
