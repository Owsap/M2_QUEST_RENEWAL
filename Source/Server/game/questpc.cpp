/// 1.
// Search @ void PC::SendQuestInfoPakcet
		qi.flag = m_iSendToClient;

// Add below
#if defined(__QUEST_RENEWAL__)
		qi.type = CQuestManager::instance().ReadQuestCategoryFile(qi.index);

		qi.is_confirmed = false;
		const LPCHARACTER c_lpCh = CQuestManager::instance().GetCurrentCharacterPtr();
		if (c_lpCh != NULL)
			qi.is_confirmed = static_cast<bool>(c_lpCh->GetQuestFlag(m_stCurQuest + ".is_confirmed"));
#endif
