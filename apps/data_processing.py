from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

layout = html.Div([


    dcc.Upload([
        'Drag and Drop or ',
        html.A('Click to Select a File'),

    ],  id='interview-data',
        style={
        'width': 'auto',
        'height': 'auto',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin-left':'6rem',
        'margin-right':'6rem'
    })
])




import pandas as pd
from dash import dcc, Dash, html, dash_table
import base64
import datetime
import re



def get_data_from_word(path_to_file):
    from docx import Document
    pathname = directory + '/' + filename
    # Creating a word file object
    doc_object = open(path_to_file, "rb")

    # creating word reader object
    doc_reader = Document(doc_object)
    data = ""

    for p in doc_reader.paragraphs:
        data += p.text + "\n"

    return data