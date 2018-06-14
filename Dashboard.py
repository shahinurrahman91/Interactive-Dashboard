#Import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from datetime import datetime
import pandas as pd
import dash_auth

USERNAME_PASSWORD_PAIRS = [['Username','Password'],['Shawon','123456']]

app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server

nsdq = pd.read_csv('data/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})
                     #Appending an empty dictionary with label and value

app.layout = html.Div([
    html.H1('Stock Exchange Dashboard!', style={'paddingRight':'40px','text-align':'center','font-family':'Helvetica'}),
    html.Div([
        html.H3('Selection of stock symbols:', style={'paddingRight':'40px','font-family':'Helvetica'}),
        dcc.Dropdown(                      #Adding the Dropdown menu for different stocks
            id='my_ticker_symbol',
            options=options,
            value=['TSLA'],
            multi=True
        )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'38%'}),
    html.Div([
        html.H3('Selection of date range:'),
        dcc.DatePickerRange(              #Adding calendar to select a specific date range
            id='my_date_picker',
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2018, 1, 1),
            end_date=datetime.today()
        )
    ], style={'display':'inline-block', 'font-family':'Helvetica'}),
    html.Div([
        html.Button(                     #Create a submit button
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':18,'marginLeft':'35px','font-weight':'bold','background-color':'#e7e7e7','cursor':'pointer','font-family':'Helvetica'}
        ),
    ], style={'display':'inline-block'}),
    dcc.Graph(                         #Setup the graphs x and y axis outline
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    )
], style={'font-family':'Helvetica', 'background-color':'#3D7EB7'})
@app.callback(                  #Callback method, output graph, input submit button, state to select date range
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):     #Function to show the graph with the date range
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []                                      #Traces for selecting multiple stock name at a time and submit
    for tic in stock_ticker:
        df = web.DataReader(tic,'iex',start,end)
        traces.append({'x':df.index, 'y': df.close, 'name':tic})
    fig = {
        'data': traces,
        'layout': {'title':', '.join(stock_ticker)+' Closing Prices'},
    }
    return fig

if __name__ == '__main__':                        #Run the server
    app.run_server()
