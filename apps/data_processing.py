from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

layout = html.Div([


    dcc.Upload([
        'Drag and Drop or ',
        html.A('Click to Select a File')
    ], style={
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
