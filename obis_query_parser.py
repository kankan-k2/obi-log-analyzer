"""
This script parses the nqquery.log file and captures all the data into a Pandas dataframe
and then inserts into an Oracle Database table

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
from collections import OrderedDict, namedtuple

# Third party imports
import pandas as pd

# import openpyxl   ## being used internally to write the pandas dataframe to an excel workbook
# import pysocks    ## being used by requests to use the socks proxy

# Local application imports
import logfile_parser
from logfile_parser import logger

print(pd.__version__)


""" ****************************** START OF CODE ****************************** """


psql_regex = re.compile(r"^\[((?:2|1)\d{3}(?:-|\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))T(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9])\.(?:[0-9]{3})[-|\+](?:[0-1][0-9]):(?:[0-5][0-9]))\] \[OracleBIServerComponent\] \[TRACE:\d\] \[\] \[\] \[ecid: ([\w^:,_-]+)\] \[tid: (\w+)\] \[messageid: [\w-]+\] \[requestid: ([\w-]+)\] \[sessionid: ([\w-]+)\] \[username: ([\w\.-]+)\] (?:\-+) Sending query to database named ([\w\s]+) \(id: <<(\d+)>>\)(?:[\w,\s]+) logical request hash (\w+), physical request hash (\w+?): \[\[\s+(.*?)\s+\]\]", re.I)
# print(psql_regex)

# ('2014-05-27T19:24:20.764-04:00', '004yabypLcr8XrP5If^Ayf0003Xu00003H,0', '475bb940', 'f2c80002', 'f2c80000', 'weblogic', 'Oracle Data Warehouse', '267809', '19859160', '63a9f3fa', 'select distinct T41656.GL_ACCOUNT_CAT_CODE as c1, T41656.GL_ACCOUNT_CAT_NAME as c2 from W_GL_GROUP_ACCOUNT_D T41656 /* Dim_W_GL_GROUP_ACCOUNT_D */ order by c1, c2')
# psql_data = namedtuple("psql_data", ["datetime" ,"ecid" ,"threadId" ,"requestId" ,"sessionId" ,"username" ,"dbName" ,"dbId" ,"lsqlRequestHash" ,"psqlRequestHash" ,"psql"])
psql_data = namedtuple("psql_data", "datetime ecid threadId requestId sessionId username dbName dbId lsqlRequestHash psqlRequestHash psql")

""" 
psql_df = pd.DataFrame()
print(psql_df)
print("\n")
"""

def generate_psql_df():
    count = 0
    for line in logfile_parser.one_log_msg():
        logger.debug(f"Log message read: {line}")
        psql_match = psql_regex.match(line)
        if psql_match:
            count += 1
            logger.debug(f"\nPhysical SQL log message # {count}: {line}")
            row = psql_data(*psql_match.groups())
            logger.debug(f"Physical SQL log messages match: {row}")
            # row_series = pd.Series(row, row._fields)
            # print(row_series.get_values())
            if count == 1:
                psql_df = pd.DataFrame(columns=row._fields)
                logger.debug(f"the count is {count}")
                logger.debug(f"Dataframe created with following columns: \n{psql_df}\n")
            psql_df.loc[len(psql_df)] = list(row)
            # psql_df.append(list(row), ignore_index=True)
            # psql_df.append(row)
    return psql_df

print(generate_psql_df())
print("\n")


