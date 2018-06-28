import dash
from dash.dependencies import Input,Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import base64

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go

from collections import deque
import queue
import numpy as np
import random
import logging
import can 
import os
import time
import threading
from threading import Thread
#from multiprocessing import Pool
#from multiprocessing.dummy import Pool as ThreadPool

# surpress logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

##################################
# init can bus globals
##################################
freq = 0.5 # set receiver frequency: 0.2
num_sens = 2 # number of sensor data 
cells = 6 # number of cells per battery pack (accus)
buff_len = 20 # length buffer
thres = 0.95 # threshold warning

# init buffer
q = queue.Queue()

a1_V_list = [] # accu 1 voltage
a1_T_list = [] # accu 1 temperature
a2_V_list = [] # accu 2 voltage
a2_T_list = [] # accu 2 temperature
for cell in range(cells):
	a1_V_list.append(deque([0] * buff_len,maxlen= buff_len))
	a1_T_list.append(deque([0] * buff_len,maxlen= buff_len))
	a2_V_list.append(deque([0] * buff_len,maxlen= buff_len))
	a2_T_list.append(deque([0] * buff_len,maxlen= buff_len))
	
##################################
# init dash globals
##################################
colors = {
    'background': '#424242',
    'text': '#7FDBFF',
    'head': '#7996c4',
    'c1': '#e5eefd',   
}
# init layouts
text_style_1 = dict(color='#444', textAlign = 'left', 
                    fontFamily='sans-serif', fontWeight=300) 
text_style_2 = dict(color='#444', textAlign = 'center', 
                    fontFamily='sans-serif', fontWeight=600) 
text_style_01 = dict(color='#444', textAlign = 'center', 
                     fontFamily='sans-serif', fontWeight=1000) 
div_style_01 = {'backgroundColor': colors['background'],
                'color': colors['text'], 'marginTop': 0, 
                'marginLeft': 0, 'marginRight': 0}

app = dash.Dash(__name__)
# in case of running the pi without internet connection
# you need download css, js scripts and need to activate
# both serve_locally = True 
#app.css.config.serve_locally = True # for local css
#app.scripts.config.serve_locally = True # for local js

