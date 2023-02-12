
import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=[
                    dbc.themes.CERULEAN,
                    dbc.icons.FONT_AWESOME
                ],)

dom_dict_text = {'People': ['Need for additional FTE resources for software accounting.',
  'Need for training to increase talent capability.',
  'Possibility to hire more talent.'],
 'Technology': ['The interviewees are expressing frustration with the number of accounting systems being used',
  'Inaccurate and unreliable reporting due to multiple components using different accounting systems',
  'Lack of a unified accounting system across the department'],
 'Data Governance': ['Issues with data quality and reliability.',
  'Need for more context behind the data.'],
 'Deployment and Usage': ['No direct issues expressed.'],
 'Architecture and Integration': ['Inefficient financial reporting system',
  'The need for a financial reporting resource that accurately and consistently reports accounting system information.'],
 'Culture and Leadership': ['Issues with project funding, business case development, planning, communication, and involving customers and partners in setting direction.'],
 'Strategy and Approach': ['Lack of vision for consolidation and improvement of data quality and accessibility.']}

def create_dom_cards(dom_text=dom_dict_text):

    if dom_text:

        card_names_img_dict = {
            'Culture and Leadership':'assets/Culture and Leadership.png',
            'Strategy and Approach':'assets/Strategy and Approach.png',
            'People': 'assets/People.png',
            'Technology':'assets/Technology.png',
            'Data Governance':'assets/Data Governance.png',
            'Deployment and Usage':'assets/Deployment and Usage.png',
            'Architecture and Integration':'assets/Architecture and Integration.png'
        }
        domain_cards=[]
        for key in card_names_img_dict.keys():
            domain_cards.append(
                dbc.Col(
                    dbc.CardGroup(
                        [
                        dbc.Card(
                            dbc.CardImg(src=card_names_img_dict[key],
                                        className='position-absolute top-50 start-50 translate-middle',

                                        style={'height': '70px',
                                               'width': '70px',
                                               # 'margin-top':'80px'
                                               }
                                        ),
                            className="bg-primary",
                            style={"maxWidth": 100},
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(key, className="card-title"),
                                    dbc.Row([html.P('• '+x, className="card-text", ) for x in dom_text[key]]),
                                ]
                            )
                        ),

                        ],
                        style={'height':'100%'},
                    className="mt-3 shadow",
                ), width =4,
                align ='center',
                style={'height':'220px'}
                    )

            )

        domain_row = [
            dbc.Row(domain_cards[0:3],
                        align='center',
                    justify='around',
                    style={'margin-top': '10px'}

                    ),
            dbc.Row(domain_cards[3:6],
                    align='center',
                    justify='around',
                    style = {'margin-top': '10px'}

        ),
            dbc.Row(domain_cards[6],
                    align='center',
                    justify='around',
                    style = {'margin-top':'10px'}

                    )
        ]

        return domain_row

    else:
        pass



app.layout = html.Div(create_dom_cards(dom_dict_text))


if __name__ == '__main__':
    app.run_server(debug=True)
