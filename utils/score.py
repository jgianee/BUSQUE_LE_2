from datetime import datetime

class Score:
	def __init__(self, username, game_id, points = 0, stage = 0):
		self.username = username
		self.game_id = game_id
		self.points = points
		self.stage = stage
	
	def update_score(self, points, stage):
		self.points = points
		self.stage = stage
	
	def record(self):
		self.game_id = datetime.now().strftime("%m/%d/%Y %I:%M %p")
		return self.username, self.points, self.stage, self.game_id