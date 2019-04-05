"""
This script fetches the count of key errors from elasticsearch and translates all the data into a Pandas dataframe
and then inserts into an Oracle Database table

@author: kanghosh

env details: 
in cmd: C:/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyze
r-g2FLMzg_/Scripts/activate.bat
in git-bash: cd /c/Users/kanghosh.ORADEV/.virtualenvs/BILogAnalyzer-g2FLMzg_/Scripts/
"""

""" ****************************** ALL IMPORTS ****************************** """

# Standard library imports

# Third party imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
# import plotly, dash_renderer

# Local application imports
import obis_query_parser
from logfile_parser import logger


""" ****************************** START OF CODE ****************************** """

psql_trigger_df, psql_only_df = obis_query_parser.split_psql_df()

def generate_table(dataframe, max_rows=50):
    logger.debug("Generate an HTML table using the dataframe passed to dash")
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
app = dash.Dash("BI Log Analyzer", external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='BI Log Analyzer'),
    html.H3(children='Physical SQLs trigger log messages from nqquery.log'),
    generate_table(psql_trigger_df),
    html.H3(children='Individual Physical SQLs from nqquery.log'),
    generate_table(psql_only_df)
])

if __name__ == '__main__':
    app.run_server(debug=True)


