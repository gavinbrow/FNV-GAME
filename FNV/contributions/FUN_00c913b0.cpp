
struct Comparator {
    virtual void unused_00();
    virtual void unused_01();
    virtual void unused_02();
    virtual void unused_03();
    virtual void unused_04();
    virtual void unused_05();
    virtual void unused_06();
    virtual void unused_07();
    virtual void unused_08();
    virtual void unused_09();
    virtual void unused_0a();
    virtual void unused_0b();
    virtual void unused_0c();
    virtual void unused_0d();
    virtual void unused_0e();
    virtual void unused_0f();
    virtual void unused_10();
    virtual void unused_11();
    virtual void unused_12();
    virtual bool accepts(const void* left, const void* right);
};
struct FilterCore {
    virtual void reserved();
    virtual unsigned char* evaluate(unsigned char* answer, const void* left, const void* right);
};
struct FilterOwner {
    void* unknown_00;
    void* unknown_04;
    FilterCore core;
};
struct Pair {
    const void* left;
    const void* right;
};
struct OpPacket {
    unsigned char opcode;
    const void* left;
    const void* right;
};
struct EventSink {
    void FUN_00cf7080(const Pair* p, int action, FilterCore* core);
};
int __cdecl FUN_00cfdd70(const void*, const void*);
struct FUN_00c913b0_Class {
    void* unknown_00;
    void* unknown_04;
    void* unknown_08;
    void* unknown_0c;
    void* unknown_10;
    void* unknown_14;
    void* unknown_18;
    void* unknown_1c;
    void* unknown_20;
    void* unknown_24;
    void* unknown_28;
    void* unknown_2c;
    void* unknown_30;
    void* unknown_34;
    void* unknown_38;
    void* unknown_3c;
    void* unknown_40;
    void* unknown_44;
    void* unknown_48;
    void* unknown_4c;
    void* unknown_50;
    void* unknown_54;
    Comparator* m_comparator;
    void* unknown_5c;
    void* unknown_60;
    EventSink* m_callback;
    void* unknown_68;
    void* unknown_6c;
    void* unknown_70;
    void* unknown_74;
    void* unknown_78;
    FilterOwner* m_filter;
    void* unknown_80;
    void* unknown_84;
    void* unknown_88;
    void* unknown_8c;
    void* unknown_90;
    void* m_pending;
    void FUN_00c91160(const OpPacket* packet);
    void FUN_00c913b0(const void* left, const void* right);
};
void FUN_00c913b0_Class::FUN_00c913b0(const void* left, const void* right)
{
    OpPacket command;
    Pair pair;
    if (m_pending) {
        command.opcode = 0x13;
        command.left = left;
        command.right = right;
        FUN_00c91160(&command);
        return;
    }

    const char* a = static_cast<const char*>(left);
    const char* b = static_cast<const char*>(right);
    const void* primaryB = b + 0x24;
    const void* primaryA = a + 0x24;
    if (m_comparator->accepts(primaryA, primaryB)) {
        unsigned char answer;
        const void* secondaryB = b + 0x10;
        const void* secondaryA = a + 0x10;
        if (*m_filter->core.evaluate(&answer, secondaryA, secondaryB)) {
            if (!FUN_00cfdd70(secondaryA, secondaryB)) {
                pair.left = primaryA;
                pair.right = primaryB;
                m_callback->FUN_00cf7080(&pair, 1, m_filter ? &m_filter->core : 0);
            }
        }
    }
}
