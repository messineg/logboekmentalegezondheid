import sqlite3, os, csv
from config_laden import load_config

def fetch_location_database():
	#Path maken waar de database moet komen
	config = load_config()
	db_name = config["database"]["name"]
	db_location = config["database"]["location"]
	db_path = os.path.join(db_location, db_name)

	if not os.path.exists(db_location):
		os.makedirs(db_location)

	return db_path

def fetch_location_advice():

	config = load_config()
	csv_name = config["advices"]["name"]
	csv_location = config["advices"]["location"]
	csv_path = os.path.join(csv_location, csv_name)

	return csv_path

def maak_connectie():
	#Ophalen database naam en locatie om te kunnen verbinden
	db_path = fetch_location_database()

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
	'''cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Entries'")
	if cursor.fetchone() is not None:
		print("Database is al ingesteld. Setup wordt overgeslagen")
		dbconnectie.close()
		return'''

	query = '''CREATE TABLE IF NOT EXISTS Entries (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					date DATE,
					mood INTEGER,
					note TEXT,
					emotions TEXT,
					triggers TEXT,
					successes TEXT,
					UNIQUE(date, mood))'''

	cursor.execute(query)


	#Gegevens doorvoeren en connectie afsluiten
	dbconnectie.commit()
	print("Database setup is voltooid.")
	load_and_insert_advice()
	dbconnectie.close()

def load_and_insert_advice():

	dbconnectie, cursor = verkrijg_cursor()

	csv_path = fetch_location_advice()

	with open(csv_path, "r") as inputbestand:
		reader = csv.reader(inputbestand)
		for row in reader:
			print(row)

	query = '''CREATE TABLE IF NOT EXISTS Advices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    min_mood INTEGER NOT NULL,
    max_mood INTEGER NOT NULL,
    advice TEXT NOT NULL)'''

	#Er moet code worden voorzien die de tabel iedere keer leegmaakt en opvult met wat er in de csv zit

	cursor.execute(query)

	dbconnectie.commit()
	print("Tabel Advices werd toegevoegd")

	dbconnectie.close()

