from core import Olx, Database
import os
import json
import time
from multiprocessing import Pool

if __name__ == "__main__":

    path = os.path.join(".", "input.txt")
    db = Database("mydb", "postgres", "59228922ddd")

    olx = Olx(path)

    all_urn = olx.get_urn()


    print("\nColetando todas as paginas...")
    pages = olx.get_pages(all_urn)
    print("{len_pages} Paginas coletadas!".format(len_pages=len(pages)))

    print("\nColetando links de todos os anuncios...")
    pool = Pool(8)
    start_links = time.time() #TIMER
    links = []
    for link in pool.map(olx.get_links, pages):
        links.extend(link)
    pool.close()
    pool.join()        
    end_links = time.time() #TIMER
    del pool   

    print("{len_links} Links coletados!\n".format(len_links=len(links)))
    print("time to get links:", end_links-start_links)

    pool = Pool(32)

    print("\nColetando dados dos anuncios...")
    start_collect = time.time() #TIMER
    data = pool.map(olx.get_json, links)
    pool.close()
    pool.join()
    end_collect = time.time() #TIMER
    print("Dados coletados!\n")
    print("time collect:", end_collect-start_collect)

    del pool

    print("\nInserindo dados no banco...")
    db.insert_data(data)
    print("Dados inseridos!\n")
    
    
