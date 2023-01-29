""" 1. """
# Search
class CharacterWindow(ui.ScriptWindow):

# Add above
if app.ENABLE_QUEST_RENEWAL:
	__author__ = "Owsap"
	__copyright__ = "Copyright (C) 2023, Owsap Development"
	__website__ = "https://owsap.dev/"

	#
	# GitHub: https://github.com/Owsap
	# M2Dev: https://metin2.dev/profile/544-owsap/
	#

	from _weakref import proxy

	QUEST_LABEL_TAB_COLOR_IMG_DICT = {
		quest.QUEST_TYPE_MAIN : "d:/ymir work/ui/quest_re/tabcolor_1_main.tga",
		quest.QUEST_TYPE_SUB : "d:/ymir work/ui/quest_re/tabcolor_2_sub.tga",
		quest.QUEST_TYPE_LEVELUP : "d:/ymir work/ui/quest_re/tabcolor_3_levelup.tga",
		quest.QUEST_TYPE_EVENT : "d:/ymir work/ui/quest_re/tabcolor_4_event.tga",
		quest.QUEST_TYPE_COLLECTION : "d:/ymir work/ui/quest_re/tabcolor_5_collection.tga",
		quest.QUEST_TYPE_SYSTEM : "d:/ymir work/ui/quest_re/tabcolor_6_system.tga",
		quest.QUEST_TYPE_SCROLL : "d:/ymir work/ui/quest_re/tabcolor_7_scroll.tga",
		quest.QUEST_TYPE_DAILY : "d:/ymir work/ui/quest_re/tabcolor_8_daily.tga"
	}

	QUEST_LABEL_NAME_DICT = {
		quest.QUEST_TYPE_MAIN : uiScriptLocale.QUEST_UI_TEXT_MAIN,
		quest.QUEST_TYPE_SUB : uiScriptLocale.QUEST_UI_TEXT_SUB,
		quest.QUEST_TYPE_LEVELUP : uiScriptLocale.QUEST_UI_TEXT_LEVELUP,
		quest.QUEST_TYPE_EVENT : uiScriptLocale.QUEST_UI_TEXT_EVENT,
		quest.QUEST_TYPE_COLLECTION : uiScriptLocale.QUEST_UI_TEXT_COLLECTION,
		quest.QUEST_TYPE_SYSTEM : uiScriptLocale.QUEST_UI_TEXT_SYSTEM,
		quest.QUEST_TYPE_SCROLL : uiScriptLocale.QUEST_UI_TEXT_SCROLL,
		quest.QUEST_TYPE_DAILY : uiScriptLocale.QUEST_UI_TEXT_DAILY
	}

	class QuestDescObject(ui.Window):
		WIDTH = 222
		HEIGHT = 15

		DESC_TEXT_MAX_WIDTH = 130 #202

		def __init__(self, parent, quest_index, desc_data = None):
			ui.Window.__init__(self)

			self.parent = parent
			self.quest_index = quest_index
			self.desc_data = desc_data

			self.quest_text = None
			self.quest_string_type = quest.QUEST_STRING_TYPE_NORMAL

			self.SetParent(parent)

			# Contents window.
			contents_window = ui.Window()
			contents_window.SetParent(self)
			contents_window.SetSize(self.WIDTH, self.HEIGHT)
			contents_window.SetPosition(15, 0)
			contents_window.Show()
			self.contents_window = contents_window

			# Contents text line.
			contents_textline = ui.TextLine()
			contents_textline.SetParent(self.contents_window)
			contents_textline.SetText(desc_data)
			contents_textline.SetPosition(0, 0)
			contents_textline.Show()
			self.contents_textline = contents_textline

			ui.Window.Show(self)

		def __del__(self):
			ui.Window.__del__(self)

			self.parent = None
			self.quest_index = None
			self.desc_data = None

			self.quest_text = None
			self.quest_string_type = None

		def SetQuestText(self, text):
			if app.GetTextWidth(text) > self.DESC_TEXT_MAX_WIDTH:
				string = text[:self.DESC_TEXT_MAX_WIDTH] + "..."
			else:
				string = text

			self.quest_text = text
			self.contents_textline.SetText(string)

		def SetQuestStringType(self, type):
			self.quest_string_type = type

		def __UpdateQuestClock(self):
			(last_name, last_time) = quest.GetQuestLastTime(self.quest_index)

			clock_text = localeInfo.QUEST_UNLIMITED_TIME
			if len(last_name) > 0:
				if last_time <= 0:
					clock_text = localeInfo.QUEST_TIMEOVER
				else:
					second = int(last_time % 60)
					minute = int((last_time / 60) % 60)
					hour = int((last_time / 60) / 60) % 24

					clock_text = last_name + " : "

					if hour > 0:
						clock_text += str(hour) + localeInfo.QUEST_HOUR
						clock_text += " "

					if minute > 0:
						clock_text += str(minute) + localeInfo.QUEST_MIN

					if second > 0 and minute < 1:
						clock_text += str(second) + localeInfo.QUEST_SEC

			self.contents_textline.SetText(clock_text)

		def OnUpdate(self):
			if self.quest_string_type == quest.QUEST_STRING_TYPE_CLOCK:
				self.__UpdateQuestClock()

	class QuestObject(ui.Window):
		def __init__(self, parent, quest_index, is_confirmed):
			ui.Window.__init__(self)

			self.parent = parent
			self.quest_index = quest_index
			self.is_confirmed = is_confirmed

			self.desc_list = []

			self.SetParent(self.parent)
			self.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.__ClickQuest))

			# Quest line image.
			line = ui.ImageBox()
			line.LoadImage("d:/ymir work/ui/quest_re/quest_list_line_01.tga")
			line.SetParent(self)
			line.Hide()
			self.line = line

			# New quest icon.
			new_image = ui.ImageBox()
			new_image.SetParent(self)
			new_image.AddFlag("not_pick")
			new_image.SetPosition(3, 4)
			new_image.LoadImage("d:/ymir work/ui/quest_re/quest_new.tga")
			if not self.is_confirmed:
				new_image.Show()
			else:
				new_image.Hide()
			self.new_image = new_image

			ui.Window.Hide(self)

		def __del__(self):
			ui.Window.__del__(self)

			self.parent = None
			self.quest_index = 0
			self.is_confirmed = False

			self.desc_list = []

		def AddLine(self):
			if not self.desc_list:
				return

			x, y = self.desc_list[-1].GetLocalPosition()

			if self.line:
				self.line.SetPosition(4, y + 15)
				self.line.Show()

		def RemoveLine(self):
			self.line.Hide()

		def ReplaceDesc(self, desc_list):
			self.desc_list = []

			for i, desc_data in enumerate(desc_list):

				desc_object = QuestDescObject(self, self.quest_index)
				desc_object.SetQuestStringType(i)

				if i == quest.QUEST_STRING_TYPE_CLOCK:
					(clock_last_name, clock_last_time) = desc_data

					clock_text = localeInfo.QUEST_UNLIMITED_TIME
					if len(clock_last_name) > 0:
						if clock_last_time <= 0:
							clock_text = localeInfo.QUEST_TIMEOVER
						else:
							quest_last_minute = clock_last_time / 60
							quest_last_sec = clock_last_time % 60

							clock_text = clock_last_name + " : "

							if quest_last_minute > 0:
								clock_text += str(quest_last_minute) + localeInfo.QUEST_MIN
								if quest_last_sec > 0:
									clock_text += " "

							if quest_last_sec > 0:
								clock_text += str(quest_last_sec) + localeInfo.QUEST_SEC

					desc_object.SetQuestText(clock_text)
					self.desc_list.append(desc_object)

				elif i == quest.QUEST_STRING_TYPE_COUNT:
					(quest_counter_name, quest_counter_value) = desc_data

					if len(quest_counter_name) > 0:
						counter_text = ("%s : %d" % (quest_counter_name, quest_counter_value))

						desc_object.SetQuestText(counter_text)
						self.desc_list.append(desc_object)

				else:
					quest_name = desc_data

					desc_object.SetQuestText(quest_name)
					self.desc_list.append(desc_object)

		def SetPositionIndex(self, pos):
			self.quest_index = pos

		def SetConfirmed(self, is_confirmed):
			self.is_confirmed = is_confirmed
			if not self.is_confirmed:
				self.new_image.Show()
			else:
				self.new_image.Hide()

		def IsConfirmed(self):
			return self.is_confirmed

		def Arrange(self):
			y = 0
			for desc_obj in self.desc_list:
				desc_obj.SetPosition(0, y)
				y += 15 # Add space between text lines.

		def __ClickQuest(self):
			import event
			event.QuestButtonClick(-2147483648 + self.quest_index)

			# Remove new image from quest object.
			self.is_confirmed = True
			self.new_image.Hide()

			if self.parent:
				self.parent.CheckNewImage()

		def GetDescCount(self):
			return len(self.desc_list)

	class QuestCategory(ui.Window):
		BOARD_WIDTH = 222
		if app.ENABLE_CONQUEROR_LEVEL:
			BOARD_HEIGHT = 340
		else:
			BOARD_HEIGHT = 297

		TAB_WIDTH = 222
		TAB_HEIGHT = 22

		def __init__(self, clipping_mask_window, parent, quest_type):
			self.clipping_mask_window = clipping_mask_window
			self.parent = parent
			self.quest_type = quest_type

			# Category position and height.
			self.x = 0
			self.y = 0
			self.height = 0

			# Dictionary that contains all the quests of this category.
			self.quest_dict = {}

			# Check if the category is on or off.
			self.is_on = False

			ui.Window.__init__(self)

			self.SetParent(self.clipping_mask_window)
			self.SetSize(self.BOARD_WIDTH, self.BOARD_HEIGHT)

			# Name window that contains all the children.
			name_window = ui.Window()
			name_window.SetParent(self)
			name_window.SetPosition(0, 0)
			name_window.SetSize(self.TAB_WIDTH, self.TAB_HEIGHT)
			name_window.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.__ClickLabel))
			name_window.Show()
			self.name_window = name_window

			# Image of the label.
			label_image = ui.ImageBox()
			label_image.SetParent(self.name_window)
			label_image.AddFlag("not_pick")
			label_image.SetPosition(0, 0)
			label_image.SetSize(10, 10)
			label_image.LoadImage("d:/ymir work/ui/quest_re/quest_tab_01.tga")
			if localeInfo.IsARABIC():
				label_image.LeftRightReverse()
			label_image.Show()
			self.label_image = label_image

			# Opened image icon.
			opened_image = ui.ImageBox()
			opened_image.SetParent(self.name_window)
			opened_image.AddFlag("not_pick")
			if localeInfo.IsARABIC():
				opened_image.SetPosition(204, 2)
			else:
				opened_image.SetPosition(4, 2)
			opened_image.LoadImage("d:/ymir work/ui/quest_re/quest_up.tga")
			opened_image.Hide()
			self.opened_image = opened_image

			# Closed image icon.
			closed_image = ui.ImageBox()
			closed_image.SetParent(self.name_window)
			closed_image.AddFlag("not_pick")
			if localeInfo.IsARABIC():
				closed_image.SetPosition(204, 2)
			else:
				closed_image.SetPosition(4, 2)
			closed_image.LoadImage("d:/ymir work/ui/quest_re/quest_down.tga")
			closed_image.Show()
			self.closed_image = closed_image

			# Quest exist image icon.
			quest_exist_image = ui.ImageBox()
			quest_exist_image.SetParent(self.name_window)
			quest_exist_image.AddFlag("not_pick")
			if localeInfo.IsARABIC():
				quest_exist_image.SetPosition(21, 12)
			else:
				quest_exist_image.SetPosition(188, 12)
			if quest_type in QUEST_LABEL_TAB_COLOR_IMG_DICT:
				quest_exist_image.LoadImage(QUEST_LABEL_TAB_COLOR_IMG_DICT[quest_type])
				quest_exist_image.Show()
			else:
				quest_exist_image.Hide()
			self.quest_exist_image = quest_exist_image

			# Label name.
			name_textline = ui.TextLine()
			name_textline.SetParent(self.name_window)
			if localeInfo.IsARABIC():
				name_textline.SetPosition(28, 2)
				name_textline.SetWindowHorizontalAlignRight()
				name_textline.SetHorizontalAlignLeft()
			else:
				name_textline.SetPosition(24, 2)
			if quest_type in QUEST_LABEL_NAME_DICT:
				name_textline.SetText(QUEST_LABEL_NAME_DICT[quest_type])
			else:
				name_textline.SetText("")
			name_textline.SetPackedFontColor(0xffCEC6B5)
			name_textline.Show()
			self.name_textline = name_textline

			# New quest icon (green dot)
			new_image = ui.ImageBox()
			new_image.SetParent(self.name_window)
			new_image.AddFlag("not_pick")
			new_image.LoadImage("d:/ymir work/ui/quest_re/quest_new.tga")
			if quest_type in QUEST_LABEL_NAME_DICT:
				new_image.SetPosition(app.GetTextWidth(QUEST_LABEL_NAME_DICT[quest_type]) + 30, 5)
				new_image.Show()
			else:
				new_image.SetPosition(0, 0)
				new_image.Hide()
			self.new_image = new_image

			self.__HideQuestExistImage()
			self.__HideNewImage()

			ui.Window.Show(self)

		def __del__(self):
			ui.Window.__del__(self)

			self.clipping_mask_window = None
			self.parent = None
			self.quest_type = 0

			self.x = 0
			self.y = 0
			self.height = 0

			self.quest_dict = {}
			self.is_on = False

			self.name_window = None
			self.label_image = None
			self.opened_image = None
			self.closed_image = None
			self.quest_exist_image = None
			self.name_textline = None
			self.new_image = None

		def __ShowClosedImg(self):
			self.opened_image.Hide()
			self.closed_image.Show()

		def __ShowOpendImg(self):
			self.closed_image.Hide()
			self.opened_image.Show()

		def __ShowQuestExistImage(self):
			self.quest_exist_image.Show()

		def __HideQuestExistImage(self):
			self.quest_exist_image.Hide()

		def __ShowNewImage(self):
			self.new_image.Show()

		def __HideNewImage(self):
			self.new_image.Hide()

		def OpenCategory(self):
			self.__ClickLabel()

		def CloseCategory(self):
			self.is_on = False
			for key, item in self.quest_dict.items():
				item.Hide()

			self.__ShowClosedImg()
			self.__Arrange()

		# When clicking on the tab label.
		def __ClickLabel(self):
			# Prevent trying to open an empty category.
			if not self.quest_dict:
				self.is_on = False
				self.__ShowClosedImg()
				return

			if self.is_on:
				self.__ShowClosedImg()
				self.is_on = False
			else:
				self.__ShowOpendImg()
				self.is_on = True

			# Show all the quests from the category.
			for key, item in self.quest_dict.items():
				item.Show() if self.is_on else item.Hide()

			self.__Arrange()

		# Check if there are any confirmed quests in the category.
		def CheckNewImage(self):
			for key, item in self.quest_dict.items():
				if not item.IsConfirmed():
					self.__ShowNewImage()
					break

			self.__HideNewImage()

		# Replace quests in the category.
		def ReplaceQuest(self, quest_index, is_confirmed, desc_data_list):
			if not quest_index in self.quest_dict:
				quest_obj = QuestObject(self, quest_index, is_confirmed)
			else:
				quest_obj = self.quest_dict[quest_index]

			quest_obj.ReplaceDesc(desc_data_list)
			if app.ENABLE_CLIP_MASK:
				quest_obj.SetClippingMaskWindow(self.clipping_mask_window)

			if self.is_on:
				quest_obj.Show()

			self.quest_dict.update({ quest_index : quest_obj })
			if self.quest_dict:
				self.__ShowQuestExistImage()

			if not is_confirmed:
				self.__ShowNewImage()
			else:
				self.__HideNewImage()

			self.__Arrange()

		# Delete quests in the category.
		def DeleteQuest(self, quest_index):
			if quest_index in self.quest_dict:
				self.quest_dict[quest_index].Hide()
				del self.quest_dict[quest_index]

			# Check if there are any quests in the dictionary.
			if not self.quest_dict:
				self.is_on = False

				self.__ShowClosedImg()

				self.__HideNewImage()
				self.__HideQuestExistImage()

			self.__Arrange()

		# Method of arranging all the quests in the category.
		def __Arrange(self):
			y = self.TAB_HEIGHT # Initial vertical position.
			for index, (key, item) in enumerate(self.quest_dict.items()):
				quest_desc_count = item.GetDescCount() # Quest description count.
				quest_desc_height = quest_desc_count * 15 # Quest description height.
				quest_desc_height += 5 # Add and extra gap for the line separator.

				item.SetSize(self.TAB_WIDTH, quest_desc_height)
				item.SetPosition(0, y)
				item.Arrange() # Arrange the quest description text lines.

				# Add line at the penultimate quest object.
				if index < len(self.quest_dict) - 1:
					item.AddLine()
				else:
					item.RemoveLine()

				# Increase vertical position by quest description height.
				y += quest_desc_height

			# Call the parent method for arranging the category positions.
			if self.parent:
				self.parent.ChildHeightChanged(self.quest_type)

		# Unused.
		def __height_resize_post_process(self, original_function):
			pass

		def IsOn(self):
			return self.is_on

		# Returns the total height of the quest object based on
		# each quest description.
		def GetQuestObjectHeight(self):
			height = 0
			for index, (key, item) in enumerate(self.quest_dict.items()):
				height += item.GetDescCount() * 15 # Quest description height.
				height += 5 # Add and extra gap for the line separator.
			return height

		# Updates the vertical position for the scroll.
		def UpdateYPosition(self, pos):
			self.SetPosition(self.x, self.y + self.height - pos)

		def UpdatePosition(self, x, y):
			self.x = x; self.y = y
			self.SetPosition(self.x, self.y)

		def SetHeight(self, height):
			self.height = height
			self.SetPosition(self.x, self.y + self.height)

		def GetPosition(self):
			return self.x, self.y

		def GetHeight(self):
			return self.height

	class QuestCategoryGroup(ui.Window):
		LABEL_HEIGHT = 22
		SCROLL_STEP = 18
		if app.ENABLE_CONQUEROR_LEVEL:
			BOARD_HEIGHT = 340
		else:
			BOARD_HEIGHT = 297

		# The constructor method that initializes everything.
		def __init__(self, clipping_mask_window, scroll_object):
			ui.Window.__init__(self)

			self.clipping_mask_window = proxy(clipping_mask_window)

			self.scroll = scroll_object
			self.scroll.SetScrollEvent(ui.__mem_func__(self.__ScrollEvent))
			self.scroll.SetScrollStep(self.SCROLL_STEP)

			self.diff_height = 0

			# Dictionary that contains all the categories.
			self.quest_category_dict = {}
			for quest_type in QUEST_LABEL_NAME_DICT.keys():
				self.quest_category_dict[quest_type] = QuestCategory(self.clipping_mask_window, self, quest_type)
				if app.ENABLE_CLIP_MASK:
					self.quest_category_dict[quest_type].SetClippingMaskWindow(self.clipping_mask_window)

			# Arrange all the categories initial position.
			self.__Arrange()

			# Refresh the scroll for its initial position.
			self.__RefreshScroll()

		# The destructor method which is called as soon as
		# all references of the object are deleted.
		def __del__(self):
			ui.Window.__del__(self)

			self.clipping_mask_window = None
			self.scroll = None
			self.diff_height = 0

			self.quest_category_dict = {}

		# This will replace (update) any quest in a category.
		def ReplaceQuest(self, quest_type, quest_index, is_confirmed, desc_data_list):
			if quest_type in self.quest_category_dict:
				self.quest_category_dict[quest_type].ReplaceQuest(quest_index, is_confirmed, desc_data_list)

		# Delete and hide the quest from the category.
		def DeleteQuest(self, quest_type, quest_index):
			if quest_type in self.quest_category_dict:
				self.quest_category_dict[quest_type].DeleteQuest(quest_index)

		# This method is called from the QuestCategory class
		# which arranges all the category positions.
		def ChildHeightChanged(self, quest_type):
			self.__ArrangeAfter(quest_type)
			self.__AdjustScrollPos(quest_type)

		# Scroll event in which while scrolling, the categories
		# move vertical along with its children.
		def __ScrollEvent(self):
			pos = self.scroll.GetPos() * self.diff_height
			for key, item in self.quest_category_dict.items():
				item.UpdateYPosition(pos)

		# Refresh the scroll based on the category height.
		def __RefreshScroll(self):
			self.diff_height = 0

			label_height = 0; height = 0
			if app.ENABLE_CONQUEROR_LEVEL:
				reserved_height = 2
			else:
				reserved_height = 7

			for key, item in self.quest_category_dict.items():
				label_height += self.LABEL_HEIGHT - reserved_height
				is_on = item.IsOn()
				height += item.GetQuestObjectHeight() if is_on else 0

			total_height = height + label_height + 12
			if total_height >= self.BOARD_HEIGHT:
				self.diff_height = height - label_height

				step_size = float(self.SCROLL_STEP) / self.diff_height
				self.scroll.SetScrollStep(step_size)
				self.scroll.Show()
			else:
				self.scroll.Hide()

		# Unused.
		def __AdjustScrollPos(self, quest_type):
			pass

		# Arranges the categories on startup in a closed state.
		def __Arrange(self):
			for key, item in self.quest_category_dict.iteritems():
				item.UpdatePosition(0, self.LABEL_HEIGHT * key)

		# This arrangement is made when any category is clicked or
		# when any other event is made in the quest object board,
		# like updating objects or removing them.
		def __ArrangeAfter(self, quest_type):
			pos = self.scroll.GetPos() * self.diff_height
			for key, item in self.quest_category_dict.items():
				last_key = key -1; last_item = None; height = 0

				if last_key in self.quest_category_dict:
					last_item = self.quest_category_dict[key - 1]
					is_on = last_item.IsOn()
					height = last_item.GetQuestObjectHeight() if is_on else 0

				# Set the height of the category from its base y position
				# from the first arrangement "__Arrange", following up
				# its height adjustment from its neighbor categories.
				item.SetHeight(height + last_item.GetHeight() if last_item else 0)

				# Update y position for the scroll step when scrolling.
				item.UpdateYPosition(pos) 

			# Refreshing the scroll will properly set the scroll step
			# size for all categories opened or closed on the board.
			# If there is an empty space at the window then there will
			# be no need for a scroll bar.
			self.__RefreshScroll()

			# Using the scroll event will snap the last category to
			# the bottom of the board preventing empty spaces at the
			# end of the window.
			self.__ScrollEvent()

		# Method used for opening a category. (Add-on)
		def OpenCategory(self, quest_type, close_all = False):
			if close_all:
				for key, item in self.quest_category_dict.items():
					item.CloseCategory()

			if quest_type in self.quest_category_dict:
				self.quest_category_dict[quest_type].OpenCategory()

		# Method used for closing a category. (Add-on)
		def CloseCategory(self, quest_type):
			for key, item in self.quest_category_dict.items():
				item.CloseCategory()

