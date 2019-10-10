"""
This script scans a location and lists out all the required log files and outputs their location for use 
by the other scripts in this utility.

@author: kanghosh

env details: 
in cmd: C:/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyze
r-g2FLMzg_/Scripts/activate.bat
in git-bash: cd /c/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyzer-g2FLMzg_/Scripts/
"""

""" ****************************** ALL IMPORTS ****************************** """

# Local application imports
import custom_logging

# Standard library imports
from pathlib import Path
import re
import logging
from pprint import pprint

# Third party imports
# import openpyxl   ## being used internally to write the pandas dataframe to an excel workbook
# import pysocks    ## being used by requests to use the socks proxy


""" ****************************** START OF CODE ****************************** """

p = Path(r"D:\My_Workspace\BILogAnalyzer\input_data\aoaciad070163oacpod-bi-1\domainhome\servers")

oac_logpath_dict = {}

for child in p.iterdir():
    oac_comp_key = child.parts[-1]
    # print(oac_comp_key)
    oac_comp_logpath = child / 'logs'

    extension = ""
    # print(bi_comp_logpath.parent)
    # oac_logpathlist = list(oac_comp_logpath.glob(f"*{extension}"))
    # print(oac_logpathlist)

    # oac_logpath_dict[oac_comp_key] = list(oac_comp_logpath.glob(f"*{extension}"))
    oac_logpath_dict[oac_comp_key] = [x for x in oac_comp_logpath.rglob(f"*{extension}") if not x.is_dir()]

pprint(oac_logpath_dict)

