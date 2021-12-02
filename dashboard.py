import pathlib
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = df['Indicator Name'].unique()


app_path = str(pathlib.Path(__file__).parent.resolve())
home = pd.read_csv(os.path.join(app_path, os.path.join("data", "smarthome.csv")))

fruits = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig_fruits = px.bar(fruits, x="Fruit", y="Amount", color="City", barmode="group")


app = dash.Dash(__name__, url_base_pathname='/dashboard/')
server = app.server

theme = {
    'background': '#1e2130',
    'text': '#7FDBFF'
}


def build_banner_energy_consumption():
    return html.Div(
        className='col-sm-10 row banner',
        children=[
            html.Div(
                className='banner-text',
                children=[
                    html.H5('Enegry Consumption'),
                ],
            ),
        ],
    )


def build_banner_fruits():
    return html.Div(
        className='col-sm-10 row banner',
        children=[
            html.Div(
                className='banner-text',
                children=[
                    html.H5('Fruit supply'),
                ],
            ),
        ],
    )


def build_banner_interactive():
    return html.Div(
        className='col-sm-10 row banner',
        children=[
            html.Div(
                className='banner-text',
                children=[
                    html.H5('Sample interactive chart'),
                ],
            ),
        ],
    )



def build_graph():
    return dcc.Graph(
        id='basic-interactions',
        figure={
            'data': [
                {
                    'x': home['Batch'][:50],
                    'y': home['Techniques'][:50],
                    'name': 'Techniques',
                    'marker': {'size': 12}
                },
                {
                    'x': home['Batch'][:50],
                    'y': home['Workplace'][:50],
                    'name': 'Workplace',
                    'marker': {'size': 12}
                },
                {
                    'x': home['Batch'][:50],
                    'y': home['Garage'][:50],
                    'name': 'Garage',
                    'marker': {'size': 12}
                },
                {
                    'x': home['Batch'][:50],
                    'y': home['Kitchen'][:50],
                    'name': 'Kitchen',
                    'marker': {'size': 12}
                },
                {
                    'x': home['Batch'][:50],
                    'y': home['Hall'][:50],
                    'name': 'Hall',
                    'marker': {'size': 12}
                },
            ],
            'layout': {
                'plot_bgcolor': theme['background'],
                'paper_bgcolor': theme['background'],
                'font': {
                    'color': theme['text']
                }
            }
        }
    )


app.layout = html.Div(
    className='big-app-container',
    children=[
       
        html.H1(
        children='Dmitry Artemasov - test dashboard',
        style={
            'textAlign': 'center',
            'color': theme['text']
        }),

        build_banner_energy_consumption(),
        

        html.Div(
            className='app-container',
            children=[
                build_graph(),
            ]
        ),

        build_banner_fruits(),

        dcc.Graph(
            id='fruits',
            figure=fig_fruits
        ),


        build_banner_interactive(),

        html.Div([

                html.Div([
                    dcc.Dropdown(
                        id='crossfilter-xaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Fertility rate, total (births per woman)',
                        style={'color': theme['background']}
                    ),
                    dcc.RadioItems(
                        id='crossfilter-xaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                    )
                ],
                style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(
                        id='crossfilter-yaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Life expectancy at birth, total (years)',
                        style={'color': theme['background']}

                    ),
                    dcc.RadioItems(
                        id='crossfilter-yaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                    )
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
            ], style={
                'padding': '10px 5px'
            }),

            html.Div([
                dcc.Graph(
                    id='crossfilter-indicator-scatter',
                    hoverData={'points': [{'customdata': 'Japan'}]}
                )
            ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
            html.Div([
                dcc.Graph(id='x-time-series'),
                dcc.Graph(id='y-time-series'),
            ], style={'display': 'inline-block', 'width': '49%'}),

            html.Div(dcc.Slider(
                id='crossfilter-year--slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].max(),
                marks={str(year): str(year) for year in df['Year'].unique()},
                step=None
            ), style={'width': '49%', 'padding': '0px 20px 20px 20px', 'color': theme['text']})



                
    
    ]
)



@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name']
            )

    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def create_time_series(dff, axis_type, title):

    fig = px.scatter(dff, x='Year', y='Value')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)
