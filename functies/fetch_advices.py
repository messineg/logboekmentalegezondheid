import sqlite3
from datetime import datetime
from db.database import fetch_cursor
from db.models import Entry, Advice

def fetch_advices(mood):
	dbconnectie, cursor = fetch_cursor()

	query = '''SELECT id, min_mood, max_mood, advice 
		FROM Advices
		WHERE ? BETWEEN min_mood AND max_mood'''
	
	try:
		cursor.execute(query, (mood,))
		resultaten = cursor.fetchall()
	except sqlite3.Error as error:
		print(f"Er deed zich een error voor bij het ophalen van de gegevens: {error}")

	if resultaten:
		for row in resultaten:
			advices = Advice(row[0], row[1], row[2], row[3])
			print("Dit zijn mogelijke adviezen:")
			print(advices)
	else:
		print("Er werden geen adviezen gevonden")