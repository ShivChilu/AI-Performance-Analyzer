from flask import Flask
import psutil
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import time
from prophet import Prophet

app = dash.Dash(__name__)
server = app.server

# Store historical data
cpu_history = []
memory_history = []
bottleneck_count = 0  # Count number of high usage events

# App layout
app.layout = html.Div([
    html.H1("AI-powered Performance Analyzer", style={'textAlign': 'center', 'color': '#4CAF50'}),

    html.Div([
        dcc.Graph(id='cpu-graph', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='memory-graph', style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.H2("Performance Insights", style={'textAlign': 'center'}),
    html.Div(id='bottleneck-alert', style={'textAlign': 'center', 'color': 'red', 'fontSize': 20}),
    html.Div(id='optimization-tips', style={'textAlign': 'center', 'color': 'blue', 'fontSize': 18}),

    html.H2("CPU Usage Forecast", style={'textAlign': 'center'}),
    dcc.Graph(id='cpu-forecast'),

    html.H2("Final Analysis", style={'textAlign': 'center'}),
    dash_table.DataTable(
        id='final-analysis-table',
        columns=[
            {"name": "Metric", "id": "metric"},
            {"name": "Value", "id": "value"}
        ],
        style_cell={'textAlign': 'center'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    ),

    dcc.Interval(id='interval-component', interval=3000, n_intervals=0)  # Update every 3 sec
])

def forecast_cpu_usage(data):
    df = pd.DataFrame(data, columns=["ds", "y"])
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=10, freq="S")
    forecast = model.predict(future)
    return forecast

@app.callback(
    [Output('cpu-graph', 'figure'),
     Output('memory-graph', 'figure'),
     Output('bottleneck-alert', 'children'),
     Output('optimization-tips', 'children'),
     Output('cpu-forecast', 'figure'),
     Output('final-analysis-table', 'data')],
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    global cpu_history, memory_history, bottleneck_count

    # Get real-time usage
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    current_time = pd.Timestamp.now()


    # Keep last 50 readings
    if len(cpu_history) > 50:
        cpu_history.pop(0)
    if len(memory_history) > 50:
        memory_history.pop(0)

    cpu_history.append((current_time, cpu_usage))
    memory_history.append((current_time, memory_usage))

    # Count bottlenecks
    if cpu_usage > 85 or memory_usage > 85:
        bottleneck_count += 1

    # Unpack history
    times, cpu_values = zip(*cpu_history)
    _, memory_values = zip(*memory_history)

    # CPU graph with color change for high usage
    cpu_trace = go.Scatter(
        x=list(times), y=list(cpu_values), mode='lines+markers',
        line=dict(color='red' if max(cpu_values) > 80 else 'green')
    )

    # Memory graph with color change for high usage
    memory_trace = go.Scatter(
        x=list(times), y=list(memory_values), mode='lines+markers',
        line=dict(color='red' if max(memory_values) > 80 else 'blue')
    )

    # Detect bottlenecks
    alert_message = ""
    if cpu_usage > 85:
        alert_message = "⚠️ High CPU Usage! Consider closing unused applications."
    elif memory_usage > 85:
        alert_message = "⚠️ High Memory Usage! Consider optimizing running processes."

    # Optimization tips
    optimization_tip = ""
    if cpu_usage > 85:
        optimization_tip = "🔧 Reduce background processes or upgrade your CPU."
    elif memory_usage > 85:
        optimization_tip = "🔧 Close memory-intensive applications or increase RAM."

    # CPU Usage Forecast
    if len(cpu_history) > 10:
        forecast_data = [(time, value) for time, value in cpu_history]
        forecast = forecast_cpu_usage(forecast_data)
        forecast_fig = go.Figure([
            go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name="Predicted Usage")
        ])
        forecast_fig.update_layout(title="Predicted CPU Usage for Next 10 Seconds", xaxis_title="Time", yaxis_title="CPU %")
    else:
        forecast_fig = go.Figure()

    # Final Analysis Table
    analysis_data = [
        {"metric": "Average CPU Usage", "value": f"{sum(cpu_values)/len(cpu_values):.2f}%"},
        {"metric": "Max CPU Usage", "value": f"{max(cpu_values)}%"},
        {"metric": "Min CPU Usage", "value": f"{min(cpu_values)}%"},
        {"metric": "Average Memory Usage", "value": f"{sum(memory_values)/len(memory_values):.2f}%"},
        {"metric": "Max Memory Usage", "value": f"{max(memory_values)}%"},
        {"metric": "Min Memory Usage", "value": f"{min(memory_values)}%"},
        {"metric": "Total Bottlenecks Detected", "value": bottleneck_count}
    ]

    return (
        {'data': [cpu_trace], 'layout': go.Layout(title="Real-Time CPU Usage", xaxis_title="Time", yaxis_title="CPU %")},
        {'data': [memory_trace], 'layout': go.Layout(title="Real-Time Memory Usage", xaxis_title="Time", yaxis_title="Memory %")},
        alert_message,
        optimization_tip,
        forecast_fig,
        analysis_data
    )
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=10000)