app.layout = html.Div([
        ########## navbar header ##########       
        html.Div([
            html.Div([
            html.Div([html.H3(" Battery Monitoring System", style={
                'padding-left' : '-1',
                'margin-left' : '-1',
                'margin-top': '15',
                'color': '#FFFFFF', 
                'textAlign' : 'center',
                'height' : '45'
					}, )]),         
		], className="col-lg-12"),
		], className="row", style={
                'backgroundColor': colors['background'], 
					},),
						
		html.Div([
		html.Div([	
		########## battery control panel ##########
		html.Div([
		html.Div([
        html.Div([
        html.H3(" Control Panel",className="card-title text-center", style={},),
        html.Hr(),
        html.H4(" Battery Pack 1",className="card-title text-center"),
        html.Div([
        html.Div([
                  html.Button('Load Pack 1', id='button-1', className="btn btn-secondary btn-lg btn-block", style={
                              'margin-top' : '12',
                              'margin-bottom' : '0',
                              'padding-top' : '20',
                              'padding-bottom' : '20',       
        }), ], className="col-lg-12 col-md-12 col-xs-4",)
        ], className="row"), 
        
        html.Div([
        html.Div([
                  html.Button('Stop Loading', id='button-2', className="btn btn-secondary btn-lg btn-block", style={
                              'margin-top' : '14',
                              'margin-bottom' : '0',
                              'padding-top' : '20',
                              'padding-bottom' : '20',       
        }), ], className="col-lg-12 col-md-12 col-xs-4",)
        ], className="row"), 
        html.Hr(),
        
        html.H4(" Battery Pack 2",className="card-title text-center"),
        html.Div([
        html.Div([
                  html.Button('Load Pack 2', id='button-3', className="btn btn-secondary btn-lg btn-block", style={
                              'margin-top' : '12',
                              'margin-bottom' : '0',
                              'padding-top' : '20',
                              'padding-bottom' : '20',       
        }), ], className="col-lg-12 col-md-12 col-xs-4",)
        ], className="row"), 
        
        html.Div([
        html.Div([
                  html.Button('Stop Loading', id='button-4', className="btn btn-secondary btn-lg btn-block", style={
                              'margin-top' : '14',
                              'margin-bottom' : '0',
                              'padding-top' : '20',
                              'padding-bottom' : '20',      
        }), ], className="col-lg-12 col-md-12 col-xs-4",)
        ], className="row"), 
        html.Hr(),
        
        html.Div(id='button1-out', style={'display':'none'}),
        #html.H5(id='button1-out', style=text_style_2),
        #html.Div(id='button1-out',children='Value')
        ], className="card-body ", style={
                'backgroundColor': colors['c1'],},),
		],className="card", style={	
        }),
		], className="col-lg-2 col-xs-12 ", style={
        }),		
		########## battery pack 1 ##########		
		html.Div([
		
		html.Div([
		          html.H4(" Battery Pack 1")
		          ], className="card-header text-center text-white mb2",style={
                'backgroundColor': colors['head'],'padding-top' : '15','padding-bottom' : '8',},),
        html.Div([
        html.Div([
        
        html.Div([
        html.Div([
            dcc.Graph(id='g01',),
            dcc.Interval(id='graph-update', interval= 2000 * 1),
        ],className="row", style={}),    
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        
        html.Div([
         html.Div([
            dcc.Input(id='input-01',readonly=True, type='text',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '0','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),                 
            dcc.Input(id='input-02',readonly=True, type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-03', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-04', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row ", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        html.Hr(),
        html.Div([
        html.Div([
            dcc.Graph(id='g02',),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center", style={}),
        
        html.Div([   
        html.Div([
            dcc.Input(id='input-05', type='text',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '0','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),                
            dcc.Input(id='input-06', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-07', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-08', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}), 
        html.Hr(),
        html.Div([
        html.Div([
            dcc.Graph(id='g03',),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center", style={}),
        
        html.Div([
           html.Div([
            dcc.Input(id='input-09', type='text',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '0','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),                
            dcc.Input(id='input-10', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-11', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-12', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row", style={}), 
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
          html.Div([              
        html.P(' Voltage in Volt (range: 10-14V),   Temperature in C° (range: 0-60C)', 
              style={'font-size': '14','padding-top' : '20'}), 
        html.P(' Measurements: Mean Ø | Current Value', 
              style={'font-size': '12','padding-top' : '0','margin-top' : '0'}), 
        ],className="d-flex align-items-center flex-column justify-content-center text-secondary", style={}),
                                       
                 ], className="card-body ", style={}),
		],className="card ", style={	
        }),
		], className="col-lg-5 col-xs-12 ", style={
        }),
		########## battery pack 2 ##########
		html.Div([
		html.Div([
		          html.H4(" Battery Pack 2")
		          ], className="card-header text-center text-white mb2",style={
                'backgroundColor': colors['head'],'padding-top' : '15','padding-bottom' : '8', },),
        html.Div([
        html.Div([
        
        html.Div([
        html.Div([
            dcc.Graph(id='g11',),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}), 
        
        html.Div([
         html.Div([
            dcc.Input(id='input-13', type='text',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '0','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),                
            dcc.Input(id='input-14', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-15', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-16', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        html.Hr(),
        html.Div([
        html.Div([
            dcc.Graph(id='g12',),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        
        html.Div([
        html.Div([
            dcc.Input(id='input-17', type='text',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '0','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),                
            dcc.Input(id='input-18', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-19', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-20', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        html.Hr(),
        html.Div([
          html.Div([
            dcc.Graph(id='g13',),
        ],className="row", style={}),  
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        
        html.Div([
        html.Div([
            dcc.Input(id='input-21', type='text',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '0','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),                
            dcc.Input(id='input-22', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-23', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-24', type='text', value='',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row", style={}), 
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        
        html.Div([              
        html.P(' Voltage in Volt (range: 10-14V),   Temperature in C° (range: 0-60C)', 
              style={'font-size': '14','padding-top' : '20'}), 
        html.P(' Measurements: Mean Ø | Current Value', 
              style={'font-size': '12','padding-top' : '0','margin-top' : '0'}), 
        ],className="d-flex align-items-center flex-column justify-content-center  text-secondary", style={}),
       
                 
        ], className="card-body"),
		], className="card"),
		], className="col-lg-5 col-xs-12"),
              
		], className="row", style={
        }),
				
], className="container-fluid", style={
            'margin-top': '10',
            'padding' : '10',
        }),	
		
], className="container-fluid", style={
            'margin': '0',
            'padding' : '0',
})

				
@app.callback(
    Output(component_id='input-01', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():
	mean_val = mean(a1_V_list[3])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_V_list[3][0])
	       
@app.callback(
    Output(component_id='input-02', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a1_T_list[3])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_T_list[3][0])
    
@app.callback(
    Output(component_id='input-03', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a1_V_list[0])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_V_list[0][0])
    
@app.callback(
    Output(component_id='input-04', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a1_T_list[0])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_T_list[0][0])

@app.callback(
    Output(component_id='input-05', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a1_V_list[4])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_V_list[4][0])

@app.callback(
    Output(component_id='input-06', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a1_T_list[4])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_T_list[4][0])
    
@app.callback(
    Output(component_id='input-07', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a1_V_list[1])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_V_list[1][0])
    
@app.callback(
    Output(component_id='input-08', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a1_T_list[1])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_T_list[1][0])

@app.callback(
    Output(component_id='input-09', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a1_V_list[5])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_V_list[5][0])

@app.callback(
    Output(component_id='input-10', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a1_T_list[5])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_T_list[5][0])
    
@app.callback(
    Output(component_id='input-11', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a1_V_list[2])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_V_list[2][0])
    
@app.callback(
    Output(component_id='input-12', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a1_T_list[2])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a1_T_list[2][0])

@app.callback(
    Output(component_id='input-13', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_V_list[3])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_V_list[3][0])

@app.callback(
    Output(component_id='input-14', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_T_list[3])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_T_list[3][0])
    
@app.callback(
    Output(component_id='input-15', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_V_list[0])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_V_list[0][0])
    
@app.callback(
    Output(component_id='input-16', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_T_list[0])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_T_list[0][0])

@app.callback(
    Output(component_id='input-17', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_V_list[4])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_V_list[4][0])

@app.callback(
    Output(component_id='input-18', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_T_list[4])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_T_list[4][0])
    
@app.callback(
    Output(component_id='input-19', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_V_list[1])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_V_list[1][0])
    
@app.callback(
    Output(component_id='input-20', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_T_list[1])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_T_list[1][0])

@app.callback(
    Output(component_id='input-21', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_V_list[5])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_V_list[5][0])

@app.callback(
    Output(component_id='input-22', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_T_list[5])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_T_list[5][0])
    
@app.callback(
    Output(component_id='input-23', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_V_list[2])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_V_list[2][0])
    
@app.callback(
    Output(component_id='input-24', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
	mean_val = mean(a2_T_list[2])	
	return 'Ø ' + "{:.1f}".format(mean_val) + ' | '\
	       "{:.1f}".format(a2_T_list[2][0])
    

@app.callback(Output('g01', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_bar():  
	X = np.arange(0,-20,-1)
	# set colors
	c_1 = compare_volt(a1_V_list[3][0])
	c_2 = compare_temp(a1_T_list[3][0])
	c_3 = compare_volt(a1_V_list[0][0])
	c_4 = compare_temp(a1_T_list[0][0])
	trace1 = go.Bar(x=list(X), y= list(a1_V_list[3]),marker=dict(color= c_1), width=1.0,showlegend=False,) #3888ba
	trace2 = go.Bar(x=list(X), y= list(a1_T_list[3]),marker=dict(color= c_2), width=1.0,showlegend=False,) #38ba72
	trace3 = go.Bar(x=list(X), y= list(a1_V_list[0]),marker=dict(color= c_3), width=1.0,showlegend=False,)
	trace4 = go.Bar(x=list(X), y= list(a1_T_list[0]),marker=dict(color= c_4), width=1.0,showlegend=False,)	
	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 4', 'Temperature 4',
	                                                          'Voltage 1', 'Temperature 1'), 
	                                                          print_grid=False)	
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
	fig['layout']['yaxis1'].update(range=[10, 14])
	fig['layout']['yaxis2'].update(range=[0, 60])
	fig['layout']['yaxis3'].update(range=[10, 14])
	fig['layout']['yaxis4'].update(range=[0, 60])
	fig['layout'].update(xaxis1=dict(showticklabels=False),
	                     yaxis1=dict(showticklabels=False),
	                     xaxis2=dict(showticklabels=False),
	                     yaxis2=dict(showticklabels=False),
	                     xaxis3=dict(showticklabels=False),
	                     yaxis3=dict(showticklabels=False),
	                     xaxis4=dict(showticklabels=False),
	                     yaxis4=dict(showticklabels=False),)
	fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40))
	fig['layout'].update(height=150, width=700)
	return fig   

@app.callback(Output('g02', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_bar():
	X = np.arange(0,-20,-1)
	# set colors
	c_1 = compare_volt(a1_V_list[4][0])
	c_2 = compare_temp(a1_T_list[4][0])
	c_3 = compare_volt(a1_V_list[1][0])
	c_4 = compare_temp(a1_T_list[1][0])
	trace1 = go.Bar(x=list(X), y=list(a1_V_list[4]),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace2 = go.Bar(x=list(X), y=list(a1_T_list[4]),marker=dict(color= c_2), width=1.0,showlegend=False)
	trace3 = go.Bar(x=list(X), y=list(a1_V_list[1]),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace4 = go.Bar(x=list(X), y=list(a1_T_list[1]),marker=dict(color= c_2), width=1.0,showlegend=False)
	
	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 5', 'Temperature 5',
	                                                          'Voltage 2', 'Temperature 2'), 
	                                                          print_grid=False)
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
	fig['layout']['yaxis1'].update(range=[10, 14])
	fig['layout']['yaxis2'].update(range=[0, 60])
	fig['layout']['yaxis3'].update(range=[10, 14])
	fig['layout']['yaxis4'].update(range=[0, 60])
	fig['layout'].update(xaxis1=dict(showticklabels=False),
	                     yaxis1=dict(showticklabels=False),
	                     xaxis2=dict(showticklabels=False),
	                     yaxis2=dict(showticklabels=False),
	                     xaxis3=dict(showticklabels=False),
	                     yaxis3=dict(showticklabels=False),
	                     xaxis4=dict(showticklabels=False),
	                     yaxis4=dict(showticklabels=False),)
	fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40))
	fig['layout'].update(height=150, width=700,)
	return fig   

@app.callback(Output('g03', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_bar():
	X = np.arange(0,-20,-1)
	# set colors
	c_1 = compare_volt(a1_V_list[5][0])
	c_2 = compare_temp(a1_T_list[5][0])
	c_3 = compare_volt(a1_V_list[2][0])
	c_4 = compare_temp(a1_T_list[2][0])
	trace1 = go.Bar(x=list(X), y=list(a1_V_list[5]),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace2 = go.Bar(x=list(X), y=list(a1_T_list[5]),marker=dict(color= c_2), width=1.0,showlegend=False)
	trace3 = go.Bar(x=list(X), y=list(a1_V_list[2]),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace4 = go.Bar(x=list(X), y=list(a1_T_list[2]),marker=dict(color= c_2), width=1.0,showlegend=False)
	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 6', 'Temperature 6',
	                                                          'Voltage 3', 'Temperature 3'), 
	                                                          print_grid=False)
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
	fig['layout']['yaxis1'].update(range=[10, 14])
	fig['layout']['yaxis2'].update(range=[0, 60])
	fig['layout']['yaxis3'].update(range=[10, 14])
	fig['layout']['yaxis4'].update(range=[0, 60])
	fig['layout'].update(xaxis1=dict(showticklabels=False),
	                     yaxis1=dict(showticklabels=False),
	                     xaxis2=dict(showticklabels=False),
	                     yaxis2=dict(showticklabels=False),
	                     xaxis3=dict(showticklabels=False),
	                     yaxis3=dict(showticklabels=False),
	                     xaxis4=dict(showticklabels=False),
	                     yaxis4=dict(showticklabels=False),)
	fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40))
	fig['layout'].update(height=150, width=700,)
	return fig    

@app.callback(Output('g11', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_bar():
	X = np.arange(0,-20,-1)
	# set colors
	c_1 = compare_volt(a2_V_list[3][0])
	c_2 = compare_temp(a2_T_list[3][0])
	c_3 = compare_volt(a2_V_list[0][0])
	c_4 = compare_temp(a2_T_list[0][0])
	trace1 = go.Bar(x=list(X), y=list(a2_V_list[3]),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace2 = go.Bar(x=list(X), y=list(a2_T_list[3]),marker=dict(color= c_2), width=1.0,showlegend=False)
	trace3 = go.Bar(x=list(X), y=list(a2_V_list[0]),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace4 = go.Bar(x=list(X), y=list(a2_T_list[0]),marker=dict(color= c_2), width=1.0,showlegend=False)
	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 4', 'Temperature 4',
	                                                          'Voltage 1', 'Temperature 1'),
	                                                           print_grid=False)
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
	fig['layout']['yaxis1'].update(range=[10, 14])
	fig['layout']['yaxis2'].update(range=[0, 60])
	fig['layout']['yaxis3'].update(range=[10, 14])
	fig['layout']['yaxis4'].update(range=[0, 60])
	fig['layout'].update(xaxis1=dict(showticklabels=False),
	                     yaxis1=dict(showticklabels=False),
	                     xaxis2=dict(showticklabels=False),
	                     yaxis2=dict(showticklabels=False),
	                     xaxis3=dict(showticklabels=False),
	                     yaxis3=dict(showticklabels=False),
	                     xaxis4=dict(showticklabels=False),
	                     yaxis4=dict(showticklabels=False),)
	fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40))
	fig['layout'].update(height=150, width=700)
	return fig  

@app.callback(Output('g12', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_bar():
	X = np.arange(0,-20,-1)
	# set colors
	c_1 = compare_volt(a2_V_list[4][0])
	c_2 = compare_temp(a2_T_list[4][0])
	c_3 = compare_volt(a2_V_list[1][0])
	c_4 = compare_temp(a2_T_list[1][0])
	trace1 = go.Bar(x=list(X), y=list(a2_V_list[4]),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace2 = go.Bar(x=list(X), y=list(a2_T_list[4]),marker=dict(color= c_2), width=1.0,showlegend=False)
	trace3 = go.Bar(x=list(X), y=list(a2_V_list[1]),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace4 = go.Bar(x=list(X), y=list(a2_T_list[1]),marker=dict(color= c_2), width=1.0,showlegend=False)
	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 5', 'Temperature 5',
	                                                          'Voltage 2', 'Temperature 2'),
	                                                           print_grid=False)
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
	fig['layout']['yaxis1'].update(range=[10, 14])
	fig['layout']['yaxis2'].update(range=[0, 60])
	fig['layout']['yaxis3'].update(range=[10, 14])
	fig['layout']['yaxis4'].update(range=[0, 60])
	fig['layout'].update(xaxis1=dict(showticklabels=False),
	                     yaxis1=dict(showticklabels=False),
	                     xaxis2=dict(showticklabels=False),
	                     yaxis2=dict(showticklabels=False),
	                     xaxis3=dict(showticklabels=False),
	                     yaxis3=dict(showticklabels=False),
	                     xaxis4=dict(showticklabels=False),
	                     yaxis4=dict(showticklabels=False),)
	fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40))
	fig['layout'].update(height=150, width=700,)
	return fig  

@app.callback(Output('g13', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_bar():
	X = np.arange(0,-20,-1)
	# set colors
	c_1 = compare_volt(a2_V_list[5][0])
	c_2 = compare_temp(a2_T_list[5][0])
	c_3 = compare_volt(a2_V_list[2][0])
	c_4 = compare_temp(a2_T_list[2][0])
	trace1 = go.Bar(x=list(X), y=list(a2_V_list[5]),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace2 = go.Bar(x=list(X), y=list(a2_T_list[5]),marker=dict(color= c_2), width=1.0,showlegend=False)
	trace3 = go.Bar(x=list(X), y=list(a2_V_list[2]),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace4 = go.Bar(x=list(X), y=list(a2_T_list[2]),marker=dict(color= c_2), width=1.0,showlegend=False)
	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 6','Temperature 6',
	                                                          'Voltage 3', 'Temperature 3'),
	                                                          print_grid=False)
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
	fig['layout']['yaxis1'].update(range=[10, 14])
	fig['layout']['yaxis2'].update(range=[0, 60])
	fig['layout']['yaxis3'].update(range=[10, 14])
	fig['layout']['yaxis4'].update(range=[0, 60])
	fig['layout'].update(xaxis1=dict(showticklabels=False),
	                     yaxis1=dict(showticklabels=False),
	                     xaxis2=dict(showticklabels=False),
	                     yaxis2=dict(showticklabels=False),
	                     xaxis3=dict(showticklabels=False),
	                     yaxis3=dict(showticklabels=False),
	                     xaxis4=dict(showticklabels=False),
	                     yaxis4=dict(showticklabels=False),)
	fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40))
	fig['layout'].update(height=150, width=700,)
	return fig
				
external_css = ["https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})   
external_js = ["https://code.jquery.com/jquery-3.3.1.slim.min.js",
               "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js",
               "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"]
for js in external_js:
    app.scripts.append_script({"external_url": js})

##################################
# Helper Functions
##################################

def mean(numbers):
	''' calculate mean '''
	return float(sum(numbers)) / max(len(numbers), 1)
	
def compare_volt(value):
	''' compare voltages and return color'''
	low_thres = 10
	high_thres = 14
	if value < low_thres or value > high_thres:
		color = 'rgb(255,0,0, 0.8)' # warning mode rot
	else:
		color = 'rgb(49,130,189, 0.8)' # normal mode blau
	return color

def compare_temp(value):
	''' compare temperatures and return color'''
	low_thres = 0
	high_thres = 60
	if value < low_thres or value > high_thres:
		color = 'rgb(255,0,0, 0.8)' # warning mode rot
	else:
		color = 'rgb(0,128,0,0.8)'# normal mode gruen
	return color	

##################################
# CAN Data Functions
##################################

def init_can():
	''' Bring up the CAN interface '''
	# Close can0 if still open
	os.system("sudo /sbin/ip link set can0 down")
	# Bring up can0 interface at 500kbps
	os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
	time.sleep(0.01)	
	# Connect to can0 interface 
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native') 
	print('connected to can0 interface')
	print('ready to send/receive can messages')
	return bus

def can_msg_rv():
	''' Put CAN messages into buffer '''
	while True:
		msg = bus.recv()
		q.put(msg)

def filter_buffer(byte_list, msg_id):
	''' a filter for CAN messages to sort into various buffers '''
	byte2 = byte_list[1] + byte_list[2]
	# convert from hex to dec
	val_dec = int(byte2, 16) / 100
	# filter into buffer (temperature and voltages)
	for pos2 in range(1,num_sens+1):
		for pos3 in range(1,cells+1):
			if byte_list[0] == str(pos2) + str(pos3):
				# sort for ID: 600 (Accu 1)
				if msg_id == 600:
					# sort for temperatures
					if pos2 == 1:
						a1_T_list[pos3-1].appendleft(val_dec)
					# sort for voltages
					if pos2 == 2:
						a1_V_list[pos3-1].appendleft(val_dec)		
				# sort for ID: 602 (Accu 2)
				if msg_id == 601:
					# sort for temperatures
					if pos2 == 1:
						a2_T_list[pos3-1].appendleft(val_dec)
					# sort for voltages
					if pos2 == 2:
						a2_V_list[pos3-1].appendleft(val_dec)
	
def can_data_loop():
	''' pull data from buffer and put it into deques'''
	while True:
		if q.empty() != True:
			msg = q.get()
			if msg != None:
				len_msg = len(msg.data)
			    # 1536= ID 600, 1537= ID 601 (Error Akku1), 
				msg_id = int('{0:x} '.format(msg.arbitration_id))
				# check correct msg length	
				if len_msg == 3:
					byte_list = [] # init empty bytestring
					for pos in range(len_msg-1,-1,-1):
						byte = '{0:x}'.format(msg.data[pos])
						if len(byte) == 1:
							byte = '0' + byte
						byte_list.append(byte)
					filter_buffer(byte_list, msg_id)

def run_dash_app():
	''' run dash app in a thread '''
	IP = '192.168.200.171' # pi hermans 192.168.200.171:9999
	app.run_server(debug=False,use_reloader=False, host=IP,port= 9999)
	
### Insert here your IP-Address on your Raspberry PI !! ###
# for example: '192.168.200.1' 
# and access the app your browser by entering: 192.168.200.1:9999
IP = '192.168.200.1' # 
if __name__ == '__main__':
	# Bring up the can0 Interface
	bus = init_can()
	# Start Threading 
	t1 = threading.Thread(target=can_msg_rv)
	t2 = threading.Thread(target=can_data_loop)
	t3 = threading.Thread(target=run_dash_app)
	t1.start()
	t2.start()
	t3.start()
	# for debugging (deactivate thread 3)
	#app.run_server(debug=True, host=IP,port= 9999)
	
	
