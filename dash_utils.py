import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import flask
from flask import Flask
import pandas as pd
import dateutil.relativedelta
from datetime import date
import datetime
import yfinance as yf
import numpy as np
import praw
import sqlite3
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots




def make_table(id, dataframe, lineHeight = '17px', page_size = 5):
    '''
    The function is used to tweak the parameters of the table.
    '''
    return   dash_table.DataTable(
        id=id,
        css=[{'selector': '.row', 'rule': 'margin: 0'}],
        columns=[
            {"name": i, "id": i} for i in dataframe.columns
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': lineHeight
            },
        # style_table = {'width':300},
        style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
        style_cell_conditional=[
            {'if': {'column_id': 'title'},
            'width': '130px'},
            {'if': {'column_id': 'post'},
            'width': '500px'},
            {'if': {'column_id': 'datetime'},
            'width': '130px'},
            {'if': {'column_id': 'text'},
            'width': '500px'}],
        page_current=0,
        page_size=page_size,
        page_action='custom',
filter_action='custom',
        filter_query='',
sort_action='custom',
        sort_mode='multi',
        sort_by=[],
        #dataframe.to_dict('records')
        )


def make_card(alert_message, color, cardbody, style_dict = None):
    '''
    The function is used to combine Dash Bootstrap components Card and Alert. 
    Bootstrap’s cards provide a flexible content container and 
    allow a fair amount of customization. 
    Alert is used to easily add color and more style if desired
    '''
    return  dbc.Card([  dbc.Alert(alert_message, color=color)
                        ,dbc.CardBody(cardbody)
                    ], style = style_dict)#end card


def ticker_inputs(inputid, pickerid, month_cutoff):
    '''
    The function is used to return the components that allow the user 
    to enter the stock ticker and select a Start Date and End Date.
    '''
    #calculate the current date
    currentDate = date.today() 
    #calculate past date for the max allowed date
    pastDate = currentDate - dateutil.relativedelta.relativedelta(months = month_cutoff)
    #return the layout components
    return html.Div([
            dcc.Input(id = inputid, type = "text", placeholder = "MSFT")
            , html.P(" ")  
            , dcc.DatePickerRange(
            id = pickerid,
            min_date_allowed=pastDate,
            #max_date_allowed=currentDate,
            #initial_visible_month=dt(2017, 8, 5),
            start_date = pastDate,
            #end_date = currentDate
            )])


def make_item(button, cardbody, i):
    '''
    The function is used to build the price chart Accordion.
    '''
    return dbc.Card([
        dbc.CardHeader(
            html.H2(
                dbc.Button(
                    button,
                    color="link",
                    id=f"group-{i}-toggle",
                ))
        ),
        dbc.Collapse(
            dbc.CardBody(cardbody),
            id=f"collapse-{i}",
        )])