from datetime import datetime
import logging
from functools import lru_cache

@lru_cache
def get_logger(module_name, dir, fname, level=logging.DEBUG):
    logger = logging.getLogger(module_name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(f"{dir}/{datetime.now():%Y-%m-%d}-{fname}.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(level)
    return logger