import base64
import datetime
import io

from dash import dcc, html, dash_table

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

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])