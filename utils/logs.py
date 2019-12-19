from logging import Logger , FileHandler
import logging
from django.conf import settings
import os

logging_settings = settings.DASHBOARD_LOGGING

if logging_settings is None:
    logging_settings = {

    'handler':'file',
    'filename':'genetherapy.log',
    'settings':{
        'path':os.path.join(settings.LOGS_DIR,'logs'),
        'encoding':'UTF-8'
        }
    }

# Define the general logger for screening web application
log = Logger('Genetherapy Logger', level=logging.INFO)
logging_settings_dir = os.path.join(logging_settings['settings']['path'],logging_settings['filename'])
file_handler = FileHandler(logging_settings_dir,mode='wb',encoding=logging_settings['settings']['encoding'])
log.addHandler(file_handler)



