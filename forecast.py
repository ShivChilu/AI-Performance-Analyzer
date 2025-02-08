import pandas as pd
from prophet import Prophet

def forecast_resource_usage(filename="process_data.csv"):
    df = pd.read_csv(filename)

    if df.empty or 'cpu_percent' not in df:
        print("No data available for forecasting.")
        return

    df['timestamp'] = pd.date_range(start='2025-01-01', periods=len(df), freq='5S')
    df.rename(columns={'timestamp': 'ds', 'cpu_percent': 'y'}, inplace=True)

    model = Prophet()
    model.fit(df[['ds', 'y']])
    
    future = model.make_future_dataframe(periods=60, freq='5S')
    forecast = model.predict(future)

    forecast.to_csv("forecast_results.csv", index=False)
    print("CPU usage forecast saved.")

if __name__ == "__main__":
    forecast_resource_usage()
