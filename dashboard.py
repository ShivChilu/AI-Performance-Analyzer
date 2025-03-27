from flask import Flask
import psutil
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"])
server = app.server

# Header Navigation Barphs

header = html.Div([
    html.Div([
        html.H2("AI Performance Analyzer", style={'color': '#00ffcc', 'marginLeft': '20px'}),
        html.Div([
            html.Button("🏠 Home", id="btn-home", n_clicks=0),
            html.Button("📊 Dashboard", id="btn-dashboard", n_clicks=0),
            html.Button("🚨 Bottlenecks", id="btn-bottlenecks", n_clicks=0),
            html.Button("🛠 Optimizations", id="btn-optimizations", n_clicks=0),
            html.Button("🔮 Predictions", id="btn-predictions", n_clicks=0),
            html.Button("🔒 Logout", id="btn-logout", n_clicks=0),
        ], style={'display': 'flex', 'gap': '15px', 'marginRight': '20px'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '15px', 'backgroundColor': '#000', 'color': 'white'})
])

# Home Page
home_content = html.Div(id='home-content', style={'textAlign': 'center', 'padding': '50px', 'color': 'white'}, children=[
    html.H1("Welcome to AI Performance Analyzer", style={'color': '#00ffcc'}),
    html.P("Monitor, detect bottlenecks, optimize performance, and predict future resource usage.", style={'fontSize': '18px'}),
    html.Button("🚀 Open Dashboard", id="start-dashboard", n_clicks=0, style={'padding': '10px 20px', 'borderRadius': '10px', 'backgroundColor': '#00ccff', 'color': 'white'}),
])

# Dashboard Page
dashboard_content = html.Div(id='dashboard-content', style={'padding': '20px', 'display': 'none'}, children=[
    html.H1("🚀 System Performance Dashboard", style={'textAlign': 'center', 'color': '#00ffcc'}),

    html.Div([
        html.Label("Select a Metric:", style={'color': 'white', 'fontSize': '18px'}),
        dcc.Dropdown(
            id="metric-dropdown",
            options=[
                {'label': 'All Metrics', 'value': 'all'},
                {'label': 'CPU Usage', 'value': 'cpu'},
                {'label': 'Memory Usage', 'value': 'memory'},
                {'label': 'Disk I/O', 'value': 'disk'},
                {'label': 'Network Activity', 'value': 'network'},
            ],
            placeholder="Select a metric...",
            style={'width': '50%', 'color': 'black'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    html.Div(id="selected-metric-container", style={'textAlign': 'center', 'backgroundColor': '#111', 'padding': '20px', 'borderRadius': '10px'})
])

# Bottlenecks Page
bottlenecks_content = html.Div(id='bottlenecks-content', style={'padding': '20px', 'display': 'none', 'textAlign': 'center', 'color': 'white'}, children=[
    html.H2("🚨 Bottlenecks Detected", style={'color': 'red'}),
    html.Div(id="bottleneck-details")
])

# Optimizations Page
optimization_content = html.Div(id='optimization-content', style={'padding': '20px', 'display': 'none', 'textAlign': 'center', 'color': 'white'}, children=[
    html.H2("🛠 Optimization Suggestions", style={'color': 'yellow'}),
    html.Div(id="optimization-suggestions")
])

# Predictions Page
predictions_content = html.Div(id='predictions-content', style={'padding': '20px', 'display': 'none', 'textAlign': 'center', 'color': 'white'}, children=[
    html.H2("🔮 Future Resource Forecast", style={'color': '#00ccff'}),
    html.Div(id="future-predictions")
])

# Main Layout
app.layout = html.Div([
    header,
    home_content,
    dashboard_content,
    bottlenecks_content,
    optimization_content,
    predictions_content
], style={'backgroundColor': '#000', 'color': 'white', 'height': '100vh', 'padding': '10px'})

# Navigation Callbacks
@app.callback(
    [Output('home-content', 'style'),
     Output('dashboard-content', 'style'),
     Output('bottlenecks-content', 'style'),
     Output('optimization-content', 'style'),
     Output('predictions-content', 'style')],
    [Input('btn-home', 'n_clicks'),
     Input('btn-dashboard', 'n_clicks'),
     Input('btn-bottlenecks', 'n_clicks'),
     Input('btn-optimizations', 'n_clicks'),
     Input('btn-predictions', 'n_clicks'),
     Input('start-dashboard', 'n_clicks')]
)
def navigate(home, dashboard, bottlenecks, optimizations, predictions, start):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [{'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]  

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    return [
        {'display': 'block' if button_id == 'btn-home' else 'none'},
        {'display': 'block' if button_id in ['btn-dashboard', 'start-dashboard'] else 'none'},
        {'display': 'block' if button_id == 'btn-bottlenecks' else 'none'},
        {'display': 'block' if button_id == 'btn-optimizations' else 'none'},
        {'display': 'block' if button_id == 'btn-predictions' else 'none'},
    ]

# **🚨 Bottleneck Detection Function**# **🚨 Bottleneck Detection Function (Now with Print Statements)**
# **🚨 Bottleneck Detection Function (Now with Images)**
# **🚨 Bottleneck Detection Function (Now with Large Image First)**
# **🚨 Bottleneck Detection Function (With Animated Images)**
@app.callback(
    [Output('bottleneck-details', 'children'),
     Output('optimization-suggestions', 'children')],
    Input('btn-bottlenecks', 'n_clicks')
)
def detect_bottlenecks(n_clicks):
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_io_counters().read_bytes / 1e6
    network_usage = psutil.net_io_counters().bytes_sent / 1e6

    bottlenecks = []
    optimizations = []

    # Image URLs
    cpu_image = "https://cdn-icons-png.flaticon.com/512/4341/4341026.png"
    memory_image = "https://cdn-icons-png.flaticon.com/512/1048/1048949.png"
    disk_image = "https://cdn-icons-png.flaticon.com/512/1027/1027328.png"
    network_image = "https://cdn-icons-png.flaticon.com/512/857/857708.png"

    # **🚀 CPU Bottleneck Detection**
    if cpu_usage > 85:
        bottlenecks.append((cpu_image, "🔥 **High CPU Usage** – Close unused applications or upgrade CPU."))
        optimizations.append("🔧 **Reduce background tasks, enable power-saving mode, and upgrade CPU if necessary.**")
    elif 70 <= cpu_usage <= 85:
        bottlenecks.append((cpu_image, "⚠️ **Moderate CPU Usage** – Running intensive tasks. Consider optimizing performance."))
        optimizations.append("💡 **Reduce active applications and unnecessary browser tabs to free CPU resources.**")

    # **💾 Memory Bottleneck Detection**
    if memory_usage > 90:
        bottlenecks.append((memory_image, "💾 **Critical Memory Usage** – System may freeze! Close programs or add more RAM."))
        optimizations.append("🛠 **Increase virtual memory, close heavy applications, and upgrade RAM if needed.**")
    elif 75 <= memory_usage <= 90:
        bottlenecks.append((memory_image, "⚠️ **High Memory Usage** – Consider closing unused apps or increasing RAM."))
        optimizations.append("💡 **Clear cache, disable auto-start programs, and increase swap space.**")

    # **📀 Disk Bottleneck Detection**
    if disk_usage > 300:
        bottlenecks.append((disk_image, "📀 **High Disk Read/Write Usage** – Reduce disk-intensive tasks."))
        optimizations.append("💽 **Run disk cleanup, upgrade to an SSD, and disable background disk-heavy processes.**")
    elif 100 <= disk_usage <= 300:
        bottlenecks.append((disk_image, "⚠️ **Moderate Disk Usage** – Heavy operations detected."))
        optimizations.append("💡 **Avoid running multiple disk-heavy apps simultaneously.**")

    # **🌐 Network Bottleneck Detection**
    if network_usage > 100:
        bottlenecks.append((network_image, "🌐 **High Network Traffic** – Limit downloads or bandwidth-heavy applications."))
        optimizations.append("🌍 **Limit streaming quality, check for malware, and optimize router settings.**")
    elif 50 <= network_usage <= 100:
        bottlenecks.append((network_image, "⚠️ **Moderate Network Usage** – Check active downloads."))
        optimizations.append("💡 **Prioritize essential network tasks and close unnecessary network-consuming apps.**")

    # **No Bottlenecks Detected**
    if not bottlenecks:
        return html.P("✅ No bottlenecks detected. System is running optimally!", style={'fontSize': '18px', 'color': 'green'}), ""

    return html.Div([
        html.Div([
            html.Img(src=image_url, style={
                'width': '120px', 'height': '120px',
                'display': 'block', 'margin': 'auto',
                'animation': 'zoomIn 1.5s ease-in-out'
            }),
            html.P(text, style={'fontSize': '18px', 'color': 'white', 'textAlign': 'center'})
        ], style={'padding': '20px', 'marginBottom': '20px', 'borderRadius': '10px', 'backgroundColor': '#111'})
        for image_url, text in bottlenecks
    ]), html.Div([
        html.P(tip, style={'fontSize': '18px', 'color': 'cyan'}) for tip in optimizations
    ])


# **✅ Corrected Dash `index_string` with Required Placeholders**
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Performance Analyzer</title>
    <style>
        @keyframes zoomIn {
            0% { transform: scale(0.5); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''

# **📊 Metric Selection Callback (Gauge Indicators for All Metrics)**
@app.callback(
    Output('selected-metric-container', 'children'),
    Input('metric-dropdown', 'value')
)
def update_metric(selected_metric):
    if not selected_metric:
        return html.P("Please select a metric to display.", style={'color': 'white', 'fontSize': '18px'})

    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_io_counters().read_bytes / 1e6
    network_usage = psutil.net_io_counters().bytes_sent / 1e6

    metric_data = {
        "cpu": ("CPU Usage", cpu_usage, "#ff4d4d"),
        "memory": ("Memory Usage", memory_usage, "#4d79ff"),
        "disk": ("Disk Read (MB)", disk_usage, "#ffaa00"),
        "network": ("Network Sent (MB)", network_usage, "#00ffcc"),
    }

    return html.Div([
        dcc.Graph(figure=go.Figure(go.Indicator(mode="gauge+number", value=value, title={'text': title}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': color}})), config={'displayModeBar': False}) 
        for title, value, color in metric_data.values()
    ]) if selected_metric == "all" else dcc.Graph(figure=go.Figure(go.Indicator(mode="gauge+number", value=metric_data[selected_metric][1], title={'text': metric_data[selected_metric][0]}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': metric_data[selected_metric][2]}})), config={'displayModeBar': False})

if __name__ == '__main__':
    app.run_server(debug=True)
