import os
import mariadb

#MARIADB_USER = "root"
#MARIADB_PASSWORD = "Chem@1910"


MARIADB_HOST = os.getenv(
    "MARIADB_HOST",
    "localhost"
)

MARIADB_PORT = int(
    os.getenv(
        "MARIADB_PORT",
        "3306"
    )
)

MARIADB_USER = os.getenv(
    "MARIADB_USER", "root"
)

MARIADB_PASSWORD = os.getenv(
    "MARIADB_PASSWORD", "Chem@1910"
)

MARIADB_DATABASE = os.getenv(
    "MARIADB_DATABASE",
    "searchhub"
)


def obter_conexao():
    return mariadb.connect(
        host=MARIADB_HOST,
        port=MARIADB_PORT,
        user=MARIADB_USER,
        password=MARIADB_PASSWORD,
        database=MARIADB_DATABASE
    )