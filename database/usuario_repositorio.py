from database.local import BancoDeDadosLocal
from modelos.usuario import Usuario, UsuarioCriarAtualizar
from datetime import datetime
import secrets



class UsuarioRepositorio:
    def __init__(self, database: BancoDeDadosLocal):
        self.bd = database


    async def buscar_usuario_por_cred(self, email: str, senha: str) -> Usuario | None:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT id, nome, email, nivel
                FROM usuarios
                WHERE email = ? AND senha = ?
                """,
                (email, senha)
            )

            linha = cursor.fetchone()

            if linha:
                return Usuario(
                    id_=linha[0],
                    nome=linha[1],
                    email=linha[2],
                    nivel=linha[3]
                )

            return None


    async def registrar_login(
        self,
        usuario_id: int,
        ip: str
    ):

        with self.bd.conectar() as conexao:

            cursor = conexao.cursor()


            cursor.execute(
                """
                UPDATE usuarios

                SET
                    ultimo_login = ?,
                    ultimo_ip = ?

                WHERE id = ?

                """,
                (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ip,
                    usuario_id
                )
            )


            conexao.commit()


    async def registrar_logout(
        self,
        usuario_id: int
    ):

        with self.bd.conectar() as conexao:

            cursor = conexao.cursor()


            cursor.execute(
                """
                UPDATE usuarios

                SET ultimo_logout = ?

                WHERE id = ?

                """,
                (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    usuario_id
                )
            )


            conexao.commit()
        
    async def buscar_usuario_por_email(self, email: str) -> Usuario | None:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email FROM usuarios WHERE email = ?", (email,))
            linha = cursor.fetchone()
            if linha:
                return Usuario(id_=linha[0], nome=linha[1], email=linha[2])
            return None
                

    async def criar_usuario(self, usuario_criar: UsuarioCriarAtualizar) -> Usuario:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, nivel) VALUES (?,?,?,?)",
                (
                    usuario_criar.nome,
                    usuario_criar.email,
                    usuario_criar.senha,
                    usuario_criar.nivel
                )
            )

            id_ = cursor.lastrowid

            return Usuario(
                id_=id_,
                nome=usuario_criar.nome,
                email=usuario_criar.email,
                senha=usuario_criar.senha,
                nivel=usuario_criar.nivel
            )


    async def criar_sessao(self, usuario_id: int):

        token = secrets.token_hex(32)


        with self.bd.conectar() as conexao:

            cursor = conexao.cursor()


            cursor.execute(
                """
                DELETE FROM sessoes
                WHERE usuario_id = ?
                """,
                (usuario_id,)
            )


            cursor.execute(
                """
                INSERT INTO sessoes
                (
                    token,
                    usuario_id
                )

                VALUES
                (
                    ?,
                    ?
                )
                """,
                (
                    token,
                    usuario_id
                )
            )


            conexao.commit()


        return token

    async def buscar_usuario_por_token(self, token: str) -> Usuario | None:

        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT 
                    u.id,
                    u.nome,
                    u.email,
                    u.nivel

                FROM usuarios u

                INNER JOIN sessoes s
                    ON s.usuario_id = u.id

                WHERE s.token = ?
                """,
                (token,)
            )

            linha = cursor.fetchone()

            if linha:

                return Usuario(
                    id_=linha[0],
                    nome=linha[1],
                    email=linha[2],
                    nivel=linha[3]
                )

            return None


    async def remover_sessao(self, token: str):

        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                """
                DELETE FROM sessoes
                WHERE token = ?
                """,
                (token,)
            )

            conexao.commit()



    async def listar_usuarios(self):

        with self.bd.conectar() as conexao:

            cursor = conexao.cursor()


            cursor.execute(
                """
                SELECT

                    u.id,
                    u.nome,
                    u.email,
                    u.nivel,
                    u.ultimo_login,
                    u.ultimo_logout,
                    u.ultimo_ip,


                    CASE

                        WHEN EXISTS (

                            SELECT 1

                            FROM sessoes s

                            WHERE s.usuario_id = u.id

                        )

                        THEN 1

                        ELSE 0

                    END AS online


                FROM usuarios u


                ORDER BY u.nome

                """
            )


            usuarios = []


            for linha in cursor.fetchall():

                usuarios.append({

                    "id": linha[0],

                    "nome": linha[1],

                    "email": linha[2],

                    "nivel": linha[3],

                    "ultimo_login": linha[4],

                    "ultimo_logout": linha[5],

                    "ultimo_ip": linha[6],

                    "online": bool(linha[7])

                })


            return usuarios

    async def alterar_nivel(
        self,
        usuario_id: int,
        nivel: str
        ):

        with self.bd.conectar() as conexao:

            cursor = conexao.cursor()

            cursor.execute(
                """
                UPDATE usuarios
                SET nivel = ?
                WHERE id = ?
                """,
                (
                    nivel,
                    usuario_id
                )
            )

            conexao.commit()


    async def remover_sessao_usuario(
        self,
        usuario_id: int
    ):

        with self.bd.conectar() as conexao:

            cursor = conexao.cursor()

            cursor.execute(
                """
                DELETE FROM sessoes
                WHERE usuario_id = ?
                """,
                (usuario_id,)
            )

            conexao.commit()