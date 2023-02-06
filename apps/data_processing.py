import base64
import datetime
import io
import spacy
import en_core_web_lg
nlp = spacy.load("en_core_web_lg")

from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc


def convert_interview_df(df):
    import pandas as pd
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

def get_top_ten_ents(df):
    import spacy
    nlp = spacy.load("en_core_web_sm")


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

    # Plot the bar graph
    fig_speaker_durations = px.bar(speaker_durations,
                                   x='duration',
                                   y='speaker',
                                   color='speaker',
                                   color_discrete_map=speaker_colors)

    # Remove the background
    fig_speaker_durations.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # transparent
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(title="Speaker"),
        xaxis_title=None,
        yaxis_title=None

    )
    fig_speaker_durations.update_xaxes(showticklabels=False)

    fig_prompt_duration = px.bar(prompt_duration_df.reset_index(),
                                 x='index',
                                 y='duration',
                                 color='speaker',
                 color_discrete_map=speaker_colors)
    # Remove the background
    fig_prompt_duration.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # transparent
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(title="Speaker"),
        xaxis_title=None,
        yaxis_title=None
    )
    fig_prompt_duration.update_xaxes(showticklabels=False)
    fig_prompt_duration.update_yaxes(showticklabels=False)


    return html.Div([
        html.H6(f'Filename: {filename}'),
        html.H6(datetime.datetime.fromtimestamp(date)),
        dbc.Card([
            dbc.CardHeader('Interview Participation', style={'font-weight':'bold','text-align':'left'}),
            dcc.Graph(figure=fig_speaker_durations),

        ],className="text-center",
            style={
                'margin-top': '10px',
                'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                              'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'}
        ),
        dbc.Card([
            dbc.CardHeader('Interview Flow', style={'font-weight':'bold','text-align':'left'}),
            dcc.Graph(figure=fig_prompt_duration),

        ],className="text-center",
        style={
            'margin-top':'10px',
            'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                         'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'}
        ),
        dbc.Card([
        dash_table.DataTable(
            c_df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            style_cell_conditional=[
                {
                    'if': {'column_id': 'text'},
                    'textAlign': 'left'
                }],
            style_data = {
                'whiteSpace':'normal',
                'height':'auto'
            },

        ),],
            style={
            'margin-top':'10px',
            'box-shadow': 'rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, '
                         'rgba(0, 0, 0, 0.3) 0px 3px 7px -3px'}
        ),

        html.Hr(),  # horizontal line


    ])