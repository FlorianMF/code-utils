import os
import functools
import logging

def create_logger(filepath, name='logger', **kwargs):
    """
    Creates a logging object and returns it
    """
    fmt = kwargs.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # create the logging file handler
    fh = logging.FileHandler(filepath)
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger

if __name__ == "__main__":
    loggername = os.path.basename(__file__).rsplit('.', 1)[0]
    loggerfile = os.path.join(os.path.dirname(__file__), 'logs',  loggername + '.log')
    logger = create_logger(loggerfile, loggername)