# CONFIGURAZIONE LOGGING
import logging
from pathlib import Path


LOG_DIR = Path("Logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "Sentiment_analysis.log"

def setup_logging(
    log_file: Path = LOG_FILE,
    level: int = logging.INFO
) -> logging.Logger:
    """
    Configura il logging del progetto:
    - output su console
    - output su file
    - formato uniforme con timestamp, livello e messaggio
    """
    logger = logging.getLogger("Sentiment_analysis")
    logger.setLevel(level)

    # Evita duplicazione di handler se la cella viene rieseguita
    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Handler file
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
