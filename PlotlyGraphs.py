import pandas as pd
import plotly.express as px
import plotly.graph_objects
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Import and clean data

# Kansas Cleaning

df1 = pd.read_csv("KansasTemps.csv", header=12)
# df = df[12:]
# print(df1[0:5])
# print(df1.keys())
df1 = df1[["Date", "MaxTemperature", "MinTemperature"]]
df1["Temperature"] = pd.to_numeric(df1["MaxTemperature"].replace(" M", None)) + pd.to_numeric(df1["MinTemperature"].replace(" M", None))

df1["Temperature"] = df1["Temperature"] / 2
df1 = df1[["Date", "Temperature"]]
df1["Date"] = pd.to_datetime(df1["Date"])
df1 = df1[pd.DatetimeIndex(df1["Date"]).year <= 2015]
df1 = df1[pd.DatetimeIndex(df1["Date"]).year >= 2008]

# print(df1[0:5])

# Loveland Cleaning

df2 = pd.read_csv("LovelandTemps.csv")
# print(df2["MaxTemp"][0:5], df2["MinTemp"][0:5])
df2["Temperature"] = df2["MaxTemp"].replace("M", None) + pd.to_numeric(df2["MinTemp"].replace("M", None))

df2["Temperature"] = df2["Temperature"] / 2
df2 = df2[["Date", "Temperature"]]
df2["Date"] = pd.to_datetime(df2["Date"])

# print(df2[0:5])

# Fort Collins Cleaning

df3 = pd.read_csv("Temperatures.csv")
df3 = df3[['Date', 'Temperature', 'Time']]
df3["Date"] = pd.to_datetime(df3["Date"] + ' ' + df3["Time"])
df3 = df3.drop(columns=["Time"])
df3.reset_index(inplace=True)

# print(df3[:5])
# print(df3["Date"][5])
# print(type(df3["Date"][5]))

dfs = {1: df1, 2: df2, 3: df3}
# App Layout
colorscales = px.colors.named_colorscales()

app.layout = html.Div([

    html.H1("Fort Collins Weather Data Analysis", style={'text-align': 'center'}),

    # dcc.Dropdown(id='slct_year',
    #              options=[
    #                  {"label": "2008", "value": 2008},
    #                  {"label": "2009", "value": 2009},
    #                  {"label": "2010", "value": 2010},
    #                  {"label": "2011", "value": 2011},
    #                  {"label": "2012", "value": 2012},
    #                  {"label": "2013", "value": 2013},
    #                  {"label": "2014", "value": 2014},
    #                  {"label": "2015", "value": 2015}],
    #              multi=False,
    #              value=2015,
    #              style={'width': "40%"}
    #              ),

    dcc.Dropdown(id='slct_color',
                 options=[{"value": x, "label": x}
                          for x in dfs],
                 value="Cividis",
                 multi=False,
                 style={'width': "40%"}
                 ),

    dcc.Dropdown(id='slct_data',
                 options=[{"value": 1, "label": "Kansas Location"},
                          {"value": 2, "label": "Loveland"},
                          {"value": 3, "label": "Fort Collins"},
                          ],
                 value=3,
                 multi=False,
                 style={'width': "40%"}
                 ),
    # html.Div(id='output_container1', children=[]),
    html.Br(),

    # dcc.Dropdown(id='slct_season',
    #              options=[
    #                  {"label": "Winter", "value": 0},
    #                  {"label": "Spring", "value": 1},
    #                  {"label": "Summer", "value": 2},
    #                  {"label": "Fall", "value": 3}],
    #              multi=False,
    #              value=0,
    #              style={'width': "40%"}
    #              ),
    #
    # html.Div(id='output_container2', children=[]),
    # html.Br(),

    dcc.Graph(id="Avg_Daily_Temps"),
    dcc.Graph(id="Monthly_Temp_Ranges"),
    dcc.Graph(id="Monthly_Avg_Temps"),
    dcc.Graph(id="Max_Min_Avg_Year_Temps"),

])


