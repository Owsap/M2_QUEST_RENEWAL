""" 1. """
# Search
	def RefreshQuest(self):
		self.interface.RefreshQuest()

# Replace with
	if app.ENABLE_QUEST_RENEWAL:
		def RefreshQuest(self, quest_type, quest_index):
			self.interface.RefreshQuest(quest_type, quest_index)

		def DeleteQuest(self, quest_type, quest_index):
			self.interface.DeleteQuest(quest_type, quest_index)
	else:
		def RefreshQuest(self):
			self.interface.RefreshQuest()
