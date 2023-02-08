import base64
import datetime
import io
# import spacy
# import en_core_web_lg

from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from domain_cards import create_dom_cards


def sub_terms(interview_string):
    interview_string = interview_string.replace('Umm,','').replace('you know','').replace('Yeah.','').replace('Umm','').replace('Yeah,','').replace('Uh,',' ').replace('uh','').replace('Uh.','')
    interview_string = interview_string.replace('So yeah','').replace('Mm-hmm','').replace('OK','').replace('soften', 'SOFM').replace('Advanta','Advana').replace('Absolute you sock', 'USASOC').replace('you sock','USASOC')
    interview_string = interview_string.replace('advanta','Advana').replace('sofam','SOFM').replace('soft 18','SOF AT&L').replace('socom','SOCOM').replace('soft ATL', 'SOF AT&L').replace('So.','')
    interview_string = interview_string.replace('SOFM','Special Operations Financial Management').replace('army','Army').replace('Defassa','DFAS').replace('USO COM','USSOCOM').replace('banana','Advana')
    interview_string = interview_string.replace('SOF', 'Special Operations Forces').replace('services','Services').replace('ADVANTA','Advana').replace('.Uh','').replace('Evanna','Advana').replace('Vanna','Advana')
    interview_string = interview_string.replace('SOCOM', 'Special Operations Command').replace('OSD','Office of the Secretary of Defense').replace('G socks',"TSOCs")
    return interview_string

def convert_interview_df(df):
    import pandas as pd
    df['text']=df['text'].apply(lambda x: sub_terms(x))
    # takes the interview df and breaks out start and end time and
    # consolidated the speaker text
    interview_text = []
    df_matter = []
    df['start_time'] = df.time.apply(lambda x: x.split('-->')[0])
    df['end_time'] = df.time.apply(lambda x: x.split('-->')[1])
    df['speaker'] = df['speaker'].apply(lambda x: x[:-19])

    for index, row in df.iterrows():
        set_speaker = row['speaker']

        if index == 0:
            cur_speaker = row['speaker']
            start_time = row['start_time']

        if set_speaker == cur_speaker:
            interview_text.append(row['text'])
            end_time = row['end_time']
            if index == df.size:
                df_matter.append([cur_speaker, ''.join(interview_text), start_time, end_time])
        else:
            df_matter.append([cur_speaker, ''.join(interview_text), start_time, end_time])
            start_time = row['start_time']
            cur_speaker = row['speaker']
            interview_text = [row['text']]
            end_time = row['end_time']

    converted_df = pd.DataFrame(df_matter)
    converted_df.columns = ['speaker', 'text', 'start_time', 'end_time']

    return converted_df

def get_time_per_speaker(df):
    import pandas as pd

    df['start_time'] = df['start_time'].str.strip()
    df['start_time'] = pd.to_datetime(df['start_time'], format='%H:%M:%S.%f')

    df['end_time'] = df['end_time'].str.strip()
    df['end_time'] = pd.to_datetime(df['end_time'], format='%H:%M:%S.%f')
    # Create a column for the duration of each speech
    df['duration'] = df['end_time'] - df['start_time']

    # Convert the duration column to seconds
    df['duration'] = df['duration'].dt.total_seconds()

    # Group the data by speaker and sum the duration for each speaker
    speaker_durations = df.groupby('speaker')['duration'].sum().reset_index()

    # Convert the start_time and end_time columns back to strings
    df['start_time'] = df['start_time'].dt.strftime("%H:%M:%S.%f")
    df['end_time'] = df['end_time'].dt.strftime("%H:%M:%S.%f")

    return speaker_durations, df