@app.callback(
    Output("Avg_Daily_Temps", "figure"),
    [Input(component_id='slct_color', component_property='value'),
     Input(component_id='slct_data', component_property='value')]
)
def update_line_chart(option_slctd, data_option):
    print("Inputs Test: ", option_slctd, data_option)
    dff = dfs[data_option].copy()
    dff["year"] = pd.DatetimeIndex(dff["Date"]).year

    dff["Date"] = dff["Date"].dt.strftime("0000-%m-%d")
    # print(dff)

    # Series
    ser = dff.groupby(["year", "Date"], as_index=True)["Temperature"].mean()
    # print(ser.index.get_level_values("year"))
    # print(ser.index.get_level_values("Date"))
    # print([i for i in ser])

    # dff = ser.unstack()
    # print(type(dff))

    # dff["Date"] = dff["Date"].dt.strftime("%m-%d %X")

    fig = go.Figure()

    fig.add_traces([go.Scatter(name=str(year), x=ser.index.get_level_values("Date"), y=ser[year],
                               mode="lines", line=dict(color='red'),
                               ) for year in ser.index.get_level_values("year").unique()])

    fig.update_traces(dict(opacity=0.8))

    fig.update_layout(legend_font_color="goldenrod", legend_bordercolor="red", title="Average Daily Temperatures")

    return fig


# @app.callback(
#     [Output(component_id='output_container1', component_property='children'),
#      Output(component_id='yearly_temperature_data', component_property='figure')],
#     [Input(component_id='slct_year', component_property='value')],
# )
# def update_graph(option_slctd):
#     print(option_slctd)
#     print(type(option_slctd))
#
#     container = f"Year Selected: {option_slctd}"
#
#     dff = df.copy()
#     dff = dff[pd.DatetimeIndex(dff["Date"]).year == option_slctd]
#
#     fig = go.Figure([go.Scatter(x=dff["Date"], y=dff["Temperature"])])
#
#     return container, fig


# @app.callback(
#     [Output(component_id='output_container2', component_property='children'),
#      Output(component_id='season_temperature_data', component_property='figure')],
#     [Input(component_id='slct_season', component_property='value')]
# )
# def update_graph(option_slctd):
#     print(option_slctd)
#     print(type(option_slctd))
#
#     dff = df.copy()
#     dff["year"] = pd.DatetimeIndex(dff["Date"]).year
#     dff["Date"] = dff["Date"].dt.strftime("%m-%d %X")
#     # print(dff[0:5])
#
#     dff = dff[pd.DatetimeIndex(dff["Date"]).month == months[option_slctd]]
#
#     mdf = dff.groupby("year").reset_index()
#     print("mdf: ")
#     print(mdf["years"])
#
#     # dff = dff[pd.DatetimeIndex(dff["Date"]).month == months[option_slctd]]
#     # fig = go.Figure([go.Scatter(x=grouped["Date"], y=grouped["Temperature"])])
#
#     # fig = go.Figure()
#     # for col in dff["years"]:
#     #     fig.add_trace(go.Scatter(x=dff["Date"],
#     #                              y=dff[col].values,
#     #                              name=col))
#     return container, fig


@app.callback(
    Output("Monthly_Temp_Ranges", "figure"),
    [Input("slct_color", "value"),
     Input(component_id='slct_data', component_property='value')]
)
def update_line_chart(option_slctd, data_option):
    print(option_slctd)

    dff = dfs[data_option].copy()
    dff["year"] = pd.DatetimeIndex(dff["Date"]).year
    dff["Date"] = dff["Date"].dt.strftime("0000-%m-00")
    # print("TEST dff: ")
    # print(dff[0:5])

    ser1 = (dff.groupby(["year", "Date"])["Temperature"].max() - dff.groupby(["year", "Date"])["Temperature"].min()).reset_index()

    ser1["Temperature"] = ser1["Temperature"].rolling(window=1).mean()
    # print("ser1: ", ser1)
    # print(type(ser1))

    ser1.set_index(["year", "Date"], inplace=True)
    ser1.sort_index(inplace=True)

    ser = ser1
    # print("Test Ser: ")
    # print(type(ser))
    # print(ser)

    # scale = [row[1] for row in px.colors.get_colorscale(option_slctd)]
    scale = [x for x in reversed(['rgb(255,0,0)', 'rgb(254,0,0)', 'rgb(252,0,0)', 'rgb(220,0,0)', 'rgb(190,0,0)', 'rgb(160,0,0)', 'rgb(130,0,0)', 'rgb(100,40,40)', 'rgb(60,60,60)'])]
    # print(scale)
    # print(ser.key())

    # mask = pd.DatetimeIndex(dff["Date"]).month
    fig = px.line(ser,
                  x=ser.index.get_level_values("Date"), y="Temperature",
                  color=ser.index.get_level_values("year"),
                  color_discrete_sequence=scale)

    fig.update_traces(dict(opacity=0.6), line_width=3)

    fig.update_layout(legend_font_color="goldenrod", legend_bordercolor="red", title="Average Monthly Temperature Range")

    return fig


