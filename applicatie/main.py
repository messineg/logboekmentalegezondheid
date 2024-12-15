from db.database import maak_connectie, setup_database
from functies.view_entries import view_entries_all, view_entries_lastweek
from functies.add_entries import add_entry



def main():
	
	setup_database()

	
	#Weergeven welke acties allemaal mogelijk zijn voor dit programma
	acties = {
    "1": ("Toon alle entries", view_entries_all),
    "2": ("Voeg entry toe", add_entry),
    "3": ("Toon entries van de laatste zeven dagen", view_entries_lastweek)
	}

	print("Beschikbare acties:")
	for key, (beschrijving, _) in acties.items():
		print(f"{key}: {beschrijving}")

	#Gebruiker vragen welke actie moet worden uitgevoerd
	user_input= input("Geef een cijfer voor de functie die je wil laten uitvoeren: ")

	#Lanceren van de functie of gebruiker er op wijzen dat een geldig cijfer moet gekozen worden
	if user_input in acties:
		acties[user_input][1]()
	else:
   		print("Ongeldige keuze, probeer het opnieuw")

if __name__ == '__main__':
	
	main()
	
	

	