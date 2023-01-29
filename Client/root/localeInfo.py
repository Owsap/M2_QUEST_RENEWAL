""" 1. """
# Search
def GetLetterImageName():
	return "season1/icon/scroll_close.tga"
def GetLetterOpenImageName():
	return "season1/icon/scroll_open.tga"
def GetLetterCloseImageName():
	return "season1/icon/scroll_close.tga"

# Add below
if app.ENABLE_QUEST_RENEWAL:
	def GetBlueLetterImageName():
		return "icon/item/scroll_close_blue.tga"
	def GetBlueLetterOpenImageName():
		return "icon/item/scroll_open_blue.tga"
	def GetBlueLetterCloseImageName():
		return "icon/item/scroll_close_blue.tga"
