import logging

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s')
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger