import psycopg2
import re
from tqdm import trange

class Database:    
    def __init__(self, dbname, user, password):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host="localhost")
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS mytable (
                    id_anuncio INTEGER,
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
        self.conn.commit()

    def insert_data(self, data):
        for i in trange(len(data)):
            try:
                new_price = re.sub(r"(R\$\s|\.)", "", data[i]["preco"])
            except TypeError:
                new_price = "0"
            self.cur.execute("""
                INSERT INTO mytable (id_anuncio, municipio, estado, cep, preco, area, tipo, titulo, descricao, fotos, ddd, telefone, url, data, profissional)
                VALUES(%s, %s, %s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s, %s ,%s);""",                
                #VALUES(%s, %s, %s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s, %s ,%s) ON CONFLICT (id_anuncio) DO NOTHING;""",                
                (data[i]["id_anuncio"],
                data[i]["municipio"],
                data[i]["estado"],
                data[i]["cep"],
                new_price,
                data[i]["area"],
                data[i]["tipo"],
                data[i]["titulo"],
                data[i]["descricao"],
                data[i]["fotos"],
                data[i]["ddd"],
                data[i]["telefone"],
                data[i]["url"],
                data[i]["data"],
                data[i]["profissional"])
            )
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()


