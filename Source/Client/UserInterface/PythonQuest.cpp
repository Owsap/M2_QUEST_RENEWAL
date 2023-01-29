/// 1.
// Search
void CPythonQuest::MakeQuest(DWORD dwIndex)

// Replace with
void CPythonQuest::MakeQuest(DWORD dwIndex
#if defined(ENABLE_QUEST_RENEWAL)
	, BYTE bType
	, bool bIsConfirmed
#endif
)

/// 2.
// Search @ void CPythonQuest::MakeQuest
	rQuestInstance.iStartTime = int(CTimer::Instance().GetCurrentSecond());

// Add below
#if defined(ENABLE_QUEST_RENEWAL)
	rQuestInstance.bType = bType;
	rQuestInstance.bIsConfirmed = bIsConfirmed;
#endif

/// 3.
// Search
int CPythonQuest::GetQuestCount()

// Add above
#if defined(ENABLE_QUEST_RENEWAL)
void CPythonQuest::SetQuestIsConfirmed(DWORD dwIndex, bool bIsConfirmed)
{
	SQuestInstance* pQuestInstance;
	if (!__GetQuestInstancePtr(dwIndex, &pQuestInstance))
		return;

	pQuestInstance->bIsConfirmed = bIsConfirmed;
}
#endif

/// 4.
// Search
int CPythonQuest::GetQuestCount()

// Add below
#if defined(ENABLE_QUEST_RENEWAL)
int CPythonQuest::GetQuestButtonNoticeCount(BYTE bQuestType)
{
	int count = 0;
	for (TQuestInstanceContainer::iterator::value_type& it : m_QuestInstanceContainer)
	{
		if (bQuestType == QUEST_TYPE_MAX)
			count += 1;
		else
			if (it.bType == bQuestType)
				count += 1;
	}
	return count;
}
#endif

/// 5.
// Search
bool CPythonQuest::GetQuestInstancePtr(DWORD dwArrayIndex, SQuestInstance** ppQuestInstance)
{
	if (dwArrayIndex >= m_QuestInstanceContainer.size())
		return false;

	*ppQuestInstance = &m_QuestInstanceContainer[dwArrayIndex];

	return true;
}

// Replace with
#if defined(ENABLE_QUEST_RENEWAL)
bool CPythonQuest::GetQuestInstancePtr(DWORD dwQuestIndex, SQuestInstance** ppQuestInstance)
{
	TQuestInstanceContainer::iterator itor = std::find_if(m_QuestInstanceContainer.begin(), m_QuestInstanceContainer.end(), FQuestInstanceCompare(dwQuestIndex));
	if (itor == m_QuestInstanceContainer.end())
		return false;

	const DWORD dwVectorIndex = std::distance(m_QuestInstanceContainer.begin(), itor);
	*ppQuestInstance = &m_QuestInstanceContainer[dwVectorIndex];
	return true;
}
#else
bool CPythonQuest::GetQuestInstancePtr(DWORD dwArrayIndex, SQuestInstance** ppQuestInstance)
{
	if (dwArrayIndex >= m_QuestInstanceContainer.size())
		return false;

	*ppQuestInstance = &m_QuestInstanceContainer[dwArrayIndex];

	return true;
}
#endif

/// 6.
// Search @ PyObject* questGetQuestData
	return Py_BuildValue("sisi", pQuestInstance->strTitle.c_str(),
		pImage,
		pQuestInstance->strCounterName.c_str(),
		pQuestInstance->iCounterValue);

// Replace with
#if defined(ENABLE_QUEST_RENEWAL)
	return Py_BuildValue("ibsisi",
		pQuestInstance->bType,
		pQuestInstance->bIsConfirmed,
		pQuestInstance->strTitle.c_str(),
		pImage,
		pQuestInstance->strCounterName.c_str(),
		pQuestInstance->iCounterValue);
#else
	return Py_BuildValue("sisi", pQuestInstance->strTitle.c_str(),
		pImage,
		pQuestInstance->strCounterName.c_str(),
		pQuestInstance->iCounterValue);
#endif

/// 7.
// Search
void initquest()

// Add above
#if defined(ENABLE_QUEST_RENEWAL)
PyObject* questGetQuestCounterData(PyObject* poSelf, PyObject* poArgs) { return Py_BuildNone(); }
PyObject* questGetQuestButtonNoticeCount(PyObject* poSelf, PyObject* poArgs)
{
	BYTE bType;
	if (!PyTuple_GetInteger(poArgs, 0, &bType))
		return Py_BadArgument();

	return Py_BuildValue("i", CPythonQuest::Instance().GetQuestButtonNoticeCount(bType));
}
#endif

/// 8.
// Search
		{ NULL, NULL, NULL },

// Add above
#if defined(ENABLE_QUEST_RENEWAL)
		{ "GetQuestCounterData", questGetQuestCounterData, METH_VARARGS },
		{ "GetQuestButtonNoticeCount", questGetQuestButtonNoticeCount, METH_VARARGS },
#endif

/// 9.
// Add to the bottom of the file above }
#if defined(ENABLE_QUEST_RENEWAL)
	PyModule_AddIntConstant(poModule, "QUEST_TYPE_MAIN", CPythonQuest::QUEST_TYPE_MAIN);
	PyModule_AddIntConstant(poModule, "QUEST_TYPE_SUB", CPythonQuest::QUEST_TYPE_SUB);
	PyModule_AddIntConstant(poModule, "QUEST_TYPE_LEVELUP", CPythonQuest::QUEST_TYPE_LEVELUP);
	PyModule_AddIntConstant(poModule, "QUEST_TYPE_EVENT", CPythonQuest::QUEST_TYPE_EVENT);
	PyModule_AddIntConstant(poModule, "QUEST_TYPE_COLLECTION", CPythonQuest::QUEST_TYPE_COLLECTION);
	PyModule_AddIntConstant(poModule, "QUEST_TYPE_SYSTEM", CPythonQuest::QUEST_TYPE_SYSTEM);
	PyModule_AddIntConstant(poModule, "QUEST_TYPE_SCROLL", CPythonQuest::QUEST_TYPE_SCROLL);
	PyModule_AddIntConstant(poModule, "QUEST_TYPE_DAILY", CPythonQuest::QUEST_TYPE_DAILY);
	PyModule_AddIntConstant(poModule, "QUEST_TYPE_UNEXPOSED", CPythonQuest::QUEST_TYPE_UNEXPOSED);
	PyModule_AddIntConstant(poModule, "QUEST_TYPE_MAX", CPythonQuest::QUEST_TYPE_MAX);

	PyModule_AddIntConstant(poModule, "QUEST_STRING_TYPE_NORMAL", CPythonQuest::QUEST_STRING_TYPE_NORMAL);
	PyModule_AddIntConstant(poModule, "QUEST_STRING_TYPE_CLOCK", CPythonQuest::QUEST_STRING_TYPE_CLOCK);
	PyModule_AddIntConstant(poModule, "QUEST_STRING_TYPE_COUNT", CPythonQuest::QUEST_STRING_TYPE_COUNT);
#endif
