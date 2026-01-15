# src/utils.py
import pandas as pd

def load_data(csv_file):
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()
    return df

def generate_time_slots():
    # Return all available time slots
    return ['08:00-09:00','09:00-10:00','10:00-11:00','11:00-12:00',
            '12:00-13:00','14:00-15:00','15:00-16:00']

def generate_classrooms():
    # Example classrooms: Labs and Theory rooms
    labs = [f"Lab-{i}" for i in range(1, 6)]
    theory_rooms = [f"Room-{i}" for i in range(101, 111)]
    return labs + theory_rooms
