import logging
import os


os.makedirs("logs", exist_ok=True)


logging.basicConfig(
    filename="logs/sistema.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


logger = logging.getLogger("auditoria")