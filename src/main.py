from core import Olx, Database
import os
import json

if __name__ == "__main__":
    
    path = os.path.join(".", "input.txt")
    db = Database("mydb", "postgres", "59228922ddd")

    olx = Olx(path)
    all_urn = olx.get_urn()
    pages = olx.get_pages(all_urn)
    links = olx.get_links(pages)

    print(*links.items(), sep="\n")

    print(len(links))

    exit()

    print("\nColetando dados...")
    olx.get_json(links)
    print("Dados coletados!\n")

    print("Inserindo dados no banco...")
    db.insert_data(list(olx.data.values()))
    print("Dados inseridos!")
    
    