""" 2. """
# Search @ def __Initialize
		self.questShowingStartIndex = 0
		self.questScrollBar = None
		self.questSlot = None
		self.questNameList = None
		self.questLastTimeList = None
		self.questLastCountList = None

# Replace with
		if app.ENABLE_QUEST_RENEWAL:
			self.questScrollBar = None
			self.questPageBoardWnd = None
			self.questCategoryGroup = None
		else:
			self.questShowingStartIndex = 0
			self.questScrollBar = None
			self.questSlot = None
			self.questNameList = None
			self.questLastTimeList = None
			self.questLastCountList = None

""" 3. """
# Search
		self.questShowingStartIndex = 0
		self.questScrollBar = self.GetChild("Quest_ScrollBar")
		self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.OnQuestScroll))
		self.questSlot = self.GetChild("Quest_Slot")
		for i in xrange(quest.QUEST_MAX_NUM):
			self.questSlot.HideSlotBaseImage(i)
			self.questSlot.SetCoverButton(i,\
				"d:/ymir work/ui/game/quest/slot_button_01.sub",\
				"d:/ymir work/ui/game/quest/slot_button_02.sub",\
				"d:/ymir work/ui/game/quest/slot_button_03.sub",\
				"d:/ymir work/ui/game/quest/slot_button_03.sub", True)

		self.questNameList = []
		self.questLastTimeList = []
		self.questLastCountList = []
		for i in xrange(quest.QUEST_MAX_NUM):
			self.questNameList.append(self.GetChild("Quest_Name_0" + str(i)))
			self.questLastTimeList.append(self.GetChild("Quest_LastTime_0" + str(i)))
			self.questLastCountList.append(self.GetChild("Quest_LastCount_0" + str(i)))

