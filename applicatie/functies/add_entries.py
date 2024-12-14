import sqlite3
from datetime import datetime
from db.database import fetch_cursor
from functies.view_entries import view_entries_all


def add_entry():
	dbconnectie, cursor = fetch_cursor()

	try:
		date_input = input("Geef de datum in (YYYY-MM-DD) ")
		valid_date = datetime.strptime(date_input, "%Y-%m-%d")
		if not date_input:
			print("De datum moet ingevuld worden")
			return
	except ValueError:
		print("Geef een geldige datum in!")

	try:
		mood = int(input("Geef je een dag een cijfer van 0 tot 10: "))
	except ValueError:
		print("Voeg een geldig cijfer in")
		return
	
	note = input("Geef een notitie in: ")
	if not note:
		print("Vergeet geen notitie toe te voegen")
		return

	
	query_notes = '''INSERT INTO Entries (date, mood, note) 
						VALUES (?, ?, ?)'''
		
	try:
		cursor.execute(query_notes, (date, mood, note))
		dbconnectie.commit()
		print(f"Log van {date} werd toegevoegd. Dit zijn de notities die op dit moment in het systeem zitten: ")
		view_entries_all()
	except sqlite3.Error as error:
		print(f"Databasefout: {error}")	
	

	#Afsluiten van de connectie
	dbconnectie.close()

def fetch_advice(date_input, mood):
	print("Hier komt de logica waar ik advies ga tonen aan de gebruiker")