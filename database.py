import psycopg2

class ConexionDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='postgres',
            user='alumno',
            password='alumno_FIE11',
            host='148.216.17.185',
            port='5432'
        )
        self.cursor = self.conn.cursor()
