import sqlite3
from db.database import verkrijg_cursor

def view_entries_all():
	#Ophalen van de connectie en de cursor
	dbconnectie, cursor = verkrijg_cursor()
	
	#Definieer de query om code leesbaarder te maken
	query = 'SELECT * FROM Entries ORDER BY date DESC'
	
	#Ophalen van resultaten met foutafhandeling
	try:
		cursor.execute(query)
		resultaten = cursor.fetchall()
	except sqlite3.Error as error:
		print(f"Er trad een fout op bij het ophalen van de gegevens: {error}")
	
	#Controle of er resultaten gevonden worden en tonen van deze resultaten
	if resultaten:
		for row in resultaten:
			print(row)
	else:
		print("Er werden geen entries gevonden")
	
	#Afsluiten connectie
	dbconnectie.close()
