import logging
import sys
from pathlib import Path
from src.config.config import get_config

def get_logger(name: str) -> logging.Logger:
    """Get logger with config-based paths"""
    try:
        config = get_config()
        log_level_str = config.get('logging.level', 'INFO').upper()
        log_dir = config.logs_dir
    except:
        # Fallback
        log_level_str = 'INFO'
        log_dir = Path('src/logs')
    
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create logs directory using config path
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # File handler with config path
    log_file = log_dir / f"{name.split('.')[-1]}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger