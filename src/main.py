from core import Olx, Database
import os
import json

if __name__ == "__main__":
    
    path = os.path.join(".", "input.txt")

    olx = Olx(path)

    db = Database("mydb", "postgres", "59228922ddd")

    all_urn = olx.get_urn()
    links = olx.get_links(all_urn)

    print("Colentado dados...")
    olx.get_json(links)

    print(json.dumps(olx.data, indent=4, ensure_ascii=False))

    db.insert_data(olx.data)