import sqlite3
from datetime import datetime
from db.database import fetch_cursor
from functies.view_entries import view_entries_all
from functies.fetch_advices import fetch_advices


def add_entry():
	dbconnectie, cursor = fetch_cursor()
	
	#DATUM INPUT
	while True:
		try:
			date_input = input("Geef de datum in (YYYY-MM-DD) ")
			if not date_input:
				print("De datum moet ingevuld worden")
				continue
			valid_date = datetime.strptime(date_input, "%Y-%m-%d")
			break
		except ValueError:
			print("Geef een geldige datum in!")

	#STEMMING INPUT
	while True:
		try:
			mood = int(input("Geef je een dag een cijfer van 0 tot 10: "))
			if 0 <= mood <= 10:
				break
			else:
				print("Het cijfer moet tussen 0 en 10 liggen")
		except ValueError:
			print("Voeg een geldig cijfer in")
	
	#NOTITIE INPUT
	while True:
		note = input("Geef een notitie in: ")
		if note:
			break
		else:
			print("Vergeet geen notitie toe te voegen")

	
	query_notes = '''INSERT INTO Entries (date, mood, note) 
						VALUES (?, ?, ?)'''
		
	try:
		cursor.execute(query_notes, (date_input, mood, note))
		dbconnectie.commit()
		print(f"Log van {date_input} werd toegevoegd.")
	except sqlite3.Error as error:
		print(f"Databasefout: {error}")	
	

	#Afsluiten van de connectie
	dbconnectie.close()

	fetch_advices(mood)

