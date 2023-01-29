/// 1.
// Search @ struct packet_quest_info
	BYTE flag;

// Add below
#if defined(__QUEST_RENEWAL__)
	BYTE type;
	bool is_confirmed;
#endif
