"""
This script reads the Pandas dataframe passed by obis_querylog_parser.py and visualizes them accordingly

@author: kanghosh

env details: 
in cmd: C:/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyze
r-g2FLMzg_/Scripts/activate.bat
in git-bash: cd /c/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyzer-g2FLMzg_/Scripts/
"""

""" ****************************** ALL IMPORTS ****************************** """

# Local application imports
import custom_logging
import obis_querylog_parser

# Standard library imports
import logging

# Third party imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
# import plotly, dash_renderer


""" ****************************** START OF CODE ****************************** """

# Set up the logger using the defaults
custom_logging.setup_logging()
logger = logging.getLogger(__name__)


psql_trigger_df, psql_only_df = obis_querylog_parser.split_psql_df(obis_querylog_parser.psql_request_regex)

def generate_table(dataframe, max_rows=50):
    logger.info(f"Generating a HTML table using the dataframe passed to dash")
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.keys()])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(name="Oracle BI Log Analyzer", external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Oracle BI Log Analyzer'),
    html.H3(children='Physical SQLs trigger/request log messages from nqquery.log'),
    generate_table(psql_trigger_df),
    html.Br(),
    html.H3(children='Individual Physical SQLs from nqquery.log'),
    generate_table(psql_only_df)
])

if __name__ == '__main__':

    try:
        logger.info(f"Dash library version used: {dash.__version__}")
        logger.info(f"Dash app server is starting")
        app.run_server(debug=True)
        # app.run_server()
    except Exception as e:
        logger.error(f"Houston, we have a major problem!\nDash app server failed to start", exc_info=True)


