struct FNVCountInterface {
    virtual void Reserved();
    virtual unsigned int GetCount();
};

struct FNVNotificationReceiver {
    virtual void Reserved00();
    virtual void Reserved01();
    virtual void Reserved02();
    virtual void Reserved03();
    virtual void Reserved04();
    virtual void Reserved05();
    virtual void Reserved06();
    virtual void Reserved07();
    virtual void Reserved08();
    virtual void Reserved09();
    virtual void Reserved10();
    virtual void Reserved11();
    virtual void Reserved12();
    virtual void Reserved13();
    virtual void Reserved14();
    virtual void Reserved15();
    virtual void Reserved16();
    virtual void Reserved17();
    virtual void Reserved18();
    virtual void Reserved19();
    virtual void Reserved20();
    virtual void Notify(int context);
};

struct FNVNotificationEntry {
    void* m_unknown00;
    void* m_unknown04;
    FNVNotificationReceiver* m_receiver;
};

struct FNVNotificationCollection {
    unsigned int m_unknown00;
    unsigned int m_unknown04;
    unsigned int m_unknown08;
    unsigned int m_unknown0c;
    unsigned int m_unknown10;
    FNVCountInterface m_countInterface;
    unsigned int m_unknown18;
    unsigned int m_unknown1c;
    unsigned int m_unknown20;
    unsigned int m_unknown24;
    unsigned int m_unknown28;
    unsigned int m_unknown2c;
    unsigned int m_unknown30;
    unsigned int m_unknown34;
    unsigned int m_unknown38;
    unsigned int m_unknown3c;
    unsigned int m_unknown40;
    FNVNotificationEntry** m_entries;
};

struct FNVNotificationOwner {
    unsigned int m_unknown00;
    unsigned int m_unknown04;
    FNVNotificationCollection* m_collection;
    void FUN_00ccf990(int context);
    void FUN_00aa0ad0(int context);
};

void FNVNotificationOwner::FUN_00ccf990(int context)
{
    unsigned int count;
    FNVNotificationCollection* collection;
    if (this && (collection = m_collection))
        count = collection->m_countInterface.GetCount();
    else
        count = 0;
    for (unsigned int index = 0; index < count; ++index) {
        if (this && m_collection) {
            FNVNotificationEntry* entry = m_collection->m_entries[index];
            if (entry) {
                FNVNotificationReceiver* receiver = entry->m_receiver;
                if (receiver)
                    receiver->Notify(context);
            }
        }
    }
    FUN_00aa0ad0(context);
}
