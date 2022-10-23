import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

data_path = '<absolute to preprocessed data csv>'
price_e = 0.42316   #price electricity
price_g = 1.77187   #price gas

df = pd.read_csv(data_path)

# Calculate daily consumption + corresponding costs of consumption

totals_e_date = df['e_total'].groupby(df['date']).sum()
totals_e_date_cost = totals_e_date.apply(lambda x: round(x*price_e, 3))

totals_g_date = df['gas_consumed'].groupby(df['date']).sum()
totals_g_date_cost = totals_g_date.apply(lambda x: round(x*price_g, 3))

# Calculate hourly consumption + corresponding costs of consumption

totals_e_hour = df['e_total'].groupby(df['hour']).mean()
totals_g_hour = df['gas_consumed'].groupby(df['hour']).mean()

# Calculate consumption per weekday + corresponding costs of consumption

totals_e_day = df['e_total'].groupby(df['day']).sum()
totals_g_day = df['gas_consumed'].groupby(df['day']).sum()

# Dash dashboard

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H5('Electricity Consumed - Last 48 hours (kWh)'),
            dcc.Graph(
                id='g1',
                figure={
                    'data': [
                        go.Scatter(
                            x=df['date_time'].tail(48),
                            y=df['e_total'].tail(48),
                            name="kWh",
                            showlegend=False,
                            line = dict(
                                    width = 1,
                                    shape = 'spline',
                            )
                        ),
                        go.Scatter(
                            x=df['date_time'].tail(48),
                            y=df['e_total_cost'].tail(48),
                            name="EUR",
                            yaxis='y2',
                            showlegend=False,
                            line = dict(
                                    width = 3,
                                    shape = 'spline',
                            )
                        ),
                    ],
                    'layout': go.Layout(
                        xaxis={
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                            },
                        yaxis={'title': 'kWh',
                            'showgrid': True,
                            'zeroline': False,
                            'showline': False,
                               },
                        yaxis2={'title': 'EUR',
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                            'overlaying': 'y',
                            'side': 'right',
                               },
                    )
                }
            )
        ], style={}, className="six columns"),

        html.Div([
            html.H5('Gas consumed  - Last 48 hours (m3)'),
            dcc.Graph(
                id='g2',
                figure={
                    'data': [
                        go.Scatter(
                            x=df['date_time'].tail(48),
                            y=df['gas_consumed'].tail(48),
                            name='m3',
                            showlegend=False,
                            line=dict(
                                width=1,
                                shape='spline',
                            )
                        ),
                        go.Scatter(
                            x=df['date_time'].tail(48),
                            y=df['gas_cost'].tail(48),
                            name='EUR',
                            yaxis='y2',
                            showlegend=False,
                            line=dict(
                                width=3,
                                shape='spline',
                            )
                        ),
                    ],
                    'layout': go.Layout(
                        xaxis={
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                            },
                        yaxis={'title': 'm3',
                            'showgrid': True,
                            'zeroline': False,
                            'showline': False,
                               },
                        yaxis2={'title': 'EUR',
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                            'overlaying': 'y',
                            'side': 'right',
                               },
                    )
                }
            )
        ], className="six columns"),
    ], className="row"),

