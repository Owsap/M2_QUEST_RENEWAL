/// 1.
// Search
void initapp()

// Add above
#if defined(ENABLE_QUEST_RENEWAL)
PyObject* appGetTextLength(PyObject* poSelf, PyObject* poArgs)
{
	int iLength = 0;

	char* szString;
	if (PyTuple_GetString(poArgs, 0, &szString))
		iLength = MultiByteToWideChar(GetDefaultCodePage(), 0, szString, -1, nullptr, 0);

	return Py_BuildValue("i", iLength);
}

PyObject* appGetTextWidth(PyObject* poSelf, PyObject* poArgs)
{
	char* szString;
	if (!PyTuple_GetString(poArgs, 0, &szString))
		return Py_BuildValue("i", 0);

	const DWORD dwDefaultCodePage = GetDefaultCodePage();
	int iLength = MultiByteToWideChar(dwDefaultCodePage, 0, szString, -1, nullptr, 0);

	wchar_t* wText = (wchar_t*)_alloca(2 * iLength);

	iLength = MultiByteToWideChar(dwDefaultCodePage, 0, szString, -1, wText, iLength);

	CGraphicText* pkDefaultFont = static_cast<CGraphicText*>(DefaultFont_GetResource());
	if (!pkDefaultFont)
		return Py_BuildValue("i", 0);

	CGraphicFontTexture* pFont = pkDefaultFont->GetFontTexturePointer();
	if (!pFont)
		return Py_BuildValue("i", 0);

	float fWidth = 0.0f;
	for (int i = 0; i < iLength; ++i)
	{
		if (!wText[i])
			continue;

		CGraphicFontTexture::TCharacterInfomation* pCharacterInfomation = pFont->GetCharacterInfomation(dwDefaultCodePage, wText[i]);
		if (!pCharacterInfomation)
			continue;

		fWidth += pCharacterInfomation->advance;
	}

	return Py_BuildValue("i", (int)ceilf(fWidth));
}
#endif

/// 2.
// Search
		{ NULL, NULL },

// Add above
#if defined(ENABLE_QUEST_RENEWAL)
		{ "GetTextLength", appGetTextLength, METH_VARARGS },
		{ "GetTextWidth", appGetTextWidth, METH_VARARGS },
#endif

/// 3.
// Add to the bottom of the file above }
#if defined(ENABLE_QUEST_RENEWAL)
	PyModule_AddIntConstant(poModule, "ENABLE_QUEST_RENEWAL", 1);
#else
	PyModule_AddIntConstant(poModule, "ENABLE_QUEST_RENEWAL", 0);
#endif

#if defined(ENABLE_CLIP_MASK) || defined(__BL_CLIP_MASK__)
	PyModule_AddIntConstant(poModule, "ENABLE_CLIP_MASK", 1);
#else
	PyModule_AddIntConstant(poModule, "ENABLE_CLIP_MASK", 0);
#endif

#if defined(ENABLE_MOUSE_WHEEL_TOP_WINDOW) || defined(__BL_MOUSE_WHEEL_TOP_WINDOW__)
	PyModule_AddIntConstant(poModule, "ENABLE_MOUSE_WHEEL_TOP_WINDOW", 1);
#else
	PyModule_AddIntConstant(poModule, "ENABLE_MOUSE_WHEEL_TOP_WINDOW", 0);
#endif

#if defined(ENABLE_CONQUEROR_LEVEL)
	PyModule_AddIntConstant(poModule, "ENABLE_CONQUEROR_LEVEL", 1);
#else
	PyModule_AddIntConstant(poModule, "ENABLE_CONQUEROR_LEVEL", 0);
#endif
