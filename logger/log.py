from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | > {message}")

# logger.debug("Это сообщение уровня DEBUG")
# logger.info("Это сообщение уровня INFO")
# logger.warning("Это сообщение уровня WARNING")
# logger.error("Это сообщение уровня ERROR")