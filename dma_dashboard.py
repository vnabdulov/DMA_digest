import dash_bootstrap_components as dbc
from dash import Input,State, Output, dcc, html
from app import app

server = app.server

sidebar = html.Div([
        html.Div(
            [
                dbc.CardImg(src="/assets/datamatter.png", style={'width':'47px'}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"),
                     html.Span("Overview")],
                    href="apps/overview",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-calendar-alt me-2"),
                        html.Span("Schedule"),
                    ],
                    href="apps/schedule",
                    active="exact",
                ),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)


jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Jumbotron", className="display-3"),
            html.P(
                "Use Containers to create a jumbotron to call attention to "
                "featured content or information.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "Use utility classes for typography and spacing to suit the "
                "larger container."
            ),
            html.P(
                dbc.Button("Learn more", color="primary"), className="lead"
            ),
        ],
        fluid=True,
        className="py-3",
    ), style={
        'margin-left': '4rem'
    },
    className="p-3 bg-light rounded-3",
)

content_style = {
    "margin-top": "0rem",
    "padding": "2rem 1rem",
    }
content = html.Div(id="page-content", style=content_style)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


from apps import overview, schedule


#create a callback to display the pages
@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])

def render_page_content(pathname):

    if pathname == "/apps/overview":
        return overview.layout
    elif pathname == "/apps/schedule":
        return schedule.layout
    # If the user tries to reach a different page, return a 404 message
    else:
        return jumbotron

if __name__ == "__main__":
    app.run_server(debug=True)


