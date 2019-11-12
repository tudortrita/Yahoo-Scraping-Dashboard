# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output, State

import webbrowser

import pandas as pd

from download_stocks import symbol_dict

from dash.dependencies import Input, Output

import plotly.graph_objs as go


###############################################################################

list_of_symbols = list(symbol_dict.keys())
list_of_symbols.sort()

list_options = [{'label': i, 'value': symbol_dict[i]} for i in list_of_symbols]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
                label='Historical Prices Chart',
                id='tab1',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    dcc.Dropdown(id='dropdown-1',
                                 options=list_options,
                                 value=symbol_dict[list_of_symbols[0]],
                                ),
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
              [Input('dropdown-1', 'value')])
def update_figure_1(symbol):
    print(f"Symbol is {symbol}")
    df = pd.read_csv(f"data/{symbol}.csv")
    df.rename(columns={df.columns[0]: "Date"}, inplace=True)
    # Works above

    trace = [go.Scatter(x = df['Date'],
                       y = df['Close'],
                       mode='lines')]

    layout = go.Layout(xaxis={'title': 'Years'},
                       yaxis={'title': 'Closing Prices'},
                       hovermode='closest')


    OUTPUT = dcc.Graph(id = 'graph',
                       figure={'data': trace,
                               'layout': layout})
    return OUTPUT

# ###############################################################################
# # Update Tab 2
# ###############################################################################

@app.callback(Output('content-tab-2', 'children'),
              [Input('dropdown-2', 'value')])
def update_figure_2(symbol):
    df = pd.read_csv(f"data/{symbol}_financials.csv")
    df.rename(columns={df.columns[0]: "Date"},
              inplace=True)

    OUTPUT = dash_table.DataTable(id='financial-table',
                                  columns=[{"name": i, "id": i} for i in df.columns],
                                  data=df.to_dict("rows"),
                                  style_cell={'width'    : '300px',
                				              'height'   : '60px',
                				              'textAlign': 'left'})

    return OUTPUT

if __name__ == '__main__':
    app.run_server(debug=True)
