import sqlite3
from db.database import verkrijg_cursor
from functies.view_entries import view_entries_all

'''
Dit bestand bevat alle functionaliteit om gegevens toe te voegen aan de tabel.
Bij het toevoegen van een film worden de gegevens van de film gevraagd.
Daarna is er een controle om te kijken of de opgegeven regisseur al bestaat in het systeem.
Indien niet, dan krijgt de gebruiker een melding te zien en zal de gebruiker eerst een regisseur moeten aanmaken.
Indien de regisseur wel wordt gevonden, wordt de film toegevoegd aan de database, 
en krijgt de gebruiker de lijst met alle films in het systeem te zien.
Wanneer de regisseur niet werd gevonden kan de gebruiker via het keuzemenu uit main.py kiezen om eerst de regisseur
toe te voegen. 
De gebruiker wordt gevraagd om de gegevens van de regisseur in te geven en erna wordt deze toegevoegd aan de tabel
'''

def add_entry():
	dbconnectie, cursor = verkrijg_cursor()

	#NOG TE DOEN: DATUM VALIDATIE
	date = input("Geef de datum in ")
	if not date:
		print("De datum moet ingevuld worden")
		return

	try:
		mood = int(input("Geef je een dag een cijfer van 0 tot 1: "))
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
		show_entries_all()
	except sqlite3.Error as error:
		print(f"Databasefout: {error}")	
	

	#Afsluiten van de connectie
	dbconnectie.close()
