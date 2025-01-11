from loguru import logger
import sys
from config.settings import settings

logger.remove()
logger.add(
    sys.stderr,
    level=settings.log_level or "INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

logger.add(
    "logs/app.log",
    rotation="00:00",
    retention="3 days",
    level=settings.log_level or "INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    compression="zip",
    backtrace=True,
    diagnose=True,
    enqueue=True,
)

__all__ = ["logger"]
