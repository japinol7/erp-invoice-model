__author__ = "Joan A. Pinol  (japinol)"

from datetime import datetime
import os
import sys

from version import version

APP_NAME = "erp-invoice-model"

LOG_START_APP_MSG = f"Start app {APP_NAME} version: {version.get_version()}"
LOG_END_APP_MSG = f"End app {APP_NAME}"

LOG_FILE = os.path.join(
    "logs", f"log_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S_%f')}.log"
)
LOG_FILE_UNIQUE = os.path.join("logs", "log.log")
SYS_STDOUT = sys.stdout