# Replace with
		if app.ENABLE_QUEST_RENEWAL:
			self.questScrollBar = self.GetChild("Quest_ScrollBar")
			self.questPageBoardWnd = self.GetChild("quest_object_board_window")
			self.questCategoryGroup = QuestCategoryGroup(self.questPageBoardWnd, self.questScrollBar)
		else:
			self.questShowingStartIndex = 0
			self.questScrollBar = self.GetChild("Quest_ScrollBar")
			self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.OnQuestScroll))
			self.questSlot = self.GetChild("Quest_Slot")
			for i in xrange(quest.QUEST_MAX_NUM):
				self.questSlot.HideSlotBaseImage(i)
				self.questSlot.SetCoverButton(i,\
					"d:/ymir work/ui/game/quest/slot_button_01.sub",\
					"d:/ymir work/ui/game/quest/slot_button_02.sub",\
					"d:/ymir work/ui/game/quest/slot_button_03.sub",\
					"d:/ymir work/ui/game/quest/slot_button_03.sub", True)

			self.questNameList = []
			self.questLastTimeList = []
			self.questLastCountList = []
			for i in xrange(quest.QUEST_MAX_NUM):
				self.questNameList.append(self.GetChild("Quest_Name_0" + str(i)))
				self.questLastTimeList.append(self.GetChild("Quest_LastTime_0" + str(i)))
				self.questLastCountList.append(self.GetChild("Quest_LastCount_0" + str(i)))

