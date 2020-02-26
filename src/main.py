from core import Olx, Database
import os
import json
import time
from tqdm import tqdm
from multiprocessing import Pool

if __name__ == "__main__":

    input_file = os.path.join(".", "input.txt")
    database = Database("mydb", "postgres", "59228922ddd")

    olx = Olx()

    all_urn = olx.get_urn(input_file)

    print("\nColetando todas as paginas...")
    pages = olx.get_pages(all_urn)
    print("{len_pages} Paginas coletadas!".format(len_pages=len(pages)))

    print("\nColetando links de todos os anuncios...")
    pool = Pool(8)
    links = []
    for link in pool.map(olx.get_links, pages):
        links.extend(link)
    pool.close()
    pool.join()        
    del pool   
    print("{len_links} Links coletados!".format(len_links=len(links)))


    pool = Pool(32)
    print("\nColetando dados dos anuncios...")
    data = pool.map(olx.get_json, tqdm(links))
    pool.close()
    pool.join()
    del pool
    print("Dados coletados!\n")

    print("\nInserindo dados no banco...")
    database.insert_data(data)
    print("Dados inseridos!\n")

    set_data = set()
    for row in data:
        set_data.add(row[0])

    print("Foram inseridos {set_data} tuplas na base dados!".format(set_data=len(set_data)))
    print("{duplicate} anuncios duplicados no total!\n".format(duplicate=len(data) - len(set_data)))
    
    
