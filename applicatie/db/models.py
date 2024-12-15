class Entry():
	def __init__(self, id, date, mood, note, emotions, triggers, successes):
		self.id = id
		self.date = date
		self.mood = mood
		self.note = note
		self.emotions = emotions
		self.triggers = triggers
		self.successes = successes

	def __str__(self):
		return f"Datum: {self.date}\nCijfer(1-10): {self.mood}\nNotitie: {self.note}"


class Advice():
	def __init__(self, id, min_mood, max_mood, advice):
		self.id = id
		self.min_mood = min_mood
		self.max_mood = max_mood
		self.advice = advice

	def __str__(self):
		 return f"- {self.advice}"