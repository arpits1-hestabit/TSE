import logging
import os

def setup_logger(log_file="nexus.log"):
    """
    Configures and returns the Nexus_AI logger.
    - Logs DEBUG+ messages to a file.
    - Logs INFO+ messages to the console.
    - If the logger is already configured, returns the existing logger instance.
    """
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", log_file)

    logger = logging.getLogger("NEXUS_AI") # named loggers are reusable across files/modules, as calling this again returns the same logger instance
    logger.setLevel(logging.DEBUG)

    # Check if file handler is already added(if this check would be removed then the logs would print multiple times is setup_logger is called more than once)
    if not logger.handlers:
        # File handler
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        ch.setFormatter(ch_formatter)
        logger.addHandler(ch)

    return logger
