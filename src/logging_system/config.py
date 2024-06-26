import logging
import os
from pathlib import Path
from typing import Dict, Any

LOG_FILE: Path = Path(os.getcwd()).joinpath('logs.log')

LOGGING_CONFIG: Dict[str, Any] = {
    'level': logging.INFO,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
    'filename': LOG_FILE
}