html.Div([
        html.Div([
            html.H5('Electricity Consumed (kWh) - Date'),
            dcc.Graph(
                id='g5',
                figure={
                    'data': [
                        go.Scatter(
                            x=totals_e_date.index.values,
                            y=totals_e_date.values.tolist(),
                            name="kWh",
                            showlegend=False,
                            line=dict(
                                width=1,
                                shape='spline',
                            )

                        ),
                        go.Scatter(
                            x=totals_e_date.index.values,
                            y=totals_e_date_cost.values.tolist(),
                            name="EUR",
                            yaxis='y2',
                            showlegend=False,
                            line=dict(
                                width=3,
                                shape='spline',
                            )

                        ),
                    ],
                    'layout': go.Layout(
                        xaxis={
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                        },
                        yaxis={'title': 'kWh',
                               'showgrid': True,
                               'zeroline': False,
                               'showline': False,
                               },
                        yaxis2={'title': 'EUR',
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                            'overlaying': 'y',
                            'side': 'right',
                               },
                    )
                }
            )

        ], style={'padding-top': 50}, className="six columns"),

        html.Div([
            html.H5('Gas consumed (m3) - Date'),
            dcc.Graph(
                id='g6',
                figure={
                    'data': [
                        go.Scatter(
                            x=totals_g_date.index.values,
                            y=totals_g_date.values.tolist(),
                            name="m3",
                            showlegend=False,
                            line=dict(
                                width=1,
                                shape='spline',
                            )

                        ),
                        go.Scatter(
                            x=totals_g_date.index.values,
                            y=totals_g_date_cost.values.tolist(),
                            name="EUR",
                            yaxis='y2',
                            showlegend=False,
                            line=dict(
                                width=3,
                                shape='spline',
                            )

                        ),
                    ],
                    'layout': go.Layout(
                        xaxis={
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                        },
                        yaxis={'title': 'm3',
                               'showgrid': True,
                               'zeroline': False,
                               'showline': False,
                               },
                        yaxis2={'title': 'EUR',
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                            'overlaying': 'y',
                            'side': 'right',
                               },
                    )
                }
            )
        ], style={'padding-top': '50'}, className="six columns"),
    ], className="row"),

html.Div([
        html.Div([
            html.H5('Electricity Consumed (kWh) - Hour'),
            dcc.Graph(
                id='g7',
                figure={
                    'data': [
                        go.Bar(
                            x=totals_g_hour.index.values,
                            y=totals_e_hour.values.tolist(),
                            name="kWh consumed",

                        ),
                    ],
                    'layout': go.Layout(
                        xaxis={
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                        },
                        yaxis={'title': 'kWh',
                               'showgrid': True,
                               'zeroline': False,
                               'showline': False,
                               },
                    )
                }
            )

        ], style={'padding-top': 50}, className="six columns"),

        html.Div([
            html.H5('Gas consumed (m3) - Hour'),
            dcc.Graph(
                id='g8',
                figure={
                    'data': [
                        go.Bar(
                            x=totals_g_hour.index.values,
                            y=totals_g_hour.values.tolist(),
                            name="m3 consumed",

                        ),
                    ],
                    'layout': go.Layout(
                        xaxis={
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                        },
                        yaxis={'title': 'm3',
                               'showgrid': True,
                               'zeroline': False,
                               'showline': False,
                               },
                    )
                }
            )
        ], style={'padding-top': '50'}, className="six columns"),
    ], className="row"),

html.Div([
        html.Div([
            html.H5('Electricity Consumed (kWh) - Day of the Week'),
            dcc.Graph(
                id='g3',
                figure={
                    'data': [
                        go.Bar(
                            x=totals_e_day.index.values,
                            y=totals_e_day.values.tolist(),
                            name="kWh consumed",

                        ),
                    ],
                    'layout': go.Layout(
                        xaxis={
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                        },
                        yaxis={'title': 'kWh',
                               'showgrid': True,
                               'zeroline': False,
                               'showline': False,
                               },
                    )
                }
            )

        ], style={'padding-top': 50}, className="six columns"),

        html.Div([
            html.H5('Gas consumed (m3) - Day of the Week'),
            dcc.Graph(
                id='g4',
                figure={
                    'data': [
                        go.Bar(
                            x=totals_g_day.index.values,
                            y=totals_g_day.values.tolist(),
                            name="m3 consumed",

                        ),
                    ],
                    'layout': go.Layout(
                        xaxis={
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                        },
                        yaxis={'title': 'm3',
                               'showgrid': True,
                               'zeroline': False,
                               'showline': False,
                               },
                    )
                }
            )
        ], style={'padding-top': '50'}, className="six columns"),
    ], className="row"),

], style={'marginBottom': 50, 'marginTop': 30, 'text-align': 'center'})


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
