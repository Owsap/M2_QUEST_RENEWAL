/// 1.
// Search @ typedef struct packet_quest_info
} TPacketGCQuestInfo;

// Add above
#if defined(ENABLE_QUEST_RENEWAL)
	BYTE type;
	bool is_confirmed;
#endif
