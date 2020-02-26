from core import Olx, Database
import os
import json
import time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool

if __name__ == "__main__":

    path = os.path.join(".", "input.txt")
    db = Database("mydb", "postgres", "59228922ddd")

    olx = Olx(path)

    
    all_urn = olx.get_urn()
    pages = olx.get_pages(all_urn)



    print("\nColetando links de todos os anuncios...")
    pool = ThreadPool(10)
    start_links = time.time() #TIMER
    links = {}
    for link in pool.map(olx.get_links, pages):
        links.update(link)
    end_links = time.time() #TIMER

    del pool   
    print("{len_links} Anuncios coletados!\n".format(len_links=len(links)))
    print("time to get links:", end_links-start_links)

    pool = ThreadPool(32)

    print("Coletando dados dos anuncios...")
    start_collect = time.time() #TIMER
    pool.map(olx.get_json, links.values())
    end_collect= time.time() #TIMER
    print("Dados coletados!\n")
    print("time collect\n:", end_collect-start_collect)

    del pool
    
    print("Inserindo dados no banco...")
    db.insert_data(list(olx.data.values()))
    print("Dados inseridos!\n")
    
    
