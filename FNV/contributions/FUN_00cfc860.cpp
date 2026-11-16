// Contact-dispatch reconstruction; incorporates earlier contributor's event-callback analysis (2026-10-25).
struct ContactRecord {
    void* m_vtable;
    void* m_unknown04;
    void* m_collidable;
};
struct ContactEvent;
void __cdecl FUN_00d01900(void* collidable, ContactEvent* eventData);
void __cdecl FUN_00d001c0(ContactRecord* record, ContactEvent* eventData);

struct ContactDispatcher {
    void* m_unknown00;
    void* m_unknown04;
    void* m_unknown08;
    void* m_unknown0c;
    ContactRecord* m_first;
    ContactRecord* m_second;
    void FUN_00cfc860(void* arg1, void* arg2);
};
struct ContactEvent {
    unsigned short m_eventType;
    unsigned short m_unknown02;
    void* m_arg2;
    ContactRecord* m_first;
    ContactRecord* m_second;
    void* m_unknown10;
    ContactDispatcher* m_dispatcher;
    void* m_arg1;
};
void ContactDispatcher::FUN_00cfc860(void* arg1, void* arg2) {
    ContactRecord* first = m_first;
    void* collidable = first->m_collidable;
    ContactEvent data;
    data.m_eventType = 0xffff;
    data.m_arg2 = arg2;
    ContactRecord* second = m_second;
    data.m_dispatcher = this;
    data.m_first = first;
    data.m_second = second;
    data.m_arg1 = arg1;
    FUN_00d01900(collidable, &data);
    if (*(unsigned short*)((char*)first + 0x204) != 0)
        FUN_00d001c0(first, &data);
    if (*(unsigned short*)((char*)second + 0x204) != 0)
        FUN_00d001c0(second, &data);
}