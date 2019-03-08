from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

load_dotenv()

hostname = os.getenv('hostname')
port = os.getenv('port')
database = os.getenv('database')
username = os.getenv('username')
password = os.getenv('password')

conn = psycopg2.connect(host=hostname, database=database, user=username, password=password)
df = pd.read_sql('select * from studies', con=conn)
phase_counts = df.groupby('phase').size()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Pie(labels=phase_counts.index, values=phase_counts.values
                       )
            ],
            layout=go.Layout(
                title='Clinical Trial Phases',
                showlegend=True,
                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph'
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
