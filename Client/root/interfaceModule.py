""" 1. """
# Add to the top of the file
if app.ENABLE_QUEST_RENEWAL:
	import quest

""" 2. """
# Search @ def MakeInterface
		self.questButtonList = []

# Add below
		if app.ENABLE_QUEST_RENEWAL:
			self.__MakeQuestButton()

""" 3. """
# Search
	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

# Replace with
	if not app.ENABLE_QUEST_RENEWAL:
		def RefreshQuest(self):
			self.wndCharacter.RefreshQuest()

""" 4. """
# Search
	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		# QUEST_LETTER_IMAGE
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())
		# END_OF_QUEST_LETTER_IMAGE

	def BINARY_RecvQuest(self, index, name, iconType, iconName):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		# QUEST_LETTER_IMAGE
		## !! 20061026.levites.Äù½ºÆ®_ÀÌ¹ÌÁö_±³Ã¼
		import item
		if "item" == iconType:
			item.SelectItem(int(iconName))
			buttonImageFileName = item.GetIconImageFileName()
		else:
			buttonImageFileName = iconName

		if localeInfo.IsEUROPE():
			if "highlight" == iconType:
				btn.SetUpVisual("locale/ymir_ui/highlighted_quest.tga")
				btn.SetOverVisual("locale/ymir_ui/highlighted_quest_r.tga")
				btn.SetDownVisual("locale/ymir_ui/highlighted_quest_r.tga")
			else:
				btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
				btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
				btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
		else:
			btn.SetUpVisual(buttonImageFileName)
			btn.SetOverVisual(buttonImageFileName)
			btn.SetDownVisual(buttonImageFileName)
			btn.Flash()
		# END_OF_QUEST_LETTER_IMAGE

		if localeInfo.IsARABIC():
			btn.SetToolTipText(name, 0, 35)
			btn.ToolTipText.SetHorizontalAlignCenter()
		else:
			btn.SetToolTipText(name, -20, 35)
			btn.ToolTipText.SetHorizontalAlignLeft()

		btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
		btn.Show()

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

		#chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.QUEST_APPEND)

	def __ArrangeQuestButton(self):
		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		## !! 20061026.levites.Äù½ºÆ®_À§Ä¡_º¸Á¤
		if self.wndParty.IsShow():
			xPos = 100 + 30
		else:
			xPos = 20

		if localeInfo.IsARABIC():
			xPos = xPos + 15

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:
			btn.SetPosition(xPos + (int(count / yCount) * 100), yPos + (count % yCount * 63))
			count += 1

			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				btn.Show()

	def __StartQuest(self, btn):
		event.QuestButtonClick(btn.index)
		self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

