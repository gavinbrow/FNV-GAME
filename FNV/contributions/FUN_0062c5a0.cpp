struct EventCaller
{
    virtual void Invoke(void* context);
    int unk04;
    int unk08;
    int unk0c;
};

struct EventNode : EventCaller, CombatWorldStateList
{
};

struct EventCollection
{
    EventNode* FUN_00825c00();
    void FUN_0062c5a0();
};

void EventCollection::FUN_0062c5a0()
{
    EventNode* node = FUN_00825c00();
    while (node != 0) {
        node->Invoke(this);
        node = static_cast<EventNode*>(node->GetNext());
    }
}