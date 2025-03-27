import psutil
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from dash import ctx
import numpy as np
from collections import deque
cpu_usage_history = deque(maxlen=20)  

app = dash.Dash(__name__, external_stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"])
server = app.server
def calculate_phs():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_io_counters().read_bytes / (1024 * 1024) 
    network_usage = psutil.net_io_counters().bytes_sent / (1024 * 1024)  

    disk_usage = min(disk_usage / 500 * 100, 100)  
    network_usage = min(network_usage / 100 * 100, 100) 

    score = 100 - ((cpu_usage * 0.4) + (memory_usage * 0.3) + (disk_usage * 0.2) + (network_usage * 0.1))

    phs_score = max(0, min(100, score))

    reasons = []
    if phs_score < 80:
        if cpu_usage > 70:
            reasons.append("⚠️ High CPU usage detected.")
        if memory_usage > 75:
            reasons.append("💾 High memory usage detected.")
        if disk_usage > 70:
            reasons.append("📀 High disk activity detected.")
        if network_usage > 50:
            reasons.append("🌐 High network traffic detected.")

    return phs_score, reasons

  
# Header Navigation Bar
header = html.Div([
    html.Div([
        #  Logo / Title
        html.H2("AI Performance Analyzer", 
                className="text-cyan-400 text-xl font-bold ml-4 tracking-wider drop-shadow-lg"),

        
        html.Div([
            html.Button("🏠 Home", id="btn-home", n_clicks=0, 
                        className="px-6 py-1.5 mx-1 border border-cyan-500 bg-transparent text-white text-sm font-medium rounded-md hover:bg-cyan-600 hover:shadow-cyan-400 hover:scale-105 transition-all duration-300 shadow-md active:scale-150"),
            html.Button("📉 PHS Score", id="btn-phs", n_clicks=0, 
                        className="px-6 py-1.5 mx-1 border border-green-500 bg-transparent text-white text-sm font-medium rounded-md hover:bg-green-600 hover:shadow-green-400 hover:scale-105 transition-all duration-300 shadow-md active:scale-150"),
            html.Button("📊 Dashboard", id="btn-dashboard", n_clicks=0, 
                        className="px-6 py-1.5 mx-1 border border-blue-500 bg-transparent text-white text-sm font-medium rounded-md hover:bg-blue-600 hover:shadow-blue-400 hover:scale-105 transition-all duration-300 shadow-md active:scale-150"),
            html.Button("📋 Processes", id="btn-processes", n_clicks=0, 
                        className="px-6 py-1.5 mx-1 border border-purple-500 bg-transparent text-white text-sm font-medium rounded-md hover:bg-purple-600 hover:shadow-purple-400 hover:scale-105 transition-all duration-300 shadow-md active:scale-150"),
            html.Button("🚨 Bottlenecks", id="btn-bottlenecks", n_clicks=0, 
                        className="px-6 py-1.5 mx-1 border border-red-500 bg-transparent text-white text-sm font-medium rounded-md hover:bg-red-600 hover:shadow-red-400 hover:scale-105 transition-all duration-300 shadow-md active:scale-150"),
            html.Button("🛠 Optimizations", id="btn-optimizations", n_clicks=0, 
                        className="px-6 py-1.5 mx-1 border border-yellow-500 bg-transparent text-white text-sm font-medium rounded-md hover:bg-yellow-600 hover:shadow-yellow-400 hover:scale-105 transition-all duration-300 shadow-md active:scale-150"),
            html.Button("🔮 Predictions", id="btn-predictions", n_clicks=0, 
                        className="px-6 py-1.5 mx-1 border border-indigo-500 bg-transparent text-white text-sm font-medium rounded-md hover:bg-indigo-600 hover:shadow-indigo-400 hover:scale-105 transition-all duration-300 shadow-md active:scale-150"),
            html.Button("🔒 Logout", id="btn-logout", n_clicks=0, 
                        className="px-6 py-1.5 mx-1 border border-gray-500 bg-transparent text-white text-sm font-medium rounded-md hover:bg-gray-600 hover:shadow-gray-400 hover:scale-105 transition-all duration-300 shadow-md active:scale-150"),
        ], className="flex gap-1.5 mr-4"),
        
    ], className="flex justify-between items-center px-4 py-4 bg-opacity-90 bg-gray-900 shadow-lg border-b-2 border-cyan-500 backdrop-blur-lg relative"),
  
])



home_content = html.Div(
    id='home-content',
    className="text-center text-white mt-12 space-y-8 bg-gradient-to-br from-gray-900 via-black to-gray-900 min-h-screen flex flex-col items-center justify-center relative",
    children=[

      
        html.H1("Welcome to AI Performance Analyzer",
                className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500 animate-pulse"),
        
        
        html.P(
            "Monitor system performance, detect bottlenecks, optimize performance, and predict future resource usage.",
            className="text-lg text-gray-300 opacity-90 animate-fadeIn"
        ),

        html.Div(
            className="grid grid-cols-1 md:grid-cols-4 gap-6 px-10 mt-8",
            children=[
                html.Div(className="bg-gray-800 bg-opacity-80 backdrop-blur-md p-8 rounded-lg shadow-xl "
                                   "transition-transform hover:scale-105 hover:shadow-cyan-500 w-96 h-56",
                         children=[
                             html.H2("🔍 AI-Powered Analysis", className="text-2xl font-semibold text-blue-300"),
                             html.P("AI continuously monitors & analyzes system performance\n"
                                    "to detect inefficiencies before issues occur.",
                                    className="text-gray-300 text-md mt-2 leading-relaxed whitespace-pre-line"),
                         ]),

                html.Div(className="bg-gray-800 bg-opacity-80 backdrop-blur-md p-8 rounded-lg shadow-xl "
                                   "transition-transform hover:scale-105 hover:shadow-yellow-500 w-96 h-56",
                         children=[
                             html.H2("📊 Predictive Insights", className="text-2xl font-semibold text-yellow-300"),
                             html.P("Forecasts future CPU, memory, and disk usage\n"
                                    "to help avoid sudden performance drops.",
                                    className="text-gray-300 text-md mt-2 leading-relaxed whitespace-pre-line"),
                         ]),

                html.Div(className="bg-gray-800 bg-opacity-80 backdrop-blur-md p-8 rounded-lg shadow-xl "
                                   "transition-transform hover:scale-105 hover:shadow-green-500 w-96 h-56",
                         children=[
                             html.H2("🚀 Smart Optimization", className="text-2xl font-semibold text-green-300"),
                             html.P("AI suggests optimizations to reduce lag,\n"
                                    "enhance performance, and save power.",
                                    className="text-gray-300 text-md mt-2 leading-relaxed whitespace-pre-line"),
                         ]),

                html.Div(className="bg-gray-800 bg-opacity-80 backdrop-blur-md p-8 rounded-lg shadow-xl "
                                   "transition-transform hover:scale-105 hover:shadow-indigo-500 w-96 h-56",
                         children=[
                             html.H2("📌 System Health Monitoring", className="text-2xl font-semibold text-indigo-300"),
                             html.P("Tracks real-time performance scores\n"
                                    "to ensure smooth system operation.",
                                    className="text-gray-300 text-md mt-2 leading-relaxed whitespace-pre-line"),
                         ]),
            ]
        ),

       
        html.Div(className="relative w-full overflow-hidden mt-10", children=[
            html.Div(className="animate-scroll flex space-x-6 whitespace-nowrap w-full", children=[
                html.Div(className="flex space-x-6", children=[
                    html.Div(className="bg-gray-800 bg-opacity-80 backdrop-blur-md p-8 rounded-lg shadow-xl "
                                       "w-96 h-64 overflow-hidden flex flex-col items-center transition-transform hover:scale-105 hover:shadow-cyan-500",
                             children=[
                                 html.Img(src="https://cdn-icons-png.flaticon.com/512/4281/4281797.png", className="w-16 h-16"),
                                 html.H2("🔍 AI-Powered Analysis", className="text-xl font-semibold text-blue-300 mt-2"),
                                 html.P("Monitors system efficiency in real time,\n"
                                        "ensuring proactive issue resolution before they impact performance.",
                                        className="text-gray-300 text-md mt-2 leading-relaxed text-center whitespace-pre-line"),
                             ]),

                    html.Div(className="bg-gray-800 bg-opacity-80 backdrop-blur-md p-8 rounded-lg shadow-xl "
                                       "w-96 h-64 overflow-hidden flex flex-col items-center transition-transform hover:scale-105 hover:shadow-yellow-500",
                             children=[
                                 html.Img(src="https://cdn-icons-png.flaticon.com/512/2333/2333227.png", className="w-16 h-16"),
                                 html.H2("📊 Predictive Insights", className="text-xl font-semibold text-yellow-300 mt-2"),
                                 html.P("Forecasts CPU, memory, and disk usage\n"
                                        "to prevent performance bottlenecks.",
                                        className="text-gray-300 text-md mt-2 leading-relaxed text-center whitespace-pre-line"),
                             ]),

                    html.Div(className="bg-gray-800 bg-opacity-80 backdrop-blur-md p-8 rounded-lg shadow-xl "
                                       "w-96 h-64 overflow-hidden flex flex-col items-center transition-transform hover:scale-105 hover:shadow-green-500",
                             children=[
                                 html.Img(src="https://cdn-icons-png.flaticon.com/512/1057/1057075.png", className="w-16 h-16"),
                                 html.H2("🚀 Smart Optimization", className="text-xl font-semibold text-green-300 mt-2"),
                                 html.P("AI-based performance tuning suggests ways\n"
                                        "to improve efficiency, enhance responsiveness,\n"
                                        "and reduce power usage.",
                                        className="text-gray-300 text-md mt-2 leading-relaxed text-center whitespace-pre-line"),
                             ]),

                    html.Div(className="bg-gray-800 bg-opacity-80 backdrop-blur-md p-8 rounded-lg shadow-xl "
                                       "w-96 h-64 overflow-hidden flex flex-col items-center transition-transform hover:scale-105 hover:shadow-red-500",
                             children=[
                                 html.Img(src="https://cdn-icons-png.flaticon.com/512/1611/1611179.png", className="w-16 h-16"),
                                 html.H2("🛡️ Security & Anomaly Detection", className="text-xl font-semibold text-red-300 mt-2"),
                                 html.P("Detects and alerts you about unusual resource spikes,\n"
                                        "which may indicate security threats or software anomalies.",
                                        className="text-gray-300 text-md mt-2 leading-relaxed text-center whitespace-pre-line"),
                             ]),
                ] * 2)  
            ]),
        ]),

      
        html.Div(className="bg-gray-900 p-6 rounded-lg mt-10 flex flex-wrap justify-center gap-6 shadow-lg", children=[
            html.Button("🚀 Open Dashboard", id="start-dashboard", n_clicks=0,
                        className="px-6 py-3 text-white font-semibold rounded-lg bg-cyan-500 hover:bg-cyan-600 transition-all shadow-xl hover:shadow-cyan-500 animate-bounce"),
            html.Button("📋 View Active Processes", id="btn-processes", n_clicks=0,
                        className="px-6 py-3 text-white font-semibold rounded-lg bg-purple-600 hover:bg-purple-700 transition-all shadow-xl hover:shadow-purple-500"),
            html.Button("🚨 Detect Bottlenecks", id="btn-bottlenecks", n_clicks=0,
                        className="px-6 py-3 text-white font-semibold rounded-lg bg-red-600 hover:bg-red-700 transition-all shadow-xl hover:shadow-red-500"),
        ]),

        
        html.Div(className="absolute top-10 left-10 w-16 h-16 bg-cyan-500 rounded-full blur-3xl opacity-20 animate-floating"),
        html.Div(className="absolute bottom-20 right-20 w-24 h-24 bg-blue-500 rounded-full blur-3xl opacity-30 animate-floating"),
    ]
)


phs_content = html.Div(id='phs-content', style={'padding': '20px', 'display': 'none', 'textAlign': 'center', 'color': 'white'}, children=[
    html.H2("📉 AI-Powered Performance Health Score (PHS)™", style={'color': '#00ccff'}),
    dcc.Interval(id='phs-timer', interval=2000, max_intervals=1, disabled=True),  

    html.Div(id='phs-loading', style={'display': 'none'}, children=[
        html.Div("⏳ Analyzing...", style={'fontSize': '22px', 'color': '#ffcc00'}),
        html.Div(className="loading-circle", style={
            'width': '50px', 'height': '50px', 'border': '5px solid #00ccff',
            'borderTop': '5px solid transparent', 'borderRadius': '50%',
            'animation': 'spin 1s linear infinite', 'margin': 'auto', 'marginTop': '10px'
        })
    ]),

    dcc.Graph(id='phs-score', style={'display': 'none'}),
    html.P(id='phs-details', style={'fontSize': '20px', 'color': 'white', 'display': 'none'})
])


# Dashboard Page
dashboard_content = html.Div(id='dashboard-content', style={'padding': '0px',
        'width': '100%',
        'height': '100vh',
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'backgroundColor': 'linear-gradient(to bottom right, #8b0000, #ff0000, #ffffff)'    }, children=[
    html.H1("🚀 System Performance Dashboard", style={'textAlign': 'center', 'color': '#00ffcc ' ,'padding': '0px', 'display': 'none', 'width': '100%', 'height': '100vh'}),

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

process_content = html.Div(id='process-content', style={'padding': '20px', 'display': 'none', 'color': 'white'}, children=[
    html.H2("📋 Active Processes", style={'color': '#00ccff', 'textAlign': 'center'}),
    html.Div(id="process-list", style={'maxHeight': '400px', 'overflowY': 'scroll', 'backgroundColor': '#111', 'padding': '10px', 'borderRadius': '10px'})
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
    html.Button("📈 Predict CPU Usage", id="btn-cpu-predict", n_clicks=0, style={'padding': '10px 20px', 'borderRadius': '10px', 'backgroundColor': '#00ccff', 'color': 'white'}),
    dcc.Graph(id='cpu-forecast-graph', style={'display': 'none'})  # Initially hidden
])
@app.callback(
    [Output('cpu-forecast-graph', 'figure'),
     Output('cpu-forecast-graph', 'style')],
    [Input('btn-cpu-predict', 'n_clicks')]
)
def predict_cpu_usage(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate

    # Generate real-time CPU usage history
    cpu_usage_history.append(psutil.cpu_percent(interval=1))

    # Simulate future predictions (simple trendline based on moving average)
    history = list(cpu_usage_history)
    future = [np.mean(history[-5:]) + np.random.uniform(-2, 2) for _ in range(10)]  # Predict next 10 points

    # Generate x-axis labels
    time_stamps = list(range(len(history)))
    future_stamps = list(range(len(history), len(history) + len(future)))

    # Create a forecast graph
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=time_stamps, y=history, mode='lines+markers', name='Historical CPU Usage', line=dict(color='yellow')))
    figure.add_trace(go.Scatter(x=future_stamps, y=future, mode='lines+markers', name='Predicted CPU Usage', line=dict(color='red', dash='dot')))

    figure.update_layout(title="📈 CPU Usage Forecast",
                         xaxis_title="Time",
                         yaxis_title="CPU Usage (%)",
                         template="plotly_dark")

    return figure, {'display': 'block'}


# Main Layout
app.layout = html.Div([
    header,
    home_content,
    phs_content, 
    dashboard_content,
    process_content,
    bottlenecks_content,
    optimization_content,
    predictions_content
], style={'backgroundColor': '#000', 'color': 'white', 'height': '100vh', 'padding': '10px'})

@app.callback(
    [Output('home-content', 'style'),
     Output('dashboard-content', 'style'),
     Output('phs-content', 'style'),  
     Output('bottlenecks-content', 'style'),
     Output('optimization-content', 'style'),
     Output('predictions-content', 'style'),
    Output('process-content', 'style')],
    [Input('btn-home', 'n_clicks'),
     Input('btn-dashboard', 'n_clicks'),
     Input('btn-phs', 'n_clicks'), 
     Input('btn-bottlenecks', 'n_clicks'),
     Input('btn-optimizations', 'n_clicks'),
     Input('btn-predictions', 'n_clicks'),
     Input('start-dashboard', 'n_clicks'),
     Input('btn-processes', 'n_clicks')]
)
def navigate(home, dashboard, phs, bottlenecks, optimizations, predictions, start,processes):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [{'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'},{'display': 'none'}]

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    return [
        {'display': 'block' if button_id == 'btn-home' else 'none'},
        {'display': 'block' if button_id in ['btn-dashboard', 'start-dashboard'] else 'none'},
        {'display': 'block' if button_id == 'btn-phs' else 'none'},  
        {'display': 'block' if button_id == 'btn-bottlenecks' else 'none'},
        {'display': 'block' if button_id == 'btn-optimizations' else 'none'},
        {'display': 'block' if button_id == 'btn-predictions' else 'none'},
        {'display': 'block' if button_id == 'btn-processes' else 'none'}
    ]


@app.callback(
    Output('process-list', 'children'),
    Input('btn-processes', 'n_clicks')
)
def list_active_processes(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate

   

    process_data = []
    for proc in psutil.process_iter(['pid', 'name',  'memory_percent']):
        try:
            process_info = proc.info
            process_data.append(f"🔹 PID: {process_info['pid']} | Name: {process_info['name']}  | RAM: {process_info['memory_percent']}%")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if not process_data:
        return html.P("⚠️ No active processes found!", style={'color': 'red'})

    return html.Div([html.P(proc, style={'margin': '5px 0'}) for proc in process_data])



@app.callback(
    [Output('bottleneck-details', 'children'),
     Output('optimization-suggestions', 'children')],
    Input('btn-bottlenecks', 'n_clicks')
)
def detect_bottlenecks(n_clicks):
    cpu_usage = psutil.cpu_percent(interval=1)
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
        return html.P(" No bottlenecks detected. System is running optimally!", style={'fontSize': '18px', 'color': 'green'}), ""

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

from dash import ctx

@app.callback(
    [Output('phs-loading', 'style'),  
     Output('phs-score', 'style'),  
     Output('phs-details', 'style'), 
     Output('phs-score', 'figure'), 
     Output('phs-details', 'children'),  
     Output('phs-timer', 'disabled')],  
    [Input('btn-phs', 'n_clicks'),
     Input('phs-timer', 'n_intervals')],
    [State('phs-timer', 'disabled')],
    prevent_initial_call=True
)
def update_phs(n_clicks, n_intervals, is_timer_disabled):
   
    if ctx.triggered_id == "btn-phs":
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, go.Figure(), "", False  # Start Timer

    if n_intervals is not None:  # Timer completed
        phs_value, reasons = calculate_phs()

      
        phs_graph = go.Figure(go.Indicator(
            mode="gauge+number",
            value=phs_value,
            title={'text': "Performance Health Score (PHS)™"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#00ffcc"}}
        ))

        #  Generate Performance Status
        phs_status = "🟢 Excellent Performance" if phs_value > 80 else "🟠 Moderate Performance" if phs_value > 50 else "🔴 Poor Performance"

        #  Combine Reasons for Poor/Moderate PHS
        reasons_text = "\n".join(reasons) if reasons else "✅ No issues detected."

        return {'display': 'none'}, {'display': 'block'}, {'display': 'block'}, phs_graph, f"PHS Score: {phs_value:.2f}% - {phs_status}\n\n{reasons_text}", True  # Stop Timer

    return dash.no_update  # Default: No UI change

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Performance Analyzer</title>
    <style>
        /* Zoom-In Animation */
        @keyframes zoomIn {
            0% { transform: scale(0.5); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        /* Spinner Animation */
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Center Loader */
        .loading-circle {
            width: 50px;
            height: 50px;
            border: 5px solid #00ccff;
            border-top: 5px solid transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: auto;
            margin-top: 10px;
        }
       @keyframes scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.animate-scroll {
    display: flex;
    animation: scroll 15s linear infinite;
}

    </style>
    <script src="https://cdn.tailwindcss.com"></script>
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

# ** Metric Selection Callback (Gauge Indicators for All Metrics)**
@app.callback(
    Output('selected-metric-container', 'children'),
    Input('metric-dropdown', 'value')
)
def update_metric(selected_metric):
    if not selected_metric:
        return html.P("Please select a metric to display.", className="text-white text-lg text-center")

    #  Fetch Real-time Metrics
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_io_counters().read_bytes / 1e6  # Convert to MB
    network_usage = psutil.net_io_counters().bytes_sent / 1e6  # Convert to MB

    #  Metric Data (Title, Value, Styling, Gauge Color)
    metric_data = {
        "cpu": ("CPU Usage", cpu_usage, "text-red-400 border-red-500 shadow-red-500", "red"),
        "memory": ("Memory Usage", memory_usage, "text-blue-400 border-blue-500 shadow-blue-500", "blue"),
        "disk": ("Disk Read (MB)", disk_usage, "text-yellow-400 border-yellow-500 shadow-yellow-500", "yellow"),
        "network": ("Network Sent (MB)", network_usage, "text-green-400 border-green-500 shadow-green-500", "green"),
    }

    #  Ensure a Single Parent Container
    content = html.Div(className="w-full flex justify-center items-center")  # Wrapper to avoid multiple gauges

   
    if selected_metric == "all":
        content = html.Div(
            className="grid grid-cols-1 md:grid-cols-2 gap-6 justify-center items-center mt-10",
            children=[
                html.Div(
                    className=f"bg-gray-900 p-6 rounded-xl border-2 {style} shadow-xl transition-all duration-300 hover:shadow-lg flex flex-col items-center",
                    children=[
                        html.H2(title, className=f"text-lg font-semibold {style} mb-4"),
                        
                        # 📊 Gauge for each metric
                        dcc.Graph(
                            figure=go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=value,
                                title={'text': title, 'font': {'color': 'white'}},
                                gauge={
                                    'axis': {'range': [0, 100], 'tickcolor': 'white'},
                                    'bar': {'color': color},
                                    'bgcolor': "black",
                                    'bordercolor': "white",
                                    'steps': [
                                        {'range': [0, value], 'color': color},
                                        {'range': [value, 100], 'color': "gray"}
                                    ]
                                }
                            )).update_layout(
                                paper_bgcolor="black",
                                font={'color': 'white'},
                                margin={'t': 20, 'b': 20}
                            ),
                            config={'displayModeBar': False}
                        ),

                        # digital Metric Display
                        html.Div(
                            className="mt-4 text-center text-white text-md font-semibold",
                            children=[
                                html.P(f"📌 Current {title}: {value:.2f}%", className="mb-2"),
                                html.P("🔎 AI Insights: Optimizing performance...", className="text-gray-400 text-sm italic"),
                            ]
                        )
                    ]
                ) for title, value, style, color in metric_data.values()
            ]
        )

    # Handle Single Metric Selection
    elif selected_metric in metric_data:
        title, value, style, color = metric_data[selected_metric]

        #  Gauge for Single Metric
        gauge_figure = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title, 'font': {'color': 'white'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': 'white'},
                'bar': {'color': color},
                'bgcolor': "black",
                'bordercolor': "white",
                'steps': [
                    {'range': [0, value], 'color': color},
                    {'range': [value, 100], 'color': "gray"}
                ]
            }
        ))

        gauge_figure.update_layout(
            paper_bgcolor="black",
            font={'color': 'white'},
            margin={'t': 20, 'b': 20}
        )

        content = html.Div(
            className="flex flex-col items-center justify-center h-screen",
            children=[
                html.Div(
                    className=f"bg-gray-900 p-6 rounded-xl border-2 {style} shadow-xl transition-all duration-300 hover:shadow-lg flex flex-col items-center w-[400px]",
                    children=[
                        html.H2(title, className=f"text-lg font-semibold {style} mb-4"),
                        
                        #  Centered Gauge
                        dcc.Graph(
                            figure=gauge_figure,
                            config={'displayModeBar': False},
                            className="w-full"
                        ),

                        # Digital Metric Display
                        html.Div(
    className="mt-6 text-center text-white text-lg font-semibold",
    children=[
        html.P(f"📌 Current {title}: {value:.2f} {'%' if selected_metric in ['cpu', 'memory'] else 'MB'}", className="mb-2"),
        html.P("🔎 AI Insights: Optimizing performance...", className="text-gray-400 text-sm italic"),
    ]
)

                    ]
                )
            ]
        )

    else:
        content = html.P("Invalid metric selected. Please try again.", className="text-red-500 text-lg text-center")

    return content


if __name__ == '__main__':
    app.run(debug=True)


