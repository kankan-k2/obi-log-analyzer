"""
This script reads the Pandas dataframe passed by obis_querylog_parser.py and visualizes them accordingly

@author: kanghosh

env details: 
in cmd: C:/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyze
r-g2FLMzg_/Scripts/activate.bat
in git-bash: cd /c/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyzer-g2FLMzg_/Scripts/
"""

""" ****************************** ALL IMPORTS ****************************** """

# Standard library imports
import os, pathlib
import yaml
import logging
import logging.config
# import coloredlogs

""" ****************************** NAIVE LOGGING CONFIG MECHANISM ****************************** """

"""
# logging.basicConfig(level='INFO', format=log_format)
logger = logging.getLogger(__name__)
# Set default logging handler to avoid "No handler found" warnings.
# logger = logging.getLogger(__name__).addHandler(logging.NullHandler())

# To override the default severity of logging
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.CRITICAL)

log_format = r'[%(asctime)s] [%(name)s] [%(module)s] [%(levelname)s] %(message)s'
formatter = logging.Formatter(log_format)

# Use FileHandler() to log to a file
# log_handler = logging.FileHandler('bi_log_analyzer.log')
log_handler = logging.StreamHandler()
log_handler.setFormatter(formatter)

# Don't forget to add the file handler
logger.addHandler(log_handler)
# logger.info("I am a log from helper")
"""

""" ****************************** CURRENT LOGGING CONFIG MECHANISM ****************************** """

def setup_logging(default_path='config/logconfig.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    | **@author:** Kankan Ghosh
    | Logging Setup
    """
    log_config_path = pathlib.Path(default_path)
    value = os.getenv(env_key, None)
    if value:
        log_config_path = pathlib.Path(value)
    if os.path.exists(log_config_path):
        print("Log configuration file relative path: " + str(log_config_path))
        with open(log_config_path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                # print(config)
                logging.config.dictConfig(config)
                # coloredlogs.install()
            except Exception as e:
                # print(e)
                print(e.with_traceback())
                print("Error in loading Logging Configuration from file. Using default configs instead.")
                logging.basicConfig(level=default_level)
                # coloredlogs.install(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        # coloredlogs.install(level=default_level)
        print("Failed to load configuration file. Using default configs")


