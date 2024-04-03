import logging 
import os

logdir ='logs'
os.makedirs(logdir,exist_ok=True)

warning_logpath = os.path.join(logdir,'warning_logs.log')
running_logpath = os.path.join(logdir,'running_logs.log')



#Warning logs 
format = logging.Formatter('[%(asctime)s] : [%(name)s] : [%(levelname)s] : [%(message)s] ')
warning_filehandler = logging.FileHandler(warning_logpath)
warning_filehandler.setFormatter(format)

logger = logging.getLogger('warning_logger')
logger.addHandler(warning_filehandler)
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler())


#INFO runings logs
format1 = logging.Formatter('[%(asctime)s] : [%(name)s] : [%(levelname)s] : [%(message)s] ')
running_filehandler = logging.FileHandler(running_logpath)
running_filehandler.setFormatter(format1)

logger1 = logging.getLogger('running_logger')
logger1.addHandler(running_filehandler)
logger1.setLevel(logging.INFO)
logger1.addHandler(logging.StreamHandler())

