import logging
from pathlib import Path
from datetime import datetime
from config.settings import settings

class LoggerSetup:
    """Custom logger setup"""
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get or create logger"""
        if name in LoggerSetup._loggers:
            return LoggerSetup._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, settings.LOG_LEVEL))
        
        # File handler
        log_file = settings.LOGS_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
        logger.addHandler(console_handler)
        
        LoggerSetup._loggers[name] = logger
        return logger


def get_logger(module_name: str) -> logging.Logger:
    """Convenience function to get logger"""
    return LoggerSetup.get_logger(module_name)
