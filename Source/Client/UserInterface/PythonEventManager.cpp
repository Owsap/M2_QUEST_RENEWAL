/// 1.
// Search
	// HIDE_QUEST_LETTER
	case EVENT_TYPE_QUEST_BUTTON_CLOSE:
	{
		PyCallClassMemberFunc(m_poInterface, "BINARY_ClearQuest",
			Py_BuildValue("(i)", atoi(GetArgument("idx", ScriptCommand.argList))));
		break;
	}
	// END_OF_HIDE_QUEST_LETTER

// Replace with
#if !defined(ENABLE_QUEST_RENEWAL)
	// HIDE_QUEST_LETTER
	case EVENT_TYPE_QUEST_BUTTON_CLOSE:
	{
		PyCallClassMemberFunc(m_poInterface, "BINARY_ClearQuest",
			Py_BuildValue("(i)", atoi(GetArgument("idx", ScriptCommand.argList))));
		break;
	}
	// END_OF_HIDE_QUEST_LETTER
#endif
