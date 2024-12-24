from db.database import maak_connectie, setup_database
from functies.view_entries import view_entries_all, view_entries_lastweek
from functies.add_entries import add_entry
from functies.analyze_entries import plot_mood_over_time_all, plot_mood_over_time_colorcode



def main():
	
	setup_database()
	print("Welkom bij de mood tracker!")
	#Weergeven welke acties allemaal mogelijk zijn voor dit programma
	acties = {
    "1": ("Toon alle entries", view_entries_all),
    "2": ("Voeg entry toe", add_entry),
    "3": ("Toon entries van de laatste zeven dagen", view_entries_lastweek),
    "4": ("Test analyse", plot_mood_over_time_colorcode),
    "5": ("Maak een analyze van de entries", plot_mood_over_time_all)
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
	
	

	