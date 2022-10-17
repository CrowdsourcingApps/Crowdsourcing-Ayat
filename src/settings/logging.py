import logging
from pathlib import Path

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
Path('src/log_files').mkdir(parents=True, exist_ok=True)
fh = logging.handlers.RotatingFileHandler('src/log_files/server.log',
                                          mode='a',
                                          maxBytes=100*1024,
                                          backupCount=3)

formatter = logging.Formatter(
    '%(asctime)s - %(module)s - %(funcName)s - '
    'line:%(lineno)d - %(levelname)s - %(message)s'
)

ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)  # Exporting logs to the screen
logger.addHandler(fh)  # Exporting logs to a file

logger = logging.getLogger(__name__)
