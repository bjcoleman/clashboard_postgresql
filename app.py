from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

load_dotenv()

hostname = os.getenv('hostname')
port = os.getenv('port')
database = os.getenv('database')
username = os.getenv('username')
password = os.getenv('password')

conn = None
df = None
study_type_counts = None
status_counts = None
phase_counts = None


def compute_results():
    print('computing results')
    conn = psycopg2.connect(host=hostname, database=database, user=username, password=password)
    df = pd.read_sql('select * from studies', con=conn)
    global study_type_counts
    study_type_counts = df.groupby('study_type').size()
    global status_counts
    status_counts = df.groupby('overall_status').size()
    global phase_counts
    phase_counts = df.groupby('phase').size()
    print('done')

compute_results()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='ClinicalTrails.gov Data Exploration'),

    html.Div(
        id='plot-area'
    ),

    dcc.Dropdown(
        options=[
            {'label': 'Study Type', 'value': 'study_type'},
            {'label': 'Status', 'value': 'overall_status'},
            {'label': 'Phase', 'value': 'phase'}
        ],
        placeholder='Select a property',
        id='dropdown-id'
    )
])


@app.callback(Output('plot-area', 'children'),
              [Input('dropdown-id', 'value')])
def update_plot(value):

    if value == 'study_type':
        labels = study_type_counts.index
        values = study_type_counts.values
        title = 'Study Type'
    elif value == 'overall_status':
        labels = status_counts.index
        values = status_counts.values
        title = 'Status'
    elif value == 'phase':
        labels = phase_counts.index
        values = phase_counts.values
        title = 'Phase'
    else:
        labels = []
        values= []
        title = ''

    return dcc.Graph(
        figure=go.Figure(
            data=[
                go.Pie(labels=labels, values=values)
            ],
            layout=go.Layout(
                title=title,
                showlegend=True,
                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph'
    )


if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
