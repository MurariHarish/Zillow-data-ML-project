import sys
from src.ZillowHouseData.logger import logger
from src.ZillowHouseData.exception import CustomException

# Checking logger and Exception
# logging
logger.info("Logging Successfull!!!")

# exception
try:
    a=1/0
except Exception as e:
    logger.info("Divide by zero")
    raise CustomException(e,sys)