def get_gpt_api():
    from pyChatGPT import ChatGPT
    session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..q46uzUDwBWXO9UZe.LvyZX9xw-XE4lgMBJCaGrLK_RWXKTVyQ37xm7Tm-sXcofPzaroaEinswo1LjqbW_Znh8YBWxys0W4Tx_6cIwOEyaKK0MxnWN1pkSfl1QsFNK8wLKaP7RWK5l1a4MR7qKApN5qQKOAurGuSJmKTUitDz0LBy4oJFN8hl7oCIhgRT7xBhc7LdMXLXKjyCngPporG4HUML175C1V2gONwVoei47zj9QiUFvX-LSAGUWE-mCWpiRo0AOPMkPb7DKH6JaQMGZ7kr5gS0wHbpR2o3CtduRpylx-SkeU8zsqLzFqkPnqIt1zRTFKEo0pwdnQMPSwt2s8sp-tA5IKUY7lF3NNe8hXSvJh6-0IpkCJUZx9mgl_aufeLEUZ-WIJbiiAeCF28GaVbAQFI4Yz08DLPHlVYSoG_8W5Mha9BS8dQ6ZAGXRAGIzK2j_kQIjdoIvCyaPqoTEsp5S9fi8yf2tYRkZPgT2DTEJ5dMy2xbKFaYszq--RHCntjCnrc319oSH3PDqBj6-UA10bt_xws5pc2-wmv0jYP-kCxzj8CYNPVKbOO-XI5rTFDrgirHt-M8bZq06sMeAYZ8b0IjDuCw4TPKksRxxzjsO76YO_hOpdN3d0N5qFYjJB4xgrouPYDM0uec-SlHs9DCUZOI0V1p4H_dnHqvZIf_WQ3QwEpjT6zn7XuEe0SFX87PJg0PVTsoQ4NHLJY2tB9EsK1DF9ZnoBKto-M4s9fSZfYt0zW0HRAGCEhExveGnRuZksS7bxgX3vRLC0BjZAM4LLaRcKn8tq-ZAo9Y3kW_PDi9pk0BtW1GIImhXPLYGgol_VY7P_LeSukoraksTrkkDXBdPWLwLVvdVOCeSnXidy3VTKvECM4ENf7wmfVbk2hIonfcxco8pMWcQcCSFNB8sBY8lbAyIjaaIC4M0Sae8vOthEPJC5cVO-ykvDWmkoSkvihpCeH5TKTRnMUFqld4S6tHyCdSA9MHS8-MHimFWNZ9sgD5kjIu-7JNuueFcuUxhwCnrv1OnfjwWgnJqvzXlcqgMaFovgrBPyi7XM0H84G70Av0N_yQp1DABBjPkT4Gu7fL--XATXuoUro1uwzQjcTOGowQit1RvZGoJFupPf_e6zQphDBq3TQpQfECXzDEAAJIqzQXwAUwqMD_YqptjxUIpHg5bXfNs1AFSIBAwn1UHWKg3rkJOQhjJZpcb5bN-RgUpefUAqFEcZQc_dkMqZX3QEKpN1OW914sUiA0XTMJTO0jS2FZH6DZr995IbdYXvapiDpy4m6TX0HJrzH_XA3PelkPiT-1Q5tH8aPUaaJjAoiXAf0HkadCkX7MwFfMWm9E9Da6w6YZJXRCXIfSs93C9vArjuuA_uhRJ7CwDgX8XQ1IuCURP1O4l5fCLB5B08uzwydTlahCXKxkKHKAN3x6Q8ApK_Ufq5VIQ5O727FxDMUHF-lJgOL6wVNCHfFvM2259Qd3FshkxUx_ZwAQgkNMbKmDHoxsHVQYsGzLihvXhimmSSTgHRoGKNbzkhsMUlEjwqZd12tIjANBL_VV7dTk3nAfpJCJ-2SvVvRilVvPO9eLCBBMVNqRn3rstK-fVa-Q8K12_xEKsCKA0T3cCTKZbvMTsCakPrNK3dgo4mGVEjogiPf79G626FHdMEc7zAhjzRsqeZoIO1KQUIWiscWkRl5c_-wyLx6fniu3l-ntwR-h3c1tcmhygkNf8nnPYd75n4_a9DbP4lkCNDhx6wBdr6P7zB0O1NYkcsUre-LinfaFyKfeu-Nnm5vD6rHtNPcigwG9Mog0me1Zc4NySO2T2Qfb1IunTg2WocWW9xhrgrdDU5kNtbb-FgvaLx-VagFMxz0y5nZbYhdz_tOgulWetbGrqSTkyfRMdWU7RSxD3nG9ooBvpLpGe4vtRz3Gt-4V-BHczl9PTtQuT7ZmjKdzC3trLTUUzE5h7hpsvKk_A5jIUdKfC3Nh5si_4iMqfX18a878bW0BI-jz0A_tKSKLSgPMoCxxhC7c1aDvGE2YGqLNoe-JAED9PKQyJeLNjCMWYfR8ggF6ML_AAgXhO286dTn6w8vXTUE4An2wdOO6a5TUiXBUuo_jZ-h2HMFuXP0naASQdeMkCKOJheDDZwW9FZwnGq7k5wCAtqX0kEHp9I797q7ND3HdAmpi2kQtXIHiW6b4kpm0knSbJvODw-8ZooKA1cwC4OGGVcVIktjqHOF0oiQOBm7aNUlhvZdqQ9oezaw96Y3kU2Z2FjnaaTbTeuuKCvVmzLYqIWK984SSzDg7tlezzq0AWjVGqnzSoUD-8jXZRpTuvKpcNMuPxKLEKpZ45HrA268i78qjITrq9zSJ7EIKaOk3RjlRxSjv6t8XhdpWFE-1ohwk_UhzgeRSrslRzunQqySJAl6YprcpItf_n8PN7NEPKNhlRUQ0OvelxUYZNYxkvhCbwSLH51yFGqRm7MmSDYmhtGgwCJvE1W1VhpLwZlobhPCE_mU9sI8sX73sot9e18W-58mevMdrSj4stN1jPLhQfQF818zpE.-xxAAQMTPl5Jl3oJUJ9pfw'
    api = ChatGPT(session_token)
    return api