@app.callback(
    Output("Monthly_Avg_Temps", "figure"),
    [Input("slct_color", "value"),
     Input(component_id='slct_data', component_property='value')]
)
def update_line_chart(option_slctd, data_option):
    print(option_slctd)

    dff = dfs[data_option].copy()
    dff["year"] = pd.DatetimeIndex(dff["Date"]).year
    dff["Date"] = dff["Date"].dt.strftime("0000-%m-00")

    ser = dff.groupby(["year", "Date"])["Temperature"].mean()
    # print("Test Ser: ")
    # print(ser)

    # dff = ser.unstack()
    # print("TEST dff: ")
    # print(dff[0:5])

    scale = [row[1] for row in px.colors.get_colorscale(option_slctd)]
    scale = [x for x in reversed(['rgb(255,0,0)', 'rgb(254,0,0)', 'rgb(252,0,0)', 'rgb(220,0,0)', 'rgb(190,0,0)', 'rgb(160,0,0)', 'rgb(130,0,0)', 'rgb(100,40,40)', 'rgb(60,60,60)'])]
    # print(scale)

    # mask = pd.DatetimeIndex(dff["Date"]).month
    fig = px.line(ser,
                  x=ser.index.get_level_values("Date"), y="Temperature",
                  color=ser.index.get_level_values("year"),
                  color_discrete_sequence=scale)

    fig.update_traces(dict(opacity=0.6), line_width=4)

    fig.update_layout(legend_font_color="goldenrod", legend_bordercolor="red", title="Average Monthly Temperatures")

    return fig


@app.callback(
    Output("Max_Min_Avg_Year_Temps", "figure"),
    [Input("slct_color", "value"),
     Input(component_id='slct_data', component_property='value')]
)
def update_line_chart(option_slctd, data_option):
    print(option_slctd)

    dff = dfs[data_option].copy()
    dff["Date"] = dff["Date"].dt.strftime("%Y")
    # print(dff[0:5])

    ser1 = dff.groupby(["Date"])["Temperature"].mean().reset_index()
    # dff1 = ser.unstack()
    # print(type(ser1))

    ser2 = dff.groupby(["Date"])["Temperature"].max().reset_index()
    ser3 = dff.groupby(["Date"])["Temperature"].min().reset_index()

    scale = [row[1] for row in px.colors.get_colorscale(option_slctd)]
    # scale = [x for x in reversed(['rgb(255,0,0)', 'rgb(254,0,0)', 'rgb(252,0,0)', 'rgb(220,0,0)', 'rgb(190,0,0)', 'rgb(160,0,0)', 'rgb(130,0,0)', 'rgb(100,40,40)', 'rgb(60,60,60)'])]
    # print(scale)

    fig = go.Figure()
    fig.add_traces([
        go.Scatter(
            x=ser1["Date"], y=ser1["Temperature"],
            mode="lines", name="Avg Temp"),
        go.Scatter(
            x=ser2["Date"], y=ser2["Temperature"],
            mode="lines", name="Max Temp"),
        go.Scatter(
            x=ser3["Date"], y=ser3["Temperature"],
            mode="lines", name="Min Temp"),
        ])

    fig.update_traces(dict(opacity=0.8), marker_line_width=30, marker_line_color=scale)

    fig.update_layout(legend_font_color="goldenrod", legend_bordercolor="red", title="Max, Min and Overall Average Yearly Temperatures")

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
