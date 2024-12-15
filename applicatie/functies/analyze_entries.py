import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
from functies.view_entries import view_entries_all
from db.database import fetch_cursor

def fetch_dates_and_moods():
    dbconnectie, cursor = fetch_cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("SELECT date, mood from Entries")

    rows = cursor.fetchall()

    dates = [entry["date"] for entry in rows]
    moods = [entry["mood"] for entry in rows]

    return dates, moods


def plot_mood_over_time():

    dates, moods = fetch_dates_and_moods()


    plt.figure(figsize=(10, 5))
    plt.plot(dates, moods, marker="o", label="Mood over time")
    plt.xlabel("Date")
    plt.ylabel("Mood")
    plt.title("Mood Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()