def generate_chunks(df):
    df = process_df(df)
    full_text = ''.join(x for x in df.drop_duplicates(subset=['interview_text']).interview_text)
    chunks =[]
    start = 0
    end = 2200
    final_end = len(full_text.split())
    for x in range(final_end//2000+1):
        try:
            chunks.append(' '.join(x for x in full_text.split()[start:end]))
            start +=2200
            end+=2200
        except:
            chunks.append(' '.join(x for x in full_text.split()[end:final_end]))
    print(len(chunks), ' chunks to analyze')
    return chunks

def remove_repeated_punct(string):
    from itertools import groupby
    from string import punctuation

    newtext = []
    for k, g in groupby(string):
        if k in set(punctuation):
            newtext.append(k)
        else:
            newtext.extend(g)

    return ''.join(newtext)

def generate_issues(chunks):
    question = '''
                Based on the following data maturity domains:
                Culture and Leadership Domain
                Looks at indicators related to organizational DNA, and the degree to which leadership is a sponsor and champion of becoming more “data-driven.”
                Strategy and Approach Domain
                Includes indicators of the organization's capabilities related to  project funding, business case development, planning and communication, and the involvement of customers and partners in setting direction.
                People Domain
                Looks at how well established various key data & analytics roles are, and whether they are staffed and organized optimally, and how well they interoperate. 
                Technology Domain
                Considers the organization’s overall data and analytics infrastructure capabilities, capacity, availability, performance, resilience, and scalability. 
                Data Governance Domain
                Assesses how well the organization defines principles and policies, and executes processes for ensuring the proper definition, handling, and use of enterprise data assets. 
                Deployment and Usage Domain
                Considers how well the organization takes advantage of available data assets and analytic output.
                Architecture & Integration Domain
                Looks at how well data flows and models support the organization’s analytics needs, and how flexible and scalable they are.

                What issues are the interviewees expressing in the following text ? (in a bulletpoint format by domain) : 
                '''

    issues = []
    for c in chunks:
        issues.append(api.send_message(question + c)['message'])
    return ''.join(issues)


# def generate_cards(domain_prompts):
#     domains =
#     domain_images =
#     domain_prompt =


# def get_top_ten_ents(df):
#     import spacy
#     nlp = spacy.load("en_core_web_lg")
#     entities =


layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename, date):
    import pandas as pd
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'docx' in filename:
            import docx
            file = io.BytesIO(decoded)
            doc = docx.Document(file)
            text = ""
            for para in doc.paragraphs:
                text += para.text+"\n"
            try:
                file_data = text.split('\n')
                paragraphs = []
                s = 0
                f = 3
                for x in range(len(file_data) // 3):
                    paragraphs.append(file_data[s:f])
                    s += 3
                    f += 3
                import pandas as pd
                df = pd.DataFrame(paragraphs)
                df.columns = ['time', 'speaker', 'text']
            except Exception as e:
                print(e)
                return html.Div([
                    'There was an error parsing this file.'
                ])

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    import plotly.express as px

    c_df = convert_interview_df(df)
    speaker_durations, prompt_duration_df = get_time_per_speaker(c_df)
    speaker_colors = {}
    speakers = df.speaker.unique()
    colors = [x for x in px.colors.qualitative.T10]
    for x in range(len(speakers)):
        speaker_colors[speakers[x]] = colors[x]

    speaker_durations = speaker_durations[speaker_durations['duration']>0]
    speaker_durations.reset_index(drop=True, inplace=True)
    # print(speaker_durations['duration'].tolist())

    # Plot the bar graph
    fig_speaker_durations = px.bar(speaker_durations,
                                   x='duration',
                                   y='speaker',
                                   color='speaker',
                                   color_discrete_map=speaker_colors,
                                   text = 'speaker',
                                   )

    # Remove the background
    fig_speaker_durations.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # transparent
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None,
        yaxis_title=None,
        margin = dict(t=3, b=3, l=3, r=3),
        legend=dict(
                title="Speaker",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
    )
    fig_speaker_durations.update_xaxes(showticklabels=False)
    fig_speaker_durations.update_yaxes(showticklabels=False)

    fig_prompt_duration = px.bar(prompt_duration_df.reset_index(),
                                 x='index',
                                 y='duration',
                                 color='speaker',

                 color_discrete_map=speaker_colors)
    # Remove the background
    fig_prompt_duration.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # transparent
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        xaxis_title=None,
        yaxis_title=None,
        margin = dict(t=3, b=3, l=3, r=3),
        legend=dict(
            title="Speaker",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig_prompt_duration.update_xaxes(showticklabels=False)
    fig_prompt_duration.update_yaxes(showticklabels=False)
    fig_prompt_duration.update_traces(width=0.5)

  #######################subplots variation######################################################
    # from plotly.subplots import make_subplots
    # # For as many traces that exist per Express figure, get the traces from each plot and store them in an array.
    # # This is essentially breaking down the Express fig into it's traces
    # prompt_duration_traces = []
    # speaker_durations_traces = []
    # for trace in range(len(fig_speaker_durations["data"])):
    #     speaker_durations_traces.append(fig_speaker_durations["data"][trace])
    # for trace in range(len(fig_prompt_duration["data"])):
    #     prompt_duration_traces.append(fig_prompt_duration["data"][trace])
    #
    # # Create a 1x2 subplot
    # fig_bothplots = make_subplots(rows=1,
    #                               cols=2,
    #                               column_widths=[0.3, 0.7],
    #                               horizontal_spacing=0.01,
    #                               subplot_titles=('Speaker Participation', 'Interview Flow')
    #                               )
    #
    # # Get the Express fig broken down as traces and add the traces to the proper plot within in the subplot
    # for traces in speaker_durations_traces:
    #     fig_bothplots.append_trace(traces, row=1, col=1)
    # for traces in prompt_duration_traces:
    #     fig_bothplots.append_trace(traces, row=1, col=2)
    #
    #
    # fig_bothplots.update_layout(
    #     paper_bgcolor='rgba(0,0,0,0)',  # transparent
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     xaxis_title=None,
    #     yaxis_title=None,
    #     margin=dict(t=10, b=10, l=3, r=3),
    #     legend=dict(
    #             title="Speaker",
    #             # font=dict(size=15),
    #             orientation="h",
    #             yanchor="bottom",
    #             y=1.02,
    #             xanchor="right",
    #             x=1
    #         )
    # )
    # fig_bothplots.update_xaxes(showticklabels=False)
    # fig_bothplots.update_yaxes(showticklabels=False)
##########################################################







###############################################################
    return html.Div([
        html.Div(create_dom_cards(),
                 style={
                     'margin-top':'10px',
                     'display': 'inline-block'
                 },  ),
        html.H6(f'Filename: {filename}',  style={'margin-top':'20px'}),
        html.H6(datetime.datetime.fromtimestamp(date)),
        # dbc.Row([
        #     dcc.Graph(figure=fig_bothplots),
        # ], style={
        #           'margin-top': '10px',
        #             'border-radius':'10px',
        #           'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
        #                         'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'}),

    # the subplot as shown in the above image
    # fig_bothplots.update_layout(legend=dict(
    #     title="Speaker",
    #     orientation="h",
    #     yanchor="bottom",
    #     y=1.02,
    #     xanchor="right",
    #     x=1
    # ))
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Interview Participation', style={'font-weight': 'bold', 'text-align': 'left'}),
                    dcc.Graph(figure=fig_speaker_durations),

                ], className="text-center",
                    style={
                        'margin-top': '10px',
                        'border-radius': '10px',
                        'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                                      'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'}
                ),
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Interview Flow', style={'font-weight': 'bold', 'text-align': 'left'}),
                    dcc.Graph(figure=fig_prompt_duration),

                ], className="text-center",
                    style={
                        'margin-top': '10px',
                        'border-radius': '10px',
                        'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                                      'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'}

                ),
            ])


        ],
            style={
                  'margin-top': '10px'
            }
                    ),

        dbc.Row([
            dbc.Card([
                dash_table.DataTable(
                    c_df.to_dict('records'),
                    [{'name': i, 'id': i} for i in df.columns],
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'text'},
                            'textAlign': 'left'
                        }],
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    },

                ), ],
                style={
                    'margin-top': '10px',
                    'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                                  'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'}
            ),
        ],
            style={
                'margin-top': '10px',
                'border-radius': '10px',
                'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                              'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'}
        ),


        html.Hr(),  # horizontal line


    ])