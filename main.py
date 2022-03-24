import plotly.express as px
import plotly.graph_objects as go
import base64
import numpy as np
import json
from skimage import io, color, segmentation, img_as_ubyte, filters, measure
from PIL import Image

from dash_canvas import DashCanvas

import dash
from dash.dependencies import Input, Output
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

from skimage import data, exposure
from dash_canvas.utils.parse_json import parse_jsonstring
from dash_canvas.utils.io_utils import image_string_to_PILImage, array_to_data_url
from dash_canvas.utils.image_processing_utils import modify_segmentation

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

width, height, bands = 1024, 512, 3

# create input image the user draws on
in_img = np.ones((height, width, bands), dtype=np.uint8) * 255
in_fig = px.imshow(in_img, binary_string=True, width=width*.75, height=height*.75)
in_fig.update_layout(
    dragmode="drawopenpath",
    showlegend=False,
    hovermode=False,
    paper_bgcolor="LightSteelBlue",
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0
    ),
)
in_fig.update_xaxes(visible=False)
in_fig.update_yaxes(visible=False)


# PLACEHOLDER OUTPUT IMAGE
out_img = np.zeros((height, width, bands), dtype=np.uint8)
out_fig = px.imshow(out_img, binary_string=True, width=width*.75, height=height*.75)
out_fig.update_layout(
    dragmode=False,
    showlegend=False,
    hovermode=False,
    paper_bgcolor="Red",
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0
    ),
)
out_fig.update_xaxes(visible=False)
out_fig.update_yaxes(visible=False)

# ------------------ App definition ---------------------


def title():
    return 'Image From Doodle'


app.layout = html.Div([
    # title
    html.H1(title()),
    # horizontal container
    html.Div(
        children=[
            # canvas
            html.Div(
                [dcc.Graph(id='doodle', figure=in_fig, config={'displayModeBar': False}), ],
                style={"width": "50%", "display": "inline-block", "padding": "0 0 0 0"}
            ),
            # button to feed image through network
            # dbc.Button("Generate Image", id='gen_img', color='primary'),
            # output
            html.Div(
                [dcc.Graph(id='output', figure=out_fig, config={'displayModeBar': False}), ],
                style={"width": "50%", "display": "inline-block", "padding": "0 0 0 0"}
            )
        ],
        style={'width': 'inherit', 'display': 'inline-block',
               'paddingRight': '50px',
               'paddingLeft': '50px'

               }
    ),

    html.Div([
        html.H6(children=['Brush width']),
        dcc.Slider(
            id='width-slider', min=5, max=40, step=4, value=5
        ),
        daq.ColorPicker(
            id='color-picker', label='Brush color', value=dict(hex='#119DFF')
        ),
    ],
        className="three columns"
    ),
],
    style={'backgroundColor': 'lightgrey',
           'width': 'inherit',
           'height': 'inherit',
           'textAlign': 'center'}
)


# flat	road · sidewalk · parking+ · rail track+
# human	person* · rider*
# vehicle	car* · truck* · bus* · on rails* · motorcycle* · bicycle* · caravan*+ · trailer*+
# construction	building · wall · fence · guard rail+ · bridge+ · tunnel+
# object	pole · pole group+ · traffic sign · traffic light
# nature	vegetation · terrain
# sky	sky
# void	ground+ · dynamic+ · static+

@app.callback(
    Output("doodle", "figure"),
    Input("width-slider", "value"),
    Input("color-picker", "value"),
    Input("doodle", "figure"),
    prevent_initial_call=True,
)
def on_style_change(slider_value, color_value, fig):
    from pprint import pprint
    print('----====='*20)
    print(parse_jsonstring(fig))
    fig['layout']['newshapes'] = dict(line=dict(color=color_value["hex"], width=slider_value))
    # pprint(fig['layout']['template'].keys())
    # pprint(fig['layout']['template']['layout'].keys())
    # pprint(fig['layout']['template']['layout']['shapedefaults']['line'])
    # print(color_value)
    print('-------'*20)
    # fig['layout']['template']['layout']['shapedefaults']['line']['color'] = color_value['hex']
    # if 'shapes' in fig['layout']:
    #     for i in range(len(fig['layout']['shapes'])):
    #         print(fig['layout']['shapes'][i]['line'][''])
    # pprint(fig['layout']['template']['layout']['shapedefaults']['line'])
    print(dir(fig))
        # fig['layout']['shapes'][i]['line']['color'] = color_value
    # print(base64.b64decode(fig.source)
    # print(dir(in_fig))
    # print(in_fig.for_each_annotation('tmp2.png'))
    # in_fig.write_image('tmp.png')
    # io.imsave('',)
    # fig = px.imshow(img)
    # fig.update_layout(
    #     dragmode="drawopenpath",
    #     showlegend=False,
    #     newshape=dict(line=dict(color=color_value["hex"], width=slider_value)),
    # )
    # fig.update_annotations(
    #     fillcolor=color_value["hex"],
    #     width=slider_value
    # )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
