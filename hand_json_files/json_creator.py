# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html

external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# markdown_text = '''
# ### Dash and Markdown

# Dash apps can be written in Markdown.
# Dash uses the [CommonMark](http://commonmark.org/)
# specification of Markdown.
# Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
# if this is your first introduction to Markdown!
# '''

# app.layout = html.Div([
#     dcc.Markdown(children=markdown_text)
# ])

fingers = [1,2,3,4]
active_finger = 0
active_joint = 0
joints = [1,2,3]
figner_orientation = 20
finger_dictionary = {'finger0':{'radius':0, 'angle': 0, 'orientation':0, 'number_segment':1}}

hand_name = ''
palm_dimensions = {'width':0, 'height':0, 'thickness':0}

palm_setup = dbc.Card(
    [
        html.Div([
            dbc.Label("Enter the name of the hand: (use _ instead of a spaces)"),
            dbc.Input(id="hand name", type="text"),
        ]),
        html.Div([
            dbc.Label(''),
            dbc.InputGroup([
            dbc.InputGroupText("Palm Style:"),
            dbc.Select(options=[{"label": "Cuboid", "value": "cuboid"}, 
            {"label": "Cylindrical", "value": "cylinder"},
            {"label": "None", "value": "None"}] )
            ]),
        ]),
        html.Div([
            dbc.Label("Palm Dimensions (in meters):"),
            dbc.InputGroup([
                dbc.InputGroupText("Width: "),
                dbc.Input(id="palm width", type="number", value=0)
            ]),
            dbc.InputGroup([
                dbc.InputGroupText("Height: "),
                dbc.Input(id="palm height", type="number", value=0)
            ]),
            dbc.InputGroup([
                dbc.InputGroupText("Thickness: "),
                dbc.Input(id="palm thickness", type="number", value=0)
            ])
        ]),
        html.Div([
            dbc.Label(''),
            dbc.InputGroup([
                dbc.InputGroupText("Number of Fingers"),
                dbc.Input(id="number of fingers", type="number", value=1)
            ])
        ]),
        html.Div([
            dbc.Label(''),
            dbc.InputGroup([
                dbc.InputGroupText('Select Finger:'),
                dbc.Select(id='active finger', options=[
                    {'label': 'finger 0', 'value': 0}
                ], value= 0)
            ]),
            dbc.Label("Finger Location On Palm:"),
            dbc.InputGroup([
                dbc.InputGroupText('Radius (meters): '),
                dbc.Input(id='finger radius', type='number', value = 0)
            ]),
            dbc.InputGroup([
                dbc.InputGroupText("Angle (degrees): "),
                dbc.Input(id='finger angle', type='number', value = 0)
            ]),
            dbc.InputGroup([
                dbc.InputGroupText("Orientation (degrees): "),
                dbc.Input(id='finger orientation', type='number', value=0)
            ])
        ])

    ], body=True)

finger_setup = dbc.Card(
    [
        html.Div([
            dbc.InputGroup([
                dbc.InputGroupText('Select Finger: '),
                dbc.Select(id='active finger2', options=[
                    {'label': 'finger 0', 'value': 0}
                ], value= 0)
            ]),
            dbc.InputGroup([
                dbc.InputGroupText('Number of Segments: '),
                dbc.Input(id='number of segments', type='number')
            ])
        ]),
        html.Div([
            dbc.Label(' '),
            dbc.InputGroup([
                dbc.InputGroupText('Select Joint: '),
                dbc.Select(id=f'{active_joint}', options=[
                    {'label': f'Joint {joint}', 'value': joint} for joint in joints
                ])
            ]),
            dbc.InputGroup([
                dbc.InputGroupText('Joint Style'),
                dbc.Select(id='active joint', options=[
                    {'label': 'pin joint', 'value': 'pin'}
                ])
            ])
        ])
    ]
)

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Generate a json for the Hand Generator", style={'textAlign':'center'}))
        ]),
        dbc.Row([
            dbc.Col([html.Div('image 1', id="image1"), html.Div('image 3?')], md=4),
            dbc.Col([html.Div('image 2', id="image2"), html.Div('image 4?')], md=4),
            dbc.Col(palm_setup, md=4,  )
        ]),
        dbc.Row([dbc.Col([dbc.Label(' ')])]),
        dbc.Row([
            dbc.Col(html.Div("Image 3", id="image3"), md=4),
            dbc.Col(html.Div("Image 4", id="image4"), md=4),
            dbc.Col(finger_setup, md=4)
        ])
    ])

])

@app.callback(
    Output('active finger', 'options'),
    Output('active finger2', 'options'),
    Input('number of fingers', 'value')
)
def update_number_fingers(input_value):
    global finger_dictionary
    finger_list = []
    for finger in range(input_value):
        finger_dictionary[f'finger{finger}'] = {'radius': 0, 'angle': 0, 'orientation': 0, 'number_segment':1}
        finger_list.append({"label": f'Finger {finger}', "value": finger})
    
    return finger_list, finger_list


@app.callback(
    Output('image1', 'children'),
    Input('finger radius', 'value'),
    Input('finger angle', 'value'),
    Input('finger orientation', 'value')
)
def update_finger_values(finger_radius, finger_angle, finger_orientation):
    global finger_dictionary, active_finger
    finger_dictionary[f'finger{active_finger}']['radius'] = finger_radius
    finger_dictionary[f'finger{active_finger}']['angle'] = finger_angle
    finger_dictionary[f'finger{active_finger}']['orientation'] = finger_orientation
    
@app.callback(
    Output('image2', 'children'),
    Input('palm width', 'value'),
    Input('palm height', 'value'),
    Input('palm thickness', 'value')
)
def update_palm_dimensions(width, height, thickness):
    global palm_dimensions
    palm_dimensions['width'] = width
    palm_dimensions['height'] = height
    palm_dimensions['thivkness'] = thickness

@app.callback(
    Output('image3', 'children'),
    Input('hand name', 'value')
)
def update_hand_name(name):
    global hand_name
    hand_name = name


@app.callback(
    Output('finger orientation', 'value'),
    Output('finger radius', 'value'),
    Output('finger angle', 'value'),
    # Output('').
    Input('active finger', 'value')
)
def update_displayed_values_for_finger(input_value):
    global finger_dictionary, active_finger
    active_finger = input_value
    return finger_dictionary[f'finger{input_value}']['orientation'], finger_dictionary[f'finger{input_value}']['radius'], finger_dictionary[f'finger{input_value}']['angle']


@app.callback(
    Output('active finger2', 'value'),
    Output('active finger', 'value'),
    Input('active finger', 'value'),
    Input('active finger2', 'value')
)
def update_finger2(active_finger1, active_finger2):
    global active_finger
    if active_finger1 != active_finger:
        active_finger = active_finger1
    else:
        active_finger = active_finger2

    # ctx = dash.callback_context
    # ctx.triggered[0]["prop_id"].split(".")[0]
    return active_finger, active_finger


if __name__ == '__main__':
    app.run_server(debug=True)
