""" Program to display historical price and financial data for
@author: Tudor Trita
@date: 12/11/2019
"""
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from download_stocks import symbol_dict  # Custom import

###############################################################################
# Parameters:
###############################################################################
list_of_symbols = list(symbol_dict.keys())
list_of_symbols.sort()
list_options = [{'label': f"{i} - ({symbol_dict[i]})", 'value': symbol_dict[i]} for i in list_of_symbols]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


###############################################################################
# Contructing main app layout:
###############################################################################

app.layout = html.Div([
    html.Div(
        html.H1('Dashboard - Tudor Trita')
    ),
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-2',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Historical Data Chart',
                id='tab1',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    dcc.Dropdown(id='dropdown-1',
                                 options=list_options,
                                 value=symbol_dict[list_of_symbols[0]],
                                ),
                    html.H6('Data to display:'),
                    dcc.RadioItems(
                        id='radio-items-1',
                        options=[
                            {'label': 'Open', 'value': 'Open'},
                            {'label': 'Close', 'value': 'Close'},
                            {'label': 'High', 'value': 'High'},
                            {'label': 'Low', 'value': 'Low'},
                            {'label': 'Adj Close', 'value': 'Adj Close'},
                            {'label': 'Volume', 'value': 'Volume'}],
                        value='Close',
                        labelStyle={'display': 'inline-block', 'text-align': 'justify'}),
                    html.H6('Indicators:'),
                    dcc.RadioItems(
                        id='radio-items-2',
                        options=[
                            {'label': 'None', 'value': 0},
                            {'label': 'Moving Averages', 'value': 'MA'},
                            {'label': 'Bollinger Bands', 'value': 'BA'},],
                        value=0,
                        labelStyle={'display': 'inline-block', 'text-align': 'justify'}),
                    html.Div(id='content-tab-1')
                ]
            ),
            dcc.Tab(
                label='Financials Data',
                id='tab2',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    dcc.Dropdown(id='dropdown-2',
                                 options=list_options,
                                 value=symbol_dict[list_of_symbols[0]],
                                ),
                    html.Div(id='content-tab-2')
                ]
            ),
        ]),
    html.Div(id='tabs-content-classes')
])


###############################################################################
# UPDATE TAB CONTENT
###############################################################################
@app.callback(Output('tabs-content-classes', 'children'),
              [Input('tabs-with-classes', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return

    elif tab == 'tab-2':
        return


###############################################################################
# Update Tab 1
###############################################################################
@app.callback(Output('content-tab-1', 'children'),
              [Input('dropdown-1', 'value'),
               Input('radio-items-1', 'value'),
               Input('radio-items-2', 'value')])
def update_figure_1(symbol, price_category, indicators):
    df = pd.read_csv(f"data/{symbol}.csv")
    df.rename(columns={df.columns[0]: "Date"}, inplace=True)
    x = df['Date']
    y = df[price_category]

    if indicators == 'MA':
        twenty_day_ma = y.rolling(window=20).mean()
        fifty_day_ma = y.rolling(window=50).mean()
        data_to_plot = [y, twenty_day_ma, fifty_day_ma]
        names = [price_category,
                 f"{price_category} 20-Day Moving Average",
                 f"{price_category} 50-Day Moving Average"]
        trace = []
        for i, data in enumerate(data_to_plot):
            trace.append(go.Scatter(x=x, y=data, mode='lines', name=names[i]))

    elif indicators == 'BA':
        thirty_day_ma = y.rolling(window=30).mean()
        thirty_day_std = y.rolling(window=30).std()
        upper_band = thirty_day_ma + thirty_day_std*2
        lower_band = thirty_day_ma - thirty_day_std*2
        data_to_plot = [y, upper_band, lower_band]

        names = [price_category,
                 f"{price_category} 30-Day Upper Band",
                 f"{price_category} 30-Day Lower Band"]
        trace = []
        for i, data in enumerate(data_to_plot):
            trace.append(go.Scatter(x=x, y=data, mode='lines', name=names[i]))

    else:
        trace = [go.Scatter(x=x, y=y, mode='lines')]
    layout = go.Layout(xaxis={'title': 'Years'},
                       yaxis={'title': price_category},
                       hovermode='closest')
    OUTPUT = dcc.Graph(id = 'graph',
                       figure={'data': trace,
                               'layout': layout})
    return OUTPUT


###############################################################################
# Update Tab 2
###############################################################################
@app.callback(Output('content-tab-2', 'children'),
              [Input('dropdown-2', 'value')])
def update_figure_2(symbol):
    df = pd.read_csv(f"data/{symbol}_financials.csv")
    df.rename(columns={df.columns[0]: "Date"}, inplace=True)
    df = df.set_index('Date').T.reset_index()
    df.rename(columns={df.columns[0]: "Fundamental|Date"},
              inplace=True)
    OUTPUT = dash_table.DataTable(id='financial-table',
                                  columns=[{"name": i, "id": i} for i in df.columns],
                                  data=df.to_dict("rows"),
                                  style_cell={'width'    : '300px',
                				              'height'   : '60px',
                				              'textAlign': 'left'})
    return OUTPUT


if __name__ == '__main__':
    print("Begin running server.")
    print("Please open following IP Address in a browser:")
    app.run_server(debug=True)
    print()
    print("Server closed")
