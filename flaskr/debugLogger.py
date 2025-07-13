import logging, sys

# print Debug & Info & WARNING & ERROR
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# don't print debug only Info & WARNING & ERROR
# logging.basicConfig(stream=sys.stderr, level=logging.INFO)
# don't print debug & Info only WARNING & ERROR
#logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
# print only ERROR
#logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
logger = logging.getLogger(__name__)

logging.debug('A debug message!')
logging.info('A Info message processed %d records', 5)
logging.warning('A warning message!')
logging.error('A error message!')

logger.info("logger name")
