/// 1.
// Search @ struct SQuestInstance
		int iStartTime;

// Add below
#if defined(ENABLE_QUEST_RENEWAL)
		BYTE bType;
		bool bIsConfirmed;
#endif

/// 2.
// Search
	typedef std::vector<SQuestInstance> TQuestInstanceContainer;

// Add below
#if defined(ENABLE_QUEST_RENEWAL)
	enum EQuestStringType
	{
		QUEST_STRING_TYPE_NORMAL,
		QUEST_STRING_TYPE_CLOCK,
		QUEST_STRING_TYPE_COUNT,
		QUEST_STRING_TYPE_MAX
	};

	enum EQuestType
	{
		QUEST_TYPE_MAIN,
		QUEST_TYPE_SUB,
		QUEST_TYPE_LEVELUP,
		QUEST_TYPE_EVENT,
		QUEST_TYPE_COLLECTION,
		QUEST_TYPE_SYSTEM,
		QUEST_TYPE_SCROLL,
		QUEST_TYPE_DAILY,
		QUEST_TYPE_UNEXPOSED,
		QUEST_TYPE_MAX
	};

	enum EQuestSkin
	{
		QUEST_SKIN_NOWINDOW,
		QUEST_SKIN_NORMAL,
		QUEST_SKIN_UNKOWN1,
		QUEST_SKIN_UNKOWN2,
		QUEST_SKIN_SCROLL,
		QUEST_SKIN_CINEMATIC,
		QUEST_SKIN_COUNT,
		QUEST_SKIN_MAX
	};
#endif

/// 3.
// Search
	void MakeQuest(DWORD dwIndex);

// Replace with
	void MakeQuest(DWORD dwIndex
#if defined(ENABLE_QUEST_RENEWAL)
		, BYTE bIndex
		, bool bIsConfirmed
#endif
	);

/// 4.
// Search
	void SetQuestIconFileName(DWORD dwIndex, const char* c_szIconFileName);

// Add below
#if defined(ENABLE_QUEST_RENEWAL)
	void SetQuestIsConfirmed(DWORD dwIndex, bool bIsConfirmed);
#endif

/// 5.
// Search
	int GetQuestCount();

// Add below
#if defined(ENABLE_QUEST_RENEWAL)
	int GetQuestButtonNoticeCount(BYTE bQuestType);
#endif

/// 6.
// Search
	bool GetQuestInstancePtr(DWORD dwArrayIndex, SQuestInstance** ppQuestInstance);

// Replace with
#if defined(ENABLE_QUEST_RENEWAL)
	bool GetQuestInstancePtr(DWORD dwQuestIndex, SQuestInstance** ppQuestInstance);
#else
	bool GetQuestInstancePtr(DWORD dwArrayIndex, SQuestInstance** ppQuestInstance);
#endif
