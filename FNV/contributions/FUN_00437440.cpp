struct TopicInfoList {
    void* pItem;
    TopicInfoList* pNext;
    TopicInfoList();
};

struct FUN_00437440 : BSExtraData {
    TopicInfoList* pTopics;
    FUN_00437440();
    virtual ~FUN_00437440();
};

FUN_00437440::FUN_00437440() : BSExtraData(0x73) {
    pTopics = new TopicInfoList;
}
