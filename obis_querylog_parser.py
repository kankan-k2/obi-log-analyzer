"""
This script parses the nqquery.log file and captures all the data into a Pandas dataframe
and which is then passed on to the dash app for visualization

@author: kanghosh

env details: 
in cmd: C:/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyze
r-g2FLMzg_/Scripts/activate.bat
in git-bash: cd /c/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyzer-g2FLMzg_/Scripts/
"""

""" ****************************** ALL IMPORTS ****************************** """

# Local application imports
import custom_logging
import obi_logfile_reader

# Standard library imports
import re
import logging
from collections import OrderedDict, namedtuple

# Third party imports
import pandas as pd

# import openpyxl   ## being used internally to write the pandas dataframe to an excel workbook
# import pysocks    ## being used by requests to use the socks proxy


""" ****************************** START OF CODE ****************************** """

# Set up the logger using the defaults
custom_logging.setup_logging()
logger = logging.getLogger(__name__)


# [2014-05-27T19:24:20.764-04:00]
obisquerylog_line_start = r"\[(?:2|1)\d{3}(?:-|\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))T(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9])\.(?:[0-9]{3})[-|\+](?:[0-1][0-9]):(?:[0-5][0-9])\]"

psql_request_pattern = r"^\[((?:2|1)\d{3}(?:-|\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))T(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9])\.(?:[0-9]{3})[-|\+](?:[0-1][0-9]):(?:[0-5][0-9]))\] \[OracleBIServerComponent\] \[TRACE:\d\] \[\] \[\] \[ecid: ([\w^:,_-]+)\] \[tid: (\w+)\] \[messageid: [\w-]+\] \[requestid: ([\w-]+)\] \[sessionid: ([\w-]+)\] \[username: ([\w\.-]+)\] (?:\-+) Sending query to database named ([\w\s]+) \(id: <<(\d+)>>\)(?:[\w,\s]+) logical request hash (\w+), physical request hash (\w+?): \[\[\s+(.*?)\s+\]\]"
psql_request_regex = re.compile(psql_request_pattern, re.I)
# print(psql_request_regex)

psql_stats_pattern = r""
psql_stats_regex = re.compile(psql_stats_pattern, re.I)

lsql_stats_pattern = r""
lsql_stats_regex = re.compile(lsql_stats_pattern, re.I)

# ('2014-05-27T19:24:20.764-04:00', '004yabypLcr8XrP5If^Ayf0003Xu00003H,0', '475bb940', 'f2c80002', 'f2c80000', 'weblogic', 'Oracle Data Warehouse', '267809', '19859160', '63a9f3fa', 'select distinct T41656.GL_ACCOUNT_CAT_CODE as c1, T41656.GL_ACCOUNT_CAT_NAME as c2 from W_GL_GROUP_ACCOUNT_D T41656 /* Dim_W_GL_GROUP_ACCOUNT_D */ order by c1, c2')
# psql_request_data = namedtuple("psql_request_data", ["datetime" ,"ecid" ,"threadId" ,"requestId" ,"sessionId" ,"username" ,"dbName" ,"dbId" ,"lsqlRequestHash" ,"psqlRequestHash" ,"psql"])
psql_request_data = namedtuple("psql_request_data_1", "datetime ecid threadId requestId sessionId username dbName dbId lsqlRequestHash psqlRequestHash psql")

""" 
psql_df = pd.DataFrame()
print(psql_df)
print("\n")
"""

logger.info(f"Pandas library version used: {pd.__version__}")

def generate_psql_df(regex):

    logger.info(f"Generating Physical SQL dataframe.")
    count = 0

    for line in obi_logfile_reader.one_log_msg(obisquerylog_line_start):
        logger.debug(f"Log message read: {line}")
        psql_match = regex.match(line)

        if psql_match:
            count += 1
            logger.debug(f"\nPhysical SQL log message # {count}: {line}")
            row = psql_request_data(*psql_match.groups())
            logger.debug(f"Physical SQL log messages match: {row}")
            # row_series = pd.Series(row, row._fields)
            # print(row_series.get_values())

            if count == 1:
                psql_df = pd.DataFrame(columns=row._fields)
                logger.debug(f"The count is {count}")
                logger.debug(f"Dataframe created with following columns: \n{psql_df}\n")

            psql_df.loc[len(psql_df)] = list(row)
            # psql_df.append(list(row), ignore_index=True)
            # psql_df.append(row)

    logger.info(f"Generated Physical SQL dataframe successfully.")
    return psql_df

""" 
print(generate_psql_df())
print("\n")
"""

def deduplicate_df(df):

    logger.info(f"Removing duplicates from the generated dataframe")
    df.drop_duplicates(keep='first', inplace=True)

    return df


def split_psql_df(regex):

    logger.info(f"Returning 2 split dataframes from the original generateed dataframe")

    psql_df = generate_psql_df(regex)
    logger.debug(f"Displaying the generated raw Physical SQL Dataframe: \n{psql_df}")
    # logger.debug(psql_df)
    psql_only_df = psql_df[['psqlRequestHash','psql']].copy()
    psql_df.drop('psql', axis=1, inplace=True)

    logger.debug(f"Displaying the modified Physical SQL Dataframe: \n{psql_df}")
    # logger.info(psql_df)
    logger.debug(f"Displaying the new Physical SQL Only Dataframe with any duplicates: \n{psql_only_df}")
    # logger.info(psql_only_df)

    return psql_df, deduplicate_df(psql_only_df)


psql_trigger_df, psql_only_df = split_psql_df(psql_request_regex)

