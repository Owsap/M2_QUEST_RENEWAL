/// 1.
// Search @ bool NPC::OnInfo
		CQuestManager::ExecuteQuestScript(pc, quest_index, itPCQuest->second.st, itQuestScript->second.GetCode(), itQuestScript->second.GetSize());
		return true;

// Add above
#if defined(__QUEST_RENEWAL__)
		CQuestManager& rkQmgr = CQuestManager::instance();
		const LPCHARACTER c_lpCh = rkQmgr.GetCurrentCharacterPtr();
		if (c_lpCh != NULL)
		{
			char szBuf[255]{};
			snprintf(szBuf, sizeof(szBuf), "%s.%s", questName, "is_confirmed");
			c_lpCh->SetQuestFlag(string(questName) + ".is_confirmed", 1);

			if (test_server)
				sys_log(0, "NPC::OnInfo: pc (name) %s has confirmed the quest %s", c_lpCh->GetName(), questName);
		}
#endif
