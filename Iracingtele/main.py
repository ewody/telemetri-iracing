import irsdk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time

ir = irsdk.IRSDK()
is_reset = False

def connect():
    if not ir.is_initialized:
        ir.startup()
    if ir.is_initialized:
        print("Connecté à iRacing")

def get_telemetry():
    if ir.is_initialized and ir.is_connected:
        speed_mps = ir['Speed']  # Vitesse en mètres par seconde
        speed_kph = speed_mps * 3.6  # Conversion en km/h
        telemetry = {
            'Speed': speed_kph,
            'RPM': ir['RPM'],
            'Throttle': ir['Throttle'],
            'Brake': ir['Brake'],
            'Gear': ir['Gear']
        }
        return telemetry
    return None

def reset(event):
    global is_reset
    is_reset = True

def calculate_average_speed(data, text_box):
    if data:
        df = pd.DataFrame(data)
        average_speed = df['Speed'].mean()
        text_box.set_text(f"Vitesse moyenne: {average_speed:.2f} km/h")
    else:
        text_box.set_text("Aucune donnée disponible")

def main():
    global is_reset

    connect()
    data = []

    plt.ion()
    fig, axs = plt.subplots(3, 1, figsize=(15, 10))
    fig.suptitle('Telemetry Data')

    # Ajout du bouton Reset
    reset_ax = plt.axes([0.1, 0.92, 0.1, 0.075])
    reset_button = Button(reset_ax, 'Reset')
    reset_button.on_clicked(reset)

    # Ajout du bouton Récupération des données
    data_ax = plt.axes([0.21, 0.92, 0.2, 0.075])  # Position ajustée pour déplacer le bouton plus près du bouton Reset
    data_button = Button(data_ax, 'Récupération des données')

    # Ajout de la zone de texte pour afficher la vitesse moyenne
    avg_speed_text = plt.text(0.7, 0.95, '', transform=plt.gcf().transFigure)

    data_button.on_clicked(lambda event: calculate_average_speed(data, avg_speed_text))

    manager = plt.get_current_fig_manager()
    manager.resize(1280, 720)  # Taille de la fenêtre au démarrage

    start_time = time.time()

    while True:
        if is_reset:
            data = []
            is_reset = False
            start_time = time.time()

        telemetry = get_telemetry()
        if telemetry:
            data.append(telemetry)

            elapsed_time = time.time() - start_time
            times = range(len(data))

            df = pd.DataFrame(data)

            # Mise à jour des graphiques
            axs[0].cla()
            axs[0].plot(times, df['Speed'], label='Speed')
            axs[0].set_title('Speed')
            axs[0].set_xlabel('Time (s)')
            axs[0].set_ylabel('km/h')
            axs[0].set_ylim([0, 300])  # Limite fixe entre 0 et 300 km/h
            axs[0].set_yticks([0, 50, 100, 150, 200, 250, 300])  # Ajouter les valeurs intermédiaires
            
            # Ajouter des lignes horizontales
            for y in [50, 100, 150, 200, 250]:
                axs[0].axhline(y=y, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

            axs[1].cla()
            axs[1].plot(times, df['RPM'], label='RPM', color='orange')
            axs[1].set_title('RPM')
            axs[1].set_xlabel('Time (s)')
            axs[1].set_ylabel('RPM')
            axs[1].set_ylim([0, df['RPM'].max() + 500])

            axs[2].cla()
            axs[2].plot(times, df['Throttle'], label='Throttle', color='green')
            axs[2].plot(times, df['Brake'], label='Brake', color='red')
            axs[2].set_title('Throttle and Brake Positions')
            axs[2].set_xlabel('Time (s)')
            axs[2].set_ylabel('%')
            axs[2].legend()

            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            fig.canvas.draw()
            fig.canvas.flush_events()

        time.sleep(0.05)  # Diminuer le temps de sommeil pour améliorer la fluidité

if __name__ == "__main__":
    main()
    plt.show()
