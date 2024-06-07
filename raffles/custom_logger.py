import logging

def setup_logger(name):
    """
    Configure and return a logging logger object.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: A configured logger object.

    Example:
        To set up a logger named 'my_logger':

        >>> logger = setup_logger('my_logger')
        >>> logger.debug('This is a debug message')
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler('/var/log/django.log')
    console_handler = logging.StreamHandler()
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
