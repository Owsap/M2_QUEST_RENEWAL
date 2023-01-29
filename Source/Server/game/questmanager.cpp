/// 1.
// Search
	void CQuestManager::Input(unsigned int pc, const char* msg)

// Add above
#if defined(__QUEST_RENEWAL__)
	int CQuestManager::ReadQuestCategoryFile(WORD quest_index)
	{
		// 받은 quest_index를 quest_name로 변환 후 비교
		int quest_type = 0;
		string quest_name = CQuestManager::instance().GetQuestNameByIndex(quest_index);
		ifstream file((g_stQuestDir + "/questcategory.txt").c_str());
		if (file)
		{
			std::string line;
			while (getline(file, line))
			{
				line.erase(remove(line.begin(), line.end(), ' '), line.end()); // remove all white spaces
				if (line.empty() || line.front() == '#')
					continue; // Skip empty lines or lines starting with #

				int type = stoi(line.substr(0, line.find('\t')));
				string name = line.substr(line.find('\t') + 1);

				if (test_server)
					sys_log(0, "QUEST reading script of %s(%d)", name.c_str(), type);

				if (quest_name == name)
				{
					quest_type = type;
					break;
				}
			}
		}
		else
			sys_err("QUEST Cannot open 'questcategory.txt'");

		return quest_type;
	}
#endif
