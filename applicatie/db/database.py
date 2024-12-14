import sqlite3, os
from config_laden import laad_config

def creatie_locatie_database():
	#Path maken waar de database moet komen
	config = laad_config()
	db_naam = config["database"]["naam"]
	db_locatie = config["database"]["locatie"]
	db_path = os.path.join(db_locatie, db_naam)

	if not os.path.exists(db_locatie):
		os.makedirs(db_locatie)

	return db_path

def maak_connectie():
	#Ophalen database naam en locatie om te kunnen verbinden
	db_path = creatie_locatie_database()

	#Verbinding maken met de database
	try:
		dbconnectie = sqlite3.connect(db_path)
		print("Verbonden met database")
		return dbconnectie
	except sqlite3.Error as error:
		print(f"Er deed zich een fout voor: {error}")

def verkrijg_cursor():
	#Functie om niet telkens de code te moeten herhalen om de cursor op te halen
	dbconnectie= maak_connectie()
	cursor = dbconnectie.cursor()

	return dbconnectie, cursor

def setup_database():
	dbconnectie, cursor = verkrijg_cursor()

	#Controleer of de setup al is uitgevoerd
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Entries'")
	if cursor.fetchone() is not None:
		print("Database is al ingesteld. Setup wordt overgeslagen")
		dbconnectie.close()
		return


	cursor.execute('''CREATE TABLE IF NOT EXISTS Entries (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					date DATE,
					mood INTEGER,
					note TEXT,
					emotions TEXT,
					triggers TEXT,
					successes TEXT,
					UNIQUE(date, mood))''')


	#Gegevens doorvoeren en connectie afsluiten
	dbconnectie.commit()
	print("Database setup is voltooid.")
	dbconnectie.close()