import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

def generate_calendar():
    pass
#create a list of cards

#distribute the cards amond an even nubmer or rows 7 each

#assign color to each

layout = html.Div([
    html.H2('Under Construction', style={'color':'red'}),
   html.Div([
       html.H1('2023',className='text-center')
   ],
   ),
    dbc.Row([
        dbc.Col([], width=3),
        dbc.Col([
            dbc.Button(html.I(className="fas fa-angle-double-left me-2"), outline=True),
        ]),
        dbc.Col(
            [html.H4('December', className='text-center')],
                className={'textAlign': 'center'}),
        dbc.Col([
            dbc.Button(html.I(className="fas fa-angle-double-right me-2"), outline=True),
        ]),

    ],  align='center',
        justify='center'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
            html.H1(x, className='text-center'),
            ],style={'align-items': 'center',
                'height':'100px',
                'border-radius': '10px',
                'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                              'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'
            }
)
        ], width=1,
        ) for x in range(7)

    ],style={
                'margin-top':'15px'
            },
        align='center',
        justify='center'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
            html.H1(x,className='text-center')
            ],style={'align-items': 'center',
                'height':'100px',
                'border-radius': '10px',
                'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                              'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'
            }
)
        ], width=1,
        ) for x in range(7)

    ],style={
                'margin-top':'15px'
            },
        align='center',
        justify='center'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
            html.H1(x, className='text-center h-50')
            ],style={'align-items': 'center',
                'height':'100px',
                'border-radius': '10px',
                'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                              'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'
            }
)
        ], width=1,
        ) for x in range(7)

    ],style={
                'margin-top':'15px'
            },
        align='center',
        justify='center'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
            html.H1(x,className='text-center')
            ],style={'align-items': 'center',
                'height':'100px',
                'border-radius': '10px',
                'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                              'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'
            }
)
        ], width=1,
        ) for x in range(7)

    ],style={
                'margin-top':'15px'
            },
        align='center',
        justify='center'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
            html.H1(x, className='text-center h-50')
            ],style={'align-items': 'center',
                'height':'100px',
                'border-radius': '10px',
                'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                              'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'
            }
)
        ], width=1,
        ) for x in range(7)

    ],style={
                'margin-top':'15px'
            },
        align='center',
        justify='center'
    ),
],
    style={'padding': '0px',
          'margin-top':'-25px',
          'margin-left':'4rem'})