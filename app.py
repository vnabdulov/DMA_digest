import dash

# meta_tags are required for the app layout to be mobile responsive
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=[
                    dbc.themes.SPACELAB,
                    dbc.icons.FONT_AWESOME
                ],)

server = app.server
