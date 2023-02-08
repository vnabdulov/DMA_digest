import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

card_complete = dbc.Card(
    dbc.CardBody(
        [
            html.H3([html.I(className="fas fa-calendar-check me-2"), "Complete"], className="text-nowrap"),
            html.H3("1 / 15"),
        ], className="border-start border-primary border-5",
    ),
    className="text-center",
    style={
        'border-radius':'10px',
        'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                         'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px',
    }

)

card_current = dbc.Card(
    dbc.CardBody(
        [
            html.H3([html.I(className="fas fa-calendar-plus me-2"),
                     "Current"], className="text-nowrap"),
            html.H3("0"),
        ], className="border-start border-primary border-5"

    ),
    className="text-center",
    style={
        'border-radius':'10px',
        'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                         'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px',
    }
)

card_score = dbc.Card(
    dbc.CardBody(
        [
            html.H3([html.I(className="fas fa-gauge me-2"), "Average Score"], className="text-nowrap"),
            html.H3("1.9"),
        ], className="border-start border-primary border-5"
    ),
    className="text-center",
    style={
        'border-radius':'10px',
        'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                         'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px',
    }
)

layout = dbc.Container(
    dbc.Row(
        [dbc.Col(card_complete), dbc.Col(card_current), dbc.Col(card_score)],
    ),
    fluid=True,
)
