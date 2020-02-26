import psycopg2
import re

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
                    titulo VARCHAR(64),
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
        for values in data.values():
            print(values["area"])
            self.cur.execute("""
                INSERT INTO mytable (id_anuncio, municipio, estado, cep, preco, area, tipo, titulo, descricao, fotos, ddd, telefone, url, data, profissional)
                VALUES(%s, %s, %s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s, %s ,%s);""",
                (values["id_anuncio"],
                values["municipio"],
                values["estado"],
                values["cep"],
                re.sub(r"(R\$\s|\.)", "", values["preco"]),
                values["area"],
                values["tipo"],
                values["titulo"],
                values["descricao"],
                values["fotos"],
                values["ddd"],
                values["telefone"],
                values["url"],
                values["data"],
                values["profissional"])
            )

    def __del__(self):
        self.cur.close()
        self.conn.close()


