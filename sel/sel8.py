import logging

logging.basicConfig(filename="D:/file.log", format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG)

logging.debug("msg")
logging.info("msg")
logging.critical("msg")
logging.error("msg")
logging.warning("msg")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


