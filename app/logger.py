# app/logger.py
import logging
import os

def get_logger(name: str) -> logging.Logger:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    os.makedirs("logs", exist_ok=True)
    handlers = [
        logging.FileHandler("logs/app.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
    logging.basicConfig(level=log_level, format=log_format, handlers=handlers)
    return logging.getLogger(name)
