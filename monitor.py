import psutil
import pandas as pd
import time


def calculate_phs():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_io_counters().read_bytes / (1024 * 1024) 
    network_usage = psutil.net_io_counters().bytes_sent / (1024 * 1024)  

    disk_usage = min(disk_usage / 500 * 100, 100)  
    network_usage = min(network_usage / 100 * 100, 100)  

    score = 100 - ((cpu_usage * 0.4) + (memory_usage * 0.3) + (disk_usage * 0.2) + (network_usage * 0.1))

    return max(0, min(100, score)) 


def get_process_data():
    processes = []
    phs_score = calculate_phs()

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'io_counters', 'num_threads', 'num_ctx_switches']):
        try:
            proc_info = proc.info
            io_counters = proc_info.pop('io_counters', None)
            ctx_switches = proc_info.pop('num_ctx_switches', None)

            if io_counters:
                proc_info['read_bytes'] = io_counters.read_bytes
                proc_info['write_bytes'] = io_counters.write_bytes
            else:
                proc_info['read_bytes'] = proc_info['write_bytes'] = 0

            if ctx_switches:
                proc_info['voluntary_ctx_switches'] = ctx_switches.voluntary
                proc_info['involuntary_ctx_switches'] = ctx_switches.involuntary
            else:
                proc_info['voluntary_ctx_switches'] = proc_info['involuntary_ctx_switches'] = 0
            
            proc_info['phs_score'] = phs_score  

            processes.append(proc_info)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return processes


def save_data_to_csv(filename="process_data.csv",duration=60):
    while True:
        data = get_process_data()
        df = pd.DataFrame(data)
        
        
        df['PHS_Score'] = calculate_phs()  

        df.to_csv(filename, index=False)
        time.sleep(5)  


if __name__ == "__main__":
    save_data_to_csv()
