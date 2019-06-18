"""
This script reads a log file with multiline log messages using a specific datetime pattern identifier
and spills out 1 log message at a time

@author: kanghosh

env details: 
in cmd: C:/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyze
r-g2FLMzg_/Scripts/activate.bat
in git-bash: cd /c/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyzer-g2FLMzg_/Scripts/
"""

""" ****************************** ALL IMPORTS ****************************** """

# Standard library imports
import re
import logging

# Third party imports

# import openpyxl   ## being used internally to write the pandas dataframe to an excel workbook
# import pysocks    ## being used by requests to use the socks proxy

# Local application imports



""" ****************************** START OF CODE ****************************** """

logging.basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)
logger.setLevel(logging.CRITICAL)

a_date, other, EOF = 0, 1, 2

filepath = "NQQuery_OAC.log"
# filepath = "nqquery_FABI.log"

""" with open(filepath, 'r') as file_in:
    i = 0
    for line in file_in:
        if i < 2:
            print(line)
            i+=1
        else:
            break
 """

def one_log_line(filepath, line_start_identifier):
    # date_regex = re.compile(r"\[(?:2|1)\d{3}(?:-|\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))T(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9])\.(?:[0-9]{3})[-|\+](?:[0-1][0-9]):(?:[0-5][0-9])\]", re.I)
    date_regex = re.compile(line_start_identifier, re.I)
        
    with open(filepath) as nqquery:

        for line in nqquery:
            line = line.strip()
            m_line = date_regex.match(line)

            if m_line:
                yield a_date, line
            else:
                yield other, line

    yield EOF, ''


def one_log_msg(line_start_identifier):
    complete_log_msg = []
    # count = 0

    for kind, content in one_log_line(filepath, line_start_identifier):
        logger.debug(f"*****inside for loop*****\nkind: {kind}")
        # logger.debug(f"Count: {count}\n")

        # if count > 10:
        #     logger.warning(f"Specified Count limit of {count-1} reached.\n")
        #     break

        if kind in [a_date, EOF]:
            logger.debug(f"**inside if 'kind' block**\n1 complete log message list:\n{complete_log_msg}\n")
            
            if complete_log_msg != []:
                logger.info("Joined the elements of complete_log_msg list: " + " ".join(complete_log_msg) + "\n")
                # print("Output to stdout: \n" + " ".join(complete_log_msg) + "\n")
                yield " ".join((complete_log_msg))

            complete_log_msg = [content]
            logger.debug(f"new complete log message from if 'kind' block: {complete_log_msg}\n")
            # count += 1
            # logger.debug("Count incremented by 1\n")

        else:
            logger.debug("**inside else block**\nAdded new content")
            complete_log_msg.append(content)
            logger.debug(f"Complete log message list after appending new content: {complete_log_msg}\n")
            
        logger.debug("==================== End of a for-loop iteration ====================\n")


