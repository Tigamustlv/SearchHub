import sqlite3
from contextlib import contextmanager


class BancoDeDadosLocal:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.inicializar_banco()


    @contextmanager
    def conectar(self):
        conexao = sqlite3.connect(self.nome_arquivo)
        try:
            yield conexao
            conexao.commit()
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()


    def inicializar_banco(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()

            if self.nome_arquivo == "clientes.db":
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        originador TEXT NOT NULL,
                        fundo TEXT NOT NULL,
                        operacao TEXT NOT NULL,
                        cessao TEXT,
                        ccb TEXT,
                        documento TEXT,
                        nome TEXT,
                        lastro TEXT
                    )
                ''')

            elif self.nome_arquivo == "usuarios.db":
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT NOT NULL,
                        senha TEXT NOT NULL,
                        nivel TEXT NOT NULL DEFAULT 'operacional'
                    )
                ''')


print("Banco de Dados inicializado!")