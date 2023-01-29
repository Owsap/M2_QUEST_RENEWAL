/// 1.
// Search @ bool CPythonNetworkStream::RecvQuestInfoPacket
		rkQuest.DeleteQuestInstance(QuestInfo.index);

// Add below
#if defined(ENABLE_QUEST_RENEWAL)
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "DeleteQuest", Py_BuildValue("(ii)", QuestInfo.type, QuestInfo.index));
#endif

/// 2.
// Search
			rkQuest.MakeQuest(QuestInfo.index);

// Replace with
#if defined(ENABLE_QUEST_RENEWAL)
			rkQuest.MakeQuest(QuestInfo.index, QuestInfo.type, QuestInfo.is_confirmed);
#else
			rkQuest.MakeQuest(QuestInfo.index);
#endif

/// 3.
// Search
		if (c_rFlag & QUEST_SEND_COUNTER_VALUE)
			rkQuest.SetQuestCounterValue(QuestInfo.index, iCounterValue);

// Add below
#if defined(ENABLE_QUEST_RENEWAL)
		rkQuest.SetQuestIsConfirmed(QuestInfo.index, QuestInfo.is_confirmed);
#endif

/// 4.
// Search
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshQuest", Py_BuildValue("()"));

// Replace with
#if defined(ENABLE_QUEST_RENEWAL)
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshQuest", Py_BuildValue("(ii)", QuestInfo.type, QuestInfo.index));
#else
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "RefreshQuest", Py_BuildValue("()"));
#endif
