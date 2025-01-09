import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
from functies.view_entries import view_entries_all
from db.database import fetch_cursor

def fetch_dates_and_moods_all():
    dbconnectie, cursor = fetch_cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute('''SELECT entries.date, entries.mood, moodcat.color 
        FROM Entries entries
        JOIN MoodCategories moodcat
        ON entries.mood BETWEEN moodcat.min_mood AND moodcat.max_mood''')

    rows = cursor.fetchall()

    dates = [entry["date"] for entry in rows]
    moods = [entry["mood"] for entry in rows]
    colors = [entry["color"] for entry in rows]

    return dates, moods, colors


def plot_mood_over_time_all():

    dates, moods, colors = fetch_dates_and_moods_all()


    plt.figure(figsize=(10, 5))
    plt.plot(dates, moods, marker="o", label="Mood over time")
    plt.xlabel("Date")
    plt.ylabel("Mood")
    plt.title("Mood Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_mood_over_time_colorcode():
    dates, moods, colors = fetch_dates_and_moods_all()
    plt.figure(figsize=(10, 5))
    for i in range(len(dates)):
        plt.scatter(dates[i], moods[i], color=colors[i], label=f"Mood {moods[i]}" if i == 0 else "")

    plt.xlabel("Date")
    plt.ylabel("Mood")
    plt.title("Mood Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()