# Replace with
	if app.ENABLE_QUEST_RENEWAL:
		def RefreshQuest(self, quest_type, quest_index):
			self.wndCharacter.RefreshQuest(quest_type, quest_index)

			# Refresh quest button.
			self.__RefreshQuestButton()

		def DeleteQuest(self, quest_type, quest_index):
			self.wndCharacter.DeleteQuest(quest_type, quest_index)

		# Unused.
		def ShowQuestButton(self):
			pass

		def __OnClickQuestLetterButton(self, btn):
			self.OpenCharacterWindowWithState("QUEST")

			if btn.type == quest.QUEST_TYPE_EVENT:
				self.wndCharacter.OpenQuestCategory(quest.QUEST_TYPE_EVENT, True)

			self.HideAllQuestButton()
			global IsQBHide
			IsQBHide = 1

		def __MakeQuestButton(self):
			btn = uiWhisper.WhisperButton()
			btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
			btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
			btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			btn.SetEvent(ui.__mem_func__(self.__OnClickQuestLetterButton), btn)
			btn.Hide()
			btn.type = quest.QUEST_TYPE_MAX
			btn.count = 0
			self.questButtonList.append(btn)

			# Used for event quests in order to highlight it.
			btn = uiWhisper.WhisperButton()
			btn.SetUpVisual(localeInfo.GetBlueLetterImageName())
			btn.SetOverVisual(localeInfo.GetBlueLetterOpenImageName())
			btn.SetDownVisual(localeInfo.GetBlueLetterOpenImageName())
			btn.SetEvent(ui.__mem_func__(self.__OnClickQuestLetterButton), btn)
			btn.Hide()
			btn.type = quest.QUEST_TYPE_EVENT
			btn.count = 0
			self.questButtonList.append(btn)

			self.__ArrangeQuestButton()

		def __ArrangeQuestButton(self):
			screen_width = wndMgr.GetScreenWidth()
			screen_height = wndMgr.GetScreenHeight()

			x = 100 + 30 if self.wndParty.IsShow() else 20
			if localeInfo.IsARABIC():
				x += 15

			y = 170 * screen_height / 600
			y_count = (screen_height - 330) / 63

			for count, btn in enumerate(self.questButtonList):
				btn.SetPosition(x + (int(count / y_count) * 100), y + (count % y_count * 63))
				btn.SetToolTipText(str(btn.count), 0, 35)

				global IsQBHide
				if IsQBHide:
					btn.Hide()
				else:
					if btn.count > 0:
						btn.Show()

		def __RefreshQuestButton(self):
			for btn in self.questButtonList:
				btn.count = quest.GetQuestButtonNoticeCount(btn.type)
			self.__ArrangeQuestButton()
	else:
		def BINARY_ClearQuest(self, index):
			btn = self.__FindQuestButton(index)
			if 0 != btn:
				self.__DestroyQuestButton(btn)

		def RecvQuest(self, index, name):
			# QUEST_LETTER_IMAGE
			self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())
			# END_OF_QUEST_LETTER_IMAGE

		def BINARY_RecvQuest(self, index, name, iconType, iconName):
			btn = self.__FindQuestButton(index)
			if 0 != btn:
				self.__DestroyQuestButton(btn)

			btn = uiWhisper.WhisperButton()

			# QUEST_LETTER_IMAGE
			## !! 20061026.levites.Äù½ºÆ®_ÀÌ¹ÌÁö_±³Ã¼
			import item
			if "item" == iconType:
				item.SelectItem(int(iconName))
				buttonImageFileName = item.GetIconImageFileName()
			else:
				buttonImageFileName = iconName

			if localeInfo.IsEUROPE():
				if "highlight" == iconType:
					btn.SetUpVisual("locale/ymir_ui/highlighted_quest.tga")
					btn.SetOverVisual("locale/ymir_ui/highlighted_quest_r.tga")
					btn.SetDownVisual("locale/ymir_ui/highlighted_quest_r.tga")
				else:
					btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
					btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
					btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			else:
				btn.SetUpVisual(buttonImageFileName)
				btn.SetOverVisual(buttonImageFileName)
				btn.SetDownVisual(buttonImageFileName)
				btn.Flash()
			# END_OF_QUEST_LETTER_IMAGE

			if localeInfo.IsARABIC():
				btn.SetToolTipText(name, 0, 35)
				btn.ToolTipText.SetHorizontalAlignCenter()
			else:
				btn.SetToolTipText(name, -20, 35)
				btn.ToolTipText.SetHorizontalAlignLeft()

			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
			btn.Show()

			btn.index = index
			btn.name = name

			self.questButtonList.insert(0, btn)
			self.__ArrangeQuestButton()

			#chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.QUEST_APPEND)

		def __ArrangeQuestButton(self):
			screenWidth = wndMgr.GetScreenWidth()
			screenHeight = wndMgr.GetScreenHeight()

			## !! 20061026.levites.Äù½ºÆ®_À§Ä¡_º¸Á¤
			if self.wndParty.IsShow():
				xPos = 100 + 30
			else:
				xPos = 20

			if localeInfo.IsARABIC():
				xPos = xPos + 15

			yPos = 170 * screenHeight / 600
			yCount = (screenHeight - 330) / 63

			count = 0
			for btn in self.questButtonList:
				btn.SetPosition(xPos + (int(count / yCount) * 100), yPos + (count % yCount * 63))
				count += 1

				global IsQBHide
				if IsQBHide:
					btn.Hide()
				else:
					btn.Show()

		def __StartQuest(self, btn):
			event.QuestButtonClick(btn.index)
			self.__DestroyQuestButton(btn)

		def __FindQuestButton(self, index):
			for btn in self.questButtonList:
				if btn.index == index:
					return btn

			return 0

		def __DestroyQuestButton(self, btn):
			btn.SetEvent(0)
			self.questButtonList.remove(btn)
			self.__ArrangeQuestButton()

""" 5. """
# Search
	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()

# Replace with
	def ShowAllQuestButton(self):
		if app.ENABLE_QUEST_RENEWAL:
			for btn in self.questButtonList:
				if btn.count > 0:
					btn.Show()
		else:
			for btn in self.questButtonList:
				btn.Show()
