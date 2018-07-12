#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Browser based Web App
Purpose: Battery Monitoring Demo
Version: 4/2018 Roboball (MattK.)
"""
import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import base64
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from collections import deque
import numpy as np
import random

########## globals ##########

# queque for Y Values 
Y = deque(maxlen=20)
Y.appendleft(1) 
for pos in range(19):
	Y.appendleft(0) 	
colors = {
    'background': '#424242',
    'text': '#7FDBFF',
    'head': '#7996c4',
    'c1': '#e5eefd',    
}
# layouts
text_style_1 = dict(color='#444', textAlign = 'left', fontFamily='sans-serif', fontWeight=300) 
text_style_2 = dict(color='#444', textAlign = 'center', fontFamily='sans-serif', fontWeight=600)
div_style_01 = {'backgroundColor': colors['background'], 'color': colors['text'],
                'marginTop': 0, 'marginLeft': 0, 'marginRight': 0}

app = dash.Dash(__name__)

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
                'backgroundColor': colors['background'],},),			
		html.Div([
		html.Div([	
		########## battery control ##########
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
            dcc.Interval(id='graph-update', interval= 1000 * 1),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        
        html.Div([
         html.Div([
            dcc.Input(id='input-01', type='text',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '0','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),                 
            dcc.Input(id='input-02', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-03', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-04', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row ", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        
        
        html.Div([
        html.Div([
            dcc.Graph(id='g02',),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        
        html.Div([   
        html.Div([
            dcc.Input(id='input-05', type='text',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '0','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),                
            dcc.Input(id='input-06', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-07', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-08', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}), 
        
        html.Div([
        html.Div([
            dcc.Graph(id='g03',),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        
        html.Div([
           html.Div([
            dcc.Input(id='input-09', type='text',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '0','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),                
            dcc.Input(id='input-10', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-11', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-12', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row", style={}), 
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),              
                                     
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
            dcc.Input(id='input-14', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-15', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-16', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        
        html.Div([
        html.Div([
            dcc.Graph(id='g12',),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center", style={}),
        
        html.Div([
        html.Div([
            dcc.Input(id='input-17', type='text',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '0','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),                
            dcc.Input(id='input-18', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-19', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-20', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row", style={}),
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
        
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
            dcc.Input(id='input-22', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-23', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
            dcc.Input(id='input-24', type='text', value='50',className="form-control form-control-lg ", style={	
                             'text-align':'center','font-size': '20', 'width': '150', 'display': 'inline-block',
                              'margin-left' : '34','margin-right' : '0','padding-left' : '0','padding-right' : '0',}),
        ],className="row", style={}), 
        ],className="d-flex align-items-center flex-column justify-content-center ", style={}),
                   
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

########## callbacks ##########
@app.callback(
    Output(component_id='input-01', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])

@app.callback(
    Output(component_id='input-02', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-03', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-04', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])

@app.callback(
    Output(component_id='input-05', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])

@app.callback(
    Output(component_id='input-06', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-07', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-08', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])

@app.callback(
    Output(component_id='input-09', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])

@app.callback(
    Output(component_id='input-10', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-11', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-12', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])

@app.callback(
    Output(component_id='input-13', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])

@app.callback(
    Output(component_id='input-14', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-15', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-16', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])

@app.callback(
    Output(component_id='input-17', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])

@app.callback(
    Output(component_id='input-18', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-19', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-20', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])

@app.callback(
    Output(component_id='input-21', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])

@app.callback(
    Output(component_id='input-22', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-23', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    
@app.callback(
    Output(component_id='input-24', component_property='value'),
           events=[Event('graph-update', 'interval')])
def update_output_div():	
    return "{:.3f}".format(Y[-1])
    

@app.callback(Output('g01', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_bar():
	
	#X.append(X[-1]+1)
	val = 1+1*random.uniform(-0.1,0.1)
	X = np.arange(0,-20,-1)
	Y.appendleft(val)
	if val < 0.95:
		c_1 = 'rgb(255,0,0, 0.8)' # warning mode
		c_2 = 'rgb(255,0,0, 0.8)' # warning mode
	else:
		c_1 = 'rgb(49,130,189, 0.8)' # normal mode
		c_2 = 'rgb(0,128,0,0.8)'     # normal mode
		
	trace1 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False,) #3888ba
	trace2 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False,) #38ba72
	trace3 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False,)
	trace4 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False,)
	
	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 4', 'Temperature 4',
	                                                          'Voltage 1', 'Temperature 1'))
	
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
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
	
	#X.append(X[-1]+1)
	val = 1+1*random.uniform(-0.1,0.1)
	X = np.arange(0,-20,-1)
	Y.appendleft(val)
	if val < 0.95:
		c_1 = 'rgb(255,0,0, 0.8)' # warning mode
		c_2 = 'rgb(255,0,0, 0.8)' # warning mode
	else:
		c_1 = 'rgb(49,130,189, 0.8)' # normal mode
		c_2 = 'rgb(0,128,0,0.8)'     # normal mode
	
	trace1 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace2 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False)
	trace3 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace4 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False)
	
	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 5', 'Temperature 5',
	                                                          'Voltage 2', 'Temperature 2'))
	
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
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
	
	#X.append(X[-1]+1)
	val = 1+1*random.uniform(-0.1,0.1)
	X = np.arange(0,-20,-1)
	Y.appendleft(val)
	if val < 0.95:
		c_1 = 'rgb(255,0,0, 0.8)' # warning mode
		c_2 = 'rgb(255,0,0, 0.8)' # warning mode
	else:
		c_1 = 'rgb(49,130,189, 0.8)' # normal mode
		c_2 = 'rgb(0,128,0,0.8)'     # normal mode
	#Red  'rgba(222,45,38,0.8)'
	trace1 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace2 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False)
	trace3 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace4 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False)
	
	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 6', 'Temperature 6',
	                                                          'Voltage 3', 'Temperature 3'),)
	
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
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
	
	#X.append(X[-1]+1)
	val = 1+1*random.uniform(-0.1,0.1)
	X = np.arange(0,-20,-1)
	Y.appendleft(val)
	if val < 0.95:
		c_1 = 'rgb(255,0,0, 0.8)' # warning mode
		c_2 = 'rgb(255,0,0, 0.8)' # warning mode
	else:
		c_1 = 'rgb(49,130,189, 0.8)' # normal mode
		c_2 = 'rgb(0,128,0,0.8)'     # normal mode
	
	trace1 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace2 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False)
	trace3 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace4 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False)

	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 4', 'Temperature 4',
	                                                          'Voltage 1', 'Temperature 1'),)
	
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
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
	
	#X.append(X[-1]+1)
	val = 1+1*random.uniform(-0.1,0.1)
	X = np.arange(0,-20,-1)
	Y.appendleft(val)
	if val < 0.95:
		c_1 = 'rgb(255,0,0, 0.8)' # warning mode
		c_2 = 'rgb(255,0,0, 0.8)' # warning mode
	else:
		c_1 = 'rgb(49,130,189, 0.8)' # normal mode
		c_2 = 'rgb(0,128,0,0.8)'     # normal mode
	
	trace1 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace2 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False)
	trace3 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace4 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False)
	
	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 5', 'Temperature 5',
	                                                          'Voltage 2', 'Temperature 2'),)
	
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
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
	
	#X.append(X[-1]+1)
	val = 1+1*random.uniform(-0.1,0.1)
	X = np.arange(0,-20,-1)
	Y.appendleft(val)
	if val < 0.95:
		c_1 = 'rgb(255,0,0, 0.8)' # warning mode
		c_2 = 'rgb(255,0,0, 0.8)' # warning mode
	else:
		c_1 = 'rgb(49,130,189, 0.8)' # normal mode
		c_2 = 'rgb(0,128,0,0.8)'     # normal mode
	
	trace1 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace2 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False)
	trace3 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_1), width=1.0,showlegend=False)
	trace4 = go.Bar(x=list(X), y=list(Y),marker=dict(color= c_2), width=1.0,showlegend=False)
		
	fig = tools.make_subplots(rows=1, cols=4, subplot_titles=('Voltage 6', 'Temperature 6',
	                                                          'Voltage 3', 'Temperature 3'),)
	
	fig.append_trace(trace1, 1, 1)
	fig.append_trace(trace2, 1, 2)
	fig.append_trace(trace3, 1, 3)
	fig.append_trace(trace4, 1, 4)
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

### external css stylesheets and js scripts ###
external_css = ["https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})
    
external_js = ["https://code.jquery.com/jquery-3.3.1.slim.min.js",
               "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js",
               "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"]              
for js in external_js:
    app.scripts.append_script({"external_url": js})



if __name__ == '__main__':
	# set your IP here:
	IP = '192.168.2.100'
	app.run_server(debug=False, host=IP,port= 9999)



