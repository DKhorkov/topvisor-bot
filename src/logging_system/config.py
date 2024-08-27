import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

LOG_FILE: Path = Path(os.getcwd()).joinpath('logs.log')

__file_handler: logging.FileHandler = logging.FileHandler(filename=LOG_FILE)
__stdout_handler: logging.StreamHandler = logging.StreamHandler(stream=sys.stdout)
__handlers: List[logging.Handler] = [__file_handler, __stdout_handler]

LOGGING_CONFIG: Dict[str, Any] = {
    'level': logging.INFO,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
    'handlers': __handlers
}
