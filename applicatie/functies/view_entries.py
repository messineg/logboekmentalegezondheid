import sqlite3
from db.database import fetch_cursor
from db.models import Entry, Advice

def view_entries_all():
	#Ophalen van de connectie en de cursor
	dbconnectie, cursor = fetch_cursor()
	
	#Definieer de query om code leesbaarder te maken
	query = 'SELECT * FROM Entries ORDER BY date DESC'
	
	#Ophalen van resultaten met foutafhandeling
	try:
		cursor.execute(query)
		results = cursor.fetchall()
	except sqlite3.Error as error:
		print(f"Er trad een fout op bij het ophalen van de gegevens: {error}")
	
	#Controle of er resultaten gevonden worden en tonen van deze resultaten
	if results:
		for row in results:
			entries = Entry(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
			print(entries)
	else:
		print("Er werden geen entries gevonden")
	
	return results
	#Afsluiten connectie
	dbconnectie.close()


def view_entries_lastweek():
	dbconnectie, cursor = fetch_cursor()
	try:
		query = """SELECT * FROM Entries 
                   WHERE date >= DATE('now', '-7 days') 
                   ORDER BY date DESC"""
        
		cursor.execute(query)
		results = cursor.fetchall()
    	
		if results:
			print("Entries van de laatste week:")
			for row in results:
				entries = Entry(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
				print(entries)
		else:
			print("Geen entries gevonden voor de laatste week.")
    
	except sqlite3.Error as error:
		print(f"Fout bij het ophalen van entries: {error}")
	finally:
		dbconnectie.close()