""" 4. """
# Search @ def __BindEvent
		self.RefreshQuest()

# Replace with
		if not app.ENABLE_QUEST_RENEWAL:
			self.RefreshQuest()

""" 5. """
# Search @ def __BindEvent
		self.questSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectQuest))

# Replace with
		if not app.ENABLE_QUEST_RENEWAL:
			self.questSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectQuest))

""" 6. """
# Search
		## Quest
		def __SelectQuest(self, slotIndex):
			questIndex = quest.GetQuestIndex(self.questShowingStartIndex+slotIndex)

			import event
			event.QuestButtonClick(-2147483648 + questIndex)

# Replace with
	if not app.ENABLE_QUEST_RENEWAL:
		## Quest
		def __SelectQuest(self, slotIndex):
			questIndex = quest.GetQuestIndex(self.questShowingStartIndex+slotIndex)

			import event
			event.QuestButtonClick(-2147483648 + questIndex)

""" 7. """
# Search
		def RefreshQuest(self):
			if self.isLoaded == 0:
				return

			questCount = quest.GetQuestCount()
			questRange = range(quest.QUEST_MAX_NUM)

			if questCount > quest.QUEST_MAX_NUM:
				self.questScrollBar.Show()
			else:
				self.questScrollBar.Hide()

			for i in questRange[:questCount]:
				(questName, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(self.questShowingStartIndex + i)

				self.questNameList[i].SetText(questName)
				self.questNameList[i].Show()
				self.questLastCountList[i].Show()
				self.questLastTimeList[i].Show()

				if len(questCounterName) > 0:
					self.questLastCountList[i].SetText("%s : %d" % (questCounterName, questCounterValue))
				else:
					self.questLastCountList[i].SetText("")

				## Icon
				self.questSlot.SetSlot(i, i, 1, 1, questIcon)

			for i in questRange[questCount:]:
				self.questNameList[i].Hide()
				self.questLastTimeList[i].Hide()
				self.questLastCountList[i].Hide()
				self.questSlot.ClearSlot(i)
				self.questSlot.HideSlotBaseImage(i)

			self.__UpdateQuestClock()

		def __UpdateQuestClock(self):
			if "QUEST" == self.state:
				# QUEST_LIMIT_COUNT_BUG_FIX
				for i in xrange(min(quest.GetQuestCount(), quest.QUEST_MAX_NUM)):
				# END_OF_QUEST_LIMIT_COUNT_BUG_FIX
					(lastName, lastTime) = quest.GetQuestLastTime(i)

					clockText = localeInfo.QUEST_UNLIMITED_TIME
					if len(lastName) > 0:
						if lastTime <= 0:
							clockText = localeInfo.QUEST_TIMEOVER
						else:
							questLastMinute = lastTime / 60
							questLastSecond = lastTime % 60

							clockText = lastName + " : "

							if questLastMinute > 0:
								clockText += str(questLastMinute) + localeInfo.QUEST_MIN
								if questLastSecond > 0:
									clockText += " "

							if questLastSecond > 0:
								clockText += str(questLastSecond) + localeInfo.QUEST_SEC

					self.questLastTimeList[i].SetText(clockText)

# Replace with
	if app.ENABLE_QUEST_RENEWAL:
		def RefreshQuest(self, quest_type, quest_index):
			if not self.isLoaded or not self.questCategoryGroup:
				return

			try:
				(quest_type, is_confirmed, quest_name, quest_icon, quest_counter_name, quest_counter_value) = quest.GetQuestData(quest_index)
				(last_clock_name, last_clock_time) = quest.GetQuestLastTime(quest_index)

				if self.questCategoryGroup:
					self.questCategoryGroup.ReplaceQuest(quest_type, quest_index, is_confirmed, [quest_name, [last_clock_name, last_clock_time], [quest_counter_name, quest_counter_value]])
			except TypeError:
				return

		def DeleteQuest(self, quest_type, quest_index):
			self.questCategoryGroup.DeleteQuest(quest_type, quest_index)

		def OpenQuestCategory(self, quest_type, close_all):
			self.questCategoryGroup.OpenCategory(quest_type, close_all)
	else:
		def RefreshQuest(self):
			if self.isLoaded == 0:
				return

			questCount = quest.GetQuestCount()
			questRange = range(quest.QUEST_MAX_NUM)

			if questCount > quest.QUEST_MAX_NUM:
				self.questScrollBar.Show()
			else:
				self.questScrollBar.Hide()

			for i in questRange[:questCount]:
				(questName, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(self.questShowingStartIndex + i)

				self.questNameList[i].SetText(questName)
				self.questNameList[i].Show()
				self.questLastCountList[i].Show()
				self.questLastTimeList[i].Show()

				if len(questCounterName) > 0:
					self.questLastCountList[i].SetText("%s : %d" % (questCounterName, questCounterValue))
				else:
					self.questLastCountList[i].SetText("")

				## Icon
				self.questSlot.SetSlot(i, i, 1, 1, questIcon)

			for i in questRange[questCount:]:
				self.questNameList[i].Hide()
				self.questLastTimeList[i].Hide()
				self.questLastCountList[i].Hide()
				self.questSlot.ClearSlot(i)
				self.questSlot.HideSlotBaseImage(i)

			self.__UpdateQuestClock()

		def __UpdateQuestClock(self):
			if "QUEST" == self.state:
				# QUEST_LIMIT_COUNT_BUG_FIX
				for i in xrange(min(quest.GetQuestCount(), quest.QUEST_MAX_NUM)):
				# END_OF_QUEST_LIMIT_COUNT_BUG_FIX
					(lastName, lastTime) = quest.GetQuestLastTime(i)

					clockText = localeInfo.QUEST_UNLIMITED_TIME
					if len(lastName) > 0:
						if lastTime <= 0:
							clockText = localeInfo.QUEST_TIMEOVER
						else:
							questLastMinute = lastTime / 60
							questLastSecond = lastTime % 60

							clockText = lastName + " : "

							if questLastMinute > 0:
								clockText += str(questLastMinute) + localeInfo.QUEST_MIN
								if questLastSecond > 0:
									clockText += " "

							if questLastSecond > 0:
								clockText += str(questLastSecond) + localeInfo.QUEST_SEC

					self.questLastTimeList[i].SetText(clockText)

""" 8. """
# Search @ def OnUpdate
		self.__UpdateQuestClock()

# Replace with
	def OnUpdate(self):
		if not app.ENABLE_QUEST_RENEWAL:
			self.__UpdateQuestClock()

""" 9. """
# Search
	def OnQuestScroll(self):
		questCount = quest.GetQuestCount()
		scrollLineCount = max(0, questCount - quest.QUEST_MAX_NUM)
		startIndex = int(scrollLineCount * self.questScrollBar.GetPos())

		if startIndex != self.questShowingStartIndex:
			self.questShowingStartIndex = startIndex
			self.RefreshQuest()

# Replace with
	if not app.ENABLE_QUEST_RENEWAL:
		def OnQuestScroll(self):
			questCount = quest.GetQuestCount()
			scrollLineCount = max(0, questCount - quest.QUEST_MAX_NUM)
			startIndex = int(scrollLineCount * self.questScrollBar.GetPos())

			if startIndex != self.questShowingStartIndex:
				self.questShowingStartIndex = startIndex
				self.RefreshQuest()

""" 10. """
# Search
	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

# Replace with
	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

		if app.ENABLE_MOUSE_WHEEL_TOP_WINDOW:
			self.SetTop()
			wndMgr.SetWheelTopWindow(self.hWnd)

""" 11. """
# Search
	def Close(self):
		if 0 != self.toolTipSkill:
			self.toolTipSkill.Hide()

		self.Hide()

# Replace with
	def Close(self):
		if 0 != self.toolTipSkill:
			self.toolTipSkill.Hide()

		self.Hide()

		if app.ENABLE_MOUSE_WHEEL_TOP_WINDOW:
			wndMgr.ClearWheelTopWindow()

""" 12. """
# Search
	def SelectSkillGroup(self, index):
		self.__SelectSkillGroup(index)

# Add below
	if app.ENABLE_MOUSE_WHEEL_TOP_WINDOW:
		def OnMouseWheelButtonUp(self):
			if "QUEST" == self.state:
				if self.questScrollBar:
					self.questScrollBar.OnUp()
					return True

			return False

		def OnMouseWheelButtonDown(self):
			if "QUEST" == self.state:
				if self.questScrollBar:
					self.questScrollBar.OnDown()
					return True

			return False
