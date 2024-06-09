import pandas as pd
import matplotlib.pyplot as plt

def plot_telemetry(file_path):
    df = pd.read_csv(file_path, names=['Speed', 'RPM'])
    plt.figure(figsize=(10, 5))
    plt.plot(df['Speed'], label='Speed')
    plt.plot(df['RPM'], label='RPM')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.title('Telemetry Data')
    plt.show()

if __name__ == "__main__":
    plot_telemetry('telemetry_data.csv')
