import psycopg2

class Database:    
    def __init__(self, dbname, user, password):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host="localhost")
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.cur.execute(
                "CREATE TABLE IF NOT EXISTS test ("
                "id_anuncio INTEGER,"
                "municipio VARCHAR(64),"
                "estado CHAR(2),"
                "cep SMALLINT,"
                "preco NUMERIC(14,2),"
                "area VARCHAR(16),"
                "tipo VARCHAR(32),"
                "titulo VARCHAR(64),"
                "descricao TEXT,"
                "fotos TEXT [],"
                "ddd CHAR(2),"
                "telefone VARCHAR(16),"
                "url TEXT,"
                "data TIMESTAMPTZ,"
                "profissional BOOLEAN,"
                "PRIMARY KEY(id_anuncio));"
            )

    def insert_data(self, data):
        keys = data.keys()
        for values in data.values():
            self.cur.execute(
                "INSERT INTO test (%(id_anuncio)s, %(municipio)s, %(estado)s, %(cep)s, %(preco)s, %(area)s, %(tipo)s, %(titulo)s, %(descricao)s, %(fotos)s, %(ddd)s, %(telefone)s, %(url)s, %(data)s, %(profissional)s);"
            )


    def __del__(self):
        self.cur.close()
        self.conn.close()


