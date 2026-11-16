
struct ContactRecord {
    unsigned short flags;
    unsigned short reserved;
    void* secondInput;
    unsigned short* firstContact;
    unsigned short* secondContact;
    void* optional;
    void* owner;
    void* firstInput;
};
void __cdecl FUN_00d01900(void* handler, ContactRecord* record);
void __cdecl FUN_00d001c0(unsigned short* contact, ContactRecord* record);
struct FUN_00cfccf0_class {
    void* m_00; void* m_04; void* m_08; void* m_0c;
    void* m_10; void* m_14; void* m_18; void* m_1c;
    void* m_20; void* m_24; void* m_28; void* m_2c;
    void* m_30; void* m_34; void* m_38; void* m_3c;
    void* m_40; void* m_44; void* m_48; void* m_4c;
    void* m_50; void* m_54;
    unsigned short* m_58;
    unsigned short* m_5c;
    void FUN_00cfccf0(void* firstInput, void* secondInput);
};
void FUN_00cfccf0_class::FUN_00cfccf0(void* firstInput, void* secondInput) {
    unsigned short* first = m_58;
    unsigned short* second = m_5c;
    ContactRecord record;
    record.flags = 0xffff;
    record.secondInput = secondInput;
    record.firstContact = first;
    record.secondContact = second;
    record.owner = this;
    record.firstInput = firstInput;
    FUN_00d01900(m_0c, &record);
    if (first[0x102]) FUN_00d001c0(first, &record);
    if (second[0x102]) FUN_00d001c0(second, &record);
}
