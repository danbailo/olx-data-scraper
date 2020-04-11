from utils import get_config, download_imgs, write_log
from multiprocessing.pool import ThreadPool
from core import Olx, Database
from datetime import timedelta
from datetime import datetime
from termcolor import colored
import tqdm
import time
import os

if __name__ == "__main__":

	first_exec = True
	count_exec = 1

	database = Database()
	olx = Olx()  

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
			links_pool = ThreadPool(8)
			links = {}
			for link in list(tqdm.tqdm(links_pool.imap(olx.get_links, pages), total=len(pages), desc="Links")):
				links.update(link)
			del links_pool   
			print("{len_links} Links coletados!".format(len_links=len(links)))

			print("\nExtraindo os dados dos anúncios...")
			data_pool = ThreadPool(8)
			len_imgs = 0
			data = []
			for data_len in list(tqdm.tqdm(data_pool.imap(olx.get_json, links.values()), total=len(links), desc="Anúncios")):
				if data_len[0][0] is False: #If the data were not found!
					continue
				data.append(data_len[0])
				len_imgs += data_len[1]
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
				if not os.path.isdir(os.path.join("imgs")):
					os.mkdir(os.path.join("imgs"))                
				imgs_pool = ThreadPool(4)
				print("\nRealizando download das imagens...")
				for value in list(tqdm.tqdm(imgs_pool.imap(download_imgs, data), total=len_imgs, desc="Anúncios")):
					total_imgs += value
				del imgs_pool             
				print("Download concluído!")
				print("\nNo total, foi realizado o download de {total_imgs} imagens!".format(total_imgs=total_imgs))

			write_log({
				"number_exec": count_exec,
				"curr_exec": datetime.now(),
				"next_exec": datetime.now() + timedelta(days=int(days)),
				"len_pages": len(pages),
				"len_links": len(links),
				"len_data": len(data),
				"total_imgs": total_imgs}
				)			

			print("Arquivo de log gerado com {success}".format(success=colored("SUCESSO!", "green")))

			count_exec += 1
			first_exec = False

	except KeyboardInterrupt:
		print("\n\nPrograma finalizado!")    
	
