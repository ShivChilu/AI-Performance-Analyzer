import pandas as pd
from sklearn.ensemble import IsolationForest

def train_anomaly_model(filename="process_data.csv"):
    df = pd.read_csv(filename)

    if df.empty or 'cpu_percent' not in df or 'memory_percent' not in df:
        print("No data available for training.")
        return None

    df.fillna(0, inplace=True)
    X = df[['cpu_percent', 'memory_percent']]

    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)

    df['anomaly'] = model.predict(X)
    df.to_csv("anomaly_results.csv", index=False)
    print("Anomaly detection completed and results saved.")

if __name__ == "__main__":
    train_anomaly_model()
