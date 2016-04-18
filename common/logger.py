import logging

__author__ = 'Randy Sorensen <sorensra@msudenver.edu>'


open_logs = []


def init(log_path):
    logging.basicConfig(filename=log_path, level=logging.INFO)


def get(module_name):
    if module_name in open_logs:
        return logging.getLogger(module_name)

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    log_handler = logging.StreamHandler()
    log_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)

    logger.addHandler(log_handler)

    open_logs.append(module_name)
    return logger
