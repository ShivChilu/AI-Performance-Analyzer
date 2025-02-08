import psutil
import pandas as pd
import time

def get_process_data():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def save_data_to_csv(filename="process_data.csv"):
    while True:
        data = get_process_data()
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        time.sleep(5)  # Collect data every 5 seconds

if __name__ == "__main__":
    save_data_to_csv()
