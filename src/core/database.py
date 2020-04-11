from tqdm import trange
import psycopg2
import re
import os

class Database:
	"""
		Classe responsável por manipular o banco de dados.
	"""	
	def get_config(self, config = os.path.join("config", "db_config.txt")):
		"""
			Pega a configuração do banco de dados contido no arquivo db_config.txt.
		"""			
		pattern_config = re.compile(r"(.*\:\s)(.*)")
		with open(config, "r") as file:
			options = []
			for line in file:
				info = pattern_config.match(line)[2]
				options.append(info)
		return options        

	def connect(self, database, user, password, host):
		"""
			Conecta no banco de dados.
		"""			
		return psycopg2.connect(
			dbname=database,
			user=user,
			password=password,
			host=host)
		
	def create_table(self, cursor):
		"""
			Cria a tabela no banco de dados.
		"""			
		cursor.execute("""
				CREATE TABLE IF NOT EXISTS dados_olx (
					id_anuncio BIGINT,
					municipio VARCHAR(64),
					estado CHAR(2),
					cep CHAR(8),
					preco NUMERIC(14,2),
					area VARCHAR(16),
					tipo VARCHAR(32),
					titulo TEXT,
					descricao TEXT,
					fotos TEXT [],
					ddd CHAR(2),
					telefone VARCHAR(16),
					url TEXT,
					data TIMESTAMPTZ,
					profissional BOOL,
					PRIMARY KEY (id_anuncio)
				); """
			)        

	def insert_data(self, cursor, data):
		"""
			Insere os dados coletados no base de dados.
		"""			
		for i in trange(len(data), desc="Anúncios"):
			try:
				id_anuncio = data[i][0]
				if id_anuncio is int(): #If the data were not found!
					continue				
				municipio = data[i][1]
				estado = data[i][2]
				cep = data[i][3]
				area = data[i][5]
				tipo = data[i][6]
				titulo = data[i][7]
				descricao = data[i][8]
				fotos = data[i][9]
				ddd = data[i][10]
				telefone = data[i][11]
				url = data[i][12]
				data_ = data[i][13]
				profissional = data[i][14]
				preco = re.sub(r"(R\$\s|\.)", "", data[i][4])
			except TypeError:
				preco = "0"
			cursor.execute("""
				INSERT INTO dados_olx 
				(id_anuncio, municipio, estado, cep, preco, area, tipo, titulo, descricao, fotos, ddd, telefone, url, data, profissional) 
				VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id_anuncio) 
				DO UPDATE SET 
				(id_anuncio, municipio, estado, cep, preco, area, tipo, titulo, 
				descricao, fotos, ddd, telefone, url, data, profissional) = 
				(EXCLUDED.id_anuncio, EXCLUDED.municipio, EXCLUDED.estado, EXCLUDED.cep, EXCLUDED.preco, EXCLUDED.area, EXCLUDED.tipo, EXCLUDED.titulo, 
				EXCLUDED.descricao, EXCLUDED.fotos, EXCLUDED.ddd, EXCLUDED.telefone, EXCLUDED.url, EXCLUDED.data, EXCLUDED.profissional);""",
				(id_anuncio, municipio, estado, cep, preco, area, tipo, titulo, descricao, fotos, ddd, telefone, url, data_, profissional)
			)

	def close(self, cursor, connection):
		"""
			Fecha a conexão com o banco de dados.
		"""				
		cursor.close()
		connection.close()